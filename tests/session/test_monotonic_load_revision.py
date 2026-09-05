"""Monotonic Load Session revision, roster preserve, honest guest sync status."""

from phoenix_command.session.domains.player_info import PlayerInfo
from phoenix_command.session.domains.token_state import TokenPlacement, TokenState
from phoenix_command.session.game_state import (
    GameState,
    apply_live_host_roster,
    clamp_loaded_revision,
    guest_sync_status_message,
)
from phoenix_command.session.sync_protocol import (
    apply_message_to_state,
    make_full_state_message,
)


def test_clamp_loaded_revision_does_not_rewind() -> None:
    loaded = GameState()
    loaded.revision = 3
    loaded.tokens = TokenState()
    loaded.tokens.placements["t1"] = TokenPlacement(token_id="t1", q=1, r=2)
    clamp_loaded_revision(11, loaded)
    assert loaded.revision == 11
    assert "t1" in loaded.tokens.placements


def test_clamp_keeps_higher_file_revision() -> None:
    loaded = GameState()
    loaded.revision = 20
    clamp_loaded_revision(11, loaded)
    assert loaded.revision == 20


def test_load_then_bump_publishes_past_guest_empty_revision() -> None:
    """Connect churn left guest at r11 empty; host Load must publish > 11 with tokens."""
    guest = GameState()
    guest.revision = 11

    loaded = GameState()
    loaded.revision = 3
    loaded.tokens = TokenState()
    loaded.tokens.placements["t1"] = TokenPlacement(
        token_id="t1", q=0, r=0, character_name="Fighter"
    )
    clamp_loaded_revision(11, loaded)
    loaded.bump_revision()  # publisher path after apply
    assert loaded.revision == 12

    result = apply_message_to_state(guest, make_full_state_message(loaded))
    assert result.revision == 12
    assert result.tokens is not None
    assert "t1" in result.tokens.placements


def test_apply_live_host_roster_keeps_guest_for_controlled_by() -> None:
    """File meta is empty/host-only; live hello roster must survive Load."""
    live_players = [
        PlayerInfo("host", "Host", is_host=True),
        PlayerInfo("guest-0", "GuestTester", is_host=False),
    ]
    loaded = GameState()
    loaded.revision = 3
    loaded.meta.players = [PlayerInfo("host", "SavedHost", is_host=True)]
    loaded.meta.connected_guests = []
    loaded.tokens = TokenState()
    loaded.tokens.placements["m16"] = TokenPlacement(token_id="m16", q=1, r=0)

    clamp_loaded_revision(11, loaded)
    apply_live_host_roster(
        loaded,
        players=live_players,
        connected_guests=["GuestTester"],
        host_name="Host",
    )
    loaded.bump_revision()

    assert [p.player_id for p in loaded.meta.players] == ["host", "guest-0"]
    assert loaded.meta.connected_guests == ["GuestTester"]
    assert loaded.revision == 12

    guest = GameState()
    guest.revision = 11
    result = apply_message_to_state(guest, make_full_state_message(loaded))
    assert result.revision == 12
    assert result.meta.get_player("guest-0") is not None
    assert result.tokens is not None
    assert "m16" in result.tokens.placements


def test_guest_sync_status_empty_session_warning() -> None:
    msg = guest_sync_status_message(11, has_characters=False, has_tokens=False)
    assert "synced r11" in msg
    assert "empty session" in msg
    assert "Load Session" in msg


def test_guest_sync_status_plain_when_content_present() -> None:
    msg = guest_sync_status_message(12, has_characters=True, has_tokens=True)
    assert msg == "Guest: synced revision 12"


def test_guest_sync_status_pending_move_overrides_empty() -> None:
    msg = guest_sync_status_message(
        5,
        has_characters=False,
        has_tokens=False,
        pending_move_hint="Continue Move …",
    )
    assert "Continue Move" in msg
    assert "empty session" not in msg
