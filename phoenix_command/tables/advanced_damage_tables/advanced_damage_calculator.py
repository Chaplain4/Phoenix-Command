import re

from phoenix_command.models.enums import AdvancedHitLocation
from phoenix_command.models.hit_result_advanced import DamageResult
from phoenix_command.tables.advanced_damage_tables.tables_data import TablesData


class AdvancedDamageCalculator:
    @classmethod
    def calculate_damage(
            cls,
            location: AdvancedHitLocation,
            dc: int,
            epen: float,
            is_front: bool,
    ) -> DamageResult:
        table_references: list[int | str] = []
        if '(' in location.value:
            for part in location.value.split('(')[-1].rstrip(')').split('&'):
                part = part.strip()
                if part == 'Weapon':
                    table_references.append('Weapon')
                else:
                    m = re.search(r'\d+', part)
                    if m:
                        table_references.append(int(m.group()))

        final_res = DamageResult(location=location)
        current_epen = epen

        # For rear shots, process tables in reverse order
        if not is_front:
            table_references = list(reversed(table_references))

        for ref in table_references:
            if ref == 'Weapon':
                # Weapon requires 10 EPEN to fully penetrate
                if current_epen > 0:
                    final_res.weapon_damaged = True
                    # Subtract weapon's EPEN requirement
                    current_epen = max(0.0, current_epen - 10.0)
                continue

            data = TablesData.TABLES_DATA.get(ref)
            if not data:
                continue

            thresholds = data["epen"]
            dc_values = data["dc"].get(dc)
            if not dc_values:
                continue

            final_res.excess_epen = 0.0
            if is_front:
                cls._process_front_shot(
                    data, thresholds, dc_values, current_epen, final_res
                )
            else:
                cls._process_rear_shot(
                    data, thresholds, dc_values, current_epen, final_res
                )

            current_epen = final_res.excess_epen

        return final_res

    @classmethod
    def _process_front_shot(cls, data: dict, thresholds: list[float], dc_values: list[str],
                           epen: float, final_res: DamageResult) -> None:
        """Process shot from front (left to right)."""
        penetration_idx = max(
            (i for i, t in enumerate(thresholds) if epen >= t),
            default=-1,
        )

        if penetration_idx >= 0:
            final_res.damage += cls.parse_val(dc_values[penetration_idx])

        # Collect organs and max shock for this table
        table_max_shock = 0
        for threshold_idx in range(penetration_idx + 1):
            # Collect organs
            cls._collect_organs(data, thresholds, threshold_idx, final_res, is_front=True)

            # Track max shock within this table
            current_threshold = thresholds[threshold_idx]
            if current_threshold in data["shock"]:
                shock_val = cls.parse_val(data["shock"][current_threshold])
                table_max_shock = max(table_max_shock, shock_val)

        # Add this table's max shock to total
        final_res.shock += table_max_shock

        # Excess EPEN if passed through completely
        if penetration_idx == len(thresholds) - 1:
            final_res.excess_epen = max(0.0, epen - thresholds[-1])

    @classmethod
    def _process_rear_shot(cls, data: dict, thresholds: list[float], dc_values: list[str],
                          epen: float, final_res: DamageResult) -> None:
        """Process shot from rear (right to left)."""
        max_idx = len(thresholds) - 1
        max_threshold = thresholds[max_idx]
        stop_threshold = max_threshold - epen

        # Find where bullet stops
        stop_idx = next((idx for idx in range(max_idx, -1, -1) if thresholds[idx] <= stop_threshold), -1)

        # Calculate damage
        max_val = cls.parse_val(dc_values[max_idx])
        if stop_idx >= 0:
            final_res.damage += max_val - cls.parse_val(dc_values[stop_idx])
        else:
            final_res.damage += max_val
            final_res.excess_epen = epen - max_threshold

        # Collect organs along the path
        for threshold_idx in range(max_idx, stop_idx, -1):
            cls._collect_organs(data, thresholds, threshold_idx, final_res, is_front=False)

        # Calculate shock for this table and add to total
        cls._calculate_rear_shock(data, thresholds, stop_idx, final_res)

    @classmethod
    def _collect_organs(cls, data: dict, thresholds: list[float], threshold_idx: int,
                       final_res: DamageResult, is_front: bool) -> None:
        """Collect organs at a threshold."""
        current_threshold = thresholds[threshold_idx]

        # Add organs when entering their boundary
        for start, end, name, is_gray in data["organs"]:
            boundary = start if is_front else end
            if current_threshold == boundary:
                final_res.pierced_organs.append(name)
                if is_gray:
                    final_res.is_disabled = True

    @classmethod
    def _calculate_rear_shock(cls, data: dict, thresholds: list[float], stop_idx: int,
                             final_res: DamageResult) -> None:
        """Calculate shock for rear shot: max shock - max unreached shock, and add to total."""
        max_shock = max((cls.parse_val(data["shock"][t]) for t in thresholds if t in data["shock"]), default=0)
        max_unreached = max((cls.parse_val(data["shock"][thresholds[i]])
                            for i in range(stop_idx + 1) if thresholds[i] in data["shock"]), default=0)
        table_shock = max(0, max_shock - max_unreached)
        final_res.shock += table_shock

    @staticmethod
    def parse_val(val: str) -> int:
        if not val or val == '-':
            return 0
        multipliers = {'H': 100, 'K': 1000, 'T': 10000, 'X': 100000, 'M': 1000000}
        val = val.strip()
        suffix = val[-1]
        if suffix in multipliers:
            return int(float(val[:-1]) * multipliers[suffix])
        return int(val)