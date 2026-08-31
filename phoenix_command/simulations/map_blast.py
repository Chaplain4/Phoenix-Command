"""Map blast centers (Table 5C scatter) and BlastModifier derivation (Table 5B)."""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Any, Iterable

from phoenix_command.item_database.armor import helmet_locs, iotv_front_vital
from phoenix_command.models.character import Character
from phoenix_command.models.enums import BlastModifier
from phoenix_command.models.hit_result_advanced import ExplosiveShotResult
from phoenix_command.session.domains.impulse_combat_state import TokenCombatRuntime
from phoenix_command.session.domains.map_state import (
    MapLayer,
    MapState,
    TerrainTile,
    WallSegment,
    hex_wall_key,
    layer_has_hex_wall,
)
from phoenix_command.session.domains.token_state import TokenPlacement
from phoenix_command.simulations.hex_tactical import AXIAL_NEIGHBORS, neighbor_direction_index
from phoenix_command.simulations.map_los import check_los
from phoenix_command.tables.catalogs.barrier_catalog import resolve_blocks_vision

DEFAULT_ENCLOSURE_RAY_HEXES = 4
ROOM_MIN_BLOCKED_RAYS = 4
TRENCH_DEPRESSION_M = 1.0
COMBAT_SUIT_HEAD_BPF = 3
COMBAT_SUIT_CHEST_BPF = 5
INDOOR_LAYER_KINDS = frozenset({"floor", "basement"})
INDOOR_TERRAIN_TYPES = frozenset({"indoor", "enclosed", "small_room", "interior"})
DEEP_WATER_TERRAIN = frozenset({"water_deep"})


@dataclass
class BlastVictimSpec:
    token_id: str
    range_hex: int
    dist_m: float
    derived_mods: list[BlastModifier]


@dataclass
class BlastPassSpec:
    center_q: int
    center_r: int
    scatter_hexes: int = 0
    is_long: bool = False
    hit: bool = True
    victims: list[BlastVictimSpec] = field(default_factory=list)


@dataclass
class PendingBlastPackage:
    """Blast geometry + auto modifiers, ready for review or apply."""

    passes: list[BlastPassSpec] = field(default_factory=list)


def scatter_blast_hex(
    aim_q: int,
    aim_r: int,
    shooter_q: int,
    shooter_r: int,
    scatter_hexes: int,
    is_long: bool,
    rng: random.Random | None = None,
) -> tuple[int, int]:
    """Offset the intended hex by Table 5C scatter distance."""
    if scatter_hexes <= 0:
        return aim_q, aim_r
    rng = rng or random
    dq = aim_q - shooter_q
    dr = aim_r - shooter_r
    if dq == 0 and dr == 0:
        di, dj = AXIAL_NEIGHBORS[rng.randrange(6)]
        return aim_q + di * scatter_hexes, aim_r + dj * scatter_hexes
    best = max(
        range(6),
        key=lambda i: AXIAL_NEIGHBORS[i][0] * dq + AXIAL_NEIGHBORS[i][1] * dr,
    )
    if is_long:
        di, dj = AXIAL_NEIGHBORS[best]
    else:
        di, dj = AXIAL_NEIGHBORS[(best + 3) % 6]
    return aim_q + di * scatter_hexes, aim_r + dj * scatter_hexes


def blast_centers_from_results(
    aim_q: int,
    aim_r: int,
    shooter_q: int,
    shooter_r: int,
    explosive_results: Iterable[ExplosiveShotResult],
    rng: random.Random | None = None,
) -> list[tuple[int, int]]:
    """One blast center per grenade: aim hex on hit, scatter hex on miss."""
    centers: list[tuple[int, int]] = []
    for expl in explosive_results:
        if expl.hit or expl.scatter_hexes <= 0:
            centers.append((aim_q, aim_r))
        else:
            centers.append(
                scatter_blast_hex(
                    aim_q,
                    aim_r,
                    shooter_q,
                    shooter_r,
                    expl.scatter_hexes,
                    expl.is_long,
                    rng=rng,
                )
            )
    return centers


def concussion_radius_hexes(explosive_ammo: Any | None) -> int:
    """Max rule hexes where base_concussion > 0 (blast-wave footprint)."""
    best = 0
    for d in getattr(explosive_ammo, "explosive_data", None) or []:
        rh = getattr(d, "range_hexes", None)
        bc = getattr(d, "base_concussion", None) or 0
        if rh is not None and bc > 0:
            best = max(best, int(rh))
    return max(1, best) if best > 0 else DEFAULT_ENCLOSURE_RAY_HEXES


def layer_has_ceiling(layer: MapLayer | None) -> bool:
    """Roof present: explicit override, else floor/basement kinds."""
    if layer is None:
        return False
    if layer.has_ceiling is True:
        return True
    if layer.has_ceiling is False:
        return False
    return layer.kind in INDOOR_LAYER_KINDS


def _hex_key(q: int, r: int) -> str:
    return f"{q},{r}"


def _layer_for(map_state: MapState | None, layer_id: str) -> MapLayer | None:
    if not map_state:
        return None
    return map_state.get_layer(layer_id) or map_state.active_layer()


def _custom(map_state: MapState | None) -> dict:
    return map_state.custom_barriers if map_state else {}


def _terrain_type(layer: MapLayer | None, q: int, r: int) -> str:
    if not layer:
        return "open"
    tile = layer.terrain.get(_hex_key(q, r))
    if isinstance(tile, TerrainTile):
        return tile.terrain_type or "open"
    return "open"


def _wall_blocks_vision(wall: WallSegment | None, custom: dict) -> bool:
    if wall is None:
        return False
    return bool(resolve_blocks_vision(wall.material, custom))


def _opaque_wall_on_edge(
    layer: MapLayer | None,
    q: int,
    r: int,
    dir_index: int,
    custom: dict,
) -> bool:
    """True if a vision-blocking wall sits on this hex edge (either side). Openings still count."""
    if layer is None or dir_index is None:
        return False
    wall = layer.walls.get(f"{q},{r}:{dir_index}")
    if _wall_blocks_vision(wall, custom):
        return True
    nq = q + AXIAL_NEIGHBORS[dir_index][0]
    nr = r + AXIAL_NEIGHBORS[dir_index][1]
    opp = (dir_index + 3) % 6
    wall2 = layer.walls.get(f"{nq},{nr}:{opp}")
    if _wall_blocks_vision(wall2, custom):
        return True
    if layer_has_hex_wall(layer, nq, nr):
        if _wall_blocks_vision(layer.walls.get(hex_wall_key(nq, nr)), custom):
            return True
    return False


def count_enclosure_rays(
    map_state: MapState | None,
    tok: TokenPlacement,
    max_hexes: int = DEFAULT_ENCLOSURE_RAY_HEXES,
) -> int:
    """How many of 6 axial rays hit a solid wall within max_hexes."""
    layer = _layer_for(map_state, tok.layer_id)
    custom = _custom(map_state)
    blocked = 0
    for di, dj in AXIAL_NEIGHBORS:
        cq, cr = tok.q, tok.r
        ray_hit = False
        for _ in range(max(1, max_hexes)):
            nq, nr = cq + di, cr + dj
            edge = neighbor_direction_index(cq, cr, nq, nr)
            if edge is not None and _opaque_wall_on_edge(layer, cq, cr, edge, custom):
                ray_hit = True
                break
            cq, cr = nq, nr
        if ray_hit:
            blocked += 1
    return blocked


def _floor_mark(layer: MapLayer | None) -> float:
    if layer is None:
        return 0.0
    return float(layer.elevation)


def surrounding_lip_m(map_state: MapState | None, tok: TokenPlacement) -> float:
    """Highest neighboring floor / berm relative to map elevation units."""
    layer = _layer_for(map_state, tok.layer_id)
    floor = _floor_mark(layer)
    best = floor
    if layer is None:
        return best
    for nq, nr, _di in (
        (tok.q + dq, tok.r + dr, i) for i, (dq, dr) in enumerate(AXIAL_NEIGHBORS)
    ):
        obs = layer.obstacles.get(_hex_key(nq, nr))
        if obs is not None:
            best = max(best, floor + float(obs.height))
        if layer_has_hex_wall(layer, nq, nr):
            wall = layer.walls.get(hex_wall_key(nq, nr))
            if wall is not None:
                best = max(best, floor + float(wall.height))
    return best


def _is_deep_water(layer: MapLayer | None, q: int, r: int) -> bool:
    t = _terrain_type(layer, q, r).lower()
    if t in DEEP_WATER_TERRAIN:
        return True
    return "water" in t and "deep" in t


def _is_indoor_tag(layer: MapLayer | None, q: int, r: int) -> bool:
    """Referee indoor tag (implies roofed interior even without walls)."""
    if layer is None:
        return False
    if not layer_has_ceiling(layer):
        return False
    if layer.kind in INDOOR_LAYER_KINDS:
        return True
    t = _terrain_type(layer, q, r).lower()
    return t in INDOOR_TERRAIN_TYPES


def _min_front_bpf(character: Character | None, locations) -> float:
    if character is None:
        return 0.0
    prot = character.armor_protection
    vals: list[float] = []
    for loc in locations:
        _pf, bpf = prot.get((loc, True), (0, 0))
        vals.append(float(bpf))
    return min(vals) if vals else 0.0


def has_combat_suit_protection(character: Character | None) -> bool:
    if character is None:
        return False
    head = _min_front_bpf(character, helmet_locs)
    chest = _min_front_bpf(character, iotv_front_vital)
    return head >= COMBAT_SUIT_HEAD_BPF and chest >= COMBAT_SUIT_CHEST_BPF


def _pick_environment(
    map_state: MapState | None,
    victim_tok: TokenPlacement,
    enclosure_max_hexes: int = DEFAULT_ENCLOSURE_RAY_HEXES,
) -> BlastModifier:
    layer = _layer_for(map_state, victim_tok.layer_id)
    if _is_deep_water(layer, victim_tok.q, victim_tok.r):
        return BlastModifier.UNDERWATER

    rays = count_enclosure_rays(map_state, victim_tok, max_hexes=enclosure_max_hexes)
    enclosed = rays >= ROOM_MIN_BLOCKED_RAYS
    ceiling = layer_has_ceiling(layer)
    indoor = _is_indoor_tag(layer, victim_tok.q, victim_tok.r)
    floor = _floor_mark(layer)
    lip = surrounding_lip_m(map_state, victim_tok)
    depression = (lip - floor) >= TRENCH_DEPRESSION_M
    explicit_trench = bool(layer and layer.kind == "trench")

    # Roofed room: referee indoor tag, or enclosed with ceiling
    if indoor or (enclosed and ceiling):
        return BlastModifier.IN_SMALL_ROOM
    # Open-top enclosure (pool/pit) or foxhole / painted trench
    if enclosed or explicit_trench or depression:
        return BlastModifier.IN_OPEN_TRENCH
    return BlastModifier.IN_THE_OPEN


def _cover_from_blast(
    map_state: MapState | None,
    blast_q: int,
    blast_r: int,
    victim_tok: TokenPlacement,
    victim_rt: TokenCombatRuntime | None,
) -> list[BlastModifier]:
    if map_state is None:
        return []
    blast_tok = TokenPlacement(
        token_id="_blast",
        q=blast_q,
        r=blast_r,
        layer_id=victim_tok.layer_id,
        character_name="",
    )
    if blast_q == victim_tok.q and blast_r == victim_tok.r:
        return []
    los = check_los(map_state, blast_tok, victim_tok, victim_rt)
    if los.blocked:
        return [BlastModifier.BEHIND_SOLID_COVER]
    cover = los.cover
    if cover is None:
        return []
    if cover.through_cover or cover.estimated_cover_pf > 0:
        if not cover.clear_silhouette:
            return [BlastModifier.UNDER_PARTIAL_COVER]
        if cover.estimated_cover_pf >= 1.0:
            return [BlastModifier.UNDER_PARTIAL_COVER]
    return []


def derive_blast_modifiers(
    map_state: MapState | None,
    blast_q: int,
    blast_r: int,
    victim_tok: TokenPlacement,
    victim_char: Character | None = None,
    token_rt: TokenCombatRuntime | None = None,
    enclosure_max_hexes: int | None = None,
    explosive_ammo: Any | None = None,
) -> list[BlastModifier]:
    """One Table 5B environment row plus stacked posture/protection."""
    if enclosure_max_hexes is None:
        enclosure_max_hexes = (
            concussion_radius_hexes(explosive_ammo)
            if explosive_ammo is not None
            else DEFAULT_ENCLOSURE_RAY_HEXES
        )
    env = _pick_environment(map_state, victim_tok, enclosure_max_hexes=enclosure_max_hexes)
    mods: list[BlastModifier] = [env]
    rt = token_rt or TokenCombatRuntime()
    if rt.stance == "prone":
        mods.append(BlastModifier.PRONE)
    if has_combat_suit_protection(victim_char):
        mods.append(BlastModifier.IN_COMBAT_SUIT)
    mods.extend(_cover_from_blast(map_state, blast_q, blast_r, victim_tok, rt))
    return mods
