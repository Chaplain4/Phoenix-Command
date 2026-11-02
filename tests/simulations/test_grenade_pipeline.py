"""Grenade pick up, arm, throw AC and fuse scheduler tests."""

from phoenix_command.models.character import Character
from phoenix_command.models.enums import Country, GrenadeType
from phoenix_command.models.gear import Grenade
from phoenix_command.session.domains.impulse_combat_state import (
    ImpulseCombatState,
    PendingShotPreview,
    TokenCombatRuntime,
)
from phoenix_command.session.domains.map_state import MapState
from phoenix_command.session.domains.token_state import TokenPlacement, TokenState
from phoenix_command.simulations.impulse_combat_engine import ImpulseCombatEngine
from phoenix_command.simulations.map_fire_ac import plan_fire_ac, validate_fire_ac


def _grenade() -> Grenade:
    return Grenade(
        name="HG 78 Frag Grenade",
        country=Country.AUSTRIA,
        grenade_type=GrenadeType.FRAG,
        weight=1.2,
        length=4.5,
        arm_time=3,
        fuse_length=2,
        range=14,
    )


def _engine(ac: float = 10.0) -> tuple[ImpulseCombatEngine, TokenPlacement]:
    ic = ImpulseCombatState(map_mode="combat", impulse=0)
    tokens = TokenState()
    tok = TokenPlacement(token_id="t1", character_name="G", q=0, r=0)
    tokens.placements["t1"] = tok
    char = Character(
        name="G",
        strength=12,
        intelligence=10,
        will=11,
        health=12,
        agility=10,
        gun_combat_skill_level=5,
    )
    char.add_gear(_grenade())
    ic.token_runtime["t1"] = TokenCombatRuntime(ac_remaining=ac)
    engine = ImpulseCombatEngine(ic, tokens, MapState(), {"G": char})
    return engine, tok


def test_pick_up_and_arm_grenade() -> None:
    engine, tok = _engine(ac=10.0)
    r1 = engine.apply_action(tok.token_id, "pick_up_grenade", {})
    assert r1.success
    rt = engine.get_runtime(tok.token_id)
    assert rt.held_grenade_name == "HG 78 Frag Grenade"
    assert rt.grenade_armed is False
    assert rt.ac_remaining == 8.0

    r2 = engine.apply_action(tok.token_id, "arm_grenade", {})
    assert r2.success
    assert rt.grenade_armed is True
    assert rt.ac_remaining == 5.0


def test_pick_up_grenade_by_name_when_multiple() -> None:
    """Named pick selects the requested grenade, not equipment[0]."""
    from phoenix_command.item_database.grenades import m67, rgd_5

    engine, tok = _engine(ac=10.0)
    char = engine.characters["G"]
    char.add_gear(m67)
    char.add_gear(rgd_5)
    # First grenade in equipment is still HG 78 from _engine.
    first = next(i.name for i in char.equipment if isinstance(i, Grenade))
    assert first != rgd_5.name
    r = engine.apply_action(
        tok.token_id, "pick_up_grenade", {"grenade_name": rgd_5.name}
    )
    assert r.success
    assert engine.get_runtime(tok.token_id).held_grenade_name == rgd_5.name


def test_throw_requires_armed() -> None:
    engine, tok = _engine(ac=10.0)
    engine.apply_action(tok.token_id, "pick_up_grenade", {})
    rt = engine.get_runtime(tok.token_id)
    preview = PendingShotPreview(
        preview_id="p",
        shooter_token_id="t1",
        target_token_id="",
        proposed_by="host",
        aim_time_ac=1,
    )
    plan = plan_fire_ac(preview, rt, "grenade", _grenade())
    ok, msg = validate_fire_ac(plan, rt, "grenade")
    assert not ok
    assert "Arm" in msg


def test_fuse_schedule_timing() -> None:
    engine, tok = _engine()
    expl = engine.schedule_grenade_explosion(
        "t1",
        8,
        {"preview_id": "p"},
        [{"hit": True, "eal": 0, "odds": 0, "roll": 0}],
        "HG 78 Frag Grenade",
        "HG 78 Frag Grenade",
    )
    assert expl.resolve_phase == 3
    assert expl.resolve_impulse == 0
    due = []
    for _ in range(8):
        _, due, _ = engine.advance_impulse()
    assert len(due) == 1
    assert len(engine.impulse_combat.pending_grenade_explosions) == 0


def test_impulse_burst_resets_each_impulse() -> None:
    engine, tok = _engine()
    rt = engine.get_runtime(tok.token_id)
    rt.impulse_burst_used = True
    engine.refill_impulse_ac()
    assert rt.impulse_burst_used is False


def test_cook_grenade_and_tick() -> None:
    engine, tok = _engine(ac=10.0)
    engine.apply_action(tok.token_id, "pick_up_grenade", {})
    engine.apply_action(tok.token_id, "arm_grenade", {})
    r = engine.apply_action(tok.token_id, "cook_grenade", {})
    assert r.success
    rt = engine.get_runtime(tok.token_id)
    assert rt.grenade_fuse_remaining_impulses == 8
    # Tick down without detonating
    for _ in range(7):
        hand, _, _ = engine.advance_impulse()
        # hand booms returned in due grenades slot
    rt = engine.get_runtime(tok.token_id)
    assert rt.grenade_fuse_remaining_impulses == 1
    due_proj, due_g, _ = engine.advance_impulse()
    assert rt.held_grenade_name is None
    assert any(getattr(e, "weapon_name", None) == "HG 78 Frag Grenade" for e in due_g)


def test_hand_detonation_applies_wounds_to_thrower() -> None:
    """BUG-04: cook-off applies blast PD + CTP/incap to thrower runtime."""
    from phoenix_command.item_database.grenades import m67
    from phoenix_command.simulations.map_fire_dispatch import (
        resolve_pending_grenade_explosion,
    )

    ic = ImpulseCombatState(map_mode="combat", impulse=0)
    tokens = TokenState()
    tok = TokenPlacement(token_id="t1", character_name="G", q=0, r=0, layer_id="L1")
    tokens.placements["t1"] = tok
    char = Character(
        name="G",
        strength=12,
        intelligence=10,
        will=11,
        health=12,
        agility=10,
        gun_combat_skill_level=5,
    )
    char.add_gear(m67)
    ic.token_runtime["t1"] = TokenCombatRuntime(
        ac_remaining=10.0,
        held_grenade_name=m67.name,
        grenade_armed=True,
        grenade_fuse_remaining_impulses=1,
    )
    map_state = MapState()
    map_state.ensure_default_layer()
    map_state.layers[0].id = "L1"
    engine = ImpulseCombatEngine(ic, tokens, map_state, {"G": char})

    _, due_g, _ = engine.advance_impulse()
    hand = next(e for e in due_g if getattr(e, "weapon_name", None) == m67.name)
    assert hand.preview_snapshot.get("shooter_token_id") == "t1"
    assert hand.preview_snapshot.get("aim_layer_id") == "L1"
    assert hand.preview_snapshot.get("hand_detonation") is True

    outcome = resolve_pending_grenade_explosion(
        hand,
        char,
        m67,
        m67,
        tokens,
        {"G": char},
        map_state,
        ic.token_runtime,
        abs_impulse=engine.absolute_impulse_index(),
    )
    thrower_hits = [r for r in outcome.shot_results if r.target is char and r.hit]
    assert thrower_hits, "thrower must receive blast/shrapnel ShotResults"
    assert char.physical_damage_total > 0

    rt = ic.token_runtime["t1"]
    label = rt.status_label()
    assert rt.incap_effect or rt.is_dead or rt.ctp_deadline_abs_impulse is not None, (
        f"expected incap/CTP/DEAD on thrower runtime, got label={label!r}"
    )
    assert "DEAD" in label or "CTP@" in label or (
        rt.incap_effect and rt.incap_effect in label
    )


def test_grenade_throw_costs_2_ac() -> None:
    rt = TokenCombatRuntime(ac_remaining=5.0, grenade_armed=True, weapon_cycled=True)
    plan = plan_fire_ac(
        PendingShotPreview(
            preview_id="p",
            shooter_token_id="t1",
            target_token_id="",
            proposed_by="host",
            aim_time_ac=1,
        ),
        rt,
        "grenade",
        _grenade(),
    )
    assert plan.fire_cost == 2.0
    ok, _ = validate_fire_ac(plan, rt, "grenade")
    assert ok


def test_lookup_grenade_after_consume() -> None:
    from phoenix_command.simulations.grenade_fuse import (
        consume_grenade,
        lookup_grenade_by_name,
    )
    from phoenix_command.item_database.grenades import rgd_5

    char = Character(
        name="G",
        strength=12,
        intelligence=10,
        will=11,
        health=12,
        agility=10,
        gun_combat_skill_level=5,
    )
    char.add_gear(rgd_5)
    assert consume_grenade(char, rgd_5.name)
    assert not any(getattr(i, "name", None) == rgd_5.name for i in char.equipment)
    found = lookup_grenade_by_name(rgd_5.name)
    assert found is not None
    assert found.name == rgd_5.name
    assert found.explosive_data


def test_fuse_resolve_uses_catalog_when_consumed() -> None:
    """Pending fuse blast must not depend on grenade still in equipment."""
    from phoenix_command.session.domains.impulse_combat_state import PendingGrenadeExplosion
    from phoenix_command.simulations.map_fire_dispatch import resolve_pending_grenade_explosion
    from phoenix_command.item_database.grenades import rgd_5
    from phoenix_command.simulations.grenade_fuse import lookup_grenade_by_name

    g = lookup_grenade_by_name(rgd_5.name)
    assert g is not None
    tokens = TokenState()
    tok = TokenPlacement(token_id="t1", character_name="G", q=0, r=0)
    tokens.placements["t1"] = tok
    char = Character(
        name="G",
        strength=12,
        intelligence=10,
        will=11,
        health=12,
        agility=10,
        gun_combat_skill_level=5,
    )
    # No grenade in inventory (already consumed).
    pending = PendingGrenadeExplosion(
        explosion_id="e1",
        resolve_phase=1,
        resolve_impulse=0,
        shooter_token_id="t1",
        preview_snapshot={"aim_q": 0, "aim_r": 0, "weapon_name": rgd_5.name},
        explosive_results=[
            {
                "hit": True,
                "eal": 0,
                "odds": 100,
                "roll": 0,
                "scatter_hexes": 0,
                "center_q": 0,
                "center_r": 0,
            }
        ],
        weapon_name=rgd_5.name,
        ammo_name=rgd_5.name,
    )
    map_state = MapState()
    map_state.ensure_default_layer()
    outcome = resolve_pending_grenade_explosion(
        pending,
        char,
        g,
        g,
        tokens,
        {"G": char},
        map_state,
        {},
        abs_impulse=1,
    )
    assert "no blast data" not in " ".join(outcome.messages).lower()
    assert outcome.blast_ammo is not None or outcome.shot_results or outcome.pending_blast
    # BUG-07: accuracy roll was logged at throw — do not re-emit on detonation.
    assert outcome.explosive_results == []
    assert any("Grenade explodes" in m for m in outcome.messages)


def test_grenade_throw_message_includes_roll_not_duplicate_channel() -> None:
    """BUG-07: throw messages carry roll/odds; kind=grenade for GUI skip of Explosive HIT."""
    from unittest.mock import patch

    from phoenix_command.item_database.grenades import m67
    from phoenix_command.models.hit_result_advanced import ExplosiveShotResult
    from phoenix_command.session.domains.impulse_combat_state import PendingShotPreview
    from phoenix_command.simulations.map_fire_dispatch import dispatch_map_fire

    tokens = TokenState()
    tok = TokenPlacement(token_id="t1", character_name="G", q=0, r=0)
    tokens.placements["t1"] = tok
    char = Character(
        name="G",
        strength=12,
        intelligence=10,
        will=11,
        health=12,
        agility=10,
        gun_combat_skill_level=5,
    )
    preview = PendingShotPreview(
        preview_id="p",
        shooter_token_id="t1",
        target_token_id="",
        proposed_by="host",
        fire_kind="grenade",
        aim_q=2,
        aim_r=0,
        aim_time_ac=1,
        weapon_name=m67.name,
        ammo_name=m67.name,
    )
    fake = ExplosiveShotResult(hit=True, eal=10, odds=53, roll=42, scatter_hexes=0)
    with patch(
        "phoenix_command.simulations.map_fire_dispatch.CombatSimulator.thrown_grenade",
        return_value=fake,
    ):
        outcome = dispatch_map_fire(
            preview,
            char,
            m67,
            m67,
            tokens,
            {"G": char},
            MapState(),
            {},
            apply_blast=False,
        )
    assert outcome.kind == "grenade"
    assert any("Grenade HIT (roll 42 vs 53%)" == m for m in outcome.messages)
    assert outcome.explosive_results  # still stored for fuse schedule / package
