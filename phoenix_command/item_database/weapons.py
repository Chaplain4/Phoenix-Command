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
    abbreviation="JHP",
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
    abbreviation="AP",
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
    abbreviation="FMJ",
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
    abbreviation="JHP",
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
    abbreviation="AP",
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
    abbreviation="FMJ",
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
    abbreviation="JHP",
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
    abbreviation="AP",
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
    abbreviation="FMJ",
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
    abbreviation="JHP",
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
    abbreviation="JHP",
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
    abbreviation="FMJ",
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
    abbreviation="JHP",
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
    abbreviation="AP",
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
    abbreviation="FMJ",
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
    abbreviation="JHP",
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
    abbreviation="AP",
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
    abbreviation="FMJ",
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
    abbreviation="JHP",
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
    abbreviation="AP",
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
# .45 ACP ammunition types
# ============================================================================

ammo_45_m15_fmj = AmmoType(
    name="45 ACP FMJ (M15)",
    abbreviation="FMJ",
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
    abbreviation="JHP",
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
    abbreviation="AP",
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
    abbreviation="FMJ",
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
    abbreviation="JHP",
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
    abbreviation="AP",
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

ammo_9mm_pa3_fmj = AmmoType(
    name="9mm Parabellum FMJ (PA3-DM)",
    abbreviation="FMJ",
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
    abbreviation="JHP",
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
    abbreviation="AP",
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
    abbreviation="FMJ",
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
    abbreviation="JHP",
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
    abbreviation="AP",
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
    abbreviation="FMJ",
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
    abbreviation="JHP",
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
    abbreviation="AP",
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
    abbreviation="FMJ",
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
    abbreviation="JHP",
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
    abbreviation="AP",
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
    abbreviation="FMJ",
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
    abbreviation="JHP",
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
    abbreviation="AP",
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
    abbreviation="FMJ",
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
    abbreviation="JHP",
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
    abbreviation="AP",
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
    abbreviation="FMJ",
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
    abbreviation="JHP",
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
    abbreviation="AP",
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
    abbreviation="FMJ",
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
    abbreviation="JHP",
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
    abbreviation="AP",
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
    abbreviation="FMJ",
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
    abbreviation="JHP",
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
    abbreviation="AP",
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
    abbreviation="FMJ",
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
    abbreviation="JHP",
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
    abbreviation="AP",
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
    abbreviation="FMJ",
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
    abbreviation="JHP",
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
    abbreviation="AP",
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
    abbreviation="FMJ",
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
    abbreviation="JHP",
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
    abbreviation="AP",
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
    abbreviation="FMJ",
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
    abbreviation="JHP",
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
    abbreviation="AP",
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
    abbreviation="FMJ",
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
    abbreviation="JHP",
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
    abbreviation="AP",
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
    abbreviation="FMJ",
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
    abbreviation="JHP",
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
    abbreviation="AP",
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
    abbreviation="FMJ",
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
    abbreviation="JHP",
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
    abbreviation="AP",
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
    abbreviation="FMJ",
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
    abbreviation="JHP",
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
    abbreviation="AP",
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
    abbreviation="FMJ",
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
    abbreviation="JHP",
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
    abbreviation="AP",
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
        RangeData(10, -6), RangeData(20, -1), RangeData(40, 4), RangeData(70, 8),
        RangeData(100, 11), RangeData(200, 16), RangeData(300, 19), RangeData(400, 21)
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
    actions_to_cycle=None,
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
    caliber="7.62 x 25mm",
    weapon_type="Pistol",
    country="China",
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
    caliber="9mm Parabellum",
    weapon_type="Pistol",
    country="France",
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
    caliber=".32 ACP",
    weapon_type="Pistol",
    country="West Germany",
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
    caliber="9mm Parabellum",
    weapon_type="Pistol",
    country="W Germany",
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
    caliber="9mm Parabellum",
    weapon_type="Pistol",
    country="W Germany",
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
    caliber="9mm Parabellum",
    weapon_type="Pistol",
    country="W Germany",
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
    caliber="9mm Parabellum",
    weapon_type="Pistol",
    country="Italy",
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
    caliber="9mm Parabellum",
    weapon_type="Pistol",
    country="Italy",
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
    ballistic_data=m93r_ballistic
)

# M951R Machine Pistol
m951r = Weapon(
    name="M951R",
    weight=3.2,
    description="Modified large capacity M1951 with fully automatic fire capability.",
    caliber="9mm Parabellum",
    weapon_type="Machine Pistol",
    country="Italy",
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
    caliber="9mm Parabellum",
    weapon_type="Automatic Pistol",
    country="Switzerland",
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
    caliber="9 x 18mm",
    weapon_type="Automatic Pistol",
    country="USSR",
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
    caliber="5.45 x 18mm",
    weapon_type="Automatic Pistol",
    country="USSR",
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
    caliber="9mm Parabellum",
    weapon_type="Automatic Pistol",
    country="USA",
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
    caliber="9mm Parabellum",
    weapon_type="Automatic Pistol",
    country="USA",
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
    caliber="45 ACP",
    weapon_type="Automatic Pistol",
    country="USA",
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
    caliber="45 ACP",
    weapon_type="Automatic Pistol",
    country="USA",
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
    caliber="9mm Parabellum",
    weapon_type="Automatic Pistol",
    country="USA",
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
    caliber="9mm Parabellum",
    weapon_type="Sub-Machinegun",
    country="Argentina",
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
    caliber="9mm Parabellum",
    weapon_type="Sub-Machinegun",
    country="Australia",
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
    caliber="9mm Parabellum",
    weapon_type="Sub-Machinegun",
    country="Austria",
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
    caliber=".32 ACP",
    weapon_type="Sub-Machine Pistol",
    country="Czechoslovakia",
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
    caliber="9mm Parabellum",
    weapon_type="Sub-Machinegun",
    country="France",
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
    caliber="9mm Parabellum",
    weapon_type="Sub-Machinegun",
    country="W Germany",
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
    caliber="9mm Parabellum",
    weapon_type="Sub-Machine Pistol",
    country="W Germany",
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
    ballistic_data=mp5k_ballistic
)

hk_53 = Weapon(
    name="Heckler & Koch 53",
    weight=8.1,
    description="Short version of the HK 33 which can be used as an SMG or rifle.",
    caliber="5.56mm NATO",
    weapon_type="Sub-Machinegun",
    country="W Germany",
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
    caliber="9mm Parabellum",
    weapon_type="Sub-Machinegun",
    country="Israel",
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
    caliber="9mm Parabellum",
    weapon_type="Sub-Machine Pistol",
    country="Israel",
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
    caliber="9mm Parabellum",
    weapon_type="Sub-Machinegun",
    country="Italy",
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
    ballistic_data=m12s_ballistic
)

spectre = Weapon(
    name="Spectre",
    weight=7.6,
    description="New SMG firing from a closed bolt using a four column magazine.",
    caliber="9mm Parabellum",
    weapon_type="Sub-Machinegun",
    country="Italy",
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
    ballistic_data=spectre_ballistic
)

armscor_bxp = Weapon(
    name="Armscor BXP",
    weight=6.3,
    description="Compact, light Sub-Machinegun which can be fired one handed.",
    caliber="9mm Parabellum",
    weapon_type="Sub-Machinegun",
    country="South Africa",
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
    caliber="5.45 x 39.5mm",
    weapon_type="Sub-Machinegun",
    country="USSR",
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
    caliber="9mm Parabellum",
    weapon_type="Sub-Machine Pistol",
    country="UK",
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
    caliber="9mm Parabellum",
    weapon_type="Sub-Machine Pistol",
    country="USA",
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
    caliber=".45 ACP",
    weapon_type="Sub-Machine Pistol",
    country="USA",
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
    caliber="5.56mm NATO",
    weapon_type="Sub-Machinegun",
    country="USA",
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

WEAPONS_LIST = [
    sig_550,
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
    bushmaster
]
