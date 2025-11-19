"""Database of weapons with their ballistic characteristics."""

from phoenix_command.models.gear import Weapon, AmmoType, BallisticData, WeaponBallisticData, RangeData
from phoenix_command.models.enums import AmmoFeedDevice


# ============================================================================
# 5.56mm NATO ammunition types
# ============================================================================
ammo_556_fmj = AmmoType(
    name="5.56mm NATO Full Metal Jacket",
    abbreviation="FMJ",
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=15, damage_class=6),
        BallisticData(range_hexes=20, penetration=15, damage_class=6),
        BallisticData(range_hexes=40, penetration=13, damage_class=6),
        BallisticData(range_hexes=70, penetration=12, damage_class=6),
        BallisticData(range_hexes=100, penetration=10, damage_class=5),
        BallisticData(range_hexes=200, penetration=6.4, damage_class=4),
        BallisticData(range_hexes=300, penetration=4.1, damage_class=3),
        BallisticData(range_hexes=400, penetration=2.6, damage_class=2),
    ]
)

ammo_556_jhp = AmmoType(
    name="5.56mm NATO Jacketed Hollow Point",
    abbreviation="JHP",
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=15, damage_class=8),
        BallisticData(range_hexes=20, penetration=14, damage_class=8),
        BallisticData(range_hexes=40, penetration=13, damage_class=7),
        BallisticData(range_hexes=70, penetration=11, damage_class=7),
        BallisticData(range_hexes=100, penetration=9.7, damage_class=7),
        BallisticData(range_hexes=200, penetration=6.2, damage_class=6),
        BallisticData(range_hexes=300, penetration=3.9, damage_class=4),
        BallisticData(range_hexes=400, penetration=2.5, damage_class=3),
    ]
)

ammo_556_ap = AmmoType(
    name="5.56mm NATO Armor Piercing",
    abbreviation="AP",
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=21, damage_class=6),
        BallisticData(range_hexes=20, penetration=21, damage_class=6),
        BallisticData(range_hexes=40, penetration=19, damage_class=6),
        BallisticData(range_hexes=70, penetration=16, damage_class=5),
        BallisticData(range_hexes=100, penetration=14, damage_class=5),
        BallisticData(range_hexes=200, penetration=9.1, damage_class=4),
        BallisticData(range_hexes=300, penetration=5.7, damage_class=3),
        BallisticData(range_hexes=400, penetration=3.6, damage_class=2),
    ]
)

# ============================================================================
# 9mm Parabellum ammunition types
# ============================================================================
ammo_9mm_fmj = AmmoType(
    name="9mm Parabellum Full Metal Jacket",
    abbreviation="FMJ",
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=2.1, damage_class=3),
        BallisticData(range_hexes=20, penetration=1.9, damage_class=3),
        BallisticData(range_hexes=40, penetration=1.6, damage_class=3),
        BallisticData(range_hexes=70, penetration=1.3, damage_class=3),
        BallisticData(range_hexes=100, penetration=1.0, damage_class=3),
        BallisticData(range_hexes=200, penetration=0.4, damage_class=3),
        BallisticData(range_hexes=300, penetration=0.2, damage_class=3),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=3),
    ]
)

ammo_9mm_jhp = AmmoType(
    name="9mm Parabellum Jacketed Hollow Point",
    abbreviation="JHP",
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=2.0, damage_class=4),
        BallisticData(range_hexes=20, penetration=1.8, damage_class=4),
        BallisticData(range_hexes=40, penetration=1.6, damage_class=4),
        BallisticData(range_hexes=70, penetration=1.2, damage_class=4),
        BallisticData(range_hexes=100, penetration=1.0, damage_class=4),
        BallisticData(range_hexes=200, penetration=0.4, damage_class=4),
        BallisticData(range_hexes=300, penetration=0.2, damage_class=4),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=4),
    ]
)

ammo_9mm_ap = AmmoType(
    name="9mm Parabellum Armor Piercing",
    abbreviation="AP",
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=2.9, damage_class=3),
        BallisticData(range_hexes=20, penetration=2.7, damage_class=3),
        BallisticData(range_hexes=40, penetration=2.3, damage_class=3),
        BallisticData(range_hexes=70, penetration=1.8, damage_class=3),
        BallisticData(range_hexes=100, penetration=1.4, damage_class=3),
        BallisticData(range_hexes=200, penetration=0.6, damage_class=3),
        BallisticData(range_hexes=300, penetration=0.3, damage_class=3),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=3),
    ]
)

# ============================================================================
# 7.62 x 25mm ammunition types
# ============================================================================
ammo_762x25_fmj = AmmoType(
    name="7.62 x 25mm Full Metal Jacket",
    abbreviation="FMJ",
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=2.7, damage_class=3),
        BallisticData(range_hexes=20, penetration=2.5, damage_class=3),
        BallisticData(range_hexes=40, penetration=2.2, damage_class=3),
        BallisticData(range_hexes=70, penetration=1.7, damage_class=3),
        BallisticData(range_hexes=100, penetration=1.3, damage_class=3),
        BallisticData(range_hexes=200, penetration=0.6, damage_class=3),
        BallisticData(range_hexes=300, penetration=0.3, damage_class=3),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=3),
    ]
)

ammo_762x25_jhp = AmmoType(
    name="7.62 x 25mm Jacketed Hollow Point",
    abbreviation="JHP",
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=2.6, damage_class=5),
        BallisticData(range_hexes=20, penetration=2.4, damage_class=5),
        BallisticData(range_hexes=40, penetration=2.1, damage_class=5),
        BallisticData(range_hexes=70, penetration=1.6, damage_class=5),
        BallisticData(range_hexes=100, penetration=1.3, damage_class=5),
        BallisticData(range_hexes=200, penetration=0.6, damage_class=5),
        BallisticData(range_hexes=300, penetration=0.3, damage_class=5),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=5),
    ]
)

ammo_762x25_ap = AmmoType(
    name="7.62 x 25mm Armor Piercing",
    abbreviation="AP",
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=3.8, damage_class=3),
        BallisticData(range_hexes=20, penetration=3.6, damage_class=3),
        BallisticData(range_hexes=40, penetration=3.0, damage_class=3),
        BallisticData(range_hexes=70, penetration=2.4, damage_class=3),
        BallisticData(range_hexes=100, penetration=1.9, damage_class=3),
        BallisticData(range_hexes=200, penetration=0.9, damage_class=3),
        BallisticData(range_hexes=300, penetration=0.4, damage_class=3),
        BallisticData(range_hexes=400, penetration=0.2, damage_class=3),
    ]
)

# ============================================================================
# .32 ACP ammunition types
# ============================================================================
ammo_32acp_fmj = AmmoType(
    name=".32 ACP Full Metal Jacket",
    abbreviation="FMJ",
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=1.0, damage_class=1),
        BallisticData(range_hexes=20, penetration=0.9, damage_class=1),
        BallisticData(range_hexes=40, penetration=0.7, damage_class=1),
        BallisticData(range_hexes=70, penetration=0.5, damage_class=1),
        BallisticData(range_hexes=100, penetration=0.3, damage_class=1),
        BallisticData(range_hexes=200, penetration=0.1, damage_class=1),
    ]
)

ammo_32acp_jhp = AmmoType(
    name=".32 ACP Jacketed Hollow Point",
    abbreviation="JHP",
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=0.9, damage_class=2),
        BallisticData(range_hexes=20, penetration=0.8, damage_class=2),
        BallisticData(range_hexes=40, penetration=0.7, damage_class=2),
        BallisticData(range_hexes=70, penetration=0.5, damage_class=2),
        BallisticData(range_hexes=100, penetration=0.3, damage_class=2),
        BallisticData(range_hexes=200, penetration=0.1, damage_class=2),
    ]
)

ammo_32acp_ap = AmmoType(
    name=".32 ACP Armor Piercing",
    abbreviation="AP",
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=1.4, damage_class=1),
        BallisticData(range_hexes=20, penetration=1.2, damage_class=1),
        BallisticData(range_hexes=40, penetration=1.0, damage_class=1),
        BallisticData(range_hexes=70, penetration=0.7, damage_class=1),
        BallisticData(range_hexes=100, penetration=0.5, damage_class=1),
        BallisticData(range_hexes=200, penetration=0.2, damage_class=1),
    ]
)

# ============================================================================
# BALLISTIC DATA FOR WEAPONS
# ============================================================================

# SIG 550 ballistic data
sig_550_ballistic = WeaponBallisticData(
    three_round_burst=[
        RangeData(range_hexes=10, value=-6),
        RangeData(range_hexes=20, value=-1),
        RangeData(range_hexes=40, value=4),
        RangeData(range_hexes=70, value=8),
        RangeData(range_hexes=100, value=11),
        RangeData(range_hexes=200, value=16),
        RangeData(range_hexes=300, value=19),
        RangeData(range_hexes=400, value=21),
    ],
    minimum_arc=[
        RangeData(range_hexes=10, value=0.3),
        RangeData(range_hexes=20, value=0.6),
        RangeData(range_hexes=40, value=1),
        RangeData(range_hexes=70, value=2),
        RangeData(range_hexes=100, value=3),
        RangeData(range_hexes=200, value=6),
        RangeData(range_hexes=300, value=10),
        RangeData(range_hexes=400, value=13),
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=60),
        RangeData(range_hexes=20, value=51),
        RangeData(range_hexes=40, value=42),
        RangeData(range_hexes=70, value=35),
        RangeData(range_hexes=100, value=30),
        RangeData(range_hexes=200, value=20),
        RangeData(range_hexes=300, value=15),
        RangeData(range_hexes=400, value=11),
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=0),
        RangeData(range_hexes=20, value=0),
        RangeData(range_hexes=40, value=1),
        RangeData(range_hexes=70, value=1),
        RangeData(range_hexes=100, value=2),
        RangeData(range_hexes=200, value=5),
        RangeData(range_hexes=300, value=8),
        RangeData(range_hexes=400, value=11),
    ]
)

# 9mm Pistol ballistic data (for FN Mk 1 and MAB PA15)
pistol_9mm_ballistic = WeaponBallisticData(
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=46),
        RangeData(range_hexes=20, value=38),
        RangeData(range_hexes=40, value=29),
        RangeData(range_hexes=70, value=22),
        RangeData(range_hexes=100, value=17),
        RangeData(range_hexes=200, value=8),
        RangeData(range_hexes=300, value=2),
        RangeData(range_hexes=400, value=-1),
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=1),
        RangeData(range_hexes=20, value=1),
        RangeData(range_hexes=40, value=2),
        RangeData(range_hexes=70, value=4),
        RangeData(range_hexes=100, value=6),
        RangeData(range_hexes=200, value=15),
        RangeData(range_hexes=300, value=24),
        RangeData(range_hexes=400, value=35),
    ]
)

# 7.62 x 25mm Pistol ballistic data (for Type 51)
pistol_762x25_ballistic = WeaponBallisticData(
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=48),
        RangeData(range_hexes=20, value=40),
        RangeData(range_hexes=40, value=31),
        RangeData(range_hexes=70, value=24),
        RangeData(range_hexes=100, value=19),
        RangeData(range_hexes=200, value=10),
        RangeData(range_hexes=300, value=5),
        RangeData(range_hexes=400, value=1),
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=0),
        RangeData(range_hexes=20, value=1),
        RangeData(range_hexes=40, value=2),
        RangeData(range_hexes=70, value=3),
        RangeData(range_hexes=100, value=5),
        RangeData(range_hexes=200, value=12),
        RangeData(range_hexes=300, value=20),
        RangeData(range_hexes=400, value=29),
    ]
)

# .32 ACP Pistol ballistic data (for Walther PPK)
pistol_32acp_ballistic = WeaponBallisticData(
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=44),
        RangeData(range_hexes=20, value=36),
        RangeData(range_hexes=40, value=27),
        RangeData(range_hexes=70, value=19),
        RangeData(range_hexes=100, value=14),
        RangeData(range_hexes=200, value=5),
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=1),
        RangeData(range_hexes=20, value=1),
        RangeData(range_hexes=40, value=3),
        RangeData(range_hexes=70, value=5),
        RangeData(range_hexes=100, value=8),
        RangeData(range_hexes=200, value=20),
    ]
)

# ============================================================================
# WEAPONS
# ============================================================================

# SIG 550 Assault Rifle
sig_550 = Weapon(
    name="SIG 550",
    weight=10.1,
    description="Swiss-made SG 550 assault rifle, featuring excellent accuracy and reliability. "
                "Standard issue for Swiss Armed Forces. Gas-operated, selective-fire rifle with "
                "folding stock. Chambered in 5.56mm NATO with 30-round magazine capacity.",
    caliber="5.56mm NATO",
    weapon_type="Assault Rifle",
    country="Switzerland",
    length_deployed=39,
    length_folded=30,
    reload_time=7,
    rate_of_fire=7,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=7,
    ammo_capacity=30,
    ammo_weight=1.1,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=4,
    sustained_auto_burst=3,
    aim_time_modifiers={
        1: -23,
        2: -13,
        3: -9,
        4: -7,
        5: -6,
        6: -5,
        7: -4,
        8: -3,
        9: -2,
        10: -1,
        11: 0,
    },
    ammunition_types=[ammo_556_fmj, ammo_556_jhp, ammo_556_ap],
    ballistic_data=sig_550_ballistic
)

# FN Mk 1 (Browning High-Power)
fn_mk1 = Weapon(
    name="FN Mk 1",
    weight=2.3,
    description="Automatic Pistol, 9mm Parabellum, Belgium, Browning High-Power pistol. "
                "Manufactured & sold world-wide.",
    caliber="9mm Parabellum",
    weapon_type="Pistol",
    country="Belgium",
    length_deployed=8,
    reload_time=4,
    rate_of_fire=None,  # * means self-loading
    self_loading_action=True,
    full_auto=False,
    ammo_capacity=13,
    ammo_weight=0.50,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=3,
    sustained_auto_burst=4,
    aim_time_modifiers={
        1: 17,
        2: 11,
        3: 10,
        4: -9,
        5: -8,
        6: -7,
    },
    ammunition_types=[ammo_9mm_fmj, ammo_9mm_jhp, ammo_9mm_ap],
    ballistic_data=pistol_9mm_ballistic
)

# Type 51
type_51 = Weapon(
    name="Type 51",
    weight=1.9,
    description="Automatic Pistol, 7.62 x 25mm, China, Chinese copy of the Soviet TT33. "
                "Standard pistol of the Chinese army.",
    caliber="7.62 x 25mm",
    weapon_type="Pistol",
    country="China",
    length_deployed=8,
    reload_time=4,
    rate_of_fire=None,  # * means self-loading
    self_loading_action=True,
    full_auto=False,
    ammo_capacity=8,
    ammo_weight=0.33,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=3,
    sustained_auto_burst=4,
    aim_time_modifiers={
        1: 16,
        2: 11,
        3: 10,
        4: -9,
        5: -8,
        6: -7,
    },
    ammunition_types=[ammo_762x25_fmj, ammo_762x25_jhp, ammo_762x25_ap],
    ballistic_data=pistol_762x25_ballistic
)

# MAB PA15
mab_pa15 = Weapon(
    name="MAB PA15",
    weight=2.8,
    description="Automatic Pistol, 9mm Parabellum, France, Modern, high capacity pistol. "
                "Standard pistol of the French army.",
    caliber="9mm Parabellum",
    weapon_type="Pistol",
    country="France",
    length_deployed=8,
    reload_time=4,
    rate_of_fire=None,  # * means self-loading
    self_loading_action=True,
    full_auto=False,
    ammo_capacity=15,
    ammo_weight=0.60,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=3,
    sustained_auto_burst=4,
    aim_time_modifiers={
        1: 18,
        2: 11,
        3: 10,
        4: -9,
        5: -8,
        6: -7,
    },
    ammunition_types=[ammo_9mm_fmj, ammo_9mm_jhp, ammo_9mm_ap],
    ballistic_data=pistol_9mm_ballistic
)

# Walther PPK
walther_ppk = Weapon(
    name="Walther PPK",
    weight=1.4,
    description="Automatic Pistol, .32 ACP, West Germany, Small, easily concealed pistol "
                "designed for police undercover use.",
    caliber=".32 ACP",
    weapon_type="Pistol",
    country="West Germany",
    length_deployed=6,
    reload_time=4,
    rate_of_fire=None,  # * means self-loading
    self_loading_action=True,
    full_auto=False,
    ammo_capacity=7,
    ammo_weight=0.31,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=2,
    sustained_auto_burst=2,
    aim_time_modifiers={
        1: 16,
        2: 11,
        3: 10,
        4: -9,
        5: -8,
        6: -7,
    },
    ammunition_types=[ammo_32acp_fmj, ammo_32acp_jhp, ammo_32acp_ap],
    ballistic_data=pistol_32acp_ballistic
)


WEAPONS_LIST = [
    sig_550,
    fn_mk1,
    type_51,
    mab_pa15,
    walther_ppk,
]
