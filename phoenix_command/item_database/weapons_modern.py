"""Modern / post-Cold-War weapons (1980s–2020s) interpolated from existing catalogue analogues.

Ballistics follow project patterns: barrel length scales PEN/DC; same barrel/cartridge
copies parent tables; WeaponBallisticData / aim mods inherit from nearest class.
"""

from phoenix_command.models.enums import AmmoFeedDevice, Caliber, Country, WeaponType
from phoenix_command.models.gear import (
    AmmoType,
    BallisticData,
    ExplosiveData,
    RangeData,
    Weapon,
    WeaponBallisticData,
)

_R = (10, 20, 40, 70, 100, 200, 300, 400)


def _bd(rows, beyond_from=400):
    out = []
    for i, r in enumerate(_R):
        pen, dc = rows[i]
        beyond = beyond_from is not None and r >= beyond_from
        out.append(BallisticData(range_hexes=r, penetration=pen, damage_class=dc, beyond_max_range=beyond))
    return out


def _rd(values):
    return [RangeData(range_hexes=r, value=v) for r, v in zip(_R, values)]


# ---------------------------------------------------------------------------
# Shared parent-class ballistic profiles (copied from weapons.py analogues)
# ---------------------------------------------------------------------------

ak74_ballistic = WeaponBallisticData(
    minimum_arc=_rd([0.2, 0.3, 0.5, 0.9, 1.0, 3.0, 4.0, 5.0]),
    ballistic_accuracy=_rd([60, 52, 43, 36, 31, 21, 16, 12]),
    time_of_flight=_rd([0, 0, 1, 2, 2, 5, 8, 12]),
)

m4a1_ballistic = WeaponBallisticData(
    minimum_arc=_rd([0.4, 0.8, 2.0, 3.0, 4.0, 8.0, 11.0, 15.0]),
    ballistic_accuracy=_rd([61, 52, 43, 36, 31, 21, 16, 12]),
    time_of_flight=_rd([0, 0, 1, 1, 2, 5, 8, 11]),
)

hk416_ballistic = m4a1_ballistic

hk417_ballistic = WeaponBallisticData(
    ballistic_accuracy=_rd([65, 56, 47, 40, 35, 25, 19, 15]),
    time_of_flight=_rd([0, 0, 1, 2, 2, 5, 8, 12]),
)

fn_mag_ballistic = WeaponBallisticData(
    minimum_arc=_rd([0.3, 0.6, 1.0, 2.0, 3.0, 6.0, 9.0, 12.0]),
    ballistic_accuracy=_rd([61, 53, 45, 37, 32, 23, 17, 13]),
    time_of_flight=_rd([0, 0, 1, 2, 2, 5, 8, 11]),
)

pistol_9mm_v2_ballistic = WeaponBallisticData(
    ballistic_accuracy=_rd([48, 40, 31, 23, 18, 8, 3, 0]),
    time_of_flight=_rd([0, 1, 2, 3, 5, 12, 20, 30]),
)

spas12_ballistic = WeaponBallisticData(
    ballistic_accuracy=_rd([52, 43, 34, 26, 20, 10, 4, 0]),
    time_of_flight=_rd([0, 0, 1, 2, 3, 7, 12, 18]),
)

# Parent ammo copies (identical tables to catalogue parents)
ammo_545x39_ak74_fmj = AmmoType(name="5.45x39.5mm FMJ (AK-74M/AK-12)", description="FMJ", weight=1.1,
    ballistic_data=_bd([(14.0, 6), (13.0, 6), (12.0, 5), (10.0, 5), (9.1, 4), (5.8, 3), (3.7, 3), (2.4, 2)]))
ammo_545x39_ak74_jhp = AmmoType(name="5.45x39.5mm JHP (AK-74M/AK-12)", description="JHP", weight=1.1,
    ballistic_data=_bd([(13.0, 7), (13.0, 7), (11.0, 7), (10.0, 7), (8.8, 6), (5.6, 5), (3.6, 4), (2.3, 3)]))
ammo_545x39_ak74_ap = AmmoType(name="5.45x39.5mm AP (AK-74M/AK-12)", description="AP", weight=1.1,
    ballistic_data=_bd([(19.0, 6), (18.0, 5), (17.0, 5), (15.0, 5), (13.0, 4), (8.2, 3), (5.2, 3), (3.3, 2)]))

ammo_762x39_akm_fmj = AmmoType(name="7.62x39mm FMJ (AK-103)", description="FMJ", weight=1.8,
    ballistic_data=_bd([(11.0, 7), (11.0, 7), (9.8, 6), (8.6, 6), (7.5, 6), (4.8, 5), (3.1, 3), (2.0, 2)], beyond_from=300))
ammo_762x39_akm_jhp = AmmoType(name="7.62x39mm JHP (AK-103)", description="JHP", weight=1.8,
    ballistic_data=_bd([(11.0, 8), (10.0, 8), (9.4, 8), (8.3, 8), (7.2, 7), (4.7, 7), (3.0, 5), (1.9, 3)], beyond_from=300))
ammo_762x39_akm_ap = AmmoType(name="7.62x39mm AP (AK-103)", description="AP", weight=1.8,
    ballistic_data=_bd([(16.0, 7), (15.0, 6), (14.0, 6), (12.0, 6), (11.0, 6), (6.8, 4), (4.4, 3), (2.8, 2)], beyond_from=300))

ammo_556nato_m4_fmj = AmmoType(name="5.56mm NATO FMJ (SCAR-L)", description="FMJ", weight=1.0,
    ballistic_data=_bd([(15.0, 6), (14.0, 6), (13.0, 6), (12.0, 5), (10.0, 5), (6.7, 4), (4.3, 3), (2.8, 2)]))
ammo_556nato_m4_jhp = AmmoType(name="5.56mm NATO JHP (SCAR-L)", description="JHP", weight=1.0,
    ballistic_data=_bd([(15.0, 8), (14.0, 8), (13.0, 7), (11.0, 7), (9.5, 7), (6.4, 6), (4.1, 4), (2.7, 3)]))
ammo_556nato_m4_ap = AmmoType(name="5.56mm NATO AP (SCAR-L)", description="AP", weight=1.0,
    ballistic_data=_bd([(21.0, 6), (20.0, 6), (18.0, 5), (16.0, 5), (14.0, 4), (9.4, 3), (6.1, 3), (4.0, 2)]))

ammo_556nato_hk416_fmj = AmmoType(name="5.56mm NATO FMJ (M27 IAR)", description="FMJ", weight=1.0,
    ballistic_data=_bd([(15.0, 6), (14.0, 6), (13.0, 6), (12.0, 5), (10.0, 5), (6.7, 4), (4.3, 3), (2.8, 2)]))
ammo_556nato_hk416_jhp = AmmoType(name="5.56mm NATO JHP (M27 IAR)", description="JHP", weight=1.0,
    ballistic_data=_bd([(15.0, 8), (14.0, 8), (13.0, 7), (11.0, 7), (9.5, 7), (6.4, 6), (4.1, 4), (2.7, 3)]))
ammo_556nato_hk416_ap = AmmoType(name="5.56mm NATO AP (M27 IAR)", description="AP", weight=1.0,
    ballistic_data=_bd([(21.0, 6), (20.0, 6), (18.0, 5), (16.0, 5), (14.0, 4), (9.4, 3), (6.1, 3), (4.0, 2)]))

ammo_762nato_hk417_fmj = AmmoType(name="7.62mm NATO FMJ (SCAR-H)", description="FMJ", weight=1.4,
    ballistic_data=_bd([(18.0, 8), (17.0, 8), (16.0, 7), (15.0, 7), (13.0, 7), (9.5, 6), (6.7, 6), (4.8, 5)], beyond_from=None))
ammo_762nato_hk417_jhp = AmmoType(name="7.62mm NATO JHP (SCAR-H)", description="JHP", weight=1.4,
    ballistic_data=_bd([(17.0, 9), (17.0, 9), (16.0, 9), (14.0, 9), (13.0, 8), (9.1, 8), (6.5, 7), (4.6, 6)], beyond_from=None))
ammo_762nato_hk417_ap = AmmoType(name="7.62mm NATO AP (SCAR-H)", description="AP", weight=1.4,
    ballistic_data=_bd([(25.0, 7), (24.0, 7), (22.0, 7), (20.0, 6), (18.0, 6), (13.0, 5), (9.2, 5), (6.6, 4)], beyond_from=None))

ammo_762nato_fnmag_fmj = AmmoType(name="7.62mm NATO FMJ (M240B)", description="FMJ", weight=6.5,
    ballistic_data=_bd([(19.0, 8), (19.0, 8), (17.0, 8), (16.0, 7), (14.0, 7), (10.0, 7), (7.4, 6), (5.3, 5)]))
ammo_762nato_fnmag_jhp = AmmoType(name="7.62mm NATO JHP (M240B)", description="JHP", weight=6.5,
    ballistic_data=_bd([(18.0, 9), (18.0, 9), (17.0, 9), (15.0, 9), (14.0, 9), (9.8, 8), (7.1, 7), (5.1, 7)]))
ammo_762nato_fnmag_ap = AmmoType(name="7.62mm NATO AP (M240B)", description="AP", weight=6.5,
    ballistic_data=_bd([(27.0, 8), (26.0, 8), (25.0, 7), (22.0, 7), (20.0, 7), (14.0, 6), (10.0, 6), (7.5, 5)]))

ammo_762x54_svd_fmj = AmmoType(name="7.62x54mmR FMJ (SV-98)", description="FMJ", weight=0.68,
    ballistic_data=_bd([(22.0, 8), (21.0, 8), (20.0, 8), (18.0, 8), (16.0, 7), (12.0, 7), (9.0, 6), (6.8, 6)], beyond_from=None))
ammo_762x54_svd_jhp = AmmoType(name="7.62x54mmR JHP (SV-98)", description="JHP", weight=0.68,
    ballistic_data=_bd([(21.0, 10), (20.0, 9), (19.0, 9), (17.0, 9), (15.0, 9), (11.0, 8), (8.5, 8), (6.5, 7)], beyond_from=None))
ammo_762x54_svd_ap = AmmoType(name="7.62x54mmR AP (SV-98)", description="AP", weight=0.68,
    ballistic_data=_bd([(31.0, 8), (30.0, 8), (28.0, 8), (25.0, 7), (23.0, 7), (17.0, 6), (12.5, 6), (9.5, 5)], beyond_from=None))

ammo_9mm_mp5_fmj = AmmoType(name="9mm Parabellum FMJ (Vityaz)", description="FMJ", weight=1.2,
    ballistic_data=_bd([(2.5, 3), (2.3, 3), (2.0, 3), (1.5, 2), (1.2, 2), (0.5, 1), (0.2, 1), (0.1, 1)], beyond_from=200))
ammo_9mm_mp5_jhp = AmmoType(name="9mm Parabellum JHP (Vityaz)", description="JHP", weight=1.2,
    ballistic_data=_bd([(2.4, 5), (2.2, 5), (1.9, 4), (1.5, 3), (1.1, 2), (0.5, 1), (0.2, 1), (0.1, 1)], beyond_from=200))
ammo_9mm_mp5_ap = AmmoType(name="9mm Parabellum AP (Vityaz)", description="AP", weight=1.2,
    ballistic_data=_bd([(3.6, 3), (3.3, 3), (2.8, 3), (2.2, 2), (1.7, 2), (0.7, 1), (0.3, 1), (0.1, 1)], beyond_from=200))

ammo_9mm_pistol_fmj = AmmoType(name="9mm Parabellum FMJ (Glock/Grach)", description="FMJ", weight=0.5,
    ballistic_data=_bd([(2.4, 3), (2.2, 3), (1.8, 2), (1.3, 2), (1.0, 1), (0.4, 1), (0.15, 1), (0.08, 1)], beyond_from=100))
ammo_9mm_pistol_jhp = AmmoType(name="9mm Parabellum JHP (Glock/Grach)", description="JHP", weight=0.5,
    ballistic_data=_bd([(2.3, 5), (2.1, 5), (1.7, 4), (1.2, 3), (0.95, 2), (0.35, 1), (0.12, 1), (0.06, 1)], beyond_from=100))
ammo_9mm_pistol_ap = AmmoType(name="9mm Parabellum AP (Glock/Grach)", description="AP", weight=0.5,
    ballistic_data=_bd([(3.4, 3), (3.1, 3), (2.6, 2), (1.9, 2), (1.4, 1), (0.55, 1), (0.2, 1), (0.1, 1)], beyond_from=100))

ammo_127sov_nsv_fmj = AmmoType(name="12.7x107mm FMJ (Kord)", description="FMJ", weight=17.0,
    ballistic_data=_bd([(45.0, 10), (44.0, 10), (43.0, 10), (40.0, 10), (38.0, 10), (32.0, 10), (27.0, 10), (23.0, 10)], beyond_from=None))
ammo_127sov_nsv_jhp = AmmoType(name="12.7x107mm JHP (Kord)", description="JHP", weight=17.0,
    ballistic_data=_bd([(43.0, 10), (42.0, 10), (41.0, 10), (39.0, 10), (37.0, 10), (31.0, 10), (26.0, 10), (22.0, 10)], beyond_from=None))
ammo_127sov_nsv_ap = AmmoType(name="12.7x107mm AP (Kord)", description="AP", weight=17.0,
    ballistic_data=_bd([(63.0, 10), (62.0, 10), (60.0, 10), (57.0, 10), (54.0, 10), (45.0, 10), (38.0, 10), (32.0, 10)], beyond_from=None))

ammo_12g_spas_aps = AmmoType(
    name="12 Gauge APS (Benelli M4)", description="APS", weight=0.13,
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
        BallisticData(range_hexes=80, penetration=18.0, damage_class=8),
    ],
)
ammo_12g_spas_shot = AmmoType(
    name="12 Gauge Shot (00) (Benelli M4)", description="Shot", pellet_count=12, weight=0.13,
    ballistic_data=[
        BallisticData(range_hexes=1, penetration=5.3, damage_class=8, shotgun_accuracy_level_modifier=-13, pattern_radius=0.0),
        BallisticData(range_hexes=2, penetration=1.6, damage_class=3, shotgun_accuracy_level_modifier=-8, base_pellet_hit_chance="*11", pattern_radius=0.0),
        BallisticData(range_hexes=4, penetration=1.5, damage_class=3, shotgun_accuracy_level_modifier=-3, base_pellet_hit_chance="*10", pattern_radius=0.0),
        BallisticData(range_hexes=6, penetration=1.5, damage_class=3, shotgun_accuracy_level_modifier=0, base_pellet_hit_chance="*9", pattern_radius=0.1),
        BallisticData(range_hexes=8, penetration=1.4, damage_class=3, shotgun_accuracy_level_modifier=2, base_pellet_hit_chance="*5", pattern_radius=0.1),
        BallisticData(range_hexes=10, penetration=1.4, damage_class=3, shotgun_accuracy_level_modifier=4, base_pellet_hit_chance="*4", pattern_radius=0.1),
        BallisticData(range_hexes=15, penetration=1.3, damage_class=2, shotgun_accuracy_level_modifier=7, base_pellet_hit_chance="*2", pattern_radius=0.2),
        BallisticData(range_hexes=20, penetration=1.2, damage_class=2, shotgun_accuracy_level_modifier=9, base_pellet_hit_chance="94", pattern_radius=0.2),
        BallisticData(range_hexes=30, penetration=1.1, damage_class=2, shotgun_accuracy_level_modifier=12, base_pellet_hit_chance="42", pattern_radius=0.3),
        BallisticData(range_hexes=40, penetration=0.9, damage_class=2, shotgun_accuracy_level_modifier=14, base_pellet_hit_chance="24", pattern_radius=0.4),
        BallisticData(range_hexes=80, penetration=0.5, damage_class=1, shotgun_accuracy_level_modifier=19, base_pellet_hit_chance="5", pattern_radius=0.9),
    ],
)

# ============================================================================
# AK family
# ============================================================================

ammo_545x39_ak105_fmj = AmmoType(name="5.45x39.5mm FMJ (AK-105)", description="FMJ", weight=1.1,
    ballistic_data=_bd([(12.5, 6), (12.0, 5), (10.5, 5), (9.0, 5), (8.1, 4), (5.1, 3), (3.2, 2), (2.0, 2)]))
ammo_545x39_ak105_jhp = AmmoType(name="5.45x39.5mm JHP (AK-105)", description="JHP", weight=1.1,
    ballistic_data=_bd([(12.0, 7), (11.5, 7), (10.0, 7), (8.9, 6), (7.8, 6), (4.9, 5), (3.1, 4), (1.95, 3)]))
ammo_545x39_ak105_ap = AmmoType(name="5.45x39.5mm AP (AK-105)", description="AP", weight=1.1,
    ballistic_data=_bd([(17.0, 5), (16.5, 5), (15.0, 5), (13.0, 4), (11.5, 4), (7.2, 3), (4.5, 2), (2.85, 2)]))

ak105_ballistic = WeaponBallisticData(
    minimum_arc=_rd([0.2, 0.3, 0.55, 0.95, 1.5, 3.0, 4.5, 6.0]),
    ballistic_accuracy=_rd([60, 52, 43, 35.5, 31, 21, 15.5, 12]),
    time_of_flight=_rd([0, 0, 1, 2, 2.5, 5.5, 8.5, 12.5]),
)
ak12_ballistic = WeaponBallisticData(
    minimum_arc=_rd([0.2, 0.3, 0.5, 0.9, 1.0, 3.0, 4.0, 5.0]),
    ballistic_accuracy=_rd([61, 53, 44, 37, 32, 22, 17, 13]),
    time_of_flight=_rd([0, 0, 1, 2, 2, 5, 8, 12]),
)
ak103_ballistic = WeaponBallisticData(
    minimum_arc=_rd([0.35, 0.7, 1.5, 2.5, 3.5, 7.0, 10.0, 14.0]),
    ballistic_accuracy=_rd([59, 51, 41, 34, 29, 19, 14, 10]),
    time_of_flight=_rd([0, 1, 1, 2, 3, 6, 10, 14]),
)

ak_74m = Weapon(
    name="AK-74M", weight=7.9,
    description="Modernized AK-74 with polymer furniture and side-folding stock. Standard Russian service rifle from the mid-1990s (Interpolated from AK 74 + AKS-74U folding stock).",
    caliber=Caliber.CAL_545X39, weapon_type=WeaponType.ASSAULT_RIFLE, country=Country.RUSSIA,
    length_deployed=37.0, length_folded=28.0, reload_time=8, self_loading_action=True, full_auto=True,
    full_auto_rof=5, ammo_capacity=30, ammo_weight=1.1, ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=4, sustained_auto_burst=2,
    aim_time_modifiers={1: -23, 2: -12, 3: -9, 4: -7, 5: -6, 6: -4, 7: -3, 8: -2, 9: -1},
    ammunition_types=[ammo_545x39_ak74_fmj, ammo_545x39_ak74_jhp, ammo_545x39_ak74_ap],
    ballistic_data=ak74_ballistic,
)

ak_103 = Weapon(
    name="AK-103", weight=8.0,
    description="7.62x39mm export AK-100 series rifle. Combines AKM cartridge punch with AK-74M polymer furniture and folding stock (Interpolated from AKM 47 ammo + AK 74 handling).",
    caliber=Caliber.CAL_762X39, weapon_type=WeaponType.ASSAULT_RIFLE, country=Country.RUSSIA,
    length_deployed=37.0, length_folded=28.0, reload_time=8, self_loading_action=True, full_auto=True,
    full_auto_rof=5, ammo_capacity=30, ammo_weight=1.8, ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=7, sustained_auto_burst=4,
    aim_time_modifiers={1: -23, 2: -12, 3: -9, 4: -7, 5: -6, 6: -4, 7: -3, 8: -2, 9: -1},
    ammunition_types=[ammo_762x39_akm_fmj, ammo_762x39_akm_jhp, ammo_762x39_akm_ap],
    ballistic_data=ak103_ballistic,
)

ak_105 = Weapon(
    name="AK-105", weight=7.1,
    description="Compact 5.45mm AK-100 carbine with a 314mm barrel. Between AKS-74U and full-length AK-74 in velocity and handling (Interpolated from AKS-74U + AK 74 + M4A1 role).",
    caliber=Caliber.CAL_545X39, weapon_type=WeaponType.CARBINE, country=Country.RUSSIA,
    length_deployed=32.0, length_folded=24.0, reload_time=8, self_loading_action=True, full_auto=True,
    full_auto_rof=6, ammo_capacity=30, ammo_weight=1.1, ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=4, sustained_auto_burst=3,
    aim_time_modifiers={1: -22, 2: -12, 3: -9, 4: -7, 5: -5, 6: -4, 7: -3, 8: -2, 9: -1},
    ammunition_types=[ammo_545x39_ak105_fmj, ammo_545x39_ak105_jhp, ammo_545x39_ak105_ap],
    ballistic_data=ak105_ballistic,
)

ak_12 = Weapon(
    name="AK-12", weight=7.7,
    description="Russian Ratnik-era 5.45mm assault rifle with improved ergonomics and accessory rails. Ballistics near AK-74 with slightly better practical accuracy (Interpolated from AK 74 + SIG 550 + HK416).",
    caliber=Caliber.CAL_545X39, weapon_type=WeaponType.ASSAULT_RIFLE, country=Country.RUSSIA,
    length_deployed=37.0, length_folded=28.0, reload_time=8, self_loading_action=True, full_auto=True,
    full_auto_rof=5, ammo_capacity=30, ammo_weight=1.1, ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=4, sustained_auto_burst=2,
    aim_time_modifiers={1: -22, 2: -12, 3: -9, 4: -7, 5: -5, 6: -4, 7: -3, 8: -2, 9: -1, 10: 0},
    ammunition_types=[ammo_545x39_ak74_fmj, ammo_545x39_ak74_jhp, ammo_545x39_ak74_ap],
    ballistic_data=ak12_ballistic,
)

# ============================================================================
# NATO rifles
# ============================================================================

ammo_556nato_g36_fmj = AmmoType(name="5.56mm NATO FMJ (G36)", description="FMJ", weight=1.0,
    ballistic_data=_bd([(16.0, 6), (15.0, 6), (14.0, 6), (12.5, 6), (11.0, 5), (7.2, 4), (4.7, 3), (3.1, 2)]))
ammo_556nato_g36_jhp = AmmoType(name="5.56mm NATO JHP (G36)", description="JHP", weight=1.0,
    ballistic_data=_bd([(15.5, 8), (14.5, 8), (13.5, 8), (12.0, 7), (10.2, 7), (6.9, 6), (4.5, 5), (2.95, 3)]))
ammo_556nato_g36_ap = AmmoType(name="5.56mm NATO AP (G36)", description="AP", weight=1.0,
    ballistic_data=_bd([(22.5, 6), (21.5, 6), (19.5, 6), (17.0, 5), (15.0, 5), (10.2, 4), (6.6, 3), (4.2, 2)]))

g36_ballistic = WeaponBallisticData(
    three_round_burst=_rd([-5, 0, 4.5, 8.5, 11.5, 16.5, 19.5, 21.5]),
    minimum_arc=_rd([0.4, 0.8, 2.0, 3.0, 4.0, 8.0, 11.0, 15.0]),
    ballistic_accuracy=_rd([61, 53, 44, 37, 32, 22, 17, 13]),
    time_of_flight=_rd([0, 0, 1, 1, 2, 5, 8, 11]),
)

ammo_762nato_mk14_fmj = AmmoType(name="7.62mm NATO FMJ (Mk 14 EBR)", description="FMJ", weight=1.4,
    ballistic_data=_bd([(19.0, 8), (18.0, 8), (17.0, 8), (15.5, 7), (14.0, 7), (10.0, 7), (7.2, 6), (5.2, 5)], beyond_from=None))
ammo_762nato_mk14_jhp = AmmoType(name="7.62mm NATO JHP (Mk 14 EBR)", description="JHP", weight=1.4,
    ballistic_data=_bd([(18.0, 9), (17.5, 9), (16.5, 9), (15.0, 9), (13.5, 9), (9.5, 8), (7.0, 8), (5.0, 7)], beyond_from=None))
ammo_762nato_mk14_ap = AmmoType(name="7.62mm NATO AP (Mk 14 EBR)", description="AP", weight=1.4,
    ballistic_data=_bd([(26.5, 8), (25.5, 8), (24.0, 7), (21.5, 7), (19.5, 7), (14.5, 6), (10.5, 6), (7.5, 5)], beyond_from=None))

mk14_ballistic = WeaponBallisticData(
    minimum_arc=_rd([0.5, 0.9, 2.0, 3.5, 5.0, 10.0, 15.0, 20.0]),
    ballistic_accuracy=_rd([64, 55, 47, 40, 35, 25, 19, 15]),
    time_of_flight=_rd([0, 0, 1, 2, 2, 5, 8, 11]),
)

fn_scar_l = Weapon(
    name="FN SCAR-L", weight=7.7,
    description="SOCOM 5.56mm modular assault rifle (Mk 16). Short-stroke gas piston, folding stock (Interpolated from M4A1 + HK416 + Steyr AUG).",
    caliber=Caliber.CAL_556_NATO, weapon_type=WeaponType.ASSAULT_RIFLE, country=Country.BELGIUM,
    length_deployed=35.0, length_folded=25.0, reload_time=8, self_loading_action=True, full_auto=True,
    full_auto_rof=7, ammo_capacity=30, ammo_weight=1.0, ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=4, sustained_auto_burst=3,
    aim_time_modifiers={1: -22, 2: -12, 3: -9, 4: -7, 5: -5, 6: -4, 7: -3, 8: -2, 9: -1, 10: 0},
    ammunition_types=[ammo_556nato_m4_fmj, ammo_556nato_m4_jhp, ammo_556nato_m4_ap],
    ballistic_data=m4a1_ballistic,
)

fn_scar_h = Weapon(
    name="FN SCAR-H", weight=11.0,
    description="SOCOM 7.62mm NATO battle/DMR rifle (Mk 17). Select-fire with folding stock (Interpolated from HK417 + FN FAL + SR-25).",
    caliber=Caliber.CAL_762_NATO, weapon_type=WeaponType.BATTLE_RIFLE, country=Country.BELGIUM,
    length_deployed=38.0, length_folded=28.0, reload_time=8, self_loading_action=True, full_auto=True,
    full_auto_rof=5, ammo_capacity=20, ammo_weight=1.4, ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=10, sustained_auto_burst=5,
    aim_time_modifiers={1: -23, 2: -13, 3: -8, 4: -6, 5: -4, 6: -3, 7: -1, 8: 0, 9: 1, 10: 2, 11: 3},
    ammunition_types=[ammo_762nato_hk417_fmj, ammo_762nato_hk417_jhp, ammo_762nato_hk417_ap],
    ballistic_data=hk417_ballistic,
)

hk_g36 = Weapon(
    name="Heckler & Koch G36", weight=8.4,
    description="German Bundeswehr 5.56mm service rifle with dual optics and polymer receiver. Widely exported (Interpolated from HK G41 + Steyr AUG + M16A2).",
    caliber=Caliber.CAL_556_NATO, weapon_type=WeaponType.ASSAULT_RIFLE, country=Country.GERMANY,
    length_deployed=39.0, length_folded=30.0, reload_time=8, self_loading_action=True, full_auto=True,
    full_auto_rof=7, ammo_capacity=30, ammo_weight=1.0, ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=4, sustained_auto_burst=3,
    aim_time_modifiers={1: -22, 2: -12, 3: -9, 4: -7, 5: -5, 6: -4, 7: -3, 8: -2, 9: -1, 10: 0, 11: 1},
    ammunition_types=[ammo_556nato_g36_fmj, ammo_556nato_g36_jhp, ammo_556nato_g36_ap],
    ballistic_data=g36_ballistic, built_in_optics=True,
)

m27_iar = Weapon(
    name="M27 IAR", weight=8.8,
    description="USMC Infantry Automatic Rifle based on HK416. Magazine-fed SAW replacement also issued as a service rifle (Interpolated from HK416 + M249 role).",
    caliber=Caliber.CAL_556_NATO, weapon_type=WeaponType.LIGHT_MACHINE_GUN, country=Country.USA,
    length_deployed=37.0, length_folded=33.0, reload_time=8, self_loading_action=True, full_auto=True,
    full_auto_rof=7, ammo_capacity=30, ammo_weight=1.0, ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=4, sustained_auto_burst=3,
    aim_time_modifiers={1: -22, 2: -12, 3: -9, 4: -7, 5: -5, 6: -4, 7: -3, 8: -2, 9: -1, 10: 0},
    ammunition_types=[ammo_556nato_hk416_fmj, ammo_556nato_hk416_jhp, ammo_556nato_hk416_ap],
    ballistic_data=hk416_ballistic,
)

mk14_ebr = Weapon(
    name="Mk 14 EBR", weight=11.5,
    description="Enhanced Battle Rifle — modernized M14 in a Sage chassis used by US SOF as a DMR (Interpolated from M 14 + SR-25 / M110).",
    caliber=Caliber.CAL_762_NATO, weapon_type=WeaponType.SNIPER_RIFLE, country=Country.USA,
    length_deployed=35.0, length_folded=26.0, reload_time=8, self_loading_action=True, full_auto=True,
    full_auto_rof=5, ammo_capacity=20, ammo_weight=1.4, ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=10, sustained_auto_burst=5,
    aim_time_modifiers={1: -23, 2: -13, 3: -8, 4: -5, 5: -4, 6: -2, 7: 0, 8: 1, 9: 2, 10: 3, 11: 4},
    ammunition_types=[ammo_762nato_mk14_fmj, ammo_762nato_mk14_jhp, ammo_762nato_mk14_ap],
    ballistic_data=mk14_ballistic, built_in_optics=True, built_in_bipod=True,
)

# ============================================================================
# MG / SMG / pistols / support
# ============================================================================

ammo_762x54_pkp_fmj = AmmoType(name="7.62x54mmR FMJ (PKP)", description="FMJ", weight=5.7,
    ballistic_data=_bd([(23.0, 8), (22.0, 8), (21.0, 8), (19.0, 8), (18.0, 8), (13.0, 7), (10.0, 7), (7.7, 6)], beyond_from=None))
ammo_762x54_pkp_jhp = AmmoType(name="7.62x54mmR JHP (PKP)", description="JHP", weight=5.7,
    ballistic_data=_bd([(22.0, 10), (21.0, 9), (20.0, 9), (18.0, 9), (17.0, 9), (13.0, 9), (9.7, 8), (7.4, 8)], beyond_from=None))
ammo_762x54_pkp_ap = AmmoType(name="7.62x54mmR AP (PKP)", description="AP", weight=5.7,
    ballistic_data=_bd([(32.0, 8), (31.0, 8), (29.0, 8), (27.0, 8), (25.0, 7), (19.0, 7), (14.0, 6), (11.0, 6)], beyond_from=None))

pkp_ballistic = WeaponBallisticData(
    minimum_arc=_rd([0.35, 0.7, 1.7, 2.7, 3.5, 7.0, 10.5, 14.0]),
    ballistic_accuracy=_rd([64, 57, 49, 42, 37, 28, 22, 18]),
    time_of_flight=_rd([0, 0, 1, 2, 2, 5, 8, 11]),
)

pkp_pecheneg = Weapon(
    name="PKP Pecheneg", weight=28.0,
    description="Modernized PKM with forced-air cooled heavy barrel for sustained fire. Russian army GPMG (Interpolated from PKM + FN MAG stability).",
    caliber=Caliber.CAL_762X54R, weapon_type=WeaponType.LIGHT_MACHINE_GUN, country=Country.RUSSIA,
    length_deployed=47.0, reload_time=12, self_loading_action=True, full_auto=True,
    full_auto_rof=6, ammo_capacity=100, ammo_weight=5.7, ammo_feed_device=AmmoFeedDevice.BELT,
    knock_down=12, sustained_auto_burst=4,
    aim_time_modifiers={1: -28, 2: -18, 3: -12, 4: -9, 5: -7, 6: -5, 7: -4, 8: -3, 9: -2, 10: -1, 12: 1},
    ammunition_types=[ammo_762x54_pkp_fmj, ammo_762x54_pkp_jhp, ammo_762x54_pkp_ap],
    ballistic_data=pkp_ballistic, built_in_bipod=True,
)

kord_ballistic = WeaponBallisticData(
    minimum_arc=_rd([0.25, 0.45, 0.9, 1.8, 2.7, 4.5, 7.0, 9.0]),
    ballistic_accuracy=_rd([65, 58, 50, 44, 39, 30, 24, 20]),
    time_of_flight=_rd([0, 0, 1, 2, 2, 5, 7, 10]),
)

kord = Weapon(
    name="Kord 6P50", weight=56.0,
    description="Russian 12.7mm heavy machine gun replacing the NSV. Lighter receiver, improved reliability (Interpolated from NSV + M2HB role).",
    caliber=Caliber.CAL_127X108, weapon_type=WeaponType.HEAVY_MACHINE_GUN, country=Country.RUSSIA,
    length_deployed=78.0, reload_time=14, self_loading_action=True, full_auto=True,
    full_auto_rof=6, ammo_capacity=50, ammo_weight=17.0, ammo_feed_device=AmmoFeedDevice.BELT,
    knock_down=49, sustained_auto_burst=3,
    aim_time_modifiers={1: -32, 2: -22, 3: -15, 4: -11, 5: -8, 6: -5, 7: -3, 8: -1, 10: 1, 12: 2, 16: 5},
    ammunition_types=[ammo_127sov_nsv_fmj, ammo_127sov_nsv_jhp, ammo_127sov_nsv_ap],
    ballistic_data=kord_ballistic, built_in_bipod=True,
)

sv98_ballistic = WeaponBallisticData(
    ballistic_accuracy=_rd([70, 62, 53, 46, 41, 32, 26, 22]),
    time_of_flight=_rd([0, 0, 1, 2, 2, 5, 8, 11]),
)

sv_98 = Weapon(
    name="SV-98", weight=15.4,
    description="Russian bolt-action sniper rifle in 7.62x54R with bipod and optics. Service sniper from the late 1990s (Interpolated from M40A1 bolt action + SVD caliber).",
    caliber=Caliber.CAL_762X54R, weapon_type=WeaponType.SNIPER_RIFLE, country=Country.RUSSIA,
    length_deployed=47.0, reload_time=16, self_loading_action=False, full_auto=False, actions_to_cycle=3,
    ammo_capacity=10, ammo_weight=0.68, ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=12, sustained_auto_burst=6,
    aim_time_modifiers={1: -25, 2: -15, 3: -8, 4: -6, 5: -4, 6: -3, 7: -1, 8: 1, 9: 2, 10: 3, 11: 4, 12: 4},
    ammunition_types=[ammo_762x54_svd_fmj, ammo_762x54_svd_jhp, ammo_762x54_svd_ap],
    ballistic_data=sv98_ballistic, built_in_optics=True, built_in_bipod=True,
)

vityaz_ballistic = WeaponBallisticData(
    minimum_arc=_rd([0.4, 0.75, 1.2, 2.2, 4.0, 7.5, 11.5, 15.0]),
    ballistic_accuracy=_rd([47, 38, 29, 22, 17, 7, 1, -2]),
    time_of_flight=_rd([0, 1, 2, 4, 6, 13, 21, 31]),
)

pp19_01_vityaz = Weapon(
    name="PP-19-01 Vityaz", weight=6.4,
    description="Russian 9mm Parabellum SMG based on the AK-100 receiver. Standard for police and SOF (Interpolated from HK MP5 + Uzi + Spectre).",
    caliber=Caliber.CAL_9MM_PARABELLUM, weapon_type=WeaponType.SUB_MACHINEGUN, country=Country.RUSSIA,
    length_deployed=19.0, length_folded=14.0, reload_time=8, self_loading_action=True, full_auto=True,
    full_auto_rof=7, ammo_capacity=30, ammo_weight=1.2, ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=4, sustained_auto_burst=3,
    aim_time_modifiers={1: -21, 2: -11, 3: -8, 4: -6, 5: -5, 6: -4, 7: -3, 8: -2, 9: -1},
    ammunition_types=[ammo_9mm_mp5_fmj, ammo_9mm_mp5_jhp, ammo_9mm_mp5_ap],
    ballistic_data=vityaz_ballistic,
)

mp443_grach = Weapon(
    name="MP-443 Grach", weight=2.1,
    description="Russian Yarygin PYa service pistol in 9mm Parabellum. Replaced the Makarov in Russian forces (Interpolated from M92F + SIG P226).",
    caliber=Caliber.CAL_9MM_PARABELLUM, weapon_type=WeaponType.AUTOMATIC_PISTOL, country=Country.RUSSIA,
    length_deployed=8.0, reload_time=4, self_loading_action=True, full_auto=False,
    ammo_capacity=17, ammo_weight=0.55, ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=3, sustained_auto_burst=4,
    aim_time_modifiers={1: -17, 2: -11, 3: -10, 4: -9, 5: -8, 6: -7},
    ammunition_types=[ammo_9mm_pistol_fmj, ammo_9mm_pistol_jhp, ammo_9mm_pistol_ap],
    ballistic_data=pistol_9mm_v2_ballistic,
)

glock_17 = Weapon(
    name="Glock 17", weight=1.4,
    description="Austrian polymer-framed 9mm pistol. Ubiquitous military, police, and civilian sidearm worldwide (Interpolated from SIG P226 + M92F).",
    caliber=Caliber.CAL_9MM_PARABELLUM, weapon_type=WeaponType.AUTOMATIC_PISTOL, country=Country.AUSTRIA,
    length_deployed=8.0, reload_time=4, self_loading_action=True, full_auto=False,
    ammo_capacity=17, ammo_weight=0.5, ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=3, sustained_auto_burst=4,
    aim_time_modifiers={1: -16, 2: -11, 3: -10, 4: -9, 5: -8, 6: -7},
    ammunition_types=[ammo_9mm_pistol_fmj, ammo_9mm_pistol_jhp, ammo_9mm_pistol_ap],
    ballistic_data=pistol_9mm_v2_ballistic,
)

m240b = Weapon(
    name="M240B", weight=27.1,
    description="US designation of the FN MAG as the standard 7.62mm medium machine gun. Replaced the M60 in US service (Interpolated from FN MAG + M60E3 + L7A2).",
    caliber=Caliber.CAL_762_NATO, weapon_type=WeaponType.MACHINE_GUN, country=Country.USA,
    length_deployed=49.0, reload_time=12, self_loading_action=True, full_auto=True,
    full_auto_rof=6, ammo_capacity=100, ammo_weight=6.5, ammo_feed_device=AmmoFeedDevice.BELT,
    knock_down=10, sustained_auto_burst=3,
    aim_time_modifiers={1: -28, 2: -18, 3: -12, 4: -9, 5: -7, 6: -6, 7: -5, 8: -4, 10: -2, 12: 0, 14: 1},
    ammunition_types=[ammo_762nato_fnmag_fmj, ammo_762nato_fnmag_jhp, ammo_762nato_fnmag_ap],
    ballistic_data=fn_mag_ballistic, built_in_bipod=True,
)

benelli_m4 = Weapon(
    name="Benelli M4", weight=8.4,
    description="Semi-automatic 12-gauge combat shotgun (M1014) used by USMC and many NATO forces (Interpolated from Franchi SPAS 12 + Remington M870).",
    caliber=Caliber.CAL_12_GAUGE, weapon_type=WeaponType.SHOTGUN, country=Country.ITALY,
    length_deployed=40.0, length_folded=35.0, reload_time=28, self_loading_action=True,
    ammo_capacity=7, ammo_weight=0.13, ammo_feed_device=AmmoFeedDevice.ROUND,
    knock_down=23, sustained_auto_burst=10,
    aim_time_modifiers={1: -22, 2: -12, 3: -8, 4: -6, 5: -5, 6: -4, 7: -3, 8: -2, 9: -1, 10: 0},
    ammunition_types=[ammo_12g_spas_aps, ammo_12g_spas_shot],
    ballistic_data=spas12_ballistic,
)

ammo_84mm_heat_at4 = AmmoType(
    name="84mm HEAT (AT4)", description="HEAT", weight=14.8,
    ballistic_data=[BallisticData(range_hexes=r, penetration=12000, damage_class=10) for r in [40, 100, 200, 400]],
    explosive_data=[
        ExplosiveData(range_hexes=0, shrapnel_penetration=6.8, shrapnel_damage_class=8, base_shrapnel_hit_chance="12", base_concussion=1800),
        ExplosiveData(range_hexes=1, shrapnel_penetration=6.6, shrapnel_damage_class=8, base_shrapnel_hit_chance="2", base_concussion=360),
        ExplosiveData(range_hexes=2, shrapnel_penetration=6.3, shrapnel_damage_class=8, base_shrapnel_hit_chance="0", base_concussion=95),
        ExplosiveData(range_hexes=3, shrapnel_penetration=6.0, shrapnel_damage_class=8, base_shrapnel_hit_chance="0", base_concussion=48),
        ExplosiveData(range_hexes=5, shrapnel_penetration=5.5, shrapnel_damage_class=7, base_shrapnel_hit_chance="0", base_concussion=20),
        ExplosiveData(range_hexes=10, shrapnel_penetration=4.5, shrapnel_damage_class=6, base_shrapnel_hit_chance="0", base_concussion=7),
    ],
)

at4 = Weapon(
    name="AT4", weight=14.8,
    description="Swedish disposable 84mm anti-armor launcher widely issued to US and NATO infantry (Interpolated from M72 A2 LAW + LAW 80).",
    caliber=Caliber.CAL_84MM, weapon_type=WeaponType.ROCKET_PROPELLED_GRENADE, country=Country.USA,
    length_folded=40, length_deployed=40, reload_time=16, self_loading_action=False,
    ammo_capacity=1, ammo_weight=14.8, ammo_feed_device=AmmoFeedDevice.ROUND,
    ammunition_types=[ammo_84mm_heat_at4],
    aim_time_modifiers={1: -24, 2: -14, 3: -9, 4: -7, 5: -6, 6: -4, 7: -3, 8: -2, 9: -1},
    ballistic_data=WeaponBallisticData(
        angle_of_impact=[RangeData(40, 0), RangeData(100, 0), RangeData(200, 1), RangeData(400, 2)],
        ballistic_accuracy=[RangeData(40, 10), RangeData(100, -2), RangeData(200, -12), RangeData(400, -21)],
        time_of_flight=[RangeData(40, 5), RangeData(100, 14), RangeData(200, 33), RangeData(400, 78)],
    ),
)

# ============================================================================
# Wave 2 — new calibers
# ============================================================================

ammo_9x39_fmj = AmmoType(name="9x39mm FMJ (SP-5)", description="FMJ", weight=1.4,
    ballistic_data=_bd([(10.0, 8), (9.5, 8), (8.5, 7), (7.2, 7), (6.0, 6), (3.5, 5), (2.0, 3), (1.2, 2)], beyond_from=200))
ammo_9x39_jhp = AmmoType(name="9x39mm JHP", description="JHP", weight=1.4,
    ballistic_data=_bd([(9.5, 9), (9.0, 9), (8.0, 9), (6.8, 8), (5.7, 8), (3.3, 7), (1.9, 5), (1.1, 3)], beyond_from=200))
ammo_9x39_ap = AmmoType(name="9x39mm AP (SP-6)", description="AP", weight=1.4,
    ballistic_data=_bd([(15.0, 7), (14.0, 7), (12.5, 7), (10.5, 6), (9.0, 6), (5.2, 4), (3.0, 3), (1.8, 2)], beyond_from=200))

as_val_ballistic = WeaponBallisticData(
    minimum_arc=_rd([0.3, 0.6, 1.2, 2.2, 3.5, 7.0, 11.0, 15.0]),
    ballistic_accuracy=_rd([58, 49, 40, 32, 27, 16, 10, 6]),
    time_of_flight=_rd([0, 1, 2, 3, 5, 11, 18, 26]),
)
vss_ballistic = WeaponBallisticData(
    ballistic_accuracy=_rd([66, 57, 48, 40, 35, 24, 17, 12]),
    time_of_flight=_rd([0, 1, 2, 3, 5, 11, 18, 26]),
)

as_val = Weapon(
    name="AS Val", weight=6.5,
    description="Integrally suppressed Russian assault rifle in 9x39mm for Spetsnaz CQB (Interpolated from 7.62x39 impulse + AKS-74U range; built-in suppressor).",
    caliber=Caliber.CAL_9X39, weapon_type=WeaponType.ASSAULT_RIFLE, country=Country.RUSSIA,
    length_deployed=34.0, length_folded=24.0, reload_time=8, self_loading_action=True, full_auto=True,
    full_auto_rof=6, ammo_capacity=20, ammo_weight=1.0, ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=6, sustained_auto_burst=3,
    aim_time_modifiers={1: -21, 2: -11, 3: -8, 4: -6, 5: -5, 6: -4, 7: -3, 8: -2, 9: -1},
    ammunition_types=[ammo_9x39_fmj, ammo_9x39_jhp, ammo_9x39_ap],
    ballistic_data=as_val_ballistic, built_in_suppressor=True,
)

vss_vintorez = Weapon(
    name="VSS Vintorez", weight=7.7,
    description="Integrally suppressed Russian sniper rifle in 9x39mm with PSO optics. Special forces DMR (Interpolated from AS Val platform + SVD optics role).",
    caliber=Caliber.CAL_9X39, weapon_type=WeaponType.SNIPER_RIFLE, country=Country.RUSSIA,
    length_deployed=35.0, reload_time=8, self_loading_action=True, full_auto=True,
    full_auto_rof=5, ammo_capacity=10, ammo_weight=0.7, ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=6, sustained_auto_burst=4,
    aim_time_modifiers={1: -22, 2: -12, 3: -7, 4: -5, 5: -4, 6: -2, 7: 0, 8: 1, 9: 2, 10: 3},
    ammunition_types=[ammo_9x39_fmj, ammo_9x39_jhp, ammo_9x39_ap],
    ballistic_data=vss_ballistic, built_in_optics=True, built_in_suppressor=True,
)

ammo_46x30_fmj = AmmoType(name="4.6x30mm FMJ (MP7)", description="FMJ", weight=0.8,
    ballistic_data=_bd([(5.5, 3), (5.0, 3), (4.2, 2), (3.2, 2), (2.5, 2), (1.2, 1), (0.6, 1), (0.3, 1)], beyond_from=200))
ammo_46x30_jhp = AmmoType(name="4.6x30mm JHP (MP7)", description="JHP", weight=0.8,
    ballistic_data=_bd([(5.2, 4), (4.7, 4), (4.0, 3), (3.0, 3), (2.3, 2), (1.1, 1), (0.5, 1), (0.25, 1)], beyond_from=200))
ammo_46x30_ap = AmmoType(name="4.6x30mm AP (MP7)", description="AP", weight=0.8,
    ballistic_data=_bd([(9.0, 2), (8.2, 2), (7.0, 2), (5.5, 2), (4.3, 1), (2.0, 1), (1.0, 1), (0.5, 1)], beyond_from=200))

mp7_ballistic = WeaponBallisticData(
    minimum_arc=_rd([0.4, 0.8, 1.5, 2.5, 4.0, 8.0, 12.0, 16.0]),
    ballistic_accuracy=_rd([50, 41, 32, 24, 19, 9, 3, 0]),
    time_of_flight=_rd([0, 0, 1, 2, 3, 7, 12, 18]),
)

hk_mp7 = Weapon(
    name="Heckler & Koch MP7", weight=4.6,
    description="German PDW in 4.6x30mm with high armor penetration for a compact SMG. Used by NATO SOF and police (Interpolated from MP5K handling + high-PEN/low-DC PDW ballistics).",
    caliber=Caliber.CAL_46X30, weapon_type=WeaponType.SUB_MACHINEGUN, country=Country.GERMANY,
    length_deployed=21.0, length_folded=13.0, reload_time=7, self_loading_action=True, full_auto=True,
    full_auto_rof=8, ammo_capacity=40, ammo_weight=0.8, ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=2, sustained_auto_burst=3,
    aim_time_modifiers={1: -19, 2: -10, 3: -8, 4: -6, 5: -5, 6: -4, 7: -3, 8: -2},
    ammunition_types=[ammo_46x30_fmj, ammo_46x30_jhp, ammo_46x30_ap],
    ballistic_data=mp7_ballistic,
)

ammo_57x28_fmj = AmmoType(name="5.7x28mm FMJ (SS190)", description="FMJ", weight=0.9,
    ballistic_data=_bd([(6.0, 3), (5.5, 3), (4.6, 3), (3.5, 2), (2.8, 2), (1.3, 1), (0.7, 1), (0.35, 1)], beyond_from=200))
ammo_57x28_jhp = AmmoType(name="5.7x28mm JHP", description="JHP", weight=0.9,
    ballistic_data=_bd([(5.7, 4), (5.2, 4), (4.3, 4), (3.3, 3), (2.6, 3), (1.2, 2), (0.6, 1), (0.3, 1)], beyond_from=200))
ammo_57x28_ap = AmmoType(name="5.7x28mm AP", description="AP", weight=0.9,
    ballistic_data=_bd([(9.5, 2), (8.7, 2), (7.4, 2), (5.8, 2), (4.6, 2), (2.2, 1), (1.1, 1), (0.55, 1)], beyond_from=200))

p90_ballistic = WeaponBallisticData(
    minimum_arc=_rd([0.35, 0.7, 1.3, 2.3, 3.5, 7.0, 11.0, 15.0]),
    ballistic_accuracy=_rd([52, 43, 34, 26, 21, 11, 5, 1]),
    time_of_flight=_rd([0, 0, 1, 2, 3, 7, 11, 17]),
)

fn_p90 = Weapon(
    name="FN P90", weight=6.6,
    description="Belgian bullpup PDW in 5.7x28mm with 50-round top magazine. Famous with special forces and vehicle crews (Interpolated from HK 53 / Bushmaster PDW role + 9mm SMG handling).",
    caliber=Caliber.CAL_57X28, weapon_type=WeaponType.SUB_MACHINEGUN, country=Country.BELGIUM,
    length_deployed=20.0, reload_time=8, self_loading_action=True, full_auto=True,
    full_auto_rof=8, ammo_capacity=50, ammo_weight=0.9, ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=2, sustained_auto_burst=3,
    aim_time_modifiers={1: -20, 2: -10, 3: -8, 4: -6, 5: -5, 6: -4, 7: -3, 8: -2, 9: -1},
    ammunition_types=[ammo_57x28_fmj, ammo_57x28_jhp, ammo_57x28_ap],
    ballistic_data=p90_ballistic,
)

fn_five_seven = Weapon(
    name="FN Five-seveN", weight=1.6,
    description="Belgian 5.7x28mm pistol companion to the P90. High magazine capacity and armor-piercing capability (Interpolated from PSM high-PEN pistol + 9mm service pistol handling).",
    caliber=Caliber.CAL_57X28, weapon_type=WeaponType.AUTOMATIC_PISTOL, country=Country.BELGIUM,
    length_deployed=8.0, reload_time=4, self_loading_action=True, full_auto=False,
    ammo_capacity=20, ammo_weight=0.4, ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=2, sustained_auto_burst=3,
    aim_time_modifiers={1: -16, 2: -11, 3: -10, 4: -9, 5: -8, 6: -7},
    ammunition_types=[ammo_57x28_fmj, ammo_57x28_jhp, ammo_57x28_ap],
    ballistic_data=WeaponBallisticData(
        ballistic_accuracy=_rd([48, 39, 30, 22, 17, 7, 2, -1]),
        time_of_flight=_rd([0, 1, 2, 3, 5, 11, 18, 27]),
    ),
)

ammo_45_ump_fmj = AmmoType(name=".45 ACP FMJ (UMP45)", description="FMJ", weight=1.5,
    ballistic_data=_bd([(3.2, 5), (3.0, 5), (2.6, 4), (2.0, 4), (1.5, 3), (0.7, 2), (0.3, 1), (0.15, 1)], beyond_from=100))
ammo_45_ump_jhp = AmmoType(name=".45 ACP JHP (UMP45)", description="JHP", weight=1.5,
    ballistic_data=_bd([(3.0, 7), (2.8, 7), (2.4, 6), (1.9, 5), (1.4, 4), (0.65, 2), (0.28, 1), (0.14, 1)], beyond_from=100))
ammo_45_ump_ap = AmmoType(name=".45 ACP AP (UMP45)", description="AP", weight=1.5,
    ballistic_data=_bd([(4.5, 5), (4.2, 4), (3.6, 4), (2.8, 3), (2.1, 3), (0.95, 2), (0.4, 1), (0.2, 1)], beyond_from=100))

ump45_ballistic = WeaponBallisticData(
    minimum_arc=_rd([0.45, 0.85, 1.5, 2.5, 4.5, 8.0, 12.0, 16.0]),
    ballistic_accuracy=_rd([46, 37, 28, 21, 16, 6, 1, -2]),
    time_of_flight=_rd([0, 1, 2, 4, 6, 14, 23, 34]),
)

hk_ump45 = Weapon(
    name="Heckler & Koch UMP45", weight=5.4,
    description="German .45 ACP SMG successor concept to the MP5 for US markets. Lower ROF and controllable recoil (Interpolated from MAC 10 .45 ACP + HK MP5).",
    caliber=Caliber.CAL_45_ACP, weapon_type=WeaponType.SUB_MACHINEGUN, country=Country.GERMANY,
    length_deployed=27.0, length_folded=18.0, reload_time=8, self_loading_action=True, full_auto=True,
    full_auto_rof=5, ammo_capacity=25, ammo_weight=1.5, ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=5, sustained_auto_burst=3,
    aim_time_modifiers={1: -21, 2: -11, 3: -8, 4: -6, 5: -5, 6: -4, 7: -3, 8: -2, 9: -1},
    ammunition_types=[ammo_45_ump_fmj, ammo_45_ump_jhp, ammo_45_ump_ap],
    ballistic_data=ump45_ballistic,
)

# ============================================================================
# Wave 2b — existing calibers + combat-proven role duplicates
# ============================================================================

# L85A2 ← Enfield IW (HK reliability rebuild, same 5.56 bullpup)
ammo_556nato_l85a2_fmj = AmmoType(name="5.56mm NATO FMJ (L85A2)", description="FMJ", weight=1.0,
    ballistic_data=_bd([(16.0, 6), (16.0, 6), (14.0, 6), (13.0, 6), (11.0, 5), (7.5, 4), (4.9, 3), (3.3, 2)]))
ammo_556nato_l85a2_jhp = AmmoType(name="5.56mm NATO JHP (L85A2)", description="JHP", weight=1.0,
    ballistic_data=_bd([(16.0, 8), (15.0, 8), (14.0, 8), (12.0, 7), (11.0, 7), (7.2, 6), (4.7, 5), (3.1, 4)]))
ammo_556nato_l85a2_ap = AmmoType(name="5.56mm NATO AP (L85A2)", description="AP", weight=1.0,
    ballistic_data=_bd([(23.0, 6), (22.0, 6), (20.0, 6), (18.0, 5), (16.0, 5), (11.0, 4), (7.0, 3), (4.6, 2)]))

l85a2_ballistic = WeaponBallisticData(
    minimum_arc=_rd([0.3, 0.6, 1.0, 2.0, 3.0, 6.0, 9.0, 13.0]),
    ballistic_accuracy=_rd([62, 54, 45, 38, 33, 23, 18, 14]),
    time_of_flight=_rd([0, 0, 1, 1, 2, 5, 8, 11]),
)

l85a2 = Weapon(
    name="L85A2", weight=9.0,
    description="British SA80 bullpup rebuilt by Heckler & Koch. Standard UK service rifle in Iraq and Afghanistan (Interpolated from Enfield IW + HK416 reliability).",
    caliber=Caliber.CAL_556_NATO, weapon_type=WeaponType.ASSAULT_RIFLE, country=Country.UK,
    length_deployed=31.0, reload_time=8, self_loading_action=True, full_auto=True,
    full_auto_rof=6, ammo_capacity=30, ammo_weight=1.0, ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=4, sustained_auto_burst=3,
    aim_time_modifiers={1: -22, 2: -12, 3: -8, 4: -6, 5: -5, 6: -4, 7: -3, 8: -2, 9: -1, 10: 0, 11: 1},
    ammunition_types=[ammo_556nato_l85a2_fmj, ammo_556nato_l85a2_jhp, ammo_556nato_l85a2_ap],
    ballistic_data=l85a2_ballistic, built_in_optics=True,
)

# Tavor X95 ← Steyr AUG (compact Israeli bullpup)
ammo_556nato_x95_fmj = AmmoType(name="5.56mm NATO FMJ (Tavor X95)", description="FMJ", weight=1.0,
    ballistic_data=_bd([(14.5, 6), (13.5, 6), (12.5, 6), (11.0, 5), (9.5, 5), (6.0, 4), (3.8, 3), (2.4, 2)]))
ammo_556nato_x95_jhp = AmmoType(name="5.56mm NATO JHP (Tavor X95)", description="JHP", weight=1.0,
    ballistic_data=_bd([(14.0, 8), (13.5, 8), (12.0, 7), (10.5, 7), (9.0, 7), (5.7, 6), (3.6, 4), (2.3, 3)]))
ammo_556nato_x95_ap = AmmoType(name="5.56mm NATO AP (Tavor X95)", description="AP", weight=1.0,
    ballistic_data=_bd([(20.0, 6), (19.0, 6), (17.0, 6), (15.0, 5), (13.0, 5), (8.3, 3), (5.3, 3), (3.3, 2)]))

x95_ballistic = WeaponBallisticData(
    minimum_arc=_rd([0.25, 0.55, 1.1, 2.1, 2.5, 5.5, 8.0, 11.0]),
    ballistic_accuracy=_rd([60, 51, 42, 35, 30, 20, 15, 11]),
    time_of_flight=_rd([0, 0, 1, 1, 2, 5, 8, 12]),
)

tavor_x95 = Weapon(
    name="Tavor X95", weight=7.5,
    description="Israeli Micro-Tavor bullpup carbine. Compact CQB service rifle for IDF and export (Interpolated from Steyr AUG + M4A1 length).",
    caliber=Caliber.CAL_556_NATO, weapon_type=WeaponType.CARBINE, country=Country.ISRAEL,
    length_deployed=23.0, reload_time=8, self_loading_action=True, full_auto=True,
    full_auto_rof=7, ammo_capacity=30, ammo_weight=1.0, ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=4, sustained_auto_burst=3,
    aim_time_modifiers={1: -21, 2: -11, 3: -8, 4: -6, 5: -5, 6: -4, 7: -3, 8: -2, 9: -1, 10: 0},
    ammunition_types=[ammo_556nato_x95_fmj, ammo_556nato_x95_jhp, ammo_556nato_x95_ap],
    ballistic_data=x95_ballistic,
)

# QBZ-95 ← AUG platform; native 5.8x42 DBP87 (not export QBZ-97 5.56)
# Ballistics between AK-74 5.45 and M16A2 5.56 — 5.8 retains energy slightly better than 5.45
ammo_58x42_qbz95_fmj = AmmoType(name="5.8x42mm FMJ (DBP87)", description="FMJ", weight=1.0,
    ballistic_data=_bd([(15.5, 6), (15.0, 6), (13.5, 6), (11.5, 5), (10.5, 5), (6.8, 4), (4.4, 3), (2.9, 2)]))
ammo_58x42_qbz95_jhp = AmmoType(name="5.8x42mm JHP (QBZ-95)", description="JHP", weight=1.0,
    ballistic_data=_bd([(15.0, 8), (14.5, 8), (13.0, 7), (11.0, 7), (10.0, 7), (6.5, 6), (4.2, 5), (2.75, 3)]))
ammo_58x42_qbz95_ap = AmmoType(name="5.8x42mm AP (DBP10)", description="AP", weight=1.0,
    ballistic_data=_bd([(21.5, 6), (20.5, 6), (19.0, 6), (16.5, 5), (14.5, 5), (9.6, 4), (6.2, 3), (4.05, 2)]))

qbz95_ballistic = WeaponBallisticData(
    minimum_arc=_rd([0.3, 0.65, 1.5, 2.5, 3.0, 6.5, 9.5, 13.0]),
    ballistic_accuracy=_rd([60, 51, 42, 35, 30, 20, 15, 11]),
    time_of_flight=_rd([0, 0, 1, 1, 2, 5, 8, 11]),
)

qbz_95 = Weapon(
    name="QBZ-95", weight=7.9,
    description="Chinese PLA Type 95 bullpup assault rifle in 5.8x42mm. Standard PLA issue (Interpolated from Steyr AUG / FA MAS handling; ammo between AK-74 5.45 and M16A2 5.56). Export QBZ-97 is the 5.56 variant.",
    caliber=Caliber.CAL_58X42, weapon_type=WeaponType.ASSAULT_RIFLE, country=Country.CHINA,
    length_deployed=29.0, reload_time=8, self_loading_action=True, full_auto=True,
    full_auto_rof=6, ammo_capacity=30, ammo_weight=1.0, ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=4, sustained_auto_burst=3,
    aim_time_modifiers={1: -23, 2: -12, 3: -9, 4: -7, 5: -6, 6: -5, 7: -4, 8: -3, 9: -2, 10: -1, 11: 0},
    ammunition_types=[ammo_58x42_qbz95_fmj, ammo_58x42_qbz95_jhp, ammo_58x42_qbz95_ap],
    ballistic_data=qbz95_ballistic,
)

# Galil ACE ← Galil AR 5.56 (lighter modernized export)
ammo_556nato_ace_fmj = AmmoType(name="5.56mm NATO FMJ (Galil ACE)", description="FMJ", weight=1.2,
    ballistic_data=_bd([(16.0, 6), (15.0, 6), (14.0, 6), (12.0, 6), (11.0, 5), (6.8, 4), (4.3, 3), (2.7, 2)]))
ammo_556nato_ace_jhp = AmmoType(name="5.56mm NATO JHP (Galil ACE)", description="JHP", weight=1.2,
    ballistic_data=_bd([(15.0, 8), (15.0, 8), (13.0, 8), (12.0, 7), (10.0, 7), (6.5, 6), (4.1, 5), (2.6, 3)]))
ammo_556nato_ace_ap = AmmoType(name="5.56mm NATO AP (Galil ACE)", description="AP", weight=1.2,
    ballistic_data=_bd([(22.0, 6), (21.0, 6), (20.0, 6), (17.0, 5), (15.0, 5), (9.5, 4), (6.1, 3), (3.9, 2)]))

galil_ace_ballistic = WeaponBallisticData(
    minimum_arc=_rd([0.2, 0.5, 0.9, 2.0, 2.0, 5.0, 7.0, 9.0]),
    ballistic_accuracy=_rd([61, 52, 43, 36, 31, 21, 16, 12]),
    time_of_flight=_rd([0, 0, 1, 1, 2, 5, 7, 11]),
)

galil_ace = Weapon(
    name="Galil ACE", weight=7.9,
    description="Modernized Galil export rifle with polymer furniture and Picatinny rails. Used by Colombia, Chile, and other forces (Interpolated from Galil AR 5.56mm + AK-74M ergonomics).",
    caliber=Caliber.CAL_556_NATO, weapon_type=WeaponType.ASSAULT_RIFLE, country=Country.ISRAEL,
    length_deployed=36.0, length_folded=27.0, reload_time=8, self_loading_action=True, full_auto=True,
    full_auto_rof=5, ammo_capacity=35, ammo_weight=1.2, ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=4, sustained_auto_burst=3,
    aim_time_modifiers={1: -22, 2: -12, 3: -9, 4: -7, 5: -5, 6: -4, 7: -3, 8: -2, 9: -1, 10: 0, 11: 1},
    ammunition_types=[ammo_556nato_ace_fmj, ammo_556nato_ace_jhp, ammo_556nato_ace_ap],
    ballistic_data=galil_ace_ballistic,
)

# CZ Bren 2 ← FNC / SIG 550
ammo_556nato_bren2_fmj = AmmoType(name="5.56mm NATO FMJ (CZ Bren 2)", description="FMJ", weight=1.0,
    ballistic_data=_bd([(15.5, 6), (15.0, 6), (13.5, 6), (12.0, 6), (10.5, 5), (6.7, 4), (4.35, 3), (2.8, 2)]))
ammo_556nato_bren2_jhp = AmmoType(name="5.56mm NATO JHP (CZ Bren 2)", description="JHP", weight=1.0,
    ballistic_data=_bd([(15.0, 8), (14.0, 8), (13.0, 7), (11.5, 7), (9.85, 7), (6.45, 6), (4.15, 5), (2.7, 3)]))
ammo_556nato_bren2_ap = AmmoType(name="5.56mm NATO AP (CZ Bren 2)", description="AP", weight=1.0,
    ballistic_data=_bd([(21.5, 6), (21.0, 6), (19.0, 6), (16.5, 5), (14.5, 5), (9.5, 4), (6.1, 3), (3.95, 2)]))

bren2_ballistic = WeaponBallisticData(
    three_round_burst=_rd([-5, 0, 4, 8, 11, 16, 19, 21]),
    minimum_arc=_rd([0.3, 0.6, 1.0, 2.0, 3.0, 6.0, 9.5, 12.5]),
    ballistic_accuracy=_rd([61, 52, 43, 36, 31, 21, 16, 12]),
    time_of_flight=_rd([0, 0, 1, 1, 2, 5, 8, 11]),
)

cz_bren_2 = Weapon(
    name="CZ Bren 2", weight=7.3,
    description="Czech modular assault rifle replacing the vz. 58 lineage in Czech service and exported widely (Interpolated from FN FNC + SIG 550).",
    caliber=Caliber.CAL_556_NATO, weapon_type=WeaponType.ASSAULT_RIFLE, country=Country.CZECH_REPUBLIC,
    length_deployed=35.0, length_folded=26.0, reload_time=8, self_loading_action=True, full_auto=True,
    full_auto_rof=7, ammo_capacity=30, ammo_weight=1.0, ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=4, sustained_auto_burst=3,
    aim_time_modifiers={1: -22, 2: -12, 3: -9, 4: -7, 5: -5, 6: -4, 7: -3, 8: -2, 9: -1, 10: 0, 11: 1},
    ammunition_types=[ammo_556nato_bren2_fmj, ammo_556nato_bren2_jhp, ammo_556nato_bren2_ap],
    ballistic_data=bren2_ballistic,
)

# AGS-30 ← AGS-17 (lighter successor)
ammo_30mm_he_ags30 = AmmoType(
    name="30mm HE (VOG-17/VOG-30) (AGS-30)",
    description="HE",
    weight=20.0,
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

ags_30 = Weapon(
    name="AGS-30 Atlant", weight=35.0,
    description="Lightweight Russian automatic grenade launcher replacing AGS-17. Same 30mm VOG ammunition, much lighter mount (Interpolated from AGS-17 Plamya).",
    caliber=Caliber.CAL_30MM_VOG, weapon_type=WeaponType.AUTOMATIC_GRENADE_LAUNCHER, country=Country.RUSSIA,
    length_deployed=33.0, reload_time=14, self_loading_action=True, full_auto=True,
    full_auto_rof=1, ammo_capacity=29, ammo_weight=20.0, ammo_feed_device=AmmoFeedDevice.BELT,
    knock_down=0, sustained_auto_burst=1,
    aim_time_modifiers={1: -36, 2: -26, 3: -20, 4: -16, 5: -13, 6: -9, 7: -7, 8: -5, 9: -4, 10: -3, 11: -2, 12: -1, 13: 0},
    ammunition_types=[ammo_30mm_he_ags30],
    ballistic_data=WeaponBallisticData(
        minimum_arc=[RangeData(40, 0.2), RangeData(100, 0.4), RangeData(200, 0.8), RangeData(400, 2.0)],
        ballistic_accuracy=[RangeData(40, 33), RangeData(100, 20), RangeData(200, 10), RangeData(400, 1)],
        time_of_flight=[RangeData(40, 4), RangeData(100, 11), RangeData(200, 24), RangeData(400, 57)],
    ),
    built_in_bipod=True,
)

# RPG-29 ← RPG-7V tandem (105mm PG-29V)
ammo_105mm_heat_rpg29 = AmmoType(
    name="105mm HEAT tandem (RPG-29)",
    description="HEAT",
    weight=14.5,
    ballistic_data=[
        BallisticData(range_hexes=r, penetration=22000, damage_class=10)
        for r in [40, 100, 200, 400]
    ],
    explosive_data=[
        ExplosiveData(range_hexes=0, shrapnel_penetration=8.5, shrapnel_damage_class=9, base_shrapnel_hit_chance="12", base_concussion=2800),
        ExplosiveData(range_hexes=1, shrapnel_penetration=8.3, shrapnel_damage_class=9, base_shrapnel_hit_chance="2", base_concussion=520),
        ExplosiveData(range_hexes=2, shrapnel_penetration=8.0, shrapnel_damage_class=8, base_shrapnel_hit_chance="0", base_concussion=140),
        ExplosiveData(range_hexes=3, shrapnel_penetration=7.6, shrapnel_damage_class=8, base_shrapnel_hit_chance="0", base_concussion=70),
        ExplosiveData(range_hexes=5, shrapnel_penetration=7.0, shrapnel_damage_class=8, base_shrapnel_hit_chance="0", base_concussion=30),
        ExplosiveData(range_hexes=10, shrapnel_penetration=5.8, shrapnel_damage_class=7, base_shrapnel_hit_chance="0", base_concussion=10),
    ],
)

rpg_29 = Weapon(
    name="RPG-29 Vampire", weight=27.5,
    description="Russian reloadable tandem HEAT rocket launcher used against modern armor in Chechnya, Iraq, and Syria (Interpolated from RPG 7V with higher tandem penetration).",
    caliber=Caliber.CAL_105MM, weapon_type=WeaponType.ROCKET_PROPELLED_GRENADE_LAUNCHER, country=Country.RUSSIA,
    length_deployed=73.0, length_folded=39.0, reload_time=18, self_loading_action=False,
    ammo_capacity=1, ammo_weight=14.5, ammo_feed_device=AmmoFeedDevice.ROUND,
    ammunition_types=[ammo_105mm_heat_rpg29],
    aim_time_modifiers={1: -29, 2: -19, 3: -12, 4: -9, 5: -7, 6: -6, 7: -5, 8: -4, 9: -3, 10: -2, 11: -1, 12: 0},
    ballistic_data=WeaponBallisticData(
        angle_of_impact=[RangeData(40, 0), RangeData(100, 0), RangeData(200, 1), RangeData(400, 2)],
        ballistic_accuracy=[RangeData(40, 16), RangeData(100, 5), RangeData(200, -5), RangeData(400, -14)],
        time_of_flight=[RangeData(40, 2), RangeData(100, 6), RangeData(200, 13), RangeData(400, 28)],
    ),
)

# IWI Negev ← M249
ammo_556nato_negev_fmj = AmmoType(name="5.56mm NATO FMJ (Negev)", description="FMJ", weight=6.5,
    ballistic_data=_bd([(15.0, 6), (15.0, 6), (14.0, 6), (12.0, 6), (11.0, 5), (7.0, 4), (4.6, 3), (3.0, 2)]))
ammo_556nato_negev_jhp = AmmoType(name="5.56mm NATO JHP (Negev)", description="JHP", weight=6.5,
    ballistic_data=_bd([(15.0, 8), (14.0, 8), (13.0, 7), (12.0, 7), (10.0, 7), (6.7, 6), (4.4, 5), (2.9, 3)]))
ammo_556nato_negev_ap = AmmoType(name="5.56mm NATO AP (Negev)", description="AP", weight=6.5,
    ballistic_data=_bd([(22.0, 6), (21.0, 6), (19.0, 6), (17.0, 5), (15.0, 5), (9.9, 4), (6.5, 3), (4.3, 2)]))

negev_ballistic = WeaponBallisticData(
    minimum_arc=_rd([0.2, 0.3, 0.7, 1.0, 2.0, 3.0, 5.0, 7.0]),
    ballistic_accuracy=_rd([61, 53, 44, 37, 32, 22, 17, 13]),
    time_of_flight=_rd([0, 0, 1, 2, 2, 5, 8, 11]),
)

iwi_negev = Weapon(
    name="IWI Negev", weight=16.3,
    description="Israeli 5.56mm light machine gun, belt or magazine fed. IDF squad automatic weapon (Interpolated from M249 Minimi).",
    caliber=Caliber.CAL_556_NATO, weapon_type=WeaponType.LIGHT_MACHINE_GUN, country=Country.ISRAEL,
    length_deployed=40.0, length_folded=31.0, reload_time=12, self_loading_action=True, full_auto=True,
    full_auto_rof=7, ammo_capacity=150, ammo_weight=6.5, ammo_feed_device=AmmoFeedDevice.BELT,
    knock_down=4, sustained_auto_burst=2,
    aim_time_modifiers={1: -27, 2: -17, 3: -11, 4: -8, 5: -7, 6: -5, 7: -4, 8: -3, 9: -2, 10: -1, 12: 0},
    ammunition_types=[ammo_556nato_negev_fmj, ammo_556nato_negev_jhp, ammo_556nato_negev_ap],
    ballistic_data=negev_ballistic, built_in_bipod=True,
)

# --- Combat-proven role duplicates ---

# M16A4 ← M16A2 (Iraq/Afghanistan flat-top)
ammo_556nato_m16a4_fmj = AmmoType(name="5.56mm NATO FMJ (M16A4)", description="FMJ", weight=1.0,
    ballistic_data=_bd([(17.0, 6), (16.0, 6), (15.0, 6), (13.0, 6), (12.0, 5), (7.7, 4), (5.1, 3), (3.4, 3)]))
ammo_556nato_m16a4_jhp = AmmoType(name="5.56mm NATO JHP (M16A4)", description="JHP", weight=1.0,
    ballistic_data=_bd([(16.0, 8), (15.0, 8), (14.0, 8), (13.0, 7), (11.0, 7), (7.4, 6), (4.9, 5), (3.2, 4)]))
ammo_556nato_m16a4_ap = AmmoType(name="5.56mm NATO AP (M16A4)", description="AP", weight=1.0,
    ballistic_data=_bd([(24.0, 6), (23.0, 6), (21.0, 6), (18.0, 5), (16.0, 5), (11.0, 4), (7.2, 3), (4.8, 2)]))

m16a4_ballistic = WeaponBallisticData(
    three_round_burst=_rd([-6, -1, 4, 8, 11, 16, 19, 21]),
    minimum_arc=_rd([0.4, 0.8, 2.0, 3.0, 4.0, 8.0, 11.0, 15.0]),
    ballistic_accuracy=_rd([61, 53, 44, 37, 32, 22, 17, 13]),
    time_of_flight=_rd([0, 0, 1, 1, 2, 5, 7, 11]),
)

m16a4 = Weapon(
    name="M16A4", weight=8.8,
    description="USMC flat-top M16 with RIS rails and ACOG-era optics. Iconic Iraq and Afghanistan service rifle (Interpolated from M16A2 + Mk 12 optics role).",
    caliber=Caliber.CAL_556_NATO, weapon_type=WeaponType.ASSAULT_RIFLE, country=Country.USA,
    length_deployed=39.5, reload_time=8, self_loading_action=True, full_auto=True,
    full_auto_rof=7, ammo_capacity=30, ammo_weight=1.0, ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=4, sustained_auto_burst=3,
    aim_time_modifiers={1: -22, 2: -12, 3: -9, 4: -7, 5: -5, 6: -4, 7: -3, 8: -2, 9: -1, 10: 0, 11: 1},
    ammunition_types=[ammo_556nato_m16a4_fmj, ammo_556nato_m16a4_jhp, ammo_556nato_m16a4_ap],
    ballistic_data=m16a4_ballistic, built_in_optics=True,
)

# L115A3 ← MRAD-class .338 (Accuracy International AWM; chambered in .338 Lapua Magnum)
ammo_338_l115_fmj = AmmoType(name=".338 Lapua Mag FMJ (L115A3)", description="FMJ", weight=1.0,
    ballistic_data=_bd([(32.0, 9), (31.0, 9), (29.0, 9), (27.0, 9), (25.0, 9), (20.0, 8), (16.0, 8), (12.0, 7)], beyond_from=None))
ammo_338_l115_jhp = AmmoType(name=".338 Lapua Mag JHP (L115A3)", description="JHP", weight=1.0,
    ballistic_data=_bd([(30.0, 10), (29.0, 10), (27.0, 10), (26.0, 10), (24.0, 10), (19.0, 9), (15.0, 9), (11.0, 8)], beyond_from=None))
ammo_338_l115_ap = AmmoType(name=".338 Lapua Mag AP (L115A3)", description="AP", weight=1.0,
    ballistic_data=_bd([(45.0, 9), (44.0, 9), (41.0, 9), (38.0, 9), (35.0, 8), (28.0, 8), (22.0, 7), (17.0, 7)], beyond_from=None))

l115a3_ballistic = WeaponBallisticData(
    ballistic_accuracy=_rd([71, 63, 54, 47, 42, 33, 27, 23]),
    time_of_flight=_rd([0, 0, 1, 1, 2, 4, 7, 10]),
)

l115a3 = Weapon(
    name="Accuracy International L115A3", weight=15.2,
    description="British .338 Lapua Magnum bolt-action sniper rifle (AWM lineage). Famous for long-range engagements in Afghanistan (Interpolated from Barrett MRAD .338 tables + Walther 2000 bolt handling).",
    caliber=Caliber.CAL_338_LAPUA_MAG, weapon_type=WeaponType.SNIPER_RIFLE, country=Country.UK,
    length_deployed=51.0, reload_time=16, self_loading_action=False, full_auto=False, actions_to_cycle=3,
    ammo_capacity=5, ammo_weight=1.0, ammo_feed_device=AmmoFeedDevice.MAGAZINE,
    knock_down=16, sustained_auto_burst=5,
    aim_time_modifiers={1: -27, 2: -17, 3: -9, 4: -7, 5: -5, 6: -3, 7: -1, 8: 0, 9: 1, 10: 2, 12: 5},
    ammunition_types=[ammo_338_l115_fmj, ammo_338_l115_jhp, ammo_338_l115_ap],
    ballistic_data=l115a3_ballistic, built_in_optics=True, built_in_bipod=True,
)

# Carl Gustaf M3 ← AT4 / LAW 80 (reloadable 84mm)
ammo_84mm_heat_cg = AmmoType(
    name="84mm HEAT (Carl Gustaf)",
    description="HEAT",
    weight=7.0,
    ballistic_data=[
        BallisticData(range_hexes=r, penetration=14000, damage_class=10)
        for r in [40, 100, 200, 400]
    ],
    explosive_data=[
        ExplosiveData(range_hexes=0, shrapnel_penetration=7.2, shrapnel_damage_class=8, base_shrapnel_hit_chance="12", base_concussion=2000),
        ExplosiveData(range_hexes=1, shrapnel_penetration=7.0, shrapnel_damage_class=8, base_shrapnel_hit_chance="2", base_concussion=400),
        ExplosiveData(range_hexes=2, shrapnel_penetration=6.7, shrapnel_damage_class=8, base_shrapnel_hit_chance="0", base_concussion=105),
        ExplosiveData(range_hexes=3, shrapnel_penetration=6.4, shrapnel_damage_class=8, base_shrapnel_hit_chance="0", base_concussion=52),
        ExplosiveData(range_hexes=5, shrapnel_penetration=5.8, shrapnel_damage_class=7, base_shrapnel_hit_chance="0", base_concussion=22),
        ExplosiveData(range_hexes=10, shrapnel_penetration=4.8, shrapnel_damage_class=6, base_shrapnel_hit_chance="0", base_concussion=8),
    ],
)
ammo_84mm_he_cg = AmmoType(
    name="84mm HE (Carl Gustaf)",
    description="HE",
    weight=7.0,
    ballistic_data=[
        BallisticData(range_hexes=r, penetration=10.0, damage_class=10)
        for r in [40, 100, 200, 400]
    ],
    explosive_data=[
        ExplosiveData(range_hexes=0, shrapnel_penetration=8.5, shrapnel_damage_class=9, base_shrapnel_hit_chance="12", base_concussion=2600),
        ExplosiveData(range_hexes=1, shrapnel_penetration=8.2, shrapnel_damage_class=9, base_shrapnel_hit_chance="2", base_concussion=480),
        ExplosiveData(range_hexes=2, shrapnel_penetration=7.8, shrapnel_damage_class=9, base_shrapnel_hit_chance="0", base_concussion=125),
        ExplosiveData(range_hexes=3, shrapnel_penetration=7.4, shrapnel_damage_class=8, base_shrapnel_hit_chance="0", base_concussion=62),
        ExplosiveData(range_hexes=5, shrapnel_penetration=6.8, shrapnel_damage_class=8, base_shrapnel_hit_chance="0", base_concussion=26),
        ExplosiveData(range_hexes=10, shrapnel_penetration=5.5, shrapnel_damage_class=7, base_shrapnel_hit_chance="0", base_concussion=9),
    ],
)

carl_gustaf_m3 = Weapon(
    name="Carl Gustaf M3", weight=22.0,
    description="Swedish reloadable 84mm recoilless rifle (US M3 MAAWS). Widely used by US and NATO infantry in Afghanistan and later conflicts (Interpolated from AT4 + LAW 80; reloadable).",
    caliber=Caliber.CAL_84MM, weapon_type=WeaponType.ROCKET_PROPELLED_GRENADE_LAUNCHER, country=Country.SWEDEN,
    length_deployed=42.0, reload_time=16, self_loading_action=False,
    ammo_capacity=1, ammo_weight=7.0, ammo_feed_device=AmmoFeedDevice.ROUND,
    ammunition_types=[ammo_84mm_heat_cg, ammo_84mm_he_cg],
    aim_time_modifiers={1: -26, 2: -16, 3: -10, 4: -8, 5: -6, 6: -5, 7: -4, 8: -3, 9: -2, 10: -1},
    ballistic_data=WeaponBallisticData(
        angle_of_impact=[RangeData(40, 0), RangeData(100, 0), RangeData(200, 1), RangeData(400, 2)],
        ballistic_accuracy=[RangeData(40, 12), RangeData(100, 0), RangeData(200, -10), RangeData(400, -19)],
        time_of_flight=[RangeData(40, 4), RangeData(100, 12), RangeData(200, 28), RangeData(400, 70)],
    ),
)

MODERN_WEAPONS = [
    ak_74m, ak_103, ak_105, ak_12,
    fn_scar_l, fn_scar_h, hk_g36, m27_iar, mk14_ebr,
    pkp_pecheneg, kord, sv_98, pp19_01_vityaz, mp443_grach,
    glock_17, m240b, benelli_m4, at4,
    as_val, vss_vintorez, hk_mp7, fn_p90, fn_five_seven, hk_ump45,
    l85a2, tavor_x95, qbz_95, galil_ace, cz_bren_2, ags_30, rpg_29, iwi_negev,
    m16a4, l115a3, carl_gustaf_m3,
]
