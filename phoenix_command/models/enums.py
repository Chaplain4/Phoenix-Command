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
    LOOKING_OVER_COVER = -4         # Look Over/Around
    FIRING_OVER_COVER = 0           # Fire Over/Around
    STANDING_EXPOSED = 7            # Standing Exposed (updated to match table)
    KNEELING_EXPOSED = 6            # Kneeling Exposed
    PRONE_EXPOSED = 2               # Prone / Crawl
    RUNNING = 8                     # Running
    LOW_CROUCH = 7                  # Low Crouch
    HANDS_AND_KNEES_CROUCH = 6      # Hands and Knees
    LOW_PRONE = 1                   # Low Prone
    HEAD = -3                       # Head
    BODY = 5                        # Body
    LEGS = 4                        # Legs
    ARMS = 3                        # Arms

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
    Hit Locations including Left/Right separation and correct Damage Table references.
    Format: "Location Name (Table X)" or "Location Name (Table X & Y)"
    Source: Table 4E (Damage Table Number column)
    """
    # --- HEAD ---
    HEAD_GLANCE = "Head Glance (Table 1)"
    SKULL_SIDE = "Skull (Table 41)"
    FOREHEAD = "Forehead (Table 2)"
    FOREHEAD_SIDE = "Forehead (Table 41)"  # New for Oblique
    EYE_NOSE = "Eye - Nose (Table 3)"
    EYE_SIDE = "Eye (Table 42)"
    MOUTH = "Mouth (Table 4)"
    JAW_SIDE = "Jaw (Table 43)"
    NECK_FLESH = "Neck - Flesh (Table 5)"
    NECK_THROAT = "Neck - Throat (Table 6)"
    BASE_OF_SKULL_SIDE = "Base of Skull (Table 44)"
    NECK_THROAT_SIDE = "Neck - Throat (Table 45)"  # New for Oblique
    NECK_SPINE_SIDE = "Neck - Spine (Table 46)"  # New for Oblique

    # --- SHOULDERS ---
    # Table 7
    SHOULDER_GLANCE_LEFT = "Shoulder Glance (Left) (Table 7)"
    SHOULDER_GLANCE_RIGHT = "Shoulder Glance (Right) (Table 7)"

    # Table 8
    SHOULDER_SOCKET_LEFT = "Shoulder Socket (Left) (Table 8)"
    SHOULDER_SOCKET_RIGHT = "Shoulder Socket (Right) (Table 8)"
    SHOULDER_SOCKET_LUNG_SIDE = "Shoulder Socket - Lung (Table 47)"
    SHOULDER_SOCKET_SPINE_SIDE = "Shoulder Socket - Spine (Table 48)"

    # Table 9
    SHOULDER_LEFT = "Shoulder (Left) (Table 9)"
    SHOULDER_RIGHT = "Shoulder (Right) (Table 9)"

    # --- ARMS ---
    # Table 10
    ARM_GLANCE_LEFT = "Arm Glance (Left) (Table 10)"
    ARM_GLANCE_RIGHT = "Arm Glance (Right) (Table 10)"

    # Tables 10 & 9
    ARM_GLANCE_SHOULDER_LEFT = "Arm Glance - Shoulder (Left) (Table 10 & 9)"
    ARM_GLANCE_SHOULDER_RIGHT = "Arm Glance - Shoulder (Right) (Table 10 & 9)"

    # Table 11
    ARM_FLESH_LEFT = "Arm Flesh (Left) (Table 11)"
    ARM_FLESH_RIGHT = "Arm Flesh (Right) (Table 11)"
    # Specific Oblique Logic (Table 11) - No Left/Right split in table rows, distinct ranges
    ARM_FLESH_OFF_SIDE = "Arm Flesh Off Side (Table 11)"
    ARM_FLESH_SHOT_SIDE = "Arm Flesh Shot Side (Table 11 & 19)"

    # Tables 11 & 9
    ARM_FLESH_SHOULDER_LEFT = "Arm Flesh - Shoulder (Left) (Table 11 & 9)"
    ARM_FLESH_SHOULDER_RIGHT = "Arm Flesh - Shoulder (Right) (Table 11 & 9)"

    # Tables 12 & 9
    ARM_BONE_LEFT = "Arm Bone (Left) (Table 12)"
    ARM_BONE_RIGHT = "Arm Bone (Right) (Table 12)"
    ARM_BONE_SHOULDER_LEFT = "Arm Bone - Shoulder (Left) (Table 12 & 9)"
    ARM_BONE_SHOULDER_RIGHT = "Arm Bone - Shoulder (Right) (Table 12 & 9)"
    # Specific Oblique Logic (Table 12)
    ARM_BONE_OFF_SIDE = "Arm Bone Off Side (Table 12)"
    ARM_BONE_SHOT_SIDE = "Arm Bone Shot Side (Table 12 & 19)"

    # Tables 13 & 9
    ELBOW_SHOULDER_LEFT = "Elbow - Shoulder (Left) (Table 13 & 9)"
    ELBOW_SHOULDER_RIGHT = "Elbow - Shoulder (Right) (Table 13 & 9)"
    ELBOW_LEFT = "Elbow (Table 13)"  # Generic for Oblique where Shoulder isn't mentioned
    ELBOW_RIGHT = "Elbow (Table 13)"

    # Tables 14 & 19
    FOREARM_FLESH_LUNG_LEFT = "Forearm Flesh - Lung (Left) (Table 14 & 19)"
    FOREARM_FLESH_LUNG_RIGHT = "Forearm Flesh - Lung (Right) (Table 14 & 19)"
    FOREARM_FLESH_LEFT = "Forearm Flesh (Table 14)"  # Oblique generic
    FOREARM_FLESH_RIGHT = "Forearm Flesh (Table 14)"

    # Tables 15 & 19
    FOREARM_BONE_LUNG_LEFT = "Forearm Bone - Lung (Left) (Table 15 & 19)"
    FOREARM_BONE_LUNG_RIGHT = "Forearm Bone - Lung (Right) (Table 15 & 19)"
    FOREARM_BONE_LEFT = "Forearm Bone (Table 15)"  # Oblique generic
    FOREARM_BONE_RIGHT = "Forearm Bone (Table 15)"

    # Tables 16 & 18
    HAND_BASE_OF_NECK_LEFT = "Hand - Base of Neck (Left) (Table 16 & 18)"
    HAND_BASE_OF_NECK_RIGHT = "Hand - Base of Neck (Right) (Table 16 & 18)"
    HAND_LEFT = "Hand (Table 16)"  # Oblique generic
    HAND_RIGHT = "Hand (Table 16)"
    HAND_WEAPON_CRITICAL = "Hand - Weapon Critical (Table 16 & Weapon)"

    # --- TORSO / ORGANS ---
    WEAPON_CRITICAL = "Weapon Critical (Weapon)"
    TORSO_GLANCE = "Torso Glance (Table 17)"
    BASE_OF_NECK = "Base of Neck (Table 18)"

    LUNG_RIB = "Lung - Rib (Table 19)"
    LUNG = "Lung (Table 20)"
    HEART = "Heart (Table 21)"
    LIVER_RIB = "Liver - Rib (Table 22)"
    LIVER = "Liver (Table 23)"
    STOMACH_RIB = "Stomach - Rib (Table 24)"
    STOMACH = "Stomach (Table 25)"
    STOMACH_SPLEEN = "Stomach - Spleen (Table 26)"
    STOMACH_KIDNEY = "Stomach - Kidney (Table 27)"
    LIVER_KIDNEY = "Liver - Kidney (Table 28)"
    LIVER_SPINE = "Liver - Spine (Table 29)"
    INTESTINES = "Intestines (Table 30)"
    SPINE = "Spine (Table 31)"
    PELVIS = "Pelvis (Table 32)"
    LUNG_SIDE = "Lung (Table 50)"
    LUNG_RIB_SIDE = "Lung - Rib (Table 49)"
    HEART_RIB_SIDE = "Heart - Rib (Table 51)"
    HEART_SIDE = "Heart (Table 52)"
    SPINE_SIDE = "Spine (Table 53)"
    STOMACH_LIVER_RIB_SIDE = "Stomach - Liver - Rib (Table 54)"
    STOMACH_LIVER_SIDE = "Stomach - Liver (Table 55)"
    SPLEEN_LIVER_SIDE = "Spleen - Liver (Table 56)"
    KIDNEY_SPINE_SIDE = "Kidney - Spine (Table 57)"
    INTESTINES_SIDE = "Intestines (Table 58)"
    INTESTINES_SPINE_SIDE = "Intestines - Spine (Table 59)"
    PELVIS_SIDE = "Pelvis (Table 60)"

    # --- LEGS ---
    # Table 33
    HIP_SOCKET_LEFT = "Hip Socket (Left) (Table 33)"
    HIP_SOCKET_RIGHT = "Hip Socket (Right) (Table 33)"
    HIP_SPINE_SIDE = "Hip - Spine (Table 61)"
    HIP_SOCKET_SIDE = "Hip Socket (Table 62)"

    # Table 34
    LEG_GLANCE_LEFT = "Leg Glance (Left) (Table 34)"
    LEG_GLANCE_RIGHT = "Leg Glance (Right) (Table 34)"

    # Table 35
    THIGH_FLESH_LEFT = "Thigh Flesh (Left) (Table 35)"
    THIGH_FLESH_RIGHT = "Thigh Flesh (Right) (Table 35)"
    THIGH_FLESH_THIGH_FLESH = "Thigh Flesh - Thigh Flesh (Table 35 & 35)"
    THIGH_FLESH_THIGH_BONE = "Thigh Flesh - Thigh Bone (Table 35 & 36)"

    # Table 36
    THIGH_BONE_LEFT = "Thigh Bone (Left) (Table 36)"
    THIGH_BONE_RIGHT = "Thigh Bone (Right) (Table 36)"

    # Table 37
    KNEE_LEFT = "Knee (Left) (Table 37)"
    KNEE_RIGHT = "Knee (Right) (Table 37)"

    # Table 38
    SHIN_FLESH_LEFT = "Shin Flesh (Left) (Table 38)"
    SHIN_FLESH_RIGHT = "Shin Flesh (Right) (Table 38)"
    # Table 63 (Side)
    SHIN_FLESH_SIDE_LEFT = "Shin Flesh (Left) (Table 63)"  # Oblique
    SHIN_FLESH_SIDE_RIGHT = "Shin Flesh (Right) (Table 63)"  # Oblique

    # Table 39
    SHIN_BONE_LEFT = "Shin Bone (Left) (Table 39)"
    SHIN_BONE_RIGHT = "Shin Bone (Right) (Table 39)"
    # Table 64 (Side)
    SHIN_BONE_SIDE_LEFT = "Shin Bone (Left) (Table 64)"  # Oblique
    SHIN_BONE_SIDE_RIGHT = "Shin Bone (Right) (Table 64)"  # Oblique

    # Table 40
    FOOT_LEFT = "Foot (Left) (Table 40)"
    FOOT_RIGHT = "Foot (Right) (Table 40)"

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

class ArmorMaterial(Enum):
    """
    Armor material types with different degradation characteristics.
    Materials affect armor protection degradation on hit and penetration.

    Each material has:
    - name: Material name
    - degradation_on_hit: Protection degradation % on non-penetrating hit
    - degradation_on_penetration: Protection degradation % when penetrated
    - global_degradation: If True, damage affects entire armor piece, not just hit location
    """
    # (name, degradation_on_hit %, degradation_on_penetration %, global_degradation)
    KEVLAR = ("Kevlar", 5.0, 10.0, False)
    UHMWPE = ("UHMWPE", 5.0, 10.0, False)  # Ultra-High-Molecular-Weight Polyethylene
    STEEL = ("Steel", 0.0, 5.0, False)
    TITANIUM = ("Titanium", 0.0, 5.0, False)
    SILICON_CARBIDE = ("Silicon Carbide", 20.0, 25.0, True)  # Ceramic - shatters affect whole plate
    BORON_CARBIDE = ("Boron Carbide", 35.0, 45.0, True)  # Ceramic - shatters affect whole plate

    def __init__(self, display_name: str, degradation_on_hit: float, degradation_on_penetration: float, global_degradation: bool):
        self._display_name = display_name
        self._degradation_on_hit = degradation_on_hit
        self._degradation_on_penetration = degradation_on_penetration
        self._global_degradation = global_degradation

    @property
    def display_name(self) -> str:
        """Display name of the material."""
        return self._display_name

    @property
    def degradation_on_hit(self) -> float:
        """Protection degradation percentage on non-penetrating hit."""
        return self._degradation_on_hit

    @property
    def degradation_on_penetration(self) -> float:
        """Protection degradation percentage when armor is penetrated."""
        return self._degradation_on_penetration

    @property
    def global_degradation(self) -> bool:
        """Whether damage affects entire armor piece or just the hit location."""
        return self._global_degradation


class Caliber(Enum):
    """Weapon caliber types."""
    # Pistol calibers
    CAL_32_ACP = ".32 ACP"
    CAL_9MM_PARABELLUM = "9mm Parabellum"
    CAL_9X18_MAKAROV = "9 x 18mm"
    CAL_45_ACP = ".45 ACP"
    CAL_545X18 = "5.45 x 18mm"
    CAL_762X25 = "7.62 x 25mm"

    # Rifle calibers
    CAL_556_NATO = "5.56mm NATO"
    CAL_545X39 = "5.45 x 39.5mm"
    CAL_762_NATO = "7.62mm NATO"
    CAL_762X39 = "7.62 x 39mm"
    CAL_75_FRENCH = "7.5 x 54mm"
    CAL_47_CASELESS = "4.7mm Caseless"
    CAL_300_WIN_MAG = "300 Winchester Magnum"
    CAL_762X54R = "7.62 x 54mm"
    CAL_127X107 = "12.7 x 107mm"
    CAL_50_BMG = ".50 Browning"

    # Shotgun calibers
    CAL_12_GAUGE = "12 Gauge"
    CAL_20_GAUGE = "20 Gauge"

    #Grenade calibers
    CAL_40x46MM = "40 x 46mm Grenade"
    CAL_40x53MM = "40 x 53mm Grenade"
    CAL_30MM_VOG = "30mm VOG Grenade"
    CAL_64MM = "64mm Rocket-Propelled Grenade"
    CAL_66MM = "66mm Rocket-Propelled Grenade"
    CAL_67MM = "67mm Rocket-Propelled Grenade"
    CAL_85MM = "85mm Rocket-Propelled Grenade"
    CAL_94MM = "94mm Rocket-Propelled Grenade"

class WeaponType(Enum):
    """Weapon type classifications."""
    ROCKET_PROPELLED_GRENADE_LAUNCHER = "Rocket Propelled Grenade Launcher"
    ROCKET_PROPELLED_GRENADE = "Rocket Propelled Grenade"
    AUTOMATIC_GRENADE_LAUNCHER = "Automatic grenade launcher"
    AUTOMATIC_PISTOL = "Automatic Pistol"
    SUB_MACHINEGUN = "Sub-Machinegun"
    ASSAULT_RIFLE = "Assault Rifle"
    BATTLE_RIFLE = "Battle Rifle"
    CARBINE = "Carbine"
    SNIPER_RIFLE = "Sniper Rifle"
    MACHINE_GUN = "Machine Gun"
    HEAVY_MACHINE_GUN = "Heavy Machine Gun"
    LIGHT_MACHINE_GUN = "Light Machine Gun"
    SHOTGUN = "Shotgun"
    GRENADE_LAUNCHER = "Grenade Launcher"


class Country(Enum):
    """Countries of weapon origin."""
    HUNGARY = "Hungary"
    ARGENTINA = "Argentina"
    AUSTRALIA = "Australia"
    AUSTRIA = "Austria"
    BELGIUM = "Belgium"
    CHINA = "China"
    CZECHOSLOVAKIA = "Czechoslovakia"
    FRANCE = "France"
    WEST_GERMANY = "West Germany"
    ISRAEL = "Israel"
    ITALY = "Italy"
    JAPAN = "Japan"
    SOUTH_AFRICA = "South Africa"
    USSR = "USSR"
    SWITZERLAND = "Switzerland"
    UK = "UK"
    USA = "USA"

