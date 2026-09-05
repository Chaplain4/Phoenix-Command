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
