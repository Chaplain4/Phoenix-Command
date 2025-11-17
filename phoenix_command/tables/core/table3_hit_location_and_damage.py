import math
import random

from phoenix_command.models.enums import WoundType, DamageType, TargetExposure, HitLocation
from phoenix_command.models.hit_result_simple import HitResult


class Table3HitLocationAndDamage:

    LOW_DAMAGE: dict[HitLocation, tuple[int, WoundType]] = {
        HitLocation.HEAD_GLANCE: (7, WoundType.LIGHT_WOUND),
        HitLocation.HEAD_FOREHEAD: (2000, WoundType.CRITICAL_WOUND),
        HitLocation.HEAD_EYE_NOSE: (3000, WoundType.CRITICAL_WOUND),
        HitLocation.HEAD_MOUTH: (300, WoundType.CRITICAL_WOUND),
        HitLocation.ARM_GLANCE: (1, WoundType.SUPERFICIAL_WOUND),
        HitLocation.ARM_SHOULDER: (21, WoundType.DISABLING_INJURY),
        HitLocation.ARM_UPPER_ARM_FLESH: (3, WoundType.SUPERFICIAL_WOUND),
        HitLocation.ARM_UPPER_ARM_BONE: (7, WoundType.DISABLING_INJURY),
        HitLocation.ARM_FOREARM_FLESH: (3, WoundType.SUPERFICIAL_WOUND),
        HitLocation.ARM_FOREARM_BONE: (6, WoundType.DISABLING_INJURY),
        HitLocation.ARM_HAND: (3, WoundType.SUPERFICIAL_WOUND),
        HitLocation.ARM_WEAPON: (0, WoundType.WEAPON_CRITICAL),
        HitLocation.BODY_GLANCE: (1, WoundType.SUPERFICIAL_WOUND),
        HitLocation.BODY_CHEST: (51, WoundType.HEAVY_WOUND),
        HitLocation.BODY_BASE_OF_NECK: (300, WoundType.CRITICAL_WOUND),
        HitLocation.BODY_HEART: (4000, WoundType.CRITICAL_WOUND),
        HitLocation.BODY_SPINE: (300, WoundType.CRITICAL_WOUND),
        HitLocation.BODY_ABDOMEN: (35, WoundType.HEAVY_WOUND),
        HitLocation.BODY_PELVIS: (21, WoundType.MEDIUM_WOUND),
        HitLocation.LEG_GLANCE: (1, WoundType.SUPERFICIAL_WOUND),
        HitLocation.LEG_THIGH_FLESH: (3, WoundType.SUPERFICIAL_WOUND),
        HitLocation.LEG_THIGH_BONE: (16, WoundType.DISABLING_INJURY),
        HitLocation.LEG_SHIN_FOOT: (14, WoundType.DISABLING_INJURY),
    }

    OPPD_DAMAGE: dict[HitLocation, list[tuple[int, WoundType]]] = {
        HitLocation.HEAD_GLANCE: [
            (7, WoundType.LIGHT_WOUND),
            (200, WoundType.MEDIUM_WOUND),
            (1000, WoundType.HEAVY_WOUND),
            (80000, WoundType.CRITICAL_WOUND),
        ],
        HitLocation.HEAD_FOREHEAD: [
            (2000, WoundType.CRITICAL_WOUND),
            (60000, WoundType.CRITICAL_WOUND),
            (math.inf, WoundType.DEAD),
            (math.inf, WoundType.DEAD),
        ],
        HitLocation.HEAD_EYE_NOSE: [
            (3000, WoundType.CRITICAL_WOUND),
            (80000, WoundType.CRITICAL_WOUND),
            (math.inf, WoundType.DEAD),
            (math.inf, WoundType.DEAD),
        ],
        HitLocation.HEAD_MOUTH: [
            (300, WoundType.CRITICAL_WOUND),
            (6000, WoundType.CRITICAL_WOUND),
            (30000, WoundType.CRITICAL_WOUND),
            (math.inf, WoundType.DEAD),
        ],
        HitLocation.ARM_GLANCE: [
            (1, WoundType.SUPERFICIAL_WOUND),
            (5, WoundType.DISABLING_INJURY),
            (11, WoundType.DISABLING_INJURY),
            (32, WoundType.DISABLING_INJURY),
        ],
        HitLocation.ARM_SHOULDER: [
            (21, WoundType.DISABLING_INJURY),
            (500, WoundType.DISABLING_INJURY),
            (1000, WoundType.DISABLING_INJURY),
            (1000, WoundType.DISABLING_INJURY),
        ],
        HitLocation.ARM_UPPER_ARM_FLESH: [
            (3, WoundType.SUPERFICIAL_WOUND),
            (12, WoundType.DISABLING_INJURY),
            (100, WoundType.DISABLING_INJURY),
            (100, WoundType.DISABLING_INJURY),
        ],
        HitLocation.ARM_UPPER_ARM_BONE: [
            (7, WoundType.DISABLING_INJURY),
            (60, WoundType.DISABLING_INJURY),
            (100, WoundType.DISABLING_INJURY),
            (100, WoundType.DISABLING_INJURY),
        ],
        HitLocation.ARM_FOREARM_FLESH: [
            (3, WoundType.SUPERFICIAL_WOUND),
            (12, WoundType.DISABLING_INJURY),
            (50, WoundType.DISABLING_INJURY),
            (50, WoundType.DISABLING_INJURY),
        ],
        HitLocation.ARM_FOREARM_BONE: [
            (6, WoundType.DISABLING_INJURY),
            (60, WoundType.DISABLING_INJURY),
            (60, WoundType.DISABLING_INJURY),
            (60, WoundType.DISABLING_INJURY),
        ],
        HitLocation.ARM_HAND: [
            (3, WoundType.SUPERFICIAL_WOUND),
            (8, WoundType.DISABLING_INJURY),
            (15, WoundType.DISABLING_INJURY),
            (15, WoundType.DISABLING_INJURY),
        ],
        HitLocation.ARM_WEAPON: [
            (0, WoundType.WEAPON_CRITICAL),
            (0, WoundType.WEAPON_CRITICAL),
            (0, WoundType.WEAPON_CRITICAL),
            (0, WoundType.WEAPON_CRITICAL),
        ],
        HitLocation.BODY_GLANCE: [
            (1, WoundType.SUPERFICIAL_WOUND),
            (7, WoundType.SUPERFICIAL_WOUND),
            (16, WoundType.SUPERFICIAL_WOUND),
            (47, WoundType.SUPERFICIAL_WOUND),
        ],
        HitLocation.BODY_CHEST: [
            (51, WoundType.HEAVY_WOUND),
            (100, WoundType.HEAVY_WOUND),
            (300, WoundType.HEAVY_WOUND),
            (2000, WoundType.CRITICAL_WOUND),
        ],
        HitLocation.BODY_BASE_OF_NECK: [
            (300, WoundType.CRITICAL_WOUND),
            (6000, WoundType.CRITICAL_WOUND),
            (40000, WoundType.CRITICAL_WOUND),
            (math.inf, WoundType.DEAD),
        ],
        HitLocation.BODY_HEART: [
            (4000, WoundType.CRITICAL_WOUND),
            (100000, WoundType.CRITICAL_WOUND),
            (math.inf, WoundType.DEAD),
            (math.inf, WoundType.DEAD),
        ],
        HitLocation.BODY_SPINE: [
            (300, WoundType.CRITICAL_WOUND),
            (5000, WoundType.CRITICAL_WOUND),
            (30000, WoundType.CRITICAL_WOUND),
            (math.inf, WoundType.DEAD),
        ],
        HitLocation.BODY_ABDOMEN: [
            (35, WoundType.HEAVY_WOUND),
            (900, WoundType.HEAVY_WOUND),
            (5000, WoundType.CRITICAL_WOUND),
            (30000, WoundType.CRITICAL_WOUND),
        ],
        HitLocation.BODY_PELVIS: [
            (21, WoundType.MEDIUM_WOUND),
            (100, WoundType.MEDIUM_WOUND),
            (500, WoundType.HEAVY_WOUND),
            (4000, WoundType.CRITICAL_WOUND),
        ],
        HitLocation.LEG_GLANCE: [
            (1, WoundType.SUPERFICIAL_WOUND),
            (7, WoundType.DISABLING_INJURY),
            (16, WoundType.DISABLING_INJURY),
            (47, WoundType.DISABLING_INJURY),
        ],
        HitLocation.LEG_THIGH_FLESH: [
            (3, WoundType.SUPERFICIAL_WOUND),
            (88, WoundType.DISABLING_INJURY),
            (500, WoundType.DISABLING_INJURY),
            (600, WoundType.DISABLING_INJURY),
        ],
        HitLocation.LEG_THIGH_BONE: [
            (16, WoundType.DISABLING_INJURY),
            (400, WoundType.DISABLING_INJURY),
            (700, WoundType.DISABLING_INJURY),
            (700, WoundType.DISABLING_INJURY),
        ],
        HitLocation.LEG_SHIN_FOOT: [
            (14, WoundType.DISABLING_INJURY),
            (200, WoundType.DISABLING_INJURY),
            (200, WoundType.DISABLING_INJURY),
            (200, WoundType.DISABLING_INJURY),
        ],
    }

    PRONE_OR_FIRING_OVER_COVER_RANGES = [
        (0, 2, HitLocation.HEAD_GLANCE),
        (3, 17, HitLocation.HEAD_FOREHEAD),
        (18, 22, HitLocation.HEAD_EYE_NOSE),
        (23, 38, HitLocation.HEAD_MOUTH),
        (39, 56, HitLocation.ARM_GLANCE),
        (57, 69, HitLocation.ARM_SHOULDER),
        (70, 76, HitLocation.ARM_UPPER_ARM_FLESH),
        (77, 80, HitLocation.ARM_UPPER_ARM_BONE),
        (81, 83, HitLocation.ARM_FOREARM_FLESH),
        (84, 92, HitLocation.ARM_FOREARM_BONE),
        (93, 95, HitLocation.ARM_HAND),
        (96, 99, HitLocation.ARM_WEAPON),
    ]

    STANDING_EXPOSED_RANGES = [
        (0, 0, HitLocation.HEAD_GLANCE),
        (1, 2, HitLocation.HEAD_FOREHEAD),
        (3, 3, HitLocation.HEAD_EYE_NOSE),
        (4, 5, HitLocation.HEAD_MOUTH),
        (6, 8, HitLocation.ARM_GLANCE),
        (9, 10, HitLocation.ARM_SHOULDER),
        (11, 11, HitLocation.ARM_UPPER_ARM_FLESH),
        (12, 12, HitLocation.ARM_UPPER_ARM_BONE),
        (13, 13, HitLocation.ARM_FOREARM_FLESH),
        (14, 14, HitLocation.ARM_FOREARM_BONE),
        (15, 15, HitLocation.ARM_HAND),
        (16, 16, HitLocation.ARM_WEAPON),
        (17, 19, HitLocation.BODY_GLANCE),
        (20, 23, HitLocation.BODY_CHEST),
        (24, 24, HitLocation.BODY_BASE_OF_NECK),
        (25, 25, HitLocation.BODY_HEART),
        (26, 30, HitLocation.BODY_SPINE),
        (31, 42, HitLocation.BODY_ABDOMEN),
        (43, 56, HitLocation.BODY_PELVIS),
        (57, 60, HitLocation.LEG_GLANCE),
        (61, 77, HitLocation.LEG_THIGH_FLESH),
        (78, 82, HitLocation.LEG_THIGH_BONE),
        (83, 99, HitLocation.LEG_SHIN_FOOT),
    ]

    LOOKING_OVER_COVER_RANGES = [
        (0, 4, HitLocation.HEAD_GLANCE),
        (5, 39, HitLocation.HEAD_FOREHEAD),
        (40, 79, HitLocation.HEAD_EYE_NOSE),
        (80, 99, HitLocation.HEAD_MOUTH),
    ]

    KNEELING_EXPOSED_RANGES = [
        (0, 0, HitLocation.HEAD_GLANCE),  # 1%
        (1, 3, HitLocation.HEAD_FOREHEAD),  # 3%
        (4, 7, HitLocation.HEAD_EYE_NOSE),  # 4%
        (8, 8, HitLocation.HEAD_MOUTH),  # 1%
        (9, 10, HitLocation.ARM_GLANCE),  # 2%
        (11, 13, HitLocation.ARM_SHOULDER),  # 3%
        (14, 18, HitLocation.ARM_UPPER_ARM_FLESH),  # 5%
        (19, 19, HitLocation.ARM_UPPER_ARM_BONE),  # 1%
        (20, 22, HitLocation.ARM_FOREARM_FLESH),  # 3%
        (23, 23, HitLocation.ARM_FOREARM_BONE),  # 1%
        (24, 25, HitLocation.ARM_HAND),  # 2%
        (26, 26, HitLocation.ARM_WEAPON),  # 1%
        (27, 30, HitLocation.BODY_GLANCE),  # 4%
        (31, 48, HitLocation.BODY_CHEST),  # 18%
        (49, 49, HitLocation.BODY_BASE_OF_NECK),  # 1%
        (50, 51, HitLocation.BODY_HEART),  # 2%
        (52, 57, HitLocation.BODY_SPINE),  # 6%
        (58, 67, HitLocation.BODY_ABDOMEN),  # 10%
        (68, 76, HitLocation.BODY_PELVIS),  # 9%
        (77, 78, HitLocation.LEG_GLANCE),  # 2%
        (79, 90, HitLocation.LEG_THIGH_FLESH),  # 12%
        (91, 93, HitLocation.LEG_THIGH_BONE),  # 3%
        (94, 99, HitLocation.LEG_SHIN_FOOT),  # 6%
    ]

    @classmethod
    def get_oppd_column(cls, wdc: int) -> int:
        """
        Returns the OPPD column index based on Weapon Damage Class.
        """
        if 1 <= wdc <= 2:
            return 0
        elif 3 <= wdc <= 5:
            return 1
        elif 6 <= wdc <= 8:
            return 2
        elif 9 <= wdc <= 10:
            return 3
        else:
            raise ValueError(f"Invalid Weapon Damage Class: {wdc}. Must be between 1 and 10.")

    @classmethod
    def get_hit_location(cls, roll: int, target_exposure: TargetExposure) -> HitLocation:
        """
        Determines the hit location based on the roll and target exposure.
        """
        if target_exposure in [TargetExposure.FIRING_OVER_COVER, TargetExposure.PRONE_EXPOSED]:
            ranges = cls.PRONE_OR_FIRING_OVER_COVER_RANGES
        elif target_exposure == TargetExposure.STANDING_EXPOSED:
            ranges = cls.STANDING_EXPOSED_RANGES
        elif target_exposure == TargetExposure.LOOKING_OVER_COVER:
            ranges = cls.LOOKING_OVER_COVER_RANGES
        elif target_exposure == TargetExposure.KNEELING_EXPOSED:
            ranges = cls.KNEELING_EXPOSED_RANGES
        else:
            raise ValueError(f"Unsupported TargetExposure: {target_exposure}")

        for min_r, max_r, location in ranges:
            if min_r <= roll <= max_r:
                return location

        raise ValueError(f"No location found for roll {roll} and exposure {target_exposure}")

    @classmethod
    def hit_location_and_damage_3a(
        cls, damage_type: DamageType, target_exposure: TargetExposure, wdc: int
    ) -> HitResult:
        """
        Determines hit location and damage based on the provided inputs.
        Generates a random roll from 0 to 99 and selects the appropriate location based on target exposure.
        Returns the damage amount, wound type, and hit location.
        """
        roll = random.randint(0, 99)
        location = cls.get_hit_location(roll, target_exposure)

        if damage_type == DamageType.LOW_VELOCITY:
            damage, wound_type = cls.LOW_DAMAGE[location]
        else:
            col = cls.get_oppd_column(wdc)
            damage, wound_type = cls.OPPD_DAMAGE[location][col]

        return HitResult(
            damage=damage,
            wound_type=wound_type,
            hit_location=location,
        )