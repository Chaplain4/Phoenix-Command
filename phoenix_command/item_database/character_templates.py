"""Pre-configured character templates for Phoenix Command."""

from phoenix_command.models.character import Character
from phoenix_command.models.gear import Gear
from phoenix_command.item_database.weapons import ak_74, ammo_545x39_ak74_fmj, dragunov_svd, ammo_762x54_svd_fmj, \
    rpk_74, ammo_545sov_rpk74_fmj, rpg_7v, ammo_85mm_he_rpg7, spas12, ammo_12g_spas_aps, ammo_12g_spas_shot, m16a2, \
    ammo_556nato_m16a2_fmj

ak74_fighter = Character(
    strength=10,
    intelligence=10,
    will=10,
    health=10,
    agility=10,
    gun_combat_skill_level=3,
    name="AK-74 Fighter"
)
ak74_fighter.add_gear(ak_74)
ak74_fighter.add_gear(Gear(name="Clothing", weight=5.0, description="Standard field clothing"),
)
for i in range(3):
    ak74_fighter.add_gear(ammo_545x39_ak74_fmj)

dragunov_fighter = Character(
    strength=10,
    intelligence=10,
    will=10,
    health=10,
    agility=10,
    gun_combat_skill_level=4,
    name="Dragunov Fighter"
)
dragunov_fighter.add_gear(dragunov_svd)
dragunov_fighter.add_gear(Gear(name="Clothing", weight=5.0, description="Standard field clothing")),
for i in range(3):
    dragunov_fighter.add_gear(ammo_762x54_svd_fmj)

rpk_74_fighter = Character(
    strength=10,
    intelligence=10,
    will=10,
    health=10,
    agility=10,
    gun_combat_skill_level=3,
    name="RPK-74 Fighter"
)
rpk_74_fighter.add_gear(rpk_74)
rpk_74_fighter.add_gear(Gear(name="Clothing", weight=5.0, description="Standard field clothing")),
rpk_74_fighter.add_gear(ammo_545sov_rpk74_fmj)

rpg_fighter = Character(
    strength=10,
    intelligence=10,
    will=10,
    health=10,
    agility=10,
    gun_combat_skill_level=4,
    name="RPG Fighter"
)
rpg_fighter.add_gear(rpg_7v)
rpg_fighter.add_gear(Gear(name="Clothing", weight=5.0, description="Standard field clothing")),
rpg_fighter.add_gear(ammo_85mm_he_rpg7)

shotgun_fighter = Character(
    strength=10,
    intelligence=10,
    will=10,
    health=10,
    agility=10,
    gun_combat_skill_level=3,
    name="Shotgun Fighter"
)
shotgun_fighter.add_gear(spas12)
shotgun_fighter.add_gear(Gear(name="Clothing", weight=5.0, description="Standard field clothing")),
shotgun_fighter.add_gear(ammo_12g_spas_aps)
shotgun_fighter.add_gear(ammo_12g_spas_shot)

m16a2_fighter = Character(
    strength=10,
    intelligence=10,
    will=10,
    health=10,
    agility=10,
    gun_combat_skill_level=3,
    name="M16A2 Fighter"
)
m16a2_fighter.add_gear(m16a2)
m16a2_fighter.add_gear(Gear(name="Clothing", weight=5.0, description="Standard field clothing")),
m16a2_fighter.add_gear(ammo_556nato_m16a2_fmj)

character_templates = [
    ak74_fighter,
    dragunov_fighter,
    rpk_74_fighter,
    rpg_fighter,
    shotgun_fighter,
    m16a2_fighter
]
