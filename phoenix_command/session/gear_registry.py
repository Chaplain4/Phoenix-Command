"""Lookup gear templates from item_database by display name."""

from __future__ import annotations

from copy import deepcopy
from typing import TYPE_CHECKING

from phoenix_command.models.gear import Armor, AmmoType, Gear, Grenade, Weapon

if TYPE_CHECKING:
    pass

_GEAR_BY_NAME: dict[str, Gear] | None = None


def _collect_gear() -> dict[str, Gear]:
    from phoenix_command.item_database import armor, equipment, grenades, weapons

    registry: dict[str, Gear] = {}

    def register(item: Gear) -> None:
        if item.name not in registry:
            registry[item.name] = item

    if hasattr(armor, "armor"):
        for piece in armor.armor:
            register(piece)

    if hasattr(grenades, "grenades"):
        for g in grenades.grenades:
            register(g)

    if hasattr(equipment, "EQUIPMENT_LIST"):
        for g in equipment.EQUIPMENT_LIST:
            register(g)

    if hasattr(weapons, "__dict__"):
        for obj in weapons.__dict__.values():
            if isinstance(obj, Weapon):
                register(obj)
                for ammo in obj.ammunition_types:
                    register(ammo)

    return registry


def get_gear_registry() -> dict[str, Gear]:
    global _GEAR_BY_NAME
    if _GEAR_BY_NAME is None:
        _GEAR_BY_NAME = _collect_gear()
    return _GEAR_BY_NAME


def resolve_gear_template(name: str) -> Gear:
    registry = get_gear_registry()
    if name not in registry:
        raise KeyError(f"Unknown gear template: {name!r}")
    return registry[name]


def clone_gear_template(name: str) -> Gear:
    return deepcopy(resolve_gear_template(name))
