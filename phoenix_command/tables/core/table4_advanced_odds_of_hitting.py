import bisect
from typing import Dict, Tuple

from phoenix_command.models.enums import ShotType, TargetExposure, AccuracyModifiers


class Table4AdvancedOddsOfHitting:
    @classmethod
    def get_accuracy_level_modifier_by_range(cls, distance: float) -> int:
        TABLE = [
            (1, 33),
            (2, 28),
            (3, 25),
            (4, 23),
            (5, 22),
            (6, 20),
            (7, 19),
            (8, 18),
            (9, 17),
            (11, 16),
            (12, 15),
            (14, 14),
            (16, 13),
            (19, 12),
            (22, 11),
            (25, 10),
            (30, 9),
            (35, 8),
            (40, 7),
            (45, 6),
            (50, 5),
            (55, 4),
            (65, 3),
            (75, 2),
            (85, 1),
            (100, 0),
            (115, -1),
            (130, -2),
            (150, -3),
            (170, -4),
            (200, -5),
            (230, -6),
            (250, -7),
            (300, -8),
            (350, -9),
            (400, -10),
            (450, -11),
            (500, -12),
            (600, -13),
            (700, -14),
            (800, -15),
            (950, -16),
            (1100, -17),
            (1250, -18),
            (1400, -19),
            (1650, -20),
            (1900, -21),
            (2150, -22),
            (2500, -23),
            (2850, -24),
            (3300, -25),
            (3800, -26),
            (4350, -27),
        ]

        if distance > 4350:
            raise ValueError("Range exceeds maximum supported distance (4350).")

        for max_range, alm in TABLE:
            if distance <= max_range:
                return alm

        raise ValueError("Unreachable range lookup state.")

    @classmethod
    def get_odds_of_hitting_4g(cls, effective_accuracy_level: int, shot_type: ShotType) -> int:
        """
        Returns the odds of hitting (as int percentage) based on effective accuracy level (EAL) and shot type.
        If EAL > 28, returns 99.
        If EAL < -22, returns 0.
        For EAL between -22 and 28, looks up from the table using floor (nearest lower EAL if exact not present).
        """
        if effective_accuracy_level > 28:
            return 99
        if effective_accuracy_level < -22:
            return 0

        table: Dict[int, Dict[ShotType, int]] = {
            28: {ShotType.SINGLE: 99, ShotType.BURST: 99},
            27: {ShotType.SINGLE: 98, ShotType.BURST: 98},
            26: {ShotType.SINGLE: 96, ShotType.BURST: 98},
            25: {ShotType.SINGLE: 94, ShotType.BURST: 97},
            24: {ShotType.SINGLE: 90, ShotType.BURST: 95},
            23: {ShotType.SINGLE: 86, ShotType.BURST: 92},
            22: {ShotType.SINGLE: 80, ShotType.BURST: 90},
            21: {ShotType.SINGLE: 74, ShotType.BURST: 86},
            20: {ShotType.SINGLE: 67, ShotType.BURST: 82},
            19: {ShotType.SINGLE: 60, ShotType.BURST: 77},
            18: {ShotType.SINGLE: 53, ShotType.BURST: 73},
            17: {ShotType.SINGLE: 46, ShotType.BURST: 68},
            16: {ShotType.SINGLE: 39, ShotType.BURST: 62},
            15: {ShotType.SINGLE: 33, ShotType.BURST: 57},
            14: {ShotType.SINGLE: 27, ShotType.BURST: 52},
            13: {ShotType.SINGLE: 22, ShotType.BURST: 47},
            12: {ShotType.SINGLE: 18, ShotType.BURST: 43},
            11: {ShotType.SINGLE: 15, ShotType.BURST: 38},
            10: {ShotType.SINGLE: 12, ShotType.BURST: 34},
            9: {ShotType.SINGLE: 9, ShotType.BURST: 31},
            8: {ShotType.SINGLE: 7, ShotType.BURST: 27},
            7: {ShotType.SINGLE: 6, ShotType.BURST: 24},
            6: {ShotType.SINGLE: 5, ShotType.BURST: 21},
            5: {ShotType.SINGLE: 4, ShotType.BURST: 19},
            4: {ShotType.SINGLE: 3, ShotType.BURST: 17},
            3: {ShotType.SINGLE: 2, ShotType.BURST: 15},
            2: {ShotType.SINGLE: 2, ShotType.BURST: 13},
            1: {ShotType.SINGLE: 1, ShotType.BURST: 11},
            0: {ShotType.SINGLE: 1, ShotType.BURST: 10},
            -1: {ShotType.SINGLE: 1, ShotType.BURST: 9},
            -2: {ShotType.SINGLE: 0, ShotType.BURST: 8},
            -3: {ShotType.SINGLE: 0, ShotType.BURST: 7},
            -4: {ShotType.SINGLE: 0, ShotType.BURST: 6},
            -5: {ShotType.SINGLE: 0, ShotType.BURST: 5},
            -6: {ShotType.SINGLE: 0, ShotType.BURST: 4},
            -8: {ShotType.SINGLE: 0, ShotType.BURST: 3},
            -10: {ShotType.SINGLE: 0, ShotType.BURST: 2},
            -15: {ShotType.SINGLE: 0, ShotType.BURST: 1},
            -17: {ShotType.SINGLE: 0, ShotType.BURST: 0},
            -22: {ShotType.SINGLE: 0, ShotType.BURST: 0},
        }

        keys = sorted(table.keys())
        index = bisect.bisect_left(keys, effective_accuracy_level)

        if index == 0:
            return table[keys[0]][shot_type]
        elif index == len(keys):
            return table[keys[-1]][shot_type]
        else:
            # Floor to the nearest lower key
            return table[keys[index - 1]][shot_type]

    @classmethod
    def get_standard_target_size_modifier_4e(cls, target_exposure: TargetExposure,
                                             modifier_type: AccuracyModifiers) -> int:
        """
        Returns the ALM modifier based on Target Exposure and Accuracy Modifier type from Table 4E.
        Args:
            target_exposure: The target exposure type.
            modifier_type: The type of accuracy modifier (Target Size, Auto Elev, or Auto Width).
        Returns:
            The corresponding ALM modifier value (int).
        Raises:
            ValueError: If the combination is invalid (unsupported exposure or type).
        """
        table = {
            TargetExposure.LOOKING_OVER_COVER: {
                AccuracyModifiers.TARGET_SIZE: -4,
                AccuracyModifiers.AUTO_ELEV: -3,
                AccuracyModifiers.AUTO_WIDTH: -3,
            },
            TargetExposure.FIRING_OVER_COVER: {
                AccuracyModifiers.TARGET_SIZE: 0,
                AccuracyModifiers.AUTO_ELEV: 2,
                AccuracyModifiers.AUTO_WIDTH: 2,
            },
            TargetExposure.STANDING_EXPOSED: {
                AccuracyModifiers.TARGET_SIZE: 7,
                AccuracyModifiers.AUTO_ELEV: 14,
                AccuracyModifiers.AUTO_WIDTH: 1,
            },
            TargetExposure.KNEELING_EXPOSED: {
                AccuracyModifiers.TARGET_SIZE: 6,
                AccuracyModifiers.AUTO_ELEV: 11,
                AccuracyModifiers.AUTO_WIDTH: 3,
            },
            TargetExposure.PRONE_EXPOSED: {
                AccuracyModifiers.TARGET_SIZE: 2,
                AccuracyModifiers.AUTO_ELEV: 2,
                AccuracyModifiers.AUTO_WIDTH: 2,
            },
            TargetExposure.RUNNING: {
                AccuracyModifiers.TARGET_SIZE: 8,
                AccuracyModifiers.AUTO_ELEV: 14,
                AccuracyModifiers.AUTO_WIDTH: 1,
            },
            TargetExposure.LOW_CROUCH: {
                AccuracyModifiers.TARGET_SIZE: 7,
                AccuracyModifiers.AUTO_ELEV: 11,
                AccuracyModifiers.AUTO_WIDTH: 2,
            },
            TargetExposure.HANDS_AND_KNEES: {
                AccuracyModifiers.TARGET_SIZE: 6,
                AccuracyModifiers.AUTO_ELEV: 8,
                AccuracyModifiers.AUTO_WIDTH: 1,
            },
            TargetExposure.LOW_PRONE: {
                AccuracyModifiers.TARGET_SIZE: 1,
                AccuracyModifiers.AUTO_ELEV: 0,
                AccuracyModifiers.AUTO_WIDTH: 5,
            },
            TargetExposure.HEAD: {
                AccuracyModifiers.TARGET_SIZE: -3,
                AccuracyModifiers.AUTO_ELEV: 0,
                AccuracyModifiers.AUTO_WIDTH: -3,
            },
            TargetExposure.BODY: {
                AccuracyModifiers.TARGET_SIZE: 5,
                AccuracyModifiers.AUTO_ELEV: 8,
                AccuracyModifiers.AUTO_WIDTH: 3,
            },
            TargetExposure.LEGS: {
                AccuracyModifiers.TARGET_SIZE: 4,
                AccuracyModifiers.AUTO_ELEV: 8,
                AccuracyModifiers.AUTO_WIDTH: 0,
            },
        }

        if target_exposure not in table:
            raise ValueError(f"Unsupported TargetExposure: {target_exposure}")

        modifiers = table[target_exposure]
        if modifier_type not in modifiers:
            raise ValueError(f"Unsupported AccuracyModifiers for {target_exposure}: {modifier_type}")

        return modifiers[modifier_type]

    @classmethod
    def get_movement_alm_and_max_aim_time(cls, speed: float, target_hpi: float) -> Tuple[int, float]:
        """
        Returns the movement ALM modifier and maximum aim impulses based on speed and target HPI from Table 4D.
        For non-exact speed or HPI, floors to the nearest lower value in the table.
        Maximum aim impulses: 2 for -10, 3 for -9, 4 for -8, 5 for -7, 6 for -6, infinity for -5 and above.
        """
        # Table: speed -> hpi -> modifier #FIXME: set up real values
        table: Dict[float, Dict[float, int]] = {
            0.5: {10: -6, 20: -5, 40: -5, 70: -5, 100: -5, 200: -5, 300: -5, 400: -5, 600: -5, 800: -5, 1000: -5,
                  1200: -5, 1500: -5},
            1.0: {10: -8, 20: -6, 40: -5, 70: -5, 100: -5, 200: -5, 300: -5, 400: -5, 600: -5, 800: -5, 1000: -5,
                  1200: -5, 1500: -5},
            2.0: {10: -10, 20: -8, 40: -6, 70: -5, 100: -5, 200: -5, 300: -5, 400: -5, 600: -5, 800: -5, 1000: -5,
                  1200: -5, 1500: -5},
            3.0: {10: -10, 20: -10, 40: -7, 70: -6, 100: -5, 200: -5, 300: -5, 400: -5, 600: -5, 800: -5, 1000: -5,
                  1200: -5, 1500: -5},
            4.0: {10: -10, 20: -10, 40: -8, 70: -6, 100: -6, 200: -5, 300: -5, 400: -5, 600: -5, 800: -5, 1000: -5,
                  1200: -5, 1500: -5},
            10.0: {10: -10, 20: -10, 40: -10, 70: -10, 100: -8, 200: -6, 300: -5, 400: -5, 600: -5, 800: -5, 1000: -5,
                   1200: -5, 1500: -5},
            20.0: {10: -10, 20: -10, 40: -10, 70: -10, 100: -10, 200: -8, 300: -7, 400: -6, 600: -5, 800: -5, 1000: -5,
                   1200: -5, 1500: -5},
            30.0: {10: -10, 20: -10, 40: -10, 70: -10, 100: -10, 200: -10, 300: -8, 400: -7, 600: -6, 800: -6, 1000: -5,
                   1200: -5, 1500: -5},
            40.0: {10: -10, 20: -10, 40: -10, 70: -10, 100: -10, 200: -10, 300: -9, 400: -8, 600: -7, 800: -6, 1000: -5,
                   1200: -5, 1500: -5},
            50.0: {10: -10, 20: -10, 40: -10, 70: -10, 100: -10, 200: -10, 300: -10, 400: -10, 600: -9, 800: -8,
                   1000: -7, 1200: -6, 1500: -5},
            60.0: {10: -10, 20: -10, 40: -10, 70: -10, 100: -10, 200: -10, 300: -10, 400: -10, 600: -10, 800: -10,
                   1000: -8, 1200: -7, 1500: -6},
            70.0: {10: -10, 20: -10, 40: -10, 70: -10, 100: -10, 200: -10, 300: -10, 400: -10, 600: -9, 800: -8,
                   1000: -7, 1200: -6, 1500: -6},
            80.0: {10: -10, 20: -10, 40: -10, 70: -10, 100: -10, 200: -10, 300: -10, 400: -10, 600: -10, 800: -10,
                   1000: -9, 1200: -8, 1500: -7},
            90.0: {10: -10, 20: -10, 40: -10, 70: -10, 100: -10, 200: -10, 300: -10, 400: -10, 600: -10, 800: -10,
                   1000: -10, 1200: -9, 1500: -8},
            100.0: {10: -10, 20: -10, 40: -10, 70: -10, 100: -10, 200: -10, 300: -10, 400: -10, 600: -10, 800: -10,
                    1000: -10, 1200: -9, 1500: -8},
            110.0: {10: -10, 20: -10, 40: -10, 70: -10, 100: -10, 200: -10, 300: -10, 400: -10, 600: -10, 800: -10,
                    1000: -10, 1200: -10, 1500: -9},
            120.0: {10: -10, 20: -10, 40: -10, 70: -10, 100: -10, 200: -10, 300: -10, 400: -10, 600: -10, 800: -10,
                    1000: -10, 1200: -10, 1500: -10},
        }

        # Max aim impulses mapping
        max_aim_map = {
            -10: 2,
            -9: 3,
            -8: 4,
            -7: 5,
            -6: 6,
            -5: float('inf'),
        }

        # Get sorted keys for speed and hpi
        speed_keys = sorted(table.keys())
        hpi_keys = sorted(table[speed_keys[0]].keys()) if table else []

        # Floor speed
        speed_index = bisect.bisect_right(speed_keys, speed) - 1
        floored_speed = speed_keys[speed_index] if speed_index >= 0 else speed_keys[0]

        # Floor hpi
        hpi_index = bisect.bisect_right(hpi_keys, target_hpi) - 1
        floored_hpi = hpi_keys[hpi_index] if hpi_index >= 0 else hpi_keys[0]

        modifier = table[floored_speed][floored_hpi]

        # Get max aim: extend pattern for modifiers > -5 or < -10
        if modifier <= -10:
            max_aim = 2
        elif modifier >= -5:
            max_aim = float('inf')
        else:
            max_aim = max_aim_map.get(modifier, 2)  # Default to 2 for unknown

        return modifier, max_aim
