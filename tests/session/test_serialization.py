"""Tests for session serialization and sync protocol."""

import copy

import pytest

from phoenix_command.models.character import Character
from phoenix_command.models.enums import AdvancedHitLocation, ArmorMaterial
from phoenix_command.models.gear import Armor, ArmorLayer, ArmorProtectionData
from phoenix_command.models.hit_result_advanced import DamageResult
from phoenix_command.session.domains.combat_state import CombatState
from phoenix_command.session.game_state import GameState, SCHEMA_VERSION
from phoenix_command.session.patch import apply_patch
from phoenix_command.session.serialization import (
    character_from_dict,
    character_to_dict,
    game_state_from_json,
    game_state_to_json,
    gear_from_dict,
    gear_to_dict,
)
from phoenix_command.session.sync_protocol import (
    MessageType,
    SyncMessage,
    apply_message_to_state,
    decode_message,
    encode_message,
    make_full_state_message,
)


@pytest.fixture
def sample_character() -> Character:
    char = Character(
        name="Test Fighter",
        strength=12,
        intelligence=10,
        will=11,
        health=12,
        agility=10,
        gun_combat_skill_level=5,
    )
    armor = Armor(name="Test Helmet", weight=3.0)
    armor.add_protection(
        AdvancedHitLocation.HEAD_GLANCE,
        True,
        ArmorMaterial.KEVLAR,
        5,
        2,
    )
    char.add_gear(armor)
    return char


def test_character_round_trip(sample_character: Character) -> None:
    data = character_to_dict(sample_character)
    restored = character_from_dict(data)
    assert restored.name == sample_character.name
    assert restored.strength == sample_character.strength
    assert len(restored.equipment) == 1
    assert isinstance(restored.equipment[0], Armor)


def test_armor_degradation_round_trip(sample_character: Character) -> None:
    armor = sample_character.equipment[0]
    assert isinstance(armor, Armor)
    armor.process_hit(AdvancedHitLocation.HEAD_GLANCE, True, 10.0)
    data = character_to_dict(sample_character)
    restored = character_from_dict(data)
    orig_layer = armor.protection[(AdvancedHitLocation.HEAD_GLANCE, True)].layers[0]
    rest_layer = restored.equipment[0].protection[
        (AdvancedHitLocation.HEAD_GLANCE, True)
    ].layers[0]
    assert rest_layer.current_condition == orig_layer.current_condition


def test_add_gear_deepcopy() -> None:
    from phoenix_command.item_database import armor as armor_db

    if not armor_db.armor:
        pytest.skip("No armor in database")
    template = armor_db.armor[0]
    char = Character(
        name="A",
        strength=10,
        intelligence=10,
        will=10,
        health=10,
        agility=10,
        gun_combat_skill_level=3,
    )
    char.add_gear(template)
    char.equipment[0].protection[list(char.equipment[0].protection.keys())[0]].layers[0].current_condition = 0.5
    assert template.protection[list(template.protection.keys())[0]].layers[0].current_condition == 1.0


def test_game_state_json_round_trip(sample_character: Character) -> None:
    state = GameState()
    state.combat.characters = [character_to_dict(sample_character)]
    state.bump_revision()
    text = game_state_to_json(state)
    loaded = game_state_from_json(text)
    assert loaded.schema_version == SCHEMA_VERSION
    assert loaded.revision == state.revision
    assert len(loaded.combat.characters) == 1


def test_json_patch_replace() -> None:
    doc = {"combat": {"characters": [{"name": "A", "physical_damage_total": 0}]}}
    patched = apply_patch(
        doc,
        [{"op": "replace", "path": "/combat/characters/0/physical_damage_total", "value": 15}],
    )
    assert patched["combat"]["characters"][0]["physical_damage_total"] == 15


def test_sync_message_encode_decode() -> None:
    state = GameState()
    msg = make_full_state_message(state)
    raw = encode_message(msg)
    decoded = decode_message(raw)
    assert decoded.type == MessageType.FULL_STATE
    assert decoded.revision == state.revision


def test_apply_full_state_message() -> None:
    state = GameState()
    state.combat.characters = [
        character_to_dict(
            Character(
                name="X",
                strength=10,
                intelligence=10,
                will=10,
                health=10,
                agility=10,
                gun_combat_skill_level=3,
            )
        )
    ]
    state.bump_revision()
    msg = make_full_state_message(state)
    empty = GameState()
    result = apply_message_to_state(empty, msg)
    assert len(result.combat.characters) == 1
    assert result.combat.characters[0]["name"] == "X"


def test_hit_history_round_trip(sample_character: Character) -> None:
    sample_character.apply_damage(
        5,
        DamageResult(location=AdvancedHitLocation.LUNG, damage=5, shock=2),
    )
    restored = character_from_dict(character_to_dict(sample_character))
    assert len(restored.hit_history) == 1
    assert restored.hit_history[0].location == AdvancedHitLocation.LUNG
