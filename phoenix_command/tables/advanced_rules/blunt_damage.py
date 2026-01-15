from phoenix_command.models.enums import AdvancedHitLocation


class Table9ABluntDamage:

    @classmethod
    def get_blunt_damage(cls, location: AdvancedHitLocation, bpf: int, pen: float) -> int:
        if bpf > 10:
            return 0
        bpf = max(1, bpf)
        bpf_idx = 10 - bpf
        def parse_val(val):
            if val == "-": return 0
            if isinstance(val, int): return val
            if "H" in val: return int(val.replace("H", "")) * 100
            if "K" in val: return int(val.replace("K", "")) * 1000
            return int(val)

        # Данные таблиц разделены по локациям
        if location in (AdvancedHitLocation.HEAD_GLANCE,
                        AdvancedHitLocation.SKULL_SIDE,
                        AdvancedHitLocation.FOREHEAD,
                        AdvancedHitLocation.FOREHEAD_SIDE,
                        AdvancedHitLocation.EYE_NOSE,
                        AdvancedHitLocation.EYE_SIDE,
                        AdvancedHitLocation.MOUTH,
                        AdvancedHitLocation.JAW_SIDE,
                        AdvancedHitLocation.NECK_FLESH,
                        AdvancedHitLocation.NECK_THROAT,
                        AdvancedHitLocation.BASE_OF_SKULL_SIDE,
                        AdvancedHitLocation.NECK_THROAT_SIDE,
                        AdvancedHitLocation.NECK_SPINE_SIDE,
                        AdvancedHitLocation.HEART_RIB_SIDE,
                        AdvancedHitLocation.HEART_SIDE,
                        AdvancedHitLocation.HEART):
            data = {
                1: ["-", "-", "-", "-", "-", "-", "-", "-", 1, 1],
                2: ["-", "-", "-", "-", "-", "-", "-", 1, 2, 8],
                3: ["-", "-", "-", "-", "-", "-", "-", 1, 40, 64],
                4: ["-", "-", "-", "-", "-", "-", "-", 14, 87, "1H"],
                5: ["-", "-", "-", "-", "-", "-", "-", 56, "2H", "3H"],
                6: ["-", "-", "-", "-", "-", "-", "-", 84, "3H", "5H"],
                7: ["-", "-", "-", "-", "-", "-", "-", "1H", "5H", "8H"],
                8: ["-", "-", "-", "-", "-", "-", "-", "2H", "8H", "1K"],
                10: ["-", "-", "-", "-", "-", "-", "-", "4H", "1K", "2K"],
                12: ["-", "-", "-", "-", "-", "-", "-", "7H", "2K", "3K"],
                14: ["-", "-", "-", "-", "-", "-", "-", "1K", "2K", "3K"],
                16: ["-", "-", "-", "-", "-", "-", "-", "2K", "3K", "4K"],
                20: ["-", "-", "-", "-", "-", 1, 1, "3K", "5K", "6K"],
                30: ["-", "-", "-", 1, 1, 1, 2, "4K", "6K", "10K"],
                50: [1, 1, 1, 2, 2, 2, 3, "5K", "7K", "12K"],
                70: [1, 1, 2, 2, 3, 4, 4, "6K", "12K", "18K"],
                90: [1, 2, 2, 3, 4, 5, "3K", "7K", "14K", "21K"]
            }

        elif location in (
                AdvancedHitLocation.LUNG_RIB,
                AdvancedHitLocation.LUNG,
                AdvancedHitLocation.LIVER_RIB,
                AdvancedHitLocation.LIVER,
                AdvancedHitLocation.STOMACH_RIB,
                AdvancedHitLocation.STOMACH,
                AdvancedHitLocation.STOMACH_SPLEEN,
                AdvancedHitLocation.STOMACH_KIDNEY,
                AdvancedHitLocation.LIVER_KIDNEY,
                AdvancedHitLocation.LIVER_SPINE,
                AdvancedHitLocation.INTESTINES,
                AdvancedHitLocation.SPINE,
                AdvancedHitLocation.PELVIS,
                AdvancedHitLocation.LUNG_SIDE,
                AdvancedHitLocation.LUNG_RIB_SIDE,
                AdvancedHitLocation.SPINE_SIDE,
                AdvancedHitLocation.STOMACH_LIVER_RIB_SIDE,
                AdvancedHitLocation.STOMACH_LIVER_SIDE,
                AdvancedHitLocation.SPLEEN_LIVER_SIDE,
                AdvancedHitLocation.KIDNEY_SPINE_SIDE,
                AdvancedHitLocation.INTESTINES_SIDE,
                AdvancedHitLocation.INTESTINES_SPINE_SIDE,
                AdvancedHitLocation.PELVIS_SIDE
        ):
            data = {
                1: ["-", "-", "-", "-", "-", "-", "-", 1, 1, 1],
                2: ["-", "-", "-", "-", "-", "-", "-", 1, 2, 3],
                3: ["-", "-", "-", "-", "-", "-", "-", 2, 5, 7],
                4: ["-", "-", "-", "-", "-", "-", "-", 4, 10, 15],
                5: ["-", "-", "-", "-", "-", "-", "-", 6, 17, 23],
                6: ["-", "-", "-", "-", "-", "-", "-", 10, 26, 36],
                7: ["-", "-", "-", "-", "-", "-", 1, 14, 37, 54],
                8: ["-", "-", "-", "-", "-", "-", 1, 18, 53, "-"],
                10: ["-", "-", "-", "-", "-", "-", 1, 1, 31, 93],
                12: ["-", "-", "-", "-", "-", 1, 1, 1, 49, "1H"],
                14: ["-", "-", "-", "-", 1, 1, 1, 1, 72, "-"],
                16: ["-", "-", "-", "-", 1, 1, 1, 1, "1H", "-"],
                20: ["-", "-", "-", 1, 1, 1, 1, 1, "2H", "-"],
                30: [1, 1, 1, 1, 1, 2, 2, "-", "-", "-"],
                50: [1, 1, 2, 2, 2, 3, 4, "-", "-", "-"],
                70: [1, 2, 2, 3, 3, 4, 5, "-", "-", "-"],
                90: [2, 2, 3, 3, 3, 5, 7, "-", "-", "-"]
            }
        else:  # LIMBS
            data = {
                1: ["-", "-", "-", "-", "-", "-", "-", 1, 1, 1],
                2: ["-", "-", "-", "-", "-", "-", "-", 1, 2, 3],
                3: ["-", "-", "-", "-", "-", "-", "-", 2, 5, 7],
                4: ["-", "-", "-", "-", "-", "-", "-", 4, 10, 14],
                5: ["-", "-", "-", "-", "-", "-", "-", 6, 16, 24],
                6: ["-", "-", "-", "-", "-", "-", "-", 10, 24, 35],
                7: ["-", "-", "-", "-", "-", "-", "-", 14, 34, 50],
                8: ["-", "-", "-", "-", "-", "-", "-", 18, 46, 67],
                10: ["-", "-", "-", "-", "-", "-", "-", 1, 30, 74],
                12: ["-", "-", "-", "-", "-", "-", "-", 1, 38, "1H"],
                14: ["-", "-", "-", "-", "-", 1, 1, 1, 46, "-"],
                16: ["-", "-", "-", "-", "-", 1, 1, 1, 55, "-"],
                20: ["-", "-", "-", "-", 1, 1, 1, 1, "-", "-"],
                30: ["-", "-", "-", 1, 1, 1, 1, 2, "-", "-"],
                50: [1, 1, 1, 1, 2, 2, 3, "-", "-", "-"],
                70: [1, 1, 1, 2, 2, 3, 4, "-", "-", "-"],
                90: [1, 1, 2, 2, 3, 3, 5, "-", "-", "-"]
            }
        sorted_keys = sorted(data.keys())
        if pen >= sorted_keys[-1]:
            return parse_val(data[sorted_keys[-1]][bpf_idx])
        if pen <= sorted_keys[0]:
            return parse_val(data[sorted_keys[0]][bpf_idx])
        if pen in data:
            return parse_val(data[pen][bpf_idx])
        x0 = max(k for k in sorted_keys if k < pen)
        x1 = min(k for k in sorted_keys if k > pen)
        y0 = parse_val(data[x0][bpf_idx])
        y1 = parse_val(data[x1][bpf_idx])
        res = y0 + (pen - x0) * (y1 - y0) / (x1 - x0)
        return round(res)
