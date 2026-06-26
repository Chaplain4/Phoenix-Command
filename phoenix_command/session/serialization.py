"""Serialize and deserialize Character, gear, and GameState."""

from __future__ import annotations

import json
from copy import deepcopy
from typing import Any

from phoenix_command.models.character import Character
from phoenix_command.models.enums import AdvancedHitLocation, ArmorMaterial
from phoenix_command.models.gear import (
    Armor,
    ArmorLayer,
    ArmorProtectionData,
    Gear,
    Grenade,
    Weapon,
)
from phoenix_command.models.hit_result_advanced import DamageResult
from phoenix_command.session.game_state import GameState
from phoenix_command.session.gear_registry import clone_gear_template, resolve_gear_template


def _armor_layer_to_dict(layer: ArmorLayer) -> dict:
    return {
        "material": layer.material.name,
        "protection_factor": layer.protection_factor,
        "blunt_protection_factor": layer.blunt_protection_factor,
        "current_condition": layer.current_condition,
    }


def _armor_layer_from_dict(data: dict) -> ArmorLayer:
    return ArmorLayer(
        material=ArmorMaterial[data["material"]],
        protection_factor=data["protection_factor"],
        blunt_protection_factor=data["blunt_protection_factor"],
        current_condition=data.get("current_condition", 1.0),
    )


def _armor_protection_to_dict(protection: dict) -> dict:
    result = {}
    for (location, is_front), pdata in protection.items():
        key = f"{location.name}:{int(is_front)}"
        result[key] = {
            "layers": [_armor_layer_to_dict(layer) for layer in pdata.layers],
        }
    return result


def _armor_protection_from_dict(data: dict) -> dict:
    protection = {}
    for key, pdata in data.items():
        loc_name, front_flag = key.rsplit(":", 1)
        location = AdvancedHitLocation[loc_name]
        is_front = bool(int(front_flag))
        layers = [_armor_layer_from_dict(layer) for layer in pdata.get("layers", [])]
        protection[(location, is_front)] = ArmorProtectionData(layers=layers)
    return protection


def gear_to_dict(gear: Gear) -> dict:
    """Serialize gear as template name plus armor degradation delta."""
    entry: dict[str, Any] = {
        "gear_ref": gear.name,
        "gear_type": type(gear).__name__,
        "weight": gear.weight,
        "description": getattr(gear, "description", "") or "",
    }
    if isinstance(gear, Armor) and gear.protection:
        entry["armor_delta"] = _armor_protection_to_dict(gear.protection)
    return entry


def _armor_from_inline(data: dict) -> Armor:
    armor = Armor(
        name=data["gear_ref"],
        weight=data.get("weight", 0.0),
        description=data.get("description", ""),
    )
    if "armor_delta" in data:
        armor.protection = _armor_protection_from_dict(data["armor_delta"])
    return armor


def gear_from_dict(data: dict) -> Gear:
    """Deserialize gear from template ref and optional armor delta."""
    try:
        gear = clone_gear_template(data["gear_ref"])
    except KeyError:
        if data.get("gear_type") == "Armor":
            return _armor_from_inline(data)
        raise
    if isinstance(gear, Armor) and "armor_delta" in data:
        gear.protection = _armor_protection_from_dict(data["armor_delta"])
    return gear


def damage_result_to_dict(result: DamageResult) -> dict:
    return {
        "location": result.location.name,
        "damage": result.damage,
        "shock": result.shock,
        "excess_epen": result.excess_epen,
        "is_disabled": result.is_disabled,
        "weapon_damaged": result.weapon_damaged,
        "pierced_organs": list(result.pierced_organs),
    }


def damage_result_from_dict(data: dict) -> DamageResult:
    return DamageResult(
        location=AdvancedHitLocation[data["location"]],
        damage=data.get("damage", 0),
        shock=data.get("shock", 0),
        excess_epen=data.get("excess_epen", 0.0),
        is_disabled=data.get("is_disabled", False),
        weapon_damaged=data.get("weapon_damaged", False),
        pierced_organs=list(data.get("pierced_organs", [])),
    )


def character_to_dict(character: Character) -> dict:
    return {
        "name": character.name,
        "strength": character.strength,
        "intelligence": character.intelligence,
        "will": character.will,
        "health": character.health,
        "agility": character.agility,
        "gun_combat_skill_level": character.gun_combat_skill_level,
        "physical_damage_total": character.physical_damage_total,
        "equipment": [gear_to_dict(g) for g in character.equipment],
        "hit_history": [damage_result_to_dict(h) for h in character.hit_history],
    }


def character_from_dict(data: dict) -> Character:
    char = Character(
        name=data.get("name", "Unnamed"),
        strength=data["strength"],
        intelligence=data["intelligence"],
        will=data["will"],
        health=data["health"],
        agility=data["agility"],
        gun_combat_skill_level=data["gun_combat_skill_level"],
        physical_damage_total=data.get("physical_damage_total", 0),
    )
    for gear_data in data.get("equipment", []):
        char.equipment.append(gear_from_dict(gear_data))
    char.hit_history = [
        damage_result_from_dict(h) for h in data.get("hit_history", [])
    ]
    return char


def game_state_to_json(state: GameState) -> str:
    return json.dumps(state.to_dict(), indent=2)


def game_state_from_json(text: str) -> GameState:
    return GameState.from_dict(json.loads(text))


def game_state_to_bytes(state: GameState) -> bytes:
    return json.dumps(state.to_dict()).encode("utf-8")


def game_state_from_bytes(data: bytes) -> GameState:
    return GameState.from_dict(json.loads(data.decode("utf-8")))
