from phoenix_command.models.enums import AdvancedHitLocation, ArmorMaterial
from phoenix_command.models.gear import Armor, ArmorProtectionData, ArmorLayer

iotv_front_vital = [
    AdvancedHitLocation.LUNG,
    AdvancedHitLocation.LUNG_RIB,
    AdvancedHitLocation.HEART,
    AdvancedHitLocation.STOMACH_RIB,
    AdvancedHitLocation.STOMACH_SPLEEN,
    AdvancedHitLocation.STOMACH_KIDNEY,
    AdvancedHitLocation.STOMACH,
    AdvancedHitLocation.LIVER_RIB,
    AdvancedHitLocation.LIVER,
    AdvancedHitLocation.LIVER_KIDNEY,
    AdvancedHitLocation.SPINE,
    AdvancedHitLocation.LIVER_SPINE,
]
iotv_back_vital = [
    AdvancedHitLocation.LUNG,
    AdvancedHitLocation.LUNG_RIB,
    AdvancedHitLocation.HEART,
    AdvancedHitLocation.STOMACH_RIB,
    AdvancedHitLocation.STOMACH_SPLEEN,
    AdvancedHitLocation.STOMACH_KIDNEY,
    AdvancedHitLocation.STOMACH,
    AdvancedHitLocation.LIVER_RIB,
    AdvancedHitLocation.LIVER,
    AdvancedHitLocation.LIVER_KIDNEY,
    AdvancedHitLocation.SPINE,
    AdvancedHitLocation.LIVER_SPINE,
]
iotv_front_soft = [
    AdvancedHitLocation.SHOULDER_LEFT,
    AdvancedHitLocation.SHOULDER_RIGHT,
    AdvancedHitLocation.TORSO_GLANCE,
    AdvancedHitLocation.INTESTINES,
    AdvancedHitLocation.INTESTINES_SPINE_SIDE,
    AdvancedHitLocation.INTESTINES_SIDE,
]
iotv_back_soft = [
    AdvancedHitLocation.SHOULDER_LEFT,
    AdvancedHitLocation.SHOULDER_RIGHT,
    AdvancedHitLocation.TORSO_GLANCE,
    AdvancedHitLocation.INTESTINES,
    AdvancedHitLocation.INTESTINES_SPINE_SIDE,
    AdvancedHitLocation.INTESTINES_SIDE,
]
side_plate_locs = [
    AdvancedHitLocation.LUNG_SIDE,
    AdvancedHitLocation.LUNG_RIB_SIDE,
    AdvancedHitLocation.SPINE_SIDE,
    AdvancedHitLocation.SPLEEN_LIVER_SIDE,
    AdvancedHitLocation.KIDNEY_SPINE_SIDE,
    AdvancedHitLocation.STOMACH_LIVER_SIDE,
    AdvancedHitLocation.HEART_SIDE,
]

collar_locs = [
    AdvancedHitLocation.NECK_FLESH,
    AdvancedHitLocation.NECK_THROAT,
    AdvancedHitLocation.NECK_THROAT_SIDE,
    AdvancedHitLocation.BASE_OF_SKULL_SIDE,
    AdvancedHitLocation.BASE_OF_NECK,
    AdvancedHitLocation.NECK_SPINE_SIDE,
]

groin_locs = [
    AdvancedHitLocation.PELVIS,
    AdvancedHitLocation.HIP_SOCKET_LEFT,
    AdvancedHitLocation.HIP_SOCKET_RIGHT
]

daps_locs = [
    AdvancedHitLocation.SHOULDER_LEFT,
    AdvancedHitLocation.SHOULDER_RIGHT,
    AdvancedHitLocation.SHOULDER_SOCKET_LEFT,
    AdvancedHitLocation.SHOULDER_SOCKET_RIGHT,
    AdvancedHitLocation.ARM_FLESH_SHOULDER_LEFT,
    AdvancedHitLocation.ARM_FLESH_SHOULDER_RIGHT,
    AdvancedHitLocation.ARM_BONE_SHOULDER_LEFT,
    AdvancedHitLocation.ARM_BONE_SHOULDER_RIGHT,
    AdvancedHitLocation.SHOULDER_SOCKET_LUNG_SIDE,
]

upper_legs_locs = [
    AdvancedHitLocation.THIGH_FLESH_LEFT,
    AdvancedHitLocation.THIGH_FLESH_RIGHT,
    AdvancedHitLocation.THIGH_BONE_LEFT,
    AdvancedHitLocation.THIGH_BONE_RIGHT,
    AdvancedHitLocation.HIP_SOCKET_SIDE
]

leba_locs = [
    AdvancedHitLocation.SHIN_FLESH_LEFT,
    AdvancedHitLocation.SHIN_FLESH_RIGHT,
    AdvancedHitLocation.SHIN_BONE_LEFT,
    AdvancedHitLocation.SHIN_BONE_RIGHT,
    AdvancedHitLocation.KNEE_LEFT,
    AdvancedHitLocation.KNEE_RIGHT,
    AdvancedHitLocation.SHIN_FLESH_SIDE_LEFT,
    AdvancedHitLocation.SHIN_FLESH_SIDE_RIGHT
]


iotv = Armor(
    name="IOTV Gen IV (w/ ESAPI)",
    weight=30.0,
    description="Базовый жилет IOTV с передней и задней плитами ESAPI. NIJ IV / ГОСТ 6.",
    protection={
        **{(loc, True): ArmorProtectionData(layers=[
            ArmorLayer(ArmorMaterial.KEVLAR, protection_factor=4, blunt_protection_factor=1),
            ArmorLayer(ArmorMaterial.UHMWPE, protection_factor=6, blunt_protection_factor=5),
            ArmorLayer(ArmorMaterial.BORON_CARBIDE, protection_factor=19, blunt_protection_factor=1)
        ]) for loc in iotv_front_vital},
        **{(loc, True): ArmorProtectionData(layers=[
            ArmorLayer(ArmorMaterial.KEVLAR, protection_factor=4, blunt_protection_factor=1)
        ]) for loc in iotv_front_soft},
        **{(loc, False): ArmorProtectionData(layers=[
            ArmorLayer(ArmorMaterial.KEVLAR, protection_factor=4, blunt_protection_factor=1),
            ArmorLayer(ArmorMaterial.UHMWPE, protection_factor=6, blunt_protection_factor=5),
            ArmorLayer(ArmorMaterial.BORON_CARBIDE, protection_factor=19, blunt_protection_factor=1)
        ]) for loc in iotv_back_vital},
        **{(loc, False): ArmorProtectionData(layers=[
            ArmorLayer(ArmorMaterial.KEVLAR, protection_factor=4, blunt_protection_factor=1)
        ]) for loc in iotv_back_soft},
    }
)

collar = Armor(
    name="IOTV Collar & Throat",
    weight=1.5,
    description="Защита шеи и горла. NIJ IIIA / ГОСТ 2.",
    protection={
        # Защищает и спереди и сзади одинаково
        **{(loc, is_front): ArmorProtectionData(layers=[
            ArmorLayer(ArmorMaterial.KEVLAR, protection_factor=6, blunt_protection_factor=4)
        ]) for loc in leba_locs for is_front in [True, False]}
    }
)

armor = [
    iotv,
    collar,
]
