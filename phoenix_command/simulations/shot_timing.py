"""§5.7 Master Phasing Count and §9.1 free-action gates."""

from __future__ import annotations

from phoenix_command.session.domains.impulse_combat_state import TokenCombatRuntime

# After firing, next non-snap shot this impulse needs Aim rebuild.
MPC_AIM_REBUILD_AC = 1.0
HIT_BEFORE_FIRE_ALM = -10


def stamp_mpc(rt: TokenCombatRuntime) -> float:
    """MPC stamp = AC already spent this impulse (before this fire's cost)."""
    return max(0.0, float(rt.ac_spent_this_impulse))


def record_ac_spend(rt: TokenCombatRuntime, amount: float) -> None:
    if amount > 0:
        rt.ac_spent_this_impulse += float(amount)


def after_fire_mpc(rt: TokenCombatRuntime) -> None:
    """Apply post-shot concentration debt (§5.7 engine reading)."""
    rt.mpc_aim_owed = max(rt.mpc_aim_owed, MPC_AIM_REBUILD_AC)


def apply_aim_toward_mpc(rt: TokenCombatRuntime, aim_ac: float) -> None:
    """Aim spend rebuilds concentration after a prior shot this impulse."""
    if aim_ac > 0 and rt.mpc_aim_owed > 0:
        rt.mpc_aim_owed = max(0.0, rt.mpc_aim_owed - float(aim_ac))


def clear_impulse_timing(rt: TokenCombatRuntime) -> None:
    rt.mpc_aim_owed = 0.0
    rt.ac_spent_this_impulse = 0.0
    rt.hexes_entered_this_impulse = 0
    rt.free_snaps_used_this_impulse = 0
    rt.free_tosses_used_this_impulse = 0
    rt.hit_before_fire_this_impulse = False


def mark_hit_this_impulse(rt: TokenCombatRuntime) -> None:
    rt.hit_before_fire_this_impulse = True


def validate_aim_vs_mpc(rt: TokenCombatRuntime, effective_aim_time: int) -> tuple[bool, str]:
    """Non-snap shots require mpc_aim_owed cleared via Aim AC spend."""
    if effective_aim_time <= 1:
        return True, ""
    if rt.mpc_aim_owed > 1e-9:
        return False, (
            f"MPC: need {rt.mpc_aim_owed:.0f} Aim AC rebuild this impulse "
            f"before Aim Time {effective_aim_time}"
        )
    return True, ""


def can_free_snap(rt: TokenCombatRuntime) -> bool:
    """One free snap or toss per hex entered this impulse."""
    if rt.hexes_entered_this_impulse <= 0:
        return False
    used = rt.free_snaps_used_this_impulse + rt.free_tosses_used_this_impulse
    return used < rt.hexes_entered_this_impulse


def can_free_toss(rt: TokenCombatRuntime) -> bool:
    return can_free_snap(rt)


def note_hex_entered(rt: TokenCombatRuntime) -> None:
    rt.hexes_entered_this_impulse += 1
    rt.moved_this_impulse = True
