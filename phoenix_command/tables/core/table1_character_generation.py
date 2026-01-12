import bisect


class Table1CharacterGeneration:
    """Implements the character generation tables from Phoenix Command Table 1."""

    @staticmethod
    def get_base_speed_1a(strength: float, encumbrance: float) -> float:
        """
        Returns the base speed (as float) based on strength and encumbrance from the recognized table.
        Handles intermediate encumbrance values by selecting the next higher encumbrance level.
        Returns 0.0 for encumbrance beyond the table's supported levels or where no value is present in the image.
        Strength is converted to int; raises ValueError if invalid.
        """
        enc_levels = [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 70, 80, 90, 100, 125, 150, 200]

        table = {
            21: [4.5, 4.5, 4.0, 4.0, 4.0, 3.5, 3.5, 3.5, 3.5, 3.5, 3.0, 3.0, 3.0, 3.0, 3.0, 2.5, 2.5, 2.0],
            20: [4.5, 4.0, 4.0, 3.5, 3.5, 3.5, 3.5, 3.5, 3.0, 3.0, 3.0, 3.0, 3.0, 2.5, 2.5, 2.5, 2.5, 2.0],
            19: [4.0, 4.0, 3.5, 3.5, 3.0, 3.0, 3.0, 3.0, 3.0, 2.5, 2.5, 2.5, 2.5, 2.5, 2.0, 2.0, 2.0, 1.5],
            18: [4.0, 3.5, 3.5, 3.0, 3.0, 3.0, 2.5, 2.5, 2.5, 2.5, 2.5, 2.0, 2.0, 2.0, 2.0, 1.5, 1.5, 1.5],
            17: [3.5, 3.0, 3.0, 3.0, 2.5, 2.5, 2.5, 2.5, 2.0, 2.0, 2.0, 2.0, 2.0, 1.5, 1.5, 1.5, 1.5, 1.0],
            16: [3.5, 3.0, 2.5, 2.5, 2.5, 2.5, 2.0, 2.0, 2.0, 2.0, 2.0, 1.5, 1.5, 1.5, 1.5, 1.0, 1.0, 1.0],
            15: [3.0, 3.0, 2.5, 2.5, 2.0, 2.0, 2.0, 2.0, 2.0, 1.5, 1.5, 1.5, 1.5, 1.5, 1.0, 1.0, 1.0, 0.0],
            14: [3.0, 2.5, 2.5, 2.0, 2.0, 2.0, 2.0, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.0, 1.0, 1.0, 1.0, 0.0],
            13: [3.0, 2.5, 2.5, 2.0, 2.0, 2.0, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0],
            12: [3.0, 2.5, 2.0, 2.0, 2.0, 2.0, 1.5, 1.5, 1.5, 1.5, 1.5, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0],
            11: [3.0, 2.5, 2.0, 2.0, 2.0, 2.0, 1.5, 1.5, 1.5, 1.5, 1.5, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0],
            10: [3.0, 2.5, 2.0, 2.0, 2.0, 2.0, 1.5, 1.5, 1.5, 1.5, 1.5, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0],
            9: [3.0, 2.5, 2.0, 2.0, 2.0, 2.0, 1.5, 1.5, 1.5, 1.5, 1.5, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0],
            8: [3.0, 2.5, 2.0, 2.0, 2.0, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0],
            7: [2.5, 2.5, 2.0, 2.0, 2.0, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0],
            6: [2.5, 2.5, 2.0, 2.0, 2.0, 1.5, 1.5, 1.5, 1.5, 1.5, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0],
            5: [2.5, 2.5, 2.0, 2.0, 1.5, 1.5, 1.5, 1.5, 1.5, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0],
            4: [2.5, 2.0, 2.0, 1.5, 1.5, 1.5, 1.5, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            3: [2.5, 2.0, 1.5, 1.5, 1.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            2: [2.0, 1.5, 1.5, 1.5, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            1: [1.5, 1.5, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        }

        stren = int(strength)
        if stren < 1 or stren > 21:
            raise ValueError("Strength must be between 1 and 21.")

        if encumbrance > enc_levels[-1]:
            return 0.0

        enc_index = 0
        for i in range(len(enc_levels)):
            if enc_levels[i] >= encumbrance:
                enc_index = i
                break

        return table[stren][enc_index]

    @staticmethod
    def get_max_speed_1b(agility: float, base_speed: float) -> float:
        """
        Returns the max speed (as float) based on agility and base speed from the provided matrix.
        Performs exact lookup; returns 0.0 if no exact match is found.
        Agility is converted to int (1-21).
        """
        matrix = {
            21: {1: 2, 1.5: 4, 2: 5, 2.5: 7, 3: 9, 3.5: 10, 4: 12, 4.5: 13},
            20: {1: 2, 1.5: 4, 2: 5, 2.5: 7, 3: 8, 3.5: 10, 4: 11, 4.5: 13},
            19: {1: 2, 1.5: 4, 2: 5, 2.5: 7, 3: 8, 3.5: 10, 4: 11, 4.5: 12},
            18: {1: 2, 1.5: 4, 2: 5, 2.5: 6, 3: 8, 3.5: 9, 4: 11, 4.5: 12},
            17: {1: 2, 1.5: 3, 2: 5, 2.5: 6, 3: 8, 3.5: 9, 4: 10, 4.5: 12},
            16: {1: 2, 1.5: 3, 2: 5, 2.5: 6, 3: 8, 3.5: 9, 4: 10, 4.5: 11},
            15: {1: 2, 1.5: 3, 2: 5, 2.5: 6, 3: 7, 3.5: 9, 4: 10, 4.5: 11},
            14: {1: 2, 1.5: 3, 2: 4, 2.5: 6, 3: 7, 3.5: 8, 4: 9, 4.5: 11},
            13: {1: 2, 1.5: 3, 2: 4, 2.5: 6, 3: 7, 3.5: 8, 4: 9, 4.5: 10},
            12: {1: 2, 1.5: 3, 2: 4, 2.5: 5, 3: 7, 3.5: 8, 4: 9, 4.5: 10},
            11: {1: 2, 1.5: 3, 2: 4, 2.5: 5, 3: 6, 3.5: 7, 4: 8, 4.5: 9},
            10: {1: 2, 1.5: 3, 2: 4, 2.5: 5, 3: 6, 3.5: 7, 4: 8, 4.5: 9},
            9: {1: 2, 1.5: 3, 2: 4, 2.5: 5, 3: 6, 3.5: 7, 4: 8, 4.5: 9},
            8: {1: 2, 1.5: 3, 2: 4, 2.5: 4, 3: 5, 3.5: 6, 4: 7, 4.5: 8},
            7: {1: 2, 1.5: 3, 2: 3, 2.5: 4, 3: 5, 3.5: 6, 4: 7, 4.5: 8},
            6: {1: 2, 1.5: 2, 2: 3, 2.5: 4, 3: 5, 3.5: 5, 4: 6, 4.5: 7},
            5: {1: 1, 1.5: 2, 2: 3, 2.5: 4, 3: 4, 3.5: 5, 4: 6, 4.5: 6},
            4: {1: 1, 1.5: 2, 2: 3, 2.5: 3, 3: 4, 3.5: 4, 4: 5, 4.5: 6},
            3: {1: 1, 1.5: 2, 2: 2, 2.5: 3, 3: 3, 3.5: 4, 4: 4, 4.5: 5},
            2: {1: 1, 1.5: 1, 2: 2, 2.5: 2, 3: 3, 3.5: 3, 4: 4, 4.5: 4},
            1: {1: 1, 1.5: 1, 2: 1, 2.5: 2, 3: 2, 3.5: 2, 4: 3, 4.5: 3}
        }

        agi = int(agility)
        if agi < 1 or agi > 21:
            return 0.0

        if agi not in matrix:
            return 0.0

        if base_speed in matrix[agi]:
            return float(matrix[agi][base_speed])
        else:
            return 0.0

    @staticmethod
    def get_skill_accuracy_level_1c(skill_level: int) -> int:
        """
        Returns the skill accuracy level based on the provided skill level from the mapping table.
        Raises ValueError if skill_level is not between 0 and 20 inclusive.
        """
        mapping = {
            "0": 0, "1": 5, "2": 7, "3": 9, "4": 10, "5": 11, "6": 12,
            "7": 13, "8": 14, "9": 15, "10": 16, "11": 17, "12": 18,
            "13": 19, "14": 20, "15": 21, "16": 22, "17": 23, "18": 24,
            "19": 25, "20": 26
        }

        if skill_level < 0 or skill_level > 20:
            raise ValueError("Skill level must be between 0 and 20.")

        key = str(skill_level)
        return mapping[key]

    @staticmethod
    def get_combat_actions_1d(max_speed: int, intelligence_skill_factor: int) -> int:
        """
        Returns the number of combat actions based on MS and ISF from the provided table.
        Raises ValueError if MS is not between 1 and 13 inclusive.
        """

        isf_values = [7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39]

        table = {
            1: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2],
            2: [1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4],
            3: [1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6],
            4: [2, 2, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7, 7],
            5: [2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9],
            6: [3, 3, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11],
            7: [3, 4, 5, 5, 6, 7, 7, 8, 9, 9, 10, 10, 11, 11, 12, 12, 13],
            8: [3, 4, 5, 6, 7, 8, 9, 9, 10, 11, 11, 12, 12, 13, 14, 14, 15],
            9: [4, 5, 6, 7, 8, 9, 10, 10, 11, 12, 13, 13, 14, 15, 15, 16, 17],
            10: [4, 6, 7, 8, 9, 10, 11, 12, 12, 13, 14, 15, 16, 16, 17, 18, 18],
            11: [5, 6, 7, 9, 10, 11, 12, 13, 14, 14, 15, 16, 17, 18, 19, 19, 20],
            12: [5, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 21, 22],
            13: [6, 7, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
        }


        if max_speed not in table:
            raise ValueError(f"No data for MS={max_speed}")

        if intelligence_skill_factor <= isf_values[0]:
            quantized_isf = isf_values[0]
        elif intelligence_skill_factor >= isf_values[-1]:
            quantized_isf = isf_values[-1]
        else:
            pos = bisect.bisect_left(isf_values, intelligence_skill_factor)
            quantized_isf = isf_values[pos]

        col_index = isf_values.index(quantized_isf)
        return table[max_speed][col_index]

    @staticmethod
    def get_impulses_1e(combat_actions: int) -> list[int]:
        """
        Returns the list of 4 impulse values based on the provided combat actions from the mapping table.
        Raises ValueError if combat_actions is not between 1 and 24 inclusive.
        """
        mapping = {
            1: [1, 0, 0, 0],
            2: [1, 0, 1, 0],
            3: [1, 0, 1, 1],
            4: [1, 1, 1, 1],
            5: [2, 1, 1, 1],
            6: [2, 1, 2, 1],
            7: [2, 1, 2, 2],
            8: [2, 2, 2, 2],
            9: [3, 2, 2, 2],
            10: [3, 2, 3, 2],
            11: [3, 2, 3, 3],
            12: [3, 3, 3, 3],
            13: [4, 3, 3, 3],
            14: [4, 3, 4, 3],
            15: [4, 3, 4, 4],
            16: [4, 4, 4, 4],
            17: [5, 4, 4, 4],
            18: [5, 4, 5, 4],
            19: [5, 4, 5, 5],
            20: [5, 5, 5, 5],
            21: [6, 5, 5, 5],
            22: [6, 5, 6, 5],
            23: [6, 5, 6, 6],
            24: [6, 6, 6, 6]
        }

        if combat_actions < 1 or combat_actions > 24:
            raise ValueError("Combat actions must be between 1 and 24.")

        return mapping[combat_actions]

    @staticmethod
    def get_defensive_alm(intelligence_skill_factor: int) -> int:
        """Returns the Defensive ALM based on Intelligence Skill Factor."""
        if intelligence_skill_factor <= 3:
            return 16
        elif intelligence_skill_factor == 4:
            return 13
        elif intelligence_skill_factor == 5:
            return 11
        elif intelligence_skill_factor == 6:
            return 10
        elif intelligence_skill_factor == 7:
            return 8
        elif intelligence_skill_factor == 8:
            return 7
        elif intelligence_skill_factor == 9:
            return 6
        elif intelligence_skill_factor == 10:
            return 5
        elif intelligence_skill_factor == 11:
            return 4
        elif intelligence_skill_factor == 12:
            return 3
        elif 13 <= intelligence_skill_factor <= 14:
            return 2
        elif 15 <= intelligence_skill_factor <= 16:
            return 1
        elif intelligence_skill_factor == 17:
            return 0
        elif 18 <= intelligence_skill_factor <= 19:
            return -1
        elif 20 <= intelligence_skill_factor <= 22:
            return -2
        elif 23 <= intelligence_skill_factor <= 24:
            return -3
        elif 25 <= intelligence_skill_factor <= 27:
            return -4
        elif 28 <= intelligence_skill_factor <= 30:
            return -5
        elif 31 <= intelligence_skill_factor <= 34:
            return -6
        elif 35 <= intelligence_skill_factor <= 38:
            return -7
        else:  # 39+
            return -8