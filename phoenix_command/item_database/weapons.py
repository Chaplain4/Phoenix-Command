"""Database of weapons with their ballistic characteristics."""

from phoenix_command.models.gear import Weapon, AmmoType, BallisticData, WeaponBallisticData, RangeData, ExplosiveData
from phoenix_command.models.enums import AmmoFeedDevice, Caliber, WeaponType, Country

# ============================================================================
# 5.56mm NATO ammunition types
# ============================================================================
ammo_556_fmj = AmmoType(
    name="5.56mm NATO Full Metal Jacket",
    description="FMJ",
    weight=1.1,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=15, damage_class=6),
        BallisticData(range_hexes=20, penetration=15, damage_class=6),
        BallisticData(range_hexes=40, penetration=13, damage_class=6),
        BallisticData(range_hexes=70, penetration=12, damage_class=6),
        BallisticData(range_hexes=100, penetration=10, damage_class=5),
        BallisticData(range_hexes=200, penetration=6.4, damage_class=4),
        BallisticData(range_hexes=300, penetration=4.1, damage_class=3),
        BallisticData(range_hexes=400, penetration=2.6, damage_class=2, beyond_max_range=True),
    ]
)

ammo_556_jhp = AmmoType(
    name="5.56mm NATO Jacketed Hollow Point",
    description="JHP",
    weight=1.1,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=15, damage_class=8),
        BallisticData(range_hexes=20, penetration=14, damage_class=8),
        BallisticData(range_hexes=40, penetration=13, damage_class=7),
        BallisticData(range_hexes=70, penetration=11, damage_class=7),
        BallisticData(range_hexes=100, penetration=9.7, damage_class=7),
        BallisticData(range_hexes=200, penetration=6.2, damage_class=6),
        BallisticData(range_hexes=300, penetration=3.9, damage_class=4),
        BallisticData(range_hexes=400, penetration=2.5, damage_class=3, beyond_max_range=True),
    ]
)

ammo_556_ap = AmmoType(
    name="5.56mm NATO Armor Piercing",
    description="AP",
    weight=1.1,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=21, damage_class=6),
        BallisticData(range_hexes=20, penetration=21, damage_class=6),
        BallisticData(range_hexes=40, penetration=19, damage_class=6),
        BallisticData(range_hexes=70, penetration=16, damage_class=5),
        BallisticData(range_hexes=100, penetration=14, damage_class=5),
        BallisticData(range_hexes=200, penetration=9.1, damage_class=4),
        BallisticData(range_hexes=300, penetration=5.7, damage_class=3),
        BallisticData(range_hexes=400, penetration=3.6, damage_class=2, beyond_max_range=True),
    ]
)

# ============================================================================
# 9mm Parabellum ammunition types
# ============================================================================
ammo_9mm_fmj = AmmoType(
    name="9mm Parabellum Full Metal Jacket",
    description="FMJ",
    weight=0.5,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=2.1, damage_class=3),
        BallisticData(range_hexes=20, penetration=1.9, damage_class=3),
        BallisticData(range_hexes=40, penetration=1.6, damage_class=2),
        BallisticData(range_hexes=70, penetration=1.3, damage_class=2),
        BallisticData(range_hexes=100, penetration=1.0, damage_class=1),
        BallisticData(range_hexes=200, penetration=0.4, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.2, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_9mm_jhp = AmmoType(
    name="9mm Parabellum Jacketed Hollow Point",
    description="JHP",
    weight=0.5,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=2.0, damage_class=4),
        BallisticData(range_hexes=20, penetration=1.8, damage_class=4),
        BallisticData(range_hexes=40, penetration=1.6, damage_class=3),
        BallisticData(range_hexes=70, penetration=1.2, damage_class=2),
        BallisticData(range_hexes=100, penetration=1.0, damage_class=2),
        BallisticData(range_hexes=200, penetration=0.4, damage_class=2, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.2, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_9mm_ap = AmmoType(
    name="9mm Parabellum Armor Piercing",
    description="AP",
    weight=0.5,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=2.9, damage_class=3),
        BallisticData(range_hexes=20, penetration=2.7, damage_class=3),
        BallisticData(range_hexes=40, penetration=2.3, damage_class=2),
        BallisticData(range_hexes=70, penetration=1.8, damage_class=2),
        BallisticData(range_hexes=100, penetration=1.4, damage_class=1),
        BallisticData(range_hexes=200, penetration=0.6, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.3, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_9mm_v2_fmj = AmmoType(
    name="9mm Parabellum FMJ (v2)",
    description="FMJ",
    weight=0.41,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=1.9, damage_class=3),
        BallisticData(range_hexes=20, penetration=1.8, damage_class=3),
        BallisticData(range_hexes=40, penetration=1.5, damage_class=2),
        BallisticData(range_hexes=70, penetration=1.1, damage_class=2),
        BallisticData(range_hexes=100, penetration=0.9, damage_class=1),
        BallisticData(range_hexes=200, penetration=0.4, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.1, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_9mm_v2_jhp = AmmoType(
    name="9mm Parabellum JHP (v2)",
    description="JHP",
    weight=0.41,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=1.9, damage_class=4),
        BallisticData(range_hexes=20, penetration=1.7, damage_class=4),
        BallisticData(range_hexes=40, penetration=1.4, damage_class=3),
        BallisticData(range_hexes=70, penetration=1.1, damage_class=2),
        BallisticData(range_hexes=100, penetration=0.8, damage_class=1),
        BallisticData(range_hexes=200, penetration=0.3, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.1, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_9mm_v2_ap = AmmoType(
    name="9mm Parabellum AP (v2)",
    description="AP",
    weight=0.41,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=2.7, damage_class=3),
        BallisticData(range_hexes=20, penetration=2.5, damage_class=2),
        BallisticData(range_hexes=40, penetration=2.1, damage_class=2),
        BallisticData(range_hexes=70, penetration=1.6, damage_class=2),
        BallisticData(range_hexes=100, penetration=1.2, damage_class=1),
        BallisticData(range_hexes=200, penetration=0.5, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.2, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_9mm_vp70_fmj = AmmoType(
    name="9mm Parabellum FMJ (VP70M)",
    description="FMJ",
    weight=0.69,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=2.0, damage_class=3),
        BallisticData(range_hexes=20, penetration=1.9, damage_class=3),
        BallisticData(range_hexes=40, penetration=1.6, damage_class=2),
        BallisticData(range_hexes=70, penetration=1.2, damage_class=2),
        BallisticData(range_hexes=100, penetration=0.9, damage_class=1),
        BallisticData(range_hexes=200, penetration=0.4, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.2, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)
ammo_9mm_vp70_jhp = AmmoType(
    name="9mm Parabellum JHP (VP70M)",
    description="JHP",
    weight=0.69,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=2.0, damage_class=4),
        BallisticData(range_hexes=20, penetration=1.8, damage_class=4),
        BallisticData(range_hexes=40, penetration=1.5, damage_class=3),
        BallisticData(range_hexes=70, penetration=1.2, damage_class=2),
        BallisticData(range_hexes=100, penetration=0.9, damage_class=2),
        BallisticData(range_hexes=200, penetration=0.4, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.2, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)
ammo_9mm_vp70_ap = AmmoType(
    name="9mm Parabellum AP (VP70M)",
    description="AP",
    weight=0.69,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=2.9, damage_class=3),
        BallisticData(range_hexes=20, penetration=2.6, damage_class=3),
        BallisticData(range_hexes=40, penetration=2.2, damage_class=2),
        BallisticData(range_hexes=70, penetration=1.7, damage_class=2),
        BallisticData(range_hexes=100, penetration=1.3, damage_class=1),
        BallisticData(range_hexes=200, penetration=0.5, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.2, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_9mm_m93r_fmj = AmmoType(
    name="9mm Parabellum FMJ (M93R)",
    description="FMJ",
    weight=0.69,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=2.2, damage_class=3),
        BallisticData(range_hexes=20, penetration=2.0, damage_class=3),
        BallisticData(range_hexes=40, penetration=1.7, damage_class=2),
        BallisticData(range_hexes=70, penetration=1.3, damage_class=2),
        BallisticData(range_hexes=100, penetration=1.0, damage_class=1),
        BallisticData(range_hexes=200, penetration=0.4, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.2, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_9mm_m93r_jhp = AmmoType(
    name="9mm Parabellum JHP (M93R)",
    description="JHP",
    weight=0.69,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=2.1, damage_class=5),
        BallisticData(range_hexes=20, penetration=2.0, damage_class=4),
        BallisticData(range_hexes=40, penetration=1.6, damage_class=4),
        BallisticData(range_hexes=70, penetration=1.3, damage_class=3),
        BallisticData(range_hexes=100, penetration=1.0, damage_class=2),
        BallisticData(range_hexes=200, penetration=0.4, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.2, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_9mm_m93r_ap = AmmoType(
    name="9mm Parabellum JHP (M93R)",
    description="JHP",
    weight=0.69,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=3.1, damage_class=3),
        BallisticData(range_hexes=20, penetration=2.9, damage_class=3),
        BallisticData(range_hexes=40, penetration=2.4, damage_class=2),
        BallisticData(range_hexes=70, penetration=1.9, damage_class=2),
        BallisticData(range_hexes=100, penetration=1.4, damage_class=1),
        BallisticData(range_hexes=200, penetration=0.6, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.3, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_9mm_m92f_fmj = AmmoType(
    name="9mm Parabellum FMJ (M92F)",
    weight=0.6,
    description="FMJ",
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=2.4, damage_class=3),
        BallisticData(range_hexes=20, penetration=2.2, damage_class=3),
        BallisticData(range_hexes=40,  penetration=1.9, damage_class=3),
        BallisticData(range_hexes=70, penetration=1.5, damage_class=2),
        BallisticData(range_hexes=100, penetration=1.1, damage_class=2),
        BallisticData(range_hexes=200, penetration=0.5, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.2, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_9mm_m92f_jhp = AmmoType(
    name="9mm Parabellum JHP (M92F)",
    description="JHP",
    weight=0.6,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=2.3, damage_class=5),
        BallisticData(range_hexes=20,  penetration=2.1, damage_class=5),
        BallisticData(range_hexes=40,  penetration=1.8, damage_class=4),
        BallisticData(range_hexes=70,  penetration=1.4, damage_class=3),
        BallisticData(range_hexes=100, penetration=1.1, damage_class=2),
        BallisticData(range_hexes=200, penetration=0.5, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.2, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_9mm_m92f_ap = AmmoType(
    name="9mm Parabellum AP (M92F)",
    description="AP",
    weight=0.6,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=3.4, damage_class=3),
        BallisticData(range_hexes=20,  penetration=3.1, damage_class=3),
        BallisticData(range_hexes=40,  penetration=2.6, damage_class=3),
        BallisticData(range_hexes=70,  penetration=2.0, damage_class=2),
        BallisticData(range_hexes=100, penetration=1.6, damage_class=2),
        BallisticData(range_hexes=200, penetration=0.7, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.3, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_545x18_fmj = AmmoType(
    name="5.45 x 18mm FMJ (PSM)",
    description="FMJ",
    weight=0.25,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=1.2, damage_class=1),
        BallisticData(range_hexes=20,  penetration=1.1, damage_class=1),
        BallisticData(range_hexes=40,  penetration=0.9, damage_class=1),
        BallisticData(range_hexes=70,  penetration=0.7, damage_class=1),
        BallisticData(range_hexes=100, penetration=0.5, damage_class=1),
    ]
)

ammo_545x18_jhp = AmmoType(
    name="5.45 x 18mm JHP (PSM)",
    description="JHP",
    weight=0.25,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=1.2, damage_class=2),
        BallisticData(range_hexes=20,  penetration=1.0, damage_class=1),
        BallisticData(range_hexes=40,  penetration=0.9, damage_class=1),
        BallisticData(range_hexes=70,  penetration=0.6, damage_class=1),
        BallisticData(range_hexes=100, penetration=0.5, damage_class=1),
    ]
)

ammo_545x18_ap = AmmoType(
    name="5.45 x 18mm AP (PSM)",
    description="AP",
    weight=0.25,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=1.7, damage_class=1),
        BallisticData(range_hexes=20,  penetration=1.5, damage_class=1),
        BallisticData(range_hexes=40,  penetration=1.3, damage_class=1),
        BallisticData(range_hexes=70,  penetration=0.9, damage_class=1),
        BallisticData(range_hexes=100, penetration=0.7, damage_class=1),
    ]
)

# ============================================================================
# 9 x 18mm Makarov ammunition types
# ============================================================================
ammo_9x18_fmj = AmmoType(
    name="9 x 18mm Makarov Full Metal Jacket",
    description="FMJ",
    weight=0.4,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=1.2, damage_class=2),
        BallisticData(range_hexes=20, penetration=1.1, damage_class=2),
        BallisticData(range_hexes=40, penetration=0.9, damage_class=1),
        BallisticData(range_hexes=70, penetration=0.6, damage_class=1),
        BallisticData(range_hexes=100, penetration=0.4, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=200, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_9x18_jhp = AmmoType(
    name="9 x 18mm Makarov Jacketed Hollow Point",
    description="JHP",
    weight=0.4,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=1.2, damage_class=3),
        BallisticData(range_hexes=20, penetration=1.0, damage_class=3),
        BallisticData(range_hexes=40, penetration=0.8, damage_class=2),
        BallisticData(range_hexes=70, penetration=0.6, damage_class=1),
        BallisticData(range_hexes=100, penetration=0.4, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=200, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_9x18_ap = AmmoType(
    name="9 x 18mm Makarov Armor Piercing",
    description="AP",
    weight=0.4,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=1.7, damage_class=2),
        BallisticData(range_hexes=20, penetration=1.5, damage_class=2),
        BallisticData(range_hexes=40, penetration=1.2, damage_class=1),
        BallisticData(range_hexes=70, penetration=0.8, damage_class=1),
        BallisticData(range_hexes=100, penetration=0.6, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=200, penetration=0.2, damage_class=1, beyond_max_range=True),
    ]
)

# ============================================================================
# 7.62 x 25mm ammunition types
# ============================================================================
ammo_762x25_fmj = AmmoType(
    name="7.62 x 25mm Full Metal Jacket",
    description="FMJ",
    weight=0.33,
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
    description="JHP",
    weight=0.33,
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
    description="AP",
    weight=0.33,
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
# .45 ACP ammunition types
# ============================================================================

ammo_45_m15_fmj = AmmoType(
    name="45 ACP FMJ (M15)",
    description="FMJ",
    weight=0.7,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=1.5, damage_class=3),
        BallisticData(range_hexes=20,  penetration=1.4, damage_class=3),
        BallisticData(range_hexes=40,  penetration=1.1, damage_class=2),
        BallisticData(range_hexes=70,  penetration=0.9, damage_class=1),
        BallisticData(range_hexes=100, penetration=0.8, damage_class=1),
        BallisticData(range_hexes=200, penetration=0.3, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.2, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_45_m15_jhp = AmmoType(
    name="45 ACP JHP (M15)",
    description="JHP",
    weight=0.7,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=1.4, damage_class=4),
        BallisticData(range_hexes=20,  penetration=1.3, damage_class=3),
        BallisticData(range_hexes=40,  penetration=1.1, damage_class=3),
        BallisticData(range_hexes=70,  penetration=0.8, damage_class=2),
        BallisticData(range_hexes=100, penetration=0.7, damage_class=1),
        BallisticData(range_hexes=200, penetration=0.3, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.1, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_45_m15_ap = AmmoType(
    name="45 ACP AP (M15)",
    description="AP",
    weight=0.7,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=2.1, damage_class=3),
        BallisticData(range_hexes=20,  penetration=2.0, damage_class=3),
        BallisticData(range_hexes=40,  penetration=1.7, damage_class=2),
        BallisticData(range_hexes=70,  penetration=1.3, damage_class=1),
        BallisticData(range_hexes=100, penetration=1.0, damage_class=1),
        BallisticData(range_hexes=200, penetration=0.5, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.2, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_45_m1911_fmj = AmmoType(
    name="45 ACP FMJ (M1911A1)",
    description="FMJ",
    weight=0.7,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=1.6, damage_class=3),
        BallisticData(range_hexes=20,  penetration=1.5, damage_class=3),
        BallisticData(range_hexes=40,  penetration=1.2, damage_class=2),
        BallisticData(range_hexes=70,  penetration=1.0, damage_class=1),
        BallisticData(range_hexes=100, penetration=0.8, damage_class=1),
        BallisticData(range_hexes=200, penetration=0.3, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.2, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_45_m1911_jhp = AmmoType(
    name="45 ACP JHP (M1911A1)",
    description="JHP",
    weight=0.7,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=1.5, damage_class=4),
        BallisticData(range_hexes=20,  penetration=1.4, damage_class=4),
        BallisticData(range_hexes=40,  penetration=1.2, damage_class=3),
        BallisticData(range_hexes=70,  penetration=0.9, damage_class=2),
        BallisticData(range_hexes=100, penetration=0.7, damage_class=1),
        BallisticData(range_hexes=200, penetration=0.3, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.1, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_45_m1911_ap = AmmoType(
    name="45 ACP AP (M1911A1)",
    description="AP",
    weight=0.7,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=2.2, damage_class=3),
        BallisticData(range_hexes=20,  penetration=2.1, damage_class=3),
        BallisticData(range_hexes=40,  penetration=1.8, damage_class=2),
        BallisticData(range_hexes=70,  penetration=1.4, damage_class=1),
        BallisticData(range_hexes=100, penetration=1.1, damage_class=1),
        BallisticData(range_hexes=200, penetration=0.5, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.2, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

# ============================================================================
# .32 ACP ammunition types
# ============================================================================
ammo_32acp_fmj = AmmoType(
    name=".32 ACP Full Metal Jacket",
    description="FMJ",
    weight=0.31,
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
    description="JHP",
    weight=0.31,
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
    description="AP",
    weight=0.31,
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

ammo_9mm_pa3_fmj = AmmoType(
    name="9mm Parabellum FMJ (PA3-DM)",
    description="FMJ",
    weight=1.1,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=2.5, damage_class=3),
        BallisticData(range_hexes=20,  penetration=2.3, damage_class=3),
        BallisticData(range_hexes=40,  penetration=2.0, damage_class=3),
        BallisticData(range_hexes=70,  penetration=1.5, damage_class=2),
        BallisticData(range_hexes=100, penetration=1.2, damage_class=2),
        BallisticData(range_hexes=200, penetration=0.5, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.2, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_9mm_pa3_jhp = AmmoType(
    name="9mm Parabellum JHP (PA3-DM)",
    description="JHP",
    weight=1.1,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=2.4, damage_class=5),
        BallisticData(range_hexes=20,  penetration=2.2, damage_class=5),
        BallisticData(range_hexes=40,  penetration=1.9, damage_class=4),
        BallisticData(range_hexes=70,  penetration=1.5, damage_class=3),
        BallisticData(range_hexes=100, penetration=1.1, damage_class=2),
        BallisticData(range_hexes=200, penetration=0.5, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.2, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_9mm_pa3_ap = AmmoType(
    name="9mm Parabellum AP (PA3-DM)",
    description="AP",
    weight=1.1,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=3.6, damage_class=3),
        BallisticData(range_hexes=20,  penetration=3.3, damage_class=3),
        BallisticData(range_hexes=40,  penetration=2.8, damage_class=3),
        BallisticData(range_hexes=70,  penetration=2.2, damage_class=2),
        BallisticData(range_hexes=100, penetration=1.7, damage_class=2),
        BallisticData(range_hexes=200, penetration=0.7, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.3, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_9mm_f1_fmj = AmmoType(
    name="9mm Parabellum FMJ (F1)",
    description="FMJ",
    weight=1.4,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=2.1, damage_class=3),
        BallisticData(range_hexes=20,  penetration=1.9, damage_class=3),
        BallisticData(range_hexes=40,  penetration=1.6, damage_class=2),
        BallisticData(range_hexes=70,  penetration=1.3, damage_class=2),
        BallisticData(range_hexes=100, penetration=1.0, damage_class=1),
        BallisticData(range_hexes=200, penetration=0.4, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.2, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_9mm_f1_jhp = AmmoType(
    name="9mm Parabellum JHP (F1)",
    description="JHP",
    weight=1.4,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=2.0, damage_class=4),
        BallisticData(range_hexes=20,  penetration=1.9, damage_class=4),
        BallisticData(range_hexes=40,  penetration=1.6, damage_class=3),
        BallisticData(range_hexes=70,  penetration=1.2, damage_class=2),
        BallisticData(range_hexes=100, penetration=0.9, damage_class=2),
        BallisticData(range_hexes=200, penetration=0.4, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.2, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_9mm_f1_ap = AmmoType(
    name="9mm Parabellum AP (F1)",
    description="AP",
    weight=1.4,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=3.0, damage_class=3),
        BallisticData(range_hexes=20,  penetration=2.7, damage_class=3),
        BallisticData(range_hexes=40,  penetration=2.3, damage_class=2),
        BallisticData(range_hexes=70,  penetration=1.8, damage_class=2),
        BallisticData(range_hexes=100, penetration=1.4, damage_class=1),
        BallisticData(range_hexes=200, penetration=0.6, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.2, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_9mm_mpi81_fmj = AmmoType(
    name="9mm Parabellum FMJ (MPi 81)",
    description="FMJ",
    weight=1.4,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=2.3, damage_class=3),
        BallisticData(range_hexes=20,  penetration=2.1, damage_class=3),
        BallisticData(range_hexes=40,  penetration=1.8, damage_class=3),
        BallisticData(range_hexes=70,  penetration=1.4, damage_class=2),
        BallisticData(range_hexes=100, penetration=1.1, damage_class=1),
        BallisticData(range_hexes=200, penetration=0.5, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.2, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_9mm_mpi81_jhp = AmmoType(
    name="9mm Parabellum JHP (MPi 81)",
    description="JHP",
    weight=1.4,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=2.2, damage_class=5),
        BallisticData(range_hexes=20,  penetration=2.0, damage_class=4),
        BallisticData(range_hexes=40,  penetration=1.7, damage_class=4),
        BallisticData(range_hexes=70,  penetration=1.3, damage_class=3),
        BallisticData(range_hexes=100, penetration=1.0, damage_class=2),
        BallisticData(range_hexes=200, penetration=0.4, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.2, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_9mm_mpi81_ap = AmmoType(
    name="9mm Parabellum AP (MPi 81)",
    description="AP",
    weight=1.4,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=3.2, damage_class=3),
        BallisticData(range_hexes=20,  penetration=3.0, damage_class=3),
        BallisticData(range_hexes=40,  penetration=2.5, damage_class=3),
        BallisticData(range_hexes=70,  penetration=1.9, damage_class=2),
        BallisticData(range_hexes=100, penetration=1.5, damage_class=1),
        BallisticData(range_hexes=200, penetration=0.6, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.3, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_32acp_m61_fmj = AmmoType(
    name=".32 ACP FMJ (M61)",
    description="FMJ",
    weight=0.9,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=1.2, damage_class=2),
        BallisticData(range_hexes=20,  penetration=1.1, damage_class=1),
        BallisticData(range_hexes=40,  penetration=0.8, damage_class=1),
        BallisticData(range_hexes=70,  penetration=0.6, damage_class=1),
        BallisticData(range_hexes=100, penetration=0.4, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=200, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_32acp_m61_jhp = AmmoType(
    name=".32 ACP JHP (M61)",
    description="JHP",
    weight=0.9,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=1.1, damage_class=3),
        BallisticData(range_hexes=20,  penetration=1.0, damage_class=2),
        BallisticData(range_hexes=40,  penetration=0.8, damage_class=2),
        BallisticData(range_hexes=70,  penetration=0.6, damage_class=1),
        BallisticData(range_hexes=100, penetration=0.4, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=200, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_32acp_m61_ap = AmmoType(
    name=".32 ACP AP (M61)",
    description="AP",
    weight=0.9,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=1.7, damage_class=2),
        BallisticData(range_hexes=20,  penetration=1.5, damage_class=1),
        BallisticData(range_hexes=40,  penetration=1.2, damage_class=1),
        BallisticData(range_hexes=70,  penetration=0.8, damage_class=1),
        BallisticData(range_hexes=100, penetration=0.6, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=200, penetration=0.2, damage_class=1, beyond_max_range=True),
    ]
)

ammo_9mm_mat49_fmj = AmmoType(
    name="9mm Parabellum FMJ (MAT 49)",
    description="FMJ",
    weight=1.5,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=2.4, damage_class=3),
        BallisticData(range_hexes=20,  penetration=2.2, damage_class=3),
        BallisticData(range_hexes=40,  penetration=1.9, damage_class=3),
        BallisticData(range_hexes=70,  penetration=1.5, damage_class=2),
        BallisticData(range_hexes=100, penetration=1.1, damage_class=2),
        BallisticData(range_hexes=200, penetration=0.5, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.2, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_9mm_mat49_jhp = AmmoType(
    name="9mm Parabellum JHP (MAT 49)",
    description="JHP",
    weight=1.5,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=2.3, damage_class=5),
        BallisticData(range_hexes=20,  penetration=2.1, damage_class=5),
        BallisticData(range_hexes=40,  penetration=1.8, damage_class=4),
        BallisticData(range_hexes=70,  penetration=1.4, damage_class=3),
        BallisticData(range_hexes=100, penetration=1.1, damage_class=2),
        BallisticData(range_hexes=200, penetration=0.5, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.2, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_9mm_mat49_ap = AmmoType(
    name="9mm Parabellum AP (MAT 49)",
    description="AP",
    weight=1.5,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=3.4, damage_class=3),
        BallisticData(range_hexes=20,  penetration=3.1, damage_class=3),
        BallisticData(range_hexes=40,  penetration=2.6, damage_class=3),
        BallisticData(range_hexes=70,  penetration=2.0, damage_class=2),
        BallisticData(range_hexes=100, penetration=1.6, damage_class=2),
        BallisticData(range_hexes=200, penetration=0.7, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.3, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_9mm_mp5_fmj = AmmoType(
    name="9mm Parabellum FMJ (MP5)",
    description="FMJ",
    weight=1.2,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=2.5, damage_class=3),
        BallisticData(range_hexes=20,  penetration=2.3, damage_class=3),
        BallisticData(range_hexes=40,  penetration=2.0, damage_class=3),
        BallisticData(range_hexes=70,  penetration=1.5, damage_class=2),
        BallisticData(range_hexes=100, penetration=1.2, damage_class=2),
        BallisticData(range_hexes=200, penetration=0.5, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.2, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_9mm_mp5_jhp = AmmoType(
    name="9mm Parabellum JHP (MP5)",
    description="JHP",
    weight=1.2,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=2.4, damage_class=5),
        BallisticData(range_hexes=20,  penetration=2.2, damage_class=5),
        BallisticData(range_hexes=40,  penetration=1.9, damage_class=4),
        BallisticData(range_hexes=70,  penetration=1.5, damage_class=3),
        BallisticData(range_hexes=100, penetration=1.1, damage_class=2),
        BallisticData(range_hexes=200, penetration=0.5, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.2, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_9mm_mp5_ap = AmmoType(
    name="9mm Parabellum AP (MP5)",
    description="AP",
    weight=1.2,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=3.6, damage_class=3),
        BallisticData(range_hexes=20,  penetration=3.3, damage_class=3),
        BallisticData(range_hexes=40,  penetration=2.8, damage_class=3),
        BallisticData(range_hexes=70,  penetration=2.2, damage_class=2),
        BallisticData(range_hexes=100, penetration=1.7, damage_class=2),
        BallisticData(range_hexes=200, penetration=0.7, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.3, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_9mm_mp5k_fmj = AmmoType(
    name="9mm Parabellum FMJ (MP5K)",
    description="FMJ",
    weight=1.2,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=2.2, damage_class=3),
        BallisticData(range_hexes=20,  penetration=2.0, damage_class=3),
        BallisticData(range_hexes=40,  penetration=1.7, damage_class=2),
        BallisticData(range_hexes=70,  penetration=1.3, damage_class=2),
        BallisticData(range_hexes=100, penetration=1.0, damage_class=1),
        BallisticData(range_hexes=200, penetration=0.4, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.2, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_9mm_mp5k_jhp = AmmoType(
    name="9mm Parabellum JHP (MP5K)",
    description="JHP",
    weight=1.2,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=2.1, damage_class=5),
        BallisticData(range_hexes=20,  penetration=2.0, damage_class=4),
        BallisticData(range_hexes=40,  penetration=1.6, damage_class=4),
        BallisticData(range_hexes=70,  penetration=1.3, damage_class=3),
        BallisticData(range_hexes=100, penetration=1.0, damage_class=2),
        BallisticData(range_hexes=200, penetration=0.4, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.2, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_9mm_mp5k_ap = AmmoType(
    name="9mm Parabellum AP (MP5K)",
    description="AP",
    weight=1.2,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=3.1, damage_class=3),
        BallisticData(range_hexes=20,  penetration=2.9, damage_class=3),
        BallisticData(range_hexes=40,  penetration=2.4, damage_class=2),
        BallisticData(range_hexes=70,  penetration=1.9, damage_class=2),
        BallisticData(range_hexes=100, penetration=1.4, damage_class=1),
        BallisticData(range_hexes=200, penetration=0.6, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.3, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_556_hk53_fmj = AmmoType(
    name="5.56mm NATO FMJ (HK 53)",
    description="FMJ",
    weight=1.4,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=10, damage_class=5),
        BallisticData(range_hexes=20,  penetration=9.9, damage_class=5),
        BallisticData(range_hexes=40,  penetration=9.0, damage_class=5),
        BallisticData(range_hexes=70,  penetration=7.9, damage_class=4),
        BallisticData(range_hexes=100, penetration=6.9, damage_class=4),
        BallisticData(range_hexes=200, penetration=4.4, damage_class=3),
        BallisticData(range_hexes=300, penetration=2.8, damage_class=2),
        BallisticData(range_hexes=400, penetration=1.8, damage_class=1, beyond_max_range=True),
    ]
)

ammo_556_hk53_jhp = AmmoType(
    name="5.56mm NATO JHP (HK 53)",
    description="JHP",
    weight=1.4,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=10, damage_class=7),
        BallisticData(range_hexes=20,  penetration=9.5, damage_class=7),
        BallisticData(range_hexes=40,  penetration=8.7, damage_class=6),
        BallisticData(range_hexes=70,  penetration=7.5, damage_class=6),
        BallisticData(range_hexes=100, penetration=6.6, damage_class=6),
        BallisticData(range_hexes=200, penetration=4.2, damage_class=5),
        BallisticData(range_hexes=300, penetration=2.7, damage_class=3),
        BallisticData(range_hexes=400, penetration=1.7, damage_class=2, beyond_max_range=True),
    ]
)

ammo_556_hk53_ap = AmmoType(
    name="5.56mm NATO AP (HK 53)",
    description="AP",
    weight=1.4,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=15, damage_class=5),
        BallisticData(range_hexes=20,  penetration=14, damage_class=5),
        BallisticData(range_hexes=40,  penetration=13, damage_class=4),
        BallisticData(range_hexes=70,  penetration=11, damage_class=4),
        BallisticData(range_hexes=100, penetration=9.7, damage_class=4),
        BallisticData(range_hexes=200, penetration=6.1, damage_class=3),
        BallisticData(range_hexes=300, penetration=3.9, damage_class=2),
        BallisticData(range_hexes=400, penetration=2.5, damage_class=1, beyond_max_range=True),
    ]
)

ammo_9mm_uzi_fmj = AmmoType(
    name="9mm Parabellum FMJ (Uzi)",
    description="FMJ",
    weight=1.3,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=2.5, damage_class=3),
        BallisticData(range_hexes=20,  penetration=2.3, damage_class=3),
        BallisticData(range_hexes=40,  penetration=2.0, damage_class=3),
        BallisticData(range_hexes=70,  penetration=1.5, damage_class=2),
        BallisticData(range_hexes=100, penetration=1.2, damage_class=2),
        BallisticData(range_hexes=200, penetration=0.5, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.2, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_9mm_uzi_jhp = AmmoType(
    name="9mm Parabellum JHP (Uzi)",
    description="JHP",
    weight=1.3,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=2.4, damage_class=5),
        BallisticData(range_hexes=20,  penetration=2.2, damage_class=5),
        BallisticData(range_hexes=40,  penetration=1.9, damage_class=4),
        BallisticData(range_hexes=70,  penetration=1.5, damage_class=3),
        BallisticData(range_hexes=100, penetration=1.1, damage_class=2),
        BallisticData(range_hexes=200, penetration=0.5, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.2, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_9mm_uzi_ap = AmmoType(
    name="9mm Parabellum AP (Uzi)",
    description="AP",
    weight=1.3,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=3.6, damage_class=3),
        BallisticData(range_hexes=20,  penetration=3.3, damage_class=3),
        BallisticData(range_hexes=40,  penetration=2.8, damage_class=3),
        BallisticData(range_hexes=70,  penetration=2.2, damage_class=2),
        BallisticData(range_hexes=100, penetration=1.7, damage_class=2),
        BallisticData(range_hexes=200, penetration=0.7, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.3, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_9mm_miniuzi_fmj = AmmoType(
    name="9mm Parabellum FMJ (Mini Uzi)",
    description="FMJ",
    weight=1.3,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=1.9, damage_class=3),
        BallisticData(range_hexes=20,  penetration=1.8, damage_class=3),
        BallisticData(range_hexes=40,  penetration=1.5, damage_class=2),
        BallisticData(range_hexes=70,  penetration=1.1, damage_class=2),
        BallisticData(range_hexes=100, penetration=0.9, damage_class=1),
        BallisticData(range_hexes=200, penetration=0.4, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.1, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_9mm_miniuzi_jhp = AmmoType(
    name="9mm Parabellum JHP (Mini Uzi)",
    description="JHP",
    weight=1.3,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=1.9, damage_class=4),
        BallisticData(range_hexes=20,  penetration=1.7, damage_class=4),
        BallisticData(range_hexes=40,  penetration=1.4, damage_class=3),
        BallisticData(range_hexes=70,  penetration=1.1, damage_class=2),
        BallisticData(range_hexes=100, penetration=0.8, damage_class=1),
        BallisticData(range_hexes=200, penetration=0.3, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.1, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_9mm_miniuzi_ap = AmmoType(
    name="9mm Parabellum AP (Mini Uzi)",
    description="AP",
    weight=1.3,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=2.7, damage_class=3),
        BallisticData(range_hexes=20,  penetration=2.5, damage_class=2),
        BallisticData(range_hexes=40,  penetration=2.1, damage_class=2),
        BallisticData(range_hexes=70,  penetration=1.6, damage_class=2),
        BallisticData(range_hexes=100, penetration=1.2, damage_class=1),
        BallisticData(range_hexes=200, penetration=0.5, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.2, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_9mm_m12s_fmj = AmmoType(
    name="9mm Parabellum FMJ (M12S)",
    description="FMJ",
    weight=1.3,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=2.3, damage_class=3),
        BallisticData(range_hexes=20,  penetration=2.1, damage_class=3),
        BallisticData(range_hexes=40,  penetration=1.8, damage_class=3),
        BallisticData(range_hexes=70,  penetration=1.4, damage_class=2),
        BallisticData(range_hexes=100, penetration=1.1, damage_class=1),
        BallisticData(range_hexes=200, penetration=0.5, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.2, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_9mm_m12s_jhp = AmmoType(
    name="9mm Parabellum JHP (M12S)",
    description="JHP",
    weight=1.3,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=2.2, damage_class=5),
        BallisticData(range_hexes=20,  penetration=2.0, damage_class=4),
        BallisticData(range_hexes=40,  penetration=1.7, damage_class=4),
        BallisticData(range_hexes=70,  penetration=1.3, damage_class=3),
        BallisticData(range_hexes=100, penetration=1.0, damage_class=2),
        BallisticData(range_hexes=200, penetration=0.4, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.2, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_9mm_m12s_ap = AmmoType(
    name="9mm Parabellum AP (M12S)",
    description="AP",
    weight=1.3,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=3.2, damage_class=3),
        BallisticData(range_hexes=20,  penetration=3.0, damage_class=3),
        BallisticData(range_hexes=40,  penetration=2.5, damage_class=2),
        BallisticData(range_hexes=70,  penetration=1.9, damage_class=2),
        BallisticData(range_hexes=100, penetration=1.5, damage_class=1),
        BallisticData(range_hexes=200, penetration=0.6, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.3, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_9mm_spectre_fmj = AmmoType(
    name="9mm Parabellum FMJ (Spectre)",
    description="FMJ",
    weight=1.6,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=2.5, damage_class=3),
        BallisticData(range_hexes=20,  penetration=2.3, damage_class=3),
        BallisticData(range_hexes=40,  penetration=2.0, damage_class=3),
        BallisticData(range_hexes=70,  penetration=1.5, damage_class=2),
        BallisticData(range_hexes=100, penetration=1.2, damage_class=2),
        BallisticData(range_hexes=200, penetration=0.5, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.2, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_9mm_spectre_jhp = AmmoType(
    name="9mm Parabellum JHP (Spectre)",
    description="JHP",
    weight=1.6,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=2.4, damage_class=5),
        BallisticData(range_hexes=20,  penetration=2.2, damage_class=5),
        BallisticData(range_hexes=40,  penetration=1.9, damage_class=4),
        BallisticData(range_hexes=70,  penetration=1.5, damage_class=3),
        BallisticData(range_hexes=100, penetration=1.1, damage_class=2),
        BallisticData(range_hexes=200, penetration=0.5, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.2, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_9mm_spectre_ap = AmmoType(
    name="9mm Parabellum AP (Spectre)",
    description="AP",
    weight=1.6,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=3.6, damage_class=3),
        BallisticData(range_hexes=20,  penetration=3.3, damage_class=3),
        BallisticData(range_hexes=40,  penetration=2.8, damage_class=3),
        BallisticData(range_hexes=70,  penetration=2.2, damage_class=2),
        BallisticData(range_hexes=100, penetration=1.7, damage_class=2),
        BallisticData(range_hexes=200, penetration=0.7, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.3, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_9mm_bxp_fmj = AmmoType(
    name="9mm Parabellum FMJ (Armscor BXP)",
    description="FMJ",
    weight=1.2,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=1.7, damage_class=2),
        BallisticData(range_hexes=20,  penetration=1.5, damage_class=2),
        BallisticData(range_hexes=40,  penetration=1.3, damage_class=2),
        BallisticData(range_hexes=70,  penetration=1.0, damage_class=1),
        BallisticData(range_hexes=100, penetration=0.7, damage_class=1),
        BallisticData(range_hexes=200, penetration=0.3, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_9mm_bxp_jhp = AmmoType(
    name="9mm Parabellum JHP (Armscor BXP)",
    description="JHP",
    weight=1.2,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=1.6, damage_class=4),
        BallisticData(range_hexes=20,  penetration=1.5, damage_class=3),
        BallisticData(range_hexes=40,  penetration=1.2, damage_class=2),
        BallisticData(range_hexes=70,  penetration=0.9, damage_class=2),
        BallisticData(range_hexes=100, penetration=0.7, damage_class=1),
        BallisticData(range_hexes=200, penetration=0.3, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_9mm_bxp_ap = AmmoType(
    name="9mm Parabellum AP (Armscor BXP)",
    description="AP",
    weight=1.2,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=2.3, damage_class=2),
        BallisticData(range_hexes=20,  penetration=2.1, damage_class=2),
        BallisticData(range_hexes=40,  penetration=1.8, damage_class=2),
        BallisticData(range_hexes=70,  penetration=1.3, damage_class=1),
        BallisticData(range_hexes=100, penetration=1.0, damage_class=1),
        BallisticData(range_hexes=200, penetration=0.4, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.2, damage_class=1, beyond_max_range=True),
    ]
)

ammo_545_aks74u_fmj = AmmoType(
    name="5.45 x 39.5mm FMJ (AKS-74U)",
    description="FMJ",
    weight=1.3,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=11, damage_class=5),
        BallisticData(range_hexes=20,  penetration=10, damage_class=5),
        BallisticData(range_hexes=40,  penetration=9.4, damage_class=5),
        BallisticData(range_hexes=70,  penetration=8.1, damage_class=4),
        BallisticData(range_hexes=100, penetration=7.1, damage_class=4),
        BallisticData(range_hexes=200, penetration=4.4, damage_class=3),
        BallisticData(range_hexes=300, penetration=2.7, damage_class=2),
        BallisticData(range_hexes=400, penetration=1.7, damage_class=1, beyond_max_range=True),
    ]
)

ammo_545_aks74u_jhp = AmmoType(
    name="5.45 x 39.5mm JHP (AKS-74U)",
    description="JHP",
    weight=1.3,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=10, damage_class=7),
        BallisticData(range_hexes=20,  penetration=9.9, damage_class=7),
        BallisticData(range_hexes=40,  penetration=9.0, damage_class=6),
        BallisticData(range_hexes=70,  penetration=7.8, damage_class=6),
        BallisticData(range_hexes=100, penetration=6.8, damage_class=6),
        BallisticData(range_hexes=200, penetration=4.2, damage_class=4),
        BallisticData(range_hexes=300, penetration=2.6, damage_class=3),
        BallisticData(range_hexes=400, penetration=1.6, damage_class=2, beyond_max_range=True),
    ]
)

ammo_545_aks74u_ap = AmmoType(
    name="5.45 x 39.5mm AP (AKS-74U)",
    description="AP",
    weight=1.3,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=15, damage_class=5),
        BallisticData(range_hexes=20,  penetration=15, damage_class=5),
        BallisticData(range_hexes=40,  penetration=13, damage_class=4),
        BallisticData(range_hexes=70,  penetration=11, damage_class=4),
        BallisticData(range_hexes=100, penetration=10, damage_class=4),
        BallisticData(range_hexes=200, penetration=6.2, damage_class=3),
        BallisticData(range_hexes=300, penetration=3.8, damage_class=2),
        BallisticData(range_hexes=400, penetration=2.4, damage_class=1, beyond_max_range=True),
    ]
)

ammo_9mm_sterling_fmj = AmmoType(
    name="9mm Parabellum FMJ (Sterling Mk 7)",
    description="FMJ",
    weight=1.2,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=2.3, damage_class=3),
        BallisticData(range_hexes=20,  penetration=2.1, damage_class=3),
        BallisticData(range_hexes=40,  penetration=1.8, damage_class=3),
        BallisticData(range_hexes=70,  penetration=1.4, damage_class=2),
        BallisticData(range_hexes=100, penetration=1.1, damage_class=1),
        BallisticData(range_hexes=200, penetration=0.5, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.2, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_9mm_sterling_jhp = AmmoType(
    name="9mm Parabellum JHP (Sterling Mk 7)",
    description="JHP",
    weight=1.2,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=2.2, damage_class=5),
        BallisticData(range_hexes=20,  penetration=2.0, damage_class=4),
        BallisticData(range_hexes=40,  penetration=1.7, damage_class=4),
        BallisticData(range_hexes=70,  penetration=1.3, damage_class=3),
        BallisticData(range_hexes=100, penetration=1.0, damage_class=2),
        BallisticData(range_hexes=200, penetration=0.4, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.2, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_9mm_sterling_ap = AmmoType(
    name="9mm Parabellum AP (Sterling Mk 7)",
    description="AP",
    weight=1.2,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=3.2, damage_class=3),
        BallisticData(range_hexes=20,  penetration=3.0, damage_class=3),
        BallisticData(range_hexes=40,  penetration=2.5, damage_class=2),
        BallisticData(range_hexes=70,  penetration=1.9, damage_class=2),
        BallisticData(range_hexes=100, penetration=1.5, damage_class=1),
        BallisticData(range_hexes=200, penetration=0.6, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.3, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_9mm_mac10_fmj = AmmoType(
    name="9mm Parabellum FMJ (MAC 10)",
    description="FMJ",
    weight=1.4,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=2.1, damage_class=3),
        BallisticData(range_hexes=20,  penetration=1.9, damage_class=3),
        BallisticData(range_hexes=40,  penetration=1.6, damage_class=2),
        BallisticData(range_hexes=70,  penetration=1.3, damage_class=2),
        BallisticData(range_hexes=100, penetration=1.0, damage_class=1),
        BallisticData(range_hexes=200, penetration=0.4, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.2, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_9mm_mac10_jhp = AmmoType(
    name="9mm Parabellum JHP (MAC 10)",
    description="JHP",
    weight=1.4,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=2.0, damage_class=4),
        BallisticData(range_hexes=20,  penetration=1.9, damage_class=4),
        BallisticData(range_hexes=40,  penetration=1.6, damage_class=3),
        BallisticData(range_hexes=70,  penetration=1.2, damage_class=2),
        BallisticData(range_hexes=100, penetration=0.9, damage_class=2),
        BallisticData(range_hexes=200, penetration=0.4, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.2, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_9mm_mac10_ap = AmmoType(
    name="9mm Parabellum AP (MAC 10)",
    description="AP",
    weight=1.4,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=3.0, damage_class=3),
        BallisticData(range_hexes=20,  penetration=2.7, damage_class=3),
        BallisticData(range_hexes=40,  penetration=2.3, damage_class=2),
        BallisticData(range_hexes=70,  penetration=1.8, damage_class=2),
        BallisticData(range_hexes=100, penetration=1.4, damage_class=1),
        BallisticData(range_hexes=200, penetration=0.6, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.2, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_45acp_mac10_fmj = AmmoType(
    name=".45 ACP FMJ (MAC 10)",
    description="FMJ",
    weight=2.2,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=1.7, damage_class=3),
        BallisticData(range_hexes=20,  penetration=1.6, damage_class=2),
        BallisticData(range_hexes=40,  penetration=1.3, damage_class=2),
        BallisticData(range_hexes=70,  penetration=1.0, damage_class=1),
        BallisticData(range_hexes=100, penetration=0.8, damage_class=1),
        BallisticData(range_hexes=200, penetration=0.4, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.2, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_45acp_mac10_jhp = AmmoType(
    name=".45 ACP JHP (MAC 10)",
    description="JHP",
    weight=2.2,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=1.6, damage_class=4),
        BallisticData(range_hexes=20,  penetration=1.5, damage_class=3),
        BallisticData(range_hexes=40,  penetration=1.3, damage_class=3),
        BallisticData(range_hexes=70,  penetration=1.0, damage_class=2),
        BallisticData(range_hexes=100, penetration=0.8, damage_class=1),
        BallisticData(range_hexes=200, penetration=0.4, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.2, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_45acp_mac10_ap = AmmoType(
    name=".45 ACP AP (MAC 10)",
    description="AP",
    weight=2.2,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=2.4, damage_class=3),
        BallisticData(range_hexes=20,  penetration=2.2, damage_class=2),
        BallisticData(range_hexes=40,  penetration=1.9, damage_class=2),
        BallisticData(range_hexes=70,  penetration=1.5, damage_class=1),
        BallisticData(range_hexes=100, penetration=1.2, damage_class=1),
        BallisticData(range_hexes=200, penetration=0.5, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=300, penetration=0.2, damage_class=1, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=0.1, damage_class=1, beyond_max_range=True),
    ]
)

ammo_556_bushmaster_fmj = AmmoType(
    name="5.56mm NATO FMJ (Bushmaster)",
    description="FMJ",
    weight=1.0,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=13, damage_class=6),
        BallisticData(range_hexes=20,  penetration=12, damage_class=6),
        BallisticData(range_hexes=40,  penetration=11, damage_class=5),
        BallisticData(range_hexes=70,  penetration=9.9, damage_class=5),
        BallisticData(range_hexes=100, penetration=8.6, damage_class=4),
        BallisticData(range_hexes=200, penetration=5.3, damage_class=3),
        BallisticData(range_hexes=300, penetration=3.3, damage_class=3),
        BallisticData(range_hexes=400, penetration=2.1, damage_class=2, beyond_max_range=True),
    ]
)

ammo_556_bushmaster_jhp = AmmoType(
    name="5.56mm NATO JHP (Bushmaster)",
    description="JHP",
    weight=1.0,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=13, damage_class=7),
        BallisticData(range_hexes=20,  penetration=12, damage_class=7),
        BallisticData(range_hexes=40,  penetration=11, damage_class=7),
        BallisticData(range_hexes=70,  penetration=9.5, damage_class=7),
        BallisticData(range_hexes=100, penetration=8.2, damage_class=6),
        BallisticData(range_hexes=200, penetration=5.1, damage_class=5),
        BallisticData(range_hexes=300, penetration=3.2, damage_class=4),
        BallisticData(range_hexes=400, penetration=2.0, damage_class=3, beyond_max_range=True),
    ]
)

ammo_556_bushmaster_ap = AmmoType(
    name="5.56mm NATO AP (Bushmaster)",
    description="AP",
    weight=1.0,
    ballistic_data=[
        BallisticData(range_hexes=10,  penetration=18, damage_class=6),
        BallisticData(range_hexes=20,  penetration=18, damage_class=5),
        BallisticData(range_hexes=40,  penetration=16, damage_class=5),
        BallisticData(range_hexes=70,  penetration=14, damage_class=5),
        BallisticData(range_hexes=100, penetration=12, damage_class=4),
        BallisticData(range_hexes=200, penetration=7.5, damage_class=3),
        BallisticData(range_hexes=300, penetration=4.7, damage_class=3),
        BallisticData(range_hexes=400, penetration=2.9, damage_class=2, beyond_max_range=True),
    ]
)

ammo_556_aug_fmj = AmmoType(
    name="5.56mm NATO FMJ (AUG)",
    description="FMJ",
    weight=1.1,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=15.0, damage_class=6),
        BallisticData(range_hexes=20, penetration=14.0, damage_class=6),
        BallisticData(range_hexes=40, penetration=13.0, damage_class=6),
        BallisticData(range_hexes=70, penetration=11.0, damage_class=5),
        BallisticData(range_hexes=100, penetration=9.9, damage_class=5),
        BallisticData(range_hexes=200, penetration=6.3, damage_class=4),
        BallisticData(range_hexes=300, penetration=4.0, damage_class=3),
        BallisticData(range_hexes=400, penetration=2.5, damage_class=2, beyond_max_range=True),
    ]
)

ammo_556_aug_jhp = AmmoType(
    name="5.56mm NATO JHP (AUG)",
    description="JHP",
    weight=1.1,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=14.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=14.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=12.0, damage_class=7),
        BallisticData(range_hexes=70, penetration=11.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=9.5, damage_class=7),
        BallisticData(range_hexes=200, penetration=6.0, damage_class=6),
        BallisticData(range_hexes=300, penetration=3.8, damage_class=4),
        BallisticData(range_hexes=400, penetration=2.4, damage_class=3, beyond_max_range=True),
    ]
)

ammo_556_aug_ap = AmmoType(
    name="5.56mm NATO AP (AUG)",
    description="AP",
    weight=1.1,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=21.0, damage_class=6),
        BallisticData(range_hexes=20, penetration=20.0, damage_class=6),
        BallisticData(range_hexes=40, penetration=18.0, damage_class=6),
        BallisticData(range_hexes=70, penetration=16.0, damage_class=5),
        BallisticData(range_hexes=100, penetration=14.0, damage_class=5),
        BallisticData(range_hexes=200, penetration=8.8, damage_class=3),
        BallisticData(range_hexes=300, penetration=5.6, damage_class=3),
        BallisticData(range_hexes=400, penetration=3.5, damage_class=2, beyond_max_range=True),
    ]
)

ammo_762_l1a1_fmj = AmmoType(
    name="7.62mm NATO FMJ (L1A1)",
    description="FMJ",
    weight=1.6,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=18.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=18.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=17.0, damage_class=8),
        BallisticData(range_hexes=70, penetration=15.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=14.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=9.8, damage_class=6),
        BallisticData(range_hexes=300, penetration=7.0, damage_class=6),
        BallisticData(range_hexes=400, penetration=5.0, damage_class=5, beyond_max_range=True),
    ]
)

ammo_762_l1a1_jhp = AmmoType(
    name="7.62mm NATO JHP (L1A1)",
    description="JHP",
    weight=1.6,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=18.0, damage_class=9),
        BallisticData(range_hexes=20, penetration=17.0, damage_class=9),
        BallisticData(range_hexes=40, penetration=16.0, damage_class=9),
        BallisticData(range_hexes=70, penetration=15.0, damage_class=9),
        BallisticData(range_hexes=100, penetration=13.0, damage_class=9),
        BallisticData(range_hexes=200, penetration=9.4, damage_class=8),
        BallisticData(range_hexes=300, penetration=6.7, damage_class=7),
        BallisticData(range_hexes=400, penetration=4.8, damage_class=7, beyond_max_range=True),
    ]
)

ammo_762_l1a1_ap = AmmoType(
    name="7.62mm NATO AP (L1A1)",
    description="AP",
    weight=1.6,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=26.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=25.0, damage_class=7),
        BallisticData(range_hexes=40, penetration=24.0, damage_class=7),
        BallisticData(range_hexes=70, penetration=21.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=19.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=14.0, damage_class=6),
        BallisticData(range_hexes=300, penetration=9.9, damage_class=6),
        BallisticData(range_hexes=400, penetration=7.1, damage_class=5, beyond_max_range=True),
    ]
)

ammo_762_fal_fmj = AmmoType(
    name="7.62mm NATO FMJ (FN FAL)",
    description="FMJ",
    weight=1.4,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=19.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=19.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=17.0, damage_class=8),
        BallisticData(range_hexes=70, penetration=16.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=14.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=10.0, damage_class=7),
        BallisticData(range_hexes=300, penetration=7.4, damage_class=6),
        BallisticData(range_hexes=400, penetration=5.3, damage_class=5, beyond_max_range=True),
    ]
)

ammo_762_fal_jhp = AmmoType(
    name="7.62mm NATO JHP (FN FAL)",
    description="JHP",
    weight=1.4,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=18.0, damage_class=9),
        BallisticData(range_hexes=20, penetration=18.0, damage_class=9),
        BallisticData(range_hexes=40, penetration=17.0, damage_class=9),
        BallisticData(range_hexes=70, penetration=15.0, damage_class=9),
        BallisticData(range_hexes=100, penetration=14.0, damage_class=9),
        BallisticData(range_hexes=200, penetration=9.8, damage_class=8),
        BallisticData(range_hexes=300, penetration=7.1, damage_class=7),
        BallisticData(range_hexes=400, penetration=5.1, damage_class=7, beyond_max_range=True),
    ]
)

ammo_762_fal_ap = AmmoType(
    name="7.62mm NATO AP (FN FAL)",
    description="AP",
    weight=1.4,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=27.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=26.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=25.0, damage_class=7),
        BallisticData(range_hexes=70, penetration=22.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=20.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=14.0, damage_class=6),
        BallisticData(range_hexes=300, penetration=10.0, damage_class=6),
        BallisticData(range_hexes=400, penetration=7.5, damage_class=5, beyond_max_range=True),
    ]
)

ammo_556_fnc_fmj = AmmoType(
    name="5.56mm NATO FMJ (FNC)",
    description="FMJ",
    weight=1.2,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=15.0, damage_class=6),
        BallisticData(range_hexes=20, penetration=15.0, damage_class=6),
        BallisticData(range_hexes=40, penetration=14.0, damage_class=6),
        BallisticData(range_hexes=70, penetration=12.0, damage_class=6),
        BallisticData(range_hexes=100, penetration=11.0, damage_class=5),
        BallisticData(range_hexes=200, penetration=7.0, damage_class=4),
        BallisticData(range_hexes=300, penetration=4.6, damage_class=3),
        BallisticData(range_hexes=400, penetration=3.0, damage_class=2, beyond_max_range=True),
    ]
)

ammo_556_fnc_jhp = AmmoType(
    name="5.56mm NATO JHP (FNC)",
    description="JHP",
    weight=1.2,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=15.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=14.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=13.0, damage_class=7),
        BallisticData(range_hexes=70, penetration=12.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=10.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=6.7, damage_class=6),
        BallisticData(range_hexes=300, penetration=4.4, damage_class=5),
        BallisticData(range_hexes=400, penetration=2.9, damage_class=3, beyond_max_range=True),
    ]
)

ammo_556_fnc_ap = AmmoType(
    name="5.56mm NATO AP (FNC)",
    description="AP",
    weight=1.2,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=22.0, damage_class=6),
        BallisticData(range_hexes=20, penetration=21.0, damage_class=6),
        BallisticData(range_hexes=40, penetration=19.0, damage_class=6),
        BallisticData(range_hexes=70, penetration=17.0, damage_class=5),
        BallisticData(range_hexes=100, penetration=15.0, damage_class=5),
        BallisticData(range_hexes=200, penetration=9.9, damage_class=4),
        BallisticData(range_hexes=300, penetration=6.5, damage_class=3),
        BallisticData(range_hexes=400, penetration=4.3, damage_class=2, beyond_max_range=True),
    ]
)

ammo_75_m1949_fmj = AmmoType(
    name="7.5 x 54mm FMJ (M1949)",
    description="FMJ",
    weight=0.95,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=18.0, damage_class=7),
        BallisticData(range_hexes=20, penetration=18.0, damage_class=7),
        BallisticData(range_hexes=40, penetration=17.0, damage_class=7),
        BallisticData(range_hexes=70, penetration=15.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=14.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=9.7, damage_class=6),
        BallisticData(range_hexes=300, penetration=7.0, damage_class=6),
        BallisticData(range_hexes=400, penetration=5.0, damage_class=5, beyond_max_range=True),
    ]
)

ammo_75_m1949_jhp = AmmoType(
    name="7.5 x 54mm JHP (M1949)",
    description="JHP",
    weight=0.95,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=17.0, damage_class=9),
        BallisticData(range_hexes=20, penetration=17.0, damage_class=9),
        BallisticData(range_hexes=40, penetration=16.0, damage_class=9),
        BallisticData(range_hexes=70, penetration=14.0, damage_class=9),
        BallisticData(range_hexes=100, penetration=13.0, damage_class=8),
        BallisticData(range_hexes=200, penetration=9.4, damage_class=8),
        BallisticData(range_hexes=300, penetration=6.7, damage_class=7),
        BallisticData(range_hexes=400, penetration=4.8, damage_class=7, beyond_max_range=True),
    ]
)

ammo_75_m1949_ap = AmmoType(
    name="7.5 x 54mm AP (M1949)",
    description="AP",
    weight=0.95,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=26.0, damage_class=7),
        BallisticData(range_hexes=20, penetration=25.0, damage_class=7),
        BallisticData(range_hexes=40, penetration=23.0, damage_class=7),
        BallisticData(range_hexes=70, penetration=21.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=19.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=14.0, damage_class=6),
        BallisticData(range_hexes=300, penetration=9.9, damage_class=5),
        BallisticData(range_hexes=400, penetration=7.1, damage_class=4, beyond_max_range=True),
    ]
)

ammo_556_famas_fmj = AmmoType(
    name="5.56mm NATO FMJ (FA MAS)",
    description="FMJ",
    weight=1.0,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=15.0, damage_class=6),
        BallisticData(range_hexes=20, penetration=15.0, damage_class=6),
        BallisticData(range_hexes=40, penetration=13.0, damage_class=6),
        BallisticData(range_hexes=70, penetration=12.0, damage_class=6),
        BallisticData(range_hexes=100, penetration=10.0, damage_class=5),
        BallisticData(range_hexes=200, penetration=6.4, damage_class=4),
        BallisticData(range_hexes=300, penetration=4.1, damage_class=3),
        BallisticData(range_hexes=400, penetration=2.6, damage_class=2, beyond_max_range=True),
    ]
)

ammo_556_famas_jhp = AmmoType(
    name="5.56mm NATO JHP (FA MAS)",
    description="JHP",
    weight=1.0,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=15.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=14.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=13.0, damage_class=7),
        BallisticData(range_hexes=70, penetration=11.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=9.7, damage_class=7),
        BallisticData(range_hexes=200, penetration=6.2, damage_class=6),
        BallisticData(range_hexes=300, penetration=3.9, damage_class=4),
        BallisticData(range_hexes=200, penetration=2.5, damage_class=3, beyond_max_range=True),
    ]
)

ammo_556_famas_ap = AmmoType(
    name="5.56mm NATO AP (FA MAS)",
    description="AP",
    weight=1.0,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=22.0, damage_class=6),
        BallisticData(range_hexes=20, penetration=21.0, damage_class=6),
        BallisticData(range_hexes=40, penetration=19.0, damage_class=6),
        BallisticData(range_hexes=70, penetration=16.0, damage_class=5),
        BallisticData(range_hexes=100, penetration=14.0, damage_class=5),
        BallisticData(range_hexes=200, penetration=9.1, damage_class=4),
        BallisticData(range_hexes=300, penetration=5.8, damage_class=3),
        BallisticData(range_hexes=400, penetration=3.7, damage_class=2, beyond_max_range=True),
    ]
)

ammo_762_frf2_fmj = AmmoType(
    name="7.62mm NATO FMJ (FR F2)", description="FMJ",
    weight=1.1,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=20.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=19.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=18.0, damage_class=8),
        BallisticData(range_hexes=70, penetration=16.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=15.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=11.0, damage_class=7),
        BallisticData(range_hexes=300, penetration=7.6, damage_class=6),
        BallisticData(range_hexes=400, penetration=5.5, damage_class=5)
    ]
)

ammo_762_frf2_jhp = AmmoType(
    name="7.62mm NATO JHP (FR F2)", description="JHP",
    weight=1.1,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=19.0, damage_class=9),
        BallisticData(range_hexes=20, penetration=18.0, damage_class=9),
        BallisticData(range_hexes=40, penetration=17.0, damage_class=9),
        BallisticData(range_hexes=70, penetration=16.0, damage_class=9),
        BallisticData(range_hexes=100, penetration=14.0, damage_class=9),
        BallisticData(range_hexes=200, penetration=10.0, damage_class=8),
        BallisticData(range_hexes=300, penetration=7.3, damage_class=8),
        BallisticData(range_hexes=400, penetration=5.3, damage_class=7)
    ]
)

ammo_762_frf2_ap = AmmoType(
    name="7.62mm NATO AP (FR F2)", description="AP",
    weight=1.1,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=28.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=27.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=25.0, damage_class=7),
        BallisticData(range_hexes=70, penetration=23.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=21.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=15.0, damage_class=6),
        BallisticData(range_hexes=300, penetration=11.0, damage_class=6),
        BallisticData(range_hexes=400, penetration=7.7, damage_class=5)
    ]
)

ammo_762_g3_fmj = AmmoType(
    name="7.62mm NATO FMJ (G3)", description="FMJ",
    weight=1.4,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=17.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=16.0, damage_class=7),
        BallisticData(range_hexes=40, penetration=15.0, damage_class=7),
        BallisticData(range_hexes=70, penetration=14.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=13.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=8.9, damage_class=6),
        BallisticData(range_hexes=300, penetration=6.3, damage_class=6),
        BallisticData(range_hexes=400, penetration=4.5, damage_class=4, beyond_max_range=True),
    ]
)

ammo_762_g3_jhp = AmmoType(
    name="7.62mm NATO JHP (G3)", description="JHP",
    weight=1.4,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=16.0, damage_class=9),
        BallisticData(range_hexes=20, penetration=16.0, damage_class=9),
        BallisticData(range_hexes=40, penetration=15.0, damage_class=9),
        BallisticData(range_hexes=70, penetration=13.0, damage_class=9),
        BallisticData(range_hexes=100, penetration=12.0, damage_class=8),
        BallisticData(range_hexes=200, penetration=8.5, damage_class=8),
        BallisticData(range_hexes=300, penetration=6.1, damage_class=7),
        BallisticData(range_hexes=400, penetration=4.3, damage_class=6, beyond_max_range=True),
    ]
)

ammo_762_g3_ap = AmmoType(
    name="7.62mm NATO AP (G3)", description="AP",
    weight=1.4,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=24.0, damage_class=7),
        BallisticData(range_hexes=20, penetration=23.0, damage_class=7),
        BallisticData(range_hexes=40, penetration=22.0, damage_class=7),
        BallisticData(range_hexes=70, penetration=20.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=18.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=13.0, damage_class=6),
        BallisticData(range_hexes=300, penetration=8.9, damage_class=5),
        BallisticData(range_hexes=400, penetration=6.4, damage_class=4, beyond_max_range=True),
    ]
)

ammo_556_g41_fmj = AmmoType(
    name="5.56mm NATO FMJ (G41)", description="FMJ",
    weight=1.1,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=16.0, damage_class=6),
        BallisticData(range_hexes=20, penetration=15.0, damage_class=6),
        BallisticData(range_hexes=40, penetration=14.0, damage_class=6),
        BallisticData(range_hexes=70, penetration=13.0, damage_class=6),
        BallisticData(range_hexes=100, penetration=11.0, damage_class=5),
        BallisticData(range_hexes=200, penetration=7.4, damage_class=4),
        BallisticData(range_hexes=300, penetration=4.9, damage_class=3),
        BallisticData(range_hexes=400, penetration=3.2, damage_class=2, beyond_max_range=True),
    ]
)

ammo_556_g41_jhp = AmmoType(
    name="5.56mm NATO JHP (G41)", description="JHP",
    weight=1.1,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=15.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=15.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=14.0, damage_class=8),
        BallisticData(range_hexes=70, penetration=12.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=11.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=7.1, damage_class=6),
        BallisticData(range_hexes=300, penetration=4.7, damage_class=5),
        BallisticData(range_hexes=400, penetration=3.1, damage_class=4, beyond_max_range=True),
    ]
)

ammo_556_g41_ap = AmmoType(
    name="5.56mm NATO AP (G41)", description="AP",
    weight=1.1,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=23.0, damage_class=6),
        BallisticData(range_hexes=20, penetration=22.0, damage_class=6),
        BallisticData(range_hexes=40, penetration=20.0, damage_class=6),
        BallisticData(range_hexes=70, penetration=18.0, damage_class=5),
        BallisticData(range_hexes=100, penetration=16.0, damage_class=5),
        BallisticData(range_hexes=200, penetration=10.0, damage_class=4),
        BallisticData(range_hexes=300, penetration=6.9, damage_class=3),
        BallisticData(range_hexes=400, penetration=4.5, damage_class=2, beyond_max_range=True),
    ]
)

ammo_47_g11_fmj = AmmoType(
    name="4.7mm Caseless FMJ", description="FMJ",
    weight=0.77,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=18.0, damage_class=5),
        BallisticData(range_hexes=20, penetration=18.0, damage_class=5),
        BallisticData(range_hexes=40, penetration=17.0, damage_class=5),
        BallisticData(range_hexes=70, penetration=15.0, damage_class=5),
        BallisticData(range_hexes=100, penetration=14.0, damage_class=4),
        BallisticData(range_hexes=200, penetration=9.9, damage_class=4),
        BallisticData(range_hexes=300, penetration=7.1, damage_class=3),
        BallisticData(range_hexes=400, penetration=5.1, damage_class=3)
    ]
)

ammo_47_g11_jhp = AmmoType(
    name="4.7mm Caseless JHP", description="JHP",
    weight=0.77,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=18.0, damage_class=7),
        BallisticData(range_hexes=20, penetration=17.0, damage_class=7),
        BallisticData(range_hexes=40, penetration=16.0, damage_class=7),
        BallisticData(range_hexes=70, penetration=15.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=13.0, damage_class=6),
        BallisticData(range_hexes=200, penetration=9.5, damage_class=6),
        BallisticData(range_hexes=300, penetration=6.8, damage_class=5),
        BallisticData(range_hexes=400, penetration=4.9, damage_class=4)
    ]
)

ammo_47_g11_ap = AmmoType(
    name="4.7mm Caseless AP", description="AP",
    weight=0.77,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=26.0, damage_class=5),
        BallisticData(range_hexes=20, penetration=25.0, damage_class=5),
        BallisticData(range_hexes=40, penetration=24.0, damage_class=5),
        BallisticData(range_hexes=70, penetration=21.0, damage_class=5),
        BallisticData(range_hexes=100, penetration=19.0, damage_class=4),
        BallisticData(range_hexes=200, penetration=14.0, damage_class=3),
        BallisticData(range_hexes=300, penetration=10.0, damage_class=3),
        BallisticData(range_hexes=400, penetration=7.2, damage_class=3)
    ]
)

ammo_300wm_wa2000_fmj = AmmoType(
    name=".300 Win Mag FMJ", description="FMJ",
    weight=0.9,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=28.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=27.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=25.0, damage_class=8),
        BallisticData(range_hexes=70, penetration=24.0, damage_class=8),
        BallisticData(range_hexes=100, penetration=22.0, damage_class=8),
        BallisticData(range_hexes=200, penetration=17.0, damage_class=7),
        BallisticData(range_hexes=300, penetration=13.0, damage_class=7),
        BallisticData(range_hexes=400, penetration=9.8, damage_class=7)
    ]
)

ammo_300wm_wa2000_jhp = AmmoType(
    name=".300 Win Mag JHP", description="JHP",
    weight=0.9,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=26.0, damage_class=10),
        BallisticData(range_hexes=20, penetration=26.0, damage_class=10),
        BallisticData(range_hexes=40, penetration=24.0, damage_class=10),
        BallisticData(range_hexes=70, penetration=23.0, damage_class=10),
        BallisticData(range_hexes=100, penetration=21.0, damage_class=9),
        BallisticData(range_hexes=200, penetration=16.0, damage_class=9),
        BallisticData(range_hexes=300, penetration=12.0, damage_class=9),
        BallisticData(range_hexes=400, penetration=9.4, damage_class=8)
    ]
)

ammo_300wm_wa2000_ap = AmmoType(
    name=".300 Win Mag AP", description="AP",
    weight=0.9,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=39.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=38.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=36.0, damage_class=8),
        BallisticData(range_hexes=70, penetration=33.0, damage_class=8),
        BallisticData(range_hexes=100, penetration=31.0, damage_class=8),
        BallisticData(range_hexes=200, penetration=24.0, damage_class=7),
        BallisticData(range_hexes=300, penetration=18.0, damage_class=7),
        BallisticData(range_hexes=400, penetration=14.0, damage_class=6)
    ]
)

ammo_762x39_amd65_fmj = AmmoType(
    name="7.62 x 39mm FMJ", description="FMJ",
    weight=1.8,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=11.0, damage_class=7),
        BallisticData(range_hexes=20, penetration=10.0, damage_class=7),
        BallisticData(range_hexes=40, penetration=9.4, damage_class=6),
        BallisticData(range_hexes=70, penetration=8.3, damage_class=6),
        BallisticData(range_hexes=100, penetration=7.2, damage_class=6),
        BallisticData(range_hexes=200, penetration=4.6, damage_class=5),
        BallisticData(range_hexes=300, penetration=3.0, damage_class=3, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=1.9, damage_class=2, beyond_max_range=True),
    ]
)

ammo_762x39_amd65_jhp = AmmoType(
    name="7.62 x 39mm JHP", description="JHP",
    weight=1.8,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=10.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=9.9, damage_class=8),
        BallisticData(range_hexes=40, penetration=9.1, damage_class=8),
        BallisticData(range_hexes=70, penetration=7.9, damage_class=8),
        BallisticData(range_hexes=100, penetration=6.9, damage_class=7),
        BallisticData(range_hexes=200, penetration=4.4, damage_class=7),
        BallisticData(range_hexes=300, penetration=2.8, damage_class=5, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=1.8, damage_class=3, beyond_max_range=True),
    ]
)

ammo_762x39_amd65_ap = AmmoType(
    name="7.62 x 39mm AP", description="AP",
    weight=1.8,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=15.0, damage_class=6),
        BallisticData(range_hexes=20, penetration=15.0, damage_class=6),
        BallisticData(range_hexes=40, penetration=13.0, damage_class=6),
        BallisticData(range_hexes=70, penetration=12.0, damage_class=6),
        BallisticData(range_hexes=100, penetration=10.0, damage_class=6),
        BallisticData(range_hexes=200, penetration=6.5, damage_class=4),
        BallisticData(range_hexes=300, penetration=4.2, damage_class=3, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=2.7, damage_class=2, beyond_max_range=True),
    ]
)

ammo_556_galil_fmj = AmmoType(
    name="5.56mm NATO FMJ (Galil)", description="FMJ",
    weight=1.6,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=16.0, damage_class=6),
        BallisticData(range_hexes=20, penetration=15.0, damage_class=6),
        BallisticData(range_hexes=40, penetration=14.0, damage_class=6),
        BallisticData(range_hexes=70, penetration=12.0, damage_class=6),
        BallisticData(range_hexes=100, penetration=11.0, damage_class=5),
        BallisticData(range_hexes=200, penetration=6.8, damage_class=4),
        BallisticData(range_hexes=300, penetration=4.3, damage_class=3),
        BallisticData(range_hexes=400, penetration=2.7, damage_class=2, beyond_max_range=True)
    ]
)

ammo_556_galil_jhp = AmmoType(
    name="5.56mm NATO JHP (Galil)", description="JHP",
    weight=1.6,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=15.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=15.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=13.0, damage_class=8),
        BallisticData(range_hexes=70, penetration=12.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=10.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=6.5, damage_class=6),
        BallisticData(range_hexes=300, penetration=4.1, damage_class=5),
        BallisticData(range_hexes=400, penetration=2.6, damage_class=3, beyond_max_range=True)
    ]
)

ammo_556_galil_ap = AmmoType(
    name="5.56mm NATO AP (Galil)", description="AP",
    weight=1.6,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=22.0, damage_class=6),
        BallisticData(range_hexes=20, penetration=21.0, damage_class=6),
        BallisticData(range_hexes=40, penetration=20.0, damage_class=6),
        BallisticData(range_hexes=70, penetration=17.0, damage_class=5),
        BallisticData(range_hexes=100, penetration=15.0, damage_class=5),
        BallisticData(range_hexes=200, penetration=9.5, damage_class=4),
        BallisticData(range_hexes=300, penetration=6.1, damage_class=3),
        BallisticData(range_hexes=400, penetration=3.9, damage_class=2, beyond_max_range=True)
    ]
)

ammo_762_galil_fmj = AmmoType(
    name="7.62mm NATO FMJ (Galil)", description="FMJ",
    weight=2.0,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=20.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=19.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=18.0, damage_class=8),
        BallisticData(range_hexes=70, penetration=16.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=15.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=11.0, damage_class=7),
        BallisticData(range_hexes=300, penetration=7.6, damage_class=6),
        BallisticData(range_hexes=400, penetration=5.5, damage_class=5, beyond_max_range=True)
    ]
)

ammo_762_galil_jhp = AmmoType(
    name="7.62mm NATO JHP (Galil)", description="JHP",
    weight=2.0,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=19.0, damage_class=9),
        BallisticData(range_hexes=20, penetration=18.0, damage_class=9),
        BallisticData(range_hexes=40, penetration=17.0, damage_class=9),
        BallisticData(range_hexes=70, penetration=16.0, damage_class=9),
        BallisticData(range_hexes=100, penetration=14.0, damage_class=9),
        BallisticData(range_hexes=200, penetration=10.0, damage_class=8),
        BallisticData(range_hexes=300, penetration=7.3, damage_class=8),
        BallisticData(range_hexes=400, penetration=5.2, damage_class=7, beyond_max_range=True)
    ]
)

ammo_762_galil_ap = AmmoType(
    name="7.62mm NATO AP (Galil)", description="AP",
    weight=2.0,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=28.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=27.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=25.0, damage_class=7),
        BallisticData(range_hexes=70, penetration=23.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=21.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=15.0, damage_class=6),
        BallisticData(range_hexes=300, penetration=11.0, damage_class=6),
        BallisticData(range_hexes=400, penetration=7.7, damage_class=5, beyond_max_range=True)
    ]
)

ammo_762_beretta_bm59_fmj = AmmoType(
    name="7.62mm NATO FMJ (Beretta)", description="FMJ",
    weight=1.5,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=18.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=18.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=17.0, damage_class=8),
        BallisticData(range_hexes=70, penetration=15.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=14.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=9.8, damage_class=6),
        BallisticData(range_hexes=300, penetration=7.0, damage_class=6),
        BallisticData(range_hexes=400, penetration=5.0, damage_class=5, beyond_max_range=True)
    ]
)

ammo_762_beretta_bm59_jhp = AmmoType(
    name="7.62mm NATO JHP (Beretta)", description="JHP",
    weight=1.5,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=18.0, damage_class=9),
        BallisticData(range_hexes=20, penetration=17.0, damage_class=9),
        BallisticData(range_hexes=40, penetration=16.0, damage_class=9),
        BallisticData(range_hexes=70, penetration=15.0, damage_class=9),
        BallisticData(range_hexes=100, penetration=13.0, damage_class=9),
        BallisticData(range_hexes=200, penetration=9.4, damage_class=8),
        BallisticData(range_hexes=300, penetration=6.7, damage_class=7),
        BallisticData(range_hexes=400, penetration=4.8, damage_class=7, beyond_max_range=True)
    ]
)

ammo_762_beretta_bm59_ap = AmmoType(
    name="7.62mm NATO AP (Beretta)", description="AP",
    weight=1.5,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=26.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=25.0, damage_class=7),
        BallisticData(range_hexes=40, penetration=24.0, damage_class=7),
        BallisticData(range_hexes=70, penetration=21.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=19.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=14.0, damage_class=6),
        BallisticData(range_hexes=300, penetration=9.9, damage_class=6),
        BallisticData(range_hexes=400, penetration=7.1, damage_class=5, beyond_max_range=True)
    ]
)

ammo_556_sc70_fmj = AmmoType(
    name="5.56mm NATO FMJ (SC 70)", description="FMJ",
    weight=1.1,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=15.0, damage_class=6),
        BallisticData(range_hexes=20, penetration=14.0, damage_class=6),
        BallisticData(range_hexes=40, penetration=13.0, damage_class=6),
        BallisticData(range_hexes=70, penetration=11.0, damage_class=5),
        BallisticData(range_hexes=100, penetration=10.0, damage_class=5),
        BallisticData(range_hexes=200, penetration=6.3, damage_class=4),
        BallisticData(range_hexes=300, penetration=4.0, damage_class=3),
        BallisticData(range_hexes=400, penetration=2.5, damage_class=2, beyond_max_range=True)
    ]
)

ammo_556_sc70_jhp = AmmoType(
    name="5.56mm NATO JHP (SC 70)", description="JHP",
    weight=1.1,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=14.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=14.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=13.0, damage_class=7),
        BallisticData(range_hexes=70, penetration=11.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=9.5, damage_class=7),
        BallisticData(range_hexes=200, penetration=6.0, damage_class=6),
        BallisticData(range_hexes=300, penetration=3.8, damage_class=4),
        BallisticData(range_hexes=400, penetration=2.4, damage_class=3, beyond_max_range=True)
    ]
)

ammo_556_sc70_ap = AmmoType(
    name="5.56mm NATO AP (SC 70)", description="AP",
    weight=1.1,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=21.0, damage_class=6),
        BallisticData(range_hexes=20, penetration=20.0, damage_class=6),
        BallisticData(range_hexes=40, penetration=18.0, damage_class=6),
        BallisticData(range_hexes=70, penetration=16.0, damage_class=5),
        BallisticData(range_hexes=100, penetration=14.0, damage_class=5),
        BallisticData(range_hexes=200, penetration=8.8, damage_class=4),
        BallisticData(range_hexes=300, penetration=5.6, damage_class=3),
        BallisticData(range_hexes=400, penetration=3.5, damage_class=2, beyond_max_range=True)
    ]
)

ammo_762_type64_fmj = AmmoType(
    name="7.62mm NATO FMJ (Type 64)", description="FMJ",
    weight=1.6,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=13.0, damage_class=7),
        BallisticData(range_hexes=20, penetration=13.0, damage_class=7),
        BallisticData(range_hexes=40, penetration=12.0, damage_class=7),
        BallisticData(range_hexes=70, penetration=11.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=9.7, damage_class=6),
        BallisticData(range_hexes=200, penetration=6.7, damage_class=6),
        BallisticData(range_hexes=300, penetration=4.7, damage_class=4),
        BallisticData(range_hexes=400, penetration=3.3, damage_class=3, beyond_max_range=True)
    ]
)

ammo_762_type64_jhp = AmmoType(
    name="7.62mm NATO JHP (Type 64)", description="JHP",
    weight=1.6,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=13.0, damage_class=9),
        BallisticData(range_hexes=20, penetration=12.0, damage_class=9),
        BallisticData(range_hexes=40, penetration=11.0, damage_class=8),
        BallisticData(range_hexes=70, penetration=10.0, damage_class=8),
        BallisticData(range_hexes=100, penetration=9.3, damage_class=8),
        BallisticData(range_hexes=200, penetration=6.5, damage_class=7),
        BallisticData(range_hexes=300, penetration=4.5, damage_class=6),
        BallisticData(range_hexes=400, penetration=3.2, damage_class=5, beyond_max_range=True)
    ]
)

ammo_762_type64_ap = AmmoType(
    name="7.62mm NATO AP (Type 64)", description="AP",
    weight=1.6,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=19.0, damage_class=7),
        BallisticData(range_hexes=20, penetration=18.0, damage_class=7),
        BallisticData(range_hexes=40, penetration=17.0, damage_class=7),
        BallisticData(range_hexes=70, penetration=15.0, damage_class=6),
        BallisticData(range_hexes=100, penetration=14.0, damage_class=6),
        BallisticData(range_hexes=200, penetration=9.5, damage_class=6),
        BallisticData(range_hexes=300, penetration=6.6, damage_class=4),
        BallisticData(range_hexes=400, penetration=4.6, damage_class=3, beyond_max_range=True)
    ]
)

ammo_556_r4_fmj = AmmoType(
    name="5.56mm NATO FMJ (R4)", description="FMJ",
    weight=1.8,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=16.0, damage_class=6),
        BallisticData(range_hexes=20, penetration=15.0, damage_class=6),
        BallisticData(range_hexes=40, penetration=14.0, damage_class=6),
        BallisticData(range_hexes=70, penetration=12.0, damage_class=6),
        BallisticData(range_hexes=100, penetration=10.0, damage_class=5),
        BallisticData(range_hexes=200, penetration=6.5, damage_class=4),
        BallisticData(range_hexes=300, penetration=4.1, damage_class=3, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=2.6, damage_class=2, beyond_max_range=True)
    ]
)

ammo_556_r4_jhp = AmmoType(
    name="5.56mm NATO JHP (R4)", description="JHP",
    weight=1.8,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=15.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=14.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=13.0, damage_class=8),
        BallisticData(range_hexes=70, penetration=11.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=10.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=6.3, damage_class=6),
        BallisticData(range_hexes=300, penetration=4.0, damage_class=4, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=2.5, damage_class=3, beyond_max_range=True)
    ]
)

ammo_556_r4_ap = AmmoType(
    name="5.56mm NATO AP (R4)", description="AP",
    weight=1.8,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=22.0, damage_class=6),
        BallisticData(range_hexes=20, penetration=21.0, damage_class=6),
        BallisticData(range_hexes=40, penetration=19.0, damage_class=6),
        BallisticData(range_hexes=70, penetration=17.0, damage_class=5),
        BallisticData(range_hexes=100, penetration=15.0, damage_class=5),
        BallisticData(range_hexes=200, penetration=9.2, damage_class=4),
        BallisticData(range_hexes=300, penetration=5.8, damage_class=3, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=3.7, damage_class=2, beyond_max_range=True)
    ]
)

ammo_762x39_akm_fmj = AmmoType(
    name="7.62x39mm FMJ", description="FMJ",
    weight=1.8,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=11.0, damage_class=7),
        BallisticData(range_hexes=20, penetration=11.0, damage_class=7),
        BallisticData(range_hexes=40, penetration=9.8, damage_class=6),
        BallisticData(range_hexes=70, penetration=8.6, damage_class=6),
        BallisticData(range_hexes=100, penetration=7.5, damage_class=6),
        BallisticData(range_hexes=200, penetration=4.8, damage_class=5),
        BallisticData(range_hexes=300, penetration=3.1, damage_class=3, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=2.0, damage_class=2, beyond_max_range=True)
    ]
)

ammo_762x39_akm_jhp = AmmoType(
    name="7.62x39mm JHP", description="JHP",
    weight=1.8,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=11.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=10.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=9.4, damage_class=8),
        BallisticData(range_hexes=70, penetration=8.3, damage_class=8),
        BallisticData(range_hexes=100, penetration=7.2, damage_class=7),
        BallisticData(range_hexes=200, penetration=4.7, damage_class=7),
        BallisticData(range_hexes=300, penetration=3.0, damage_class=5, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=1.9, damage_class=3, beyond_max_range=True)
    ]
)

ammo_762x39_akm_ap = AmmoType(
    name="7.62x39mm AP", description="AP",
    weight=1.8,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=16.0, damage_class=7),
        BallisticData(range_hexes=20, penetration=15.0, damage_class=6),
        BallisticData(range_hexes=40, penetration=14.0, damage_class=6),
        BallisticData(range_hexes=70, penetration=12.0, damage_class=6),
        BallisticData(range_hexes=100, penetration=11.0, damage_class=6),
        BallisticData(range_hexes=200, penetration=6.8, damage_class=4),
        BallisticData(range_hexes=300, penetration=4.4, damage_class=3, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=2.8, damage_class=2, beyond_max_range=True)
    ]
)

ammo_545x39_ak74_fmj = AmmoType(
    name="5.45x39.5mm FMJ", description="FMJ",
    weight=1.1,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=14.0, damage_class=6),
        BallisticData(range_hexes=20, penetration=13.0, damage_class=6),
        BallisticData(range_hexes=40, penetration=12.0, damage_class=5),
        BallisticData(range_hexes=70, penetration=10.0, damage_class=5),
        BallisticData(range_hexes=100, penetration=9.1, damage_class=4),
        BallisticData(range_hexes=200, penetration=5.8, damage_class=3),
        BallisticData(range_hexes=300, penetration=3.7, damage_class=3),
        BallisticData(range_hexes=400, penetration=2.4, damage_class=2, beyond_max_range=True)
    ]
)

ammo_545x39_ak74_jhp = AmmoType(
    name="5.45x39.5mm JHP", description="JHP",
    weight=1.1,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=13.0, damage_class=7),
        BallisticData(range_hexes=20, penetration=13.0, damage_class=7),
        BallisticData(range_hexes=40, penetration=11.0, damage_class=7),
        BallisticData(range_hexes=70, penetration=10.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=8.8, damage_class=6),
        BallisticData(range_hexes=200, penetration=5.6, damage_class=5),
        BallisticData(range_hexes=300, penetration=3.6, damage_class=4),
        BallisticData(range_hexes=400, penetration=2.3, damage_class=3, beyond_max_range=True)
    ]
)

ammo_545x39_ak74_ap = AmmoType(
    name="5.45x39.5mm AP", description="AP",
    weight=1.1,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=19.0, damage_class=6),
        BallisticData(range_hexes=20, penetration=18.0, damage_class=5),
        BallisticData(range_hexes=40, penetration=17.0, damage_class=5),
        BallisticData(range_hexes=70, penetration=15.0, damage_class=5),
        BallisticData(range_hexes=100, penetration=13.0, damage_class=4),
        BallisticData(range_hexes=200, penetration=8.2, damage_class=3),
        BallisticData(range_hexes=300, penetration=5.2, damage_class=3),
        BallisticData(range_hexes=400, penetration=3.3, damage_class=2, beyond_max_range=True)
    ]
)

ammo_762x54_svd_fmj = AmmoType(
    name="7.62x54mm FMJ", description="FMJ",
    weight=0.68,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=23.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=22.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=21.0, damage_class=8),
        BallisticData(range_hexes=70, penetration=19.0, damage_class=8),
        BallisticData(range_hexes=100, penetration=18.0, damage_class=8),
        BallisticData(range_hexes=200, penetration=14.0, damage_class=7),
        BallisticData(range_hexes=300, penetration=10.0, damage_class=7),
        BallisticData(range_hexes=400, penetration=7.8, damage_class=6)
    ]
)

ammo_762x54_svd_jhp = AmmoType(
    name="7.62x54mm JHP", description="JHP",
    weight=0.68,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=22.0, damage_class=10),
        BallisticData(range_hexes=20, penetration=21.0, damage_class=9),
        BallisticData(range_hexes=40, penetration=20.0, damage_class=9),
        BallisticData(range_hexes=70, penetration=19.0, damage_class=9),
        BallisticData(range_hexes=100, penetration=17.0, damage_class=9),
        BallisticData(range_hexes=200, penetration=13.0, damage_class=9),
        BallisticData(range_hexes=300, penetration=9.9, damage_class=8),
        BallisticData(range_hexes=400, penetration=7.5, damage_class=8)
    ]
)

ammo_762x54_svd_ap = AmmoType(
    name="7.62x54mm AP", description="AP",
    weight=0.68,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=32.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=31.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=30.0, damage_class=8),
        BallisticData(range_hexes=70, penetration=27.0, damage_class=8),
        BallisticData(range_hexes=100, penetration=25.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=19.0, damage_class=7),
        BallisticData(range_hexes=300, penetration=15.0, damage_class=6),
        BallisticData(range_hexes=400, penetration=11.0, damage_class=6)
    ]
)

ammo_762nato_l1a1_fmj = AmmoType(
    name="7.62mm NATO FMJ", description="FMJ",
    weight=1.5,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=19.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=19.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=17.0, damage_class=8),
        BallisticData(range_hexes=70, penetration=16.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=14.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=10.0, damage_class=7),
        BallisticData(range_hexes=300, penetration=7.3, damage_class=6),
        BallisticData(range_hexes=400, penetration=5.3, damage_class=5, beyond_max_range=True)
    ]
)

ammo_762nato_l1a1_jhp = AmmoType(
    name="7.62mm NATO JHP", description="JHP",
    weight=1.5,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=18.0, damage_class=9),
        BallisticData(range_hexes=20, penetration=18.0, damage_class=9),
        BallisticData(range_hexes=40, penetration=17.0, damage_class=9),
        BallisticData(range_hexes=70, penetration=15.0, damage_class=9),
        BallisticData(range_hexes=100, penetration=14.0, damage_class=9),
        BallisticData(range_hexes=200, penetration=9.8, damage_class=8),
        BallisticData(range_hexes=300, penetration=7.0, damage_class=7),
        BallisticData(range_hexes=400, penetration=5.1, damage_class=7, beyond_max_range=True)
    ]
)

ammo_762nato_l1a1_ap = AmmoType(
    name="7.62mm NATO AP", description="AP",
    weight=1.5,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=27.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=26.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=24.0, damage_class=7),
        BallisticData(range_hexes=70, penetration=22.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=20.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=14.0, damage_class=6),
        BallisticData(range_hexes=300, penetration=10.0, damage_class=6),
        BallisticData(range_hexes=400, penetration=7.4, damage_class=5, beyond_max_range=True)
    ]
)

ammo_556nato_enfield_fmj = AmmoType(
    name="5.56mm NATO FMJ", description="FMJ",
    weight=1.0,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=16.0, damage_class=6),
        BallisticData(range_hexes=20, penetration=16.0, damage_class=6),
        BallisticData(range_hexes=40, penetration=14.0, damage_class=6),
        BallisticData(range_hexes=70, penetration=13.0, damage_class=6),
        BallisticData(range_hexes=100, penetration=11.0, damage_class=5),
        BallisticData(range_hexes=200, penetration=7.5, damage_class=4),
        BallisticData(range_hexes=300, penetration=4.9, damage_class=3),
        BallisticData(range_hexes=400, penetration=3.3, damage_class=2, beyond_max_range=True)
    ]
)

ammo_556nato_enfield_jhp = AmmoType(
    name="5.56mm NATO JHP", description="JHP",
    weight=1.0,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=16.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=15.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=14.0, damage_class=8),
        BallisticData(range_hexes=70, penetration=12.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=11.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=7.2, damage_class=6),
        BallisticData(range_hexes=300, penetration=4.7, damage_class=5),
        BallisticData(range_hexes=400, penetration=3.1, damage_class=4, beyond_max_range=True)
    ]
)

ammo_556nato_enfield_ap = AmmoType(
    name="5.56mm NATO AP", description="AP",
    weight=1.0,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=23.0, damage_class=6),
        BallisticData(range_hexes=20, penetration=22.0, damage_class=6),
        BallisticData(range_hexes=40, penetration=20.0, damage_class=6),
        BallisticData(range_hexes=70, penetration=18.0, damage_class=5),
        BallisticData(range_hexes=100, penetration=16.0, damage_class=5),
        BallisticData(range_hexes=200, penetration=11.0, damage_class=4),
        BallisticData(range_hexes=300, penetration=7.0, damage_class=3),
        BallisticData(range_hexes=400, penetration=4.6, damage_class=2, beyond_max_range=True)
    ]
)

ammo_762nato_m14_fmj = AmmoType(
    name="7.62mm NATO FMJ", description="FMJ",
    weight=1.5,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=20.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=19.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=18.0, damage_class=8),
        BallisticData(range_hexes=70, penetration=16.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=15.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=11.0, damage_class=7),
        BallisticData(range_hexes=300, penetration=7.7, damage_class=6),
        BallisticData(range_hexes=400, penetration=5.5, damage_class=5, beyond_max_range=True)
    ]
)

ammo_762nato_m14_jhp = AmmoType(
    name="7.62mm NATO JHP", description="JHP",
    weight=1.5,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=19.0, damage_class=9),
        BallisticData(range_hexes=20, penetration=18.0, damage_class=9),
        BallisticData(range_hexes=40, penetration=17.0, damage_class=9),
        BallisticData(range_hexes=70, penetration=16.0, damage_class=9),
        BallisticData(range_hexes=100, penetration=14.0, damage_class=9),
        BallisticData(range_hexes=200, penetration=10.0, damage_class=8),
        BallisticData(range_hexes=300, penetration=7.4, damage_class=8),
        BallisticData(range_hexes=400, penetration=5.3, damage_class=7, beyond_max_range=True)
    ]
)

ammo_762nato_m14_ap = AmmoType(
    name="7.62mm NATO AP", description="AP",
    weight=1.5,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=28.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=27.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=25.0, damage_class=7),
        BallisticData(range_hexes=70, penetration=23.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=21.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=15.0, damage_class=6),
        BallisticData(range_hexes=300, penetration=11.0, damage_class=6),
        BallisticData(range_hexes=400, penetration=7.8, damage_class=5, beyond_max_range=True)
    ]

)

ammo_556nato_m16a1_fmj = AmmoType(
    name="5.56mm NATO FMJ (M16A1)", description="FMJ",
    weight=1.0,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=17.0, damage_class=6),
        BallisticData(range_hexes=20, penetration=16.0, damage_class=6),
        BallisticData(range_hexes=40, penetration=15.0, damage_class=6),
        BallisticData(range_hexes=70, penetration=13.0, damage_class=6),
        BallisticData(range_hexes=100, penetration=11.0, damage_class=5),
        BallisticData(range_hexes=200, penetration=7.1, damage_class=4),
        BallisticData(range_hexes=300, penetration=4.5, damage_class=3),
        BallisticData(range_hexes=400, penetration=2.9, damage_class=2, beyond_max_range=True)
    ]
)

ammo_556nato_m16a1_jhp = AmmoType(
    name="5.56mm NATO JHP (M16A1)", description="JHP",
    weight=1.0,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=16.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=15.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=14.0, damage_class=8),
        BallisticData(range_hexes=70, penetration=12.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=11.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=6.8, damage_class=6),
        BallisticData(range_hexes=300, penetration=4.4, damage_class=5),
        BallisticData(range_hexes=400, penetration=2.8, damage_class=3, beyond_max_range=True)
    ]
)

ammo_556nato_m16a1_ap = AmmoType(
    name="5.56mm NATO AP (M16A1)", description="AP",
    weight=1.0,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=23.0, damage_class=6),
        BallisticData(range_hexes=20, penetration=22.0, damage_class=6),
        BallisticData(range_hexes=40, penetration=20.0, damage_class=6),
        BallisticData(range_hexes=70, penetration=18.0, damage_class=6),
        BallisticData(range_hexes=100, penetration=16.0, damage_class=5),
        BallisticData(range_hexes=200, penetration=10.0, damage_class=4),
        BallisticData(range_hexes=300, penetration=6.4, damage_class=3),
        BallisticData(range_hexes=400, penetration=4.1, damage_class=2, beyond_max_range=True)
    ]
)

ammo_556nato_xm177_fmj = AmmoType(
    name="5.56mm NATO FMJ (CAR 16)", description="FMJ",
    weight=1.0,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=14.0, damage_class=6),
        BallisticData(range_hexes=20, penetration=13.0, damage_class=6),
        BallisticData(range_hexes=40, penetration=12.0, damage_class=6),
        BallisticData(range_hexes=70, penetration=11.0, damage_class=5),
        BallisticData(range_hexes=100, penetration=9.3, damage_class=5),
        BallisticData(range_hexes=200, penetration=5.9, damage_class=4),
        BallisticData(range_hexes=300, penetration=3.7, damage_class=3),
        BallisticData(range_hexes=400, penetration=2.3, damage_class=2, beyond_max_range=True)
    ]
)

ammo_556nato_xm177_jhp = AmmoType(
    name="5.56mm NATO JHP (CAR 16)", description="JHP",
    weight=1.0,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=14.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=13.0, damage_class=7),
        BallisticData(range_hexes=40, penetration=12.0, damage_class=7),
        BallisticData(range_hexes=70, penetration=10.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=8.9, damage_class=7),
        BallisticData(range_hexes=200, penetration=5.6, damage_class=6),
        BallisticData(range_hexes=300, penetration=3.5, damage_class=4),
        BallisticData(range_hexes=400, penetration=2.2, damage_class=3, beyond_max_range=True)
    ]
)

ammo_556nato_xm177_ap = AmmoType(
    name="5.56mm NATO AP (CAR 16)", description="AP",
    weight=1.0,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=20.0, damage_class=6),
        BallisticData(range_hexes=20, penetration=19.0, damage_class=6),
        BallisticData(range_hexes=40, penetration=17.0, damage_class=5),
        BallisticData(range_hexes=70, penetration=15.0, damage_class=5),
        BallisticData(range_hexes=100, penetration=13.0, damage_class=4),
        BallisticData(range_hexes=200, penetration=8.3, damage_class=3),
        BallisticData(range_hexes=300, penetration=5.2, damage_class=3),
        BallisticData(range_hexes=400, penetration=3.3, damage_class=2, beyond_max_range=True)
    ]
)

ammo_556nato_m16a2_fmj = AmmoType(
    name="5.56mm NATO FMJ (M16A2)", description="FMJ",
    weight=1.0,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=17.0, damage_class=6),
        BallisticData(range_hexes=20, penetration=16.0, damage_class=6),
        BallisticData(range_hexes=40, penetration=15.0, damage_class=6),
        BallisticData(range_hexes=70, penetration=13.0, damage_class=6),
        BallisticData(range_hexes=100, penetration=12.0, damage_class=5),
        BallisticData(range_hexes=200, penetration=7.7, damage_class=4),
        BallisticData(range_hexes=300, penetration=5.1, damage_class=3),
        BallisticData(range_hexes=400, penetration=3.4, damage_class=3, beyond_max_range=True)
    ]
)

ammo_556nato_m16a2_jhp = AmmoType(
    name="5.56mm NATO JHP (M16A2)", description="JHP",
    weight=1.0,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=16.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=15.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=14.0, damage_class=8),
        BallisticData(range_hexes=70, penetration=13.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=11.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=7.4, damage_class=6),
        BallisticData(range_hexes=300, penetration=4.9, damage_class=5),
        BallisticData(range_hexes=400, penetration=3.2, damage_class=4, beyond_max_range=True)
    ]
)

ammo_556nato_m16a2_ap = AmmoType(
    name="5.56mm NATO AP (M16A2)", description="AP",
    weight=1.0,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=24.0, damage_class=6),
        BallisticData(range_hexes=20, penetration=23.0, damage_class=6),
        BallisticData(range_hexes=40, penetration=21.0, damage_class=6),
        BallisticData(range_hexes=70, penetration=18.0, damage_class=5),
        BallisticData(range_hexes=100, penetration=16.0, damage_class=5),
        BallisticData(range_hexes=200, penetration=11.0, damage_class=4),
        BallisticData(range_hexes=300, penetration=7.2, damage_class=3),
        BallisticData(range_hexes=400, penetration=4.8, damage_class=2, beyond_max_range=True)
    ]
)

ammo_762nato_m40a1_fmj = AmmoType(
    name="7.62mm NATO FMJ (M40A1)", description="FMJ",
    weight=0.06,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=20.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=19.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=18.0, damage_class=8),
        BallisticData(range_hexes=70, penetration=16.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=15.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=11.0, damage_class=7),
        BallisticData(range_hexes=300, penetration=7.7, damage_class=6),
        BallisticData(range_hexes=400, penetration=5.5, damage_class=5)
    ]
)

ammo_762nato_m40a1_jhp = AmmoType(
    name="7.62mm NATO JHP (M40A1)", description="JHP",
    weight=0.06,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=19.0, damage_class=9),
        BallisticData(range_hexes=20, penetration=18.0, damage_class=9),
        BallisticData(range_hexes=40, penetration=17.0, damage_class=9),
        BallisticData(range_hexes=70, penetration=16.0, damage_class=9),
        BallisticData(range_hexes=100, penetration=14.0, damage_class=9),
        BallisticData(range_hexes=200, penetration=10.0, damage_class=8),
        BallisticData(range_hexes=300, penetration=7.4, damage_class=8),
        BallisticData(range_hexes=400, penetration=5.3, damage_class=7)
    ]
)

ammo_762nato_m40a1_ap = AmmoType(
    name="7.62mm NATO AP (M40A1)", description="AP",
    weight=0.06,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=28.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=27.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=25.0, damage_class=7),
        BallisticData(range_hexes=70, penetration=23.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=21.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=15.0, damage_class=6),
        BallisticData(range_hexes=300, penetration=11.0, damage_class=6),
        BallisticData(range_hexes=400, penetration=7.8, damage_class=5)
    ]
)

ammo_556nato_steyr_fmj = AmmoType(
    name="5.56mm NATO FMJ (Steyr LSW)", description="FMJ",
    weight=1.5,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=17.0, damage_class=6),
        BallisticData(range_hexes=20, penetration=16.0, damage_class=6),
        BallisticData(range_hexes=40, penetration=15.0, damage_class=6),
        BallisticData(range_hexes=70, penetration=13.0, damage_class=6),
        BallisticData(range_hexes=100, penetration=11.0, damage_class=5),
        BallisticData(range_hexes=200, penetration=7.1, damage_class=4),
        BallisticData(range_hexes=300, penetration=4.5, damage_class=3),
        BallisticData(range_hexes=400, penetration=2.9, damage_class=2, beyond_max_range=True)
    ]
)

ammo_556nato_steyr_jhp = AmmoType(
    name="5.56mm NATO JHP (Steyr LSW)", description="JHP",
    weight=1.5,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=16.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=15.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=14.0, damage_class=8),
        BallisticData(range_hexes=70, penetration=12.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=11.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=6.8, damage_class=6),
        BallisticData(range_hexes=300, penetration=4.4, damage_class=5),
        BallisticData(range_hexes=400, penetration=2.8, damage_class=3, beyond_max_range=True)
    ]
)

ammo_556nato_steyr_ap = AmmoType(
    name="5.56mm NATO AP (Steyr LSW)", description="AP",
    weight=1.5,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=23.0, damage_class=6),
        BallisticData(range_hexes=20, penetration=22.0, damage_class=6),
        BallisticData(range_hexes=40, penetration=20.0, damage_class=6),
        BallisticData(range_hexes=70, penetration=18.0, damage_class=6),
        BallisticData(range_hexes=100, penetration=16.0, damage_class=5),
        BallisticData(range_hexes=200, penetration=10.0, damage_class=4),
        BallisticData(range_hexes=300, penetration=6.4, damage_class=3),
        BallisticData(range_hexes=400, penetration=4.1, damage_class=2, beyond_max_range=True)
    ]
)

ammo_762nato_fnmag_fmj = AmmoType(
    name="7.62mm NATO FMJ (FN MAG)", description="FMJ",
    weight=3.2,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=19.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=19.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=17.0, damage_class=8),
        BallisticData(range_hexes=70, penetration=16.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=14.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=10.0, damage_class=7),
        BallisticData(range_hexes=300, penetration=7.4, damage_class=6),
        BallisticData(range_hexes=400, penetration=5.3, damage_class=5, beyond_max_range=True)
    ]
)

ammo_762nato_fnmag_jhp = AmmoType(
    name="7.62mm NATO JHP (FN MAG)", description="JHP",
    weight=3.2,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=18.0, damage_class=9),
        BallisticData(range_hexes=20, penetration=18.0, damage_class=9),
        BallisticData(range_hexes=40, penetration=17.0, damage_class=9),
        BallisticData(range_hexes=70, penetration=15.0, damage_class=9),
        BallisticData(range_hexes=100, penetration=14.0, damage_class=9),
        BallisticData(range_hexes=200, penetration=9.8, damage_class=8),
        BallisticData(range_hexes=300, penetration=7.1, damage_class=7),
        BallisticData(range_hexes=400, penetration=5.1, damage_class=7, beyond_max_range=True)
    ]
)

ammo_762nato_fnmag_ap = AmmoType(
    name="7.62mm NATO AP (FN MAG)", description="AP",
    weight=3.2,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=27.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=26.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=25.0, damage_class=7),
        BallisticData(range_hexes=70, penetration=22.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=20.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=14.0, damage_class=6),
        BallisticData(range_hexes=300, penetration=10.0, damage_class=6),
        BallisticData(range_hexes=400, penetration=7.5, damage_class=5, beyond_max_range=True)
    ]
)

ammo_762x54_type67_fmj = AmmoType(
    name="7.62x54mm FMJ (Type 67)", description="FMJ",
    weight=5.8,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=23.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=22.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=21.0, damage_class=8),
        BallisticData(range_hexes=70, penetration=20.0, damage_class=8),
        BallisticData(range_hexes=100, penetration=18.0, damage_class=8),
        BallisticData(range_hexes=200, penetration=14.0, damage_class=7),
        BallisticData(range_hexes=300, penetration=10.0, damage_class=7),
        BallisticData(range_hexes=400, penetration=8.0, damage_class=6)
    ]
)

ammo_762x54_type67_jhp = AmmoType(
    name="7.62x54mm JHP (Type 67)", description="JHP",
    weight=5.8,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=22.0, damage_class=10),
        BallisticData(range_hexes=20, penetration=22.0, damage_class=9),
        BallisticData(range_hexes=40, penetration=20.0, damage_class=9),
        BallisticData(range_hexes=70, penetration=19.0, damage_class=9),
        BallisticData(range_hexes=100, penetration=17.0, damage_class=9),
        BallisticData(range_hexes=200, penetration=13.0, damage_class=9),
        BallisticData(range_hexes=300, penetration=10.0, damage_class=8),
        BallisticData(range_hexes=400, penetration=7.6, damage_class=8)
    ]
)

ammo_762x54_type67_ap = AmmoType(
    name="7.62x54mm AP (Type 67)", description="AP",
    weight=5.8,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=33.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=32.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=30.0, damage_class=8),
        BallisticData(range_hexes=70, penetration=28.0, damage_class=8),
        BallisticData(range_hexes=100, penetration=25.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=19.0, damage_class=7),
        BallisticData(range_hexes=300, penetration=15.0, damage_class=6),
        BallisticData(range_hexes=400, penetration=11.0, damage_class=6)
    ]
)

ammo_762nato_aa762_fmj = AmmoType(
    name="7.62mm NATO FMJ (AA 7.62)", description="FMJ",
    weight=6.5,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=19.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=19.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=17.0, damage_class=8),
        BallisticData(range_hexes=70, penetration=16.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=14.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=10.0, damage_class=7),
        BallisticData(range_hexes=300, penetration=7.4, damage_class=6),
        BallisticData(range_hexes=400, penetration=5.3, damage_class=5, beyond_max_range=True)
    ]
)

ammo_762nato_aa762_jhp = AmmoType(
    name="7.62mm NATO JHP (AA 7.62)", description="JHP",
    weight=6.5,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=19.0, damage_class=9),
        BallisticData(range_hexes=20, penetration=18.0, damage_class=9),
        BallisticData(range_hexes=40, penetration=17.0, damage_class=9),
        BallisticData(range_hexes=70, penetration=15.0, damage_class=9),
        BallisticData(range_hexes=100, penetration=14.0, damage_class=9),
        BallisticData(range_hexes=200, penetration=9.9, damage_class=8),
        BallisticData(range_hexes=300, penetration=7.1, damage_class=7),
        BallisticData(range_hexes=400, penetration=5.1, damage_class=7, beyond_max_range=True)
    ]
)

ammo_762nato_aa762_ap = AmmoType(
    name="7.62mm NATO AP (AA 7.62)", description="AP",
    weight=6.5,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=27.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=26.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=25.0, damage_class=7),
        BallisticData(range_hexes=70, penetration=22.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=20.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=15.0, damage_class=6),
        BallisticData(range_hexes=300, penetration=10.0, damage_class=6),
        BallisticData(range_hexes=400, penetration=7.5, damage_class=5, beyond_max_range=True)
    ]
)

ammo_556nato_hk13e_fmj = AmmoType(
    name="5.56mm NATO FMJ (HK 13E)", description="FMJ",
    weight=1.1,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=17.0, damage_class=6),
        BallisticData(range_hexes=20, penetration=16.0, damage_class=6),
        BallisticData(range_hexes=40, penetration=15.0, damage_class=6),
        BallisticData(range_hexes=70, penetration=13.0, damage_class=6),
        BallisticData(range_hexes=100, penetration=12.0, damage_class=5),
        BallisticData(range_hexes=200, penetration=7.7, damage_class=4),
        BallisticData(range_hexes=300, penetration=5.1, damage_class=3),
        BallisticData(range_hexes=400, penetration=3.4, damage_class=3, beyond_max_range=True)
    ]
)

ammo_556nato_hk13e_jhp = AmmoType(
    name="5.56mm NATO JHP (HK 13E)", description="JHP",
    weight=1.1,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=16.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=15.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=14.0, damage_class=8),
        BallisticData(range_hexes=70, penetration=13.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=11.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=7.3, damage_class=6),
        BallisticData(range_hexes=300, penetration=4.9, damage_class=5),
        BallisticData(range_hexes=400, penetration=3.2, damage_class=4, beyond_max_range=True)
    ]
)

ammo_556nato_hk13e_ap = AmmoType(
    name="5.56mm NATO AP (HK 13E)", description="AP",
    weight=1.1,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=23.0, damage_class=6),
        BallisticData(range_hexes=20, penetration=23.0, damage_class=6),
        BallisticData(range_hexes=40, penetration=21.0, damage_class=6),
        BallisticData(range_hexes=70, penetration=18.0, damage_class=5),
        BallisticData(range_hexes=100, penetration=16.0, damage_class=5),
        BallisticData(range_hexes=200, penetration=11.0, damage_class=4),
        BallisticData(range_hexes=300, penetration=7.2, damage_class=3),
        BallisticData(range_hexes=400, penetration=4.8, damage_class=2, beyond_max_range=True)
    ]
)

ammo_762nato_hk11e_fmj = AmmoType(
    name="7.62mm NATO FMJ (HK 11E)", description="FMJ",
    weight=1.5,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=17.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=17.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=16.0, damage_class=7),
        BallisticData(range_hexes=70, penetration=14.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=13.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=9.2, damage_class=6),
        BallisticData(range_hexes=300, penetration=6.5, damage_class=6),
        BallisticData(range_hexes=400, penetration=4.7, damage_class=4, beyond_max_range=True)
    ]
)

ammo_762nato_hk11e_jhp = AmmoType(
    name="7.62mm NATO JHP (HK 11E)", description="JHP",
    weight=1.5,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=17.0, damage_class=9),
        BallisticData(range_hexes=20, penetration=16.0, damage_class=9),
        BallisticData(range_hexes=40, penetration=15.0, damage_class=9),
        BallisticData(range_hexes=70, penetration=14.0, damage_class=9),
        BallisticData(range_hexes=100, penetration=12.0, damage_class=9),
        BallisticData(range_hexes=200, penetration=8.8, damage_class=8),
        BallisticData(range_hexes=300, penetration=6.3, damage_class=7),
        BallisticData(range_hexes=400, penetration=4.5, damage_class=6, beyond_max_range=True)
    ]
)

ammo_762nato_hk11e_ap = AmmoType(
    name="7.62mm NATO AP (HK 11E)", description="AP",
    weight=1.5,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=25.0, damage_class=7),
        BallisticData(range_hexes=20, penetration=24.0, damage_class=7),
        BallisticData(range_hexes=40, penetration=22.0, damage_class=7),
        BallisticData(range_hexes=70, penetration=20.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=18.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=13.0, damage_class=6),
        BallisticData(range_hexes=300, penetration=9.2, damage_class=5),
        BallisticData(range_hexes=400, penetration=6.6, damage_class=4, beyond_max_range=True)
    ]
)

ammo_556nato_hk23e_fmj = AmmoType(
    name="5.56mm NATO FMJ (HK 23E)", description="FMJ",
    weight=6.2,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=16.0, damage_class=6),
        BallisticData(range_hexes=20, penetration=16.0, damage_class=6),
        BallisticData(range_hexes=40, penetration=15.0, damage_class=6),
        BallisticData(range_hexes=70, penetration=13.0, damage_class=6),
        BallisticData(range_hexes=100, penetration=11.0, damage_class=5),
        BallisticData(range_hexes=200, penetration=7.6, damage_class=4),
        BallisticData(range_hexes=300, penetration=5.0, damage_class=3),
        BallisticData(range_hexes=400, penetration=3.3, damage_class=3, beyond_max_range=True)
    ]
)

ammo_556nato_hk23e_jhp = AmmoType(
    name="5.56mm NATO JHP (HK 23E)", description="JHP",
    weight=6.2,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=16.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=15.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=14.0, damage_class=8),
        BallisticData(range_hexes=70, penetration=12.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=11.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=7.3, damage_class=6),
        BallisticData(range_hexes=300, penetration=4.8, damage_class=5),
        BallisticData(range_hexes=400, penetration=3.2, damage_class=4, beyond_max_range=True)
    ]
)

ammo_556nato_hk23e_ap = AmmoType(
    name="5.56mm NATO AP (HK 23E)", description="AP",
    weight=6.2,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=23.0, damage_class=6),
        BallisticData(range_hexes=20, penetration=22.0, damage_class=6),
        BallisticData(range_hexes=40, penetration=21.0, damage_class=6),
        BallisticData(range_hexes=70, penetration=18.0, damage_class=5),
        BallisticData(range_hexes=100, penetration=16.0, damage_class=5),
        BallisticData(range_hexes=200, penetration=11.0, damage_class=4),
        BallisticData(range_hexes=300, penetration=7.1, damage_class=3),
        BallisticData(range_hexes=400, penetration=4.7, damage_class=2, beyond_max_range=True)
    ]
)

ammo_762nato_hk21e_fmj = AmmoType(
    name="7.62mm NATO FMJ (HK 21E)", description="FMJ",
    weight=6.5,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=19.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=19.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=17.0, damage_class=8),
        BallisticData(range_hexes=70, penetration=16.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=14.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=10.0, damage_class=7),
        BallisticData(range_hexes=300, penetration=7.4, damage_class=6),
        BallisticData(range_hexes=400, penetration=5.3, damage_class=5, beyond_max_range=True)
    ]
)

ammo_762nato_hk21e_jhp = AmmoType(
    name="7.62mm NATO JHP (HK 21E)", description="JHP",
    weight=6.5,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=19.0, damage_class=9),
        BallisticData(range_hexes=20, penetration=18.0, damage_class=9),
        BallisticData(range_hexes=40, penetration=17.0, damage_class=9),
        BallisticData(range_hexes=70, penetration=15.0, damage_class=9),
        BallisticData(range_hexes=100, penetration=14.0, damage_class=9),
        BallisticData(range_hexes=200, penetration=9.9, damage_class=8),
        BallisticData(range_hexes=300, penetration=7.1, damage_class=7),
        BallisticData(range_hexes=400, penetration=5.1, damage_class=7, beyond_max_range=True)
    ]
)

ammo_762nato_hk21e_ap = AmmoType(
    name="7.62mm NATO AP (HK 21E)", description="AP",
    weight=6.5,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=27.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=26.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=25.0, damage_class=7),
        BallisticData(range_hexes=70, penetration=22.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=20.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=15.0, damage_class=6),
        BallisticData(range_hexes=300, penetration=10.0, damage_class=6),
        BallisticData(range_hexes=400, penetration=7.5, damage_class=5, beyond_max_range=True)
    ]
)

ammo_762nato_mg3_fmj = AmmoType(
    name="7.62mm NATO FMJ (MG3)", description="FMJ",
    weight=6.5,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=18.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=18.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=17.0, damage_class=7),
        BallisticData(range_hexes=70, penetration=15.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=14.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=9.7, damage_class=6),
        BallisticData(range_hexes=300, penetration=7.0, damage_class=6),
        BallisticData(range_hexes=400, penetration=5.0, damage_class=5, beyond_max_range=True)
    ]
)

ammo_762nato_mg3_jhp = AmmoType(
    name="7.62mm NATO JHP (MG3)", description="JHP",
    weight=6.5,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=18.0, damage_class=9),
        BallisticData(range_hexes=20, penetration=17.0, damage_class=9),
        BallisticData(range_hexes=40, penetration=16.0, damage_class=9),
        BallisticData(range_hexes=70, penetration=14.0, damage_class=9),
        BallisticData(range_hexes=100, penetration=13.0, damage_class=9),
        BallisticData(range_hexes=200, penetration=9.3, damage_class=8),
        BallisticData(range_hexes=300, penetration=6.7, damage_class=7),
        BallisticData(range_hexes=400, penetration=4.8, damage_class=7, beyond_max_range=True)
    ]
)

ammo_762nato_mg3_ap = AmmoType(
    name="7.62mm NATO AP (MG3)", description="AP",
    weight=6.5,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=26.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=25.0, damage_class=7),
        BallisticData(range_hexes=40, penetration=23.0, damage_class=7),
        BallisticData(range_hexes=70, penetration=21.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=19.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=14.0, damage_class=6),
        BallisticData(range_hexes=300, penetration=9.8, damage_class=6),
        BallisticData(range_hexes=400, penetration=7.0, damage_class=5, beyond_max_range=True)
    ]
)

ammo_556nato_galil_fmj = AmmoType(
    name="5.56mm NATO FMJ (Galil ARM)", description="FMJ",
    weight=2.2,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=16.0, damage_class=6),
        BallisticData(range_hexes=20, penetration=15.0, damage_class=6),
        BallisticData(range_hexes=40, penetration=14.0, damage_class=6),
        BallisticData(range_hexes=70, penetration=12.0, damage_class=6),
        BallisticData(range_hexes=100, penetration=11.0, damage_class=5),
        BallisticData(range_hexes=200, penetration=6.8, damage_class=4),
        BallisticData(range_hexes=300, penetration=4.3, damage_class=3),
        BallisticData(range_hexes=400, penetration=2.7, damage_class=2, beyond_max_range=True)
    ]
)

ammo_556nato_galil_jhp = AmmoType(
    name="5.56mm NATO JHP (Galil ARM)", description="JHP",
    weight=2.2,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=15.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=15.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=13.0, damage_class=8),
        BallisticData(range_hexes=70, penetration=12.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=10.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=6.5, damage_class=6),
        BallisticData(range_hexes=300, penetration=4.1, damage_class=5),
        BallisticData(range_hexes=400, penetration=2.6, damage_class=3, beyond_max_range=True)
    ]
)

ammo_556nato_galil_ap = AmmoType(
    name="5.56mm NATO AP (Galil ARM)", description="AP",
    weight=2.2,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=22.0, damage_class=6),
        BallisticData(range_hexes=20, penetration=21.0, damage_class=6),
        BallisticData(range_hexes=40, penetration=20.0, damage_class=5),
        BallisticData(range_hexes=100, penetration=15.0, damage_class=5),
        BallisticData(range_hexes=200, penetration=9.5, damage_class=4),
        BallisticData(range_hexes=300, penetration=6.1, damage_class=3),
        BallisticData(range_hexes=400, penetration=3.9, damage_class=2, beyond_max_range=True)
    ]
)

ammo_556nato_beretta_fmj = AmmoType(
    name="5.56mm NATO FMJ (Beretta M70-78)", description="FMJ",
    weight=1.7,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=16.0, damage_class=6),
        BallisticData(range_hexes=20, penetration=15.0, damage_class=6),
        BallisticData(range_hexes=40, penetration=14.0, damage_class=6),
        BallisticData(range_hexes=70, penetration=12.0, damage_class=6),
        BallisticData(range_hexes=100, penetration=10.0, damage_class=5),
        BallisticData(range_hexes=200, penetration=6.6, damage_class=4),
        BallisticData(range_hexes=300, penetration=4.2, damage_class=3),
        BallisticData(range_hexes=400, penetration=2.7, damage_class=2, beyond_max_range=True)
    ]
)

ammo_556nato_beretta_jhp = AmmoType(
    name="5.56mm NATO JHP (Beretta M70-78)", description="JHP",
    weight=1.7,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=15.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=14.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=13.0, damage_class=8),
        BallisticData(range_hexes=70, penetration=11.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=10.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=6.3, damage_class=6),
        BallisticData(range_hexes=300, penetration=4.0, damage_class=4),
        BallisticData(range_hexes=400, penetration=2.6, damage_class=3, beyond_max_range=True)
    ]
)

ammo_556nato_beretta_ap = AmmoType(
    name="5.56mm NATO AP (Beretta M70-78)", description="AP",
    weight=1.7,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=22.0, damage_class=6),
        BallisticData(range_hexes=20, penetration=21.0, damage_class=6),
        BallisticData(range_hexes=40, penetration=19.0, damage_class=6),
        BallisticData(range_hexes=70, penetration=17.0, damage_class=5),
        BallisticData(range_hexes=100, penetration=15.0, damage_class=5),
        BallisticData(range_hexes=200, penetration=9.3, damage_class=4),
        BallisticData(range_hexes=300, penetration=5.9, damage_class=3),
        BallisticData(range_hexes=400, penetration=3.8, damage_class=2, beyond_max_range=True)
    ]
)

ammo_545sov_rpk74_fmj = AmmoType(
    name="5.45x39.5mm FMJ (RPK 74)", description="FMJ",
    weight=1.5,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=17.0, damage_class=6),
        BallisticData(range_hexes=20, penetration=16.0, damage_class=6),
        BallisticData(range_hexes=40, penetration=15.0, damage_class=6),
        BallisticData(range_hexes=70, penetration=13.0, damage_class=6),
        BallisticData(range_hexes=100, penetration=12.0, damage_class=5),
        BallisticData(range_hexes=200, penetration=7.5, damage_class=4),
        BallisticData(range_hexes=300, penetration=4.9, damage_class=3),
        BallisticData(range_hexes=400, penetration=3.2, damage_class=2, beyond_max_range=True)
    ]
)

ammo_545sov_rpk74_jhp = AmmoType(
    name="5.45x39.5mm JHP (RPK 74)", description="JHP",
    weight=1.5,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=16.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=16.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=14.0, damage_class=8),
        BallisticData(range_hexes=70, penetration=13.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=11.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=7.2, damage_class=6),
        BallisticData(range_hexes=300, penetration=4.7, damage_class=5),
        BallisticData(range_hexes=400, penetration=3.1, damage_class=4, beyond_max_range=True)
    ]
)

ammo_545sov_rpk74_ap = AmmoType(
    name="5.45x39.5mm AP (RPK 74)", description="AP",
    weight=1.5,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=24.0, damage_class=6),
        BallisticData(range_hexes=20, penetration=23.0, damage_class=6),
        BallisticData(range_hexes=40, penetration=21.0, damage_class=6),
        BallisticData(range_hexes=70, penetration=19.0, damage_class=5),
        BallisticData(range_hexes=100, penetration=16.0, damage_class=5),
        BallisticData(range_hexes=200, penetration=11.0, damage_class=4),
        BallisticData(range_hexes=300, penetration=6.9, damage_class=3),
        BallisticData(range_hexes=400, penetration=4.5, damage_class=2, beyond_max_range=True)
    ]
)

ammo_762sov_rpk_fmj = AmmoType(
    name="7.62x39mm FMJ (RPK)", description="FMJ",
    weight=4.6,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=12.0, damage_class=7),
        BallisticData(range_hexes=20, penetration=11.0, damage_class=7),
        BallisticData(range_hexes=40, penetration=10.0, damage_class=7),
        BallisticData(range_hexes=70, penetration=9.1, damage_class=6),
        BallisticData(range_hexes=100, penetration=7.9, damage_class=6),
        BallisticData(range_hexes=200, penetration=5.1, damage_class=5),
        BallisticData(range_hexes=300, penetration=3.3, damage_class=3, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=2.1, damage_class=2, beyond_max_range=True)
    ]
)

ammo_762sov_rpk_jhp = AmmoType(
    name="7.62x39mm JHP (RPK)", description="JHP",
    weight=4.6,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=11.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=11.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=10.0, damage_class=8),
        BallisticData(range_hexes=70, penetration=8.7, damage_class=8),
        BallisticData(range_hexes=100, penetration=7.6, damage_class=8),
        BallisticData(range_hexes=200, penetration=4.9, damage_class=7),
        BallisticData(range_hexes=300, penetration=3.2, damage_class=5, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=2.1, damage_class=3, beyond_max_range=True)
    ]
)

ammo_762sov_rpk_ap = AmmoType(
    name="7.62x39mm AP (RPK)", description="AP",
    weight=4.6,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=17.0, damage_class=7),
        BallisticData(range_hexes=20, penetration=16.0, damage_class=7),
        BallisticData(range_hexes=40, penetration=15.0, damage_class=6),
        BallisticData(range_hexes=70, penetration=13.0, damage_class=6),
        BallisticData(range_hexes=100, penetration=11.0, damage_class=6),
        BallisticData(range_hexes=200, penetration=7.2, damage_class=5),
        BallisticData(range_hexes=300, penetration=4.7, damage_class=3, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=3.0, damage_class=2, beyond_max_range=True)
    ]
)

ammo_762R_rp46_fmj = AmmoType(
    name="7.62x54mmR FMJ (RP 46)", description="FMJ",
    weight=14.3,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=23.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=23.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=22.0, damage_class=8),
        BallisticData(range_hexes=70, penetration=20.0, damage_class=8),
        BallisticData(range_hexes=100, penetration=18.0, damage_class=8),
        BallisticData(range_hexes=200, penetration=14.0, damage_class=7),
        BallisticData(range_hexes=300, penetration=11.0, damage_class=7),
        BallisticData(range_hexes=400, penetration=8.1, damage_class=6)
    ]
)

ammo_762R_rp46_jhp = AmmoType(
    name="7.62x54mmR JHP (RP 46)", description="JHP",
    weight=14.3,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=22.0, damage_class=10),
        BallisticData(range_hexes=20, penetration=22.0, damage_class=10),
        BallisticData(range_hexes=40, penetration=21.0, damage_class=9),
        BallisticData(range_hexes=70, penetration=19.0, damage_class=9),
        BallisticData(range_hexes=100, penetration=18.0, damage_class=9),
        BallisticData(range_hexes=200, penetration=13.0, damage_class=9),
        BallisticData(range_hexes=300, penetration=10.0, damage_class=8),
        BallisticData(range_hexes=400, penetration=7.7, damage_class=8)
    ]
)

ammo_762R_rp46_ap = AmmoType(
    name="7.62x54mmR AP (RP 46)", description="AP",
    weight=14.3,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=33.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=32.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=30.0, damage_class=8),
        BallisticData(range_hexes=70, penetration=28.0, damage_class=8),
        BallisticData(range_hexes=100, penetration=26.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=20.0, damage_class=7),
        BallisticData(range_hexes=300, penetration=15.0, damage_class=6),
        BallisticData(range_hexes=400, penetration=11.0, damage_class=6)
    ]
)

ammo_762sov_rpd_fmj = AmmoType(
    name="7.62x39mm FMJ (RPD)", description="FMJ",
    weight=5.3,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=11.0, damage_class=7),
        BallisticData(range_hexes=20, penetration=10.0, damage_class=7),
        BallisticData(range_hexes=40, penetration=9.4, damage_class=6),
        BallisticData(range_hexes=70, penetration=8.2, damage_class=6),
        BallisticData(range_hexes=100, penetration=7.2, damage_class=6),
        BallisticData(range_hexes=200, penetration=4.6, damage_class=5),
        BallisticData(range_hexes=300, penetration=3.0, damage_class=3, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=1.9, damage_class=2, beyond_max_range=True)
    ]
)

ammo_762sov_rpd_jhp = AmmoType(
    name="7.62x39mm JHP (RPD)", description="JHP",
    weight=5.3,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=10.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=9.9, damage_class=8),
        BallisticData(range_hexes=40, penetration=9.0, damage_class=8),
        BallisticData(range_hexes=70, penetration=7.9, damage_class=8),
        BallisticData(range_hexes=100, penetration=6.9, damage_class=7),
        BallisticData(range_hexes=200, penetration=4.4, damage_class=6),
        BallisticData(range_hexes=300, penetration=2.8, damage_class=5, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=1.8, damage_class=3, beyond_max_range=True)
    ]
)

ammo_762sov_rpd_ap = AmmoType(
    name="7.62x39mm AP (RPD)", description="AP",
    weight=5.3,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=15.0, damage_class=6),
        BallisticData(range_hexes=20, penetration=14.0, damage_class=6),
        BallisticData(range_hexes=40, penetration=13.0, damage_class=6),
        BallisticData(range_hexes=70, penetration=12.0, damage_class=6),
        BallisticData(range_hexes=100, penetration=10.0, damage_class=6),
        BallisticData(range_hexes=200, penetration=6.5, damage_class=4),
        BallisticData(range_hexes=300, penetration=4.2, damage_class=3, beyond_max_range=True),
        BallisticData(range_hexes=400, penetration=2.7, damage_class=2, beyond_max_range=True)
    ]
)

ammo_762R_pkm_fmj = AmmoType(
    name="7.62x54mmR FMJ (PKM)", description="FMJ",
    weight=5.7,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=23.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=22.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=21.0, damage_class=8),
        BallisticData(range_hexes=70, penetration=19.0, damage_class=8),
        BallisticData(range_hexes=100, penetration=18.0, damage_class=8),
        BallisticData(range_hexes=200, penetration=13.0, damage_class=7),
        BallisticData(range_hexes=300, penetration=10.0, damage_class=7),
        BallisticData(range_hexes=400, penetration=7.7, damage_class=6)
    ]
)

ammo_762R_pkm_jhp = AmmoType(
    name="7.62x54mmR JHP (PKM)", description="JHP",
    weight=5.7,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=22.0, damage_class=10),
        BallisticData(range_hexes=20, penetration=21.0, damage_class=9),
        BallisticData(range_hexes=40, penetration=20.0, damage_class=9),
        BallisticData(range_hexes=70, penetration=18.0, damage_class=9),
        BallisticData(range_hexes=100, penetration=17.0, damage_class=9),
        BallisticData(range_hexes=200, penetration=13.0, damage_class=9),
        BallisticData(range_hexes=300, penetration=9.7, damage_class=8),
        BallisticData(range_hexes=400, penetration=7.4, damage_class=8)
    ]
)

ammo_762R_pkm_ap = AmmoType(
    name="7.62x54mmR AP (PKM)", description="AP",
    weight=5.7,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=32.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=31.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=29.0, damage_class=8),
        BallisticData(range_hexes=70, penetration=27.0, damage_class=8),
        BallisticData(range_hexes=100, penetration=25.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=19.0, damage_class=7),
        BallisticData(range_hexes=300, penetration=14.0, damage_class=6),
        BallisticData(range_hexes=400, penetration=11.0, damage_class=6)
    ]
)

ammo_127sov_nsv_fmj = AmmoType(
    name="12.7x107mm FMJ (NSV)", description="FMJ",
    weight=17.0,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=45.0, damage_class=10),
        BallisticData(range_hexes=20, penetration=44.0, damage_class=10),
        BallisticData(range_hexes=40, penetration=43.0, damage_class=10),
        BallisticData(range_hexes=70, penetration=40.0, damage_class=10),
        BallisticData(range_hexes=100, penetration=38.0, damage_class=10),
        BallisticData(range_hexes=200, penetration=32.0, damage_class=10),
        BallisticData(range_hexes=300, penetration=27.0, damage_class=10),
        BallisticData(range_hexes=400, penetration=23.0, damage_class=10)
    ]
)

ammo_127sov_nsv_jhp = AmmoType(
    name="12.7x107mm JHP (NSV)", description="JHP",
    weight=17.0,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=43.0, damage_class=10),
        BallisticData(range_hexes=20, penetration=42.0, damage_class=10),
        BallisticData(range_hexes=40, penetration=41.0, damage_class=10),
        BallisticData(range_hexes=70, penetration=39.0, damage_class=10),
        BallisticData(range_hexes=100, penetration=37.0, damage_class=10),
        BallisticData(range_hexes=200, penetration=31.0, damage_class=10),
        BallisticData(range_hexes=300, penetration=26.0, damage_class=10),
        BallisticData(range_hexes=400, penetration=22.0, damage_class=10)
    ]
)

ammo_127sov_nsv_ap = AmmoType(
    name="12.7x107mm AP (NSV)", description="AP",
    weight=17.0,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=63.0, damage_class=10),
        BallisticData(range_hexes=20, penetration=62.0, damage_class=10),
        BallisticData(range_hexes=40, penetration=60.0, damage_class=10),
        BallisticData(range_hexes=70, penetration=57.0, damage_class=10),
        BallisticData(range_hexes=100, penetration=54.0, damage_class=10),
        BallisticData(range_hexes=200, penetration=45.0, damage_class=10),
        BallisticData(range_hexes=300, penetration=38.0, damage_class=10),
        BallisticData(range_hexes=400, penetration=32.0, damage_class=10)
    ]
)

ammo_556nato_lsw_fmj = AmmoType(
    name="5.56mm NATO FMJ (Enfield LSW)", description="FMJ",
    weight=1.0,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=16.0, damage_class=6),
        BallisticData(range_hexes=20, penetration=15.0, damage_class=6),
        BallisticData(range_hexes=40, penetration=14.0, damage_class=6),
        BallisticData(range_hexes=70, penetration=12.0, damage_class=6),
        BallisticData(range_hexes=100, penetration=10.0, damage_class=5),
        BallisticData(range_hexes=200, penetration=6.6, damage_class=4),
        BallisticData(range_hexes=300, penetration=4.2, damage_class=3),
        BallisticData(range_hexes=400, penetration=2.7, damage_class=2, beyond_max_range=True)
    ]
)

ammo_556nato_lsw_jhp = AmmoType(
    name="5.56mm NATO JHP (Enfield LSW)", description="JHP",
    weight=1.0,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=15.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=14.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=13.0, damage_class=8),
        BallisticData(range_hexes=70, penetration=11.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=10.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=6.3, damage_class=6),
        BallisticData(range_hexes=300, penetration=4.0, damage_class=4),
        BallisticData(range_hexes=400, penetration=2.6, damage_class=3, beyond_max_range=True)
    ]
)

ammo_556nato_lsw_ap = AmmoType(
    name="5.56mm NATO AP (Enfield LSW)", description="AP",
    weight=1.0,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=22.0, damage_class=6),
        BallisticData(range_hexes=20, penetration=21.0, damage_class=6),
        BallisticData(range_hexes=40, penetration=19.0, damage_class=6),
        BallisticData(range_hexes=70, penetration=17.0, damage_class=5),
        BallisticData(range_hexes=100, penetration=15.0, damage_class=5),
        BallisticData(range_hexes=200, penetration=9.3, damage_class=4),
        BallisticData(range_hexes=300, penetration=5.9, damage_class=3),
        BallisticData(range_hexes=400, penetration=3.8, damage_class=2, beyond_max_range=True)
    ]
)

ammo_762nato_bren_fmj = AmmoType(
    name="7.62mm NATO FMJ (Bren L4)", description="FMJ",
    weight=2.6,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=18.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=18.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=17.0, damage_class=8),
        BallisticData(range_hexes=70, penetration=15.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=14.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=9.8, damage_class=6),
        BallisticData(range_hexes=300, penetration=7.0, damage_class=6),
        BallisticData(range_hexes=400, penetration=5.0, damage_class=5, beyond_max_range=True)
    ]
)

ammo_762nato_bren_jhp = AmmoType(
    name="7.62mm NATO JHP (Bren L4)", description="JHP",
    weight=2.6,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=18.0, damage_class=9),
        BallisticData(range_hexes=20, penetration=17.0, damage_class=9),
        BallisticData(range_hexes=40, penetration=16.0, damage_class=9),
        BallisticData(range_hexes=70, penetration=15.0, damage_class=9),
        BallisticData(range_hexes=100, penetration=13.0, damage_class=8),
        BallisticData(range_hexes=200, penetration=9.4, damage_class=8),
        BallisticData(range_hexes=300, penetration=6.7, damage_class=7),
        BallisticData(range_hexes=400, penetration=4.8, damage_class=7, beyond_max_range=True)
    ]
)

ammo_762nato_bren_ap = AmmoType(
    name="7.62mm NATO AP (Bren L4)", description="AP",
    weight=2.6,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=26.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=25.0, damage_class=7),
        BallisticData(range_hexes=40, penetration=24.0, damage_class=7),
        BallisticData(range_hexes=70, penetration=21.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=19.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=14.0, damage_class=6),
        BallisticData(range_hexes=300, penetration=9.9, damage_class=6),
        BallisticData(range_hexes=400, penetration=7.1, damage_class=5, beyond_max_range=True)
    ]
)

ammo_762nato_l7a2_fmj = AmmoType(
    name="7.62mm NATO FMJ (L7A2)", description="FMJ",
    weight=6.5,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=19.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=19.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=17.0, damage_class=8),
        BallisticData(range_hexes=70, penetration=16.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=14.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=10.0, damage_class=7),
        BallisticData(range_hexes=300, penetration=7.3, damage_class=6),
        BallisticData(range_hexes=400, penetration=5.3, damage_class=5, beyond_max_range=True)
    ]
)

ammo_762nato_l7a2_jhp = AmmoType(
    name="7.62mm NATO JHP (L7A2)", description="JHP",
    weight=6.5,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=18.0, damage_class=9),
        BallisticData(range_hexes=20, penetration=18.0, damage_class=9),
        BallisticData(range_hexes=40, penetration=17.0, damage_class=9),
        BallisticData(range_hexes=70, penetration=15.0, damage_class=9),
        BallisticData(range_hexes=100, penetration=14.0, damage_class=9),
        BallisticData(range_hexes=200, penetration=9.8, damage_class=8),
        BallisticData(range_hexes=300, penetration=7.0, damage_class=7),
        BallisticData(range_hexes=400, penetration=5.1, damage_class=7, beyond_max_range=True)
    ]
)

ammo_762nato_l7a2_ap = AmmoType(
    name="7.62mm NATO AP (L7A2)", description="AP",
    weight=6.5,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=27.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=26.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=24.0, damage_class=7),
        BallisticData(range_hexes=70, penetration=22.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=20.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=14.0, damage_class=7),
        BallisticData(range_hexes=300, penetration=10.0, damage_class=6),
        BallisticData(range_hexes=400, penetration=7.4, damage_class=5, beyond_max_range=True)
    ]
)

ammo_556nato_m249_fmj = AmmoType(
    name="5.56mm NATO FMJ (M249)", description="FMJ",
    weight=6.9,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=15.0, damage_class=6),
        BallisticData(range_hexes=20, penetration=15.0, damage_class=6),
        BallisticData(range_hexes=40, penetration=14.0, damage_class=6),
        BallisticData(range_hexes=70, penetration=12.0, damage_class=6),
        BallisticData(range_hexes=100, penetration=11.0, damage_class=5),
        BallisticData(range_hexes=200, penetration=7.0, damage_class=4),
        BallisticData(range_hexes=300, penetration=4.6, damage_class=3),
        BallisticData(range_hexes=400, penetration=3.0, damage_class=2, beyond_max_range=True)
    ]
)

ammo_556nato_m249_jhp = AmmoType(
    name="5.56mm NATO JHP (M249)", description="JHP",
    weight=6.9,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=15.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=14.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=13.0, damage_class=7),
        BallisticData(range_hexes=70, penetration=12.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=10.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=6.7, damage_class=6),
        BallisticData(range_hexes=300, penetration=4.4, damage_class=5),
        BallisticData(range_hexes=400, penetration=2.9, damage_class=3, beyond_max_range=True)
    ]
)

ammo_556nato_m249_ap = AmmoType(
    name="5.56mm NATO AP (M249)", description="AP",
    weight=6.9,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=22.0, damage_class=6),
        BallisticData(range_hexes=20, penetration=21.0, damage_class=6),
        BallisticData(range_hexes=40, penetration=19.0, damage_class=6),
        BallisticData(range_hexes=70, penetration=17.0, damage_class=5),
        BallisticData(range_hexes=100, penetration=15.0, damage_class=5),
        BallisticData(range_hexes=200, penetration=9.9, damage_class=4),
        BallisticData(range_hexes=300, penetration=6.5, damage_class=3),
        BallisticData(range_hexes=400, penetration=4.3, damage_class=2, beyond_max_range=True)
    ]
)

ammo_762nato_m60_fmj = AmmoType(
    name="7.62mm NATO FMJ (M60)", description="FMJ",
    weight=6.5,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=20.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=19.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=18.0, damage_class=8),
        BallisticData(range_hexes=70, penetration=16.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=15.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=11.0, damage_class=7),
        BallisticData(range_hexes=300, penetration=7.7, damage_class=6),
        BallisticData(range_hexes=400, penetration=5.5, damage_class=5, beyond_max_range=True)
    ]
)

ammo_762nato_m60_jhp = AmmoType(
    name="7.62mm NATO JHP (M60)", description="JHP",
    weight=6.5,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=19.0, damage_class=9),
        BallisticData(range_hexes=20, penetration=19.0, damage_class=9),
        BallisticData(range_hexes=40, penetration=17.0, damage_class=9),
        BallisticData(range_hexes=70, penetration=16.0, damage_class=9),
        BallisticData(range_hexes=100, penetration=14.0, damage_class=9),
        BallisticData(range_hexes=200, penetration=10.0, damage_class=8),
        BallisticData(range_hexes=300, penetration=7.4, damage_class=8),
        BallisticData(range_hexes=400, penetration=5.3, damage_class=7, beyond_max_range=True)
    ]
)

ammo_762nato_m60_ap = AmmoType(
    name="7.62mm NATO AP (M60)", description="AP",
    weight=6.5,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=28.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=27.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=25.0, damage_class=7),
        BallisticData(range_hexes=70, penetration=23.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=21.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=15.0, damage_class=7),
        BallisticData(range_hexes=300, penetration=11.0, damage_class=6),
        BallisticData(range_hexes=400, penetration=7.8, damage_class=5, beyond_max_range=True)
    ]
)

ammo_762nato_m60e3_fmj = AmmoType(
    name="7.62mm NATO FMJ (M60E3)", description="FMJ",
    weight=6.5,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=20.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=20.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=18.0, damage_class=8),
        BallisticData(range_hexes=70, penetration=17.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=15.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=11.0, damage_class=7),
        BallisticData(range_hexes=300, penetration=7.8, damage_class=6),
        BallisticData(range_hexes=400, penetration=5.6, damage_class=5, beyond_max_range=True)
    ]
)

ammo_762nato_m60e3_jhp = AmmoType(
    name="7.62mm NATO JHP (M60E3)", description="JHP",
    weight=6.5,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=19.0, damage_class=9),
        BallisticData(range_hexes=20, penetration=19.0, damage_class=9),
        BallisticData(range_hexes=40, penetration=18.0, damage_class=9),
        BallisticData(range_hexes=70, penetration=16.0, damage_class=9),
        BallisticData(range_hexes=100, penetration=14.0, damage_class=9),
        BallisticData(range_hexes=200, penetration=10.0, damage_class=8),
        BallisticData(range_hexes=300, penetration=7.5, damage_class=8),
        BallisticData(range_hexes=400, penetration=5.4, damage_class=7, beyond_max_range=True)
    ]
)

ammo_762nato_m60e3_ap = AmmoType(
    name="7.62mm NATO AP (M60E3)", description="AP",
    weight=6.5,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=28.0, damage_class=8),
        BallisticData(range_hexes=20, penetration=28.0, damage_class=8),
        BallisticData(range_hexes=40, penetration=26.0, damage_class=8),
        BallisticData(range_hexes=70, penetration=23.0, damage_class=7),
        BallisticData(range_hexes=100, penetration=21.0, damage_class=7),
        BallisticData(range_hexes=200, penetration=15.0, damage_class=6),
        BallisticData(range_hexes=300, penetration=11.0, damage_class=6),
        BallisticData(range_hexes=400, penetration=7.9, damage_class=5, beyond_max_range=True)
    ]
)

ammo_50bmg_m2hb_fmj = AmmoType(
    name=".50 Browning FMJ (M2HB)", description="FMJ",
    weight=28.8,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=40.0, damage_class=10),
        BallisticData(range_hexes=20, penetration=39.0, damage_class=10),
        BallisticData(range_hexes=40, penetration=37.0, damage_class=10),
        BallisticData(range_hexes=70, penetration=35.0, damage_class=10),
        BallisticData(range_hexes=100, penetration=34.0, damage_class=10),
        BallisticData(range_hexes=200, penetration=28.0, damage_class=10),
        BallisticData(range_hexes=300, penetration=23.0, damage_class=10),
        BallisticData(range_hexes=400, penetration=19.0, damage_class=10)
    ]
)

ammo_50bmg_m2hb_jhp = AmmoType(
    name=".50 Browning JHP (M2HB)", description="JHP",
    weight=28.8,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=38.0, damage_class=10),
        BallisticData(range_hexes=20, penetration=37.0, damage_class=10),
        BallisticData(range_hexes=40, penetration=36.0, damage_class=10),
        BallisticData(range_hexes=70, penetration=34.0, damage_class=10),
        BallisticData(range_hexes=100, penetration=32.0, damage_class=10),
        BallisticData(range_hexes=200, penetration=27.0, damage_class=10),
        BallisticData(range_hexes=300, penetration=22.0, damage_class=10),
        BallisticData(range_hexes=400, penetration=19.0, damage_class=10)
    ]
)

ammo_50bmg_m2hb_ap = AmmoType(
    name=".50 Browning AP (M2HB)", description="AP",
    weight=28.8,
    ballistic_data=[
        BallisticData(range_hexes=10, penetration=56.0, damage_class=10),
        BallisticData(range_hexes=20, penetration=55.0, damage_class=10),
        BallisticData(range_hexes=40, penetration=53.0, damage_class=10),
        BallisticData(range_hexes=70, penetration=50.0, damage_class=10),
        BallisticData(range_hexes=100, penetration=47.0, damage_class=10),
        BallisticData(range_hexes=200, penetration=39.0, damage_class=10),
        BallisticData(range_hexes=300, penetration=33.0, damage_class=10),
        BallisticData(range_hexes=400, penetration=27.0, damage_class=10)
    ]
)

ammo_12g_spas_aps = AmmoType(
    name="12 Gauge APS (Franchi SPAS 12)", description="APS",
    weight=0.13,
    ballistic_data=[
        BallisticData(range_hexes=1, penetration=21.0, damage_class=9),
        BallisticData(range_hexes=2, penetration=21.0, damage_class=9),
        BallisticData(range_hexes=4, penetration=21.0, damage_class=9),
        BallisticData(range_hexes=6, penetration=21.0, damage_class=9),
        BallisticData(range_hexes=8, penetration=21.0, damage_class=9),
        BallisticData(range_hexes=10, penetration=21.0, damage_class=9),
        BallisticData(range_hexes=15, penetration=21.0, damage_class=9),
        BallisticData(range_hexes=20, penetration=20.0, damage_class=9),
        BallisticData(range_hexes=30, penetration=20.0, damage_class=9),
        BallisticData(range_hexes=40, penetration=19.0, damage_class=9),
        BallisticData(range_hexes=80, penetration=18.0, damage_class=8)
    ]
)

ammo_12g_spas_shot = AmmoType(
    name="12 Gauge Shot (00) (Franchi SPAS 12)", description="Shot", pellet_count=12,
    weight=0.13,
    ballistic_data=[
        BallisticData(range_hexes=1, penetration=5.3, damage_class=8, shotgun_accuracy_level_modifier=-13, base_pellet_hit_chance=None, pattern_radius=0.0),
        BallisticData(range_hexes=2, penetration=1.6, damage_class=3, shotgun_accuracy_level_modifier=-8, base_pellet_hit_chance="*11", pattern_radius=0.0),
        BallisticData(range_hexes=4, penetration=1.5, damage_class=3, shotgun_accuracy_level_modifier=-3, base_pellet_hit_chance="*10", pattern_radius=0.0),
        BallisticData(range_hexes=6, penetration=1.5, damage_class=3, shotgun_accuracy_level_modifier=0, base_pellet_hit_chance="*9", pattern_radius=0.1),
        BallisticData(range_hexes=8, penetration=1.4, damage_class=3, shotgun_accuracy_level_modifier=2, base_pellet_hit_chance="*5", pattern_radius=0.1),
        BallisticData(range_hexes=10, penetration=1.4, damage_class=3, shotgun_accuracy_level_modifier=4, base_pellet_hit_chance="*4", pattern_radius=0.1),
        BallisticData(range_hexes=15, penetration=1.3, damage_class=2, shotgun_accuracy_level_modifier=7, base_pellet_hit_chance="*2", pattern_radius=0.2),
        BallisticData(range_hexes=20, penetration=1.2, damage_class=2, shotgun_accuracy_level_modifier=9, base_pellet_hit_chance="94", pattern_radius=0.2),
        BallisticData(range_hexes=30, penetration=1.1, damage_class=2, shotgun_accuracy_level_modifier=12, base_pellet_hit_chance="42", pattern_radius=0.3),
        BallisticData(range_hexes=40, penetration=0.9, damage_class=2, shotgun_accuracy_level_modifier=14, base_pellet_hit_chance="24", pattern_radius=0.4),
        BallisticData(range_hexes=80, penetration=0.5, damage_class=1, shotgun_accuracy_level_modifier=19, base_pellet_hit_chance="5", pattern_radius=0.9)
    ]
)

ammo_12g_caws_slug = AmmoType(
    name="12 Gauge Slug (CAWS)", description="Slug",
    weight=2.1,
    ballistic_data=[
        BallisticData(range_hexes=1, penetration=7.0, damage_class=10),
        BallisticData(range_hexes=2, penetration=7.0, damage_class=10),
        BallisticData(range_hexes=4, penetration=6.9, damage_class=10),
        BallisticData(range_hexes=6, penetration=6.9, damage_class=10),
        BallisticData(range_hexes=8, penetration=6.8, damage_class=10),
        BallisticData(range_hexes=10, penetration=6.7, damage_class=10),
        BallisticData(range_hexes=15, penetration=6.6, damage_class=9),
        BallisticData(range_hexes=20, penetration=6.5, damage_class=9),
        BallisticData(range_hexes=30, penetration=6.3, damage_class=9),
        BallisticData(range_hexes=40, penetration=6.0, damage_class=9),
        BallisticData(range_hexes=80, penetration=5.2, damage_class=8)
    ]
)

ammo_12g_caws_shot = AmmoType(
    name="12 Gauge Shot (000) (CAWS)", description="Shot", pellet_count=8,
    weight=2.1,
    ballistic_data=[
        BallisticData(range_hexes=1, penetration=5.6, damage_class=8, shotgun_accuracy_level_modifier=-13, base_pellet_hit_chance=None, pattern_radius=0.0),
        BallisticData(range_hexes=2, penetration=2.4, damage_class=4, shotgun_accuracy_level_modifier=-8, base_pellet_hit_chance="*7", pattern_radius=0.0),
        BallisticData(range_hexes=4, penetration=2.4, damage_class=4, shotgun_accuracy_level_modifier=-3, base_pellet_hit_chance="*7", pattern_radius=0.0),
        BallisticData(range_hexes=6, penetration=2.3, damage_class=4, shotgun_accuracy_level_modifier=0, base_pellet_hit_chance="*6", pattern_radius=0.1),
        BallisticData(range_hexes=8, penetration=2.3, damage_class=4, shotgun_accuracy_level_modifier=2, base_pellet_hit_chance="*4", pattern_radius=0.1),
        BallisticData(range_hexes=10, penetration=2.2, damage_class=4, shotgun_accuracy_level_modifier=4, base_pellet_hit_chance="*2", pattern_radius=0.1),
        BallisticData(range_hexes=15, penetration=2.1, damage_class=3, shotgun_accuracy_level_modifier=7, base_pellet_hit_chance="*1", pattern_radius=0.2),
        BallisticData(range_hexes=20, penetration=2.0, damage_class=3, shotgun_accuracy_level_modifier=9, base_pellet_hit_chance="66", pattern_radius=0.2),
        BallisticData(range_hexes=30, penetration=1.7, damage_class=3, shotgun_accuracy_level_modifier=11, base_pellet_hit_chance="30", pattern_radius=0.3),
        BallisticData(range_hexes=40, penetration=1.5, damage_class=3, shotgun_accuracy_level_modifier=14, base_pellet_hit_chance="16", pattern_radius=0.4),
        BallisticData(range_hexes=80, penetration=0.9, damage_class=2, shotgun_accuracy_level_modifier=19, base_pellet_hit_chance="3", pattern_radius=0.9)
    ]
)

ammo_12g_mossberg_slug = AmmoType(
    name="12 Gauge Slug (Mossberg Bullpup)", description="Slug",
    weight=0.13,
    ballistic_data=[
        BallisticData(range_hexes=1, penetration=7.5, damage_class=10),
        BallisticData(range_hexes=2, penetration=7.4, damage_class=10),
        BallisticData(range_hexes=4, penetration=7.4, damage_class=10),
        BallisticData(range_hexes=6, penetration=7.3, damage_class=10),
        BallisticData(range_hexes=8, penetration=7.3, damage_class=10),
        BallisticData(range_hexes=10, penetration=7.2, damage_class=10),
        BallisticData(range_hexes=15, penetration=7.1, damage_class=10),
        BallisticData(range_hexes=20, penetration=7.0, damage_class=10),
        BallisticData(range_hexes=30, penetration=6.7, damage_class=9),
        BallisticData(range_hexes=40, penetration=6.5, damage_class=9),
        BallisticData(range_hexes=80, penetration=5.6, damage_class=9)
    ]
)

ammo_12g_mossberg_shot = AmmoType(
    name="12 Gauge Shot (00) (Mossberg Bullpup)", description="Shot", pellet_count=12,
    weight=0.13,
    ballistic_data=[
        BallisticData(range_hexes=1, penetration=5.4, damage_class=8, shotgun_accuracy_level_modifier=-14, base_pellet_hit_chance=None, pattern_radius=0.0),
        BallisticData(range_hexes=2, penetration=1.7, damage_class=3, shotgun_accuracy_level_modifier=-9, base_pellet_hit_chance="*11", pattern_radius=0.0),
        BallisticData(range_hexes=4, penetration=1.6, damage_class=3, shotgun_accuracy_level_modifier=-4, base_pellet_hit_chance="*10", pattern_radius=0.0),
        BallisticData(range_hexes=6, penetration=1.6, damage_class=3, shotgun_accuracy_level_modifier=-1, base_pellet_hit_chance="*9", pattern_radius=0.1),
        BallisticData(range_hexes=8, penetration=1.6, damage_class=3, shotgun_accuracy_level_modifier=1, base_pellet_hit_chance="*7", pattern_radius=0.1),
        BallisticData(range_hexes=10, penetration=1.5, damage_class=3, shotgun_accuracy_level_modifier=2, base_pellet_hit_chance="*5", pattern_radius=0.1),
        BallisticData(range_hexes=15, penetration=1.4, damage_class=2, shotgun_accuracy_level_modifier=5, base_pellet_hit_chance="*2", pattern_radius=0.1),
        BallisticData(range_hexes=20, penetration=1.3, damage_class=2, shotgun_accuracy_level_modifier=7, base_pellet_hit_chance="*1", pattern_radius=0.2),
        BallisticData(range_hexes=30, penetration=1.1, damage_class=2, shotgun_accuracy_level_modifier=10, base_pellet_hit_chance="62", pattern_radius=0.3),
        BallisticData(range_hexes=40, penetration=1.0, damage_class=2, shotgun_accuracy_level_modifier=12, base_pellet_hit_chance="35", pattern_radius=0.4),
        BallisticData(range_hexes=80, penetration=0.6, damage_class=1, shotgun_accuracy_level_modifier=17, base_pellet_hit_chance="8", pattern_radius=0.7)
    ]
)

ammo_12g_remington_slug = AmmoType(
    name="12 Gauge Slug (Remington M870)", description="Slug",
    weight=0.13,
    ballistic_data=[
        BallisticData(range_hexes=1, penetration=7.7, damage_class=10),
        BallisticData(range_hexes=2, penetration=7.7, damage_class=10),
        BallisticData(range_hexes=4, penetration=7.6, damage_class=10),
        BallisticData(range_hexes=6, penetration=7.5, damage_class=10),
        BallisticData(range_hexes=8, penetration=7.5, damage_class=10),
        BallisticData(range_hexes=10, penetration=7.4, damage_class=10),
        BallisticData(range_hexes=15, penetration=7.3, damage_class=10),
        BallisticData(range_hexes=20, penetration=7.2, damage_class=10),
        BallisticData(range_hexes=30, penetration=6.9, damage_class=10),
        BallisticData(range_hexes=40, penetration=6.7, damage_class=9),
        BallisticData(range_hexes=80, penetration=5.7, damage_class=9)
    ]
)

ammo_12g_remington_shot = AmmoType(
    name="12 Gauge Shot (00) (Remington M870)", description="Shot", pellet_count=12,
    weight=0.13,
    ballistic_data=[
        BallisticData(range_hexes=1, penetration=5.4, damage_class=8, shotgun_accuracy_level_modifier=-14, base_pellet_hit_chance=None, pattern_radius=0.0),
        BallisticData(range_hexes=2, penetration=1.7, damage_class=3, shotgun_accuracy_level_modifier=-9, base_pellet_hit_chance="*11", pattern_radius=0.0),
        BallisticData(range_hexes=4, penetration=1.7, damage_class=3, shotgun_accuracy_level_modifier=-4, base_pellet_hit_chance="*10", pattern_radius=0.0),
        BallisticData(range_hexes=6, penetration=1.6, damage_class=3, shotgun_accuracy_level_modifier=-1, base_pellet_hit_chance="*9", pattern_radius=0.1),
        BallisticData(range_hexes=8, penetration=1.6, damage_class=3, shotgun_accuracy_level_modifier=1, base_pellet_hit_chance="*7", pattern_radius=0.1),
        BallisticData(range_hexes=10, penetration=1.6, damage_class=3, shotgun_accuracy_level_modifier=2, base_pellet_hit_chance="*5", pattern_radius=0.1),
        BallisticData(range_hexes=15, penetration=1.4, damage_class=2, shotgun_accuracy_level_modifier=5, base_pellet_hit_chance="*2", pattern_radius=0.1),
        BallisticData(range_hexes=20, penetration=1.4, damage_class=2, shotgun_accuracy_level_modifier=7, base_pellet_hit_chance="*1", pattern_radius=0.2),
        BallisticData(range_hexes=30, penetration=1.2, damage_class=2, shotgun_accuracy_level_modifier=10, base_pellet_hit_chance="62", pattern_radius=0.3),
        BallisticData(range_hexes=40, penetration=1.0, damage_class=2, shotgun_accuracy_level_modifier=12, base_pellet_hit_chance="35", pattern_radius=0.4),
        BallisticData(range_hexes=80, penetration=0.6, damage_class=1, shotgun_accuracy_level_modifier=17, base_pellet_hit_chance="8", pattern_radius=0.7)
    ]
)

ammo_12g_high_standard_slug = AmmoType(
    name="12 Gauge Slug (High Standard M10B)", description="Slug",
    weight=0.13,
    ballistic_data=[
        BallisticData(range_hexes=1, penetration=7.0, damage_class=10),
        BallisticData(range_hexes=2, penetration=7.0, damage_class=10),
        BallisticData(range_hexes=4, penetration=6.9, damage_class=10),
        BallisticData(range_hexes=6, penetration=6.9, damage_class=10),
        BallisticData(range_hexes=8, penetration=6.8, damage_class=10),
        BallisticData(range_hexes=10, penetration=6.7, damage_class=10),
        BallisticData(range_hexes=15, penetration=6.6, damage_class=9),
        BallisticData(range_hexes=20, penetration=6.5, damage_class=9),
        BallisticData(range_hexes=30, penetration=6.3, damage_class=9),
        BallisticData(range_hexes=40, penetration=6.0, damage_class=9),
        BallisticData(range_hexes=80, penetration=5.2, damage_class=8)
    ]
)

ammo_12g_high_standard_shot = AmmoType(
    name="12 Gauge Shot (00) (High Standard M10B)", description="Shot", pellet_count=12,
    weight=0.13,
    ballistic_data=[
        BallisticData(range_hexes=1, penetration=5.3, damage_class=8, shotgun_accuracy_level_modifier=-13, base_pellet_hit_chance=None, pattern_radius=0.0),
        BallisticData(range_hexes=2, penetration=1.6, damage_class=3, shotgun_accuracy_level_modifier=-8, base_pellet_hit_chance="*11", pattern_radius=0.0),
        BallisticData(range_hexes=4, penetration=1.5, damage_class=3, shotgun_accuracy_level_modifier=-3, base_pellet_hit_chance="*10", pattern_radius=0.0),
        BallisticData(range_hexes=6, penetration=1.5, damage_class=2, shotgun_accuracy_level_modifier=0, base_pellet_hit_chance="*9", pattern_radius=0.1),
        BallisticData(range_hexes=8, penetration=1.4, damage_class=2, shotgun_accuracy_level_modifier=2, base_pellet_hit_chance="*5", pattern_radius=0.1),
        BallisticData(range_hexes=10, penetration=1.4, damage_class=2, shotgun_accuracy_level_modifier=4, base_pellet_hit_chance="*3", pattern_radius=0.1),
        BallisticData(range_hexes=15, penetration=1.3, damage_class=2, shotgun_accuracy_level_modifier=7, base_pellet_hit_chance="*2", pattern_radius=0.2),
        BallisticData(range_hexes=20, penetration=1.2, damage_class=2, shotgun_accuracy_level_modifier=9, base_pellet_hit_chance="93", pattern_radius=0.2),
        BallisticData(range_hexes=30, penetration=1.1, damage_class=2, shotgun_accuracy_level_modifier=12, base_pellet_hit_chance="42", pattern_radius=0.3),
        BallisticData(range_hexes=40, penetration=0.9, damage_class=2, shotgun_accuracy_level_modifier=14, base_pellet_hit_chance="23", pattern_radius=0.4),
        BallisticData(range_hexes=80, penetration=0.5, damage_class=1, shotgun_accuracy_level_modifier=19, base_pellet_hit_chance="5", pattern_radius=0.9)
    ]
)

ammo_12g_atchisson_slug = AmmoType(
    name="12 Gauge Slug (Atchisson Assault 12)", description="Slug",
    weight=4.6,
    ballistic_data=[
        BallisticData(range_hexes=1, penetration=7.0, damage_class=10),
        BallisticData(range_hexes=2, penetration=7.0, damage_class=10),
        BallisticData(range_hexes=4, penetration=6.9, damage_class=10),
        BallisticData(range_hexes=6, penetration=6.9, damage_class=10),
        BallisticData(range_hexes=8, penetration=6.8, damage_class=10),
        BallisticData(range_hexes=10, penetration=6.7, damage_class=10),
        BallisticData(range_hexes=15, penetration=6.6, damage_class=9),
        BallisticData(range_hexes=20, penetration=6.5, damage_class=9),
        BallisticData(range_hexes=30, penetration=6.3, damage_class=9),
        BallisticData(range_hexes=40, penetration=6.0, damage_class=9),
        BallisticData(range_hexes=80, penetration=5.2, damage_class=8)
    ]
)

ammo_12g_atchisson_shot = AmmoType(
    name="12 Gauge Shot (00) (Atchisson Assault 12)", description="Shot", pellet_count=12,
    weight=4.6,
    ballistic_data=[
        BallisticData(range_hexes=1, penetration=5.4, damage_class=8, shotgun_accuracy_level_modifier=-13, base_pellet_hit_chance=None, pattern_radius=0.0),
        BallisticData(range_hexes=2, penetration=1.6, damage_class=3, shotgun_accuracy_level_modifier=-8, base_pellet_hit_chance="*11", pattern_radius=0.0),
        BallisticData(range_hexes=4, penetration=1.5, damage_class=3, shotgun_accuracy_level_modifier=-3, base_pellet_hit_chance="*10", pattern_radius=0.0),
        BallisticData(range_hexes=6, penetration=1.5, damage_class=2, shotgun_accuracy_level_modifier=0, base_pellet_hit_chance="*9", pattern_radius=0.1),
        BallisticData(range_hexes=8, penetration=1.4, damage_class=2, shotgun_accuracy_level_modifier=2, base_pellet_hit_chance="*5", pattern_radius=0.1),
        BallisticData(range_hexes=10, penetration=1.4, damage_class=2, shotgun_accuracy_level_modifier=4, base_pellet_hit_chance="*3", pattern_radius=0.1),
        BallisticData(range_hexes=15, penetration=1.3, damage_class=2, shotgun_accuracy_level_modifier=7, base_pellet_hit_chance="*2", pattern_radius=0.2),
        BallisticData(range_hexes=20, penetration=1.2, damage_class=2, shotgun_accuracy_level_modifier=9, base_pellet_hit_chance="93", pattern_radius=0.2),
        BallisticData(range_hexes=30, penetration=1.1, damage_class=2, shotgun_accuracy_level_modifier=12, base_pellet_hit_chance="42", pattern_radius=0.3),
        BallisticData(range_hexes=40, penetration=0.9, damage_class=2, shotgun_accuracy_level_modifier=14, base_pellet_hit_chance="23", pattern_radius=0.4),
        BallisticData(range_hexes=80, penetration=0.5, damage_class=1, shotgun_accuracy_level_modifier=19, base_pellet_hit_chance="5", pattern_radius=0.9)
    ]
)

ammo_40mm_heat_standard = AmmoType(
    name="40×46mm HEAT",
    description="HEAT",
    weight=0.51,
    ballistic_data=[
        BallisticData(range_hexes=40, penetration=288, damage_class=10),
        BallisticData(range_hexes=100, penetration=288, damage_class=10),
        BallisticData(range_hexes=200, penetration=288, damage_class=10),
    ],
    explosive_data=[
        ExplosiveData(range_hexes=0, shrapnel_penetration=1.6, shrapnel_damage_class=1, base_shrapnel_hit_chance="*2", base_concussion=241),
        ExplosiveData(range_hexes=1, shrapnel_penetration=1.4, shrapnel_damage_class=1, base_shrapnel_hit_chance="47", base_concussion=71),
        ExplosiveData(range_hexes=2, shrapnel_penetration=1.0, shrapnel_damage_class=1, base_shrapnel_hit_chance="11", base_concussion=23),
        ExplosiveData(range_hexes=3, shrapnel_penetration=0.7, shrapnel_damage_class=1, base_shrapnel_hit_chance="4", base_concussion=12),
        ExplosiveData(range_hexes=5, shrapnel_penetration=0.4, shrapnel_damage_class=1, base_shrapnel_hit_chance="1", base_concussion=5),
        ExplosiveData(range_hexes=10, shrapnel_penetration=0.0, shrapnel_damage_class=1, base_shrapnel_hit_chance="0", base_concussion=1),
    ],
)

ammo_40mm_he_hk = AmmoType(
    name="40×46mm HE (H&K)",
    description="HE",
    weight=0.51,
    ballistic_data=[
        BallisticData(range_hexes=40, penetration=2.0, damage_class=10),
        BallisticData(range_hexes=100, penetration=2.0, damage_class=10),
        BallisticData(range_hexes=200, penetration=2.0, damage_class=10),
    ],
    explosive_data=[
        ExplosiveData(range_hexes=0, shrapnel_penetration=1.4, shrapnel_damage_class=1, base_shrapnel_hit_chance="*3", base_concussion=250),
        ExplosiveData(range_hexes=1, shrapnel_penetration=1.2, shrapnel_damage_class=1, base_shrapnel_hit_chance="73", base_concussion=74),
        ExplosiveData(range_hexes=2, shrapnel_penetration=0.8, shrapnel_damage_class=1, base_shrapnel_hit_chance="17", base_concussion=23),
        ExplosiveData(range_hexes=3, shrapnel_penetration=0.6, shrapnel_damage_class=1, base_shrapnel_hit_chance="7", base_concussion=12),
        ExplosiveData(range_hexes=5, shrapnel_penetration=0.3, shrapnel_damage_class=1, base_shrapnel_hit_chance="2", base_concussion=5),
        ExplosiveData(range_hexes=10, shrapnel_penetration=0.0, shrapnel_damage_class=1, base_shrapnel_hit_chance="0", base_concussion=1),
    ],
)

ammo_40mm_he_armscor = AmmoType(
    name="40×46mm HE (Armscor)",
    description="HE",
    weight=0.51,
    ballistic_data=[
        BallisticData(range_hexes=40, penetration=2.0, damage_class=10),
        BallisticData(range_hexes=100, penetration=2.0, damage_class=10),
        BallisticData(range_hexes=200, penetration=2.0, damage_class=10),
    ],
    explosive_data=[
        ExplosiveData(range_hexes=0, shrapnel_penetration=1.6, shrapnel_damage_class=1, base_shrapnel_hit_chance="*3", base_concussion=273),
        ExplosiveData(range_hexes=1, shrapnel_penetration=1.4, shrapnel_damage_class=1, base_shrapnel_hit_chance="62", base_concussion=80),
        ExplosiveData(range_hexes=2, shrapnel_penetration=1.0, shrapnel_damage_class=1, base_shrapnel_hit_chance="15", base_concussion=25),
        ExplosiveData(range_hexes=3, shrapnel_penetration=0.7, shrapnel_damage_class=1, base_shrapnel_hit_chance="6", base_concussion=13),
        ExplosiveData(range_hexes=5, shrapnel_penetration=0.4, shrapnel_damage_class=1, base_shrapnel_hit_chance="2", base_concussion=6),
        ExplosiveData(range_hexes=10, shrapnel_penetration=0.0, shrapnel_damage_class=1, base_shrapnel_hit_chance="0", base_concussion=1),
    ],
)

ammo_30mm_he_ak = AmmoType(
    name="30mm HE (VOG-17/VOG-25)",
    description="HE",
    weight=0.56,
    ballistic_data=[
        BallisticData(range_hexes=40, penetration=2.5, damage_class=10),
        BallisticData(range_hexes=100, penetration=2.5, damage_class=10),
        BallisticData(range_hexes=200, penetration=2.5, damage_class=10),
    ],
    explosive_data=[
        ExplosiveData(range_hexes=0, shrapnel_penetration=2.4, shrapnel_damage_class=2, base_shrapnel_hit_chance="*2", base_concussion=250),
        ExplosiveData(range_hexes=1, shrapnel_penetration=2.2, shrapnel_damage_class=2, base_shrapnel_hit_chance="58", base_concussion=74),
        ExplosiveData(range_hexes=2, shrapnel_penetration=1.8, shrapnel_damage_class=2, base_shrapnel_hit_chance="14", base_concussion=23),
        ExplosiveData(range_hexes=3, shrapnel_penetration=1.5, shrapnel_damage_class=2, base_shrapnel_hit_chance="6", base_concussion=12),
        ExplosiveData(range_hexes=5, shrapnel_penetration=1.0, shrapnel_damage_class=1, base_shrapnel_hit_chance="1", base_concussion=5),
        ExplosiveData(range_hexes=10, shrapnel_penetration=0.4, shrapnel_damage_class=1, base_shrapnel_hit_chance="-2", base_concussion=1),
    ],
)

ammo_30mm_he_ags = AmmoType(
    name="30mm HE (VOG-17/VOG-25)",
    description="HE",
    weight=24.0,
    ballistic_data=[
        BallisticData(range_hexes=40, penetration=2.5, damage_class=10),
        BallisticData(range_hexes=100, penetration=2.5, damage_class=10),
        BallisticData(range_hexes=200, penetration=2.5, damage_class=10),
        BallisticData(range_hexes=400, penetration=2.5, damage_class=10),
    ],
    explosive_data=[
        ExplosiveData(range_hexes=0, shrapnel_penetration=2.4, shrapnel_damage_class=2, base_shrapnel_hit_chance="*2", base_concussion=250),
        ExplosiveData(range_hexes=1, shrapnel_penetration=2.2, shrapnel_damage_class=2, base_shrapnel_hit_chance="58", base_concussion=74),
        ExplosiveData(range_hexes=2, shrapnel_penetration=1.8, shrapnel_damage_class=2, base_shrapnel_hit_chance="14", base_concussion=23),
        ExplosiveData(range_hexes=3, shrapnel_penetration=1.5, shrapnel_damage_class=2, base_shrapnel_hit_chance="6", base_concussion=12),
        ExplosiveData(range_hexes=5, shrapnel_penetration=1.0, shrapnel_damage_class=1, base_shrapnel_hit_chance="1", base_concussion=5),
        ExplosiveData(range_hexes=10, shrapnel_penetration=0.4, shrapnel_damage_class=1, base_shrapnel_hit_chance="-2", base_concussion=1),
    ],
)

ammo_40mm_heat_hv = AmmoType(
    name="40×53mm HEAT",
    description="HEAT",
    weight=45.2,
    ballistic_data=[
        BallisticData(range_hexes=40, penetration=288, damage_class=10),
        BallisticData(range_hexes=100, penetration=288, damage_class=10),
        BallisticData(range_hexes=200, penetration=288, damage_class=10),
        BallisticData(range_hexes=400, penetration=288, damage_class=10),
    ],
    explosive_data=[
        ExplosiveData(range_hexes=0, shrapnel_penetration=1.6, shrapnel_damage_class=1, base_shrapnel_hit_chance="*2", base_concussion=241),
        ExplosiveData(range_hexes=1, shrapnel_penetration=1.4, shrapnel_damage_class=1, base_shrapnel_hit_chance="47", base_concussion=71),
        ExplosiveData(range_hexes=2, shrapnel_penetration=1.0, shrapnel_damage_class=1, base_shrapnel_hit_chance="11", base_concussion=23),
        ExplosiveData(range_hexes=3, shrapnel_penetration=0.7, shrapnel_damage_class=1, base_shrapnel_hit_chance="4", base_concussion=12),
        ExplosiveData(range_hexes=5, shrapnel_penetration=0.4, shrapnel_damage_class=1, base_shrapnel_hit_chance="1", base_concussion=5),
        ExplosiveData(range_hexes=10, shrapnel_penetration=0.0, shrapnel_damage_class=1, base_shrapnel_hit_chance="0", base_concussion=1),
    ],
)

ammo_40mm_he_hv = AmmoType(
    name="40×53mm HE",
    description="HE",
    weight=45.2,
    ballistic_data=[
        BallisticData(range_hexes=40, penetration=2.6, damage_class=10),
        BallisticData(range_hexes=100, penetration=2.6, damage_class=10),
        BallisticData(range_hexes=200, penetration=2.6, damage_class=10),
        BallisticData(range_hexes=400, penetration=2.6, damage_class=10),
    ],
    explosive_data=[
        ExplosiveData(range_hexes=0, shrapnel_penetration=2.5, shrapnel_damage_class=3, base_shrapnel_hit_chance="6", base_concussion=353),
        ExplosiveData(range_hexes=1, shrapnel_penetration=2.4, shrapnel_damage_class=3, base_shrapnel_hit_chance="1", base_concussion=100),
        ExplosiveData(range_hexes=2, shrapnel_penetration=2.2, shrapnel_damage_class=3, base_shrapnel_hit_chance="-3", base_concussion=31),
        ExplosiveData(range_hexes=3, shrapnel_penetration=2.0, shrapnel_damage_class=3, base_shrapnel_hit_chance="-6", base_concussion=16),
        ExplosiveData(range_hexes=5, shrapnel_penetration=1.6, shrapnel_damage_class=2, base_shrapnel_hit_chance="-9", base_concussion=7),
        ExplosiveData(range_hexes=10, shrapnel_penetration=1.0, shrapnel_damage_class=1, base_shrapnel_hit_chance="-15", base_concussion=2),
    ],
)

ammo_40mm_heat = AmmoType(
    name="40×46mm HEAT",
    description="HEAT",
    weight=0.51,
    ballistic_data=[
        BallisticData(range_hexes=40, penetration=288, damage_class=10),
        BallisticData(range_hexes=100, penetration=288, damage_class=10),
        BallisticData(range_hexes=200, penetration=288, damage_class=10),
    ],
    explosive_data=[
        ExplosiveData(range_hexes=0, shrapnel_penetration=1.6, shrapnel_damage_class=1, base_shrapnel_hit_chance="*2", base_concussion=241),
        ExplosiveData(range_hexes=1, shrapnel_penetration=1.4, shrapnel_damage_class=1, base_shrapnel_hit_chance="47", base_concussion=71),
        ExplosiveData(range_hexes=2, shrapnel_penetration=1.0, shrapnel_damage_class=1, base_shrapnel_hit_chance="11", base_concussion=23),
        ExplosiveData(range_hexes=3, shrapnel_penetration=0.7, shrapnel_damage_class=1, base_shrapnel_hit_chance="4", base_concussion=12),
        ExplosiveData(range_hexes=5, shrapnel_penetration=0.4, shrapnel_damage_class=1, base_shrapnel_hit_chance="1", base_concussion=5),
        ExplosiveData(range_hexes=10, shrapnel_penetration=0.0, shrapnel_damage_class=1, base_shrapnel_hit_chance="0", base_concussion=1),

    ],
)

ammo_40mm_he = AmmoType(
    name="40×46mm HE",
    description="HE",
    weight=0.51,
    ballistic_data=[
        BallisticData(range_hexes=40, penetration=2.1, damage_class=10),
        BallisticData(range_hexes=100, penetration=2.1, damage_class=10),
        BallisticData(range_hexes=200, penetration=2.1, damage_class=10),
    ],
    explosive_data=[
        ExplosiveData(range_hexes=0, shrapnel_penetration=1.6, shrapnel_damage_class=1, base_shrapnel_hit_chance="*3", base_concussion=273),
        ExplosiveData(range_hexes=1, shrapnel_penetration=1.4, shrapnel_damage_class=1, base_shrapnel_hit_chance="62", base_concussion=80),
        ExplosiveData(range_hexes=2, shrapnel_penetration=1.0, shrapnel_damage_class=1, base_shrapnel_hit_chance="15", base_concussion=25),
        ExplosiveData(range_hexes=3, shrapnel_penetration=0.7, shrapnel_damage_class=1, base_shrapnel_hit_chance="6", base_concussion=13),
        ExplosiveData(range_hexes=5, shrapnel_penetration=0.4, shrapnel_damage_class=1, base_shrapnel_hit_chance="2", base_concussion=6),
        ExplosiveData(range_hexes=10, shrapnel_penetration=0.0, shrapnel_damage_class=1, base_shrapnel_hit_chance="0", base_concussion=1),
    ],
)

ammo_66mm_heat_pzf44 = AmmoType(
    name="66mm HEAT (PZF 44)",
    description="HEAT",
    weight=5.5,
    ballistic_data=[
        BallisticData(range_hexes=r, penetration=8900, damage_class=10)
        for r in [40, 100, 200, 400]
    ],
    explosive_data=[
        ExplosiveData(range_hexes=0, shrapnel_penetration=5.2, shrapnel_damage_class=7, base_shrapnel_hit_chance="15", base_concussion=1100),
        ExplosiveData(range_hexes=1, shrapnel_penetration=5.1, shrapnel_damage_class=7, base_shrapnel_hit_chance="3", base_concussion=252),
        ExplosiveData(range_hexes=2, shrapnel_penetration=4.8, shrapnel_damage_class=7, base_shrapnel_hit_chance="0", base_concussion=72),
        ExplosiveData(range_hexes=3, shrapnel_penetration=4.6, shrapnel_damage_class=7, base_shrapnel_hit_chance="0", base_concussion=36),
        ExplosiveData(range_hexes=5, shrapnel_penetration=4.2, shrapnel_damage_class=6, base_shrapnel_hit_chance="0", base_concussion=16),
        ExplosiveData(range_hexes=10, shrapnel_penetration=3.4, shrapnel_damage_class=6, base_shrapnel_hit_chance="0", base_concussion=5),
    ],
)

ammo_66mm_he_pzf44 = AmmoType(
    name="66mm HE (PZF 44)",
    description="HE",
    weight=5.5,
    ballistic_data=[
        BallisticData(range_hexes=r, penetration=6.1, damage_class=10)
        for r in [40, 100, 200, 400]
    ],
    explosive_data=[
        ExplosiveData(range_hexes=0, shrapnel_penetration=6.0, shrapnel_damage_class=7, base_shrapnel_hit_chance="15", base_concussion=1300),
        ExplosiveData(range_hexes=1, shrapnel_penetration=5.9, shrapnel_damage_class=7, base_shrapnel_hit_chance="3", base_concussion=287),
        ExplosiveData(range_hexes=2, shrapnel_penetration=5.6, shrapnel_damage_class=7, base_shrapnel_hit_chance="0", base_concussion=81),
        ExplosiveData(range_hexes=3, shrapnel_penetration=5.4, shrapnel_damage_class=7, base_shrapnel_hit_chance="0", base_concussion=40),
        ExplosiveData(range_hexes=5, shrapnel_penetration=4.9, shrapnel_damage_class=7, base_shrapnel_hit_chance="0", base_concussion=17),
        ExplosiveData(range_hexes=10, shrapnel_penetration=3.9, shrapnel_damage_class=6, base_shrapnel_hit_chance="0", base_concussion=6),
    ],
)


ammo_67mm_heat_armbrust = AmmoType(
    name="67mm HEAT (Armbrust)",
    description="HEAT",
    weight=16.0,
    ballistic_data=[
        BallisticData(range_hexes=r, penetration=6600, damage_class=10)
        for r in [40, 100, 200, 400]
    ],
    explosive_data=[
        ExplosiveData(range_hexes=0, shrapnel_penetration=5.2, shrapnel_damage_class=7, base_shrapnel_hit_chance="15", base_concussion=1100),
        ExplosiveData(range_hexes=1, shrapnel_penetration=5.1, shrapnel_damage_class=7, base_shrapnel_hit_chance="3", base_concussion=252),
        ExplosiveData(range_hexes=2, shrapnel_penetration=4.8, shrapnel_damage_class=7, base_shrapnel_hit_chance="0", base_concussion=72),
        ExplosiveData(range_hexes=3, shrapnel_penetration=4.6, shrapnel_damage_class=7, base_shrapnel_hit_chance="0", base_concussion=36),
        ExplosiveData(range_hexes=5, shrapnel_penetration=4.2, shrapnel_damage_class=6, base_shrapnel_hit_chance="0", base_concussion=16),
        ExplosiveData(range_hexes=10, shrapnel_penetration=3.4, shrapnel_damage_class=6, base_shrapnel_hit_chance="0", base_concussion=5),
    ],
)

ammo_67mm_he_armbrust = AmmoType(
    name="67mm HE (Armbrust)",
    description="HE",
    weight=16.0,
    ballistic_data=[
        BallisticData(range_hexes=r, penetration=4.2, damage_class=10)
        for r in [40, 100, 200, 400]
    ],
    explosive_data=[
        ExplosiveData(range_hexes=0, shrapnel_penetration=1.4, shrapnel_damage_class=1, base_shrapnel_hit_chance="*6", base_concussion=1100),
        ExplosiveData(range_hexes=1, shrapnel_penetration=1.2, shrapnel_damage_class=1, base_shrapnel_hit_chance="*2", base_concussion=252),
        ExplosiveData(range_hexes=2, shrapnel_penetration=0.8, shrapnel_damage_class=1, base_shrapnel_hit_chance="38", base_concussion=72),
        ExplosiveData(range_hexes=3, shrapnel_penetration=0.6, shrapnel_damage_class=1, base_shrapnel_hit_chance="16", base_concussion=36),
        ExplosiveData(range_hexes=5, shrapnel_penetration=0.3, shrapnel_damage_class=1, base_shrapnel_hit_chance="5", base_concussion=16),
        ExplosiveData(range_hexes=10, shrapnel_penetration=0.0, shrapnel_damage_class=1, base_shrapnel_hit_chance="0", base_concussion=5),
    ],
)

ammo_64mm_heat_rpg18 = AmmoType(
    name="64mm HEAT (RPG 18)",
    description="HEAT",
    weight=16.0,
    ballistic_data=[
        BallisticData(range_hexes=r, penetration=5900, damage_class=10)
        for r in [40, 100, 200, 400]
    ],
    explosive_data=[
        ExplosiveData(range_hexes=0, shrapnel_penetration=4.8, shrapnel_damage_class=7, base_shrapnel_hit_chance="15", base_concussion=1000),
        ExplosiveData(range_hexes=1, shrapnel_penetration=4.7, shrapnel_damage_class=7, base_shrapnel_hit_chance="3", base_concussion=232),
        ExplosiveData(range_hexes=2, shrapnel_penetration=4.5, shrapnel_damage_class=6, base_shrapnel_hit_chance="0", base_concussion=67),
        ExplosiveData(range_hexes=3, shrapnel_penetration=4.3, shrapnel_damage_class=6, base_shrapnel_hit_chance="0", base_concussion=34),
        ExplosiveData(range_hexes=5, shrapnel_penetration=3.9, shrapnel_damage_class=6, base_shrapnel_hit_chance="0", base_concussion=15),
        ExplosiveData(range_hexes=10, shrapnel_penetration=3.1, shrapnel_damage_class=5, base_shrapnel_hit_chance="0", base_concussion=5),
    ],
)

ammo_85mm_heat_rpg7 = AmmoType(
    name="85mm HEAT (RPG-7V)",
    description="HEAT",
    weight=5.0,
    ballistic_data=[
        BallisticData(range_hexes=r, penetration=7200, damage_class=10)
        for r in [40, 100, 200, 400]
    ],
    explosive_data=[
        ExplosiveData(range_hexes=0, shrapnel_penetration=7.2, shrapnel_damage_class=8, base_shrapnel_hit_chance="11", base_concussion=2000),
        ExplosiveData(range_hexes=1, shrapnel_penetration=7.1, shrapnel_damage_class=8, base_shrapnel_hit_chance="2", base_concussion=393),
        ExplosiveData(range_hexes=2, shrapnel_penetration=6.9, shrapnel_damage_class=8, base_shrapnel_hit_chance="0", base_concussion=105),
        ExplosiveData(range_hexes=3, shrapnel_penetration=6.7, shrapnel_damage_class=8, base_shrapnel_hit_chance="0", base_concussion=52),
        ExplosiveData(range_hexes=5, shrapnel_penetration=6.2, shrapnel_damage_class=8, base_shrapnel_hit_chance="0", base_concussion=22),
        ExplosiveData(range_hexes=10, shrapnel_penetration=5.2, shrapnel_damage_class=7, base_shrapnel_hit_chance="0", base_concussion=7),
    ],
)

ammo_85mm_he_rpg7 = AmmoType(
    name="85mm HE (RPG-7V)",
    description="HE",
    weight=5.0,
    ballistic_data=[
        BallisticData(range_hexes=r, penetration=8.2, damage_class=10)
        for r in [40, 100, 200, 400]
    ],
    explosive_data=[
        ExplosiveData(range_hexes=0, shrapnel_penetration=8.1, shrapnel_damage_class=9, base_shrapnel_hit_chance="11", base_concussion=2400),
        ExplosiveData(range_hexes=1, shrapnel_penetration=8.0, shrapnel_damage_class=9, base_shrapnel_hit_chance="2", base_concussion=441),
        ExplosiveData(range_hexes=2, shrapnel_penetration=7.7, shrapnel_damage_class=9, base_shrapnel_hit_chance="0", base_concussion=115),
        ExplosiveData(range_hexes=3, shrapnel_penetration=7.5, shrapnel_damage_class=8, base_shrapnel_hit_chance="0", base_concussion=57),
        ExplosiveData(range_hexes=5, shrapnel_penetration=7.0, shrapnel_damage_class=8, base_shrapnel_hit_chance="0", base_concussion=24),
        ExplosiveData(range_hexes=10, shrapnel_penetration=5.9, shrapnel_damage_class=8, base_shrapnel_hit_chance="0", base_concussion=8),
    ],
)

ammo_94mm_heat_law80 = AmmoType(
    name="94mm HEAT (LAW 80)",
    description="HEAT",
    weight=21.2,
    ballistic_data=[
        BallisticData(range_hexes=r, penetration=17000, damage_class=10)
        for r in [40, 100, 200, 400]
    ],
    explosive_data=[
        ExplosiveData(range_hexes=0, shrapnel_penetration=8.3, shrapnel_damage_class=9, base_shrapnel_hit_chance="10", base_concussion=2600),
        ExplosiveData(range_hexes=1, shrapnel_penetration=8.2, shrapnel_damage_class=9, base_shrapnel_hit_chance="2", base_concussion=480),
        ExplosiveData(range_hexes=2, shrapnel_penetration=8.0, shrapnel_damage_class=9, base_shrapnel_hit_chance="0", base_concussion=123),
        ExplosiveData(range_hexes=3, shrapnel_penetration=7.7, shrapnel_damage_class=9, base_shrapnel_hit_chance="0", base_concussion=60),
        ExplosiveData(range_hexes=5, shrapnel_penetration=7.3, shrapnel_damage_class=9, base_shrapnel_hit_chance="0", base_concussion=26),
        ExplosiveData(range_hexes=10, shrapnel_penetration=6.2, shrapnel_damage_class=8, base_shrapnel_hit_chance="0", base_concussion=9),
    ],
)

ammo_66mm_heat_m72 = AmmoType(
    name="66mm HEAT (M72 A2)",
    description="HEAT",
    weight=5.2,
    ballistic_data=[
        BallisticData(range_hexes=r, penetration=6800, damage_class=10)
        for r in [40, 100, 200, 400]
    ],
    explosive_data=[
        ExplosiveData(range_hexes=0, shrapnel_penetration=5.0, shrapnel_damage_class=7, base_shrapnel_hit_chance="15", base_concussion=1100),
        ExplosiveData(range_hexes=1, shrapnel_penetration=4.9, shrapnel_damage_class=7, base_shrapnel_hit_chance="3", base_concussion=245),
        ExplosiveData(range_hexes=2, shrapnel_penetration=4.7, shrapnel_damage_class=7, base_shrapnel_hit_chance="0", base_concussion=70),
        ExplosiveData(range_hexes=3, shrapnel_penetration=4.5, shrapnel_damage_class=7, base_shrapnel_hit_chance="0", base_concussion=36),
        ExplosiveData(range_hexes=5, shrapnel_penetration=4.1, shrapnel_damage_class=6, base_shrapnel_hit_chance="0", base_concussion=15),
        ExplosiveData(range_hexes=10, shrapnel_penetration=3.3, shrapnel_damage_class=5, base_shrapnel_hit_chance="0", base_concussion=5),
    ],
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

pistol_9mm_v2_ballistic = WeaponBallisticData(
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=45),
        RangeData(range_hexes=20, value=37),
        RangeData(range_hexes=40, value=28),
        RangeData(range_hexes=70, value=21),
        RangeData(range_hexes=100, value=16),
        RangeData(range_hexes=200, value=6),
        RangeData(range_hexes=300, value=1),
        RangeData(range_hexes=400, value=-2),
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=1),
        RangeData(range_hexes=20, value=1),
        RangeData(range_hexes=40, value=2),
        RangeData(range_hexes=70, value=4),
        RangeData(range_hexes=100, value=6),
        RangeData(range_hexes=200, value=15),
        RangeData(range_hexes=300, value=25),
        RangeData(range_hexes=400, value=36),
    ]
)

vp70m_ballistic = WeaponBallisticData(
    three_round_burst=[
        RangeData(range_hexes=10, value=-10),
        RangeData(range_hexes=20, value=-5),
        RangeData(range_hexes=40, value=0),
        RangeData(range_hexes=70, value=4),
        RangeData(range_hexes=100, value=7),
        RangeData(range_hexes=200, value=12),
        RangeData(range_hexes=300, value=15),
        RangeData(range_hexes=400, value=17)
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=45),
        RangeData(range_hexes=20, value=37),
        RangeData(range_hexes=40, value=28),
        RangeData(range_hexes=70, value=21),
        RangeData(range_hexes=100, value=16),
        RangeData(range_hexes=200, value=6),
        RangeData(range_hexes=300, value=1),
        RangeData(range_hexes=400, value=-2)
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=1),
        RangeData(range_hexes=20, value=1),
        RangeData(range_hexes=40, value=2),
        RangeData(range_hexes=70, value=4),
        RangeData(range_hexes=100, value=6),
        RangeData(range_hexes=200, value=14),
        RangeData(range_hexes=300, value=24),
        RangeData(range_hexes=400, value=35)
    ]
)

m93r_ballistic = WeaponBallisticData(
    three_round_burst=[
        RangeData(10, -2), RangeData(20, 3), RangeData(40, 8), RangeData(70, 12),
        RangeData(100, 15), RangeData(200, 20), RangeData(300, 22), RangeData(400, 24)
    ],
    ballistic_accuracy=[
        RangeData(10, 46), RangeData(20, 37), RangeData(40, 28), RangeData(70, 21),
        RangeData(100, 16), RangeData(200, 6), RangeData(300, 1), RangeData(400, -2)
    ],
    time_of_flight=[
        RangeData(10, 0), RangeData(20, 1), RangeData(40, 2), RangeData(70, 4),
        RangeData(100, 6), RangeData(200, 14), RangeData(300, 23), RangeData(400, 33)
    ]
)

makarov_ballistic = WeaponBallisticData(
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=41),
        RangeData(range_hexes=20, value=32),
        RangeData(range_hexes=40, value=23),
        RangeData(range_hexes=70, value=15),
        RangeData(range_hexes=100, value=10),
        RangeData(range_hexes=200, value=1),
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=1),
        RangeData(range_hexes=20, value=1),
        RangeData(range_hexes=40, value=3),
        RangeData(range_hexes=70, value=5),
        RangeData(range_hexes=100, value=7),
        RangeData(range_hexes=200, value=18),
    ]
)

psm_ballistic = WeaponBallisticData(
    ballistic_accuracy=[
        RangeData(range_hexes=10,  value=48),
        RangeData(range_hexes=20,  value=41),
        RangeData(range_hexes=40,  value=33),
        RangeData(range_hexes=70,  value=26),
        RangeData(range_hexes=100, value=21),
    ],
    time_of_flight=[
        RangeData(range_hexes=10,  value=1),
        RangeData(range_hexes=20,  value=1),
        RangeData(range_hexes=40,  value=3),
        RangeData(range_hexes=70,  value=5),
        RangeData(range_hexes=100, value=7),
    ]
)

sw_m469_ballistic = WeaponBallisticData(
    ballistic_accuracy=[
        RangeData(range_hexes=10,  value=45),
        RangeData(range_hexes=20,  value=37),
        RangeData(range_hexes=40,  value=28),
        RangeData(range_hexes=70,  value=21),
        RangeData(range_hexes=100, value=16),
        RangeData(range_hexes=200, value=6),
        RangeData(range_hexes=300, value=1),
        RangeData(range_hexes=400, value=-2),
    ],
    time_of_flight=[
        RangeData(range_hexes=10,  value=1),
        RangeData(range_hexes=20,  value=1),
        RangeData(range_hexes=40,  value=2),
        RangeData(range_hexes=70,  value=4),
        RangeData(range_hexes=100, value=6),
        RangeData(range_hexes=200, value=14),
        RangeData(range_hexes=300, value=24),
        RangeData(range_hexes=400, value=35),
    ]
)

m92f_ballistic = WeaponBallisticData(
    ballistic_accuracy=[
        RangeData(range_hexes=10,  value=46),
        RangeData(range_hexes=20,  value=37),
        RangeData(range_hexes=40,  value=28),
        RangeData(range_hexes=70,  value=21),
        RangeData(range_hexes=100, value=16),
        RangeData(range_hexes=200, value=7),
        RangeData(range_hexes=300, value=1),
        RangeData(range_hexes=400, value=-2),
    ],
    time_of_flight=[
        RangeData(range_hexes=10,  value=0),
        RangeData(range_hexes=20,  value=1),
        RangeData(range_hexes=40,  value=2),
        RangeData(range_hexes=70,  value=4),
        RangeData(range_hexes=100, value=6),
        RangeData(range_hexes=200, value=13),
        RangeData(range_hexes=300, value=22),
        RangeData(range_hexes=400, value=32),
    ]
)

m1911a1_ballistic = WeaponBallisticData(
    ballistic_accuracy=[
        RangeData(range_hexes=10,  value=45),
        RangeData(range_hexes=20,  value=36),
        RangeData(range_hexes=40,  value=27),
        RangeData(range_hexes=70,  value=20),
        RangeData(range_hexes=100, value=15),
        RangeData(range_hexes=200, value=5),
        RangeData(range_hexes=300, value=0),
        RangeData(range_hexes=400, value=-4),
    ],
    time_of_flight=[
        RangeData(range_hexes=10,  value=1),
        RangeData(range_hexes=20,  value=2),
        RangeData(range_hexes=40,  value=3),
        RangeData(range_hexes=70,  value=5),
        RangeData(range_hexes=100, value=8),
        RangeData(range_hexes=200, value=19),
        RangeData(range_hexes=300, value=31),
        RangeData(range_hexes=400, value=45),
    ]
)

m15_ballistic = WeaponBallisticData(
    ballistic_accuracy=[
        RangeData(range_hexes=10,  value=45),
        RangeData(range_hexes=20,  value=37),
        RangeData(range_hexes=40,  value=27),
        RangeData(range_hexes=70,  value=20),
        RangeData(range_hexes=100, value=15),
        RangeData(range_hexes=200, value=5),
        RangeData(range_hexes=300, value=0),
        RangeData(range_hexes=400, value=-4),
    ],
    time_of_flight=[
        RangeData(range_hexes=10,  value=1),
        RangeData(range_hexes=20,  value=2),
        RangeData(range_hexes=40,  value=3),
        RangeData(range_hexes=70,  value=5),
        RangeData(range_hexes=100, value=8),
        RangeData(range_hexes=200, value=20),
        RangeData(range_hexes=300, value=32),
        RangeData(range_hexes=400, value=47),
    ]
)

pa3_ballistic = WeaponBallisticData(
    minimum_arc=[
        RangeData(range_hexes=10,  value=0.2), RangeData(range_hexes=20,  value=0.4),
        RangeData(range_hexes=40,  value=0.9),   RangeData(range_hexes=70,  value=2),
        RangeData(range_hexes=100, value=2),   RangeData(range_hexes=200, value=4),
        RangeData(range_hexes=300, value=7),  RangeData(range_hexes=400, value=9),
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10,  value=46), RangeData(range_hexes=20,  value=37),
        RangeData(range_hexes=40,  value=28), RangeData(range_hexes=70,  value=21),
        RangeData(range_hexes=100, value=16), RangeData(range_hexes=200, value=7),
        RangeData(range_hexes=300, value=1),  RangeData(range_hexes=400, value=-2),
    ],
    time_of_flight=[
        RangeData(range_hexes=10,  value=0),  RangeData(range_hexes=20,  value=1),
        RangeData(range_hexes=40,  value=2),  RangeData(range_hexes=70,  value=4),
        RangeData(range_hexes=100, value=6),  RangeData(range_hexes=200, value=13),
        RangeData(range_hexes=300, value=21), RangeData(range_hexes=400, value=31),
    ]
)

mpi81_ballistic = WeaponBallisticData(
    minimum_arc=[
        RangeData(range_hexes=10, value=0.3), RangeData(range_hexes=20, value=0.5),
        RangeData(range_hexes=40, value=1.0), RangeData(range_hexes=70, value=2.0),
        RangeData(range_hexes=100, value=3.0), RangeData(range_hexes=200, value=5.0),
        RangeData(range_hexes=300, value=8.0), RangeData(range_hexes=400, value=11.0),
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10,  value=46), RangeData(range_hexes=20,  value=37),
        RangeData(range_hexes=40,  value=28), RangeData(range_hexes=70,  value=21),
        RangeData(range_hexes=100, value=16), RangeData(range_hexes=200, value=7),
        RangeData(range_hexes=300, value=1),  RangeData(range_hexes=400, value=-2),
    ],
    time_of_flight=[
        RangeData(range_hexes=10,  value=0),  RangeData(range_hexes=20,  value=1),
        RangeData(range_hexes=40,  value=2),  RangeData(range_hexes=70,  value=4),
        RangeData(range_hexes=100, value=6),  RangeData(range_hexes=200, value=13),
        RangeData(range_hexes=300, value=23), RangeData(range_hexes=400, value=32),
    ]
)

f1_ballistic = WeaponBallisticData(
    minimum_arc=[
        RangeData(range_hexes=10, value=0.2), RangeData(range_hexes=20, value=0.4),
        RangeData(range_hexes=40, value=0.8), RangeData(range_hexes=70, value=1),
        RangeData(range_hexes=100, value=2), RangeData(range_hexes=200, value=4),
        RangeData(range_hexes=300, value=6), RangeData(range_hexes=400, value=8),
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10,  value=46), RangeData(range_hexes=20,  value=37),
        RangeData(range_hexes=40,  value=28), RangeData(range_hexes=70,  value=21),
        RangeData(range_hexes=100, value=16), RangeData(range_hexes=200, value=6),
        RangeData(range_hexes=300, value=1),  RangeData(range_hexes=400, value=-2),
    ],
    time_of_flight=[
        RangeData(range_hexes=10,  value=1),  RangeData(range_hexes=20,  value=1),
        RangeData(range_hexes=40,  value=2),  RangeData(range_hexes=70,  value=4),
        RangeData(range_hexes=100, value=6),  RangeData(range_hexes=200, value=14),
        RangeData(range_hexes=300, value=24), RangeData(range_hexes=400, value=34),
    ]
)

m61_ballistic = WeaponBallisticData(
    minimum_arc=[
        RangeData(range_hexes=10, value=0.2), RangeData(range_hexes=20, value=0.4),
        RangeData(range_hexes=40, value=0.9), RangeData(range_hexes=70, value=1.0),
        RangeData(range_hexes=100, value=2.0), RangeData(range_hexes=200, value=4.0),
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=43), RangeData(range_hexes=20, value=35),
        RangeData(range_hexes=40, value=25), RangeData(range_hexes=70, value=18),
        RangeData(range_hexes=100, value=13), RangeData(range_hexes=200, value=4),
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=1), RangeData(range_hexes=20, value=1),
        RangeData(range_hexes=40, value=3), RangeData(range_hexes=70, value=5),
        RangeData(range_hexes=100, value=7), RangeData(range_hexes=200, value=18),
    ]
)

mat49_ballistic = WeaponBallisticData(
    minimum_arc=[
        RangeData(range_hexes=10,  value=0.2), RangeData(range_hexes=20,  value=0.4),
        RangeData(range_hexes=40,  value=0.8), RangeData(range_hexes=70,  value=1.0),
        RangeData(range_hexes=100, value=2.0), RangeData(range_hexes=200, value=4.0),
        RangeData(range_hexes=300, value=6.0), RangeData(range_hexes=400, value=8.0),
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10,  value=46), RangeData(range_hexes=20,  value=37),
        RangeData(range_hexes=40,  value=28), RangeData(range_hexes=70,  value=21),
        RangeData(range_hexes=100, value=16), RangeData(range_hexes=200, value=7),
        RangeData(range_hexes=300, value=1),  RangeData(range_hexes=400, value=-2),
    ],
    time_of_flight=[
        RangeData(range_hexes=10,  value=0),  RangeData(range_hexes=20,  value=1),
        RangeData(range_hexes=40,  value=2),  RangeData(range_hexes=70,  value=4),
        RangeData(range_hexes=100, value=6),  RangeData(range_hexes=200, value=13),
        RangeData(range_hexes=300, value=22), RangeData(range_hexes=400, value=32),
    ]
)

mp5_ballistic = WeaponBallisticData(
    minimum_arc=[
        RangeData(range_hexes=10,  value=0.4), RangeData(range_hexes=20,  value=0.7),
        RangeData(range_hexes=40,  value=1.0), RangeData(range_hexes=70,  value=2.0),
        RangeData(range_hexes=100, value=4.0), RangeData(range_hexes=200, value=7.0),
        RangeData(range_hexes=300, value=11.0), RangeData(range_hexes=400, value=14.0),
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10,  value=46), RangeData(range_hexes=20,  value=37),
        RangeData(range_hexes=40,  value=28), RangeData(range_hexes=70,  value=21),
        RangeData(range_hexes=100, value=16), RangeData(range_hexes=200, value=7),
        RangeData(range_hexes=300, value=1),  RangeData(range_hexes=400, value=-2),
    ],
    time_of_flight=[
        RangeData(range_hexes=10,  value=0),  RangeData(range_hexes=20,  value=1),
        RangeData(range_hexes=40,  value=2),  RangeData(range_hexes=70,  value=4),
        RangeData(range_hexes=100, value=6),  RangeData(range_hexes=200, value=13),
        RangeData(range_hexes=300, value=21), RangeData(range_hexes=400, value=31),
    ]
)

mp5k_ballistic = WeaponBallisticData(
    three_round_burst=[
        RangeData(range_hexes=10, value=-6),
        RangeData(range_hexes=20, value=-1),
        RangeData(range_hexes=40, value=4),
        RangeData(range_hexes=70, value=8),
        RangeData(range_hexes=100, value=11),
        RangeData(range_hexes=200, value=16),
        RangeData(range_hexes=300, value=19),
        RangeData(range_hexes=400, value=21)
    ],
    minimum_arc=[
        RangeData(range_hexes=10,  value=0.4), RangeData(range_hexes=20,  value=0.8),
        RangeData(range_hexes=40,  value=2.0), RangeData(range_hexes=70,  value=3.0),
        RangeData(range_hexes=100, value=4.0), RangeData(range_hexes=200, value=8.0),
        RangeData(range_hexes=300, value=12.0), RangeData(range_hexes=400, value=17.0),
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10,  value=46), RangeData(range_hexes=20,  value=37),
        RangeData(range_hexes=40,  value=28), RangeData(range_hexes=70,  value=21),
        RangeData(range_hexes=100, value=16), RangeData(range_hexes=200, value=6),
        RangeData(range_hexes=300, value=1),  RangeData(range_hexes=400, value=-2),
    ],
    time_of_flight=[
        RangeData(range_hexes=10,  value=0),  RangeData(range_hexes=20,  value=1),
        RangeData(range_hexes=40,  value=2),  RangeData(range_hexes=70,  value=4),
        RangeData(range_hexes=100, value=6),  RangeData(range_hexes=200, value=14),
        RangeData(range_hexes=300, value=23), RangeData(range_hexes=400, value=33),
    ]
)

hk53_ballistic = WeaponBallisticData(
    minimum_arc=[
        RangeData(range_hexes=10,  value=0.3), RangeData(range_hexes=20,  value=0.5),
        RangeData(range_hexes=40,  value=1.0), RangeData(range_hexes=70,  value=2.0),
        RangeData(range_hexes=100, value=3.0), RangeData(range_hexes=200, value=5.0),
        RangeData(range_hexes=300, value=8.0), RangeData(range_hexes=400, value=11.0),
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10,  value=61), RangeData(range_hexes=20,  value=52),
        RangeData(range_hexes=40,  value=44), RangeData(range_hexes=70,  value=36),
        RangeData(range_hexes=100, value=31), RangeData(range_hexes=200, value=22),
        RangeData(range_hexes=300, value=16), RangeData(range_hexes=400, value=12),
    ],
    time_of_flight=[
        RangeData(range_hexes=10,  value=0),  RangeData(range_hexes=20,  value=0),
        RangeData(range_hexes=40,  value=1),  RangeData(range_hexes=70,  value=2),
        RangeData(range_hexes=100, value=3),  RangeData(range_hexes=200, value=6),
        RangeData(range_hexes=300, value=10), RangeData(range_hexes=400, value=14),
    ]
)

uzi_ballistic = WeaponBallisticData(
    minimum_arc=[
        RangeData(range_hexes=10,  value=0.2), RangeData(range_hexes=20,  value=0.4),
        RangeData(range_hexes=40,  value=0.9), RangeData(range_hexes=70,  value=1.0),
        RangeData(range_hexes=100, value=2.0), RangeData(range_hexes=200, value=4.0),
        RangeData(range_hexes=300, value=6.0), RangeData(range_hexes=400, value=9.0),
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10,  value=46), RangeData(range_hexes=20,  value=37),
        RangeData(range_hexes=40,  value=28), RangeData(range_hexes=70,  value=21),
        RangeData(range_hexes=100, value=16), RangeData(range_hexes=200, value=7),
        RangeData(range_hexes=300, value=1),  RangeData(range_hexes=400, value=-2),
    ],
    time_of_flight=[
        RangeData(range_hexes=10,  value=0),  RangeData(range_hexes=20,  value=1),
        RangeData(range_hexes=40,  value=2),  RangeData(range_hexes=70,  value=4),
        RangeData(range_hexes=100, value=6),  RangeData(range_hexes=200, value=13),
        RangeData(range_hexes=300, value=21), RangeData(range_hexes=400, value=31),
    ]
)

miniuzi_ballistic = WeaponBallisticData(
    minimum_arc=[
        RangeData(range_hexes=10,  value=0.3), RangeData(range_hexes=20,  value=0.7),
        RangeData(range_hexes=40,  value=1.0), RangeData(range_hexes=70,  value=2.0),
        RangeData(range_hexes=100, value=3.0), RangeData(range_hexes=200, value=7.0),
        RangeData(range_hexes=300, value=10.0), RangeData(range_hexes=400, value=13.0),
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10,  value=45), RangeData(range_hexes=20,  value=37),
        RangeData(range_hexes=40,  value=28), RangeData(range_hexes=70,  value=21),
        RangeData(range_hexes=100, value=16), RangeData(range_hexes=200, value=6),
        RangeData(range_hexes=300, value=1),  RangeData(range_hexes=400, value=-2),
    ],
    time_of_flight=[
        RangeData(range_hexes=10,  value=1),  RangeData(range_hexes=20,  value=1),
        RangeData(range_hexes=40,  value=2),  RangeData(range_hexes=70,  value=4),
        RangeData(range_hexes=100, value=6),  RangeData(range_hexes=200, value=15),
        RangeData(range_hexes=300, value=25), RangeData(range_hexes=400, value=36),
    ]
)

m12s_ballistic = WeaponBallisticData(
    minimum_arc=[
        RangeData(range_hexes=10,  value=0.2), RangeData(range_hexes=20,  value=0.4),
        RangeData(range_hexes=40,  value=0.8), RangeData(range_hexes=70,  value=1.0),
        RangeData(range_hexes=100, value=2.0), RangeData(range_hexes=200, value=4.0),
        RangeData(range_hexes=300, value=6.0), RangeData(range_hexes=400, value=8.0),
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10,  value=46), RangeData(range_hexes=20,  value=37),
        RangeData(range_hexes=40,  value=28), RangeData(range_hexes=70,  value=21),
        RangeData(range_hexes=100, value=16), RangeData(range_hexes=200, value=7),
        RangeData(range_hexes=300, value=1),  RangeData(range_hexes=400, value=-2),
    ],
    time_of_flight=[
        RangeData(range_hexes=10,  value=0),  RangeData(range_hexes=20,  value=1),
        RangeData(range_hexes=40,  value=2),  RangeData(range_hexes=70,  value=4),
        RangeData(range_hexes=100, value=6),  RangeData(range_hexes=200, value=13),
        RangeData(range_hexes=300, value=23), RangeData(range_hexes=400, value=32),
    ]
)

spectre_ballistic = WeaponBallisticData(
    minimum_arc=[
        RangeData(range_hexes=10,  value=0.4), RangeData(range_hexes=20,  value=0.8),
        RangeData(range_hexes=40,  value=2.0), RangeData(range_hexes=70,  value=3.0),
        RangeData(range_hexes=100, value=4.0), RangeData(range_hexes=200, value=8.0),
        RangeData(range_hexes=300, value=11.0), RangeData(range_hexes=400, value=15.0),
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10,  value=46), RangeData(range_hexes=20,  value=37),
        RangeData(range_hexes=40,  value=28), RangeData(range_hexes=70,  value=21),
        RangeData(range_hexes=100, value=16), RangeData(range_hexes=200, value=7),
        RangeData(range_hexes=300, value=1),  RangeData(range_hexes=400, value=-2),
    ],
    time_of_flight=[
        RangeData(range_hexes=10,  value=0),  RangeData(range_hexes=20,  value=1),
        RangeData(range_hexes=40,  value=2),  RangeData(range_hexes=70,  value=4),
        RangeData(range_hexes=100, value=6),  RangeData(range_hexes=200, value=13),
        RangeData(range_hexes=300, value=21), RangeData(range_hexes=400, value=31),
    ]
)

bxp_ballistic = WeaponBallisticData(
    minimum_arc=[
        RangeData(range_hexes=10,  value=0.3), RangeData(range_hexes=20,  value=0.5),
        RangeData(range_hexes=40,  value=1.0), RangeData(range_hexes=70,  value=2.0),
        RangeData(range_hexes=100, value=3.0), RangeData(range_hexes=200, value=5.0),
        RangeData(range_hexes=300, value=8.0),
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10,  value=45), RangeData(range_hexes=20,  value=37),
        RangeData(range_hexes=40,  value=28), RangeData(range_hexes=70,  value=20),
        RangeData(range_hexes=100, value=15), RangeData(range_hexes=200, value=6),
        RangeData(range_hexes=300, value=1),
    ],
    time_of_flight=[
        RangeData(range_hexes=10,  value=1),  RangeData(range_hexes=20,  value=1),
        RangeData(range_hexes=40,  value=2),  RangeData(range_hexes=70,  value=5),
        RangeData(range_hexes=100, value=7),  RangeData(range_hexes=200, value=16),
        RangeData(range_hexes=300, value=27),
    ]
)

aks74u_ballistic = WeaponBallisticData(
    minimum_arc=[
        RangeData(range_hexes=10,  value=0.2), RangeData(range_hexes=20,  value=0.3),
        RangeData(range_hexes=40,  value=0.6), RangeData(range_hexes=70,  value=1.0),
        RangeData(range_hexes=100, value=2.0), RangeData(range_hexes=200, value=3.0),
        RangeData(range_hexes=300, value=5.0), RangeData(range_hexes=400, value=7.0),
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10,  value=60), RangeData(range_hexes=20,  value=52),
        RangeData(range_hexes=40,  value=43), RangeData(range_hexes=70,  value=35),
        RangeData(range_hexes=100, value=31), RangeData(range_hexes=200, value=21),
        RangeData(range_hexes=300, value=15), RangeData(range_hexes=400, value=12),
    ],
    time_of_flight=[
        RangeData(range_hexes=10,  value=0),  RangeData(range_hexes=20,  value=0),
        RangeData(range_hexes=40,  value=1),  RangeData(range_hexes=70,  value=2),
        RangeData(range_hexes=100, value=3),  RangeData(range_hexes=200, value=6),
        RangeData(range_hexes=300, value=9),  RangeData(range_hexes=400, value=13),
    ]
)

sterling_ballistic = WeaponBallisticData(
    minimum_arc=[
        RangeData(range_hexes=10,  value=0.4), RangeData(range_hexes=20,  value=0.8),
        RangeData(range_hexes=40,  value=2.0), RangeData(range_hexes=70,  value=3.0),
        RangeData(range_hexes=100, value=4.0), RangeData(range_hexes=200, value=8.0),
        RangeData(range_hexes=300, value=13.0), RangeData(range_hexes=400, value=17.0),
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10,  value=46), RangeData(range_hexes=20,  value=37),
        RangeData(range_hexes=40,  value=28), RangeData(range_hexes=70,  value=21),
        RangeData(range_hexes=100, value=16), RangeData(range_hexes=200, value=7),
        RangeData(range_hexes=300, value=1),  RangeData(range_hexes=400, value=-2),
    ],
    time_of_flight=[
        RangeData(range_hexes=10,  value=0),  RangeData(range_hexes=20,  value=1),
        RangeData(range_hexes=40,  value=2),  RangeData(range_hexes=70,  value=4),
        RangeData(range_hexes=100, value=6),  RangeData(range_hexes=200, value=13),
        RangeData(range_hexes=300, value=23), RangeData(range_hexes=400, value=32),
    ]
)

mac10_9mm_ballistic = WeaponBallisticData(
    minimum_arc=[
        RangeData(range_hexes=10,  value=0.4), RangeData(range_hexes=20,  value=0.8),
        RangeData(range_hexes=40,  value=2.0), RangeData(range_hexes=70,  value=3.0),
        RangeData(range_hexes=100, value=4.0), RangeData(range_hexes=200, value=8.0),
        RangeData(range_hexes=300, value=12.0), RangeData(range_hexes=400, value=15.0),
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10,  value=46), RangeData(range_hexes=20,  value=37),
        RangeData(range_hexes=40,  value=28), RangeData(range_hexes=70,  value=21),
        RangeData(range_hexes=100, value=16), RangeData(range_hexes=200, value=6),
        RangeData(range_hexes=300, value=1),  RangeData(range_hexes=400, value=-2),
    ],
    time_of_flight=[
        RangeData(range_hexes=10,  value=1),  RangeData(range_hexes=20,  value=1),
        RangeData(range_hexes=40,  value=2),  RangeData(range_hexes=70,  value=4),
        RangeData(range_hexes=100, value=6),  RangeData(range_hexes=200, value=14),
        RangeData(range_hexes=300, value=24), RangeData(range_hexes=400, value=34),
    ]
)

mac10_45_ballistic = WeaponBallisticData(
    minimum_arc=[
        RangeData(range_hexes=10,  value=0.6), RangeData(range_hexes=20,  value=1.0),
        RangeData(range_hexes=40,  value=2.0), RangeData(range_hexes=70,  value=4.0),
        RangeData(range_hexes=100, value=6.0), RangeData(range_hexes=200, value=12.0),
        RangeData(range_hexes=300, value=19.0), RangeData(range_hexes=400, value=25.0),
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10,  value=45), RangeData(range_hexes=20,  value=37),
        RangeData(range_hexes=40,  value=28), RangeData(range_hexes=70,  value=21),
        RangeData(range_hexes=100, value=16), RangeData(range_hexes=200, value=6),
        RangeData(range_hexes=300, value=1),  RangeData(range_hexes=400, value=-3),
    ],
    time_of_flight=[
        RangeData(range_hexes=10,  value=1),  RangeData(range_hexes=20,  value=1),
        RangeData(range_hexes=40,  value=3),  RangeData(range_hexes=70,  value=5),
        RangeData(range_hexes=100, value=8),  RangeData(range_hexes=200, value=18),
        RangeData(range_hexes=300, value=30), RangeData(range_hexes=400, value=43),
    ]
)

bushmaster_ballistic = WeaponBallisticData(
    minimum_arc=[
        RangeData(range_hexes=10,  value=0.3), RangeData(range_hexes=20,  value=0.7),
        RangeData(range_hexes=40,  value=1.0), RangeData(range_hexes=70,  value=2.0),
        RangeData(range_hexes=100, value=3.0), RangeData(range_hexes=200, value=7.0),
        RangeData(range_hexes=300, value=10.0), RangeData(range_hexes=400, value=13.0),
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10,  value=60), RangeData(range_hexes=20,  value=51),
        RangeData(range_hexes=40,  value=42), RangeData(range_hexes=70,  value=35),
        RangeData(range_hexes=100, value=30), RangeData(range_hexes=200, value=20),
        RangeData(range_hexes=300, value=15), RangeData(range_hexes=400, value=11),
    ],
    time_of_flight=[
        RangeData(range_hexes=10,  value=0),  RangeData(range_hexes=20,  value=0),
        RangeData(range_hexes=40,  value=1),  RangeData(range_hexes=70,  value=2),
        RangeData(range_hexes=100, value=2),  RangeData(range_hexes=200, value=5),
        RangeData(range_hexes=300, value=8),  RangeData(range_hexes=400, value=12),
    ]
)

aug_ballistic = WeaponBallisticData(
    minimum_arc=[
        RangeData(range_hexes=10, value=0.2),
        RangeData(range_hexes=20, value=0.5),
        RangeData(range_hexes=40, value=1.0),
        RangeData(range_hexes=70, value=2.0),
        RangeData(range_hexes=100, value=2.0),
        RangeData(range_hexes=200, value=5.0),
        RangeData(range_hexes=300, value=7.0),
        RangeData(range_hexes=400, value=10.0)
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=60),
        RangeData(range_hexes=20, value=51),
        RangeData(range_hexes=40, value=42),
        RangeData(range_hexes=70, value=35),
        RangeData(range_hexes=100, value=30),
        RangeData(range_hexes=200, value=20),
        RangeData(range_hexes=300, value=15),
        RangeData(range_hexes=400, value=11)
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=0),
        RangeData(range_hexes=20, value=0),
        RangeData(range_hexes=40, value=1),
        RangeData(range_hexes=70, value=1),
        RangeData(range_hexes=100, value=2),
        RangeData(range_hexes=200, value=5),
        RangeData(range_hexes=300, value=8),
        RangeData(range_hexes=400, value=11)
    ]
)

l1a1_ballistic = WeaponBallisticData(
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=61),
        RangeData(range_hexes=20, value=53),
        RangeData(range_hexes=40, value=45),
        RangeData(range_hexes=70, value=37),
        RangeData(range_hexes=100, value=32),
        RangeData(range_hexes=200, value=23),
        RangeData(range_hexes=300, value=17),
        RangeData(range_hexes=400, value=13)
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=0),
        RangeData(range_hexes=20, value=0),
        RangeData(range_hexes=40, value=1),
        RangeData(range_hexes=70, value=2),
        RangeData(range_hexes=100, value=2),
        RangeData(range_hexes=200, value=5),
        RangeData(range_hexes=300, value=8),
        RangeData(range_hexes=400, value=12)
    ]
)

fal_ballistic = WeaponBallisticData(
    minimum_arc=[
        RangeData(range_hexes=10, value=0.6),
        RangeData(range_hexes=20, value=1.0),
        RangeData(range_hexes=40, value=3.0),
        RangeData(range_hexes=70, value=4.0),
        RangeData(range_hexes=100, value=6.0),
        RangeData(range_hexes=200, value=13.0),
        RangeData(range_hexes=300, value=19.0),
        RangeData(range_hexes=400, value=25.0)
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=61),
        RangeData(range_hexes=20, value=53),
        RangeData(range_hexes=40, value=45),
        RangeData(range_hexes=70, value=37),
        RangeData(range_hexes=100, value=32),
        RangeData(range_hexes=200, value=23),
        RangeData(range_hexes=300, value=17),
        RangeData(range_hexes=400, value=13)
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=0),
        RangeData(range_hexes=20, value=0),
        RangeData(range_hexes=40, value=1),
        RangeData(range_hexes=70, value=2),
        RangeData(range_hexes=100, value=2),
        RangeData(range_hexes=200, value=5),
        RangeData(range_hexes=300, value=8),
        RangeData(range_hexes=400, value=11)
    ]
)

fnc_ballistic = WeaponBallisticData(
    three_round_burst=[
        RangeData(range_hexes=10, value=-4), RangeData(range_hexes=20, value=1),
        RangeData(range_hexes=40, value=6), RangeData(range_hexes=70, value=10),
        RangeData(range_hexes=100, value=13), RangeData(range_hexes=200, value=17),
        RangeData(range_hexes=300, value=20), RangeData(range_hexes=400, value=22)
    ],
    minimum_arc=[
        RangeData(range_hexes=10, value=0.3), RangeData(range_hexes=20, value=0.6),
        RangeData(range_hexes=40, value=1.0), RangeData(range_hexes=70, value=2.0),
        RangeData(range_hexes=100, value=3.0), RangeData(range_hexes=200, value=6.0),
        RangeData(range_hexes=300, value=9.0), RangeData(range_hexes=400, value=12.0),
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=61), RangeData(range_hexes=20, value=53),
        RangeData(range_hexes=40, value=44), RangeData(range_hexes=70, value=37),
        RangeData(range_hexes=100, value=32), RangeData(range_hexes=200, value=22),
        RangeData(range_hexes=300, value=17), RangeData(range_hexes=400, value=13)
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=0), RangeData(range_hexes=20, value=0),
        RangeData(range_hexes=40, value=1), RangeData(range_hexes=70, value=2),
        RangeData(range_hexes=100, value=2), RangeData(range_hexes=200, value=5),
        RangeData(range_hexes=300, value=8), RangeData(range_hexes=400, value=11)
    ]
)

m1949_ballistic = WeaponBallisticData(
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=62), RangeData(range_hexes=20, value=54),
        RangeData(range_hexes=40, value=45), RangeData(range_hexes=70, value=38),
        RangeData(range_hexes=100, value=33), RangeData(range_hexes=200, value=24),
        RangeData(range_hexes=300, value=18), RangeData(range_hexes=400, value=14)
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=0), RangeData(range_hexes=20, value=0),
        RangeData(range_hexes=40, value=1), RangeData(range_hexes=70, value=2),
        RangeData(range_hexes=100, value=2), RangeData(range_hexes=200, value=5),
        RangeData(range_hexes=300, value=8), RangeData(range_hexes=400, value=12)
    ]
)

famas_ballistic = WeaponBallisticData(
    three_round_burst=[
        RangeData(range_hexes=10, value=-6), RangeData(range_hexes=20, value=-1),
        RangeData(range_hexes=40, value=4), RangeData(range_hexes=70, value=8),
        RangeData(range_hexes=100, value=10), RangeData(range_hexes=200, value=15),
        RangeData(range_hexes=300, value=18), RangeData(range_hexes=400, value=20)
    ],
    minimum_arc=[
        RangeData(range_hexes=10, value=0.4), RangeData(range_hexes=20, value=0.8),
        RangeData(range_hexes=40, value=2.0), RangeData(range_hexes=70, value=3.0),
        RangeData(range_hexes=100, value=4.0), RangeData(range_hexes=200, value=8.0),
        RangeData(range_hexes=300, value=12.0), RangeData(range_hexes=400, value=16.0),
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=60), RangeData(range_hexes=20, value=51),
        RangeData(range_hexes=40, value=42), RangeData(range_hexes=70, value=35),
        RangeData(range_hexes=100, value=30), RangeData(range_hexes=200, value=20),
        RangeData(range_hexes=300, value=15), RangeData(range_hexes=400, value=11)
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=0), RangeData(range_hexes=20, value=0),
        RangeData(range_hexes=40, value=1), RangeData(range_hexes=70, value=1),
        RangeData(range_hexes=100, value=2), RangeData(range_hexes=200, value=5),
        RangeData(range_hexes=300, value=8), RangeData(range_hexes=400, value=11)
    ]
)

fr_f2_ballistic = WeaponBallisticData(
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=68), RangeData(range_hexes=20, value=59),
        RangeData(range_hexes=40, value=50), RangeData(range_hexes=70, value=43),
        RangeData(range_hexes=100, value=38), RangeData(range_hexes=200, value=28),
        RangeData(range_hexes=300, value=22), RangeData(range_hexes=400, value=18)
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=0), RangeData(range_hexes=20, value=0),
        RangeData(range_hexes=40, value=1), RangeData(range_hexes=70, value=2),
        RangeData(range_hexes=100, value=2), RangeData(range_hexes=200, value=5),
        RangeData(range_hexes=300, value=8), RangeData(range_hexes=400, value=11)
    ]
)

g3_ballistic = WeaponBallisticData(
    minimum_arc=[
        RangeData(range_hexes=10, value=0.5), RangeData(range_hexes=20, value=1.0),
        RangeData(range_hexes=40, value=2.0), RangeData(range_hexes=70, value=3.0),
        RangeData(range_hexes=100, value=5.0), RangeData(range_hexes=200, value=10.0),
        RangeData(range_hexes=300, value=14.0), RangeData(range_hexes=400, value=19.0)
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=61), RangeData(range_hexes=20, value=53),
        RangeData(range_hexes=40, value=44), RangeData(range_hexes=70, value=37),
        RangeData(range_hexes=100, value=32), RangeData(range_hexes=200, value=23),
        RangeData(range_hexes=300, value=17), RangeData(range_hexes=400, value=13)
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=0), RangeData(range_hexes=20, value=0),
        RangeData(range_hexes=40, value=1), RangeData(range_hexes=70, value=2),
        RangeData(range_hexes=100, value=3), RangeData(range_hexes=200, value=5),
        RangeData(range_hexes=300, value=9), RangeData(range_hexes=400, value=12)
    ]
)

g41_ballistic = WeaponBallisticData(
    three_round_burst=[
        RangeData(range_hexes=10, value=-4), RangeData(range_hexes=20, value=1),
        RangeData(range_hexes=40, value=5), RangeData(range_hexes=70, value=9),
        RangeData(range_hexes=100, value=12), RangeData(range_hexes=200, value=17),
        RangeData(range_hexes=300, value=20), RangeData(range_hexes=400, value=22)
    ],
    minimum_arc=[
        RangeData(range_hexes=10, value=0.4), RangeData(range_hexes=20, value=0.8),
        RangeData(range_hexes=40, value=2.0), RangeData(range_hexes=70, value=3.0),
        RangeData(range_hexes=100, value=4.0), RangeData(range_hexes=200, value=8.0),
        RangeData(range_hexes=300, value=11.0), RangeData(range_hexes=400, value=15.0)
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=61), RangeData(range_hexes=20, value=53),
        RangeData(range_hexes=40, value=44), RangeData(range_hexes=70, value=37),
        RangeData(range_hexes=100, value=32), RangeData(range_hexes=200, value=22),
        RangeData(range_hexes=300, value=17), RangeData(range_hexes=400, value=13)
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=0), RangeData(range_hexes=20, value=0),
        RangeData(range_hexes=40, value=1), RangeData(range_hexes=70, value=1),
        RangeData(range_hexes=100, value=2), RangeData(range_hexes=200, value=5),
        RangeData(range_hexes=300, value=8), RangeData(range_hexes=400, value=11)
    ]
)

g11_ballistic = WeaponBallisticData(
    three_round_burst=[
        RangeData(range_hexes=10, value=-20), RangeData(range_hexes=20, value=-16),
        RangeData(range_hexes=40, value=-11), RangeData(range_hexes=70, value=-7),
        RangeData(range_hexes=100, value=-4), RangeData(range_hexes=200, value=1),
        RangeData(range_hexes=300, value=4), RangeData(range_hexes=400, value=6)
    ],
    minimum_arc=[
        RangeData(range_hexes=10, value=0.2), RangeData(range_hexes=20, value=0.5),
        RangeData(range_hexes=40, value=0.9), RangeData(range_hexes=70, value=2.0),
        RangeData(range_hexes=100, value=2.0), RangeData(range_hexes=200, value=5.0),
        RangeData(range_hexes=300, value=7.0), RangeData(range_hexes=400, value=9.0),
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=64), RangeData(range_hexes=20, value=57),
        RangeData(range_hexes=40, value=49), RangeData(range_hexes=70, value=43),
        RangeData(range_hexes=100, value=38), RangeData(range_hexes=200, value=29),
        RangeData(range_hexes=300, value=23), RangeData(range_hexes=400, value=19)
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=0), RangeData(range_hexes=20, value=0),
        RangeData(range_hexes=40, value=1), RangeData(range_hexes=70, value=1),
        RangeData(range_hexes=100, value=2), RangeData(range_hexes=200, value=5),
        RangeData(range_hexes=300, value=7), RangeData(range_hexes=400, value=10)
    ]
)

wa2000_ballistic = WeaponBallisticData(
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=70), RangeData(range_hexes=20, value=62),
        RangeData(range_hexes=40, value=53), RangeData(range_hexes=70, value=46),
        RangeData(range_hexes=100, value=41), RangeData(range_hexes=200, value=32),
        RangeData(range_hexes=300, value=26), RangeData(range_hexes=400, value=22)
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=0), RangeData(range_hexes=20, value=0),
        RangeData(range_hexes=40, value=1), RangeData(range_hexes=70, value=1),
        RangeData(range_hexes=100, value=2), RangeData(range_hexes=200, value=5),
        RangeData(range_hexes=300, value=7), RangeData(range_hexes=400, value=10)
    ]
)

amd65_ballistic = WeaponBallisticData(
    minimum_arc=[
        RangeData(range_hexes=10, value=0.4), RangeData(range_hexes=20, value=0.8),
        RangeData(range_hexes=40, value=2.0), RangeData(range_hexes=70, value=3.0),
        RangeData(range_hexes=100, value=4.0), RangeData(range_hexes=200, value=8.0),
        RangeData(range_hexes=300, value=12.0), RangeData(range_hexes=400, value=16.0),
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=58), RangeData(range_hexes=20, value=50),
        RangeData(range_hexes=40, value=40), RangeData(range_hexes=70, value=33),
        RangeData(range_hexes=100, value=28), RangeData(range_hexes=200, value=18),
        RangeData(range_hexes=300, value=13), RangeData(range_hexes=400, value=9)
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=0), RangeData(range_hexes=20, value=1),
        RangeData(range_hexes=40, value=1), RangeData(range_hexes=70, value=2),
        RangeData(range_hexes=100, value=3), RangeData(range_hexes=200, value=6),
        RangeData(range_hexes=300, value=10), RangeData(range_hexes=400, value=15)
    ]
)

galil_556_ballistic = WeaponBallisticData(
    minimum_arc=[
        RangeData(range_hexes=10, value=0.2), RangeData(range_hexes=20, value=0.5),
        RangeData(range_hexes=40, value=0.9), RangeData(range_hexes=70, value=2.0),
        RangeData(range_hexes=100, value=2.0), RangeData(range_hexes=200, value=5.0),
        RangeData(range_hexes=300, value=7.0), RangeData(range_hexes=400, value=9.0)
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=60), RangeData(range_hexes=20, value=51),
        RangeData(range_hexes=40, value=42), RangeData(range_hexes=70, value=35),
        RangeData(range_hexes=100, value=30), RangeData(range_hexes=200, value=20),
        RangeData(range_hexes=300, value=15), RangeData(range_hexes=400, value=11)
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=0), RangeData(range_hexes=20, value=0),
        RangeData(range_hexes=40, value=1), RangeData(range_hexes=70, value=1),
        RangeData(range_hexes=100, value=2), RangeData(range_hexes=200, value=5),
        RangeData(range_hexes=300, value=7), RangeData(range_hexes=400, value=11)
    ]
)

galil_762_ballistic = WeaponBallisticData(
    minimum_arc=[
        RangeData(range_hexes=10, value=0.5), RangeData(range_hexes=20, value=1.0),
        RangeData(range_hexes=40, value=2.0), RangeData(range_hexes=70, value=4.0),
        RangeData(range_hexes=100, value=5.0), RangeData(range_hexes=200, value=11.0),
        RangeData(range_hexes=300, value=16.0), RangeData(range_hexes=400, value=21.0)
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=61), RangeData(range_hexes=20, value=53),
        RangeData(range_hexes=40, value=45), RangeData(range_hexes=70, value=37),
        RangeData(range_hexes=100, value=32), RangeData(range_hexes=200, value=23),
        RangeData(range_hexes=300, value=17), RangeData(range_hexes=400, value=13)
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=0), RangeData(range_hexes=20, value=0),
        RangeData(range_hexes=40, value=1), RangeData(range_hexes=70, value=2),
        RangeData(range_hexes=100, value=2), RangeData(range_hexes=200, value=5),
        RangeData(range_hexes=300, value=8), RangeData(range_hexes=400, value=11)
    ]
)

beretta_bm59_ballistic = WeaponBallisticData(
    minimum_arc=[
        RangeData(range_hexes=10, value=0.6), RangeData(range_hexes=20, value=1.0),
        RangeData(range_hexes=40, value=2.0), RangeData(range_hexes=70, value=4.0),
        RangeData(range_hexes=100, value=6.0), RangeData(range_hexes=200, value=12.0),
        RangeData(range_hexes=300, value=18.0), RangeData(range_hexes=400, value=24.0)
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=61), RangeData(range_hexes=20, value=53),
        RangeData(range_hexes=40, value=45), RangeData(range_hexes=70, value=37),
        RangeData(range_hexes=100, value=32), RangeData(range_hexes=200, value=23),
        RangeData(range_hexes=300, value=17), RangeData(range_hexes=400, value=13)
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=0), RangeData(range_hexes=20, value=0),
        RangeData(range_hexes=40, value=1), RangeData(range_hexes=70, value=2),
        RangeData(range_hexes=100, value=2), RangeData(range_hexes=200, value=5),
        RangeData(range_hexes=300, value=8), RangeData(range_hexes=400, value=12)
    ]
)

sc70_ballistic = WeaponBallisticData(
    minimum_arc=[
        RangeData(range_hexes=10, value=0.2), RangeData(range_hexes=20, value=0.5),
        RangeData(range_hexes=40, value=1.0), RangeData(range_hexes=70, value=2.0),
        RangeData(range_hexes=100, value=2.0), RangeData(range_hexes=200, value=5.0),
        RangeData(range_hexes=300, value=7.0), RangeData(range_hexes=400, value=10.0)
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=60), RangeData(range_hexes=20, value=51),
        RangeData(range_hexes=40, value=42), RangeData(range_hexes=70, value=35),
        RangeData(range_hexes=100, value=30), RangeData(range_hexes=200, value=20),
        RangeData(range_hexes=300, value=15), RangeData(range_hexes=400, value=11)
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=0), RangeData(range_hexes=20, value=0),
        RangeData(range_hexes=40, value=1), RangeData(range_hexes=70, value=1),
        RangeData(range_hexes=100, value=2), RangeData(range_hexes=200, value=5),
        RangeData(range_hexes=300, value=8), RangeData(range_hexes=400, value=11)
    ]
)

type64_ballistic = WeaponBallisticData(
    minimum_arc=[
        RangeData(range_hexes=10, value=0.3), RangeData(range_hexes=20, value=0.7),
        RangeData(range_hexes=40, value=1.0), RangeData(range_hexes=70, value=2.0),
        RangeData(range_hexes=100, value=3.0), RangeData(range_hexes=200, value=7.0),
        RangeData(range_hexes=300, value=10.0), RangeData(range_hexes=400, value=14.0)
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=61), RangeData(range_hexes=20, value=53),
        RangeData(range_hexes=40, value=44), RangeData(range_hexes=70, value=37),
        RangeData(range_hexes=100, value=32), RangeData(range_hexes=200, value=22),
        RangeData(range_hexes=300, value=17), RangeData(range_hexes=400, value=13)
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=0), RangeData(range_hexes=20, value=1),
        RangeData(range_hexes=40, value=1), RangeData(range_hexes=70, value=2),
        RangeData(range_hexes=100, value=3), RangeData(range_hexes=200, value=6),
        RangeData(range_hexes=300, value=10), RangeData(range_hexes=400, value=14)
    ]
)

r4_ballistic = WeaponBallisticData(
    minimum_arc=[
        RangeData(range_hexes=10, value=0.2), RangeData(range_hexes=20, value=0.4),
        RangeData(range_hexes=40, value=0.9), RangeData(range_hexes=70, value=1.0),
        RangeData(range_hexes=100, value=2.0), RangeData(range_hexes=200, value=4.0),
        RangeData(range_hexes=300, value=6.0), RangeData(range_hexes=400, value=9.0)
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=59), RangeData(range_hexes=20, value=51),
        RangeData(range_hexes=40, value=42), RangeData(range_hexes=70, value=35),
        RangeData(range_hexes=100, value=30), RangeData(range_hexes=200, value=20),
        RangeData(range_hexes=300, value=14), RangeData(range_hexes=400, value=11)
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=0), RangeData(range_hexes=20, value=0),
        RangeData(range_hexes=40, value=1), RangeData(range_hexes=70, value=1),
        RangeData(range_hexes=100, value=2), RangeData(range_hexes=200, value=5),
        RangeData(range_hexes=300, value=7), RangeData(range_hexes=400, value=11)
    ]
)

akm_ballistic = WeaponBallisticData(
    minimum_arc=[
        RangeData(range_hexes=10, value=0.4), RangeData(range_hexes=20, value=0.8),
        RangeData(range_hexes=40, value=2.0), RangeData(range_hexes=70, value=3.0),
        RangeData(range_hexes=100, value=4.0), RangeData(range_hexes=200, value=8.0),
        RangeData(range_hexes=300, value=12.0), RangeData(range_hexes=400, value=17.0),
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=58), RangeData(range_hexes=20, value=50),
        RangeData(range_hexes=40, value=40), RangeData(range_hexes=70, value=33),
        RangeData(range_hexes=100, value=28), RangeData(range_hexes=200, value=18),
        RangeData(range_hexes=300, value=13), RangeData(range_hexes=9, value=9)
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=0), RangeData(range_hexes=20, value=1),
        RangeData(range_hexes=40, value=1), RangeData(range_hexes=70, value=2),
        RangeData(range_hexes=100, value=3), RangeData(range_hexes=200, value=6),
        RangeData(range_hexes=300, value=10), RangeData(range_hexes=400, value=14)
    ]
)

ak74_ballistic = WeaponBallisticData(
    minimum_arc=[
        RangeData(range_hexes=10, value=0.2), RangeData(range_hexes=20, value=0.3),
        RangeData(range_hexes=40, value=0.5), RangeData(range_hexes=70, value=0.9),
        RangeData(range_hexes=100, value=1.0), RangeData(range_hexes=200, value=3.0),
        RangeData(range_hexes=300, value=4.0), RangeData(range_hexes=400, value=5.0),
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=60), RangeData(range_hexes=20, value=52),
        RangeData(range_hexes=40, value=43), RangeData(range_hexes=70, value=36),
        RangeData(range_hexes=100, value=31), RangeData(range_hexes=200, value=21),
        RangeData(range_hexes=300, value=16), RangeData(range_hexes=400, value=12)
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=0), RangeData(range_hexes=20, value=0),
        RangeData(range_hexes=40, value=1), RangeData(range_hexes=70, value=2),
        RangeData(range_hexes=100, value=2), RangeData(range_hexes=200, value=5),
        RangeData(range_hexes=300, value=8), RangeData(range_hexes=400, value=12)
    ]
)

svd_ballistic = WeaponBallisticData(
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=69), RangeData(range_hexes=20, value=62),
        RangeData(range_hexes=40, value=53), RangeData(range_hexes=70, value=46),
        RangeData(range_hexes=100, value=41), RangeData(range_hexes=200, value=32),
        RangeData(range_hexes=300, value=26), RangeData(range_hexes=400, value=22)
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=0), RangeData(range_hexes=20, value=0),
        RangeData(range_hexes=40, value=1), RangeData(range_hexes=70, value=2),
        RangeData(range_hexes=100, value=2), RangeData(range_hexes=200, value=5),
        RangeData(range_hexes=300, value=8), RangeData(range_hexes=400, value=11)
    ]
)

enfield_iw_ballistic = WeaponBallisticData(
    minimum_arc=[
        RangeData(range_hexes=10, value=0.3), RangeData(range_hexes=20, value=0.6),
        RangeData(range_hexes=40, value=1.0), RangeData(range_hexes=70, value=2.0),
        RangeData(range_hexes=100, value=3.0), RangeData(range_hexes=200, value=6.0),
        RangeData(range_hexes=300, value=9.0), RangeData(range_hexes=400, value=13.0),
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=61), RangeData(range_hexes=20, value=53),
        RangeData(range_hexes=40, value=44), RangeData(range_hexes=70, value=37),
        RangeData(range_hexes=100, value=32), RangeData(range_hexes=200, value=22),
        RangeData(range_hexes=300, value=17), RangeData(range_hexes=400, value=13)
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=0), RangeData(range_hexes=20, value=0),
        RangeData(range_hexes=40, value=1), RangeData(range_hexes=70, value=1),
        RangeData(range_hexes=100, value=2), RangeData(range_hexes=200, value=5),
        RangeData(range_hexes=300, value=8), RangeData(range_hexes=400, value=11)
    ]
)

m14_ballistic = WeaponBallisticData(
    minimum_arc=[
        RangeData(range_hexes=10, value=0.6), RangeData(range_hexes=20, value=1.0),
        RangeData(range_hexes=40, value=2.0), RangeData(range_hexes=70, value=4.0),
        RangeData(range_hexes=100, value=6.0), RangeData(range_hexes=200, value=12.0),
        RangeData(range_hexes=300, value=19.0), RangeData(range_hexes=400, value=25.0)
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=61), RangeData(range_hexes=20, value=53),
        RangeData(range_hexes=40, value=45), RangeData(range_hexes=70, value=37),
        RangeData(range_hexes=100, value=32), RangeData(range_hexes=200, value=23),
        RangeData(range_hexes=300, value=17), RangeData(range_hexes=400, value=13)
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=0), RangeData(range_hexes=20, value=0),
        RangeData(range_hexes=40, value=1), RangeData(range_hexes=70, value=2),
        RangeData(range_hexes=100, value=2), RangeData(range_hexes=200, value=5),
        RangeData(range_hexes=300, value=8), RangeData(range_hexes=400, value=11)
    ]
)

m16a1_ballistic = WeaponBallisticData(
    minimum_arc=[
        RangeData(range_hexes=10, value=0.4), RangeData(range_hexes=20, value=0.8),
        RangeData(range_hexes=40, value=2.0), RangeData(range_hexes=70, value=3.0),
        RangeData(range_hexes=100, value=4.0), RangeData(range_hexes=200, value=8.0),
        RangeData(range_hexes=300, value=11.0), RangeData(range_hexes=400, value=15.0)
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=60), RangeData(range_hexes=20, value=51),
        RangeData(range_hexes=40, value=42), RangeData(range_hexes=70, value=35),
        RangeData(range_hexes=100, value=30), RangeData(range_hexes=200, value=20),
        RangeData(range_hexes=300, value=15), RangeData(range_hexes=400, value=11)
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=0), RangeData(range_hexes=20, value=0),
        RangeData(range_hexes=40, value=1), RangeData(range_hexes=70, value=1),
        RangeData(range_hexes=100, value=2), RangeData(range_hexes=200, value=4),
        RangeData(range_hexes=300, value=7), RangeData(range_hexes=400, value=10)
    ]
)

xm177_ballistic = WeaponBallisticData(
    minimum_arc=[
        RangeData(range_hexes=10, value=0.4), RangeData(range_hexes=20, value=0.8),
        RangeData(range_hexes=40, value=2.0), RangeData(range_hexes=70, value=3.0),
        RangeData(range_hexes=100, value=4.0), RangeData(range_hexes=200, value=8.0),
        RangeData(range_hexes=300, value=11.0), RangeData(range_hexes=400, value=15.0)
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=60), RangeData(range_hexes=20, value=51),
        RangeData(range_hexes=40, value=42), RangeData(range_hexes=70, value=35),
        RangeData(range_hexes=100, value=30), RangeData(range_hexes=200, value=20),
        RangeData(range_hexes=300, value=15), RangeData(range_hexes=400, value=11)
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=0), RangeData(range_hexes=20, value=0),
        RangeData(range_hexes=40, value=1), RangeData(range_hexes=70, value=1),
        RangeData(range_hexes=100, value=2), RangeData(range_hexes=200, value=5),
        RangeData(range_hexes=300, value=8), RangeData(range_hexes=400, value=11)
    ]
)

m16a2_ballistic = WeaponBallisticData(
    three_round_burst=[
        RangeData(range_hexes=10, value=-5), RangeData(range_hexes=20, value=-0),
        RangeData(range_hexes=40, value=5), RangeData(range_hexes=70, value=9),
        RangeData(range_hexes=100, value=11), RangeData(range_hexes=200, value=16),
        RangeData(range_hexes=300, value=19), RangeData(range_hexes=400, value=21)
    ],
    minimum_arc=[
        RangeData(range_hexes=10, value=0.4), RangeData(range_hexes=20, value=0.8),
        RangeData(range_hexes=40, value=2.0), RangeData(range_hexes=70, value=3.0),
        RangeData(range_hexes=100, value=4.0), RangeData(range_hexes=200, value=8.0),
        RangeData(range_hexes=300, value=11.0), RangeData(range_hexes=400, value=15.0)
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=61), RangeData(range_hexes=20, value=53),
        RangeData(range_hexes=40, value=44), RangeData(range_hexes=70, value=37),
        RangeData(range_hexes=100, value=32), RangeData(range_hexes=200, value=22),
        RangeData(range_hexes=300, value=17), RangeData(range_hexes=400, value=13)
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=0), RangeData(range_hexes=20, value=0),
        RangeData(range_hexes=40, value=1), RangeData(range_hexes=70, value=1),
        RangeData(range_hexes=100, value=2), RangeData(range_hexes=200, value=5),
        RangeData(range_hexes=300, value=7), RangeData(range_hexes=400, value=11)
    ]
)

m40a1_ballistic = WeaponBallisticData(
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=68), RangeData(range_hexes=20, value=59),
        RangeData(range_hexes=40, value=50), RangeData(range_hexes=70, value=43),
        RangeData(range_hexes=100, value=38), RangeData(range_hexes=200, value=28),
        RangeData(range_hexes=300, value=22), RangeData(range_hexes=400, value=18)
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=0), RangeData(range_hexes=20, value=0),
        RangeData(range_hexes=40, value=1), RangeData(range_hexes=70, value=2),
        RangeData(range_hexes=100, value=2), RangeData(range_hexes=200, value=5),
        RangeData(range_hexes=300, value=8), RangeData(range_hexes=400, value=11)
    ]
)

steyr_lsw_ballistic = WeaponBallisticData(
    minimum_arc=[
        RangeData(range_hexes=10, value=0.2), RangeData(range_hexes=20, value=0.4),
        RangeData(range_hexes=40, value=0.9), RangeData(range_hexes=70, value=2.0),
        RangeData(range_hexes=100, value=2.0), RangeData(range_hexes=200, value=4.0),
        RangeData(range_hexes=300, value=7.0), RangeData(range_hexes=400, value=9.0)
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=60), RangeData(range_hexes=20, value=51),
        RangeData(range_hexes=40, value=42), RangeData(range_hexes=70, value=35),
        RangeData(range_hexes=100, value=30), RangeData(range_hexes=200, value=20),
        RangeData(range_hexes=300, value=15), RangeData(range_hexes=400, value=11)
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=0), RangeData(range_hexes=20, value=0),
        RangeData(range_hexes=40, value=1), RangeData(range_hexes=70, value=1),
        RangeData(range_hexes=100, value=2), RangeData(range_hexes=200, value=4),
        RangeData(range_hexes=300, value=7), RangeData(range_hexes=400, value=10)
    ]
)

fn_mag_ballistic = WeaponBallisticData(
    minimum_arc=[
        RangeData(range_hexes=10, value=0.3), RangeData(range_hexes=20, value=0.6),
        RangeData(range_hexes=40, value=1.0), RangeData(range_hexes=70, value=2.0),
        RangeData(range_hexes=100, value=3.0), RangeData(range_hexes=200, value=6.0),
        RangeData(range_hexes=300, value=9.0), RangeData(range_hexes=400, value=12.0)
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=61), RangeData(range_hexes=20, value=53),
        RangeData(range_hexes=40, value=45), RangeData(range_hexes=70, value=37),
        RangeData(range_hexes=100, value=32), RangeData(range_hexes=200, value=23),
        RangeData(range_hexes=300, value=17), RangeData(range_hexes=400, value=13)
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=0), RangeData(range_hexes=20, value=0),
        RangeData(range_hexes=40, value=1), RangeData(range_hexes=70, value=2),
        RangeData(range_hexes=100, value=2), RangeData(range_hexes=200, value=5),
        RangeData(range_hexes=300, value=8), RangeData(range_hexes=400, value=11)
    ]
)

type_67_ballistic = WeaponBallisticData(
    minimum_arc=[
        RangeData(range_hexes=10, value=0.3), RangeData(range_hexes=20, value=0.6),
        RangeData(range_hexes=40, value=1.0), RangeData(range_hexes=70, value=2.0),
        RangeData(range_hexes=100, value=3.0), RangeData(range_hexes=200, value=6.0),
        RangeData(range_hexes=300, value=10.0), RangeData(range_hexes=400, value=13.0)
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=63), RangeData(range_hexes=20, value=56),
        RangeData(range_hexes=40, value=48), RangeData(range_hexes=70, value=41),
        RangeData(range_hexes=100, value=36), RangeData(range_hexes=200, value=27),
        RangeData(range_hexes=300, value=21), RangeData(range_hexes=400, value=17)
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=0), RangeData(range_hexes=20, value=0),
        RangeData(range_hexes=40, value=1), RangeData(range_hexes=70, value=2),
        RangeData(range_hexes=100, value=2), RangeData(range_hexes=200, value=5),
        RangeData(range_hexes=300, value=8), RangeData(range_hexes=400, value=11)
    ]
)

aa_762_ballistic = WeaponBallisticData(
    minimum_arc=[
        RangeData(range_hexes=10, value=0.3), RangeData(range_hexes=20, value=0.6),
        RangeData(range_hexes=40, value=1.0), RangeData(range_hexes=70, value=2.0),
        RangeData(range_hexes=100, value=3.0), RangeData(range_hexes=200, value=6.0),
        RangeData(range_hexes=300, value=10.0), RangeData(range_hexes=400, value=13.0)
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=61), RangeData(range_hexes=20, value=53),
        RangeData(range_hexes=40, value=45), RangeData(range_hexes=70, value=37),
        RangeData(range_hexes=100, value=32), RangeData(range_hexes=200, value=23),
        RangeData(range_hexes=300, value=17), RangeData(range_hexes=400, value=13)
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=0), RangeData(range_hexes=20, value=0),
        RangeData(range_hexes=40, value=1), RangeData(range_hexes=70, value=2),
        RangeData(range_hexes=100, value=2), RangeData(range_hexes=200, value=5),
        RangeData(range_hexes=300, value=8), RangeData(range_hexes=400, value=11)
    ]
)

hk_13e_ballistic = WeaponBallisticData(
    three_round_burst=[
        RangeData(range_hexes=10, value=-8), RangeData(range_hexes=20, value=-3),
        RangeData(range_hexes=40, value=2), RangeData(range_hexes=70, value=6),
        RangeData(range_hexes=100, value=9), RangeData(range_hexes=200, value=14),
        RangeData(range_hexes=300, value=17), RangeData(range_hexes=400, value=19)
    ],
    minimum_arc=[
        RangeData(range_hexes=10, value=0.2), RangeData(range_hexes=20, value=0.3),
        RangeData(range_hexes=40, value=0.7), RangeData(range_hexes=70, value=1.0),
        RangeData(range_hexes=100, value=2.0), RangeData(range_hexes=200, value=3.0),
        RangeData(range_hexes=300, value=5.0), RangeData(range_hexes=400, value=7.0)
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=61), RangeData(range_hexes=20, value=53),
        RangeData(range_hexes=40, value=44), RangeData(range_hexes=70, value=37),
        RangeData(range_hexes=100, value=32), RangeData(range_hexes=200, value=22),
        RangeData(range_hexes=300, value=17), RangeData(range_hexes=400, value=13)
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=0), RangeData(range_hexes=20, value=0),
        RangeData(range_hexes=40, value=1), RangeData(range_hexes=70, value=1),
        RangeData(range_hexes=100, value=2), RangeData(range_hexes=200, value=5),
        RangeData(range_hexes=300, value=7), RangeData(range_hexes=400, value=11)
    ]
)

hk_11e_ballistic = WeaponBallisticData(
    three_round_burst=[
        RangeData(range_hexes=10, value=-4), RangeData(range_hexes=20, value=1),
        RangeData(range_hexes=40, value=6), RangeData(range_hexes=70, value=10),
        RangeData(range_hexes=100, value=13), RangeData(range_hexes=200, value=17),
        RangeData(range_hexes=300, value=20), RangeData(range_hexes=400, value=22)
    ],
    minimum_arc=[
        RangeData(range_hexes=10, value=0.4), RangeData(range_hexes=20, value=0.8),
        RangeData(range_hexes=40, value=2.0), RangeData(range_hexes=70, value=3.0),
        RangeData(range_hexes=100, value=4.0), RangeData(range_hexes=200, value=8.0),
        RangeData(range_hexes=300, value=12.0), RangeData(range_hexes=400, value=16.0)
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=61), RangeData(range_hexes=20, value=53),
        RangeData(range_hexes=40, value=45), RangeData(range_hexes=70, value=37),
        RangeData(range_hexes=100, value=32), RangeData(range_hexes=200, value=23),
        RangeData(range_hexes=300, value=17), RangeData(range_hexes=400, value=13)
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=0), RangeData(range_hexes=20, value=0),
        RangeData(range_hexes=40, value=1), RangeData(range_hexes=70, value=2),
        RangeData(range_hexes=100, value=2), RangeData(range_hexes=200, value=5),
        RangeData(range_hexes=300, value=9), RangeData(range_hexes=400, value=12)
    ]
)

hk_23e_ballistic = WeaponBallisticData(
    three_round_burst=[
        RangeData(range_hexes=10, value=-8), RangeData(range_hexes=20, value=-3),
        RangeData(range_hexes=40, value=2), RangeData(range_hexes=70, value=6),
        RangeData(range_hexes=100, value=8), RangeData(range_hexes=200, value=13),
        RangeData(range_hexes=300, value=16), RangeData(range_hexes=400, value=18)
    ],
    minimum_arc=[
        RangeData(range_hexes=10, value=0.2), RangeData(range_hexes=20, value=0.3),
        RangeData(range_hexes=40, value=0.7), RangeData(range_hexes=70, value=1.0),
        RangeData(range_hexes=100, value=2.0), RangeData(range_hexes=200, value=3.0),
        RangeData(range_hexes=300, value=5.0), RangeData(range_hexes=400, value=7.0)
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=61), RangeData(range_hexes=20, value=53),
        RangeData(range_hexes=40, value=44), RangeData(range_hexes=70, value=37),
        RangeData(range_hexes=100, value=32), RangeData(range_hexes=200, value=22),
        RangeData(range_hexes=300, value=17), RangeData(range_hexes=400, value=13)
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=0), RangeData(range_hexes=20, value=0),
        RangeData(range_hexes=40, value=1), RangeData(range_hexes=70, value=1),
        RangeData(range_hexes=100, value=2), RangeData(range_hexes=200, value=5),
        RangeData(range_hexes=300, value=8), RangeData(range_hexes=400, value=11)
    ]
)

hk_21e_ballistic = WeaponBallisticData(
    three_round_burst=[
        RangeData(range_hexes=10, value=-4), RangeData(range_hexes=20, value=1),
        RangeData(range_hexes=40, value=6), RangeData(range_hexes=70, value=10),
        RangeData(range_hexes=100, value=12), RangeData(range_hexes=200, value=17),
        RangeData(range_hexes=300, value=20), RangeData(range_hexes=400, value=22)
    ],
    minimum_arc=[
        RangeData(range_hexes=10, value=0.4), RangeData(range_hexes=20, value=0.8),
        RangeData(range_hexes=40, value=2.0), RangeData(range_hexes=70, value=3.0),
        RangeData(range_hexes=100, value=4.0), RangeData(range_hexes=200, value=8.0),
        RangeData(range_hexes=300, value=12.0), RangeData(range_hexes=400, value=16.0)
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=61), RangeData(range_hexes=20, value=53),
        RangeData(range_hexes=40, value=45), RangeData(range_hexes=70, value=37),
        RangeData(range_hexes=100, value=32), RangeData(range_hexes=200, value=23),
        RangeData(range_hexes=300, value=17), RangeData(range_hexes=400, value=13)
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=0), RangeData(range_hexes=20, value=0),
        RangeData(range_hexes=40, value=1), RangeData(range_hexes=70, value=2),
        RangeData(range_hexes=100, value=2), RangeData(range_hexes=200, value=5),
        RangeData(range_hexes=300, value=8), RangeData(range_hexes=400, value=11)
    ]
)

mg3_ballistic = WeaponBallisticData(
    minimum_arc=[
        RangeData(range_hexes=10, value=0.5), RangeData(range_hexes=20, value=1.0),
        RangeData(range_hexes=40, value=2.0), RangeData(range_hexes=70, value=3.0),
        RangeData(range_hexes=100, value=5.0), RangeData(range_hexes=200, value=10.0),
        RangeData(range_hexes=300, value=14.0), RangeData(range_hexes=400, value=19.0)
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=61), RangeData(range_hexes=20, value=53),
        RangeData(range_hexes=40, value=45), RangeData(range_hexes=70, value=37),
        RangeData(range_hexes=100, value=32), RangeData(range_hexes=200, value=23),
        RangeData(range_hexes=300, value=17), RangeData(range_hexes=400, value=13)
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=0), RangeData(range_hexes=20, value=0),
        RangeData(range_hexes=40, value=1), RangeData(range_hexes=70, value=2),
        RangeData(range_hexes=100, value=2), RangeData(range_hexes=200, value=5),
        RangeData(range_hexes=300, value=8), RangeData(range_hexes=400, value=12)
    ]
)

galil_arm_ballistic = WeaponBallisticData(
    minimum_arc=[
        RangeData(range_hexes=10, value=0.2),
        RangeData(range_hexes=20, value=0.4),
        RangeData(range_hexes=40, value=0.8),
        RangeData(range_hexes=70, value=1.0),
        RangeData(range_hexes=100, value=2.0),
        RangeData(range_hexes=200, value=4.0),
        RangeData(range_hexes=300, value=6.0),
        RangeData(range_hexes=400, value=8.0)
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=60),
        RangeData(range_hexes=20, value=51),
        RangeData(range_hexes=40, value=42),
        RangeData(range_hexes=70, value=35),
        RangeData(range_hexes=100, value=30),
        RangeData(range_hexes=200, value=20),
        RangeData(range_hexes=300, value=15),
        RangeData(range_hexes=400, value=11)
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=0),
        RangeData(range_hexes=20, value=0),
        RangeData(range_hexes=40, value=1),
        RangeData(range_hexes=70, value=1),
        RangeData(range_hexes=100, value=2),
        RangeData(range_hexes=200, value=5),
        RangeData(range_hexes=300, value=7),
        RangeData(range_hexes=400, value=11)
    ]
)

beretta_m70_78_ballistic = WeaponBallisticData(
    minimum_arc=[
        RangeData(range_hexes=10, value=0.2),
        RangeData(range_hexes=20, value=0.4),
        RangeData(range_hexes=40, value=0.8),
        RangeData(range_hexes=70, value=1.0),
        RangeData(range_hexes=100, value=2.0),
        RangeData(range_hexes=200, value=4.0),
        RangeData(range_hexes=300, value=6.0),
        RangeData(range_hexes=400, value=8.0)
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=60),
        RangeData(range_hexes=20, value=51),
        RangeData(range_hexes=40, value=42),
        RangeData(range_hexes=70, value=35),
        RangeData(range_hexes=100, value=30),
        RangeData(range_hexes=200, value=20),
        RangeData(range_hexes=300, value=15),
        RangeData(range_hexes=400, value=11)
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=0),
        RangeData(range_hexes=20, value=0),
        RangeData(range_hexes=40, value=1),
        RangeData(range_hexes=70, value=1),
        RangeData(range_hexes=100, value=2),
        RangeData(range_hexes=200, value=5),
        RangeData(range_hexes=300, value=8),
        RangeData(range_hexes=400, value=11)
    ]
)

rpk_74_ballistic = WeaponBallisticData(
    minimum_arc=[
        RangeData(range_hexes=10, value=0.2),
        RangeData(range_hexes=20, value=0.4),
        RangeData(range_hexes=40, value=0.8),
        RangeData(range_hexes=70, value=1.0),
        RangeData(range_hexes=100, value=2.0),
        RangeData(range_hexes=200, value=4.0),
        RangeData(range_hexes=300, value=6.0),
        RangeData(range_hexes=400, value=8.0)
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=61),
        RangeData(range_hexes=20, value=52),
        RangeData(range_hexes=40, value=44),
        RangeData(range_hexes=70, value=36),
        RangeData(range_hexes=100, value=31),
        RangeData(range_hexes=200, value=22),
        RangeData(range_hexes=300, value=16),
        RangeData(range_hexes=400, value=12)
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=0),
        RangeData(range_hexes=20, value=0),
        RangeData(range_hexes=40, value=1),
        RangeData(range_hexes=70, value=1),
        RangeData(range_hexes=100, value=2),
        RangeData(range_hexes=200, value=4),
        RangeData(range_hexes=300, value=7),
        RangeData(range_hexes=400, value=10)
    ]
)

rpk_762_ballistic = WeaponBallisticData(
    minimum_arc=[
        RangeData(range_hexes=10, value=0.3),
        RangeData(range_hexes=20, value=0.5),
        RangeData(range_hexes=40, value=1.0),
        RangeData(range_hexes=70, value=2.0),
        RangeData(range_hexes=100, value=3.0),
        RangeData(range_hexes=200, value=5.0),
        RangeData(range_hexes=300, value=8.0),
        RangeData(range_hexes=400, value=10.0)
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=58),
        RangeData(range_hexes=20, value=50),
        RangeData(range_hexes=40, value=41),
        RangeData(range_hexes=70, value=33),
        RangeData(range_hexes=100, value=28),
        RangeData(range_hexes=200, value=18),
        RangeData(range_hexes=300, value=13),
        RangeData(range_hexes=400, value=9)
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=0),
        RangeData(range_hexes=20, value=1),
        RangeData(range_hexes=40, value=1),
        RangeData(range_hexes=70, value=2),
        RangeData(range_hexes=100, value=3),
        RangeData(range_hexes=200, value=6),
        RangeData(range_hexes=300, value=10),
        RangeData(range_hexes=400, value=14)
    ]
)

rp_46_ballistic = WeaponBallisticData(
    minimum_arc=[
        RangeData(range_hexes=10, value=0.3),
        RangeData(range_hexes=20, value=0.5),
        RangeData(range_hexes=40, value=1.0),
        RangeData(range_hexes=70, value=2.0),
        RangeData(range_hexes=100, value=3.0),
        RangeData(range_hexes=200, value=5.0),
        RangeData(range_hexes=300, value=8.0),
        RangeData(range_hexes=400, value=10.0)
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=63),
        RangeData(range_hexes=20, value=56),
        RangeData(range_hexes=40, value=48),
        RangeData(range_hexes=70, value=41),
        RangeData(range_hexes=100, value=36),
        RangeData(range_hexes=200, value=27),
        RangeData(range_hexes=300, value=21),
        RangeData(range_hexes=400, value=17)
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=0),
        RangeData(range_hexes=20, value=0),
        RangeData(range_hexes=40, value=1),
        RangeData(range_hexes=70, value=2),
        RangeData(range_hexes=100, value=2),
        RangeData(range_hexes=200, value=5),
        RangeData(range_hexes=300, value=8),
        RangeData(range_hexes=400, value=11)
    ]
)

rpd_ballistic = WeaponBallisticData(
    minimum_arc=[
        RangeData(range_hexes=10, value=0.2),
        RangeData(range_hexes=20, value=0.5),
        RangeData(range_hexes=40, value=0.9),
        RangeData(range_hexes=70, value=2.0),
        RangeData(range_hexes=100, value=2.0),
        RangeData(range_hexes=200, value=5.0),
        RangeData(range_hexes=300, value=7.0),
        RangeData(range_hexes=400, value=9.0)
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=58),
        RangeData(range_hexes=20, value=50),
        RangeData(range_hexes=40, value=40),
        RangeData(range_hexes=70, value=33),
        RangeData(range_hexes=100, value=28),
        RangeData(range_hexes=200, value=18),
        RangeData(range_hexes=300, value=13),
        RangeData(range_hexes=400, value=9)
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=0),
        RangeData(range_hexes=20, value=1),
        RangeData(range_hexes=40, value=1),
        RangeData(range_hexes=70, value=2),
        RangeData(range_hexes=100, value=3),
        RangeData(range_hexes=200, value=6),
        RangeData(range_hexes=300, value=10),
        RangeData(range_hexes=400, value=15)
    ]
)

pkm_ballistic = WeaponBallisticData(
    minimum_arc=[
        RangeData(range_hexes=10, value=0.4),
        RangeData(range_hexes=20, value=0.8),
        RangeData(range_hexes=40, value=2.0),
        RangeData(range_hexes=70, value=3.0),
        RangeData(range_hexes=100, value=4.0),
        RangeData(range_hexes=200, value=8.0),
        RangeData(range_hexes=300, value=12.0),
        RangeData(range_hexes=400, value=16.0)
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=63),
        RangeData(range_hexes=20, value=56),
        RangeData(range_hexes=40, value=48),
        RangeData(range_hexes=70, value=41),
        RangeData(range_hexes=100, value=36),
        RangeData(range_hexes=200, value=27),
        RangeData(range_hexes=300, value=21),
        RangeData(range_hexes=400, value=17)
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=0),
        RangeData(range_hexes=20, value=0),
        RangeData(range_hexes=40, value=1),
        RangeData(range_hexes=70, value=2),
        RangeData(range_hexes=100, value=2),
        RangeData(range_hexes=200, value=5),
        RangeData(range_hexes=300, value=8),
        RangeData(range_hexes=400, value=11)
    ]
)

nsv_ballistic = WeaponBallisticData(
    minimum_arc=[
        RangeData(range_hexes=10, value=0.3),
        RangeData(range_hexes=20, value=0.5),
        RangeData(range_hexes=40, value=1.0),
        RangeData(range_hexes=70, value=2.0),
        RangeData(range_hexes=100, value=3.0),
        RangeData(range_hexes=200, value=5.0),
        RangeData(range_hexes=300, value=8.0),
        RangeData(range_hexes=400, value=10.0)
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=64),
        RangeData(range_hexes=20, value=57),
        RangeData(range_hexes=40, value=49),
        RangeData(range_hexes=70, value=43),
        RangeData(range_hexes=100, value=38),
        RangeData(range_hexes=200, value=29),
        RangeData(range_hexes=300, value=23),
        RangeData(range_hexes=400, value=19)
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=0),
        RangeData(range_hexes=20, value=0),
        RangeData(range_hexes=40, value=1),
        RangeData(range_hexes=70, value=2),
        RangeData(range_hexes=100, value=2),
        RangeData(range_hexes=200, value=5),
        RangeData(range_hexes=300, value=7),
        RangeData(range_hexes=400, value=10)
    ]
)

enfield_lsw_ballistic = WeaponBallisticData(
    minimum_arc=[
        RangeData(range_hexes=10, value=0.2),
        RangeData(range_hexes=20, value=0.4),
        RangeData(range_hexes=40, value=0.7),
        RangeData(range_hexes=70, value=1.0),
        RangeData(range_hexes=100, value=2.0),
        RangeData(range_hexes=200, value=4.0),
        RangeData(range_hexes=300, value=6.0),
        RangeData(range_hexes=400, value=7.0)
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=60),
        RangeData(range_hexes=20, value=51),
        RangeData(range_hexes=40, value=42),
        RangeData(range_hexes=70, value=35),
        RangeData(range_hexes=100, value=30),
        RangeData(range_hexes=200, value=20),
        RangeData(range_hexes=300, value=15),
        RangeData(range_hexes=400, value=11)
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=0),
        RangeData(range_hexes=20, value=0),
        RangeData(range_hexes=40, value=1),
        RangeData(range_hexes=70, value=1),
        RangeData(range_hexes=100, value=2),
        RangeData(range_hexes=200, value=5),
        RangeData(range_hexes=300, value=8),
        RangeData(range_hexes=400, value=11)
    ]
)

bren_l4_ballistic = WeaponBallisticData(
    minimum_arc=[
        RangeData(range_hexes=10, value=0.2),
        RangeData(range_hexes=20, value=0.4),
        RangeData(range_hexes=40, value=0.8),
        RangeData(range_hexes=70, value=1.0),
        RangeData(range_hexes=100, value=2.0),
        RangeData(range_hexes=200, value=4.0),
        RangeData(range_hexes=300, value=6.0),
        RangeData(range_hexes=400, value=8.0)
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=61),
        RangeData(range_hexes=20, value=53),
        RangeData(range_hexes=40, value=45),
        RangeData(range_hexes=70, value=37),
        RangeData(range_hexes=100, value=32),
        RangeData(range_hexes=200, value=23),
        RangeData(range_hexes=300, value=17),
        RangeData(range_hexes=400, value=13)
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=0),
        RangeData(range_hexes=20, value=0),
        RangeData(range_hexes=40, value=1),
        RangeData(range_hexes=70, value=2),
        RangeData(range_hexes=100, value=2),
        RangeData(range_hexes=200, value=5),
        RangeData(range_hexes=300, value=8),
        RangeData(range_hexes=400, value=12)
    ]
)

l7a2_ballistic = WeaponBallisticData(
    minimum_arc=[
        RangeData(range_hexes=10, value=0.3),
        RangeData(range_hexes=20, value=0.6),
        RangeData(range_hexes=40, value=1.0),
        RangeData(range_hexes=70, value=2.0),
        RangeData(range_hexes=100, value=3.0),
        RangeData(range_hexes=200, value=6.0),
        RangeData(range_hexes=300, value=10.0),
        RangeData(range_hexes=400, value=13.0)
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=61),
        RangeData(range_hexes=20, value=53),
        RangeData(range_hexes=40, value=45),
        RangeData(range_hexes=70, value=37),
        RangeData(range_hexes=100, value=32),
        RangeData(range_hexes=200, value=23),
        RangeData(range_hexes=300, value=17),
        RangeData(range_hexes=400, value=13)
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=0),
        RangeData(range_hexes=20, value=0),
        RangeData(range_hexes=40, value=1),
        RangeData(range_hexes=70, value=2),
        RangeData(range_hexes=100, value=2),
        RangeData(range_hexes=200, value=5),
        RangeData(range_hexes=300, value=8),
        RangeData(range_hexes=400, value=12)
    ]
)

m249_minimi_ballistic = WeaponBallisticData(
    minimum_arc=[
        RangeData(range_hexes=10, value=0.2),
        RangeData(range_hexes=20, value=0.3),
        RangeData(range_hexes=40, value=0.7),
        RangeData(range_hexes=70, value=1.0),
        RangeData(range_hexes=100, value=2.0),
        RangeData(range_hexes=200, value=3.0),
        RangeData(range_hexes=300, value=5.0),
        RangeData(range_hexes=400, value=7.0)
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=61),
        RangeData(range_hexes=20, value=53),
        RangeData(range_hexes=40, value=44),
        RangeData(range_hexes=70, value=37),
        RangeData(range_hexes=100, value=32),
        RangeData(range_hexes=200, value=22),
        RangeData(range_hexes=300, value=17),
        RangeData(range_hexes=400, value=13)
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=0),
        RangeData(range_hexes=20, value=0),
        RangeData(range_hexes=40, value=1),
        RangeData(range_hexes=70, value=2),
        RangeData(range_hexes=100, value=2),
        RangeData(range_hexes=200, value=5),
        RangeData(range_hexes=300, value=8),
        RangeData(range_hexes=400, value=11)
    ]
)

m60_ballistic = WeaponBallisticData(
    minimum_arc=[
        RangeData(range_hexes=10, value=0.3),
        RangeData(range_hexes=20, value=0.5),
        RangeData(range_hexes=40, value=1.0),
        RangeData(range_hexes=70, value=2.0),
        RangeData(range_hexes=100, value=3.0),
        RangeData(range_hexes=200, value=5.0),
        RangeData(range_hexes=300, value=8.0),
        RangeData(range_hexes=400, value=10.0)
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=61),
        RangeData(range_hexes=20, value=53),
        RangeData(range_hexes=40, value=45),
        RangeData(range_hexes=70, value=37),
        RangeData(range_hexes=100, value=32),
        RangeData(range_hexes=200, value=23),
        RangeData(range_hexes=300, value=17),
        RangeData(range_hexes=400, value=13)
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=0),
        RangeData(range_hexes=20, value=0),
        RangeData(range_hexes=40, value=1),
        RangeData(range_hexes=70, value=2),
        RangeData(range_hexes=100, value=2),
        RangeData(range_hexes=200, value=5),
        RangeData(range_hexes=300, value=8),
        RangeData(range_hexes=400, value=11)
    ]
)

m60e3_ballistic = WeaponBallisticData(
    minimum_arc=[
        RangeData(range_hexes=10, value=0.3),
        RangeData(range_hexes=20, value=0.6),
        RangeData(range_hexes=40, value=1.0),
        RangeData(range_hexes=70, value=2.0),
        RangeData(range_hexes=100, value=3.0),
        RangeData(range_hexes=200, value=6.0),
        RangeData(range_hexes=300, value=9.0),
        RangeData(range_hexes=400, value=12.0)
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=61),
        RangeData(range_hexes=20, value=53),
        RangeData(range_hexes=40, value=45),
        RangeData(range_hexes=70, value=37),
        RangeData(range_hexes=100, value=33),
        RangeData(range_hexes=200, value=23),
        RangeData(range_hexes=300, value=17),
        RangeData(range_hexes=400, value=13)
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=0),
        RangeData(range_hexes=20, value=0),
        RangeData(range_hexes=40, value=1),
        RangeData(range_hexes=70, value=2),
        RangeData(range_hexes=100, value=2),
        RangeData(range_hexes=200, value=5),
        RangeData(range_hexes=300, value=8),
        RangeData(range_hexes=400, value=11)
    ]
)

m2hb_ballistic = WeaponBallisticData(
    minimum_arc=[
        RangeData(range_hexes=10, value=0.2),
        RangeData(range_hexes=20, value=0.3),
        RangeData(range_hexes=40, value=0.6),
        RangeData(range_hexes=70, value=1.0),
        RangeData(range_hexes=100, value=2.0),
        RangeData(range_hexes=200, value=3.0),
        RangeData(range_hexes=300, value=5.0),
        RangeData(range_hexes=400, value=6.0)
    ],
    ballistic_accuracy=[
        RangeData(range_hexes=10, value=64),
        RangeData(range_hexes=20, value=57),
        RangeData(range_hexes=40, value=49),
        RangeData(range_hexes=70, value=42),
        RangeData(range_hexes=100, value=37),
        RangeData(range_hexes=200, value=28),
        RangeData(range_hexes=300, value=22),
        RangeData(range_hexes=400, value=19)
    ],
    time_of_flight=[
        RangeData(range_hexes=10, value=0),
        RangeData(range_hexes=20, value=0),
        RangeData(range_hexes=40, value=1),
        RangeData(range_hexes=70, value=2),
        RangeData(range_hexes=100, value=2),
        RangeData(range_hexes=200, value=5),
        RangeData(range_hexes=300, value=8),
        RangeData(range_hexes=400, value=11)
    ]
)

spas12_ballistic = WeaponBallisticData(
    ballistic_accuracy=[
        RangeData(range_hexes=1, value=71),
        RangeData(range_hexes=2, value=61),
        RangeData(range_hexes=4, value=52),
        RangeData(range_hexes=6, value=46),
        RangeData(range_hexes=8, value=42),
        RangeData(range_hexes=10, value=39),
        RangeData(range_hexes=15, value=33),
        RangeData(range_hexes=20, value=29),
        RangeData(range_hexes=30, value=23),
        RangeData(range_hexes=40, value=19),
        RangeData(range_hexes=80, value=9)
    ],
    time_of_flight=[
        RangeData(range_hexes=1, value=0),
        RangeData(range_hexes=2, value=0),
        RangeData(range_hexes=4, value=0),
        RangeData(range_hexes=6, value=0),
        RangeData(range_hexes=8, value=0),
        RangeData(range_hexes=10, value=0),
        RangeData(range_hexes=15, value=1),
        RangeData(range_hexes=20, value=1),
        RangeData(range_hexes=30, value=1),
        RangeData(range_hexes=40, value=2),
        RangeData(range_hexes=80, value=4)
    ]
)

caws_ballistic = WeaponBallisticData(
    ballistic_accuracy=[
        RangeData(range_hexes=1, value=67),
        RangeData(range_hexes=2, value=58),
        RangeData(range_hexes=4, value=48),
        RangeData(range_hexes=6, value=42),
        RangeData(range_hexes=8, value=38),
        RangeData(range_hexes=10, value=35),
        RangeData(range_hexes=15, value=29),
        RangeData(range_hexes=20, value=25),
        RangeData(range_hexes=30, value=19),
        RangeData(range_hexes=40, value=15),
        RangeData(range_hexes=80, value=5)
    ],
    time_of_flight=[
        RangeData(range_hexes=1, value=0),
        RangeData(range_hexes=2, value=0),
        RangeData(range_hexes=4, value=0),
        RangeData(range_hexes=6, value=0),
        RangeData(range_hexes=8, value=0),
        RangeData(range_hexes=10, value=0),
        RangeData(range_hexes=15, value=1),
        RangeData(range_hexes=20, value=1),
        RangeData(range_hexes=30, value=1),
        RangeData(range_hexes=40, value=2),
        RangeData(range_hexes=80, value=4)
    ]
)

mossberg_ballistic = WeaponBallisticData(
    ballistic_accuracy=[
        RangeData(range_hexes=1, value=67),
        RangeData(range_hexes=2, value=58),
        RangeData(range_hexes=4, value=48),
        RangeData(range_hexes=6, value=42),
        RangeData(range_hexes=8, value=38),
        RangeData(range_hexes=10, value=35),
        RangeData(range_hexes=15, value=29),
        RangeData(range_hexes=20, value=25),
        RangeData(range_hexes=30, value=19),
        RangeData(range_hexes=40, value=15),
        RangeData(range_hexes=80, value=5)
    ],
    time_of_flight=[
        RangeData(range_hexes=1, value=0),
        RangeData(range_hexes=2, value=0),
        RangeData(range_hexes=4, value=0),
        RangeData(range_hexes=6, value=0),
        RangeData(range_hexes=8, value=0),
        RangeData(range_hexes=10, value=0),
        RangeData(range_hexes=15, value=1),
        RangeData(range_hexes=20, value=1),
        RangeData(range_hexes=30, value=1),
        RangeData(range_hexes=40, value=2),
        RangeData(range_hexes=80, value=4)
    ]
)

remington_ballistic = WeaponBallisticData(
    ballistic_accuracy=[
        RangeData(range_hexes=1, value=67),
        RangeData(range_hexes=2, value=58),
        RangeData(range_hexes=4, value=48),
        RangeData(range_hexes=6, value=42),
        RangeData(range_hexes=8, value=38),
        RangeData(range_hexes=10, value=35),
        RangeData(range_hexes=15, value=29),
        RangeData(range_hexes=20, value=25),
        RangeData(range_hexes=30, value=19),
        RangeData(range_hexes=40, value=15),
        RangeData(range_hexes=80, value=5)
    ],
    time_of_flight=[
        RangeData(range_hexes=1, value=0),
        RangeData(range_hexes=2, value=0),
        RangeData(range_hexes=4, value=0),
        RangeData(range_hexes=6, value=0),
        RangeData(range_hexes=8, value=0),
        RangeData(range_hexes=10, value=0),
        RangeData(range_hexes=15, value=1),
        RangeData(range_hexes=20, value=1),
        RangeData(range_hexes=30, value=1),
        RangeData(range_hexes=40, value=2),
        RangeData(range_hexes=80, value=4)
    ]
)

atchisson_ballistic = WeaponBallisticData(
    ballistic_accuracy=[
        RangeData(range_hexes=1, value=67),
        RangeData(range_hexes=2, value=58),
        RangeData(range_hexes=4, value=48),
        RangeData(range_hexes=6, value=42),
        RangeData(range_hexes=8, value=38),
        RangeData(range_hexes=10, value=35),
        RangeData(range_hexes=15, value=29),
        RangeData(range_hexes=20, value=25),
        RangeData(range_hexes=30, value=19),
        RangeData(range_hexes=40, value=15),
        RangeData(range_hexes=80, value=5)
    ],
    time_of_flight=[
        RangeData(range_hexes=1, value=0),
        RangeData(range_hexes=2, value=0),
        RangeData(range_hexes=4, value=0),
        RangeData(range_hexes=6, value=0),
        RangeData(range_hexes=8, value=0),
        RangeData(range_hexes=10, value=0),
        RangeData(range_hexes=15, value=1),
        RangeData(range_hexes=20, value=1),
        RangeData(range_hexes=30, value=1),
        RangeData(range_hexes=40, value=2),
        RangeData(range_hexes=80, value=4)
    ],
    minimum_arc=[
        RangeData(range_hexes=1, value=0.1),
        RangeData(range_hexes=2, value=0.2),
        RangeData(range_hexes=4, value=0.3),
        RangeData(range_hexes=6, value=0.5),
        RangeData(range_hexes=8, value=0.7),
        RangeData(range_hexes=10, value=0.8),
        RangeData(range_hexes=15, value=1.0),
        RangeData(range_hexes=20, value=2.0),
        RangeData(range_hexes=30, value=2.0),
        RangeData(range_hexes=40, value=3.0),
        RangeData(range_hexes=80, value=7.0)
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
    caliber=Caliber.CAL_556_NATO,
    weapon_type=WeaponType.ASSAULT_RIFLE,
    country=Country.SWITZERLAND,
    length_deployed=39,
    length_folded=30,
    reload_time=7,
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
    ballistic_data=sig_550_ballistic,
    built_in_bipod=True
)

# FN Mk 1 (Browning High-Power)
fn_mk1 = Weapon(
    name="FN Mk 1",
    weight=2.3,
    description="Automatic Pistol, 9mm Parabellum, Belgium, Browning High-Power pistol. "
                "Manufactured & sold world-wide.",
    caliber=Caliber.CAL_9MM_PARABELLUM,
    weapon_type=WeaponType.AUTOMATIC_PISTOL,
    country=Country.BELGIUM,
    length_deployed=8,
    reload_time=4,
    actions_to_cycle=None,
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
    caliber=Caliber.CAL_762X25,
    weapon_type=WeaponType.AUTOMATIC_PISTOL,
    country=Country.CHINA,
    length_deployed=8,
    reload_time=4,
    actions_to_cycle=None,
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
    caliber=Caliber.CAL_9MM_PARABELLUM,
    weapon_type=WeaponType.AUTOMATIC_PISTOL,
    country=Country.FRANCE,
    length_deployed=8,
    reload_time=4,
    actions_to_cycle=None,
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
    caliber=Caliber.CAL_32_ACP,
    weapon_type=WeaponType.AUTOMATIC_PISTOL,
    country=Country.WEST_GERMANY,
    length_deployed=6,
    reload_time=4,
    actions_to_cycle=None,
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

# Walther P1
walther_p1 = Weapon(
    name="Walther P1",
    weight=2.1,
    description="Current version of the WWII P38. Standard pistol of the West German army.",
    caliber=Caliber.CAL_9MM_PARABELLUM,
    weapon_type=WeaponType.AUTOMATIC_PISTOL,
    country=Country.WEST_GERMANY,
    length_deployed=9.0,
    reload_time=5,
    actions_to_cycle=None,
    self_loading_action=True,
    full_auto=False,
    ammo_capacity=8,
    ammo_weight=0.41,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=3,
    sustained_auto_burst=4,
    aim_time_modifiers={1: -17, 2: -11, 3: -10, 4: -9, 5: -8, 6: -7},
    ammunition_types=[ammo_9mm_v2_fmj, ammo_9mm_v2_jhp, ammo_9mm_v2_ap],
    ballistic_data=pistol_9mm_v2_ballistic
)

# HK P7M13
hk_p7m13 = Weapon(
    name="HK P7M13",
    weight=2.5,
    description="Modern pistol of innovative design used by the West German army and police.",
    caliber=Caliber.CAL_9MM_PARABELLUM,
    weapon_type=WeaponType.AUTOMATIC_PISTOL,
    country=Country.WEST_GERMANY,
    length_deployed=7.0,
    reload_time=3,
    actions_to_cycle=None,
    self_loading_action=True,
    full_auto=False,
    ammo_capacity=13,
    ammo_weight=0.63,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=3,
    sustained_auto_burst=4,
    aim_time_modifiers={1: -17, 2: -11, 3: -10, 4: -9, 5: -8, 6: -7},
    ammunition_types=[ammo_9mm_v2_fmj, ammo_9mm_v2_jhp, ammo_9mm_v2_ap],
    ballistic_data=pistol_9mm_v2_ballistic
)

# HK VP70M
hk_vp70m = Weapon(
    name="HK VP70M",
    weight=2.5,
    description="Late model pistol with three round burst capability when its shoulder stock is attached.",
    caliber=Caliber.CAL_9MM_PARABELLUM,
    weapon_type=WeaponType.AUTOMATIC_PISTOL,
    country=Country.WEST_GERMANY,
    length_deployed=21.0,
    length_folded=8.0,
    reload_time=5,
    actions_to_cycle=None,
    self_loading_action=True,
    full_auto=False,
    ammo_capacity=18,
    ammo_weight=0.69,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=3,
    sustained_auto_burst=4,
    aim_time_modifiers={1: -17, 2: -11, 3: -10, 4: -9, 5: -8, 6: -7},
    ammunition_types=[ammo_9mm_vp70_fmj, ammo_9mm_vp70_jhp, ammo_9mm_vp70_ap],
    ballistic_data=vp70m_ballistic
)

# Beretta M1951
m1951 = Weapon(
    name="M1951",
    weight=1.9,
    description="This Beretta pistol is used by the Italian & Israeli armies. It is also popular in the civilian market.",
    caliber=Caliber.CAL_9MM_PARABELLUM,
    weapon_type=WeaponType.AUTOMATIC_PISTOL,
    country=Country.ITALY,
    length_deployed=8.0,
    reload_time=5,
    actions_to_cycle=None,
    self_loading_action=True,
    full_auto=False,
    ammo_capacity=8,
    ammo_weight=0.40,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=3,
    sustained_auto_burst=4,
    aim_time_modifiers={1: -16, 2: -11, 3: -10, 4: -9, 5: -8, 6: -7},
    ammunition_types=[ammo_9mm_v2_fmj, ammo_9mm_v2_jhp, ammo_9mm_v2_ap],
    ballistic_data=pistol_9mm_v2_ballistic
)

# Beretta M93R
m93r = Weapon(
    name="M93R",
    weight=3.1,
    description="Beretta with three round burst capability. Issued to the Italian Special Forces.",
    caliber=Caliber.CAL_9MM_PARABELLUM,
    weapon_type=WeaponType.AUTOMATIC_PISTOL,
    country=Country.ITALY,
    length_deployed=9.0,
    reload_time=4,
    actions_to_cycle=None,
    self_loading_action=True,
    full_auto=False,
    ammo_capacity=20,
    ammo_weight=0.69,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=3,
    sustained_auto_burst=4,
    aim_time_modifiers={1: -18, 2: -11, 3: -10, 4: -9, 5: -8, 6: -7},
    ammunition_types=[ammo_9mm_m93r_fmj, ammo_9mm_m93r_jhp, ammo_9mm_m93r_ap],
    ballistic_data=m93r_ballistic,
    built_in_foregrip=True,
)

# M951R Machine Pistol
m951r = Weapon(
    name="M951R",
    weight=3.2,
    description="Modified large capacity M1951 with fully automatic fire capability.",
    caliber=Caliber.CAL_9MM_PARABELLUM,
    weapon_type=WeaponType.AUTOMATIC_PISTOL,
    country=Country.ITALY,
    length_deployed=7.0,
    reload_time=4,
    actions_to_cycle=None,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=6,
    ammo_capacity=10,
    ammo_weight=0.44,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=3,
    sustained_auto_burst=4,
    aim_time_modifiers={1: -18, 2: -12, 3: -10, 4: -9, 5: -8, 6: -7},
    ammunition_types=[ammo_9mm_m93r_fmj, ammo_9mm_m93r_jhp, ammo_9mm_m93r_ap],
    ballistic_data=m93r_ballistic
)

# SIG P226
sig_p226 = Weapon(
    name="SIG P226",
    weight=2.2,
    description="Well balanced, large capacity version of the SIG P220 with ambidextrous magazine catch.",
    caliber=Caliber.CAL_9MM_PARABELLUM,
    weapon_type=WeaponType.AUTOMATIC_PISTOL,
    country=Country.SWITZERLAND,
    length_deployed=8.0,
    reload_time=4,
    actions_to_cycle=None,
    self_loading_action=True,
    full_auto=False,
    ammo_capacity=15,
    ammo_weight=0.55,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=3,
    sustained_auto_burst=4,
    aim_time_modifiers={1: -17, 2: -11, 3: -10, 4: -9, 5: -8, 6: -7},
    ammunition_types=[ammo_9mm_v2_fmj, ammo_9mm_v2_jhp, ammo_9mm_v2_ap],
    ballistic_data=pistol_9mm_v2_ballistic
)

# Makarov PM
makarov_pm = Weapon(
    name="Makarov PM",
    weight=1.7,
    description="Dating back to the 1950s, this is still the standard pistol of the Soviet military.",
    caliber=Caliber.CAL_9X18_MAKAROV,
    weapon_type=WeaponType.AUTOMATIC_PISTOL,
    country=Country.USSR,
    length_deployed=6.0,
    reload_time=5,
    actions_to_cycle=None,
    self_loading_action=True,
    full_auto=False,
    ammo_capacity=8,
    ammo_weight=0.40,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=2,
    sustained_auto_burst=3,
    aim_time_modifiers={1: -16, 2: -11, 3: -10, 4: -9, 5: -8},
    ammunition_types=[ammo_9x18_fmj, ammo_9x18_jhp, ammo_9x18_ap],
    ballistic_data=makarov_ballistic
)

# 5.45 PSM
psm = Weapon(
    name="5.45 PSM",
    weight=1.1,
    description="Soviet pistol issued to internal security forces. It has an under-powered cartridge.",
    caliber=Caliber.CAL_545X18,
    weapon_type=WeaponType.AUTOMATIC_PISTOL,
    country=Country.USSR,
    length_deployed=6.0,
    reload_time=5,
    actions_to_cycle=None,
    self_loading_action=True,
    full_auto=False,
    ammo_capacity=8,
    ammo_weight=0.25,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=1,
    sustained_auto_burst=2,
    aim_time_modifiers={1: -15, 2: -11, 3: -10, 4: -9, 5: -8},
    ammunition_types=[ammo_545x18_fmj, ammo_545x18_jhp, ammo_545x18_ap],
    ballistic_data=psm_ballistic
)

# M92F
m92f = Weapon(
    name="M92F",
    weight=2.4,
    description="Beretta 9mm which has become extremely popular since its successes in U.S. military trials.",
    caliber=Caliber.CAL_9MM_PARABELLUM,
    weapon_type=WeaponType.AUTOMATIC_PISTOL,
    country=Country.USA,
    length_deployed=9.0,
    reload_time=4,
    actions_to_cycle=None,
    self_loading_action=True,
    full_auto=False,
    ammo_capacity=15,
    ammo_weight=0.60,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=3,
    sustained_auto_burst=4,
    aim_time_modifiers={1: -17, 2: -11, 3: -10, 4: -9, 5: -8, 6: -7},
    ammunition_types=[ammo_9mm_m92f_fmj, ammo_9mm_m92f_jhp, ammo_9mm_m92f_ap],
    ballistic_data=m92f_ballistic
)

# S&W M469
sw_m469 = Weapon(
    name="S&W M469",
    weight=1.9,
    description="Shortened version of the Smith and Wesson M459 designed for the US Air Force.",
    caliber=Caliber.CAL_9MM_PARABELLUM,
    weapon_type=WeaponType.AUTOMATIC_PISTOL,
    country=Country.USA,
    length_deployed=7.0,
    reload_time=4,
    actions_to_cycle=None,
    self_loading_action=True,
    full_auto=False,
    ammo_capacity=12,
    ammo_weight=0.50,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=3,
    sustained_auto_burst=4,
    aim_time_modifiers={1: -16, 2: -11, 3: -10, 4: -9, 5: -8},
    ammunition_types=[ammo_9mm_vp70_fmj, ammo_9mm_vp70_jhp, ammo_9mm_vp70_ap],
    ballistic_data=sw_m469_ballistic
)

m1911a1 = Weapon(
    name="M1911A1",
    weight=3.0,
    description="The Colt 45 Automatic Pistol has been the USA's standard military sidearm since WW I.",
    caliber=Caliber.CAL_45_ACP,
    weapon_type=WeaponType.AUTOMATIC_PISTOL,
    country=Country.USA,
    length_deployed=9.0,
    reload_time=4,
    actions_to_cycle=None,
    self_loading_action=True,
    full_auto=False,
    ammo_capacity=7,
    ammo_weight=0.70,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=5,
    sustained_auto_burst=5,
    aim_time_modifiers={1: -18, 2: -11, 3: -10, 4: -9, 5: -8, 6: -7},
    ammunition_types=[ammo_45_m1911_fmj, ammo_45_m1911_jhp, ammo_45_m1911_ap],
    ballistic_data=m1911a1_ballistic
)

m15 = Weapon(
    name="M15",
    weight=2.8,
    description="The M15 General Officers Pistol is a shortened version of the M1911A1.",
    caliber=Caliber.CAL_45_ACP,
    weapon_type=WeaponType.AUTOMATIC_PISTOL,
    country=Country.USA,
    length_deployed=8.0,
    reload_time=4,
    actions_to_cycle=None,
    self_loading_action=True,
    full_auto=False,
    ammo_capacity=7,
    ammo_weight=0.70,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=5,
    sustained_auto_burst=5,
    aim_time_modifiers={1: -18, 2: -11, 3: -10, 4: -9, 5: -8, 6: -7},
    ammunition_types=[ammo_45_m15_fmj, ammo_45_m15_jhp, ammo_45_m15_ap],
    ballistic_data=m15_ballistic
)

asp_9mm = Weapon(
    name="ASP 9mm",
    weight=1.4,
    description="Modified Smith & Wesson M39 with Guttersnipe sights intended for high level security.",
    caliber=Caliber.CAL_9MM_PARABELLUM,
    weapon_type=WeaponType.AUTOMATIC_PISTOL,
    country=Country.USA,
    length_deployed=7.0,
    reload_time=4,
    actions_to_cycle=None,
    self_loading_action=True,
    full_auto=False,
    ammo_capacity=7,
    ammo_weight=0.40,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=3,
    sustained_auto_burst=4,
    aim_time_modifiers={1: -16, 2: -12, 3: -10},
    ammunition_types=[ammo_9mm_v2_fmj, ammo_9mm_v2_jhp, ammo_9mm_v2_ap],
    ballistic_data=pistol_9mm_v2_ballistic
)

pa3_dm = Weapon(
    name="PA3-DM",
    weight=8.7,
    description="Standard Sub-Machinegun of the Argentine military.",
    caliber=Caliber.CAL_9MM_PARABELLUM,
    weapon_type=WeaponType.SUB_MACHINEGUN,
    country=Country.ARGENTINA,
    length_deployed=27.0,
    length_folded=21.0,
    reload_time=8,
    actions_to_cycle=None,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=5,
    ammo_capacity=25,
    ammo_weight=1.1,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=4,
    sustained_auto_burst=3,
    aim_time_modifiers={1: -23, 2: -12, 3: -9, 4: -8, 5: -6, 6: -5, 7: -4, 8: -3, 9: -2},
    ammunition_types=[ammo_9mm_pa3_fmj, ammo_9mm_pa3_jhp, ammo_9mm_pa3_ap],
    ballistic_data=pa3_ballistic
)

f1_smg = Weapon(
    name="F1",
    weight=8.6,
    description="Australian Sub-Machinegun unusual for its top loading magazine.",
    caliber=Caliber.CAL_9MM_PARABELLUM,
    weapon_type=WeaponType.SUB_MACHINEGUN,
    country=Country.AUSTRALIA,
    length_deployed=28.0,
    reload_time=9,
    actions_to_cycle=None,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=5,
    ammo_capacity=34,
    ammo_weight=1.4,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=3,
    sustained_auto_burst=3,
    aim_time_modifiers={1: -23, 2: -12, 3: -9, 4: -8, 5: -6, 6: -5, 7: -4, 8: -3, 9: -3, 10: -2},
    ammunition_types=[ammo_9mm_f1_fmj, ammo_9mm_f1_jhp, ammo_9mm_f1_ap],
    ballistic_data=f1_ballistic
)

steyr_mpi81 = Weapon(
    name="Steyr MPi 81",
    weight=7.8,
    description="Steyr SMG used by the police & military. Adopted by the Australian army.",
    caliber=Caliber.CAL_9MM_PARABELLUM,
    weapon_type=WeaponType.SUB_MACHINEGUN,
    country=Country.AUSTRIA,
    length_deployed=24.0,
    length_folded=17.0,
    reload_time=8,
    actions_to_cycle=None,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=6,
    ammo_capacity=32,
    ammo_weight=1.4,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=3,
    sustained_auto_burst=3,
    aim_time_modifiers={1: -22, 2: -12, 3: -9, 4: -7, 5: -6, 6: -5, 7: -4, 8: -3, 9: -2},
    ammunition_types=[ammo_9mm_mpi81_fmj, ammo_9mm_mpi81_jhp, ammo_9mm_mpi81_ap],
    ballistic_data=mpi81_ballistic
)

m61_skorpion = Weapon(
    name="M61 Skorpion",
    weight=4.4,
    description="The Skorpion SMP is intended for vehicular crews and heavily loaded infantry.",
    caliber=Caliber.CAL_32_ACP,
    weapon_type=WeaponType.SUB_MACHINEGUN,
    country=Country.CZECHOSLOVAKIA,
    length_deployed=20.0,
    length_folded=11.0,
    reload_time=7,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=7,
    ammo_capacity=20,
    ammo_weight=0.90,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=2,
    sustained_auto_burst=2,
    aim_time_modifiers={1: -19, 2: -11, 3: -8, 4: -7, 5: -6, 6: -5, 7: -4},
    ammunition_types=[ammo_32acp_m61_fmj, ammo_32acp_m61_jhp, ammo_32acp_m61_ap],
    ballistic_data=m61_ballistic
)

mat_49 = Weapon(
    name="MAT 49",
    weight=9.2,
    description="Well made weapon used by the French army and former colonies.",
    caliber=Caliber.CAL_9MM_PARABELLUM,
    weapon_type=WeaponType.SUB_MACHINEGUN,
    country=Country.FRANCE,
    length_deployed=28.0,
    length_folded=18.0,
    reload_time=8,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=5,
    ammo_capacity=32,
    ammo_weight=1.5,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=3,
    sustained_auto_burst=3,
    aim_time_modifiers={1: -23, 2: -12, 3: -9, 4: -8, 5: -6, 6: -5, 7: -4, 8: -3, 9: -2},
    ammunition_types=[ammo_9mm_mat49_fmj, ammo_9mm_mat49_jhp, ammo_9mm_mat49_ap],
    ballistic_data=mat49_ballistic
)

hk_mp5 = Weapon(
    name="Heckler & Koch MP5",
    weight=6.8,
    description="Widely exported SMG used by W German police & border guards.",
    caliber=Caliber.CAL_9MM_PARABELLUM,
    weapon_type=WeaponType.SUB_MACHINEGUN,
    country=Country.WEST_GERMANY,
    length_deployed=27.0,
    length_folded=19.0,
    reload_time=8,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=7,
    ammo_capacity=30,
    ammo_weight=1.2,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=4,
    sustained_auto_burst=3,
    aim_time_modifiers={1: -20, 2: -10, 3: -8, 4: -6, 5: -5, 6: -4, 7: -3, 8: -2, 9: -1},
    ammunition_types=[ammo_9mm_mp5_fmj, ammo_9mm_mp5_jhp, ammo_9mm_mp5_ap],
    ballistic_data=mp5_ballistic
)

hk_mp5k = Weapon(
    name="Heckler & Koch MP5K",
    weight=5.6,
    description="Short MP5 designed for anti-terrorist units.",
    caliber=Caliber.CAL_9MM_PARABELLUM,
    weapon_type=WeaponType.SUB_MACHINEGUN,
    country=Country.WEST_GERMANY,
    length_deployed=13.0,
    reload_time=7,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=8,
    ammo_capacity=30,
    ammo_weight=1.2,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=3,
    sustained_auto_burst=3,
    aim_time_modifiers={1: -19, 2: -11, 3: -10, 4: -9, 5: -8, 6: -7, 7: -6},
    ammunition_types=[ammo_9mm_mp5k_fmj, ammo_9mm_mp5k_jhp, ammo_9mm_mp5k_ap],
    ballistic_data=mp5k_ballistic,
    built_in_foregrip=True,
)

hk_53 = Weapon(
    name="Heckler & Koch 53",
    weight=8.1,
    description="Short version of the HK 33 which can be used as an SMG or rifle.",
    caliber=Caliber.CAL_556_NATO,
    weapon_type=WeaponType.SUB_MACHINEGUN,
    country=Country.WEST_GERMANY,
    length_deployed=30.0,
    length_folded=22.0,
    reload_time=8,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=6,
    ammo_capacity=40,
    ammo_weight=1.4,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=4,
    sustained_auto_burst=3,
    aim_time_modifiers={1: -21, 2: -11, 3: -8, 4: -7, 5: -5, 6: -4, 7: -3, 8: -2, 9: -1},
    ammunition_types=[ammo_556_hk53_fmj, ammo_556_hk53_jhp, ammo_556_hk53_ap],
    ballistic_data=hk53_ballistic
)

uzi = Weapon(
    name="Uzi",
    weight=9.0,
    description="Sturdy, reliable weapon popular with police and secret service.",
    caliber=Caliber.CAL_9MM_PARABELLUM,
    weapon_type=WeaponType.SUB_MACHINEGUN,
    country=Country.ISRAEL,
    length_deployed=26.0,
    length_folded=19.0,
    reload_time=8,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=5,
    ammo_capacity=32,
    ammo_weight=1.3,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=4,
    sustained_auto_burst=3,
    aim_time_modifiers={1: -23, 2: -12, 3: -9, 4: -8, 5: -6, 6: -5, 7: -4, 8: -3},
    ammunition_types=[ammo_9mm_uzi_fmj, ammo_9mm_uzi_jhp, ammo_9mm_uzi_ap],
    ballistic_data=uzi_ballistic
)

mini_uzi = Weapon(
    name="Mini Uzi",
    weight=7.3,
    description="Small version of the Uzi intended for police and security forces.",
    caliber=Caliber.CAL_9MM_PARABELLUM,
    weapon_type=WeaponType.SUB_MACHINEGUN,
    country=Country.ISRAEL,
    length_deployed=24.0,
    length_folded=14.0,
    reload_time=7,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=8,
    ammo_capacity=32,
    ammo_weight=1.3,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=3,
    sustained_auto_burst=3,
    aim_time_modifiers={1: -22, 2: -12, 3: -9, 4: -7, 5: -6, 6: -5, 7: -4, 8: -3},
    ammunition_types=[ammo_9mm_miniuzi_fmj, ammo_9mm_miniuzi_jhp, ammo_9mm_miniuzi_ap],
    ballistic_data=miniuzi_ballistic
)

beretta_m12s = Weapon(
    name="Beretta M12S",
    weight=8.4,
    description="Widely exported SMG used in Italy, Africa, and South America.",
    caliber=Caliber.CAL_9MM_PARABELLUM,
    weapon_type=WeaponType.SUB_MACHINEGUN,
    country=Country.ITALY,
    length_deployed=26.0,
    length_folded=17.0,
    reload_time=8,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=5,
    ammo_capacity=32,
    ammo_weight=1.3,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=3,
    sustained_auto_burst=3,
    aim_time_modifiers={1: -22, 2: -12, 3: -9, 4: -7, 5: -6, 6: -5, 7: -4, 8: -3},
    ammunition_types=[ammo_9mm_m12s_fmj, ammo_9mm_m12s_jhp, ammo_9mm_m12s_ap],
    ballistic_data=m12s_ballistic,
    built_in_foregrip=True,
)

spectre = Weapon(
    name="Spectre",
    weight=7.6,
    description="New SMG firing from a closed bolt using a four column magazine.",
    caliber=Caliber.CAL_9MM_PARABELLUM,
    weapon_type=WeaponType.SUB_MACHINEGUN,
    country=Country.ITALY,
    length_deployed=23.0,
    length_folded=14.0,
    reload_time=8,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=8,
    ammo_capacity=50,
    ammo_weight=1.6,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=4,
    sustained_auto_burst=3,
    aim_time_modifiers={1: -20, 2: -10, 3: -7, 4: -5, 5: -4, 6: -3, 7: -2, 8: -1},
    ammunition_types=[ammo_9mm_spectre_fmj, ammo_9mm_spectre_jhp, ammo_9mm_spectre_ap],
    ballistic_data=spectre_ballistic,
    built_in_foregrip=True,
)

armscor_bxp = Weapon(
    name="Armscor BXP",
    weight=6.3,
    description="Compact, light Sub-Machinegun which can be fired one handed.",
    caliber=Caliber.CAL_9MM_PARABELLUM,
    weapon_type=WeaponType.SUB_MACHINEGUN,
    country=Country.SOUTH_AFRICA,
    length_deployed=22.0,
    length_folded=14.0,
    reload_time=7,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=6,
    ammo_capacity=32,
    ammo_weight=1.2,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=3,
    sustained_auto_burst=3,
    aim_time_modifiers={1: -21, 2: -11, 3: -9, 4: -7, 5: -6, 6: -5, 7: -4, 8: -3},
    ammunition_types=[ammo_9mm_bxp_fmj, ammo_9mm_bxp_jhp, ammo_9mm_bxp_ap],
    ballistic_data=bxp_ballistic
)

aks74u = Weapon(
    name="AKS-74U",
    weight=7.3,
    description="SMG version of the AKS 74 rifle. In service with Soviet forces.",
    caliber=Caliber.CAL_545X39,
    weapon_type=WeaponType.CARBINE,
    country=Country.USSR,
    length_deployed=27.0,
    length_folded=17.0,
    reload_time=8,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=7,
    ammo_capacity=30,
    ammo_weight=1.3,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=3,
    sustained_auto_burst=3,
    aim_time_modifiers={1: -22, 2: -12, 3: -9, 4: -7, 5: -6, 6: -5, 7: -4, 8: -3},
    ammunition_types=[ammo_545_aks74u_fmj, ammo_545_aks74u_jhp, ammo_545_aks74u_ap],
    ballistic_data=aks74u_ballistic
)

sterling_mk7 = Weapon(
    name="Sterling Mk 7",
    weight=5.7,
    description="Special purpose paratroopers machine pistol.",
    caliber=Caliber.CAL_9MM_PARABELLUM,
    weapon_type=WeaponType.SUB_MACHINEGUN,
    country=Country.UK,
    length_deployed=14.0,
    reload_time=8,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=8,
    ammo_capacity=34,
    ammo_weight=1.2,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=3,
    sustained_auto_burst=3,
    aim_time_modifiers={1: -20, 2: -12, 3: -11, 4: -10, 5: -9, 6: -8, 7: -8, 8: -7},
    ammunition_types=[ammo_9mm_sterling_fmj, ammo_9mm_sterling_jhp, ammo_9mm_sterling_ap],
    ballistic_data=sterling_ballistic
)

ingram_mac10_9mm = Weapon(
    name="Ingram MAC 10 (9mm)",
    weight=7.6,
    description="Compact Sub-Machinegun chambered for 9mm Parabellum.",
    caliber=Caliber.CAL_9MM_PARABELLUM,
    weapon_type=WeaponType.SUB_MACHINEGUN,
    country=Country.USA,
    length_deployed=22.0,
    length_folded=11.0,
    reload_time=7,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=9,
    ammo_capacity=32,
    ammo_weight=1.4,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=3,
    sustained_auto_burst=3,
    aim_time_modifiers={1: -22, 2: -12, 3: -9, 4: -7, 5: -6, 6: -5, 7: -4, 8: -3},
    ammunition_types=[ammo_9mm_mac10_fmj, ammo_9mm_mac10_jhp, ammo_9mm_mac10_ap],
    ballistic_data=mac10_9mm_ballistic
)

ingram_mac10_45 = Weapon(
    name="Ingram MAC 10 (.45 ACP)",
    weight=8.4,
    description="MAC 10 chambered for 45 ACP. Its high recoil hinders one hand fire.",
    caliber=Caliber.CAL_45_ACP,
    weapon_type=WeaponType.SUB_MACHINEGUN,
    country=Country.USA,
    length_deployed=22.0,
    length_folded=11.0,
    reload_time=7,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=10,
    ammo_capacity=30,
    ammo_weight=2.2,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=5,
    sustained_auto_burst=4,
    aim_time_modifiers={1: -22, 2: -12, 3: -9, 4: -7, 5: -6, 6: -5, 7: -4, 8: -3},
    ammunition_types=[ammo_45acp_mac10_fmj, ammo_45acp_mac10_jhp, ammo_45acp_mac10_ap],
    ballistic_data=mac10_45_ballistic
)

bushmaster = Weapon(
    name="Bushmaster",
    weight=6.2,
    description="Powerful SMG designed for 1 hand fire braced against the forearm.",
    caliber=Caliber.CAL_556_NATO,
    weapon_type=WeaponType.CARBINE,
    country=Country.USA,
    length_deployed=21.0,
    reload_time=8,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=6,
    ammo_capacity=30,
    ammo_weight=1.0,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=4,
    sustained_auto_burst=3,
    aim_time_modifiers={1: -21, 2: -12, 3: -11, 4: -10, 5: -9, 6: -8},
    ammunition_types=[ammo_556_bushmaster_fmj, ammo_556_bushmaster_jhp, ammo_556_bushmaster_ap],
    ballistic_data=bushmaster_ballistic
)

steyr_aug = Weapon(
    name="Steyr AUG",
    weight=9.0,
    description="New Austrian rifle with an optical scope in its carrying handle.",
    caliber=Caliber.CAL_556_NATO,
    weapon_type=WeaponType.ASSAULT_RIFLE,
    country=Country.AUSTRIA,
    length_deployed=31.0,
    reload_time=10,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=5,
    ammo_capacity=30,
    ammo_weight=1.1,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=4,
    sustained_auto_burst=3,
    aim_time_modifiers={
        1: -23, 2: -12, 3: -8, 4: -6, 5: -5, 
        6: -4, 7: -3, 8: -2, 9: -1, 10: 0, 11: 1
    },
    ammunition_types=[ammo_556_aug_fmj, ammo_556_aug_jhp, ammo_556_aug_ap],
    ballistic_data=aug_ballistic,
    built_in_optics=True,
    built_in_foregrip=True,
)

l1a1_f1 = Weapon(
    name="L1A1 - F1",
    weight=12.0,
    description="Standard Australian army rifle patterned after the FN FAL. It is being replaced by the Austrian Steyr AUG.",
    caliber=Caliber.CAL_762_NATO,
    weapon_type=WeaponType.BATTLE_RIFLE,
    country=Country.AUSTRALIA,
    length_deployed=42.0,
    reload_time=8,
    self_loading_action=True,
    full_auto=False,
    ammo_capacity=20,
    ammo_weight=1.6,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=10,
    sustained_auto_burst=5,
    aim_time_modifiers={
        1: -24, 2: -14, 3: -10, 4: -8, 5: -6,
        6: -5, 7: -4, 8: -3, 9: -2, 10: -1, 11: 0
    },
    ammunition_types=[ammo_762_l1a1_fmj, ammo_762_l1a1_jhp, ammo_762_l1a1_ap],
    ballistic_data=l1a1_ballistic
)

fn_fal = Weapon(
    name="FN FAL",
    weight=10.8,
    description="Highly successful weapon exported to over 90 countries including the United Kingdom and Israel.",
    caliber=Caliber.CAL_762_NATO,
    weapon_type=WeaponType.BATTLE_RIFLE,
    country=Country.BELGIUM,
    length_deployed=43.0,
    reload_time=8,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=6,
    ammo_capacity=20,
    ammo_weight=1.4,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=10,
    sustained_auto_burst=5,
    aim_time_modifiers={
        1: -24, 2: -13, 3: -9, 4: -8, 5: -6,
        6: -5, 7: -4, 8: -3, 9: -2, 10: -1, 11: 0
    },
    ammunition_types=[ammo_762_fal_fmj, ammo_762_fal_jhp, ammo_762_fal_ap],
    ballistic_data=fal_ballistic
)

fn_fnc = Weapon(
    name="FN FNC",
    weight=9.6,
    description="Modern successor to the FN CAL. This weapon has three round burst capability and like the FN FAL has been marketed for export.",
    caliber=Caliber.CAL_556_NATO,
    weapon_type=WeaponType.ASSAULT_RIFLE,
    country=Country.BELGIUM,
    length_deployed=39.0,
    length_folded=30.0,
    reload_time=8,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=6,
    ammo_capacity=30,
    ammo_weight=1.2,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=4,
    sustained_auto_burst=3,
    aim_time_modifiers={
        1: -23, 2: -12, 3: -9, 4: -7, 5: -6, 6: -5, 7: -4, 8: -3, 9: -2, 10: -1, 11: 0
    },
    ammunition_types=[ammo_556_fnc_fmj, ammo_556_fnc_jhp, ammo_556_fnc_ap],
    ballistic_data=fnc_ballistic
)

m1949_56 = Weapon(
    name="M1949 - 56",
    weight=9.6,
    description="This French army rifle is still in service and is being replaced by the FA MAS. The FA MAS is currently only available to elite troops.",
    caliber=Caliber.CAL_75_FRENCH,
    weapon_type=WeaponType.BATTLE_RIFLE,
    country=Country.FRANCE,
    length_deployed=40.0,
    reload_time=8,
    self_loading_action=True,
    full_auto=False,
    ammo_capacity=10,
    ammo_weight=0.95,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=9,
    sustained_auto_burst=5,
    aim_time_modifiers={
        1: -23, 2: -12, 3: -9, 4: -7, 5: -6, 6: -5, 7: -4, 8: -3, 9: -2, 10: -1, 11: 0
    },
    ammunition_types=[ammo_75_m1949_fmj, ammo_75_m1949_jhp, ammo_75_m1949_ap],
    ballistic_data=m1949_ballistic
)

fa_mas = Weapon(
    name="FA MAS",
    weight=9.0,
    description="New French army rifle of lightweight, bullpup design.",
    caliber=Caliber.CAL_556_NATO,
    weapon_type=WeaponType.ASSAULT_RIFLE,
    country=Country.FRANCE,
    length_deployed=30.0,
    reload_time=10,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=8, # ROF is **8
    ammo_capacity=25,
    ammo_weight=1.0,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=4,
    sustained_auto_burst=3,
    aim_time_modifiers={
        1: -23, 2: -12, 3: -9, 4: -7, 5: -6, 6: -5, 7: -4, 8: -3, 9: -2, 10: -1, 11: 0
    },
    ammunition_types=[ammo_556_famas_fmj, ammo_556_famas_jhp, ammo_556_famas_ap],
    ballistic_data=famas_ballistic
)

fr_f2 = Weapon(
    name="FR F2",
    weight=12.5,
    description="French sniper rifle with optical scope and bipod chambered in 7.62mm NATO.",
    caliber=Caliber.CAL_762_NATO,
    weapon_type=WeaponType.SNIPER_RIFLE,
    country=Country.FRANCE,
    length_deployed=45.0,
    reload_time=8,
    self_loading_action=False,
    full_auto=False,
    actions_to_cycle=3,
    ammo_capacity=10,
    ammo_weight=1.1,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=10,
    sustained_auto_burst=5,
    aim_time_modifiers={1: -24, 2: -14, 3: -7, 4: -5, 5: -4, 6: -2, 7: 0, 8: 1, 9: 2, 10: 3, 12: 5},
    ammunition_types=[ammo_762_frf2_fmj, ammo_762_frf2_jhp, ammo_762_frf2_ap],
    ballistic_data=fr_f2_ballistic,
    built_in_optics=True,
    built_in_bipod=True,
)

hk_g3 = Weapon(
    name="Heckler & Koch G3",
    weight=11.1,
    description="Standard rifle of the West German army. It is also widely used in Africa and South America.",
    caliber=Caliber.CAL_762_NATO,
    weapon_type=WeaponType.BATTLE_RIFLE,
    country=Country.WEST_GERMANY,
    length_deployed=40.0,
    reload_time=8,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=5,
    ammo_capacity=20,
    ammo_weight=1.4,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=10,
    sustained_auto_burst=5,
    aim_time_modifiers={1: -24, 2: -14, 3: -9, 4: -8, 5: -6, 6: -5, 7: -4, 8: -3, 9: -2, 10: -1, 11: 0},
    ammunition_types=[ammo_762_g3_fmj, ammo_762_g3_jhp, ammo_762_g3_ap],
    ballistic_data=g3_ballistic
)

hk_g41 = Weapon(
    name="Heckler & Koch G41",
    weight=8.6,
    description="5.56mm NATO version of the G3. This weapon is considerably lighter than the G3 and has three round burst capability.",
    caliber=Caliber.CAL_556_NATO,
    weapon_type=WeaponType.ASSAULT_RIFLE,
    country=Country.WEST_GERMANY,
    length_deployed=39.0,
    reload_time=8,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=7,
    ammo_capacity=30,
    ammo_weight=1.1,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=4,
    sustained_auto_burst=3,
    aim_time_modifiers={1: -23, 2: -12, 3: -9, 4: -7, 5: -6, 6: -5, 7: -4, 8: -3, 9: -2, 10: -1, 11: 0},
    ammunition_types=[ammo_556_g41_fmj, ammo_556_g41_jhp, ammo_556_g41_ap],
    ballistic_data=g41_ballistic
)

hk_g11 = Weapon(
    name="Heckler & Koch G11",
    weight=8.7,
    description="Advanced caseless rifle under development.",
    caliber=Caliber.CAL_47_CASELESS,
    weapon_type=WeaponType.ASSAULT_RIFLE,
    country=Country.WEST_GERMANY,
    length_deployed=30.0,
    reload_time=10,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=5,
    ammo_capacity=50,
    ammo_weight=0.77,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=4,
    sustained_auto_burst=3,
    aim_time_modifiers={1: -23, 2: -12, 3: -8, 4: -6, 5: -5, 6: -4, 7: -3, 8: -2, 9: -1, 10: 0, 11: 1},
    ammunition_types=[ammo_47_g11_fmj, ammo_47_g11_jhp, ammo_47_g11_ap],
    ballistic_data=g11_ballistic,
    built_in_optics=True,
)

walther_2000 = Weapon(
    name="Walther 2000",
    weight=18.3,
    description="Specially designed sniper rifle with optical scope and bipod.",
    caliber=Caliber.CAL_300_WIN_MAG,
    weapon_type=WeaponType.SNIPER_RIFLE,
    country=Country.WEST_GERMANY,
    length_deployed=36.0,
    reload_time=10,
    self_loading_action=True,
    full_auto=False,
    ammo_capacity=6,
    ammo_weight=0.90,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=13,
    sustained_auto_burst=5,
    aim_time_modifiers={1: -26, 2: -16, 3: -8, 4: -6, 5: -4, 6: -3, 7: -1, 8: 0, 9: 1, 10: 2, 12: 5},
    ammunition_types=[ammo_300wm_wa2000_fmj, ammo_300wm_wa2000_jhp, ammo_300wm_wa2000_ap],
    ballistic_data=wa2000_ballistic,
    built_in_optics=True,
)

amd_65 = Weapon(
    name="AMD 65",
    weight=9.0,
    description="Hungarian modified AK 63 with folding stock and foregrip.",
    caliber=Caliber.CAL_762X39,
    weapon_type=WeaponType.CARBINE,
    country=Country.HUNGARY,
    length_deployed=34.0,
    length_folded=26.0,
    reload_time=8,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=5,
    ammo_capacity=30,
    ammo_weight=1.8,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=7,
    sustained_auto_burst=4,
    aim_time_modifiers={1: -23, 2: -13, 3: -9, 4: -7, 5: -6, 6: -4, 7: -3, 8: -2},
    ammunition_types=[ammo_762x39_amd65_fmj, ammo_762x39_amd65_jhp, ammo_762x39_amd65_ap],
    ballistic_data=amd65_ballistic,
    built_in_foregrip=True,
)

galil_ar_556 = Weapon(
    name="Galil AR 5.56mm",
    weight=10.2,
    description="Galil Assault Rifle in 5.56mm NATO.",
    caliber=Caliber.CAL_556_NATO,
    weapon_type=WeaponType.ASSAULT_RIFLE,
    country=Country.ISRAEL,
    length_deployed=39.0,
    length_folded=29.0,
    reload_time=8,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=5,
    ammo_capacity=35,
    ammo_weight=1.6,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=4,
    sustained_auto_burst=3,
    aim_time_modifiers={1: -23, 2: -13, 3: -9, 4: -7, 5: -6, 6: -5, 7: -4, 8: -3, 9: -2, 10: -1, 11: 0},
    ammunition_types=[ammo_556_galil_fmj, ammo_556_galil_jhp, ammo_556_galil_ap],
    ballistic_data=galil_556_ballistic
)

galil_ar_762 = Weapon(
    name="Galil AR 7.62mm",
    weight=10.7,
    description="Galil Assault Rifle in 7.62mm NATO. This weapon & the 5.56mm version are also available in a Short Assault Rifle (SAR) variant.",
    caliber=Caliber.CAL_762_NATO,
    weapon_type=WeaponType.BATTLE_RIFLE,
    country=Country.ISRAEL,
    length_deployed=41.0,
    length_folded=32.0,
    reload_time=8,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=5,
    ammo_capacity=25,
    ammo_weight=2.0,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=10,
    sustained_auto_burst=5,
    aim_time_modifiers={1: -24, 2: -13, 3: -9, 4: -7, 5: -6, 6: -5, 7: -4, 8: -3, 9: -2, 10: -1, 11: 0},
    ammunition_types=[ammo_762_galil_fmj, ammo_762_galil_jhp, ammo_762_galil_ap],
    ballistic_data=galil_762_ballistic
)

beretta_bm59 = Weapon(
    name="Beretta BM 59",
    weight=11.3,
    description="Standard rifle of the Italian army. Similar to the M1 Garand.",
    caliber=Caliber.CAL_762_NATO,
    weapon_type=WeaponType.BATTLE_RIFLE,
    country=Country.ITALY,
    length_deployed=43.0,
    reload_time=8,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=6,
    ammo_capacity=20,
    ammo_weight=1.5,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=10,
    sustained_auto_burst=5,
    aim_time_modifiers={1: -24, 2: -14, 3: -9, 4: -8, 5: -6, 6: -5, 7: -4, 8: -3, 9: -2, 10: -1, 11: 0},
    ammunition_types=[ammo_762_beretta_bm59_fmj, ammo_762_beretta_bm59_jhp, ammo_762_beretta_bm59_ap],
    ballistic_data=beretta_bm59_ballistic,
    built_in_bipod=True,
)

beretta_sc70 = Weapon(
    name="Beretta SC 70",
    weight=9.3,
    description="Folding stock version of the Beretta AR 70 rifle.",
    caliber=Caliber.CAL_556_NATO,
    weapon_type=WeaponType.ASSAULT_RIFLE,
    country=Country.ITALY,
    length_deployed=38.0,
    length_folded=29.0,
    reload_time=8,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=5,
    ammo_capacity=30,
    ammo_weight=1.1,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=4,
    sustained_auto_burst=3,
    aim_time_modifiers={1: -23, 2: -12, 3: -9, 4: -7, 5: -6, 6: -5, 7: -4, 8: -3, 9: -2, 10: -1, 11: 0},
    ammunition_types=[ammo_556_sc70_fmj, ammo_556_sc70_jhp, ammo_556_sc70_ap],
    ballistic_data=sc70_ballistic
)

type_64 = Weapon(
    name="Type 64",
    weight=11.3,
    description="Standard rifle of the Japanese army using a reduced load 7.62mm round.",
    caliber=Caliber.CAL_762_NATO,
    weapon_type=WeaponType.BATTLE_RIFLE,
    country=Country.JAPAN,
    length_deployed=39.0,
    reload_time=8,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=4,
    ammo_capacity=20,
    ammo_weight=1.6,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=8,
    sustained_auto_burst=5,
    aim_time_modifiers={1: -24, 2: -14, 3: -9, 4: -8, 5: -6, 6: -5, 7: -4, 8: -3, 9: -2, 10: -1, 11: 0},
    ammunition_types=[ammo_762_type64_fmj, ammo_762_type64_jhp, ammo_762_type64_ap],
    ballistic_data=type64_ballistic,
    built_in_bipod=True,
)

r4 = Weapon(
    name="R4",
    weight=11.2,
    description="Modified Galil AR. South African Defense Force's standard rifle.",
    caliber=Caliber.CAL_556_NATO,
    weapon_type=WeaponType.ASSAULT_RIFLE,
    country=Country.SOUTH_AFRICA,
    length_deployed=40.0,
    length_folded=29.0,
    reload_time=8,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=5,
    ammo_capacity=35,
    ammo_weight=1.8,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=4,
    sustained_auto_burst=3,
    aim_time_modifiers={1: -24, 2: -14, 3: -9, 4: -7, 5: -6, 6: -5, 7: -4, 8: -3, 9: -2, 10: -1},
    ammunition_types=[ammo_556_r4_fmj, ammo_556_r4_jhp, ammo_556_r4_ap],
    ballistic_data=r4_ballistic,
    built_in_bipod=True,
)

akm = Weapon(
    name="AKM 47",
    weight=8.7,
    description="New model AK 47. The most widely exported communist weapon.",
    caliber=Caliber.CAL_762X39,
    weapon_type=WeaponType.ASSAULT_RIFLE,
    country=Country.USSR,
    length_deployed=35.0,
    reload_time=8,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=5,
    ammo_capacity=30,
    ammo_weight=1.8,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=7,
    sustained_auto_burst=5,
    aim_time_modifiers={1: -23, 2: -12, 3: -9, 4: -7, 5: -6, 6: -4, 7: -3, 8: -2, 9: -1},
    ammunition_types=[ammo_762x39_akm_fmj, ammo_762x39_akm_jhp, ammo_762x39_akm_ap],
    ballistic_data=akm_ballistic,
)

ak_74 = Weapon(
    name="AK 74",
    weight=8.7,
    description="New Soviet rifle with an effective muzzle brake. It is replacing the AKM 47.",
    caliber=Caliber.CAL_545X39,
    weapon_type=WeaponType.ASSAULT_RIFLE,
    country=Country.USSR,
    length_deployed=37.0,
    reload_time=8,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=5,
    ammo_capacity=30,
    ammo_weight=1.1,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=4,
    sustained_auto_burst=2,
    aim_time_modifiers={1: -23, 2: -12, 3: -9, 4: -7, 5: -6, 6: -4, 7: -3, 8: -2, 9: -1},
    ammunition_types=[ammo_545x39_ak74_fmj, ammo_545x39_ak74_jhp, ammo_545x39_ak74_ap],
    ballistic_data=ak74_ballistic,
)

dragunov_svd = Weapon(
    name="Dragunov SVD",
    weight=10.2,
    description="The Dragunov is equipped with a PSO-1 4x optical sight whose reticle is illuminated by a small battery. The scope is capable of detecting an infra-red source.",
    caliber=Caliber.CAL_762X54R,
    weapon_type=WeaponType.SNIPER_RIFLE,
    country=Country.USSR,
    length_deployed=48.0,
    reload_time=8,
    self_loading_action=True,
    full_auto=False,
    ammo_capacity=10,
    ammo_weight=0.68,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=12,
    sustained_auto_burst=6,
    aim_time_modifiers={1: -22, 2: -12, 3: -7, 4: -5, 5: -4, 6: -2, 7: 0, 8: 1, 9: 2, 10: 3, 11: 4},
    ammunition_types=[ammo_762x54_svd_fmj, ammo_762x54_svd_jhp, ammo_762x54_svd_ap],
    ballistic_data=svd_ballistic,
    built_in_optics=True,
)

l1a1 = Weapon(
    name="L1A1",
    weight=11.0,
    description="Patterned on the FN FAL, the L1A1 is the standard British service rifle. Normally a semi-automatic weapon, it can easily be modified for fully automatic fire.",
    caliber=Caliber.CAL_762_NATO,
    weapon_type=WeaponType.BATTLE_RIFLE,
    country=Country.UK,
    length_deployed=45.0,
    reload_time=8,
    self_loading_action=True,
    full_auto=False,
    ammo_capacity=20,
    ammo_weight=1.5,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=10,
    sustained_auto_burst=5,
    aim_time_modifiers={1: -24, 2: -14, 3: -9, 4: -8, 5: -6, 6: -5, 7: -4, 8: -3, 9: -2, 10: -1, 11: 0},
    ammunition_types=[ammo_762nato_l1a1_fmj, ammo_762nato_l1a1_jhp, ammo_762nato_l1a1_ap],
    ballistic_data=l1a1_ballistic,
)

enfield_iw = Weapon(
    name="Enfield IW",
    weight=9.2,
    description="New British rifle replacing the L1A1.",
    caliber=Caliber.CAL_556_NATO,
    weapon_type=WeaponType.ASSAULT_RIFLE,
    country=Country.UK,
    length_deployed=31.0,
    reload_time=10,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=6,
    ammo_capacity=30,
    ammo_weight=1.0,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=4,
    sustained_auto_burst=3,
    aim_time_modifiers={1: -23, 2: -12, 3: -8, 4: -6, 5: -5, 6: -4, 7: -3, 8: -2, 9: -1, 10: 0, 11: 1},
    ammunition_types=[ammo_556nato_enfield_fmj, ammo_556nato_enfield_jhp, ammo_556nato_enfield_ap],
    ballistic_data=enfield_iw_ballistic,
)

m14 = Weapon(
    name="M 14",
    weight=11.2,
    description="Standard US army rifle adopted in 1957. The M14 was often replaced by the M16 starting in 1962 but remains in service. Most notably with the US Marine Corp.", #
    caliber=Caliber.CAL_762_NATO,
    weapon_type=WeaponType.BATTLE_RIFLE,
    country=Country.USA,
    length_deployed=44.0,
    reload_time=8,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=6,
    ammo_capacity=20,
    ammo_weight=1.5,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=10,
    sustained_auto_burst=5,
    aim_time_modifiers={1:-24, 2:-14, 3:-10, 4:-8, 5:-6, 6:-5, 7:-4, 8:-3, 9:-2, 10:-1, 12:0},
    ammunition_types=[ammo_762nato_m14_fmj, ammo_762nato_m14_jhp, ammo_762nato_m14_ap],
    ballistic_data=m14_ballistic,
)

m16a1 = Weapon(
    name="M16A1",
    weight=8.0,
    description="Standard US army rifle adopted in 1962, it was used extensively in Vietnam.",
    caliber=Caliber.CAL_556_NATO,
    weapon_type=WeaponType.ASSAULT_RIFLE,
    country=Country.USA,
    length_deployed=39.0,
    reload_time=8,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=7,
    ammo_capacity=30,
    ammo_weight=1.0,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=4,
    sustained_auto_burst=3,
    aim_time_modifiers={1:-22, 2:-12, 3:-9, 4:-7, 5:-6, 6:-5, 7:-4, 8:-3, 9:-2, 10:-1, 11:0},
    ammunition_types=[ammo_556nato_m16a1_fmj, ammo_556nato_m16a1_jhp, ammo_556nato_m16a1_ap],
    ballistic_data=m16a1_ballistic,
)

xm177 = Weapon(
    name="XM177",
    weight=7.1,
    description="Shortened M16 with folding stock often used by officers and NCOs.",
    caliber=Caliber.CAL_556_NATO,
    weapon_type=WeaponType.CARBINE,
    country=Country.USA,
    length_deployed=31.0,
    length_folded=28.0,
    reload_time=8,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=7,
    ammo_capacity=30,
    ammo_weight=1.0,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=4,
    sustained_auto_burst=3,
    aim_time_modifiers={1:-22, 2:-11, 3:-9, 4:-7, 5:-5, 6:-4, 7:-3, 8:-2, 9:-1},
    ammunition_types=[ammo_556nato_xm177_fmj, ammo_556nato_xm177_jhp, ammo_556nato_xm177_ap],
    ballistic_data=xm177_ballistic,
)

m16a2 = Weapon(
    name="M16A2",
    weight=8.5,
    description="Late version of the M16A1 with three round burst capability.", #
    caliber=Caliber.CAL_556_NATO,
    weapon_type=WeaponType.ASSAULT_RIFLE,
    country=Country.USA,
    length_deployed=39.0,
    reload_time=8,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=7,
    ammo_capacity=30,
    ammo_weight=1.0,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=4,
    sustained_auto_burst=3,
    aim_time_modifiers={1: -22, 2: -12, 3: -9, 4: -7, 5: -6, 6: -5, 7: -4, 8: -3, 9: -2, 10: -1, 11: 0},
    ammunition_types=[ammo_556nato_m16a2_fmj, ammo_556nato_m16a2_jhp, ammo_556nato_m16a2_ap],
    ballistic_data=m16a2_ballistic,
)

m16a1_m203 = Weapon(
    name="M16A1 with M203",
    weight=11.6,
    description="M16A1 with 40mm grenade launcher. It replaced the M79 grenade launcher.", #
    caliber=Caliber.CAL_556_NATO,
    weapon_type=WeaponType.ASSAULT_RIFLE,
    country=Country.USA,
    length_deployed=39.0,
    reload_time=8,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=7,
    ammo_capacity=30,
    ammo_weight=1.0,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=4,
    sustained_auto_burst=3,
    aim_time_modifiers={1: -25, 2: -15, 3: -9, 4: -8, 5: -6, 6: -5, 7: -4, 8: -3, 9: -2, 10: -1, 11: 0},
    ammunition_types=[ammo_556nato_m16a1_fmj, ammo_556nato_m16a1_jhp, ammo_556nato_m16a1_ap],
    ballistic_data=m16a1_ballistic,
)

m40a1 = Weapon(
    name="M40A1",
    weight=14.8,
    description="Remington bolt action rifle with heavy barrel and USMC 10x sniper scope. This is the standard sniper's weapon of the US Marine Corps.",
    caliber=Caliber.CAL_762_NATO,
    weapon_type=WeaponType.SNIPER_RIFLE,
    country=Country.USA,
    length_deployed=44.0,
    reload_time=16,
    self_loading_action=False,
    full_auto=False,
    actions_to_cycle=3,
    ammo_capacity=5,
    ammo_weight=0.06,
    ammo_feed_device=AmmoFeedDevice.ROUND,
    knock_down=10,
    sustained_auto_burst=5,
    aim_time_modifiers={1: -25, 2: -15, 3: -8, 4: -6, 5: -4, 6: -3, 7: -1, 8: 1, 9: 2, 10: 3, 11: 4, 12: 4},
    ammunition_types=[ammo_762nato_m40a1_fmj, ammo_762nato_m40a1_jhp, ammo_762nato_m40a1_ap],
    ballistic_data=m40a1_ballistic,
    built_in_optics=True
)

steyr_lsw = Weapon(
    name="Steyr LSW",
    weight=12.3,
    description="Light Support Weapon version of the Army Universal Gun.",
    caliber=Caliber.CAL_556_NATO,
    weapon_type=WeaponType.LIGHT_MACHINE_GUN,
    country=Country.AUSTRIA,
    length_deployed=35.0,
    reload_time=8,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=6,
    ammo_capacity=42,
    ammo_weight=1.5,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=4,
    sustained_auto_burst=2,
    aim_time_modifiers={1: -24, 2: -14, 3: -8, 4: -6, 5: -5, 6: -4, 7: -3, 8: -2, 9: -1, 10: 0, 12: 1},
    ammunition_types=[ammo_556nato_steyr_fmj, ammo_556nato_steyr_jhp, ammo_556nato_steyr_ap],
    ballistic_data=steyr_lsw_ballistic,
    built_in_bipod=True,
)

fn_mag = Weapon(
    name="FN MAG",
    weight=27.2,
    description="Reliable weapon considered one of the best GPMGs made.",
    caliber=Caliber.CAL_762_NATO,
    weapon_type=WeaponType.MACHINE_GUN,
    country=Country.BELGIUM,
    length_deployed=50.0,
    reload_time=12,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=6,
    ammo_capacity=50,
    ammo_weight=3.2,
    ammo_feed_device=AmmoFeedDevice.BELT,
    knock_down=10,
    sustained_auto_burst=3,
    aim_time_modifiers={1: -29, 2: -19, 3: -13, 4: -9, 5: -8, 6: -6, 7: -5, 8: -4, 10: -2, 12: -1, 14: 1},
    ammunition_types=[ammo_762nato_fnmag_fmj, ammo_762nato_fnmag_jhp, ammo_762nato_fnmag_ap],
    ballistic_data=fn_mag_ballistic,
    built_in_bipod=True,
)

type_67 = Weapon(
    name="Type 67",
    weight=27.7,
    description="Chinese designed machine gun adopted in the early 1970s.",
    caliber=Caliber.CAL_762X54R,
    weapon_type=WeaponType.MACHINE_GUN,
    country=Country.CHINA,
    length_deployed=45.0,
    reload_time=12,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=5,
    ammo_capacity=100,
    ammo_weight=5.8,
    ammo_feed_device=AmmoFeedDevice.BELT,
    knock_down=12,
    sustained_auto_burst=4,
    aim_time_modifiers={1: -29, 2: -20, 3: -13, 4: -9, 5: -8, 6: -6, 7: -5, 8: -4, 9: -3, 10: -2, 12: 0},
    ammunition_types=[ammo_762x54_type67_fmj, ammo_762x54_type67_jhp, ammo_762x54_type67_ap],
    ballistic_data=type_67_ballistic,
    built_in_bipod=True,
)

aa_762 = Weapon(
    name="AA 7.62",
    weight=28.5,
    description="Standard MG of the French army. AA 52 converted to 7.62mm NATO.",
    caliber=Caliber.CAL_762_NATO,
    weapon_type=WeaponType.MACHINE_GUN,
    country=Country.FRANCE,
    length_deployed=45.0,
    length_folded=39.0,
    reload_time=12,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=6,
    ammo_capacity=100,
    ammo_weight=6.5,
    ammo_feed_device=AmmoFeedDevice.BELT,
    knock_down=10,
    sustained_auto_burst=3,
    aim_time_modifiers={1: -30, 2: -20, 3: -14, 4: -9, 5: -8, 6: -6, 7: -5, 8: -4, 9: -3, 10: -2, 12: 0},
    ammunition_types=[ammo_762nato_aa762_fmj, ammo_762nato_aa762_jhp, ammo_762nato_aa762_ap],
    ballistic_data=aa_762_ballistic,
    built_in_bipod=True,
)

hk_13e = Weapon(
    name="Heckler & Koch 13E",
    weight=18.7,
    description="Squad Automatic Weapon version of the HK 13 LMG.",
    caliber=Caliber.CAL_556_NATO,
    weapon_type=WeaponType.LIGHT_MACHINE_GUN,
    country=Country.WEST_GERMANY,
    length_deployed=41.0,
    reload_time=8,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=6,
    ammo_capacity=30,
    ammo_weight=1.1,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=4,
    sustained_auto_burst=2,
    aim_time_modifiers={1: -27, 2: -17, 3: -11, 4: -8, 5: -7, 6: -6, 7: -4, 8: -3, 9: -3, 10: -2, 12: 0},
    ammunition_types=[ammo_556nato_hk13e_fmj, ammo_556nato_hk13e_jhp, ammo_556nato_hk13e_ap],
    ballistic_data=hk_13e_ballistic,
    built_in_bipod=True,
)

hk_11e = Weapon(
    name="Heckler & Koch 11E",
    weight=19.5,
    description="Squad Automatic Weapon variant of the HK 11A1 LMG.",
    caliber=Caliber.CAL_762_NATO,
    weapon_type=WeaponType.MACHINE_GUN,
    country=Country.WEST_GERMANY,
    length_deployed=41.0,
    reload_time=8,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=7,
    ammo_capacity=20,
    ammo_weight=1.5,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=10,
    sustained_auto_burst=4,
    aim_time_modifiers={1: -27, 2: -17, 3: -11, 4: -9, 5: -7, 6: -6, 7: -5, 8: -4, 9: -3, 10: -2, 12: 0},
    ammunition_types=[ammo_762nato_hk11e_fmj, ammo_762nato_hk11e_jhp, ammo_762nato_hk11e_ap],
    ballistic_data=hk_11e_ballistic,
    built_in_bipod=True,
)

hk_23e = Weapon(
    name="Heckler & Koch 23E",
    weight=25.5,
    description="New version of the HK 21A1 in 5.56mm NATO.",
    caliber=Caliber.CAL_556_NATO,
    weapon_type=WeaponType.LIGHT_MACHINE_GUN,
    country=Country.WEST_GERMANY,
    length_deployed=41.0,
    reload_time=12,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=6,
    ammo_capacity=200,
    ammo_weight=6.2,
    ammo_feed_device=AmmoFeedDevice.BELT,
    knock_down=4,
    sustained_auto_burst=2,
    aim_time_modifiers={1: -29, 2: -19, 3: -12, 4: -9, 5: -7, 6: -6, 7: -5, 8: -4, 9: -3, 10: -2, 12: 0},
    ammunition_types=[ammo_556nato_hk23e_fmj, ammo_556nato_hk23e_jhp, ammo_556nato_hk23e_ap],
    ballistic_data=hk_23e_ballistic,
    built_in_bipod=True,
)

hk_21e = Weapon(
    name="Heckler & Koch 21E",
    weight=27.0,
    description="Newest version of the HK 21A1.",
    caliber=Caliber.CAL_762_NATO,
    weapon_type=WeaponType.MACHINE_GUN,
    country=Country.WEST_GERMANY,
    length_deployed=45.0,
    reload_time=12,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=7,
    ammo_capacity=100,
    ammo_weight=6.5,
    ammo_feed_device=AmmoFeedDevice.BELT,
    knock_down=10,
    sustained_auto_burst=3,
    aim_time_modifiers={1: -29, 2: -19, 3: -13, 4: -9, 5: -8, 6: -6, 7: -5, 8: -4, 9: -3, 10: -2, 12: 0},
    ammunition_types=[ammo_762nato_hk21e_fmj, ammo_762nato_hk21e_jhp, ammo_762nato_hk21e_ap],
    ballistic_data=hk_21e_ballistic,
    built_in_bipod=True,
)

mg3 = Weapon(
    name="MG3",
    weight=30.9,
    description="The MG3 is based on the World War II MG42.",
    caliber=Caliber.CAL_762_NATO,
    weapon_type=WeaponType.MACHINE_GUN,
    country=Country.WEST_GERMANY,
    length_deployed=48.0,
    reload_time=12,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=10,
    ammo_capacity=100,
    ammo_weight=6.5,
    ammo_feed_device=AmmoFeedDevice.BELT,
    knock_down=10,
    sustained_auto_burst=3,
    aim_time_modifiers={1: -30, 2: -20, 3: -14, 4: -10, 5: -8, 6: -6, 7: -5, 8: -4, 9: -3, 10: -2, 11: -1},
    ammunition_types=[ammo_762nato_mg3_fmj, ammo_762nato_mg3_jhp, ammo_762nato_mg3_ap],
    ballistic_data=mg3_ballistic,
    built_in_bipod=True,
)

galil_arm = Weapon(
    name="Galil ARM",
    weight=11.5,
    description="SAW version of the Galil Assault Rifle & light Machine gun (ARM).",
    caliber=Caliber.CAL_556_NATO,
    weapon_type=WeaponType.LIGHT_MACHINE_GUN,
    country=Country.ISRAEL,
    length_deployed=39.0,
    length_folded=29.0,
    reload_time=8,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=5,
    ammo_capacity=50,
    ammo_weight=2.2,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=4,
    sustained_auto_burst=2,
    aim_time_modifiers={1: -24, 2: -14, 3: -9, 4: -8, 5: -6, 6: -5, 7: -4, 8: -3, 9: -2, 10: -1, 11: 0},
    ammunition_types=[ammo_556nato_galil_fmj, ammo_556nato_galil_jhp, ammo_556nato_galil_ap],
    ballistic_data=galil_arm_ballistic,
    built_in_bipod=True,
)

beretta_m70_78 = Weapon(
    name="Beretta M70-78",
    weight=13.4,
    description="Squad Automatic Weapon based on the AR70 rifle.",
    caliber=Caliber.CAL_556_NATO,
    weapon_type=WeaponType.LIGHT_MACHINE_GUN,
    country=Country.ITALY,
    length_deployed=38.0,
    reload_time=8,
    full_auto_rof=6,
    ammo_capacity=40,
    ammo_weight=1.7,
    knock_down=4,
    sustained_auto_burst=2,
    aim_time_modifiers={1: -25, 2: -15, 3: -10, 4: -8, 5: -6, 6: -5, 7: -4, 8: -3, 9: -2, 10: -1, 11: 0},
    ammunition_types=[ammo_556nato_beretta_fmj, ammo_556nato_beretta_jhp, ammo_556nato_beretta_ap],
    ballistic_data=beretta_m70_78_ballistic,
    built_in_bipod=True,
)

rpk_74 = Weapon(
    name="RPK 74",
    weight=11.4,
    description="Squad Automatic Weapon version of the AK 74 rifle.",
    caliber=Caliber.CAL_545X39,
    weapon_type=WeaponType.LIGHT_MACHINE_GUN,
    country=Country.USSR,
    length_deployed=45.0,
    reload_time=8,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=5,
    ammo_capacity=40,
    ammo_weight=1.5,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=4,
    sustained_auto_burst=2,
    aim_time_modifiers={1: -24, 2: -14, 3: -10, 4: -8, 5: -6, 6: -5, 7: -4, 8: -3, 9: -2, 10: -1, 11: 0},
    ammunition_types=[ammo_545sov_rpk74_fmj, ammo_545sov_rpk74_jhp, ammo_545sov_rpk74_ap],
    ballistic_data=rpk_74_ballistic,
    built_in_bipod=True,
)

rpk_762 = Weapon(
    name="RPK",
    weight=15.7,
    description="This SAW has replaced the RPD in the Soviet arsenal.",
    caliber=Caliber.CAL_762X39,
    weapon_type=WeaponType.LIGHT_MACHINE_GUN,
    country=Country.USSR,
    length_deployed=41.0,
    reload_time=10,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=6,
    ammo_capacity=75,
    ammo_weight=4.6,
    ammo_feed_device=AmmoFeedDevice.DRUM,
    knock_down=7,
    sustained_auto_burst=3,
    aim_time_modifiers={1: -26, 2: -16, 3: -10, 4: -8, 5: -7, 6: -5, 7: -4, 8: -3, 9: -2, 10: -1, 12: 0},
    ammunition_types=[ammo_762sov_rpk_fmj, ammo_762sov_rpk_jhp, ammo_762sov_rpk_ap],
    ballistic_data=rpk_762_ballistic,
    built_in_bipod=True,
)

rp_46 = Weapon(
    name="RP 46",
    weight=43.0,
    description="Developed in 1946, it is still in service in the third world.",
    caliber=Caliber.CAL_762X54R,
    weapon_type=WeaponType.MACHINE_GUN,
    country=Country.USSR,
    length_deployed=51.0,
    reload_time=12,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=5,
    ammo_capacity=250,
    ammo_weight=14.3,
    ammo_feed_device=AmmoFeedDevice.BELT,
    knock_down=12,
    sustained_auto_burst=3,
    aim_time_modifiers={1: -32, 2: -22, 3: -17, 4: -11, 5: -9, 6: -7, 7: -6, 8: -5, 9: -4, 11: -2, 13: 0},
    ammunition_types=[ammo_762R_rp46_fmj, ammo_762R_rp46_jhp, ammo_762R_rp46_ap],
    ballistic_data=rp_46_ballistic,
    built_in_bipod=True,
)

rpd = Weapon(
    name="RPD",
    weight=22.0,
    description="Obsolete in the Soviet army, it is still found in Africa and Asia.",
    caliber=Caliber.CAL_762X39,
    weapon_type=WeaponType.LIGHT_MACHINE_GUN,
    country=Country.USSR,
    length_deployed=41.0,
    reload_time=14,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=6,
    ammo_capacity=100,
    ammo_weight=5.3,
    ammo_feed_device=AmmoFeedDevice.DRUM,
    knock_down=7,
    sustained_auto_burst=2,
    aim_time_modifiers={1: -28, 2: -18, 3: -11, 4: -9, 5: -7, 6: -6, 7: -5, 8: -4, 9: -3, 10: -2, 12: 0},
    ammunition_types=[ammo_762sov_rpd_fmj, ammo_762sov_rpd_jhp, ammo_762sov_rpd_ap],
    ballistic_data=rpd_ballistic,
    built_in_bipod=True,
)

pkm = Weapon(
    name="PKM",
    weight=25.5,
    description="Standard LMG in the Soviet army. It has replaced the RP 46.",
    caliber=Caliber.CAL_762X54R,
    weapon_type=WeaponType.LIGHT_MACHINE_GUN,
    country=Country.USSR,
    length_deployed=46.0,
    reload_time=12,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=6,
    ammo_capacity=100,
    ammo_weight=5.7,
    ammo_feed_device=AmmoFeedDevice.BELT,
    knock_down=12,
    sustained_auto_burst=4,
    aim_time_modifiers={1: -29, 2: -19, 3: -12, 4: -9, 5: -7, 6: -6, 7: -5, 8: -4, 9: -3, 10: -2, 12: 0},
    ammunition_types=[ammo_762R_pkm_fmj, ammo_762R_pkm_jhp, ammo_762R_pkm_ap],
    ballistic_data=pkm_ballistic,
    built_in_bipod=True,
)

nsv = Weapon(
    name="NSV",
    weight=116.0,
    description="Developed in 1969. Used as heavy ground support, air defense, and tank air defense weapon.",
    caliber=Caliber.CAL_127X107,
    weapon_type=WeaponType.HEAVY_MACHINE_GUN,
    country=Country.USSR,
    length_deployed=61.0,
    reload_time=14,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=6,
    ammo_capacity=50,
    ammo_weight=17.0,
    ammo_feed_device=AmmoFeedDevice.BELT,
    knock_down=49,
    sustained_auto_burst=3,
    aim_time_modifiers={1: -33, 2: -23, 3: -16, 4: -12, 5: -8, 6: -6, 7: -4, 8: -2, 10: 0, 12: 1, 16: 4},
    ammunition_types=[ammo_127sov_nsv_fmj, ammo_127sov_nsv_jhp, ammo_127sov_nsv_ap],
    ballistic_data=nsv_ballistic,
    built_in_bipod=True,
)

enfield_lsw = Weapon(
    name="Enfield LSW",
    weight=15.2,
    description="Squad Automatic Weapon variant of the Enfield IW rifle.",
    caliber=Caliber.CAL_556_NATO,
    weapon_type=WeaponType.LIGHT_MACHINE_GUN,
    country=Country.UK,
    length_deployed=35.0,
    reload_time=10,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=6,
    ammo_capacity=30,
    ammo_weight=1.0,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=4,
    sustained_auto_burst=2,
    aim_time_modifiers={1: -26, 2: -16, 3: -9, 4: -7, 5: -6, 6: -4, 7: -3, 8: -2, 9: -1, 10: 0, 12: 2},
    ammunition_types=[ammo_556nato_lsw_fmj, ammo_556nato_lsw_jhp, ammo_556nato_lsw_ap],
    ballistic_data=enfield_lsw_ballistic,
    built_in_bipod=True,
)

bren_l4 = Weapon(
    name="Bren L4",
    weight=23.6,
    description="L4 series Bren gun in 7.62mm NATO. Used by all British forces.",
    caliber=Caliber.CAL_762_NATO,
    weapon_type=WeaponType.MACHINE_GUN,
    country=Country.UK,
    length_deployed=45.0,
    reload_time=8,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=4,
    ammo_capacity=30,
    ammo_weight=2.6,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=10,
    sustained_auto_burst=3,
    aim_time_modifiers={1: -28, 2: -19, 3: -12, 4: -9, 5: -7, 6: -6, 7: -5, 8: -4, 9: -3, 11: -1, 13: 1},
    ammunition_types=[ammo_762nato_bren_fmj, ammo_762nato_bren_jhp, ammo_762nato_bren_ap],
    ballistic_data=bren_l4_ballistic,
    built_in_bipod=True,
)

l7a2 = Weapon(
    name="L7A2",
    weight=32.8,
    description="Based on the FN MAG, the L7A2 is the standard GPMG of the British army.",
    caliber=Caliber.CAL_762_NATO,
    weapon_type=WeaponType.MACHINE_GUN,
    country=Country.UK,
    length_deployed=49.0,
    reload_time=12,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=7,
    ammo_capacity=100,
    ammo_weight=6.5,
    ammo_feed_device=AmmoFeedDevice.BELT,
    knock_down=10,
    sustained_auto_burst=3,
    aim_time_modifiers={1: -31, 2: -21, 3: -15, 4: -10, 5: -8, 6: -7, 7: -5, 8: -4, 10: -3, 12: -1, 15: 1},
    ammunition_types=[ammo_762nato_l7a2_fmj, ammo_762nato_l7a2_jhp, ammo_762nato_l7a2_ap],
    ballistic_data=l7a2_ballistic,
    built_in_bipod=True,
)

m249_minimi = Weapon(
    name="M249 Minimi",
    weight=22.0,
    description="Belgium designed Squad Automatic Weapon adopted by the US army.",
    caliber=Caliber.CAL_556_NATO,
    weapon_type=WeaponType.LIGHT_MACHINE_GUN,
    country=Country.USA,
    length_deployed=41.0,
    reload_time=14,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=7,
    ammo_capacity=200,
    ammo_weight=6.9,
    ammo_feed_device=AmmoFeedDevice.BELT,
    knock_down=4,
    sustained_auto_burst=2,
    aim_time_modifiers={1: -28, 2: -18, 3: -11, 4: -9, 5: -7, 6: -6, 7: -4, 8: -3, 9: -2, 10: -1, 12: 0},
    ammunition_types=[ammo_556nato_m249_fmj, ammo_556nato_m249_jhp, ammo_556nato_m249_ap],
    ballistic_data=m249_minimi_ballistic,
    built_in_bipod=True,
)

m60 = Weapon(
    name="M60",
    weight=29.7,
    description="Adopted in the 1950s, this is the standard GPMG of US forces.",
    caliber=Caliber.CAL_762_NATO,
    weapon_type=WeaponType.MACHINE_GUN,
    country=Country.USA,
    length_deployed=44.0,
    reload_time=12,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=5,
    ammo_capacity=100,
    ammo_weight=6.5,
    ammo_feed_device=AmmoFeedDevice.BELT,
    knock_down=10,
    sustained_auto_burst=3,
    aim_time_modifiers={1: -30, 2: -20, 3: -14, 4: -10, 5: -8, 6: -6, 7: -5, 8: -4, 9: -3, 10: -2, 12: 0},
    ammunition_types=[ammo_762nato_m60_fmj, ammo_762nato_m60_jhp, ammo_762nato_m60_ap],
    ballistic_data=m60_ballistic,
    built_in_bipod=True,
)

m60e3 = Weapon(
    name="M60E3",
    weight=25.5,
    description="Light version of the M60 adopted by the US Navy and Marine Corps.",
    caliber=Caliber.CAL_762_NATO,
    weapon_type=WeaponType.MACHINE_GUN,
    country=Country.USA,
    length_deployed=42.0,
    reload_time=12,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=5,
    ammo_capacity=100,
    ammo_weight=6.5,
    ammo_feed_device=AmmoFeedDevice.BELT,
    knock_down=10,
    sustained_auto_burst=4,
    aim_time_modifiers={1: -29, 2: -19, 3: -12, 4: -9, 5: -7, 6: -6, 7: -5, 8: -4, 9: -3, 10: -2, 12: 0},
    ammunition_types=[ammo_762nato_m60e3_fmj, ammo_762nato_m60e3_jhp, ammo_762nato_m60e3_ap],
    ballistic_data=m60e3_ballistic,
    built_in_bipod=True,
)

m2hb = Weapon(
    name="M2HB",
    weight=157.5,
    description="Standard US Heavy Machine Gun in service since 1933.",
    caliber=Caliber.CAL_50_BMG,
    weapon_type=WeaponType.HEAVY_MACHINE_GUN,
    country=Country.USA,
    length_deployed=65.0,
    reload_time=14,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=5,
    ammo_capacity=105,
    ammo_weight=28.8,
    ammo_feed_device=AmmoFeedDevice.BELT,
    knock_down=45,
    sustained_auto_burst=2,
    aim_time_modifiers={1: -37, 2: -27, 3: -21, 4: -17, 5: -14, 6: -10, 7: -8, 8: -6, 10: -4, 12: -2, 14: 0},
    ammunition_types=[ammo_50bmg_m2hb_fmj, ammo_50bmg_m2hb_jhp, ammo_50bmg_m2hb_ap],
    ballistic_data=m2hb_ballistic,
    built_in_bipod=True,
)

spas12 = Weapon(
    name="Franchi SPAS 12",
    weight=10.1,
    description="Special Purpose Automatic Shotgun for police and military.",
    caliber=Caliber.CAL_12_GAUGE,
    weapon_type=WeaponType.SHOTGUN,
    country=Country.ITALY,
    length_deployed=37.0,
    length_folded=28.0,
    reload_time=30,
    self_loading_action=True,
    ammo_capacity=7,
    ammo_weight=0.13,
    ammo_feed_device=AmmoFeedDevice.ROUND,
    knock_down=23,
    sustained_auto_burst=10,
    aim_time_modifiers={1: -23, 2: -13, 3: -9, 4: -7, 5: -6, 6: -4, 7: -3, 8: -2, 9: -1},
    ammunition_types=[ammo_12g_spas_aps, ammo_12g_spas_shot],
    ballistic_data=spas12_ballistic
)

caws = Weapon(
    name="Olin - Heckler & Koch CAWS",
    weight=11.6,
    description="Close Assault Weapon System uses a belted brass cartridge.",
    caliber=Caliber.CAL_12_GAUGE,
    weapon_type=WeaponType.SHOTGUN,
    country=Country.USA,
    length_deployed=30.0,
    reload_time=8,
    self_loading_action=True,
    ammo_capacity=10,
    ammo_weight=2.1,
    ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=23,
    sustained_auto_burst=10,
    aim_time_modifiers={1: -24, 2: -14, 3: -9, 4: -7, 5: -5, 6: -4, 7: -3, 8: -2, 9: -1, 10: 0, 11: 1, 12: 2},
    ammunition_types=[ammo_12g_caws_slug, ammo_12g_caws_shot],
    ballistic_data=caws_ballistic
)

mossberg_bullpup = Weapon(
    name="Mossberg Bullpup 12",
    weight=9.4,
    description="Mossberg 500 action in a military style stock.",
    caliber=Caliber.CAL_12_GAUGE,
    weapon_type=WeaponType.SHOTGUN,
    country=Country.USA,
    length_deployed=31.0,
    reload_time=34,
    self_loading_action=False,
    actions_to_cycle=2,
    ammo_capacity=8,
    ammo_weight=0.13,
    ammo_feed_device=AmmoFeedDevice.ROUND,
    knock_down=24,
    sustained_auto_burst=11,
    aim_time_modifiers={1: -23, 2: -12, 3: -9, 4: -7, 5: -6, 6: -5, 7: -4, 8: -3, 9: -2, 10: -1},
    ammunition_types=[ammo_12g_mossberg_slug, ammo_12g_mossberg_shot],
    ballistic_data=mossberg_ballistic
)

remington_m870 = Weapon(
    name="Remington M870",
    weight=8.8,
    description="US Marine Corps version of the Remington Model 870. Adopted in 1966 with M7 bayonet mounting lug.",
    caliber=Caliber.CAL_12_GAUGE,
    weapon_type=WeaponType.SHOTGUN,
    country=Country.USA,
    length_deployed=42.0,
    reload_time=30,
    self_loading_action=False,
    actions_to_cycle=2,
    ammo_capacity=7,
    ammo_weight=0.13,
    ammo_feed_device=AmmoFeedDevice.ROUND,
    knock_down=25,
    sustained_auto_burst=12,
    aim_time_modifiers={1: -23, 2: -12, 3: -9, 4: -7, 5: -6, 6: -4, 7: -3, 8: -2},
    ammunition_types=[ammo_12g_remington_slug, ammo_12g_remington_shot],
    ballistic_data=remington_ballistic
)

high_standard_m10b = Weapon(
    name="High Standard M10B",
    weight=9.5,
    description="Compact shotgun for police tactical teams.",
    caliber=Caliber.CAL_12_GAUGE,
    weapon_type=WeaponType.SHOTGUN,
    country=Country.USA,
    length_deployed=27.0,
    reload_time=22,
    self_loading_action=True,
    ammo_capacity=5,
    ammo_weight=0.13,
    ammo_feed_device=AmmoFeedDevice.ROUND,
    knock_down=23,
    sustained_auto_burst=10,
    aim_time_modifiers={1: -23, 2: -12, 3: -9, 4: -7, 5: -6, 6: -4, 7: -3, 8: -2},
    ammunition_types=[ammo_12g_high_standard_slug, ammo_12g_high_standard_shot],
    ballistic_data=remington_ballistic
)

atchisson_assault_12 = Weapon(
    name="Atchisson Assault 12",
    weight=16.1,
    description="Fully automatic, high capacity, drum fed shotgun. Very few were produced and it has not been adopted by any military.",
    caliber=Caliber.CAL_12_GAUGE,
    weapon_type=WeaponType.SHOTGUN,
    country=Country.USA,
    length_deployed=39.0,
    reload_time=14,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=4,
    ammo_capacity=20,
    ammo_weight=4.6,
    ammo_feed_device=AmmoFeedDevice.DRUM,
    knock_down=23,
    sustained_auto_burst=8,
    aim_time_modifiers={
        1: -26, 2: -16, 3: -10, 4: -8, 5: -7, 6: -5, 7: -4, 8: -3, 9: -2, 10: -1, 11: -1, 12: 0
    },
    ammunition_types=[ammo_12g_atchisson_slug, ammo_12g_atchisson_shot],
    ballistic_data=atchisson_ballistic
)

hk_69a1 = Weapon(
    name="H & K 69A1",
    weight=4.1,
    description="Compact grenade launcher with folding stock. Single shot, break-action design.",
    caliber=Caliber.CAL_40x46MM,
    weapon_type=WeaponType.GRENADE_LAUNCHER,
    country=Country.WEST_GERMANY,
    length_folded=18,
    length_deployed=27,
    reload_time=10,
    self_loading_action=False,
    ammo_capacity=1,
    ammo_weight=0.51,
    ammo_feed_device=AmmoFeedDevice.ROUND,
    ammunition_types=[ammo_40mm_heat_standard, ammo_40mm_he_hk],
    sustained_auto_burst=11,
    aim_time_modifiers={
        1: -19, 2: -10, 3: -8, 4: -6, 5: -5, 6: -4, 7: -3
    },
    ballistic_data=WeaponBallisticData(
        angle_of_impact=[
            RangeData(40, 0),
            RangeData(100, 1),
            RangeData(200, 4),
        ],
        ballistic_accuracy=[
            RangeData(40, 23),
            RangeData(100, 10),
            RangeData(200, 1),
        ],
        time_of_flight=[
            RangeData(40, 11),
            RangeData(100, 33),
            RangeData(200, 80),
        ],
    ),
)

hk_79 = Weapon(
    name="H & K 79",
    weight=14.9,
    description="Under-barrel grenade launcher for G3 or G41 rifles. Barrel drops down for loading.",
    caliber=Caliber.CAL_40x46MM,
    weapon_type=WeaponType.GRENADE_LAUNCHER,
    country=Country.WEST_GERMANY,
    length_deployed=40,
    reload_time=12,
    self_loading_action=False,
    ammo_capacity=1,
    ammo_weight=0.51,
    ammo_feed_device=AmmoFeedDevice.ROUND,
    ammunition_types=[ammo_40mm_heat_standard, ammo_40mm_he_hk],
    sustained_auto_burst=7,
    aim_time_modifiers={
        1: -26, 2: -16, 3: -10, 4: -7, 5: -6, 6: -4
    },
    ballistic_data=WeaponBallisticData(
        angle_of_impact=[
            RangeData(40, 0),
            RangeData(100, 1),
            RangeData(200, 4),
        ],
        ballistic_accuracy=[
            RangeData(40, 23),
            RangeData(100, 10),
            RangeData(200, 1),
        ],
        time_of_flight=[
            RangeData(40, 11),
            RangeData(100, 33),
            RangeData(200, 80),
        ],
    ),
)

armscor_6 = Weapon(
    name="Armscor 6",
    weight=15.0,
    description="Six shot semi-automatic grenade launcher using a revolver type feed. Provided with collimating sight.",
    caliber=Caliber.CAL_40x46MM,
    weapon_type=WeaponType.GRENADE_LAUNCHER,
    country=Country.SOUTH_AFRICA,
    length_folded=22,
    length_deployed=31,
    reload_time=24,
    self_loading_action=True,
    ammo_capacity=6,
    ammo_weight=0.51,
    ammo_feed_device=AmmoFeedDevice.ROUND,
    ammunition_types=[ammo_40mm_heat_standard, ammo_40mm_he_armscor],
    sustained_auto_burst=7,
    aim_time_modifiers={
        1: -26, 2: -16, 3: -10, 4: -8, 5: -6, 6: -5, 7: -3
    },
    ballistic_data=WeaponBallisticData(
        angle_of_impact=[
            RangeData(40, 0),
            RangeData(100, 1),
            RangeData(200, 4),
        ],
        ballistic_accuracy=[
            RangeData(40, 23),
            RangeData(100, 10),
            RangeData(200, 1),
        ],
        time_of_flight=[
            RangeData(40, 11),
            RangeData(100, 33),
            RangeData(200, 80),
        ],
    ),
    built_in_optics=True,
)


ak74_gp = Weapon(
    name="AK 74 with 30mm Grenade Launcher",
    weight=10.1,
    description="AK 74 rifle with 30mm grenade launcher (GP-type). Similar to US M203.",
    caliber=Caliber.CAL_30MM_VOG,
    weapon_type=WeaponType.GRENADE_LAUNCHER,
    country=Country.USSR,
    length_deployed=37,
    reload_time=12,
    self_loading_action=False,
    ammo_capacity=1,
    ammo_weight=0.56,
    ammo_feed_device=AmmoFeedDevice.ROUND,
    ammunition_types=[ammo_30mm_he_ak],
    sustained_auto_burst=8,
    aim_time_modifiers={
        1: -23, 2: -13, 3: -9, 4: -7, 5: -5
    },
    ballistic_data=WeaponBallisticData(
        angle_of_impact=[RangeData(40, 0), RangeData(100, 1), RangeData(200, 4)],
        ballistic_accuracy=[RangeData(40, 23), RangeData(100, 5), RangeData(200, -4)],
        time_of_flight=[RangeData(40, 11), RangeData(100, 35), RangeData(200, 81)],
    ),
)

ags_17 = Weapon(
    name="AGS-17 Plamya",
    weight=140.5,
    description="Automatic 30mm grenade launcher on tripod. Introduced in 1975.",
    caliber=Caliber.CAL_30MM_VOG,
    weapon_type=WeaponType.AUTOMATIC_GRENADE_LAUNCHER,
    country=Country.USSR,
    length_deployed=33,
    reload_time=12,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=1,
    ammo_capacity=29,
    ammo_weight=24.0,
    ammo_feed_device=AmmoFeedDevice.DRUM,
    ammunition_types=[ammo_30mm_he_ags],
    sustained_auto_burst=1,
    aim_time_modifiers={
        1: -38, 2: -28, 3: -22, 4: -18, 5: -15, 6: -10, 7: -8, 8: -6, 9: -5, 10: -4, 11: -3, 12: -2, 13: -1
    },
    ballistic_data=WeaponBallisticData(
        angle_of_impact=[RangeData(40, 0), RangeData(100, 0), RangeData(200, 0), RangeData(400, 1)],
        minimum_arc=[RangeData(40, 0.2), RangeData(100, 0.4), RangeData(200, 0.8), RangeData(400, 2.0)],
        ballistic_accuracy=[RangeData(40, 32), RangeData(100, 19), RangeData(200, 9), RangeData(400, 0)],
        time_of_flight=[RangeData(40, 4), RangeData(100, 11), RangeData(200, 24), RangeData(400, 57)],
    ),
    built_in_bipod=True,
)


m79 = Weapon(
    name="M79 Grenade Launcher",
    weight=6.5,
    description="Single-shot breech-loading 40mm grenade launcher.",
    caliber=Caliber.CAL_40x46MM,
    weapon_type=WeaponType.GRENADE_LAUNCHER,
    country=Country.USA,
    length_deployed=29,
    reload_time=10,
    self_loading_action=False,
    ammo_capacity=1,
    ammo_weight=0.51,
    ammo_feed_device=AmmoFeedDevice.ROUND,
    ammunition_types=[ammo_40mm_heat, ammo_40mm_he],
    sustained_auto_burst=11,
    aim_time_modifiers={
        1: -21, 2: -11, 3: -8, 4: -7, 5: -5, 6: -4, 7: -3
    },
    ballistic_data=WeaponBallisticData(
        angle_of_impact=[
            RangeData(40, 0),
            RangeData(100, 1),
            RangeData(200, 4),
        ],
        ballistic_accuracy=[
            RangeData(40, 23),
            RangeData(100, 10),
            RangeData(200, 1),
        ],
        time_of_flight=[
            RangeData(40, 11),
            RangeData(100, 33),
            RangeData(200, 80),
        ],
    ),
)

m203 = Weapon(
    name="M203 Grenade Launcher",
    weight=11.6,
    description="Single-shot slide-action 40mm launcher mounted under M16.",
    caliber=Caliber.CAL_40x46MM,
    weapon_type=WeaponType.GRENADE_LAUNCHER,
    country=Country.USA,
    length_deployed=39,
    reload_time=12,
    self_loading_action=False,
    ammo_capacity=1,
    ammo_weight=0.51,
    ammo_feed_device=AmmoFeedDevice.ROUND,
    ammunition_types=[ammo_40mm_heat, ammo_40mm_he],
    sustained_auto_burst=8,
    aim_time_modifiers={
        1: -24, 2: -14, 3: -9, 4: -7, 5: -6, 6: -4
    },
    ballistic_data=WeaponBallisticData(
        angle_of_impact=[
            RangeData(40, 0),
            RangeData(100, 1),
            RangeData(200, 4),
        ],
        ballistic_accuracy=[
            RangeData(40, 23),
            RangeData(100, 10),
            RangeData(200, 1),
        ],
        time_of_flight=[
            RangeData(40, 11),
            RangeData(100, 33),
            RangeData(200, 80),
        ],
    ),
)

m174 = Weapon(
    name="M174 Automatic Grenade Launcher",
    weight=40.8,
    description="Automatic 40mm grenade launcher on tripod.",
    caliber=Caliber.CAL_40x46MM,
    weapon_type=WeaponType.AUTOMATIC_GRENADE_LAUNCHER,
    country=Country.USA,
    length_deployed=28,
    reload_time=14,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=3,
    ammo_capacity=12,
    ammo_weight=9.9,
    ammo_feed_device=AmmoFeedDevice.DRUM,
    ammunition_types=[ammo_40mm_heat, ammo_40mm_he],
    sustained_auto_burst=4,
    built_in_bipod=True,
    ballistic_data=WeaponBallisticData(
        angle_of_impact=[
            RangeData(40, 0),
            RangeData(100, 1),
            RangeData(200, 4),
        ],
        minimum_arc=[
            RangeData(40, 7),
            RangeData(100, 2),
            RangeData(200, 4),
        ],
        ballistic_accuracy=[
            RangeData(40, 23),
            RangeData(100, 10),
            RangeData(200, 1),
        ],
        time_of_flight=[
            RangeData(40, 11),
            RangeData(100, 33),
            RangeData(200, 80),
        ],
    ),
)

m19 = Weapon(
    name="M19 Automatic Grenade Launcher",
    weight=137.2,
    description="Automatic 40mm grenade launcher (Mk 19). Uses its own longer 40mm grenades.",
    caliber=Caliber.CAL_40x53MM,
    weapon_type=WeaponType.AUTOMATIC_GRENADE_LAUNCHER,
    country=Country.USA,
    length_deployed=41,
    reload_time=14,
    self_loading_action=True,
    full_auto=True,
    full_auto_rof=3,
    ammo_capacity=50,
    ammo_weight=45.2,
    ammo_feed_device=AmmoFeedDevice.BELT,
    ammunition_types=[ammo_40mm_heat_hv, ammo_40mm_he_hv],
    sustained_auto_burst=4,
    aim_time_modifiers={
        1: -40, 2: -30, 3: -25, 4: -21, 5: -17, 6: -15, 7: -10, 8: -8, 9: -6, 10: -5, 11: -3
    },
    ballistic_data=WeaponBallisticData(
        angle_of_impact=[RangeData(40, 0), RangeData(100, 0), RangeData(200, 0), RangeData(400, 1)],
        minimum_arc=[RangeData(40, 0.8), RangeData(100, 2.0), RangeData(200, 4.0), RangeData(400, 8.0)],
        ballistic_accuracy=[RangeData(40, 27), RangeData(100, 14), RangeData(200, 5), RangeData(400, -4)],
        time_of_flight=[RangeData(40, 3), RangeData(100, 9), RangeData(200, 21), RangeData(400, 52)],
    ),
    built_in_bipod=True,
)

pzf_44 = Weapon(
    name="PZF 44 2A1 Lanze",
    weight=22.7,
    description="Reloadable RPG launcher similar to Soviet RPG 7V.",
    caliber=Caliber.CAL_66MM,
    weapon_type=WeaponType.ROCKET_PROPELLED_GRENADE_LAUNCHER,
    country=Country.WEST_GERMANY,
    length_folded=35,
    length_deployed=46,
    reload_time=28,
    self_loading_action=False,
    ammo_capacity=1,
    ammo_weight=5.5,
    ammo_feed_device=AmmoFeedDevice.ROUND,
    ammunition_types=[ammo_66mm_heat_pzf44, ammo_66mm_he_pzf44],
    aim_time_modifiers={
        1: -28, 2: -18, 3: -11, 4: -9, 5: -7, 6: -6, 7: -4, 8: -3, 9: -2, 10: -1
    },
    ballistic_data=WeaponBallisticData(
        angle_of_impact=[RangeData(40, 0), RangeData(100, 0), RangeData(200, 0), RangeData(400, 1)],
        ballistic_accuracy=[RangeData(40, 14), RangeData(100, 2), RangeData(200, -7), RangeData(400, -17)],
        time_of_flight=[RangeData(40, 4), RangeData(100, 9), RangeData(200, 20), RangeData(400, 45)]
    )
)

armbrust = Weapon(
    name="Armbrust",
    weight=16.0,
    description="One-shot disposable rocket launcher with counter-mass for recoilless effect.",
    caliber=Caliber.CAL_67MM,
    weapon_type=WeaponType.ROCKET_PROPELLED_GRENADE,
    country=Country.WEST_GERMANY,
    length_deployed=34,
    reload_time=14,
    self_loading_action=False,
    ammo_capacity=1,
    ammo_weight=16.0,
    ammo_feed_device=AmmoFeedDevice.ROUND,
    ammunition_types=[ammo_67mm_heat_armbrust, ammo_67mm_he_armbrust],
    aim_time_modifiers={
        1: -26, 2: -16, 3: -10, 4: -8, 5: -6, 6: -5, 7: -4, 8: -3, 9: -2, 10: -1
    },
    ballistic_data=WeaponBallisticData(
        angle_of_impact=[RangeData(40, 0), RangeData(100, 0), RangeData(200, 0), RangeData(400, 1)],
        ballistic_accuracy=[RangeData(40, 12), RangeData(100, -1), RangeData(200, -10), RangeData(400, -20)],
        time_of_flight=[RangeData(40, 4), RangeData(100, 10), RangeData(200, 21), RangeData(400, 50)]
    )
)

rpg_18 = Weapon(
    name="RPG 18",
    weight=14.3,
    description="Disposable 64mm anti-tank rocket launcher similar to US M72 LAW.",
    caliber=Caliber.CAL_64MM,
    weapon_type=WeaponType.ROCKET_PROPELLED_GRENADE,
    country=Country.USSR,
    length_folded=28,
    length_deployed=39,
    reload_time=20,
    self_loading_action=False,
    ammo_capacity=1,
    ammo_weight=16.0,
    ammo_feed_device=AmmoFeedDevice.ROUND,
    ammunition_types=[ammo_64mm_heat_rpg18],
    ballistic_data=WeaponBallisticData(
        angle_of_impact=[RangeData(40, 0), RangeData(100, 0), RangeData(200, 1), RangeData(400, 2)],
        ballistic_accuracy=[RangeData(40, 16), RangeData(100, 5), RangeData(200, -5), RangeData(400, -14)],
        time_of_flight=[RangeData(40, 7), RangeData(100, 17), RangeData(200, 36), RangeData(400, 78)]
    )
)

rpg_7v = Weapon(
    name="RPG 7V",
    weight=20.4,
    description="Standard man-portable anti-tank weapon of the Soviet army. Reload time assumes propellant charge is pre-screwed.",
    caliber=Caliber.CAL_85MM,
    weapon_type=WeaponType.ROCKET_PROPELLED_GRENADE_LAUNCHER,
    country=Country.USSR,
    length_folded=39,
    length_deployed=54,
    reload_time=15,
    self_loading_action=False,
    ammo_capacity=1,
    ammo_weight=5.0,
    ammo_feed_device=AmmoFeedDevice.ROUND,
    ammunition_types=[ammo_85mm_heat_rpg7, ammo_85mm_he_rpg7],
    aim_time_modifiers={
        1: -28, 2: -18, 3: -11, 4: -9, 5: -7, 6: -6, 7: -5, 8: -4, 9: -3, 10: -2, 11: -1, 12: 0
    },
    ballistic_data=WeaponBallisticData(
        ballistic_accuracy=[RangeData(40, 15), RangeData(100, 4), RangeData(200, -6), RangeData(400, -15)],
        time_of_flight=[RangeData(40, 2), RangeData(100, 6), RangeData(200, 14), RangeData(400, 30)],
    ),
)

law_80 = Weapon(
    name="LAW 80",
    weight=21.2,
    description="One-shot disposable weapon with built-in 9mm spotting rifle (5 round capacity).",
    caliber=Caliber.CAL_94MM,
    weapon_type=WeaponType.ROCKET_PROPELLED_GRENADE,
    country=Country.UK,
    length_folded=39,
    length_deployed=59,
    reload_time=20,
    self_loading_action=False,
    ammo_capacity=1,
    ammo_weight=21.2,
    ammo_feed_device=AmmoFeedDevice.ROUND,
    ammunition_types=[ammo_94mm_heat_law80],
    aim_time_modifiers={
        1: -28, 2: -18, 3: -11, 4: -9, 5: -7, 6: -5, 7: -4, 8: -3, 9: -2, 10: -1
    },
    ballistic_data=WeaponBallisticData(
        angle_of_impact=[RangeData(40, 0), RangeData(100, 0), RangeData(200, 1), RangeData(400, 2)],
        ballistic_accuracy=[RangeData(40, 8), RangeData(100, -4), RangeData(200, -14), RangeData(400, -23)],
        time_of_flight=[RangeData(40, 5), RangeData(100, 15), RangeData(200, 35), RangeData(400, 85)],
    ),
)

m72_a2_law = Weapon(
    name="M72 A2 LAW",
    weight=5.2,
    description="Standard NATO disposable anti-tank launcher. Reload time includes extending tube and deploying sights.",
    caliber=Caliber.CAL_66MM,
    weapon_type=WeaponType.ROCKET_PROPELLED_GRENADE,
    country=Country.USA,
    length_folded=26,
    length_deployed=35,
    reload_time=14,
    self_loading_action=False,
    ammo_capacity=1,
    ammo_weight=5.2,
    ammo_feed_device=AmmoFeedDevice.ROUND,
    ammunition_types=[ammo_66mm_heat_m72],
    aim_time_modifiers={
        1: -20, 2: -11, 3: -8, 4: -6, 5: -5, 6: -4, 7: -3, 8: -2
    },
    ballistic_data=WeaponBallisticData(
        angle_of_impact=[RangeData(40, 0), RangeData(100, 0), RangeData(200, 1), RangeData(400, 1)],
        ballistic_accuracy=[RangeData(40, 11), RangeData(100, -1), RangeData(200, -11), RangeData(400, -20)],
        time_of_flight=[RangeData(40, 5), RangeData(100, 14), RangeData(200, 32), RangeData(400, 75)],
    ),
)


WEAPONS_LIST = [
    fn_mk1,
    type_51,
    mab_pa15,
    walther_ppk,
    walther_p1,
    hk_p7m13,
    hk_vp70m,
    m1951,
    m93r,
    m951r,
    sig_p226,
    makarov_pm,
    psm,
    m92f,
    sw_m469,
    m1911a1,
    m15,
    asp_9mm,
    pa3_dm,
    f1_smg,
    steyr_mpi81,
    m61_skorpion,
    mat_49,
    hk_mp5,
    hk_mp5k,
    hk_53,
    uzi,
    mini_uzi,
    beretta_m12s,
    spectre,
    armscor_bxp,
    aks74u,
    sterling_mk7,
    ingram_mac10_9mm,
    ingram_mac10_45,
    bushmaster,
    steyr_aug,
    l1a1_f1,
    fn_fal,
    fn_fnc,
    m1949_56,
    fa_mas,
    fr_f2,
    hk_g3,
    hk_g41,
    hk_g11,
    walther_2000,
    amd_65,
    galil_ar_556,
    galil_ar_762,
    beretta_bm59,
    beretta_sc70,
    type_64,
    r4,
    sig_550,
    akm,
    ak_74,
    dragunov_svd,
    l1a1,
    enfield_iw,
    m14,
    m16a1,
    xm177,
    m16a2,
    m16a1_m203,
    m40a1,
    steyr_lsw,
    fn_mag,
    type_67,
    aa_762,
    hk_13e,
    hk_11e,
    hk_23e,
    hk_21e,
    mg3,
    galil_arm,
    beretta_m70_78,
    rpk_74,
    rpk_762,
    rp_46,
    rpd,
    pkm,
    nsv,
    enfield_lsw,
    bren_l4,
    l7a2,
    m249_minimi,
    m60,
    m60e3,
    m2hb,
    spas12,
    caws,
    mossberg_bullpup,
    remington_m870,
    high_standard_m10b,
    atchisson_assault_12,
    hk_69a1,
    hk_79,
    armscor_6,
    ak74_gp,
    ags_17,
    m79,
    m203,
    m174,
    m19,
    pzf_44,
    armbrust,
    rpg_18,
    rpg_7v,
    law_80,
    m72_a2_law
]
