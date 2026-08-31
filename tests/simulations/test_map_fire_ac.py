"""Tests for map fire AC gate and aim state."""

from phoenix_command.models.character import Character
from phoenix_command.models.enums import Caliber, Country, WeaponType
from phoenix_command.models.gear import Weapon
from phoenix_command.session.domains.impulse_combat_state import (
    PendingShotPreview,
    TokenCombatRuntime,
)
from phoenix_command.simulations.map_fire_ac import (
    apply_fire_ac,
    clear_aim_state,
    plan_fire_ac,
    validate_fire_ac,
)
from phoenix_command.simulations.map_shot_context import build_map_shot_context
from phoenix_command.session.domains.token_state import TokenPlacement


def _fighter() -> Character:
    return Character(
        name="F",
        strength=12,
        intelligence=10,
        will=11,
        health=12,
        agility=10,
        gun_combat_skill_level=5,
    )


def _preview() -> PendingShotPreview:
    return PendingShotPreview(
        preview_id="p1",
        shooter_token_id="t1",
        target_token_id="t2",
        proposed_by="host",
        aim_time_ac=1,
    )


def test_hip_fire_plan_and_validate() -> None:
    rt = TokenCombatRuntime(ac_remaining=2.0, weapon_cycled=True)
    plan = plan_fire_ac(_preview(), rt, "single", None)
    assert plan.is_hip is True
    assert plan.effective_aim_time == 1
    ok, _ = validate_fire_ac(plan, rt, "single")
    assert ok
    apply_fire_ac(plan, rt)
    assert rt.ac_remaining == 1.0


def test_confirm_rejects_without_ac() -> None:
    rt = TokenCombatRuntime(ac_remaining=0.0, weapon_cycled=True)
    plan = plan_fire_ac(_preview(), rt, "single", None)
    ok, msg = validate_fire_ac(plan, rt, "single")
    assert not ok
    assert "AC" in msg


def test_aimed_caps_to_accumulated() -> None:
    rt = TokenCombatRuntime(ac_remaining=3.0, aim_ac_accumulated=2.0, weapon_cycled=True)
    preview = _preview()
    preview.aim_time_ac = 3
    plan = plan_fire_ac(preview, rt, "single", None)
    assert plan.is_hip is False
    assert plan.effective_aim_time == 2
    ok, _ = validate_fire_ac(plan, rt, "single")
    assert ok


def test_burst_cap_per_impulse() -> None:
    rt = TokenCombatRuntime(ac_remaining=3.0, impulse_burst_used=True, weapon_cycled=True)
    plan = plan_fire_ac(_preview(), rt, "burst", None)
    ok, msg = validate_fire_ac(plan, rt, "burst")
    assert not ok
    assert "burst" in msg.lower()


def test_clear_aim_state() -> None:
    rt = TokenCombatRuntime(
        aim_ac_accumulated=4.0,
        aim_target_token_id="t2",
        aim_impulses=2,
        aimed_this_impulse=True,
    )
    clear_aim_state(rt)
    assert rt.aim_ac_accumulated == 0.0
    assert rt.aim_target_token_id is None
    assert rt.aim_impulses == 0


def test_build_map_shot_context_hip_not_two() -> None:
    shooter = TokenPlacement(token_id="s", q=0, r=0)
    target = TokenPlacement(token_id="t", q=2, r=0)
    rt = TokenCombatRuntime()
    ctx = build_map_shot_context(shooter, rt, target, rt, None)
    assert ctx.shot_params.aim_time_ac == 1
    from phoenix_command.models.enums import SituationStanceModifier4B

    assert SituationStanceModifier4B.FIRING_FROM_THE_HIP in ctx.shot_params.situation_stance_modifiers
