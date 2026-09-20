"""Tests for facing turns and multi-impulse routes."""

from phoenix_command.models.character import Character
from phoenix_command.models.enums import Caliber, Country, WeaponType
from phoenix_command.models.gear import Weapon
from phoenix_command.session.domains.impulse_combat_state import (
    ImpulseCombatState,
    TokenCombatRuntime,
)
from phoenix_command.session.domains.map_state import MapState, Opening, WallSegment
from phoenix_command.session.domains.token_state import TokenPlacement, TokenState
from phoenix_command.simulations.hex_tactical import (
    apply_free_facing,
    shortest_facing_delta,
)
from phoenix_command.simulations.impulse_combat_engine import ImpulseCombatEngine
from phoenix_command.simulations import map_route


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


def _engine(ac: float = 10.0, facing: int = 0) -> tuple[ImpulseCombatEngine, TokenPlacement]:
    ic = ImpulseCombatState(map_mode="combat", impulse=0)
    tokens = TokenState()
    tok = TokenPlacement(
        token_id="t1",
        character_name="Fighter",
        q=0,
        r=0,
        facing=facing,
        side_id="alpha",
    )
    tokens.placements["t1"] = tok
    enemy = TokenPlacement(
        token_id="t2",
        character_name="Enemy",
        q=3,
        r=0,
        facing=6,
        side_id="bravo",
    )
    tokens.placements["t2"] = enemy
    ic.token_runtime["t1"] = TokenCombatRuntime(ac_remaining=ac, stance="standing")
    ic.token_runtime["t2"] = TokenCombatRuntime(ac_remaining=ac)
    char = _fighter()
    weapon = Weapon(
        name="Test Rifle",
        weight=8.0,
        caliber=Caliber.CAL_556_NATO,
        weapon_type=WeaponType.ASSAULT_RIFLE,
        country=Country.USA,
        length_deployed=30.0,
        reload_time=6,
        actions_to_cycle=None,
    )
    char.add_gear(weapon)
    engine = ImpulseCombatEngine(ic, tokens, MapState(), {"Fighter": char})
    engine.get_runtime("t1").held_weapon_name = "Test Rifle"
    return engine, tok


def test_facing_change_60_costs_1_and_updates() -> None:
    engine, tok = _engine(ac=5.0, facing=0)
    result = engine.apply_action(
        "t1", "facing_change_60_120", {"delta_steps": 2}
    )
    assert result.success
    assert tok.facing == 2
    assert engine.get_runtime("t1").ac_remaining == 4.0


def test_facing_firing_stance_costs_2() -> None:
    engine, tok = _engine(ac=5.0, facing=0)
    rt = engine.get_runtime("t1")
    rt.firing_stance_held = True
    result = engine.apply_action(
        "t1", "facing_change_60_firing", {"delta_steps": 2}
    )
    assert result.success
    assert tok.facing == 2
    assert rt.ac_remaining == 3.0
    assert rt.firing_stance_held is True


def test_hip_cover_does_not_set_proper_stance() -> None:
    engine, _ = _engine(ac=5.0)
    result = engine.apply_action("t1", "assume_hip_firing_stance_cover", {})
    assert result.success
    rt = engine.get_runtime("t1")
    assert rt.looking_over_cover is True
    assert rt.firing_stance_held is False


def test_proper_cover_stance_sets_firing_stance() -> None:
    engine, _ = _engine(ac=5.0)
    result = engine.apply_action("t1", "assume_firing_stance_cover", {})
    assert result.success
    rt = engine.get_runtime("t1")
    assert rt.firing_stance_held is True
    assert rt.looking_over_cover is True


def test_free_facing_60_on_hex_enter() -> None:
    # Move east (dir 0) from facing 10 (need +2 = 60°) → free
    engine, tok = _engine(ac=5.0, facing=10)
    result = engine.apply_action("t1", "move", {"target_q": 1, "target_r": 0})
    assert result.success
    assert tok.q == 1
    assert tok.facing == 0  # desired east


def test_free_facing_partial_90() -> None:
    # Need 90° (3 steps): free 2, leave facing short of desired
    current = 0
    desired = 3
    after = apply_free_facing(current, desired, free_steps=2)
    assert after == 2
    rem = shortest_facing_delta(after, desired)
    assert rem == 1


def test_declared_target() -> None:
    engine, _ = _engine()
    result = engine.apply_action(
        "t1", "set_declared_target", {"target_token_id": "t2"}
    )
    assert result.success
    assert engine.get_runtime("t1").declared_target_token_id == "t2"
    engine.apply_action("t1", "clear_declared_target", {})
    assert engine.get_runtime("t1").declared_target_token_id is None


def test_route_chain_and_estimate() -> None:
    engine, tok = _engine(ac=10.0, facing=0)
    engine.apply_action("t1", "plan_route_chain", {"target_q": 1, "target_r": 0})
    engine.apply_action("t1", "plan_route_chain", {"target_q": 2, "target_r": 0})
    engine.apply_action("t1", "plan_route_chain", {"target_q": 3, "target_r": 0})
    rt = engine.get_runtime("t1")
    assert len([s for s in rt.route_steps if s.get("kind") == "hex"]) == 3
    est = map_route.estimate_route(rt, _fighter(), current_impulse=0)
    assert est.hex_steps_left == 3
    assert est.remaining_ac > 0


def test_route_pathfind_around_wall() -> None:
    engine, tok = _engine(ac=20.0, facing=0)
    layer = engine.map_state.get_active_layer()
    assert layer is not None
    # Block direct east cell
    from phoenix_command.session.domains.map_state import hex_wall_key

    layer.walls[hex_wall_key(1, 0)] = WallSegment()
    result = engine.apply_action(
        "t1", "plan_route_pathfind", {"target_q": 2, "target_r": 0}
    )
    assert result.success
    rt = engine.get_runtime("t1")
    hexes = [(s["q"], s["r"]) for s in rt.route_steps if s.get("kind") == "hex"]
    assert (2, 0) in hexes
    assert (1, 0) not in hexes


def test_continue_route_across_impulse() -> None:
    # Forward hex costs 0.5 AC on 1m grid; use tiny AC so first continue is partial.
    engine, tok = _engine(ac=0.25, facing=0)
    engine.apply_action("t1", "plan_route_chain", {"target_q": 1, "target_r": 0})
    r1 = engine.apply_action("t1", "continue_route", {})
    assert r1.success
    rt = engine.get_runtime("t1")
    assert tok.q == 0
    assert rt.move_progress > 0
    engine.refill_impulse_ac()
    r2 = engine.apply_action("t1", "continue_route", {})
    assert r2.success
    assert tok.q == 1


def test_clear_and_edit_route() -> None:
    engine, _ = _engine(ac=10.0)
    engine.apply_action("t1", "plan_route_chain", {"target_q": 1, "target_r": 0})
    engine.apply_action("t1", "plan_route_chain", {"target_q": 2, "target_r": 0})
    engine.apply_action("t1", "edit_route", {"target_q": 1, "target_r": 0})
    rt = engine.get_runtime("t1")
    hexes = [(s["q"], s["r"]) for s in rt.route_steps if s.get("kind") == "hex"]
    assert hexes == [(1, 0)]
    engine.apply_action("t1", "clear_route", {})
    assert rt.route_steps == []


def test_open_door() -> None:
    engine, tok = _engine(ac=10.0)
    layer = engine.map_state.get_active_layer()
    assert layer is not None
    wall = WallSegment(openings=[Opening(kind="door", state="closed")])
    layer.walls[f"0,0:0"] = wall
    result = engine.apply_action("t1", "open_door", {})
    assert result.success
    assert wall.openings[0].state == "open"


def test_braced_move_preserves_firing_stance() -> None:
    engine, tok = _engine(ac=5.0, facing=0)
    rt = engine.get_runtime("t1")
    rt.firing_stance_held = True
    engine.apply_action("t1", "movement_while_braced", {"target_q": 1, "target_r": 0})
    assert tok.q == 1
    assert rt.firing_stance_held is True
    assert rt.braced is True
