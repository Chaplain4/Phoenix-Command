from phoenix_command.models.enums import WeaponType, SituationStanceModifier4B


class EffectiveMinimumArc:
    COLUMNS = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    DATA = {
        "rifle_standing": [0.5, 0.7, 1, 1, 1, 2, 2, 2, 2, 5, 7, 10, 12, 14, 17, 19, 22, 24, 26, 29, 31, 34, 36],
        "rifle_kneeling": [0.4, 0.5, 0.7, 0.9, 1, 1, 1, 2, 2, 4, 5, 7, 9, 11, 13, 14, 16, 18, 20, 22, 23, 25, 27],
        "rifle_prone": [0.2, 0.3, 0.4, 0.5, 0.5, 0.6, 0.7, 0.8, 0.9, 2, 3, 4, 5, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
        "mg_standing": [0.8, 1, 2, 2, 2, 3, 3, 3, 4, 8, 11, 15, 19, 23, 26, 30, 34, 38, 41, 45, 49, 53, 56],
        "mg_kneeling": [0.6, 0.8, 1, 1, 2, 2, 2, 3, 3, 6, 8, 11, 14, 17, 20, 22, 25, 28, 31, 34, 36, 39, 42],
        "mg_hip": [0.3, 0.5, 0.6, 0.8, 1, 1, 1, 1, 2, 3, 5, 6, 8, 10, 11, 13, 14, 16, 18, 19, 21, 22, 24],
        "str_3_8": [0.3, 0.4, 0.5, 0.7, 0.8, 0.9, 1, 1, 1, 3, 4, 5, 7, 8, 9, 10, 12, 13, 14, 16, 17, 18, 20],
        "str_12_15": [0.2, 0.3, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 2, 3, 3, 4, 5, 6, 7, 8, 9, 9, 10, 11, 12, 13],
        "str_16_18": [0.2, 0.2, 0.2, 0.3, 0.4, 0.4, 0.5, 0.5, 0.6, 1, 2, 2, 3, 4, 4, 5, 5, 6, 7, 7, 8, 8, 9],
        "one_hand": [0.4, 0.5, 0.7, 0.9, 1, 1, 1, 2, 2, 4, 5, 7, 9, 11, 13, 14, 16, 18, 20, 22, 23, 25, 27],
        "moving": [0.4, 0.6, 0.8, 1, 1, 1, 2, 2, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]
    }

    def _lookup_table(self, current_ma, situation_key):
        try:
            col_idx = self.COLUMNS.index(current_ma)
        except ValueError:
            col_idx = min(range(len(self.COLUMNS)), key=lambda i: abs(self.COLUMNS[i] - current_ma))
        return self.DATA[situation_key][col_idx]

    def get_effective_ma(self, base_ma: float, weapon_type: WeaponType, stance: SituationStanceModifier4B,
                               strength: int, is_one_handed: bool = False, is_moving: bool = False):
        current_ma = base_ma
        if weapon_type in (WeaponType.SUB_MACHINEGUN, WeaponType.AUTOMATIC_PISTOL, 
                          WeaponType.ASSAULT_RIFLE, WeaponType.CARBINE, WeaponType.BATTLE_RIFLE):
            if stance in (SituationStanceModifier4B.STANDING, SituationStanceModifier4B.STANDING_AND_BRACED):
                current_ma = self._lookup_table(current_ma, "rifle_standing")
            elif stance in (SituationStanceModifier4B.KNEELING, SituationStanceModifier4B.KNEELING_AND_BRACED):
                current_ma = self._lookup_table(current_ma, "rifle_kneeling")
            elif stance in (SituationStanceModifier4B.PRONE, SituationStanceModifier4B.PRONE_AND_BRACED):
                current_ma = self._lookup_table(current_ma, "rifle_prone")
        else:
            if stance in (SituationStanceModifier4B.STANDING, SituationStanceModifier4B.STANDING_AND_BRACED):
                current_ma = self._lookup_table(current_ma, "mg_standing")
            elif stance in (SituationStanceModifier4B.KNEELING, SituationStanceModifier4B.KNEELING_AND_BRACED):
                current_ma = self._lookup_table(current_ma, "mg_kneeling")
            elif stance == SituationStanceModifier4B.FIRING_FROM_THE_HIP:
                current_ma = self._lookup_table(current_ma, "mg_hip")

        if 3 <= strength <= 8:
            current_ma = self._lookup_table(current_ma, "str_3_8")
        elif 12 <= strength <= 15:
            current_ma = self._lookup_table(current_ma, "str_12_15")
        elif 16 <= strength <= 18:
            current_ma = self._lookup_table(current_ma, "str_16_18")

        if is_one_handed:
            current_ma = self._lookup_table(current_ma, "one_hand")

        if is_moving:
            current_ma = self._lookup_table(current_ma, "moving")

        return current_ma
