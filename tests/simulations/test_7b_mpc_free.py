"""Table 7B dual-path, §5.7 MPC, and §9.1 free-action tests."""

from phoenix_command.models.character import Character
from phoenix_command.models.enums import Caliber, Country, WeaponType
from phoenix_command.models.gear import Weapon
from phoenix_command.session.domains.impulse_combat_state import (
    ImpulseCombatState,
    TokenCombatRuntime,
)
from phoenix_command.session.domains.map_state import MapState, Opening, WallSegment
from phoenix_command.session.domains.token_state import TokenPlacement, TokenState
from phoenix_command.simulations.impulse_combat_engine import ImpulseCombatEngine
from phoenix_command.simulations.map_fire_ac import plan_fire_ac, validate_fire_ac
from phoenix_command.session.domains.impulse_combat_state import PendingShotPreview
from phoenix_command.simulations import shot_timing


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


def _engine(ac: float = 20.0) -> tuple[ImpulseCombatEngine, TokenPlacement]:
    ic = ImpulseCombatState(map_mode="combat", impulse=0)
    tokens = TokenState()
    tok = TokenPlacement(
        token_id="t1", character_name="Fighter", q=0, r=0, facing=0, side_id="a"
    )
    tokens.placements["t1"] = tok
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
    pistol = Weapon(
        name="Test Pistol",
        weight=2.0,
        caliber=Caliber.CAL_9MM_PARABELLUM,
        weapon_type=WeaponType.AUTOMATIC_PISTOL,
        country=Country.USA,
        length_deployed=8.0,
        reload_time=4,
        actions_to_cycle=None,
    )
    char.add_gear(weapon)
    char.add_gear(pistol)
    ic.token_runtime["t1"] = TokenCombatRuntime(ac_remaining=ac, stance="standing")
    engine = ImpulseCombatEngine(ic, tokens, MapState(), {"Fighter": char})
    engine.get_runtime("t1").held_weapon_name = "Test Rifle"
    return engine, tok


def test_reload_micro_steps() -> None:
    engine, _ = _engine()
    r1 = engine.apply_action("t1", "take_bullet_magazine", {})
    assert r1.success
    rt = engine.get_runtime("t1")
    assert rt.mag_in_hand is True
    r2 = engine.apply_action("t1", "replace_bullet_magazine", {})
    assert r2.success
    assert rt.mag_in_hand is False
    assert rt.weapon_cycled is True


def test_draw_modern_holster() -> None:
    engine, _ = _engine()
    r = engine.apply_action("t1", "draw_modern_holster", {})
    assert r.success
    assert engine.get_runtime("t1").held_weapon_name == "Test Pistol"


def test_equipment_scope_in() -> None:
    engine, _ = _engine()
    r = engine.apply_action("t1", "scope_in", {})
    assert r.success
    assert engine.get_runtime("t1").equipment_flags.get("scope") is True


def test_climb_through_window() -> None:
    engine, tok = _engine(ac=20.0)
    layer = engine.map_state.get_active_layer()
    assert layer is not None
    wall = WallSegment(openings=[Opening(kind="window", state="closed")])
    layer.walls["0,0:0"] = wall
    r = engine.apply_action("t1", "climb_through_window", {})
    assert r.success
    assert tok.q == 1 and tok.r == 0
    assert wall.openings[0].state == "open"


def test_mpc_blocks_non_snap_after_fire() -> None:
    from phoenix_command.simulations.map_fire_ac import apply_fire_ac, clear_aim_state

    rt = TokenCombatRuntime(ac_remaining=5.0, weapon_cycled=True, aim_ac_accumulated=3.0)
    preview = PendingShotPreview(
        preview_id="p",
        shooter_token_id="t1",
        target_token_id="t2",
        proposed_by="host",
        aim_time_ac=3,
    )
    plan = plan_fire_ac(preview, rt, "single", None)
    assert plan.effective_aim_time == 3
    ok, _ = validate_fire_ac(plan, rt, "single")
    assert ok

    apply_fire_ac(plan, rt)
    assert rt.mpc_aim_owed >= 1.0
    # Confirm path clears aim bank — requested Aim Time>1 must still hit MPC gate.
    clear_aim_state(rt)
    preview.aim_time_ac = 3
    plan2 = plan_fire_ac(preview, rt, "single", None)
    assert plan2.effective_aim_time == 1
    assert plan2.requested_aim_time == 3
    ok2, msg = validate_fire_ac(plan2, rt, "single")
    assert not ok2
    assert "MPC" in msg
    # Snap still OK
    preview.aim_time_ac = 1
    plan3 = plan_fire_ac(preview, rt, "single", None)
    assert plan3.effective_aim_time == 1
    ok3, _ = validate_fire_ac(plan3, rt, "single")
    assert ok3


def test_hex_entered_still_tracked() -> None:
    engine, tok = _engine(ac=10.0)
    rt = engine.get_runtime("t1")
    engine.apply_action("t1", "move", {"target_q": 1, "target_r": 0})
    assert tok.q == 1
    assert rt.hexes_entered_this_impulse == 1


def test_safety_fire_select() -> None:
    engine, _ = _engine()
    rt = engine.get_runtime("t1")
    rt.fire_mode = "single"
    r = engine.apply_action("t1", "safety_fire_select", {"fire_mode": "auto"})
    assert r.success
    assert rt.fire_mode == "auto"


def test_runtime_mpc_serialize() -> None:
    import json

    rt = TokenCombatRuntime(
        mpc_aim_owed=1.0,
        hexes_entered_this_impulse=2,
        free_snaps_used_this_impulse=1,
        grenade_fuse_remaining_impulses=3,
        mag_in_hand=True,
        equipment_flags={"scope": True},
    )
    raw = json.loads(json.dumps(rt.to_dict()))
    back = TokenCombatRuntime.from_dict(raw)
    assert back.mpc_aim_owed == 1.0
    assert back.hexes_entered_this_impulse == 2
    assert back.grenade_fuse_remaining_impulses == 3
    assert back.equipment_flags.get("scope") is True
