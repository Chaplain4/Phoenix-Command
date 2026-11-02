"""Map fire AC validation and aim state for Confirm shot."""

from __future__ import annotations

from dataclasses import dataclass

from phoenix_command.models.enums import SituationStanceModifier4B
from phoenix_command.models.gear import Grenade, Weapon
from phoenix_command.session.domains.impulse_combat_state import (
    PendingShotPreview,
    TokenCombatRuntime,
)
from phoenix_command.simulations.map_knockdown import BURST_FIRE_KINDS
from phoenix_command.simulations.shot_timing import (
    after_fire_mpc,
    record_ac_spend,
    validate_aim_vs_mpc,
)
from phoenix_command.simulations.grenade_fuse import clear_grenade_state
from phoenix_command.tables.catalogs.action_catalog import BUILTIN_ACTIONS

SINGLE_FIRE_KINDS = frozenset({"single", "shotgun"})
FIRE_COST_AC = 1.0
GRENADE_THROW_AC = float(BUILTIN_ACTIONS["throw_small_object"].cost)


@dataclass
class FireAcPlan:
    """AC and aim model for one Confirm fire action."""

    fire_cost: float = FIRE_COST_AC
    is_hip: bool = False
    effective_aim_time: int = 1
    requested_aim_time: int = 1
    is_burst: bool = False
    is_grenade: bool = False
    grenade_arm_time: int = 0


def proper_firing_stance(rt: TokenCombatRuntime) -> bool:
    """True when weapon is in a proper (non-hip) firing stance — clears −6 hip ALM."""
    return bool(rt.firing_stance_held)


def plan_fire_ac(
    preview: PendingShotPreview,
    shooter_rt: TokenCombatRuntime,
    fire_kind: str,
    weapon: Weapon | Grenade | None,
) -> FireAcPlan:
    """Derive hip from stance and aim time from accumulated Aim AC (independent)."""
    is_grenade = fire_kind == "grenade" or isinstance(weapon, Grenade)
    is_burst = fire_kind in BURST_FIRE_KINDS
    grenade_arm_time = 0
    if is_grenade and isinstance(weapon, Grenade):
        grenade_arm_time = int(weapon.arm_time or 0)

    accumulated = int(shooter_rt.aim_ac_accumulated or 0)
    is_hip = not is_grenade and not proper_firing_stance(shooter_rt)
    requested = max(1, int(preview.aim_time_ac or 1))

    if is_grenade:
        if accumulated > 0:
            effective = max(1, min(requested, accumulated))
        else:
            effective = requested
        fire_cost = GRENADE_THROW_AC
    elif accumulated > 0:
        effective = max(1, min(requested, accumulated))
        fire_cost = FIRE_COST_AC
    else:
        # No Aim banked: hip/snap column only (Aim Time 1). Requested >1 is gated in validate.
        effective = 1
        fire_cost = FIRE_COST_AC

    return FireAcPlan(
        fire_cost=fire_cost,
        is_hip=is_hip,
        effective_aim_time=effective,
        requested_aim_time=requested,
        is_burst=is_burst,
        is_grenade=is_grenade,
        grenade_arm_time=grenade_arm_time,
    )


def sync_preview_from_plan(
    preview: PendingShotPreview,
    plan: FireAcPlan,
    shooter_rt: TokenCombatRuntime,
) -> None:
    """Apply hip fire mods and aim time to preview before resolve."""
    preview.aim_time_ac = plan.effective_aim_time
    hip_name = SituationStanceModifier4B.FIRING_FROM_THE_HIP.name
    if plan.is_hip:
        if hip_name not in preview.stance_mods:
            preview.stance_mods = list(preview.stance_mods) + [hip_name]
        note = "Hip fire (not in firing stance)"
        if note not in " ".join(preview.notes):
            preview.notes = list(preview.notes) + [note]
    else:
        preview.stance_mods = [m for m in preview.stance_mods if m != hip_name]
    aim_note = f"Aim time {plan.effective_aim_time}"
    if aim_note not in " ".join(preview.notes):
        preview.notes = list(preview.notes) + [aim_note]


def validate_fire_ac(
    plan: FireAcPlan,
    rt: TokenCombatRuntime,
    fire_kind: str,
) -> tuple[bool, str]:
    owed = max(0.0, rt.recoil_ac_owed) + max(0.0, rt.balance_ac_owed)
    if owed > rt.ac_remaining:
        return False, f"Need {owed:.0f} AC to recover (recoil/balance) first"
    if fire_kind in SINGLE_FIRE_KINDS and not rt.weapon_cycled:
        return False, "Cycle weapon first"
    if rt.ac_remaining < plan.fire_cost:
        return False, f"Need {plan.fire_cost:.0f} AC, have {rt.ac_remaining:.1f}"
    if plan.is_burst and rt.impulse_burst_used:
        return False, "Already fired a burst this impulse"
    if plan.is_grenade and plan.grenade_arm_time > 0 and not rt.grenade_armed:
        return False, "Arm grenade first"
    # Use requested Aim Time so preview Aim Time>1 cannot silently become snap after fire.
    ok_mpc, mpc_msg = validate_aim_vs_mpc(rt, plan.requested_aim_time)
    if not ok_mpc:
        return False, mpc_msg
    if not plan.is_grenade and plan.requested_aim_time > 1:
        if rt.aim_ac_accumulated < plan.requested_aim_time:
            return False, (
                f"Need {plan.requested_aim_time} AC aim, "
                f"have {int(rt.aim_ac_accumulated)}"
            )
    return True, ""


def apply_fire_ac(plan: FireAcPlan, rt: TokenCombatRuntime) -> None:
    if plan.fire_cost > 0:
        rt.ac_remaining -= plan.fire_cost
        record_ac_spend(rt, plan.fire_cost)
    if plan.is_burst:
        rt.impulse_burst_used = True
    after_fire_mpc(rt)


def clear_aim_state(rt: TokenCombatRuntime) -> None:
    rt.aim_ac_accumulated = 0.0
    rt.aim_ac_this_impulse = 0.0
    rt.aim_target_token_id = None
    rt.aim_impulses = 0
    rt.aimed_this_impulse = False


def clear_grenade_hand(rt: TokenCombatRuntime) -> None:
    clear_grenade_state(rt)
