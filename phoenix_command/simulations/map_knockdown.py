"""Apply §5.12 Knock Down, §6.9 recoil, and §5.8 second-shot to map token runtime."""

from __future__ import annotations

from phoenix_command.models.character import Character
from phoenix_command.models.gear import Weapon
from phoenix_command.models.hit_result_advanced import ShotResult
from phoenix_command.session.domains.impulse_combat_state import TokenCombatRuntime
from phoenix_command.session.domains.token_state import TokenPlacement, TokenState
from phoenix_command.tables.advanced_rules.knock_down import KnockDownEffect
from phoenix_command.tables.advanced_rules.recoil_recovery import recoil_recovery_ac

HANDS_FREE_AC = 3.0

BURST_FIRE_KINDS = frozenset({"burst", "3rb", "agl", "shotgun_burst"})


def second_shot_aim_bonus(
    rt: TokenCombatRuntime,
    target_q: int,
    target_r: int,
    layer_id: str = "",
) -> int:
    """+1 AC aim time when stationary, stance held, same hex as last shot (§5.8)."""
    if not rt.firing_stance_held:
        return 0
    if rt.last_shot_q is None or rt.last_shot_r is None:
        return 0
    if rt.last_shot_q != target_q or rt.last_shot_r != target_r:
        return 0
    last_layer = rt.last_shot_layer_id or ""
    if last_layer != (layer_id or ""):
        return 0
    return 1


def apply_knock_down_effects(rt: TokenCombatRuntime, effects: list[KnockDownEffect]) -> None:
    """Worst effect wins for off-feet; AC penalties from other hits sum."""
    real = [e for e in effects if e is not None and not e.is_none()]
    if not real:
        return
    off = any(e.off_feet for e in real)
    ac = sum(e.ac_penalty for e in real if not e.off_feet)
    if ac:
        rt.balance_ac_owed += float(ac)
    if off:
        rt.stance = "prone"
        rt.knockdown_phase = "falling"
        rt.hands_free = False
        rt.ac_remaining = 0.0
        rt.braced = False
        rt.firing_stance_held = False
        rt.looking_over_cover = False


def tokens_for_character(tokens: TokenState, name: str) -> list[str]:
    return [
        tid
        for tid, p in tokens.placements.items()
        if p.character_name == name
    ]


def apply_shot_knockdowns(
    shot_results: list[ShotResult],
    tokens: TokenState,
    runtime: dict[str, TokenCombatRuntime],
) -> None:
    by_name: dict[str, list[KnockDownEffect]] = {}
    for result in shot_results:
        kd = getattr(result, "knock_down", None)
        if kd is None or kd.is_none():
            continue
        name = result.target.name
        by_name.setdefault(name, []).append(kd)
    for name, effects in by_name.items():
        for tid in tokens_for_character(tokens, name):
            rt = runtime.get(tid)
            if rt is None:
                rt = TokenCombatRuntime()
                runtime[tid] = rt
            apply_knock_down_effects(rt, effects)


def apply_shooter_after_fire(
    rt: TokenCombatRuntime,
    *,
    fire_kind: str,
    weapon: Weapon | None,
    shooter: Character,
    aim_tok: TokenPlacement | None,
    aim_q: int | None,
    aim_r: int | None,
    aim_layer_id: str = "",
) -> None:
    q = aim_tok.q if aim_tok is not None else aim_q
    r = aim_tok.r if aim_tok is not None else aim_r
    layer = (aim_tok.layer_id if aim_tok is not None else aim_layer_id) or ""
    if q is not None and r is not None:
        rt.last_shot_q = int(q)
        rt.last_shot_r = int(r)
        rt.last_shot_layer_id = layer
        rt.firing_stance_held = True
    if fire_kind in BURST_FIRE_KINDS:
        return
    if fire_kind not in ("single", "shotgun"):
        return
    if weapon is None or not isinstance(weapon, Weapon):
        return
    rt.recoil_ac_owed = float(
        recoil_recovery_ac(int(getattr(weapon, "knock_down", 0) or 0), shooter.gun_combat_skill_level)
    )
    if getattr(weapon, "actions_to_cycle", None) is not None:
        rt.weapon_cycled = False
