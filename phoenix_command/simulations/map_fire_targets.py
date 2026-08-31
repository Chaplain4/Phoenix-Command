"""Suggest map tokens for multi-target fire (arc, shotgun pattern, blast)."""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from phoenix_command.gui.utils.hex_geometry import axial_distance
from phoenix_command.session.domains.impulse_combat_state import TokenCombatRuntime
from phoenix_command.session.domains.map_state import MapState, rules_hexes
from phoenix_command.session.domains.token_state import TokenPlacement, TokenState
from phoenix_command.simulations.hex_tactical import facing_to_radians
from phoenix_command.simulations.map_shot_context import build_map_shot_context


@dataclass
class FireTargetInfo:
    """One candidate target derived from map geometry."""

    token_id: str
    range_rule_hexes: int
    orientation: str
    orientation_key: str
    exposure: str
    visible_exposures: list[str] = field(default_factory=list)
    is_front: bool = True
    los_clear: bool = True
    notes: list[str] = field(default_factory=list)


def _angle_diff(a: float, b: float) -> float:
    d = abs(a - b) % (2 * math.pi)
    return min(d, 2 * math.pi - d)


def _hex_bearing(q0: int, r0: int, q1: int, r1: int) -> float:
    dq = q1 - q0
    dr = r1 - r0
    return math.atan2(dr * math.sqrt(3) / 2, dq * 1.5 + dr * 0.75)


def _meters_per_hex(map_state: MapState | None) -> float:
    if map_state:
        return map_state.grid.meters_per_hex
    return 1.0


def _enemy_tokens(
    shooter: TokenPlacement,
    tokens: TokenState,
    exclude_ids: set[str] | None = None,
) -> list[TokenPlacement]:
    exclude = exclude_ids or set()
    result = []
    for tid, tok in tokens.placements.items():
        if tid in exclude or tid == shooter.token_id:
            continue
        if not tok.character_name:
            continue
        if shooter.side_id and tok.side_id == shooter.side_id:
            continue
        result.append(tok)
    return result


def tokens_in_arc(
    shooter: TokenPlacement,
    tokens: TokenState,
    map_state: MapState | None,
    token_runtime: dict[str, TokenCombatRuntime] | None = None,
    max_range_hexes: float = 50.0,
    half_angle_deg: float = 30.0,
    same_layer_only: bool = False,
    ammo=None,
) -> list[FireTargetInfo]:
    """
    Enemy tokens roughly in the shooter's facing cone.

    half_angle_deg is half the cone width from facing centerline.
    """
    runtime = token_runtime or {}
    facing_angle = facing_to_radians(shooter.facing)
    half = math.radians(half_angle_deg)
    mph = _meters_per_hex(map_state)
    out: list[FireTargetInfo] = []

    for tok in _enemy_tokens(shooter, tokens):
        if same_layer_only and tok.layer_id and shooter.layer_id and tok.layer_id != shooter.layer_id:
            continue
        dist_m = axial_distance(shooter.q, shooter.r, tok.q, tok.r) * mph
        range_hex = max(1, round(rules_hexes(dist_m)))
        if range_hex > max_range_hexes:
            continue
        if axial_distance(shooter.q, shooter.r, tok.q, tok.r) == 0:
            bearing_ok = True
        else:
            bearing = _hex_bearing(shooter.q, shooter.r, tok.q, tok.r)
            bearing_ok = _angle_diff(bearing, facing_angle) <= half
        if not bearing_ok:
            continue

        shooter_rt = runtime.get(shooter.token_id, TokenCombatRuntime())
        target_rt = runtime.get(tok.token_id, TokenCombatRuntime())
        pen: float | None = None
        if ammo is not None and hasattr(ammo, "get_pen"):
            pen = float(ammo.get_pen(range_hex))
        ctx = build_map_shot_context(
            shooter, shooter_rt, tok, target_rt, map_state, pen=pen
        )
        los = ctx.los
        out.append(
            FireTargetInfo(
                token_id=tok.token_id,
                range_rule_hexes=ctx.range_rule_hexes,
                orientation=ctx.shot_params.target_orientation.name,
                orientation_key=ctx.orientation_key,
                exposure=ctx.target_exposure.name,
                visible_exposures=[e.name for e in ctx.visible_exposures],
                is_front=ctx.is_front_shot,
                los_clear=bool(los and los.clear and not los.blocked),
                notes=list(ctx.visibility_notes),
            )
        )
    out.sort(key=lambda t: t.range_rule_hexes)
    return out


def tokens_in_pattern(
    center_q: int,
    center_r: int,
    radius_m: float,
    tokens: TokenState,
    map_state: MapState | None,
    shooter: TokenPlacement | None = None,
    exclude_ids: set[str] | None = None,
    layer_id: str = "",
) -> list[str]:
    """Token ids within pattern radius (meters) of a hex center."""
    mph = _meters_per_hex(map_state)
    exclude = set(exclude_ids or set())
    if shooter:
        exclude.add(shooter.token_id)
    ids: list[str] = []
    for tid, tok in tokens.placements.items():
        if tid in exclude or not tok.character_name:
            continue
        if shooter and shooter.side_id and tok.side_id == shooter.side_id:
            continue
        if layer_id and tok.layer_id and tok.layer_id != layer_id:
            continue
        dist_m = axial_distance(center_q, center_r, tok.q, tok.r) * mph
        if dist_m <= radius_m + 1e-6:
            ids.append(tid)
    return ids


def tokens_in_blast(
    center_q: int,
    center_r: int,
    max_range_m: float,
    tokens: TokenState,
    map_state: MapState | None,
    shooter: TokenPlacement | None = None,
    layer_id: str = "",
) -> list[tuple[str, float]]:
    """(token_id, distance_m) within blast radius."""
    mph = _meters_per_hex(map_state)
    result: list[tuple[str, float]] = []
    for tid, tok in tokens.placements.items():
        if shooter and tid == shooter.token_id:
            continue
        if not tok.character_name:
            continue
        if layer_id and tok.layer_id and tok.layer_id != layer_id:
            continue
        dist_m = axial_distance(center_q, center_r, tok.q, tok.r) * mph
        if dist_m <= max_range_m + 1e-6:
            result.append((tid, dist_m))
    result.sort(key=lambda x: x[1])
    return result


def is_pellet_ammo(ammo) -> bool:
    if ammo is None:
        return False
    if getattr(ammo, "pellet_count", None):
        return True
    for bd in getattr(ammo, "ballistic_data", None) or []:
        if getattr(bd, "shotgun_accuracy_level_modifier", None) is not None:
            return True
        if getattr(bd, "pattern_radius", None) is not None:
            return True
        if getattr(bd, "base_pellet_hit_chance", None) is not None:
            return True
    return False


def default_ammo_for_weapon(weapon, fire_mode: str = "single"):
    """Pick ammo for map preview; prefer pellets for shotgun weapons and auto."""
    from phoenix_command.models.enums import WeaponType
    from phoenix_command.models.gear import AmmoType

    types = getattr(weapon, "ammunition_types", None) or []
    is_shotgun = getattr(weapon, "weapon_type", None) == WeaponType.SHOTGUN
    if fire_mode == "auto" or is_shotgun:
        for raw in types:
            if isinstance(raw, AmmoType) and is_pellet_ammo(raw):
                return raw
    for raw in types:
        if isinstance(raw, AmmoType):
            return raw
    return types[0] if types else None


def suggest_arc_hexes(max_range: int = 10) -> float:
    """Default arc of fire in rule hexes for UI when auto."""
    return float(max(1, max_range // 5))


def infer_fire_kind(fire_mode: str, weapon, ammo) -> str:
    """Map weapon/ammo/mode to dispatcher kind."""
    from phoenix_command.models.enums import WeaponType
    from phoenix_command.models.gear import Grenade

    if isinstance(weapon, Grenade) or (
        ammo is not None and getattr(ammo, "explosive_data", None)
    ):
        if weapon and getattr(weapon, "weapon_type", None) == WeaponType.AUTOMATIC_GRENADE_LAUNCHER:
            return "agl"
        if fire_mode == "auto":
            return "agl"
        return "grenade"
    if weapon and getattr(weapon, "weapon_type", None) == WeaponType.AUTOMATIC_GRENADE_LAUNCHER:
        return "agl"
    if is_pellet_ammo(ammo):
        return "shotgun_burst" if fire_mode == "auto" else "shotgun"
    if fire_mode == "auto":
        return "burst"
    if fire_mode == "3rb":
        return "3rb"
    return "single"


def build_per_target_entry(info: FireTargetInfo) -> dict:
    return {
        "range_hexes": info.range_rule_hexes,
        "exposure": info.exposure,
        "orientation": info.orientation,
        "orientation_key": info.orientation_key,
        "is_front": info.is_front,
        "visible_exposures": list(info.visible_exposures),
        "los_clear": info.los_clear,
        "notes": list(info.notes),
    }
