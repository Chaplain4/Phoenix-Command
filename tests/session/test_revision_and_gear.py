"""Tests for revision-0 stale guard and unknown gear fallback."""

from phoenix_command.session.game_state import GameState
from phoenix_command.session.serialization import gear_from_dict
from phoenix_command.session.sync_protocol import (
    MessageType,
    SyncMessage,
    apply_message_to_state,
)


def test_revision_zero_does_not_overwrite_live_state() -> None:
    state = GameState()
    state.revision = 5
    state.meta.session_name = "live"
    msg = SyncMessage(
        type=MessageType.FULL_STATE,
        revision=0,
        payload=GameState().to_dict(),
    )
    result = apply_message_to_state(state, msg)
    assert result.revision == 5
    assert result.meta.session_name == "live"


def test_first_sync_both_at_zero_still_applies() -> None:
    state = GameState()
    payload = GameState().to_dict()
    payload["meta"]["session_name"] = "boot"
    msg = SyncMessage(type=MessageType.FULL_STATE, revision=0, payload=payload)
    result = apply_message_to_state(state, msg)
    assert result.meta.session_name == "boot"


def test_unknown_weapon_gear_fallback() -> None:
    gear = gear_from_dict(
        {
            "gear_ref": "Totally Made Up Rifle XYZ",
            "gear_type": "Weapon",
            "weight": 7.5,
            "description": "custom",
        }
    )
    assert gear.name == "Totally Made Up Rifle XYZ"
    assert gear.weight == 7.5
