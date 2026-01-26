"""Pre-configured character templates for Phoenix Command."""

from phoenix_command.models.character import Character
from phoenix_command.models.gear import Gear
from phoenix_command.item_database.weapons import ak_74, ammo_545x39_ak74_fmj, dragunov_svd, ammo_762x54_svd_fmj, \
    rpk_74, ammo_545sov_rpk74_fmj, rpg_7v, ammo_85mm_he_rpg7

ak74_fighter = Character(
    strength=10,
    intelligence=10,
    will=10,
    health=10,
    agility=10,
    gun_combat_skill_level=3
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
    gun_combat_skill_level=4
)
dragunov_fighter.add_gear(dragunov_svd)
dragunov_fighter.add_gear(Gear(name="Clothing", weight=5.0, description="Standard field clothing")),
for i in range(3):
    ak74_fighter.add_gear(ammo_762x54_svd_fmj)

rpk_74_fighter = Character(
    strength=10,
    intelligence=10,
    will=10,
    health=10,
    agility=10,
    gun_combat_skill_level=3
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
    gun_combat_skill_level=4
)
rpg_fighter.add_gear(rpg_7v)
rpg_fighter.add_gear(Gear(name="Clothing", weight=5.0, description="Standard field clothing")),
rpg_fighter.add_gear(ammo_85mm_he_rpg7)

character_templates = [
    ak74_fighter,
    dragunov_fighter,
    rpk_74_fighter,
    rpg_fighter
]
