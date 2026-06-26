"""Tests for sync protocol patch application on GameState."""

from phoenix_command.session.game_state import GameState
from phoenix_command.session.serialization import character_to_dict
from phoenix_command.session.sync_protocol import (
    MessageType,
    SyncMessage,
    apply_message_to_state,
)
from phoenix_command.models.character import Character


def test_domain_delta_updates_combat() -> None:
    state = GameState()
    state.combat.characters = [
        character_to_dict(
            Character(
                name="A",
                strength=10,
                intelligence=10,
                will=10,
                health=10,
                agility=10,
                gun_combat_skill_level=3,
            )
        )
    ]
    state.revision = 1
    msg = SyncMessage(
        type=MessageType.DOMAIN_DELTA,
        revision=2,
        domain="combat",
        patch=[
            {
                "op": "replace",
                "path": "/combat/characters/0/physical_damage_total",
                "value": 20,
            }
        ],
    )
    result = apply_message_to_state(state, msg)
    assert result.revision == 2
    assert result.combat.characters[0]["physical_damage_total"] == 20


def test_stale_revision_ignored() -> None:
    state = GameState()
    state.revision = 10
    msg = SyncMessage(
        type=MessageType.FULL_STATE,
        revision=5,
        payload=GameState().to_dict(),
    )
    result = apply_message_to_state(state, msg)
    assert result.revision == 10
