"""BUG-06: Free Break Stance during pending stance-change."""

from phoenix_command.models.character import Character
from phoenix_command.session.domains.impulse_combat_state import (
    ImpulseCombatState,
    TokenCombatRuntime,
)
from phoenix_command.session.domains.map_state import MapState
from phoenix_command.session.domains.token_state import TokenPlacement, TokenState
from phoenix_command.simulations.impulse_combat_engine import ImpulseCombatEngine


def test_free_break_stance_during_pending_stance_change() -> None:
    ic = ImpulseCombatState(map_mode="combat", impulse=0)
    tokens = TokenState()
    tok = TokenPlacement(token_id="t1", character_name="T", q=0, r=0)
    tokens.placements["t1"] = tok
    char = Character(
        name="T",
        strength=12,
        intelligence=10,
        will=11,
        health=12,
        agility=10,
        gun_combat_skill_level=5,
    )
    rt = TokenCombatRuntime(
        ac_remaining=1.0,
        firing_stance_held=True,
        stance="standing",
    )
    rt.set_pending("standing_to_prone", 2.0, {}, progress=1.0)
    ic.token_runtime["t1"] = rt
    engine = ImpulseCombatEngine(ic, tokens, MapState(), {"T": char})

    ids = {a[0] for a in engine.available_actions("t1")}
    assert "free_break_stance" in ids

    result = engine.apply_action("t1", "free_break_stance", {})
    assert result.success, result.message
    assert rt.firing_stance_held is False
    assert rt.pending_id() == "standing_to_prone"
    assert rt.pending_progress_ac == 1.0
    assert rt.ac_remaining == 1.0
