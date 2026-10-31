"""§5.7 deferred same-impulse fire queue (MPC order)."""

from phoenix_command.session.domains.impulse_combat_state import (
    ImpulseCombatState,
    PendingShotPreview,
    TokenCombatRuntime,
)
from phoenix_command.simulations import impulse_fire_queue as ifq
from phoenix_command.simulations import shot_timing
from phoenix_command.simulations.map_shot_context import build_map_shot_context
from phoenix_command.session.domains.map_state import MapState
from phoenix_command.session.domains.token_state import TokenPlacement


def _preview(shooter: str, note: str = "") -> PendingShotPreview:
    return PendingShotPreview(
        preview_id=f"p-{shooter}",
        shooter_token_id=shooter,
        target_token_id="tgt",
        proposed_by="host",
        weapon_name="Test Rifle",
        ammo_name="Ball",
        notes=[note] if note else [],
    )


def test_drain_orders_by_mpc_then_fire_id() -> None:
    state = ImpulseCombatState()
    # Higher MPC enqueued first (UI reverse order).
    ifq.enqueue_impulse_fire(state, "b", _preview("b"), mpc_stamp=2.0)
    ifq.enqueue_impulse_fire(state, "a", _preview("a"), mpc_stamp=0.0)
    ifq.enqueue_impulse_fire(state, "c", _preview("c"), mpc_stamp=2.0)
    ordered = ifq.take_sorted_impulse_fires(state)
    assert [f.shooter_token_id for f in ordered] == ["a", "b", "c"] or (
        ordered[0].shooter_token_id == "a"
        and ordered[1].mpc_stamp == 2.0
        and ordered[2].mpc_stamp == 2.0
    )
    assert ordered[0].mpc_stamp == 0.0
    assert ordered[1].mpc_stamp == 2.0
    assert ordered[2].mpc_stamp == 2.0
    # Tie-break stable by fire_id
    assert ordered[1].fire_id <= ordered[2].fire_id
    assert state.pending_impulse_fires == []


def test_fire_cancel_when_incapacitated() -> None:
    dead = TokenCombatRuntime(is_dead=True)
    cancel, msg = ifq.fire_should_cancel(dead)
    assert cancel
    assert "dead" in msg.lower() or "incap" in msg.lower()

    ko = TokenCombatRuntime(incap_effect="Knocked Out")
    cancel, _ = ifq.fire_should_cancel(ko)
    assert cancel

    stunned = TokenCombatRuntime(incap_effect="Stunned")
    cancel, _ = ifq.fire_should_cancel(stunned)
    assert cancel

    ok_rt = TokenCombatRuntime()
    cancel, _ = ifq.fire_should_cancel(ok_rt)
    assert not cancel


def test_hit_before_fire_adds_minus_10_alm_in_context() -> None:
    shooter = TokenPlacement(
        token_id="s1", character_name="A", q=0, r=0, facing=0, side_id="a"
    )
    target = TokenPlacement(
        token_id="t1", character_name="B", q=3, r=0, facing=3, side_id="b"
    )
    rt = TokenCombatRuntime(hit_before_fire_this_impulse=True)
    tgt_rt = TokenCombatRuntime()
    ctx = build_map_shot_context(shooter, rt, target, tgt_rt, MapState())
    mods = list(ctx.shot_params.custom_eal_modifiers or [])
    labels = [m[0] for m in mods]
    assert any("Hit before fire" in lab for lab in labels)
    vals = [m[1] for m in mods if "Hit before fire" in m[0]]
    assert vals and vals[0] == shot_timing.HIT_BEFORE_FIRE_ALM


def test_tof_path_does_not_require_queue() -> None:
    """TOF uses PendingProjectile; queue helpers are independent."""
    state = ImpulseCombatState()
    assert state.pending_impulse_fires == []
    # Scheduling a projectile does not touch the impulse fire queue.
    from phoenix_command.simulations.impulse_combat_engine import ImpulseCombatEngine
    from phoenix_command.session.domains.token_state import TokenState
    from phoenix_command.models.character import Character

    tokens = TokenState()
    tokens.placements["s1"] = TokenPlacement(
        token_id="s1", character_name="A", q=0, r=0, facing=0, side_id="a"
    )
    ic = ImpulseCombatState(map_mode="combat")
    char = Character(
        name="A",
        strength=10,
        intelligence=10,
        will=10,
        health=10,
        agility=10,
        gun_combat_skill_level=5,
    )
    engine = ImpulseCombatEngine(ic, tokens, MapState(), {"A": char})

    engine.schedule_projectile("s1", "t1", 2, {"weapon_name": "Test"})
    assert ic.pending_impulse_fires == []
    assert len(ic.pending_projectiles) == 1


def test_pending_impulse_fire_serialization_round_trip() -> None:
    state = ImpulseCombatState()
    ifq.enqueue_impulse_fire(state, "s1", _preview("s1", "note"), mpc_stamp=1.5)
    raw = state.to_dict()
    restored = ImpulseCombatState.from_dict(raw)
    assert len(restored.pending_impulse_fires) == 1
    pf = restored.pending_impulse_fires[0]
    assert pf.shooter_token_id == "s1"
    assert pf.mpc_stamp == 1.5
    assert pf.preview_snapshot.get("weapon_name") == "Test Rifle"
    assert pf.preview_snapshot.get("notes") == ["note"]


def test_mpc_stamp_before_fire_cost() -> None:
    rt = TokenCombatRuntime()
    shot_timing.record_ac_spend(rt, 3.0)
    assert ifq.mpc_stamp_before_fire_cost(rt) == 3.0
    # Fire cost recorded after stamp would raise spend — stamp stays pre-fire.
    shot_timing.record_ac_spend(rt, 1.0)
    assert ifq.mpc_stamp_before_fire_cost(rt) == 4.0


def test_refill_clears_pending_impulse_fires() -> None:
    from phoenix_command.simulations.impulse_combat_engine import ImpulseCombatEngine
    from phoenix_command.session.domains.token_state import TokenState
    from phoenix_command.models.character import Character

    tokens = TokenState()
    tokens.placements["s1"] = TokenPlacement(
        token_id="s1", character_name="A", q=0, r=0, facing=0, side_id="a"
    )
    char = Character(
        name="A",
        strength=10,
        intelligence=10,
        will=10,
        health=10,
        agility=10,
        gun_combat_skill_level=5,
    )
    ic = ImpulseCombatState(map_mode="combat", impulse=0)
    ifq.enqueue_impulse_fire(ic, "s1", _preview("s1"), mpc_stamp=0.0)
    assert ic.pending_impulse_fires
    engine = ImpulseCombatEngine(ic, tokens, MapState(), {"A": char})
    engine.refill_impulse_ac()
    assert ic.pending_impulse_fires == []
