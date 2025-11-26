from enum import Enum


class ShooterStance(Enum):
    STANDING = 0
    KNEELING = 3
    PRONE = 6
    HIP_FIRING = -6

class TargetExposure(Enum):
    """
    Enum for Target Exposure types (Table 4E rows).
    Values represent base ALM (Aim Level Modifier) adjustments for Target Size.
    """
    LOOKING_OVER_COVER = -4  # Look Over/Around
    FIRING_OVER_COVER = 0    # Fire Over/Around
    STANDING_EXPOSED = 7     # Standing Exposed (updated to match table)
    KNEELING_EXPOSED = 6     # Kneeling Exposed
    PRONE_EXPOSED = 2        # Prone / Crawl
    RUNNING = 8              # Running
    LOW_CROUCH = 7           # Low Crouch
    HANDS_AND_KNEES = 6      # Hands and Knees
    LOW_PRONE = 1            # Low Prone
    HEAD = -3                # Head
    BODY = 5                 # Body
    LEGS = 4                 # Legs
    ARMS = 3                 # Arms

class ExplosiveTarget(Enum):
    HEX = 12
    WINDOW = 9
    DOOR = 13

class DamageType(Enum):
    LOW_VELOCITY = "LOW_VELOCITY"
    OVER_PENETRATING = "OVER_PENETRATING"

class WoundType(Enum):
    SUPERFICIAL_WOUND = "SUPERFICIAL_WOUND"
    LIGHT_WOUND = "LIGHT_WOUND"
    MEDIUM_WOUND = "MEDIUM_WOUND"
    HEAVY_WOUND = "HEAVY_WOUND"
    CRITICAL_WOUND = "CRITICAL_WOUND"
    DISABLING_INJURY = "DISABLING_INJURY"
    DEAD = "DEAD"
    WEAPON_CRITICAL = "WEAPON_CRITICAL"

class HitLocation(Enum):
    HEAD_GLANCE = 'HEAD_GLANCE'
    HEAD_FOREHEAD = 'HEAD_FOREHEAD'
    HEAD_EYE_NOSE = 'HEAD_EYE_NOSE'
    HEAD_MOUTH = 'HEAD_MOUTH'
    ARM_GLANCE = 'ARM_GLANCE'
    ARM_SHOULDER = 'ARM_SHOULDER'
    ARM_UPPER_ARM_FLESH = 'ARM_UPPER_ARM_FLESH'
    ARM_UPPER_ARM_BONE = 'ARM_UPPER_ARM_BONE'
    ARM_FOREARM_FLESH = 'ARM_FOREARM_FLESH'
    ARM_FOREARM_BONE = 'ARM_FOREARM_BONE'
    ARM_HAND = 'ARM_HAND'
    ARM_WEAPON = 'ARM_WEAPON'
    BODY_GLANCE = 'BODY_GLANCE'
    BODY_CHEST = 'BODY_CHEST'
    BODY_BASE_OF_NECK = 'BODY_BASE_OF_NECK'
    BODY_HEART = 'BODY_HEART'
    BODY_SPINE = 'BODY_SPINE'
    BODY_ABDOMEN = 'BODY_ABDOMEN'
    BODY_PELVIS = 'BODY_PELVIS'
    LEG_GLANCE = 'LEG_GLANCE'
    LEG_THIGH_FLESH = 'LEG_THIGH_FLESH'
    LEG_THIGH_BONE = 'LEG_THIGH_BONE'
    LEG_SHIN_FOOT = 'LEG_SHIN_FOOT'

class AdvancedHitLocation(Enum):
    """
    Hit Locations including Left/Right separation for applicable limbs.
    """
    HEAD_GLANCE = "Head Glance"
    FOREHEAD = "Forehead"
    EYE_NOSE = "Eye - Nose"
    MOUTH = "Mouth"
    NECK_FLESH = "Neck - Flesh"
    NECK_THROAT = "Neck - Throat"

    # Shoulders
    SHOULDER_GLANCE_LEFT = "Shoulder Glance (Left)"
    SHOULDER_GLANCE_RIGHT = "Shoulder Glance (Right)"

    SHOULDER_SOCKET_LEFT = "Shoulder Socket (Left)"
    SHOULDER_SOCKET_RIGHT = "Shoulder Socket (Right)"

    SHOULDER_LEFT = "Shoulder (Left)"
    SHOULDER_RIGHT = "Shoulder (Right)"

    # Arms
    ARM_GLANCE_LEFT = "Arm Glance (Left)"
    ARM_GLANCE_RIGHT = "Arm Glance (Right)"

    ARM_GLANCE_SHOULDER_LEFT = "Arm Glance - Shoulder (Left)"
    ARM_GLANCE_SHOULDER_RIGHT = "Arm Glance - Shoulder (Right)"

    ARM_FLESH_LEFT = "Arm Flesh (Left)"
    ARM_FLESH_RIGHT = "Arm Flesh (Right)"

    ARM_FLESH_SHOULDER_LEFT = "Arm Flesh - Shoulder (Left)"
    ARM_FLESH_SHOULDER_RIGHT = "Arm Flesh - Shoulder (Right)"

    ARM_BONE_SHOULDER_LEFT = "Arm Bone - Shoulder (Left)"
    ARM_BONE_SHOULDER_RIGHT = "Arm Bone - Shoulder (Right)"

    ELBOW_SHOULDER_LEFT = "Elbow - Shoulder (Left)"
    ELBOW_SHOULDER_RIGHT = "Elbow - Shoulder (Right)"

    FOREARM_FLESH_LUNG_LEFT = "Forearm Flesh - Lung (Left)"
    FOREARM_FLESH_LUNG_RIGHT = "Forearm Flesh - Lung (Right)"

    FOREARM_BONE_LUNG_LEFT = "Forearm Bone - Lung (Left)"
    FOREARM_BONE_LUNG_RIGHT = "Forearm Bone - Lung (Right)"

    HAND_BASE_OF_NECK_LEFT = "Hand - Base of Neck (Left)"
    HAND_BASE_OF_NECK_RIGHT = "Hand - Base of Neck (Right)"

    WEAPON_CRITICAL = "Weapon Critical"
    TORSO_GLANCE = "Torso Glance"
    BASE_OF_NECK = "Base of Neck"

    LUNG_RIB = "Lung - Rib"
    LUNG = "Lung"
    HEART = "Heart"
    LIVER_RIB = "Liver - Rib"
    LIVER = "Liver"
    STOMACH_RIB = "Stomach - Rib"
    STOMACH = "Stomach"
    STOMACH_SPLEEN = "Stomach - Spleen"
    STOMACH_KIDNEY = "Stomach - Kidney"
    LIVER_KIDNEY = "Liver - Kidney"
    LIVER_SPINE = "Liver - Spine"
    INTESTINES = "Intestines"
    SPINE = "Spine"
    PELVIS = "Pelvis"

    # Legs
    HIP_SOCKET_LEFT = "Hip Socket (Left)"
    HIP_SOCKET_RIGHT = "Hip Socket (Right)"

    LEG_GLANCE_LEFT = "Leg Glance (Left)"
    LEG_GLANCE_RIGHT = "Leg Glance (Right)"

    THIGH_FLESH_LEFT = "Thigh Flesh (Left)"
    THIGH_FLESH_RIGHT = "Thigh Flesh (Right)"

    THIGH_BONE_LEFT = "Thigh Bone (Left)"
    THIGH_BONE_RIGHT = "Thigh Bone (Right)"

    KNEE_LEFT = "Knee (Left)"
    KNEE_RIGHT = "Knee (Right)"

    SHIN_FLESH_LEFT = "Shin Flesh (Left)"
    SHIN_FLESH_RIGHT = "Shin Flesh (Right)"

    SHIN_BONE_LEFT = "Shin Bone (Left)"
    SHIN_BONE_RIGHT = "Shin Bone (Right)"

    FOOT_LEFT = "Foot (Left)"
    FOOT_RIGHT = "Foot (Right)"

    MISS = "Miss"

class MedicalAid(Enum):
    NO_AID = "No Aid"
    FIRST_AID = "First Aid"
    AID_STATION = "Aid Station"
    FIELD_HOSPITAL = "Field Hospital"
    TRAUMA_CENTER = "Trauma Center"

class ShotType(Enum):
    SINGLE = "SINGLE"
    BURST = "BURST"

class SituationStanceModifier4B(Enum):
    """
    Enum for Situation & Stance Modifiers (Table 4B).
    Values represent ALM (Aim Level Modifier) adjustments.
    """
    STANDING = 0  # Standing (standing & braced +4)
    STANDING_AND_BRACED = 4
    KNEELING = 3  # Kneeling (kneeling & braced +5)
    KNEELING_AND_BRACED = 5
    PRONE = 6  # Prone (prone & braced +7)
    PRONE_AND_BRACED = 7
    USING_SLING_FOR_SUPPORT_WHEN_AIM_TIME_GT_7 = 1  # Using Sling for Support (Aim Time >7)
    FIRING_FROM_THE_HIP = -6
    FIRING_RIFLE_WITH_ONE_HAND = -7
    FIRING_PISTOL_WITH_ONE_HAND = -4
    FOLDING_STOCK_NOT_USED = -4
    FIRING_PISTOL_DOUBLE_ACTION = -3
    DEPLOYED_BIPOD_NOT_BRACED = -2
    BIPOD_MOUNTED_WEAPON = 3
    TRIPOD_MOUNTED_WEAPON = 5
    TURRET_MOUNTED_WEAPON = 11
    PISTOL_WITH_SHOULDER_STOCK = 3

class VisibilityModifier4C(Enum):
    """
    Enum for Visibility Modifiers (Table 4C).
    Values represent ALM (Aim Level Modifier) adjustments.
    """
    GOOD_VISIBILITY = 0
    DUSK = -2
    NIGHT_FULL_MOON = -4
    HALF_MOON = -6
    NO_MOON = -12
    FIRING_AT_MUZZLE_FLASH = -10
    SMOKE_HAZE_FOG = -6  # Smoke, Haze, Fog
    LOOKING_INTO_A_LIGHT = -8
    OPTICAL_SCOPE_UNDER_8_HEXES = -6
    OPTICAL_SCOPE_BROKEN = -4
    ADVANCED_AIMING_SYSTEM_BROKEN = -8
    WEAPON_SIGHTS_BROKEN = -4
    FIRING_FROM_TEARGAS_NO_MASK = -8  # Firing from Teargas, No Mask
    SHOOTER_NOT_LOOKING = -14

class AccuracyModifiers(Enum):
    """
    Enum for Accuracy Modifiers types (Table 4E columns).
    """
    TARGET_SIZE = "TARGET_SIZE"
    AUTO_ELEV = "AUTO_ELEV"
    AUTO_WIDTH = "AUTO_WIDTH"

class AmmoFeedDevice(Enum):
    """Type of ammunition feed device."""
    MAGAZINE = "Magazine"
    BELT = "Belt"
    DRUM = "Drum"
    ROUND = "Round"