import re

from phoenix_command.models.enums import AdvancedHitLocation
from phoenix_command.models.hit_result_advanced import DamageResult


class AdvancedDamageCalculator:
    # Damage tables database
    TABLES_DATA = {
        1: {
            "epen": [0.1, 0.2, 0.3, 0.4, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3],
            "shock": {0.6: "10", 0.9: "20"},  # Shock values added
            "organs": [
                (0.1, 0.2, "Scalp", False),
                (0.2, 1.2, "Skull Bone", False),
                (1.2, 1.3, "Scalp", False)
            ],
            "dc": {
                10: ["164", "423", "783", "12H", "18H", "24H", "31H", "39H", "48H", "58H", "76H", "84H"],
                9: ["76", "197", "364", "576", "830", "11H", "15H", "18H", "22H", "27H", "36H", "39H"],
                8: ["35", "90", "166", "263", "379", "514", "666", "835", "10H", "12H", "16H", "18H"],
                7: ["20", "51", "94", "148", "214", "289", "375", "471", "576", "690", "914", "10H"],
                6: ["8", "22", "40", "64", "92", "124", "161", "202", "247", "296", "392", "433"],
                5: ["6", "15", "27", "43", "61", "83", "108", "135", "165", "198", "263", "289"],
                4: ["3", "9", "16", "25", "37", "50", "64", "81", "99", "118", "156", "172"],
                3: ["2", "4", "8", "12", "18", "24", "31", "39", "47", "57", "75", "83"],
                2: ["1", "1", "2", "4", "5", "7", "9", "11", "14", "16", "22", "24"],
                1: ["1", "1", "1", "1", "1", "2", "3", "3", "4", "5", "6", "7"]
            }
        },
        2: {
            "epen": [0.4, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.8, 3.2],
            "shock": {0.4: "10", 0.7: "20", 3.2: "40"},
            "organs": [
                (0.4, 0.7, "Skull", False),
                (0.7, 2.5, "Brain", False),
                (2.8, 3.2, "Skull", False)
            ],
            "dc": {
                10: ["22", "29K", "20T", "72T", "74T", "79T", "83T", "88T", "93T", "98T", "10X", "11X", "11X", "12X", "12X", "13X", "13X", "14X", "14X", "15X", "15X", "15X"],
                9: ["15", "19K", "13T", "47T", "49T", "52T", "55T", "58T", "62T", "65T", "66T", "70T", "73T", "77T", "81T", "84T", "86T", "90T", "94T", "96T", "96T", "97T"],
                8: ["9", "11K", "79K", "28T", "29T", "31T", "32T", "34T", "36T", "38T", "39T", "41T", "43T", "45T", "48T", "50T", "51T", "53T", "56T", "57T", "57T", "57T"],
                7: ["5", "65H", "46K", "16T", "17T", "18T", "19T", "20T", "21T", "22T", "23T", "24T", "25T", "26T", "28T", "29T", "29T", "31T", "32T", "33T", "33T", "33T"],
                6: ["2", "28H", "20K", "69K", "71K", "76K", "80K", "85K", "90K", "95K", "97K", "10T", "11T", "11T", "12T", "12T", "13T", "13T", "14T", "14T", "14T", "14T"],
                5: ["1", "19H", "13K", "46K", "48K", "51K", "54K", "57K", "60K", "63K", "65K", "68K", "71K", "75K", "79K", "82K", "84K", "88K", "92K", "94K", "95K", "95K"],
                4: ["1", "11H", "78H", "28K", "28K", "30K", "32K", "34K", "36K", "38K", "39K", "41K", "43K", "45K", "47K", "49K", "50K", "53K", "55K", "56K", "56K", "56K"],
                3: ["1", "539", "38H", "13K", "14K", "15K", "15K", "16K", "17K", "18K", "19K", "20K", "21K", "22K", "23K", "24K", "24K", "25K", "27K", "27K", "27K", "27K"],
                2: ["1", "155", "11H", "38H", "39H", "42H", "44H", "50H", "52H", "53H", "56H", "62H", "65H", "68H", "69H", "73H", "76H", "78H", "78H", "78H", "78H", "78H"],
                1: ["1", "44", "310", "11H", "11H", "12H", "13H", "13H", "14H", "15H", "15H", "16H", "17H", "18H", "19H", "20H", "20H", "21H", "22H", "22H", "22H", "22H"]
            }
        },
    }

    @classmethod
    def calculate_damage(cls, location: AdvancedHitLocation, dc: int, epen: float, is_front: bool) -> DamageResult:
        """
        Calculates damage from a hit.

        Args:
            location: Hit location
            dc: Damage Class (ammunition damage class)
            epen: Effective Penetration (effective penetration value)
            is_front: True if shot from front, False if from rear

        Returns:
            DamageResult with information about damage, shock, pierced organs, etc.
        """
        table_numbers = re.findall(r'S?\d+', location.value.split('(Table')[-1] if 'Table' in location.value else '')
        final_res = DamageResult(location=location)

        for t_num_str in table_numbers:
            # Try to convert to int for numeric tables, skip if alphanumeric (S-tables not yet implemented)
            try:
                t_num = int(t_num_str)
            except ValueError:
                # Skip S-tables (S1, S24, etc.) as they are not yet in TABLES_DATA
                continue

            if t_num not in cls.TABLES_DATA:
                continue

            data = cls.TABLES_DATA[t_num]
            thresholds: list[float] = data["epen"]
            dc_values: list[str] | None = data["dc"].get(dc)

            if not dc_values:
                continue

            # Find last threshold the bullet overcame
            penetration_idx = -1
            for idx, threshold_value in enumerate(thresholds):
                if epen >= threshold_value:
                    penetration_idx = idx

            if is_front:
                cls._process_front_shot(data, thresholds, dc_values, penetration_idx, epen, final_res)
            else:
                cls._process_rear_shot(data, thresholds, dc_values, penetration_idx, epen, final_res)

        return final_res

    @classmethod
    def _process_front_shot(cls, data: dict, thresholds: list[float], dc_values: list[str],
                           penetration_idx: int, epen: float, final_res: DamageResult) -> None:
        """Process shot from front (left to right)."""
        if penetration_idx >= 0:
            final_res.damage += cls.parse_val(dc_values[penetration_idx])

        # Collect organs and shock along the path
        for threshold_idx in range(penetration_idx + 1):
            cls._collect_organs_and_shock(data, thresholds, threshold_idx, final_res, is_front=True)

        # Excess EPEN if passed through completely
        if penetration_idx == len(thresholds) - 1:
            final_res.excess_epen = max(0.0, epen - thresholds[-1])

    @classmethod
    def _process_rear_shot(cls, data: dict, thresholds: list[float], dc_values: list[str],
                          penetration_idx: int, epen: float, final_res: DamageResult) -> None:
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
            cls._collect_organs_and_shock(data, thresholds, threshold_idx, final_res, is_front=False)

        # Calculate shock: max shock - max unreached shock
        cls._calculate_rear_shock(data, thresholds, stop_idx, final_res)

    @classmethod
    def _collect_organs_and_shock(cls, data: dict, thresholds: list[float], threshold_idx: int,
                                  final_res: DamageResult, is_front: bool) -> None:
        """Collect organs and shock at a threshold."""
        current_threshold = thresholds[threshold_idx]

        # Add organs when entering their boundary
        for start, end, name, is_gray in data["organs"]:
            boundary = start if is_front else end
            if current_threshold == boundary:
                final_res.pierced_organs.append(name)
                if is_gray:
                    final_res.is_disabled = True

        # Collect shock (only for front shots, rear uses different logic)
        if is_front and current_threshold in data["shock"]:
            shock_val = cls.parse_val(data["shock"][current_threshold])
            final_res.shock = max(final_res.shock, shock_val)

    @classmethod
    def _calculate_rear_shock(cls, data: dict, thresholds: list[float], stop_idx: int,
                             final_res: DamageResult) -> None:
        """Calculate shock for rear shot: max shock - max unreached shock."""
        max_shock = max((cls.parse_val(data["shock"][t]) for t in thresholds if t in data["shock"]), default=0)
        max_unreached = max((cls.parse_val(data["shock"][thresholds[i]])
                            for i in range(stop_idx + 1) if thresholds[i] in data["shock"]), default=0)
        final_res.shock = max(0, max_shock - max_unreached)

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