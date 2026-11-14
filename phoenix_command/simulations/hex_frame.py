"""Canonical hex edge / facing frame shared by GUI and combat engine.

Edge index k matches ``hex_geometry.hex_corners`` / ``nearest_edge``:
screen Y-down, corners clockwise, edge k = corners[k]→corners[k+1].
Neighbor beyond edge k is ``EDGE_NEIGHBORS[orientation][k]``.
"""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from phoenix_command.session.domains.map_state import HexGridConfig, MapLayer, WallSegment

# Screen-CW neighbor deltas (GUI / editor convention).
EDGE_NEIGHBORS: dict[str, tuple[tuple[int, int], ...]] = {
    # SE, S, SW, NW, N, NE
    "flat": ((1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)),
    # SE, SW, W, NW, NE, E
    "pointy": ((0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1), (1, 0)),
}

# Pre-fix engine order (math Y-up): E, NE, NW, W, SW, SE — for migration only.
LEGACY_ENGINE_NEIGHBORS: tuple[tuple[int, int], ...] = (
    (1, 0),
    (1, -1),
    (0, -1),
    (-1, 0),
    (-1, 1),
    (0, 1),
)

EDGE_CONVENTION_SCREEN_CW = "screen_cw_v1"


def edge_neighbors(orientation: str = "flat") -> tuple[tuple[int, int], ...]:
    return EDGE_NEIGHBORS.get(orientation, EDGE_NEIGHBORS["flat"])


def axial_neighbors(
    q: int, r: int, orientation: str = "flat"
) -> list[tuple[int, int, int]]:
    """Return list of (nq, nr, edge_index 0..5)."""
    return [(q + dq, r + dr, i) for i, (dq, dr) in enumerate(edge_neighbors(orientation))]


def edge_toward(
    q0: int, r0: int, q1: int, r1: int, orientation: str = "flat"
) -> int | None:
    """Edge index from (q0,r0) toward adjacent (q1,r1), or None if not adjacent."""
    dq, dr = q1 - q0, r1 - r0
    for i, (ndq, ndr) in enumerate(edge_neighbors(orientation)):
        if dq == ndq and dr == ndr:
            return i
    return None


# Alias used throughout simulations
neighbor_direction_index = edge_toward


def facing_for_edge(edge: int, orientation: str = "flat") -> int:
    """Facing (0..11) of the outward normal of edge k (side midpoint)."""
    k = int(edge) % 6
    if orientation == "pointy":
        return (2 * k + 2) % 12
    return (2 * k + 1) % 12


def direction_index_to_facing(dir_index: int, orientation: str = "flat") -> int:
    return facing_for_edge(dir_index, orientation)


def facing_to_radians(facing: int) -> float:
    """Facing 0-11 to radians; 0 = east on screen (Y down)."""
    return math.radians((facing % 12) * 30)


def shortest_facing_delta(from_facing: int, to_facing: int) -> int:
    """Signed shortest turn in facing steps (−6..+6). Positive = clockwise."""
    delta = (int(to_facing) - int(from_facing)) % 12
    if delta > 6:
        delta -= 12
    return delta


def apply_free_facing(current_facing: int, desired_facing: int, free_steps: int = 2) -> int:
    """Apply up to free_steps toward desired facing (book: ≤60° free per hex)."""
    delta = shortest_facing_delta(current_facing, desired_facing)
    if delta == 0:
        return int(current_facing) % 12
    step = max(-free_steps, min(free_steps, delta))
    return (int(current_facing) + step) % 12


def classify_movement_base(
    facing: int, dir_index: int, orientation: str = "flat"
) -> str:
    """
    Classify movement relative to token facing into Table 7A base id.

    Uses angle between facing and edge outward normal (30° steps).
    """
    desired = facing_for_edge(dir_index, orientation)
    d = abs(shortest_facing_delta(facing, desired))
    if d <= 1:
        return "forward"
    if d >= 5:
        return "backward"
    if d == 2:
        return "oblique"
    return "sideways"


def _cube_round(fq: float, fr: float) -> tuple[int, int]:
    fs = -fq - fr
    rq = round(fq)
    rr = round(fr)
    rs = round(fs)
    dq = abs(rq - fq)
    dr = abs(rr - fr)
    ds = abs(rs - fs)
    if dq > dr and dq > ds:
        rq = -rr - rs
    elif dr > ds:
        rr = -rq - rs
    return int(rq), int(rr)


def line_hexes(q0: int, r0: int, q1: int, r1: int) -> list[tuple[int, int]]:
    """Cube-lerp line of hexes (epsilon nudge avoids vertex ambiguity)."""
    dq = q1 - q0
    dr = r1 - r0
    dist = max(abs(dq), abs(dr), abs(dq + dr))
    if dist == 0:
        return [(q0, r0)]
    # Nudge so vertex hits resolve consistently toward +q/+r
    nq0 = q0 + 1e-6
    nr0 = r0 + 1e-6
    nq1 = q1 + 1e-6
    nr1 = r1 + 1e-6
    results: list[tuple[int, int]] = []
    for i in range(dist + 1):
        t = i / dist
        q = nq0 + (nq1 - nq0) * t
        r = nr0 + (nr1 - nr0) * t
        hq, hr = _cube_round(q, r)
        if not results or results[-1] != (hq, hr):
            results.append((hq, hr))
    return results


def bearing(
    q0: int,
    r0: int,
    q1: int,
    r1: int,
    grid: "HexGridConfig | None" = None,
) -> float:
    """Screen bearing from hex center to hex center (atan2, Y down)."""
    from phoenix_command.gui.utils.hex_geometry import axial_to_pixel
    from phoenix_command.session.domains.map_state import HexGridConfig

    g = grid or HexGridConfig()
    x0, y0 = axial_to_pixel(q0, r0, g)
    x1, y1 = axial_to_pixel(q1, r1, g)
    return math.atan2(y1 - y0, x1 - x0)


def _normalize_angle(radians: float) -> float:
    while radians > math.pi:
        radians -= 2 * math.pi
    while radians <= -math.pi:
        radians += 2 * math.pi
    return radians


def relative_orientation(
    target_facing: int,
    target_q: int,
    target_r: int,
    shooter_q: int,
    shooter_r: int,
    grid: "HexGridConfig | None" = None,
) -> str:
    """
    Target orientation relative to incoming shot direction.

    Returns one of: front, rear, oblique, left_side, right_side.
    """
    if target_q == shooter_q and target_r == shooter_r:
        return "front"
    shot_angle = bearing(target_q, target_r, shooter_q, shooter_r, grid)
    facing_angle = facing_to_radians(target_facing)
    rel = _normalize_angle(shot_angle - facing_angle)
    abs_rel = abs(rel)
    if abs_rel <= math.pi / 4:
        return "front"
    if abs_rel >= 3 * math.pi / 4:
        return "rear"
    if abs(abs_rel - math.pi / 2) <= math.pi / 8:
        return "left_side" if rel > 0 else "right_side"
    return "oblique"


def edge_key(q: int, r: int, edge: int) -> str:
    return f"{q},{r}:{int(edge) % 6}"


def opposite_edge(edge: int) -> int:
    return (int(edge) + 3) % 6


def neighbor_hex(
    q: int, r: int, edge: int, orientation: str = "flat"
) -> tuple[int, int]:
    dq, dr = edge_neighbors(orientation)[int(edge) % 6]
    return q + dq, r + dr


def canonical_edge_key(
    q: int, r: int, edge: int, orientation: str = "flat"
) -> str:
    """Stable key for a physical edge: prefer the hex with smaller (q,r), else edge≤2."""
    e = int(edge) % 6
    nq, nr = neighbor_hex(q, r, e, orientation)
    if (q, r) < (nq, nr):
        return edge_key(q, r, e)
    if (nq, nr) < (q, r):
        return edge_key(nq, nr, opposite_edge(e))
    # Should not happen for distinct hexes
    return edge_key(q, r, min(e, opposite_edge(e)))


def wall_on_edge(
    layer: "MapLayer | None",
    q: int,
    r: int,
    edge: int,
    orientation: str = "flat",
) -> tuple[str, "WallSegment"] | None:
    """Return (wall_key, wall) for this physical edge, checking both sides."""
    if layer is None:
        return None
    e = int(edge) % 6
    key = edge_key(q, r, e)
    wall = layer.walls.get(key)
    if wall is not None:
        return key, wall
    nq, nr = neighbor_hex(q, r, e, orientation)
    key2 = edge_key(nq, nr, opposite_edge(e))
    wall2 = layer.walls.get(key2)
    if wall2 is not None:
        return key2, wall2
    return None


def engine_edge_to_gui(engine_k: int, orientation: str = "flat") -> int:
    """Map legacy engine AXIAL_NEIGHBORS index to GUI edge index."""
    legacy = LEGACY_ENGINE_NEIGHBORS[int(engine_k) % 6]
    for i, d in enumerate(edge_neighbors(orientation)):
        if d == legacy:
            return i
    return int(engine_k) % 6


def gui_edge_to_engine(gui_k: int, orientation: str = "flat") -> int:
    """Inverse of engine_edge_to_gui."""
    gui = edge_neighbors(orientation)[int(gui_k) % 6]
    for i, d in enumerate(LEGACY_ENGINE_NEIGHBORS):
        if d == gui:
            return i
    return int(gui_k) % 6


def migrate_wall_keys_engine_to_gui(
    walls: dict, orientation: str = "flat"
) -> dict:
    """Rewrite edge wall keys from legacy engine numbering to GUI numbering."""
    from phoenix_command.session.domains.map_state import HEX_WALL_EDGE

    out: dict = {}
    for key, wall in walls.items():
        if not isinstance(key, str) or ":" not in key:
            out[key] = wall
            continue
        coords, edge_s = key.rsplit(":", 1)
        if edge_s == HEX_WALL_EDGE:
            out[key] = wall
            continue
        try:
            q_s, r_s = coords.split(",")
            q, r, e = int(q_s), int(r_s), int(edge_s)
        except ValueError:
            out[key] = wall
            continue
        gui_e = engine_edge_to_gui(e, orientation)
        new_key = edge_key(q, r, gui_e)
        # Prefer keeping richer wall if both map to same key
        if new_key in out:
            existing = out[new_key]
            if hasattr(wall, "openings") and wall.openings and not existing.openings:
                out[new_key] = wall
        else:
            out[new_key] = wall
    return out


def _parse_edge_wall_key(key: str) -> tuple[int, int, int] | None:
    from phoenix_command.session.domains.map_state import HEX_WALL_EDGE

    if not isinstance(key, str) or ":" not in key:
        return None
    coords, edge_s = key.rsplit(":", 1)
    if edge_s == HEX_WALL_EDGE:
        return None
    try:
        q_s, r_s = coords.split(",")
        return int(q_s), int(r_s), int(edge_s)
    except ValueError:
        return None


def looks_like_engine_edge_keys(
    walls: dict, orientation: str = "flat"
) -> bool:
    """True if edge keys look paired in legacy engine numbering (scripted maps)."""
    edge_keys = [k for k in walls if _parse_edge_wall_key(k) is not None]
    if len(edge_keys) < 2:
        return False
    engine_pairs = 0
    gui_pairs = 0
    key_set = set(edge_keys)
    for key in edge_keys:
        parsed = _parse_edge_wall_key(key)
        if parsed is None:
            continue
        q, r, e = parsed
        opp = opposite_edge(e)
        ldq, ldr = LEGACY_ENGINE_NEIGHBORS[e % 6]
        if edge_key(q + ldq, r + ldr, opp) in key_set:
            engine_pairs += 1
        gdq, gdr = edge_neighbors(orientation)[e % 6]
        if edge_key(q + gdq, r + gdr, opp) in key_set:
            gui_pairs += 1
    # Dual-written scripted maps: opposite sides stored with engine deltas.
    threshold = max(2, int(0.5 * len(edge_keys)))
    return engine_pairs >= threshold and engine_pairs > gui_pairs


def normalize_wall_material(material: str) -> str:
    if material == "cinder_block":
        return "wall_cinder_block"
    return material
