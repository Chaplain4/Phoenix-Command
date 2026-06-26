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
helmet_locs = [
    AdvancedHitLocation.HEAD_GLANCE,
    AdvancedHitLocation.SKULL_SIDE,
    AdvancedHitLocation.FOREHEAD,
    AdvancedHitLocation.FOREHEAD_SIDE,
]


# --- US ---

iotv = Armor(
    name="IOTV Gen I (w/ ESAPI)",
    weight=30.0,
    description="Base IOTV vest with front and back ESAPI plates. NIJ IV / GOST 6.",
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
    description="Neck and throat protection. NIJ IIIA / GOST 2.",
    protection={
        **{(loc, is_front): ArmorProtectionData(layers=[
            ArmorLayer(ArmorMaterial.KEVLAR, protection_factor=4, blunt_protection_factor=1)
        ]) for loc in collar_locs for is_front in [True, False]}
    }
)

side_plates = Armor(
    name="IOTV Side Plate Carriers",
    weight=6.0,
    description="Side ballistic plates for torso protection. NIJ IIIa / GOST 2.",
    protection={
        **{(loc, is_front): ArmorProtectionData(layers=[
            ArmorLayer(ArmorMaterial.KEVLAR, protection_factor=4, blunt_protection_factor=1),
            ArmorLayer(ArmorMaterial.UHMWPE, protection_factor=6, blunt_protection_factor=5)
        ]) for loc in side_plate_locs for is_front in [True, False]}
    }
)

groin_protector = Armor(
    name="Groin Protector",
    weight=2.0,
    description="Pelvic and groin area protection. NIJ IIIA / GOST 2.",
    protection={
        **{(loc, is_front): ArmorProtectionData(layers=[
            ArmorLayer(ArmorMaterial.KEVLAR, protection_factor=4, blunt_protection_factor=1),
            ArmorLayer(ArmorMaterial.UHMWPE, protection_factor=6, blunt_protection_factor=5)
        ]) for loc in groin_locs for is_front in [True, False]}
    }
)

daps = Armor(
    name="DAPS (Deltoid and Axillary Protection System)",
    weight=3.0,
    description="Shoulder and upper arm protection (pauldrons). NIJ IIIA / GOST 2.",
    protection={
        **{(loc, is_front): ArmorProtectionData(layers=[
            ArmorLayer(ArmorMaterial.KEVLAR, protection_factor=4, blunt_protection_factor=1),
        ]) for loc in daps_locs for is_front in [True, False]}
    }
)

upper_legs_protector = Armor(
    name="Upper Legs Protector",
    weight=4.0,
    description="Thigh protection (kevlar shorts). NIJ IIIA / GOST 2.",
    protection={
        **{(loc, is_front): ArmorProtectionData(layers=[
            ArmorLayer(ArmorMaterial.KEVLAR, protection_factor=4, blunt_protection_factor=1),
        ]) for loc in upper_legs_locs for is_front in [True, False]}
    }
)

leba = Armor(
    name="LEBA (Lower Extremity Body Armor)",
    weight=5.0,
    description="Lower leg and shin protection. NIJ IIIA / GOST 2.",
    protection={
        **{(loc, is_front): ArmorProtectionData(layers=[
            ArmorLayer(ArmorMaterial.KEVLAR, protection_factor=4, blunt_protection_factor=1),
        ]) for loc in leba_locs for is_front in [True, False]}
    }
)

msa_tc2002 = Armor(
    name="MSA TC-2002 Combat Helmet",
    weight=4.5,
    description="Ballistic combat helmet used by JSOC. Has additional side accessory rails and headphones. NIJ III / GOST 3.",
    protection={
        **{(loc, is_front): ArmorProtectionData(layers=[
            ArmorLayer(ArmorMaterial.UHMWPE, protection_factor=4, blunt_protection_factor=3),
        ]) for loc in helmet_locs for is_front in [True, False]}
    }
)

mich_tc2000 = Armor(
    name="MICH TC-2000 Combat Helmet",
    weight=4.5,
    description="Ballistic combat helmet widely used across armed force branches. NIJ III / GOST 3.",
    protection={
        **{(loc, is_front): ArmorProtectionData(layers=[
            ArmorLayer(ArmorMaterial.UHMWPE, protection_factor=4, blunt_protection_factor=3),
        ]) for loc in helmet_locs for is_front in [True, False]}
    }
)

# --- USSR/Russia ---

ratnik_6b45 = Armor(
    name="6B45 Ratnik Vest (w/ Granit plates)",
    weight=28.0,
    description="Russian Ratnik body armor with front and back Granit ceramic plates. NIJ IV / GOST 6.",
    protection={
        **{(loc, True): ArmorProtectionData(layers=[
            ArmorLayer(ArmorMaterial.KEVLAR, protection_factor=4, blunt_protection_factor=1),
            ArmorLayer(ArmorMaterial.UHMWPE, protection_factor=6, blunt_protection_factor=5),
            ArmorLayer(ArmorMaterial.SILICON_CARBIDE, protection_factor=19, blunt_protection_factor=1),
        ]) for loc in iotv_front_vital},
        **{(loc, True): ArmorProtectionData(layers=[
            ArmorLayer(ArmorMaterial.KEVLAR, protection_factor=4, blunt_protection_factor=1),
        ]) for loc in iotv_front_soft},
        **{(loc, False): ArmorProtectionData(layers=[
            ArmorLayer(ArmorMaterial.KEVLAR, protection_factor=4, blunt_protection_factor=1),
            ArmorLayer(ArmorMaterial.UHMWPE, protection_factor=6, blunt_protection_factor=5),
            ArmorLayer(ArmorMaterial.SILICON_CARBIDE, protection_factor=19, blunt_protection_factor=1),
        ]) for loc in iotv_back_vital},
        **{(loc, False): ArmorProtectionData(layers=[
            ArmorLayer(ArmorMaterial.KEVLAR, protection_factor=4, blunt_protection_factor=1),
        ]) for loc in iotv_back_soft},
    }
)

ratnik_6b45_collar = Armor(
    name="6B45 Ratnik Collar",
    weight=1.5,
    description="Neck and throat protection for Ratnik kit. NIJ IIIA / GOST 2.",
    protection={
        **{(loc, is_front): ArmorProtectionData(layers=[
            ArmorLayer(ArmorMaterial.KEVLAR, protection_factor=4, blunt_protection_factor=1),
        ]) for loc in collar_locs for is_front in [True, False]}
    }
)

ratnik_6b45_side_plates = Armor(
    name="6B45 Ratnik Side Plates",
    weight=5.5,
    description="Side ballistic plates for Ratnik torso protection. NIJ IIIa / GOST 2.",
    protection={
        **{(loc, is_front): ArmorProtectionData(layers=[
            ArmorLayer(ArmorMaterial.KEVLAR, protection_factor=4, blunt_protection_factor=1),
            ArmorLayer(ArmorMaterial.UHMWPE, protection_factor=6, blunt_protection_factor=5),
        ]) for loc in side_plate_locs for is_front in [True, False]}
    }
)

ratnik_6b45_groin = Armor(
    name="6B45 Ratnik Groin Protector",
    weight=2.0,
    description="Pelvic and groin area protection for Ratnik kit. NIJ IIIA / GOST 2.",
    protection={
        **{(loc, is_front): ArmorProtectionData(layers=[
            ArmorLayer(ArmorMaterial.KEVLAR, protection_factor=4, blunt_protection_factor=1),
            ArmorLayer(ArmorMaterial.UHMWPE, protection_factor=6, blunt_protection_factor=5),
        ]) for loc in groin_locs for is_front in [True, False]}
    }
)

ratnik_6b45_daps = Armor(
    name="6B45 Ratnik Shoulder Pads",
    weight=2.5,
    description="Shoulder and upper arm protection for Ratnik kit. NIJ IIIA / GOST 2.",
    protection={
        **{(loc, is_front): ArmorProtectionData(layers=[
            ArmorLayer(ArmorMaterial.KEVLAR, protection_factor=4, blunt_protection_factor=1),
        ]) for loc in daps_locs for is_front in [True, False]}
    }
)

ratnik_6b45_upper_legs = Armor(
    name="6B45 Ratnik Upper Legs Protector",
    weight=4.0,
    description="Thigh protection for Ratnik kit. NIJ IIIA / GOST 2.",
    protection={
        **{(loc, is_front): ArmorProtectionData(layers=[
            ArmorLayer(ArmorMaterial.KEVLAR, protection_factor=4, blunt_protection_factor=1),
        ]) for loc in upper_legs_locs for is_front in [True, False]}
    }
)

ratnik_6b45_leba = Armor(
    name="6B45 Ratnik Lower Legs Protector",
    weight=5.0,
    description="Lower leg and shin protection for Ratnik kit. NIJ IIIA / GOST 2.",
    protection={
        **{(loc, is_front): ArmorProtectionData(layers=[
            ArmorLayer(ArmorMaterial.KEVLAR, protection_factor=4, blunt_protection_factor=1),
        ]) for loc in leba_locs for is_front in [True, False]}
    }
)

helmet_6b47 = Armor(
    name="6B47 Ratnik Combat Helmet",
    weight=3.0,
    description="Aramid composite combat helmet of the Ratnik system. NIJ III / GOST 3.",
    protection={
        **{(loc, is_front): ArmorProtectionData(layers=[
            ArmorLayer(ArmorMaterial.UHMWPE, protection_factor=4, blunt_protection_factor=3),
        ]) for loc in helmet_locs for is_front in [True, False]}
    }
)

vest_6b23_1 = Armor(
    name="6B23-1 Vest (w/ DTO-4 plates)",
    weight=26.0,
    description="Early Russian body armor with titanium DTO-4 front and back plates. NIJ III / GOST 5.",
    protection={
        **{(loc, True): ArmorProtectionData(layers=[
            ArmorLayer(ArmorMaterial.KEVLAR, protection_factor=4, blunt_protection_factor=1),
            ArmorLayer(ArmorMaterial.TITANIUM, protection_factor=15, blunt_protection_factor=3),
        ]) for loc in iotv_front_vital},
        **{(loc, True): ArmorProtectionData(layers=[
            ArmorLayer(ArmorMaterial.KEVLAR, protection_factor=4, blunt_protection_factor=1),
        ]) for loc in iotv_front_soft},
        **{(loc, False): ArmorProtectionData(layers=[
            ArmorLayer(ArmorMaterial.KEVLAR, protection_factor=4, blunt_protection_factor=1),
            ArmorLayer(ArmorMaterial.TITANIUM, protection_factor=15, blunt_protection_factor=3),
        ]) for loc in iotv_back_vital},
        **{(loc, False): ArmorProtectionData(layers=[
            ArmorLayer(ArmorMaterial.KEVLAR, protection_factor=4, blunt_protection_factor=1),
        ]) for loc in iotv_back_soft},
    }
)

helmet_ssh_68 = Armor(
    name="SSh-68 Steel Helmet",
    weight=3.0,
    description="Soviet steel combat helmet. NIJ II / GOST 3.",
    protection={
        **{(loc, is_front): ArmorProtectionData(layers=[
            ArmorLayer(ArmorMaterial.STEEL, protection_factor=4, blunt_protection_factor=2),
        ]) for loc in helmet_locs for is_front in [True, False]}
    }
)

# --- France ---

vest_spectra = Armor(
    name="SPECTRA Vest (w/ plates)",
    weight=27.0,
    description="French SPECTRA body armor with ceramic composite plates. NIJ IV / GOST 6.",
    protection={
        **{(loc, True): ArmorProtectionData(layers=[
            ArmorLayer(ArmorMaterial.KEVLAR, protection_factor=4, blunt_protection_factor=1),
            ArmorLayer(ArmorMaterial.UHMWPE, protection_factor=6, blunt_protection_factor=5),
            ArmorLayer(ArmorMaterial.SILICON_CARBIDE, protection_factor=19, blunt_protection_factor=1),
        ]) for loc in iotv_front_vital},
        **{(loc, True): ArmorProtectionData(layers=[
            ArmorLayer(ArmorMaterial.KEVLAR, protection_factor=4, blunt_protection_factor=1),
        ]) for loc in iotv_front_soft},
        **{(loc, False): ArmorProtectionData(layers=[
            ArmorLayer(ArmorMaterial.KEVLAR, protection_factor=4, blunt_protection_factor=1),
            ArmorLayer(ArmorMaterial.UHMWPE, protection_factor=6, blunt_protection_factor=5),
            ArmorLayer(ArmorMaterial.SILICON_CARBIDE, protection_factor=19, blunt_protection_factor=1),
        ]) for loc in iotv_back_vital},
        **{(loc, False): ArmorProtectionData(layers=[
            ArmorLayer(ArmorMaterial.KEVLAR, protection_factor=4, blunt_protection_factor=1),
        ]) for loc in iotv_back_soft},
    }
)

helmet_hbh = Armor(
    name="HBH Combat Helmet (Casque balistique)",
    weight=3.2,
    description="French composite ballistic combat helmet. NIJ III / GOST 3.",
    protection={
        **{(loc, is_front): ArmorProtectionData(layers=[
            ArmorLayer(ArmorMaterial.UHMWPE, protection_factor=4, blunt_protection_factor=3),
        ]) for loc in helmet_locs for is_front in [True, False]}
    }
)

armor = [
    iotv,
    collar,
    side_plates,
    groin_protector,
    daps,
    upper_legs_protector,
    leba,
    msa_tc2002,
    mich_tc2000,
    ratnik_6b45,
    ratnik_6b45_collar,
    ratnik_6b45_side_plates,
    ratnik_6b45_groin,
    ratnik_6b45_daps,
    ratnik_6b45_upper_legs,
    ratnik_6b45_leba,
    helmet_6b47,
    vest_6b23_1,
    helmet_ssh_68,
    vest_spectra,
    helmet_hbh,
]
