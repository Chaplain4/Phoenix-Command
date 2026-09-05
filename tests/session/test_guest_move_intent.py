"""Guest move intent semantics: pending carry-over, not finished by Next Impulse alone."""

from phoenix_command.models.character import Character
from phoenix_command.session.domains.impulse_combat_state import (
    ImpulseCombatState,
    TokenCombatRuntime,
)
from phoenix_command.session.domains.map_state import MapState
from phoenix_command.session.domains.token_state import TokenPlacement, TokenState
from phoenix_command.session.game_state import GameState
from phoenix_command.session.sync_protocol import apply_message_to_state, make_full_state_message
from phoenix_command.simulations.impulse_combat_engine import ImpulseCombatEngine


def _fighter() -> Character:
    return Character(
        name="Fighter",
        strength=12,
        intelligence=10,
        will=11,
        health=12,
        agility=10,
        gun_combat_skill_level=5,
    )


def _engine(ac: float = 0.5) -> tuple[ImpulseCombatEngine, TokenPlacement]:
    ic = ImpulseCombatState(map_mode="combat", impulse=0)
    tokens = TokenState()
    tok = TokenPlacement(
        token_id="t1",
        character_name="Fighter",
        q=0,
        r=0,
        facing=0,
        controlled_by="guest-abc",
    )
    tokens.placements["t1"] = tok
    ic.token_runtime["t1"] = TokenCombatRuntime(ac_remaining=ac, stance="standing")
    engine = ImpulseCombatEngine(ic, tokens, MapState(), {"Fighter": _fighter()})
    return engine, tok


def test_guest_move_intent_partial_progress() -> None:
    engine, tok = _engine(ac=0.5)
    result = engine.apply_action(
        "t1",
        "move",
        {"target_q": -1, "target_r": 0},
        player_id="guest-abc",
        is_host=False,
    )
    assert result.success
    rt = engine.get_runtime("t1")
    assert rt.move_progress > 0
    assert tok.q == 0 and tok.r == 0
    assert rt.pending_id() == "move" or rt.move_target_q == -1


def test_advance_impulse_alone_does_not_finish_pending_move() -> None:
    engine, tok = _engine(ac=0.5)
    engine.apply_action(
        "t1",
        "move",
        {"target_q": -1, "target_r": 0},
        player_id="guest-abc",
        is_host=False,
    )
    rt = engine.get_runtime("t1")
    progress = rt.move_progress
    assert progress > 0
    assert tok.q == 0
    engine.advance_impulse()
    # Progress and target survive impulse advance; hex stays put.
    assert rt.move_progress == progress
    assert rt.move_target_q == -1
    assert tok.q == 0 and tok.r == 0


def test_continue_move_after_refill_completes() -> None:
    engine, tok = _engine(ac=0.5)
    engine.apply_action(
        "t1",
        "move",
        {"target_q": -1, "target_r": 0},
        player_id="guest-abc",
        is_host=False,
    )
    rt = engine.get_runtime("t1")
    progress = rt.move_progress
    engine.refill_impulse_ac()
    assert rt.move_progress == progress
    result = engine.apply_action(
        "t1",
        "move",
        {"target_q": -1, "target_r": 0},
        player_id="guest-abc",
        is_host=False,
    )
    assert result.success
    assert tok.q == -1 and tok.r == 0
    assert rt.move_progress == 0.0


def test_guest_sees_partial_move_via_full_state_sync() -> None:
    engine, tok = _engine(ac=0.5)
    engine.apply_action(
        "t1",
        "move",
        {"target_q": -1, "target_r": 0},
        player_id="guest-abc",
        is_host=False,
    )
    host_state = GameState()
    host_state.impulse_combat = engine.impulse_combat
    host_state.tokens = engine.tokens
    host_state.map = engine.map_state
    host_state.bump_revision()
    msg = make_full_state_message(host_state)
    guest_state = apply_message_to_state(GameState(), msg)
    rt = guest_state.impulse_combat.token_runtime["t1"]
    assert rt.move_progress > 0
    assert rt.move_target_q == -1
    assert guest_state.tokens.placements["t1"].q == 0
    assert guest_state.tokens.placements["t1"].controlled_by == "guest-abc"


def test_wrong_player_cannot_move_token() -> None:
    engine, _ = _engine(ac=5.0)
    bad = engine.apply_action(
        "t1",
        "move",
        {"target_q": -1, "target_r": 0},
        player_id="guest-other",
        is_host=False,
    )
    assert not bad.success
    assert "control" in bad.message.lower()
