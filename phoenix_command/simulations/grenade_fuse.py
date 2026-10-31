"""Grenade fuse / cook-off helpers (§3.6)."""

from __future__ import annotations

from phoenix_command.models.character import Character
from phoenix_command.models.gear import Grenade
from phoenix_command.session.domains.impulse_combat_state import TokenCombatRuntime


def fuse_impulses_for(grenade: Grenade) -> int:
    return max(0, int(grenade.fuse_length or 0) * 4)


def start_cook(rt: TokenCombatRuntime, grenade: Grenade) -> tuple[bool, str]:
    if not rt.held_grenade_name:
        return False, "No grenade in hand"
    if not rt.grenade_armed and (grenade.arm_time or 0) > 0:
        return False, "Arm grenade first"
    phases = int(grenade.fuse_length or 0)
    if phases <= 0:
        return False, "Impact fuse — cannot cook"
    if rt.grenade_fuse_remaining_impulses is not None:
        return False, "Already cooking"
    rt.grenade_fuse_remaining_impulses = fuse_impulses_for(grenade)
    rt.grenade_armed = True
    return True, f"Cooking {grenade.name} ({rt.grenade_fuse_remaining_impulses} impulses)"


def clear_grenade_state(rt: TokenCombatRuntime) -> None:
    rt.held_grenade_name = None
    rt.grenade_armed = False
    rt.grenade_fuse_remaining_impulses = None


def consume_grenade(char: Character | None, grenade_name: str | None) -> bool:
    """Remove one matching grenade from character equipment."""
    if not char or not grenade_name:
        return False
    for i, item in enumerate(list(char.equipment)):
        if isinstance(item, Grenade) and item.name == grenade_name:
            char.equipment.pop(i)
            return True
    return False


def throw_fuse_impulses(rt: TokenCombatRuntime, grenade: Grenade) -> int:
    """Impulses until blast after throw: remaining if cooking, else full fuse."""
    if rt.grenade_fuse_remaining_impulses is not None:
        return max(0, int(rt.grenade_fuse_remaining_impulses))
    return fuse_impulses_for(grenade)
