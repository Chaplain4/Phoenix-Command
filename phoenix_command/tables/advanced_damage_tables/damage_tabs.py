import re

from phoenix_command.models.enums import AdvancedHitLocation
from phoenix_command.models.hit_result_advanced import DamageResult


class AdvancedDamageCalculator:
    # База данных таблиц
    TABLES_DATA = {
        3: {
            "epen": [0.1, 0.2, 0.3, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.4],
            "shock": {0.1: "10", 0.4: "40", 0.5: "50", 0.8: "80", 2.4: "100"},
            "organs": [
                (0.1, 0.2, "Eye", False),
                (0.2, 0.6, "Skull", False),
                (0.6, 1.8, "Brain", False),
                (1.9, 2.4, "Skull X", False)
            ],
            "dc": {
                10: ["578", "17H", "24H", "79T", "84T", "88T", "92T", "99T", "10X", "11X", "11X", "12X", "14X", "16X",
                     "18X", "21X", "23X", "24X", "24X"],
                1: ["1", "2", "3", "986", "10H", "11H", "11H", "12H", "13H", "14H", "14H", "15H", "17H", "19H", "22H",
                    "26H", "29H", "30H", "30H"]
            }
        },
        4: {
            "epen": [0.1, 0.2, 0.3, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.5, 0.6, 0.7, 0.8, 1.1, 1.9, 2.0, 2.1, 2.2, 2.5,
                     3.3, 3.4, 3.5],
            "shock": {0.1: "10", 1.1: "55", 1.9: "410"},
            "organs": [
                (0.0, 0.1, "Teeth", False),
                (0.1, 0.5, "Mouth", False),
                (0.5, 1.1, "Throat", False),
                (1.9, 3.5, "Spine", True)  # Gray zone starts at 1.9
            ],
            "dc": {
                10: ["13", "36", "80", "80", "80", "80", "80", "80", "80", "80", "398", "917", "16H", "20H", "24H",
                     "29H", "36K", "12T", "16T", "18T", "18T", "18T", "18T"],
                1: ["1", "1", "2", "3", "3", "4", "45", "154", "204", "220", "223", "227", "230"]
                # Simplified for example
            }
        }
    }

    @classmethod
    def calculate_damage(cls, location: AdvancedHitLocation, dc: int, epen: float, is_front: bool) -> DamageResult:
        # Извлекаем номера таблиц из строки Enum, например "Eye - Nose (Table 3)" -> [3]
        table_numbers = [int(n) for n in re.findall(r'Table (\d+)', location.value)]
        final_res = DamageResult(location=location)
        for t_num in table_numbers:
            if t_num not in cls.TABLES_DATA:
                continue
            data = cls.TABLES_DATA[t_num]
            thresholds = data["epen"]
            # Находим индекс пробития
            last_idx = -1
            for i, val in enumerate(thresholds):
                if epen >= val:
                    last_idx = i
                else:
                    break
            if is_front:
                # 1. Урон
                val_str = data["dc"][dc][last_idx] if last_idx >= 0 else "0"
                final_res.damage += cls.parse_val(val_str)

                # 2. Органы и Шок по пути
                for i in range(last_idx + 1):
                    current_threshold = thresholds[i]
                    # Органы
                    for start, end, name, is_gray in data["organs"]:
                        if start <= current_threshold <= end:
                            if name not in final_res.pierced_organs:
                                final_res.pierced_organs.append(name)
                            if is_gray: final_res.is_disabled = True
                    # Шок (берем максимальный встреченный)
                    if current_threshold in data["shock"]:
                        final_res.shock = max(final_res.shock, cls.parse_val(data["shock"][current_threshold]))

                # 3. Избыточный EPEN (только для последней таблицы или если пробило навылет)
                final_res.excess_epen = max(0.0, epen - thresholds[-1])

            else:
                # Логика REAR: Максимальный урон минус значение в точке остановки
                max_idx = len(thresholds) - 1
                max_val = cls.parse_val(data["dc"][dc][max_idx])

                # Точка остановки сзади (инверсия)
                stop_idx = max_idx - (last_idx + 1)
                val_at_stop = cls.parse_val(data["dc"][dc][stop_idx]) if stop_idx >= 0 else 0

                final_res.damage += (max_val - val_at_stop)
                # (Логика органов для Rear инвертируется по аналогии)

        return final_res

    @staticmethod
    def parse_val(val: str) -> int:
        if not val or val == '-': return 0
        multipliers = {'H': 100, 'K': 1000, 'T': 10000, 'X': 100000, 'M': 1000000}
        val = val.strip()
        suffix = val[-1]
        if suffix in multipliers:
            return int(float(val[:-1]) * multipliers[suffix])
        return int(val)