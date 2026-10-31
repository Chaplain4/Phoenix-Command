"""§5.7 same-impulse fire queue: enqueue + MPC-ordered drain."""

from __future__ import annotations

import uuid

from phoenix_command.session.domains.impulse_combat_state import (
    ImpulseCombatState,
    PendingImpulseFire,
    PendingShotPreview,
    TokenCombatRuntime,
)
from phoenix_command.simulations.map_wounds import can_fire_weapon
from phoenix_command.simulations.shot_timing import stamp_mpc


def enqueue_impulse_fire(
    state: ImpulseCombatState,
    shooter_token_id: str,
    preview: PendingShotPreview,
    mpc_stamp: float,
) -> PendingImpulseFire:
    """Append a committed fire to the same-impulse queue."""
    item = PendingImpulseFire(
        fire_id=str(uuid.uuid4()),
        shooter_token_id=shooter_token_id,
        mpc_stamp=float(mpc_stamp),
        preview_snapshot=preview.to_dict(),
    )
    state.pending_impulse_fires.append(item)
    return item


def take_sorted_impulse_fires(state: ImpulseCombatState) -> list[PendingImpulseFire]:
    """Pop all pending fires sorted by (mpc_stamp, fire_id)."""
    items = list(state.pending_impulse_fires)
    state.pending_impulse_fires.clear()
    items.sort(key=lambda f: (f.mpc_stamp, f.fire_id))
    return items


def clear_impulse_fires(state: ImpulseCombatState) -> None:
    state.pending_impulse_fires.clear()


def fire_should_cancel(rt: TokenCombatRuntime | None) -> tuple[bool, str]:
    """True if shooter cannot resolve a queued fire (dead / KO / Stunned / spine)."""
    if rt is None:
        return True, "Shooter runtime missing"
    ok, msg = can_fire_weapon(rt)
    if not ok:
        return True, msg
    if rt.incap_effect in ("Knocked Out", "Stunned"):
        return True, f"{rt.incap_effect} — fire cancelled"
    if rt.is_dead or rt.disabled_head_spine:
        return True, "Shooter incapacitated — fire cancelled"
    return False, ""


def mpc_stamp_before_fire_cost(rt: TokenCombatRuntime) -> float:
    """MPC stamp = AC spent this impulse before deducting this fire's cost."""
    return stamp_mpc(rt)
