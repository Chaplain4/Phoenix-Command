"""Map application of §2.7–2.10 / §5.13 incapacitation, disables, CTP survival, HT/20 CA."""

from __future__ import annotations

import random
from typing import TYPE_CHECKING, Literal

from phoenix_command.models.character import Character
from phoenix_command.models.enums import (
    AdvancedHitLocation,
    IncapacitationEffect,
    MedicalAid,
    SituationStanceModifier4B,
    WeaponType,
)
from phoenix_command.models.gear import Weapon
from phoenix_command.models.hit_result_advanced import DamageResult, ShotResult
from phoenix_command.models.recovery import Recovery
from phoenix_command.session.domains.impulse_combat_state import TokenCombatRuntime
from phoenix_command.session.domains.token_state import TokenState
from phoenix_command.simulations.map_knockdown import tokens_for_character
from phoenix_command.tables.core.table8_healing_and_recovery import Table8HealingAndRecovery

if TYPE_CHECKING:
    from phoenix_command.simulations.impulse_combat_engine import ActionResult, ImpulseCombatEngine

DisableKind = Literal["head_spine", "arm_l", "arm_r", "leg", "none"]

IMPULSES_PER_PHASE = 4

_INCAP_SEVERITY: dict[str, int] = {
    IncapacitationEffect.DISORIENTED.value: 1,
    IncapacitationEffect.DAZED.value: 2,
    IncapacitationEffect.STUNNED.value: 3,
    IncapacitationEffect.KNOCKED_OUT.value: 4,
    "Disoriented": 1,
    "Dazed": 2,
    "Stunned": 3,
    "Knocked Out": 4,
}

_OFFENSIVE_ACTIONS = frozenset(
    {
        "aim",
        "brace_weapon",
        "assume_firing_stance_cover",
        "assume_hip_firing_stance_cover",
        "look_over_cover",
        "pick_up_grenade",
        "arm_grenade",
        "reload",
        "cycle",
        "select_weapon",
    }
)

_NON_OFFENSIVE_OK = frozenset(
    {
        "duck",
        "duck_from_firing",
        "skip_impulse",
        "abandon_pending",
        "set_fire_mode",
        "recover",
        "recover_hands",
        "move",
        "set_medical_aid",
        "standing_to_prone",
        "kneeling_to_prone",
        "prone_to_kneeling",  # disoriented may change stance while fleeing
    }
)


def incap_severity(effect: str | IncapacitationEffect | None) -> int:
    if effect is None:
        return 0
    if isinstance(effect, IncapacitationEffect):
        return _INCAP_SEVERITY.get(effect.value, 0)
    return _INCAP_SEVERITY.get(effect, 0)


def merge_incapacitation(
    current: str | None,
    new: IncapacitationEffect | str | None,
) -> str | None:
    """Keep the more severe incapacitation; never downgrade."""
    if new is None:
        return current
    new_name = new.value if isinstance(new, IncapacitationEffect) else str(new)
    if incap_severity(new_name) >= incap_severity(current):
        return new_name
    return current


def classify_disable(location: AdvancedHitLocation) -> DisableKind:
    """Map advanced hit location to disabling injury category."""
    if location in (AdvancedHitLocation.MISS, AdvancedHitLocation.WEAPON_CRITICAL):
        return "none"
    name = location.name
    if (
        name.startswith(("HEAD", "SKULL", "FOREHEAD", "EYE", "MOUTH", "JAW", "NECK", "BASE_OF_SKULL"))
        or name == "BASE_OF_NECK"
        or "SPINE" in name
    ):
        return "head_spine"
    if name.startswith(("SHOULDER", "ARM", "ELBOW", "FOREARM", "HAND")):
        if "LEFT" in name:
            return "arm_l"
        if "RIGHT" in name:
            return "arm_r"
        if "OFF_SIDE" in name:
            return "arm_l"
        if "SHOT_SIDE" in name:
            return "arm_r"
        return "arm_l"
    if name.startswith(("LEG", "THIGH", "KNEE", "SHIN", "FOOT", "HIP", "ANKLE", "PELVIS")):
        return "leg"
    return "none"


def apply_disable_flags(rt: TokenCombatRuntime, location: AdvancedHitLocation) -> None:
    kind = classify_disable(location)
    if kind == "head_spine":
        rt.disabled_head_spine = True
        rt.ac_remaining = 0.0
    elif kind == "arm_l":
        rt.disabled_arm_left = True
    elif kind == "arm_r":
        rt.disabled_arm_right = True
    elif kind == "leg":
        rt.disabled_leg = True
        rt.stance = "prone"
        rt.braced = False


def wound_ca_penalty_from_healing_days(healing_days: float) -> float:
    """§2.10: CA penalty = Healing Time / 20 (rounded)."""
    return float(round(healing_days / 20.0))


def _medical_aid_from_name(name: str) -> MedicalAid:
    for aid in MedicalAid:
        if aid.value == name or aid.name == name:
            return aid
    return MedicalAid.NO_AID


def refresh_recovery_clock(
    rt: TokenCombatRuntime,
    character: Character,
    abs_impulse: int,
    *,
    allow_ctp_extend: bool = False,
) -> None:
    """Recompute HT / CTP / RR from current PD for rt.medical_aid."""
    if character.physical_damage_total <= 0:
        return
    recovery = Table8HealingAndRecovery.get_critical_time_period_and_recovery_chance_8a(
        character.physical_damage_total, character.health
    )
    apply_recovery_to_runtime(
        rt, recovery, abs_impulse, allow_ctp_extend=allow_ctp_extend
    )


def apply_recovery_to_runtime(
    rt: TokenCombatRuntime,
    recovery: Recovery | None,
    abs_impulse: int,
    *,
    allow_ctp_extend: bool = False,
) -> None:
    """Apply Table 8A Recovery to runtime CTP clock.

    New damage never lengthens an active CTP deadline (``min`` with candidate).
    After a successful RR, a new wound restarts onset at ``abs_impulse``.
    Medical-aid upgrades may extend via ``allow_ctp_extend=True``.
    """
    if recovery is None:
        return
    rt.healing_days = float(recovery.healing_time_in_days)
    aid = _medical_aid_from_name(rt.medical_aid)
    ctp_phases, rr = recovery.aid_data.get(aid, (None, None))
    if ctp_phases is None:
        ctp_phases = 0
    ctp_phases = int(ctp_phases)

    if not allow_ctp_extend and rt.ctp_resolved and not rt.is_dead:
        # New wound after surviving prior CTP — restart the clock
        rt.wound_onset_abs_impulse = abs_impulse
        rt.ctp_resolved = False
    elif rt.wound_onset_abs_impulse is None:
        rt.wound_onset_abs_impulse = abs_impulse

    onset = rt.wound_onset_abs_impulse
    if ctp_phases <= 0:
        rt.is_dead = True
        rt.ctp_deadline_abs_impulse = onset
        rt.recovery_rr = None
        rt.ctp_resolved = True
        rt.ac_remaining = 0.0
        return

    candidate = onset + ctp_phases * IMPULSES_PER_PHASE
    old = rt.ctp_deadline_abs_impulse
    if allow_ctp_extend or old is None:
        rt.ctp_deadline_abs_impulse = candidate
    else:
        # Active CTP + new damage: never extend past the prior deadline
        rt.ctp_deadline_abs_impulse = min(old, candidate)
    # RR 0 / missing → auto-death at CTP end (book: no Recovery Roll given)
    rt.recovery_rr = int(rr) if rr is not None and int(rr) > 0 else None


def apply_incap_to_runtime(
    rt: TokenCombatRuntime,
    effect: IncapacitationEffect | str | None,
    time_phases: int | None,
) -> bool:
    """Apply incap if not a downgrade. Returns True if status changed/accepted."""
    if effect is None:
        return False
    effect_name = effect.value if isinstance(effect, IncapacitationEffect) else str(effect)
    if incap_severity(effect_name) < incap_severity(rt.incap_effect):
        return False
    rt.incap_effect = effect_name
    if time_phases is not None:
        rt.incap_remaining_phases = max(0, int(time_phases))
    if rt.incap_effect == IncapacitationEffect.DAZED.value:
        rt.dazed_wait_impulses = max(rt.dazed_wait_impulses, 1)
    if rt.incap_effect in (
        IncapacitationEffect.KNOCKED_OUT.value,
        IncapacitationEffect.STUNNED.value,
    ):
        rt.ac_remaining = 0.0
    return True


def apply_damage_result_disables(rt: TokenCombatRuntime, damage: DamageResult | None) -> None:
    if damage is None or not damage.is_disabled:
        return
    apply_disable_flags(rt, damage.location)


def apply_shot_result_to_runtime(
    rt: TokenCombatRuntime,
    result: ShotResult,
    abs_impulse: int,
) -> None:
    if rt.is_dead:
        return
    if result.damage_result is not None:
        apply_damage_result_disables(rt, result.damage_result)
    if result.recovery is not None:
        apply_recovery_to_runtime(rt, result.recovery, abs_impulse)
    if result.incapacitation_effect is not None:
        apply_incap_to_runtime(
            rt,
            result.incapacitation_effect,
            result.incapacitation_time_phases,
        )


def result_has_wound(results: list[ShotResult]) -> bool:
    return any(
        (r.damage_result is not None and r.damage_result.damage > 0)
        or r.recovery is not None
        or r.incapacitation_effect is not None
        for r in results
    )


def apply_shot_wounds(
    shot_results: list[ShotResult],
    tokens: TokenState,
    runtime: dict[str, TokenCombatRuntime],
    characters: dict[str, Character],
    abs_impulse: int,
) -> None:
    """Apply disable / incap / CTP from map fire ShotResults onto token runtimes."""
    by_name: dict[str, list[ShotResult]] = {}
    for result in shot_results:
        if (
            result.damage_result is None
            and result.incapacitation_effect is None
            and result.recovery is None
        ):
            continue
        name = result.target.name
        by_name.setdefault(name, []).append(result)

    for name, results in by_name.items():
        char = characters.get(name)
        for tid in tokens_for_character(tokens, name):
            rt = runtime.get(tid)
            if rt is None:
                rt = TokenCombatRuntime()
                runtime[tid] = rt
            for result in results:
                apply_shot_result_to_runtime(rt, result, abs_impulse)
            if char is not None and char.physical_damage_total > 0 and result_has_wound(results):
                refresh_recovery_clock(rt, char, abs_impulse)


def resolve_ctp_if_due(rt: TokenCombatRuntime, abs_impulse: int, rng=random) -> str | None:
    """If CTP expired, roll RR or die. Returns log message or None."""
    if rt.is_dead or rt.ctp_resolved:
        return None
    if rt.ctp_deadline_abs_impulse is None:
        return None
    if abs_impulse < rt.ctp_deadline_abs_impulse:
        return None
    rt.ctp_resolved = True
    if rt.recovery_rr is None:
        rt.is_dead = True
        rt.ac_remaining = 0.0
        return "CTP expired with no Recovery Roll — dead"
    roll = rng.randint(0, 99)
    if roll > rt.recovery_rr:
        rt.is_dead = True
        rt.ac_remaining = 0.0
        return f"Recovery Roll {roll} > {rt.recovery_rr} — dead"
    rt.ctp_deadline_abs_impulse = None
    return f"Recovery Roll {roll} <= {rt.recovery_rr} — survived"


def tick_incap_phase(rt: TokenCombatRuntime) -> None:
    """Call once per game phase (4 impulses)."""
    if rt.is_dead or not rt.incap_effect:
        return
    if rt.incap_remaining_phases <= 0:
        return
    rt.incap_remaining_phases -= 1
    if rt.incap_remaining_phases <= 0:
        # Recovered from incapacitation → HT/20 CA penalty (§2.10)
        rt.incap_effect = None
        rt.dazed_wait_impulses = 0
        if rt.healing_days > 0:
            rt.wound_ca_penalty = wound_ca_penalty_from_healing_days(rt.healing_days)


def tick_impulse_flags(rt: TokenCombatRuntime) -> None:
    """Call every impulse advance."""
    if rt.dazed_wait_impulses > 0:
        rt.dazed_wait_impulses -= 1


def tick_wounds_on_impulse_advance(engine: "ImpulseCombatEngine") -> list[str]:
    """Tick incap (on phase boundary), dazed wait, and CTP. Returns log lines."""
    logs: list[str] = []
    abs_now = engine.absolute_impulse_index()
    phase_rolled = engine.impulse_combat.impulse == 0  # just wrapped into new phase
    for tid, rt in engine.impulse_combat.token_runtime.items():
        tick_impulse_flags(rt)
        if phase_rolled:
            tick_incap_phase(rt)
        msg = resolve_ctp_if_due(rt, abs_now)
        if msg:
            placement = engine.tokens.placements.get(tid)
            name = placement.character_name if placement else tid
            logs.append(f"{name}: {msg}")
    return logs


def effective_impulse_ac(base_ac: float, rt: TokenCombatRuntime) -> float:
    """Apply death / incap / HT/20 / Dazed half-CA to Table 1E AC."""
    if rt.is_dead or rt.disabled_head_spine:
        return 0.0
    if rt.incap_effect in (
        IncapacitationEffect.KNOCKED_OUT.value,
        IncapacitationEffect.STUNNED.value,
    ):
        return 0.0
    if rt.incap_effect == IncapacitationEffect.DAZED.value and rt.dazed_wait_impulses > 0:
        return 0.0
    ac = max(0.0, float(base_ac) - float(rt.wound_ca_penalty))
    if rt.incap_effect == IncapacitationEffect.DAZED.value:
        ac *= 0.5
    return ac


def is_pistol_weapon(weapon: Weapon | None) -> bool:
    if weapon is None:
        return False
    return getattr(weapon, "weapon_type", None) == WeaponType.AUTOMATIC_PISTOL


def one_hand_alm_for_shot(
    rt: TokenCombatRuntime,
    weapon: Weapon | None,
) -> SituationStanceModifier4B | None:
    """Table 4B one-hand ALM when one arm is disabled (other arm free)."""
    if rt.disabled_head_spine:
        return None
    left = rt.disabled_arm_left
    right = rt.disabled_arm_right
    if left and right:
        return None  # cannot fire at all — caller must block
    if not left and not right:
        return None
    if is_pistol_weapon(weapon):
        return SituationStanceModifier4B.FIRING_PISTOL_WITH_ONE_HAND
    return SituationStanceModifier4B.FIRING_RIFLE_WITH_ONE_HAND


def can_fire_weapon(rt: TokenCombatRuntime) -> tuple[bool, str]:
    if rt.is_dead:
        return False, "Character is dead"
    if rt.disabled_head_spine:
        return False, "Disabled head/spine — cannot act"
    if rt.disabled_arm_left and rt.disabled_arm_right:
        return False, "Both arms disabled — cannot fire"
    if rt.incap_effect in (
        IncapacitationEffect.KNOCKED_OUT.value,
        IncapacitationEffect.STUNNED.value,
    ):
        return False, f"{rt.incap_effect} — cannot act"
    if rt.incap_effect == IncapacitationEffect.DAZED.value:
        return False, "Dazed — no offensive actions"
    if rt.incap_effect == IncapacitationEffect.DISORIENTED.value:
        return False, "Disoriented — no offensive actions"
    return True, ""


def can_perform_action(
    rt: TokenCombatRuntime,
    action: str,
    args: dict | None = None,
) -> "ActionResult | None":
    """Return ActionResult failure if blocked by wounds/incap; else None."""
    from phoenix_command.simulations.impulse_combat_engine import ActionResult

    if action == "skip_impulse":
        return None
    if action == "set_medical_aid":
        if rt.is_dead:
            return ActionResult(False, "Character is dead")
        return None

    if rt.is_dead:
        return ActionResult(False, "Character is dead")
    if rt.disabled_head_spine:
        return ActionResult(False, "Disabled head/spine — cannot act")

    if rt.incap_effect in (
        IncapacitationEffect.KNOCKED_OUT.value,
        IncapacitationEffect.STUNNED.value,
    ):
        return ActionResult(False, f"{rt.incap_effect} — cannot act")

    if action in ("abandon_pending", "set_fire_mode"):
        return None

    if rt.incap_effect == IncapacitationEffect.DAZED.value:
        if rt.dazed_wait_impulses > 0:
            return ActionResult(False, "Dazed — recovering this impulse")
        if action in _OFFENSIVE_ACTIONS:
            return ActionResult(False, "Dazed — no offensive actions")
        if action in ("move", "movement_while_braced"):
            return None  # flee geometry enforced in _apply_move
        if action not in _NON_OFFENSIVE_OK and action not in STANCE_OK_DAZED:
            return ActionResult(False, "Dazed — limited actions only")
        return None

    if rt.incap_effect == IncapacitationEffect.DISORIENTED.value:
        if action in _OFFENSIVE_ACTIONS:
            return ActionResult(False, "Disoriented — no offensive actions")
        return None

    if rt.disabled_leg and action in (
        "standing_to_kneeling",
        "kneeling_to_standing",
        "prone_to_standing",
        "prone_to_kneeling",
        "standing_to_prone",
        "kneeling_to_prone",
    ):
        if action not in ("standing_to_prone", "kneeling_to_prone"):
            return ActionResult(False, "Disabled leg — crawl only (prone)")
    return None


STANCE_OK_DAZED = frozenset(
    {
        "standing_to_prone",
        "kneeling_to_prone",
        "standing_to_kneeling",
        "kneeling_to_standing",
        "prone_to_kneeling",
        "prone_to_standing",
    }
)


def min_dist_to_enemies(
    q: int,
    r: int,
    self_side: str | None,
    self_token_id: str,
    tokens: TokenState,
    runtime: dict[str, TokenCombatRuntime],
) -> int | None:
    """Minimum axial distance to any living enemy token, or None if none."""
    from phoenix_command.gui.utils.hex_geometry import axial_distance

    best: int | None = None
    for tid, tok in tokens.placements.items():
        if tid == self_token_id or not tok.character_name:
            continue
        if self_side is not None and tok.side_id == self_side:
            continue
        ert = runtime.get(tid)
        if ert is not None and ert.is_dead:
            continue
        d = axial_distance(q, r, tok.q, tok.r)
        if best is None or d < best:
            best = d
    return best


def move_closes_on_enemy(
    from_q: int,
    from_r: int,
    to_q: int,
    to_r: int,
    self_side: str | None,
    self_token_id: str,
    tokens: TokenState,
    runtime: dict[str, TokenCombatRuntime],
) -> bool:
    """True if moving to (to_q,to_r) reduces distance to any enemy."""
    d0 = min_dist_to_enemies(from_q, from_r, self_side, self_token_id, tokens, runtime)
    if d0 is None:
        return False
    d1 = min_dist_to_enemies(to_q, to_r, self_side, self_token_id, tokens, runtime)
    if d1 is None:
        return False
    return d1 < d0


def set_medical_aid(
    rt: TokenCombatRuntime,
    character: Character,
    aid: MedicalAid | str,
    abs_impulse: int,
) -> None:
    """Host upgrades medical aid; CTP clock still counted from wound onset."""
    if isinstance(aid, MedicalAid):
        rt.medical_aid = aid.value
    else:
        rt.medical_aid = str(aid)
    if not rt.is_dead:
        rt.ctp_resolved = False
    refresh_recovery_clock(rt, character, abs_impulse, allow_ctp_extend=True)
