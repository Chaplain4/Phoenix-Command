from phoenix_command.models.enums import Country, GrenadeType
from phoenix_command.models.gear import Grenade, ExplosiveData

hg_78 = Grenade(
    name="HG 78 Frag Grenade",
    country=Country.AUSTRIA,
    grenade_type=GrenadeType.FRAG,
    weight=1.2,
    length=4.5,
    arm_time=3,
    fuse_length=2,
    range=14,
    explosive_data=[
        ExplosiveData(range_hexes=None, shrapnel_penetration=2.6, shrapnel_damage_class=10, base_shrapnel_hit_chance="*2000", base_concussion=6000),
        ExplosiveData(range_hexes=0, shrapnel_penetration=1.4, shrapnel_damage_class=1, base_shrapnel_hit_chance="*23", base_concussion=414),
        ExplosiveData(range_hexes=1, shrapnel_penetration=1.2, shrapnel_damage_class=1, base_shrapnel_hit_chance="*6", base_concussion=114),
        ExplosiveData(range_hexes=2, shrapnel_penetration=0.8, shrapnel_damage_class=1, base_shrapnel_hit_chance="*1", base_concussion=35),
        ExplosiveData(range_hexes=3, shrapnel_penetration=0.6, shrapnel_damage_class=1, base_shrapnel_hit_chance="64", base_concussion=18),
        ExplosiveData(range_hexes=5, shrapnel_penetration=0.3, shrapnel_damage_class=1, base_shrapnel_hit_chance="22", base_concussion=8),
        ExplosiveData(range_hexes=10, shrapnel_penetration=0.0, shrapnel_damage_class=0, base_shrapnel_hit_chance="0", base_concussion=3)
    ]
)

of_hg_78 = Grenade(
    name="OF HG 78 Blast Grenade",
    country=Country.AUSTRIA,
    grenade_type=GrenadeType.BLAST,
    weight=0.5,
    length=4.5,
    arm_time=3,
    fuse_length=2,
    range=21,
    explosive_data=[
        ExplosiveData(range_hexes=None, shrapnel_penetration=2.6, shrapnel_damage_class=10, base_shrapnel_hit_chance="0", base_concussion=6000),
        ExplosiveData(range_hexes=0, shrapnel_penetration=0.0, shrapnel_damage_class=0, base_shrapnel_hit_chance="0", base_concussion=414),
        ExplosiveData(range_hexes=1, shrapnel_penetration=0.0, shrapnel_damage_class=0, base_shrapnel_hit_chance="0", base_concussion=114),
        ExplosiveData(range_hexes=2, shrapnel_penetration=0.0, shrapnel_damage_class=0, base_shrapnel_hit_chance="0", base_concussion=35),
        ExplosiveData(range_hexes=3, shrapnel_penetration=0.0, shrapnel_damage_class=0, base_shrapnel_hit_chance="0", base_concussion=18),
        ExplosiveData(range_hexes=5, shrapnel_penetration=0.0, shrapnel_damage_class=0, base_shrapnel_hit_chance="0", base_concussion=8),
        ExplosiveData(range_hexes=10, shrapnel_penetration=0.0, shrapnel_damage_class=0, base_shrapnel_hit_chance="0", base_concussion=3)
    ]
)

hg_80 = Grenade(
    name="HG 80 Mini Grenade",
    country=Country.AUSTRIA,
    grenade_type=GrenadeType.FRAG,
    weight=0.4,
    length=3.0,
    arm_time=3,
    fuse_length=2,
    range=25,
    explosive_data=[
        ExplosiveData(range_hexes=None, shrapnel_penetration=1.6, shrapnel_damage_class=10, base_shrapnel_hit_chance="*300", base_concussion=1400),
        ExplosiveData(range_hexes=0, shrapnel_penetration=1.4, shrapnel_damage_class=1, base_shrapnel_hit_chance="*4", base_concussion=158),
        ExplosiveData(range_hexes=1, shrapnel_penetration=1.2, shrapnel_damage_class=1, base_shrapnel_hit_chance="*1", base_concussion=49),
        ExplosiveData(range_hexes=2, shrapnel_penetration=0.8, shrapnel_damage_class=1, base_shrapnel_hit_chance="25", base_concussion=16),
        ExplosiveData(range_hexes=3, shrapnel_penetration=0.6, shrapnel_damage_class=1, base_shrapnel_hit_chance="11", base_concussion=8),
        ExplosiveData(range_hexes=5, shrapnel_penetration=0.3, shrapnel_damage_class=1, base_shrapnel_hit_chance="3", base_concussion=4),
        ExplosiveData(range_hexes=10, shrapnel_penetration=0.0, shrapnel_damage_class=1, base_shrapnel_hit_chance="1", base_concussion=1)
    ]
)

nr_423 = Grenade(
    name="NR 423 Frag Grenade",
    country=Country.BELGIUM,
    grenade_type=GrenadeType.FRAG,
    weight=0.5,
    length=3.2,
    arm_time=3,
    fuse_length=2,
    range=21,
    explosive_data=[
        ExplosiveData(range_hexes=None, shrapnel_penetration=2.5, shrapnel_damage_class=10, base_shrapnel_hit_chance="*300", base_concussion=5200),
        ExplosiveData(range_hexes=0, shrapnel_penetration=1.8, shrapnel_damage_class=2, base_shrapnel_hit_chance="*4", base_concussion=376),
        ExplosiveData(range_hexes=1, shrapnel_penetration=1.6, shrapnel_damage_class=2, base_shrapnel_hit_chance="94", base_concussion=105),
        ExplosiveData(range_hexes=2, shrapnel_penetration=1.2, shrapnel_damage_class=1, base_shrapnel_hit_chance="23", base_concussion=33),
        ExplosiveData(range_hexes=3, shrapnel_penetration=1.0, shrapnel_damage_class=1, base_shrapnel_hit_chance="10", base_concussion=17),
        ExplosiveData(range_hexes=5, shrapnel_penetration=0.6, shrapnel_damage_class=1, base_shrapnel_hit_chance="3", base_concussion=7),
        ExplosiveData(range_hexes=10, shrapnel_penetration=0.0, shrapnel_damage_class=0, base_shrapnel_hit_chance="0", base_concussion=2)
    ]
)

nr_446 = Grenade(
    name="NR 446 Blast Grenade",
    country=Country.BELGIUM,
    grenade_type=GrenadeType.BLAST,
    weight=0.6,
    length=3.2,
    arm_time=3,
    fuse_length=2,
    range=20,
    explosive_data=[
        ExplosiveData(range_hexes=None, shrapnel_penetration=2.8, shrapnel_damage_class=10, base_shrapnel_hit_chance="0", base_concussion=7300),
        ExplosiveData(range_hexes=0, shrapnel_penetration=0.0, shrapnel_damage_class=0, base_shrapnel_hit_chance="0", base_concussion=468),
        ExplosiveData(range_hexes=1, shrapnel_penetration=0.0, shrapnel_damage_class=0, base_shrapnel_hit_chance="0", base_concussion=126),
        ExplosiveData(range_hexes=2, shrapnel_penetration=0.0, shrapnel_damage_class=0, base_shrapnel_hit_chance="0", base_concussion=39),
        ExplosiveData(range_hexes=3, shrapnel_penetration=0.0, shrapnel_damage_class=0, base_shrapnel_hit_chance="0", base_concussion=20),
        ExplosiveData(range_hexes=5, shrapnel_penetration=0.0, shrapnel_damage_class=0, base_shrapnel_hit_chance="0", base_concussion=9),
        ExplosiveData(range_hexes=10, shrapnel_penetration=0.0, shrapnel_damage_class=0, base_shrapnel_hit_chance="0", base_concussion=3)
    ]
)

type_59 = Grenade(
    name="Type 59 Frag Grenade",
    country=Country.CHINA,
    grenade_type=GrenadeType.FRAG,
    weight=0.7,
    length=4.5,
    arm_time=3,
    fuse_length=2,
    range=18,
    explosive_data=[
        ExplosiveData(range_hexes=None, shrapnel_penetration=3.1, shrapnel_damage_class=10, base_shrapnel_hit_chance="*200", base_concussion=9400),
        ExplosiveData(range_hexes=0, shrapnel_penetration=2.9, shrapnel_damage_class=3, base_shrapnel_hit_chance="*3", base_concussion=554),
        ExplosiveData(range_hexes=1, shrapnel_penetration=2.7, shrapnel_damage_class=3, base_shrapnel_hit_chance="69", base_concussion=145),
        ExplosiveData(range_hexes=2, shrapnel_penetration=2.3, shrapnel_damage_class=2, base_shrapnel_hit_chance="16", base_concussion=44),
        ExplosiveData(range_hexes=3, shrapnel_penetration=2.0, shrapnel_damage_class=2, base_shrapnel_hit_chance="7", base_concussion=22),
        ExplosiveData(range_hexes=5, shrapnel_penetration=1.4, shrapnel_damage_class=2, base_shrapnel_hit_chance="2", base_concussion=10),
        ExplosiveData(range_hexes=10, shrapnel_penetration=0.7, shrapnel_damage_class=1, base_shrapnel_hit_chance="0", base_concussion=3)
    ]
)

type_82 = Grenade(
    name="Type 82 Frag Grenade",
    country=Country.CHINA,
    grenade_type=GrenadeType.FRAG,
    weight=0.6,
    length=3.3,
    arm_time=5,
    fuse_length=2,
    range=20,
    explosive_data=[
        ExplosiveData(range_hexes=None, shrapnel_penetration=3.3, shrapnel_damage_class=10, base_shrapnel_hit_chance="*90", base_concussion=5300),
        ExplosiveData(range_hexes=0, shrapnel_penetration=3.2, shrapnel_damage_class=3, base_shrapnel_hit_chance="*1", base_concussion=383),
        ExplosiveData(range_hexes=1, shrapnel_penetration=2.9, shrapnel_damage_class=3, base_shrapnel_hit_chance="31", base_concussion=107),
        ExplosiveData(range_hexes=2, shrapnel_penetration=2.5, shrapnel_damage_class=3, base_shrapnel_hit_chance="7", base_concussion=33),
        ExplosiveData(range_hexes=3, shrapnel_penetration=2.2, shrapnel_damage_class=2, base_shrapnel_hit_chance="3", base_concussion=17),
        ExplosiveData(range_hexes=5, shrapnel_penetration=1.6, shrapnel_damage_class=2, base_shrapnel_hit_chance="0", base_concussion=7),
        ExplosiveData(range_hexes=10, shrapnel_penetration=0.8, shrapnel_damage_class=1, base_shrapnel_hit_chance="0", base_concussion=2)
    ]
)

df_37 = Grenade(
    name="DF 37 Frag Grenade",
    country=Country.FRANCE,
    grenade_type=GrenadeType.FRAG,
    weight=1.2,
    length=3.9,
    arm_time=3,
    fuse_length=2,
    range=14,
    explosive_data=[
        ExplosiveData(range_hexes=None, shrapnel_penetration=2.4, shrapnel_damage_class=10, base_shrapnel_hit_chance="*30", base_concussion=4900),
        ExplosiveData(range_hexes=0, shrapnel_penetration=1.9, shrapnel_damage_class=3, base_shrapnel_hit_chance="41", base_concussion=360),
        ExplosiveData(range_hexes=1, shrapnel_penetration=1.9, shrapnel_damage_class=3, base_shrapnel_hit_chance="10", base_concussion=101),
        ExplosiveData(range_hexes=2, shrapnel_penetration=1.7, shrapnel_damage_class=3, base_shrapnel_hit_chance="2", base_concussion=32),
        ExplosiveData(range_hexes=3, shrapnel_penetration=1.6, shrapnel_damage_class=3, base_shrapnel_hit_chance="0", base_concussion=16),
        ExplosiveData(range_hexes=5, shrapnel_penetration=1.4, shrapnel_damage_class=3, base_shrapnel_hit_chance="0", base_concussion=7),
        ExplosiveData(range_hexes=10, shrapnel_penetration=1.0, shrapnel_damage_class=2, base_shrapnel_hit_chance="0", base_concussion=2)
    ]
)

of_37 = Grenade(
    name="OF 37 Blast Grenade",
    country=Country.FRANCE,
    grenade_type=GrenadeType.BLAST,
    weight=0.3,
    length=3.7,
    arm_time=3,
    fuse_length=2,
    range=21,
    explosive_data=[
        ExplosiveData(range_hexes=None, shrapnel_penetration=2.8, shrapnel_damage_class=10, base_shrapnel_hit_chance="0", base_concussion=7700),
        ExplosiveData(range_hexes=0, shrapnel_penetration=0.0, shrapnel_damage_class=0, base_shrapnel_hit_chance="0", base_concussion=485),
        ExplosiveData(range_hexes=1, shrapnel_penetration=0.0, shrapnel_damage_class=0, base_shrapnel_hit_chance="0", base_concussion=130),
        ExplosiveData(range_hexes=2, shrapnel_penetration=0.0, shrapnel_damage_class=0, base_shrapnel_hit_chance="0", base_concussion=40),
        ExplosiveData(range_hexes=3, shrapnel_penetration=0.0, shrapnel_damage_class=0, base_shrapnel_hit_chance="0", base_concussion=20),
        ExplosiveData(range_hexes=5, shrapnel_penetration=0.0, shrapnel_damage_class=0, base_shrapnel_hit_chance="0", base_concussion=9),
        ExplosiveData(range_hexes=10, shrapnel_penetration=0.0, shrapnel_damage_class=0, base_shrapnel_hit_chance="0", base_concussion=3)
    ]
)

mdn_21 = Grenade(
    name="MDN 21 Frag Grenade",
    country=Country.WEST_GERMANY,
    grenade_type=GrenadeType.FRAG,
    weight=0.5,
    length=3.3,
    arm_time=3,
    fuse_length=2,
    range=21,
    explosive_data=[
        ExplosiveData(range_hexes=None, shrapnel_penetration=2.2, shrapnel_damage_class=10, base_shrapnel_hit_chance="*700", base_concussion=4000),
        ExplosiveData(range_hexes=0, shrapnel_penetration=1.4, shrapnel_damage_class=1, base_shrapnel_hit_chance="*9", base_concussion=316),
        ExplosiveData(range_hexes=1, shrapnel_penetration=1.2, shrapnel_damage_class=1, base_shrapnel_hit_chance="*2", base_concussion=91),
        ExplosiveData(range_hexes=2, shrapnel_penetration=0.8, shrapnel_damage_class=1, base_shrapnel_hit_chance="57", base_concussion=28),
        ExplosiveData(range_hexes=3, shrapnel_penetration=0.6, shrapnel_damage_class=1, base_shrapnel_hit_chance="25", base_concussion=15),
        ExplosiveData(range_hexes=5, shrapnel_penetration=0.3, shrapnel_damage_class=1, base_shrapnel_hit_chance="8", base_concussion=6),
        ExplosiveData(range_hexes=10, shrapnel_penetration=0.0, shrapnel_damage_class=0, base_shrapnel_hit_chance="0", base_concussion=2)
    ]
)

dm_51 = Grenade(
    name="DM 51 Frag Grenade",
    country=Country.WEST_GERMANY,
    grenade_type=GrenadeType.FRAG,
    weight=1.0,
    length=3.9,
    arm_time=3,
    fuse_length=2,
    range=15,
    explosive_data=[
        ExplosiveData(range_hexes=None, shrapnel_penetration=2.7, shrapnel_damage_class=10, base_shrapnel_hit_chance="*2000", base_concussion=6900),
        ExplosiveData(range_hexes=0, shrapnel_penetration=1.4, shrapnel_damage_class=1, base_shrapnel_hit_chance="*27", base_concussion=453),
        ExplosiveData(range_hexes=1, shrapnel_penetration=1.1, shrapnel_damage_class=1, base_shrapnel_hit_chance="*7", base_concussion=123),
        ExplosiveData(range_hexes=2, shrapnel_penetration=0.8, shrapnel_damage_class=1, base_shrapnel_hit_chance="*2", base_concussion=38),
        ExplosiveData(range_hexes=3, shrapnel_penetration=0.5, shrapnel_damage_class=1, base_shrapnel_hit_chance="75", base_concussion=19),
        ExplosiveData(range_hexes=5, shrapnel_penetration=0.0, shrapnel_damage_class=0, base_shrapnel_hit_chance="0", base_concussion=8),
        ExplosiveData(range_hexes=10, shrapnel_penetration=0.0, shrapnel_damage_class=0, base_shrapnel_hit_chance="0", base_concussion=3)
    ]
)

m26_a2_isr = Grenade(
    name="M26 A2 Frag Grenade",
    country=Country.ISRAEL,
    grenade_type=GrenadeType.FRAG,
    weight=0.9,
    length=4.2,
    arm_time=3,
    fuse_length=2,
    range=15,
    explosive_data=[
        ExplosiveData(range_hexes=None, shrapnel_penetration=3.3, shrapnel_damage_class=10, base_shrapnel_hit_chance="*300", base_concussion=13000),
        ExplosiveData(range_hexes=0, shrapnel_penetration=2.4, shrapnel_damage_class=2, base_shrapnel_hit_chance="*4", base_concussion=684),
        ExplosiveData(range_hexes=1, shrapnel_penetration=2.2, shrapnel_damage_class=2, base_shrapnel_hit_chance="*1", base_concussion=171),
        ExplosiveData(range_hexes=2, shrapnel_penetration=1.8, shrapnel_damage_class=2, base_shrapnel_hit_chance="25", base_concussion=51),
        ExplosiveData(range_hexes=3, shrapnel_penetration=1.5, shrapnel_damage_class=2, base_shrapnel_hit_chance="11", base_concussion=26),
        ExplosiveData(range_hexes=5, shrapnel_penetration=1.0, shrapnel_damage_class=1, base_shrapnel_hit_chance="3", base_concussion=11),
        ExplosiveData(range_hexes=10, shrapnel_penetration=0.4, shrapnel_damage_class=1, base_shrapnel_hit_chance="0", base_concussion=4)
    ]
)

blast_14 = Grenade(
    name="#14 Blast Grenade",
    country=Country.ISRAEL,
    grenade_type=GrenadeType.BLAST,
    weight=0.7,
    length=5.3,
    arm_time=3,
    fuse_length=2,
    range=18,
    explosive_data=[
        ExplosiveData(range_hexes=None, shrapnel_penetration=3.7, shrapnel_damage_class=10, base_shrapnel_hit_chance="0", base_concussion=17000),
        ExplosiveData(range_hexes=0, shrapnel_penetration=0.0, shrapnel_damage_class=0, base_shrapnel_hit_chance="0", base_concussion=840),
        ExplosiveData(range_hexes=1, shrapnel_penetration=0.0, shrapnel_damage_class=0, base_shrapnel_hit_chance="0", base_concussion=202),
        ExplosiveData(range_hexes=2, shrapnel_penetration=0.0, shrapnel_damage_class=0, base_shrapnel_hit_chance="0", base_concussion=59),
        ExplosiveData(range_hexes=3, shrapnel_penetration=0.0, shrapnel_damage_class=0, base_shrapnel_hit_chance="0", base_concussion=30),
        ExplosiveData(range_hexes=5, shrapnel_penetration=0.0, shrapnel_damage_class=0, base_shrapnel_hit_chance="0", base_concussion=13),
        ExplosiveData(range_hexes=10, shrapnel_penetration=0.0, shrapnel_damage_class=0, base_shrapnel_hit_chance="0", base_concussion=4)
    ]
)

mu_50 = Grenade(
    name="MU 50 Frag Grenade",
    country=Country.ITALY,
    grenade_type=GrenadeType.FRAG,
    weight=0.4,
    length=2.8,
    arm_time=3,
    fuse_length=2,
    range=23,
    explosive_data=[
        ExplosiveData(range_hexes=None, shrapnel_penetration=2.2, shrapnel_damage_class=10, base_shrapnel_hit_chance="*400", base_concussion=3600),
        ExplosiveData(range_hexes=0, shrapnel_penetration=1.4, shrapnel_damage_class=1, base_shrapnel_hit_chance="*6", base_concussion=295),
        ExplosiveData(range_hexes=1, shrapnel_penetration=1.2, shrapnel_damage_class=1, base_shrapnel_hit_chance="*1", base_concussion=85),
        ExplosiveData(range_hexes=2, shrapnel_penetration=0.8, shrapnel_damage_class=1, base_shrapnel_hit_chance="36", base_concussion=27),
        ExplosiveData(range_hexes=3, shrapnel_penetration=0.6, shrapnel_damage_class=1, base_shrapnel_hit_chance="15", base_concussion=14),
        ExplosiveData(range_hexes=5, shrapnel_penetration=0.3, shrapnel_damage_class=1, base_shrapnel_hit_chance="5", base_concussion=6),
        ExplosiveData(range_hexes=10, shrapnel_penetration=0.0, shrapnel_damage_class=0, base_shrapnel_hit_chance="0", base_concussion=2)
    ]
)

rgd_5 = Grenade(
    name="RGD 5 Frag Grenade",
    country=Country.USSR,
    grenade_type=GrenadeType.FRAG,
    weight=0.7,
    length=4.5,
    arm_time=3,
    fuse_length=2,
    range=18,
    explosive_data=[
        ExplosiveData(range_hexes=None, shrapnel_penetration=3.1, shrapnel_damage_class=10, base_shrapnel_hit_chance="*200", base_concussion=9400),
        ExplosiveData(range_hexes=0, shrapnel_penetration=2.9, shrapnel_damage_class=3, base_shrapnel_hit_chance="*3", base_concussion=554),
        ExplosiveData(range_hexes=1, shrapnel_penetration=2.7, shrapnel_damage_class=3, base_shrapnel_hit_chance="69", base_concussion=145),
        ExplosiveData(range_hexes=2, shrapnel_penetration=2.3, shrapnel_damage_class=2, base_shrapnel_hit_chance="16", base_concussion=44),
        ExplosiveData(range_hexes=3, shrapnel_penetration=2.0, shrapnel_damage_class=2, base_shrapnel_hit_chance="7", base_concussion=22),
        ExplosiveData(range_hexes=5, shrapnel_penetration=1.4, shrapnel_damage_class=2, base_shrapnel_hit_chance="2", base_concussion=10),
        ExplosiveData(range_hexes=10, shrapnel_penetration=0.7, shrapnel_damage_class=1, base_shrapnel_hit_chance="0", base_concussion=3)
    ]
)

rkg_3m = Grenade(
    name="RKG 3M Anti-Tank Grenade",
    country=Country.USSR,
    grenade_type=GrenadeType.ANTI_TANK,
    weight=2.4,
    length=14.3,
    arm_time=3,
    fuse_length=0,
    range=10,
    explosive_data=[
        ExplosiveData(range_hexes=None, shrapnel_penetration=2800.0, shrapnel_damage_class=10, base_shrapnel_hit_chance="*9", base_concussion=54000),
        ExplosiveData(range_hexes=0, shrapnel_penetration=10.0, shrapnel_damage_class=8, base_shrapnel_hit_chance="12", base_concussion=1900),
        ExplosiveData(range_hexes=1, shrapnel_penetration=9.7, shrapnel_damage_class=8, base_shrapnel_hit_chance="2", base_concussion=379),
        ExplosiveData(range_hexes=2, shrapnel_penetration=9.2, shrapnel_damage_class=8, base_shrapnel_hit_chance="0", base_concussion=102),
        ExplosiveData(range_hexes=3, shrapnel_penetration=8.7, shrapnel_damage_class=7, base_shrapnel_hit_chance="0", base_concussion=50),
        ExplosiveData(range_hexes=5, shrapnel_penetration=7.8, shrapnel_damage_class=7, base_shrapnel_hit_chance="0", base_concussion=22),
        ExplosiveData(range_hexes=10, shrapnel_penetration=6.0, shrapnel_damage_class=6, base_shrapnel_hit_chance="0", base_concussion=7)
    ]
)

l2_a2 = Grenade(
    name="L2 A2 Frag Grenade",
    country=Country.UK,
    grenade_type=GrenadeType.FRAG,
    weight=0.9,
    length=3.3,
    arm_time=3,
    fuse_length=2,
    range=16,
    explosive_data=[
        ExplosiveData(range_hexes=None, shrapnel_penetration=3.5, shrapnel_damage_class=10, base_shrapnel_hit_chance="*200", base_concussion=15000),
        ExplosiveData(range_hexes=0, shrapnel_penetration=2.4, shrapnel_damage_class=2, base_shrapnel_hit_chance="*3", base_concussion=747),
        ExplosiveData(range_hexes=1, shrapnel_penetration=2.2, shrapnel_damage_class=2, base_shrapnel_hit_chance="77", base_concussion=184),
        ExplosiveData(range_hexes=2, shrapnel_penetration=1.8, shrapnel_damage_class=2, base_shrapnel_hit_chance="19", base_concussion=55),
        ExplosiveData(range_hexes=3, shrapnel_penetration=1.5, shrapnel_damage_class=2, base_shrapnel_hit_chance="8", base_concussion=28),
        ExplosiveData(range_hexes=5, shrapnel_penetration=1.0, shrapnel_damage_class=1, base_shrapnel_hit_chance="2", base_concussion=12),
        ExplosiveData(range_hexes=10, shrapnel_penetration=0.4, shrapnel_damage_class=1, base_shrapnel_hit_chance="0", base_concussion=4)
    ]
)

m67 = Grenade(
    name="M 67 Frag Grenade",
    country=Country.USA,
    grenade_type=GrenadeType.FRAG,
    weight=0.9,
    length=3.5,
    arm_time=3,
    fuse_length=2,
    range=16,
    explosive_data=[
        ExplosiveData(range_hexes=None, shrapnel_penetration=5.0, shrapnel_damage_class=10, base_shrapnel_hit_chance="*23", base_concussion=16000),
        ExplosiveData(range_hexes=0, shrapnel_penetration=4.9, shrapnel_damage_class=6, base_shrapnel_hit_chance="31", base_concussion=779),
        ExplosiveData(range_hexes=1, shrapnel_penetration=4.8, shrapnel_damage_class=6, base_shrapnel_hit_chance="7", base_concussion=190),
        ExplosiveData(range_hexes=2, shrapnel_penetration=4.5, shrapnel_damage_class=5, base_shrapnel_hit_chance="1", base_concussion=56),
        ExplosiveData(range_hexes=3, shrapnel_penetration=4.2, shrapnel_damage_class=5, base_shrapnel_hit_chance="0", base_concussion=29),
        ExplosiveData(range_hexes=5, shrapnel_penetration=3.7, shrapnel_damage_class=5, base_shrapnel_hit_chance="0", base_concussion=12),
        ExplosiveData(range_hexes=10, shrapnel_penetration=2.6, shrapnel_damage_class=4, base_shrapnel_hit_chance="0", base_concussion=4)
    ]
)

m68 = Grenade(
    name="M 68 Frag Grenade",
    country=Country.USA,
    grenade_type=GrenadeType.FRAG,
    weight=0.9,
    length=3.5,
    arm_time=3,
    fuse_length=0,
    range=16,
    explosive_data=[
        ExplosiveData(range_hexes=None, shrapnel_penetration=5.1, shrapnel_damage_class=10, base_shrapnel_hit_chance="*21", base_concussion=16000),
        ExplosiveData(range_hexes=0, shrapnel_penetration=5.0, shrapnel_damage_class=6, base_shrapnel_hit_chance="28", base_concussion=791),
        ExplosiveData(range_hexes=1, shrapnel_penetration=4.8, shrapnel_damage_class=6, base_shrapnel_hit_chance="6", base_concussion=192),
        ExplosiveData(range_hexes=2, shrapnel_penetration=4.5, shrapnel_damage_class=5, base_shrapnel_hit_chance="1", base_concussion=57),
        ExplosiveData(range_hexes=3, shrapnel_penetration=4.2, shrapnel_damage_class=5, base_shrapnel_hit_chance="0", base_concussion=29),
        ExplosiveData(range_hexes=5, shrapnel_penetration=3.7, shrapnel_damage_class=5, base_shrapnel_hit_chance="0", base_concussion=12),
        ExplosiveData(range_hexes=10, shrapnel_penetration=2.7, shrapnel_damage_class=4, base_shrapnel_hit_chance="0", base_concussion=4)
    ]
)

m61 = Grenade(
    name="M 61 Frag Grenade",
    country=Country.USA,
    grenade_type=GrenadeType.FRAG,
    weight=1.0,
    length=3.8,
    arm_time=3,
    fuse_length=2,
    range=15,
    explosive_data=[
        ExplosiveData(range_hexes=None, shrapnel_penetration=3.4, shrapnel_damage_class=10, base_shrapnel_hit_chance="*200", base_concussion=13000),
        ExplosiveData(range_hexes=0, shrapnel_penetration=2.4, shrapnel_damage_class=2, base_shrapnel_hit_chance="*3", base_concussion=704),
        ExplosiveData(range_hexes=1, shrapnel_penetration=2.2, shrapnel_damage_class=2, base_shrapnel_hit_chance="84", base_concussion=176),
        ExplosiveData(range_hexes=2, shrapnel_penetration=1.8, shrapnel_damage_class=2, base_shrapnel_hit_chance="20", base_concussion=52),
        ExplosiveData(range_hexes=3, shrapnel_penetration=1.5, shrapnel_damage_class=2, base_shrapnel_hit_chance="8", base_concussion=27),
        ExplosiveData(range_hexes=5, shrapnel_penetration=1.0, shrapnel_damage_class=1, base_shrapnel_hit_chance="2", base_concussion=12),
        ExplosiveData(range_hexes=10, shrapnel_penetration=0.4, shrapnel_damage_class=1, base_shrapnel_hit_chance="0", base_concussion=4)
    ]
)

m26_a2 = Grenade(
    name="M 26 A2 Frag Grenade",
    country=Country.USA,
    grenade_type=GrenadeType.FRAG,
    weight=1.0,
    length=3.9,
    arm_time=3,
    fuse_length=0,
    range=15,
    explosive_data=[
        ExplosiveData(range_hexes=None, shrapnel_penetration=3.4, shrapnel_damage_class=10, base_shrapnel_hit_chance="*300", base_concussion=13000),
        ExplosiveData(range_hexes=0, shrapnel_penetration=2.4, shrapnel_damage_class=2, base_shrapnel_hit_chance="*4", base_concussion=704),
        ExplosiveData(range_hexes=1, shrapnel_penetration=2.2, shrapnel_damage_class=2, base_shrapnel_hit_chance="*1", base_concussion=176),
        ExplosiveData(range_hexes=2, shrapnel_penetration=1.8, shrapnel_damage_class=2, base_shrapnel_hit_chance="25", base_concussion=52),
        ExplosiveData(range_hexes=3, shrapnel_penetration=1.5, shrapnel_damage_class=2, base_shrapnel_hit_chance="11", base_concussion=27),
        ExplosiveData(range_hexes=5, shrapnel_penetration=1.0, shrapnel_damage_class=1, base_shrapnel_hit_chance="3", base_concussion=12),
        ExplosiveData(range_hexes=10, shrapnel_penetration=0.4, shrapnel_damage_class=1, base_shrapnel_hit_chance="0", base_concussion=4)
    ]
)

mk_a3 = Grenade(
    name="Mk A3 Blast Grenade",
    country=Country.USA,
    grenade_type=GrenadeType.BLAST,
    weight=1.0,
    length=5.3,
    arm_time=3,
    fuse_length=2,
    range=15,
    explosive_data=[
        ExplosiveData(range_hexes=None, shrapnel_penetration=3.8, shrapnel_damage_class=10, base_shrapnel_hit_chance="0", base_concussion=20000),
        ExplosiveData(range_hexes=0, shrapnel_penetration=0.0, shrapnel_damage_class=0, base_shrapnel_hit_chance="0", base_concussion=928),
        ExplosiveData(range_hexes=1, shrapnel_penetration=0.0, shrapnel_damage_class=0, base_shrapnel_hit_chance="0", base_concussion=218),
        ExplosiveData(range_hexes=2, shrapnel_penetration=0.0, shrapnel_damage_class=0, base_shrapnel_hit_chance="0", base_concussion=63),
        ExplosiveData(range_hexes=3, shrapnel_penetration=0.0, shrapnel_damage_class=0, base_shrapnel_hit_chance="0", base_concussion=32),
        ExplosiveData(range_hexes=5, shrapnel_penetration=0.0, shrapnel_damage_class=0, base_shrapnel_hit_chance="0", base_concussion=14),
        ExplosiveData(range_hexes=10, shrapnel_penetration=0.0, shrapnel_damage_class=0, base_shrapnel_hit_chance="0", base_concussion=4)
    ]
)

tnt_2lb = Grenade(
    name="2 lb TNT",
    country=Country.USA,
    grenade_type=GrenadeType.DEMO_SATCHEL,
    weight=2.0,
    length=3.8,
    arm_time=0,
    fuse_length=0,
    range=11,
    explosive_data=[
        ExplosiveData(range_hexes=None, shrapnel_penetration=10.0, shrapnel_damage_class=10, base_shrapnel_hit_chance="0", base_concussion=92000),
        ExplosiveData(range_hexes=0, shrapnel_penetration=0.0, shrapnel_damage_class=0, base_shrapnel_hit_chance="0", base_concussion=2900),
        ExplosiveData(range_hexes=1, shrapnel_penetration=0.0, shrapnel_damage_class=0, base_shrapnel_hit_chance="0", base_concussion=520),
        ExplosiveData(range_hexes=2, shrapnel_penetration=0.0, shrapnel_damage_class=0, base_shrapnel_hit_chance="0", base_concussion=131),
        ExplosiveData(range_hexes=3, shrapnel_penetration=0.0, shrapnel_damage_class=0, base_shrapnel_hit_chance="0", base_concussion=64),
        ExplosiveData(range_hexes=5, shrapnel_penetration=0.0, shrapnel_damage_class=0, base_shrapnel_hit_chance="0", base_concussion=27),
        ExplosiveData(range_hexes=10, shrapnel_penetration=0.0, shrapnel_damage_class=0, base_shrapnel_hit_chance="0", base_concussion=9)
    ]
)

tnt_10lb = Grenade(
    name="10 lb TNT",
    country=Country.USA,
    grenade_type=GrenadeType.DEMO_SATCHEL,
    weight=10.0,
    length=6.5,
    arm_time=0,
    fuse_length=0,
    range=5,
    explosive_data=[
        ExplosiveData(range_hexes=None, shrapnel_penetration=10.0, shrapnel_damage_class=10, base_shrapnel_hit_chance="0", base_concussion=590000),
        ExplosiveData(range_hexes=0, shrapnel_penetration=0.0, shrapnel_damage_class=0, base_shrapnel_hit_chance="0", base_concussion=15000),
        ExplosiveData(range_hexes=1, shrapnel_penetration=0.0, shrapnel_damage_class=0, base_shrapnel_hit_chance="0", base_concussion=1900),
        ExplosiveData(range_hexes=2, shrapnel_penetration=0.0, shrapnel_damage_class=0, base_shrapnel_hit_chance="0", base_concussion=347),
        ExplosiveData(range_hexes=3, shrapnel_penetration=0.0, shrapnel_damage_class=0, base_shrapnel_hit_chance="0", base_concussion=153),
        ExplosiveData(range_hexes=5, shrapnel_penetration=0.0, shrapnel_damage_class=0, base_shrapnel_hit_chance="0", base_concussion=61),
        ExplosiveData(range_hexes=10, shrapnel_penetration=0.0, shrapnel_damage_class=0, base_shrapnel_hit_chance="0", base_concussion=19)
    ]
)

grenades = [
    hg_78,
    of_hg_78,
    hg_80,
    nr_423,
    nr_446,
    type_59,
    type_82,
    df_37,
    of_37,
    mdn_21,
    dm_51,
    m26_a2_isr,
    blast_14,
    mu_50,
    rgd_5,
    rkg_3m,
    l2_a2,
    m67,
    m68,
    m61,
    m26_a2,
    mk_a3,
    tnt_2lb,
    tnt_10lb
]