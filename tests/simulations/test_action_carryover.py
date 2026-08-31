"""Tests for unfinished action carry-over, aim interrupt, and Duck."""

from phoenix_command.models.character import Character
from phoenix_command.models.enums import Caliber, Country, WeaponType
from phoenix_command.models.gear import Weapon
from phoenix_command.session.domains.impulse_combat_state import (
    ImpulseCombatState,
    TokenCombatRuntime,
)
from phoenix_command.session.domains.map_state import MapState
from phoenix_command.session.domains.token_state import TokenPlacement, TokenState
from phoenix_command.simulations.impulse_combat_engine import ImpulseCombatEngine
from phoenix_command.simulations.map_shot_context import build_map_shot_context


def _fighter(name: str = "Fighter") -> Character:
    return Character(
        name=name,
        strength=12,
        intelligence=10,
        will=11,
        health=12,
        agility=10,
        gun_combat_skill_level=5,
    )


def _engine(
    ac: float = 1.0,
    *,
    reload_time: int = 6,
) -> tuple[ImpulseCombatEngine, TokenPlacement]:
    ic = ImpulseCombatState(map_mode="combat", impulse=0)
    tokens = TokenState()
    tok = TokenPlacement(
        token_id="t1",
        character_name="Fighter",
        q=0,
        r=0,
        facing=0,
    )
    tokens.placements["t1"] = tok
    rt = TokenCombatRuntime(ac_remaining=ac, stance="standing")
    ic.token_runtime["t1"] = rt
    char = _fighter()
    weapon = Weapon(
        name="Test Rifle",
        weight=8.0,
        caliber=Caliber.CAL_556_NATO,
        weapon_type=WeaponType.ASSAULT_RIFLE,
        country=Country.USA,
        length_deployed=30.0,
        reload_time=reload_time,
        actions_to_cycle=2,
    )
    char.add_gear(weapon)
    engine = ImpulseCombatEngine(ic, tokens, MapState(), {"Fighter": char})
    engine.get_runtime("t1").held_weapon_name = "Test Rifle"
    return engine, tok


def test_partial_reload_carries_across_impulse() -> None:
    engine, _ = _engine(ac=2.0, reload_time=8)
    r1 = engine.apply_action("t1", "reload", {})
    assert r1.success
    rt = engine.get_runtime("t1")
    assert rt.pending_action_id == "reload"
    assert rt.pending_progress_ac == 2.0
    assert rt.pending_total_cost_ac == 8.0
    engine.refill_impulse_ac()
    assert rt.pending_progress_ac == 2.0
    r2 = engine.apply_action("t1", "reload", {})
    assert r2.success
    assert rt.pending_progress_ac == 2.0 + float(_fighter().impulses[0])
    # Finish with enough AC
    rt.ac_remaining = 20.0
    r3 = engine.apply_action("t1", "reload", {})
    assert r3.success
    assert "complete" in r3.message.lower()
    assert rt.pending_action_id is None
    assert rt.weapon_cycled is True


def test_abandon_mid_reload() -> None:
    engine, _ = _engine(ac=2.0, reload_time=8)
    engine.apply_action("t1", "reload", {})
    rt = engine.get_runtime("t1")
    assert rt.has_pending()
    blocked = engine.apply_action("t1", "aim", {"ac": 1})
    assert not blocked.success
    assert "pending" in blocked.message.lower()
    abandon = engine.apply_action("t1", "abandon_pending", {})
    assert abandon.success
    assert not rt.has_pending()
    assert rt.pending_progress_ac == 0.0
    rt.ac_remaining = 2.0
    ok = engine.apply_action("t1", "aim", {"ac": 1})
    assert ok.success


def test_move_progress_survives_refill() -> None:
    engine, tok = _engine(ac=0.5)
    engine.apply_action("t1", "move", {"target_q": -1, "target_r": 0})
    rt = engine.get_runtime("t1")
    progress = rt.move_progress
    assert progress > 0
    assert tok.q == 0
    engine.refill_impulse_ac()
    assert rt.move_progress == progress
    assert rt.move_target_q == -1
    result = engine.apply_action("t1", "move", {"target_q": -1, "target_r": 0})
    assert result.success
    assert tok.q == -1
    assert rt.move_progress == 0.0


def test_aim_cleared_on_move() -> None:
    engine, _ = _engine(ac=10.0)
    engine.apply_action("t1", "aim", {"ac": 2, "target_token_id": "enemy"})
    rt = engine.get_runtime("t1")
    assert rt.aim_ac_accumulated == 2.0
    engine.apply_action("t1", "move", {"target_q": 1, "target_r": 0})
    assert rt.aim_ac_accumulated == 0.0
    assert rt.aim_target_token_id is None


def test_free_duck_interrupts_pending_and_aim() -> None:
    engine, _ = _engine(ac=3.0, reload_time=8)
    engine.apply_action("t1", "aim", {"ac": 1, "target_token_id": "e1"})
    rt = engine.get_runtime("t1")
    assert rt.aim_ac_accumulated == 1.0
    engine.apply_action("t1", "reload", {})
    assert rt.aim_ac_accumulated == 0.0
    assert rt.has_pending()
    duck = engine.apply_action("t1", "duck", {})
    assert duck.success
    assert rt.ducking is True
    assert not rt.has_pending()
    assert rt.aim_ac_accumulated == 0.0
    engine.refill_impulse_ac()
    assert rt.ducking is False


def test_duck_from_firing_gated() -> None:
    engine, _ = _engine(ac=5.0)
    fail = engine.apply_action("t1", "duck_from_firing", {})
    assert not fail.success
    rt = engine.get_runtime("t1")
    rt.firing_stance_held = True
    ok = engine.apply_action("t1", "duck_from_firing", {})
    assert ok.success
    assert rt.firing_stance_held is False
    assert rt.ducking is True


def test_map_shot_context_duck_flags() -> None:
    shooter = TokenPlacement(token_id="s", q=0, r=0, character_name="A")
    target = TokenPlacement(token_id="t", q=3, r=0, character_name="B")
    s_rt = TokenCombatRuntime(ducking=True, aim_ac_accumulated=2.0)
    t_rt = TokenCombatRuntime(ducking=True)
    ctx = build_map_shot_context(shooter, s_rt, target, t_rt, MapState())
    assert ctx.shot_params.reflexive_duck_shooter is True
    assert ctx.shot_params.reflexive_duck_target is True
    assert any("ducking" in n.lower() for n in ctx.visibility_notes)


def test_runtime_pending_serialization() -> None:
    rt = TokenCombatRuntime(
        pending_action_id="reload",
        pending_progress_ac=3.0,
        pending_total_cost_ac=8.0,
        pending_args={"x": 1},
        looking_over_cover=True,
        ducking=True,
    )
    restored = TokenCombatRuntime.from_dict(rt.to_dict())
    assert restored.pending_action_id == "reload"
    assert restored.pending_progress_ac == 3.0
    assert restored.pending_total_cost_ac == 8.0
    assert restored.pending_args == {"x": 1}
    assert restored.looking_over_cover is True
    assert restored.ducking is True
    assert "pending reload" in restored.status_label()
    assert "ducking" in restored.status_label()
