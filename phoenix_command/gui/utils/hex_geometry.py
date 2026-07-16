"""Hex grid geometry utilities."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING, Iterator

if TYPE_CHECKING:
    from phoenix_command.session.domains.map_state import HexGridConfig


def _sqrt3() -> float:
    return math.sqrt(3.0)


def offset_to_axial(col: int, row: int, grid: "HexGridConfig") -> tuple[int, int]:
    """Convert offset (col, row) to axial (q, r)."""
    if grid.orientation == "flat":
        # odd-q vertical layout
        q = col
        r = row - (col + (col & 1)) // 2
    else:
        # odd-r horizontal layout
        q = col - (row + (row & 1)) // 2
        r = row
    return q, r


def axial_to_offset(q: int, r: int, grid: "HexGridConfig") -> tuple[int, int]:
    """Convert axial (q, r) to offset (col, row)."""
    if grid.orientation == "flat":
        col = q
        row = r + (q + (q & 1)) // 2
    else:
        col = q + (r + (r & 1)) // 2
        row = r
    return col, row


def is_in_bounds(q: int, r: int, grid: "HexGridConfig") -> bool:
    """Return True if axial hex is inside the rectangular map."""
    col, row = axial_to_offset(q, r, grid)
    return 0 <= col < grid.cols and 0 <= row < grid.rows


def iter_rect_cells(grid: "HexGridConfig") -> Iterator[tuple[int, int]]:
    """Iterate all axial (q, r) cells in the rectangular map."""
    for col in range(grid.cols):
        for row in range(grid.rows):
            yield offset_to_axial(col, row, grid)


def iter_offset_rect(
    col0: int, row0: int, col1: int, row1: int, grid: "HexGridConfig"
) -> Iterator[tuple[int, int]]:
    """Iterate axial cells in an offset-coordinate rectangle (inclusive)."""
    c_min, c_max = min(col0, col1), max(col0, col1)
    r_min, r_max = min(row0, row1), max(row0, row1)
    for col in range(c_min, c_max + 1):
        for row in range(r_min, r_max + 1):
            if 0 <= col < grid.cols and 0 <= row < grid.rows:
                yield offset_to_axial(col, row, grid)


def rect_bounds_pixels(grid: "HexGridConfig") -> tuple[float, float, float, float]:
    """Return (min_x, min_y, max_x, max_y) bounding box of the map in pixels."""
    min_x = min_y = float("inf")
    max_x = max_y = float("-inf")
    for q, r in iter_rect_cells(grid):
        for x, y in hex_corners(q, r, grid):
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x)
            max_y = max(max_y, y)
    if min_x == float("inf"):
        return 0.0, 0.0, 100.0, 100.0
    return min_x, min_y, max_x, max_y


def axial_to_pixel(q: int, r: int, grid: "HexGridConfig") -> tuple[float, float]:
    """Convert axial hex coordinates to pixel center."""
    size = grid.size
    if grid.orientation == "flat":
        x = size * (3.0 / 2.0 * q)
        y = size * (_sqrt3() / 2.0 * q + _sqrt3() * r)
    else:
        x = size * (_sqrt3() * q + _sqrt3() / 2.0 * r)
        y = size * (3.0 / 2.0 * r)
    return grid.origin_x + x, grid.origin_y + y


def pixel_to_axial(x: float, y: float, grid: "HexGridConfig") -> tuple[int, int]:
    """Convert pixel coordinates to axial hex coordinates."""
    x -= grid.origin_x
    y -= grid.origin_y
    size = grid.size
    if grid.orientation == "flat":
        q = (2.0 / 3.0 * x) / size
        r = (-1.0 / 3.0 * x + _sqrt3() / 3.0 * y) / size
    else:
        q = (_sqrt3() / 3.0 * x - 1.0 / 3.0 * y) / size
        r = (2.0 / 3.0 * y) / size
    return _axial_round(q, r)


def pixel_to_offset(x: float, y: float, grid: "HexGridConfig") -> tuple[int, int]:
    """Convert pixel coordinates to offset (col, row)."""
    q, r = pixel_to_axial(x, y, grid)
    return axial_to_offset(q, r, grid)


def _axial_round(q: float, r: float) -> tuple[int, int]:
    s = -q - r
    rq = round(q)
    rr = round(r)
    rs = round(s)
    dq = abs(rq - q)
    dr = abs(rr - r)
    ds = abs(rs - s)
    if dq > dr and dq > ds:
        rq = -rr - rs
    elif dr > ds:
        rr = -rq - rs
    return int(rq), int(rr)


def hex_corners(q: int, r: int, grid: "HexGridConfig") -> list[tuple[float, float]]:
    """Return six corner points of a hex."""
    cx, cy = axial_to_pixel(q, r, grid)
    size = grid.size
    corners = []
    start_angle = 0.0 if grid.orientation == "flat" else math.pi / 6.0
    for i in range(6):
        angle = start_angle + math.pi / 3.0 * i
        corners.append((cx + size * math.cos(angle), cy + size * math.sin(angle)))
    return corners


def edge_endpoints(
    q: int, r: int, edge: int, grid: "HexGridConfig"
) -> tuple[tuple[float, float], tuple[float, float]]:
    """Return start and end pixel points for a hex edge (0..5)."""
    corners = hex_corners(q, r, grid)
    edge = edge % 6
    return corners[edge], corners[(edge + 1) % 6]


def edge_midpoint(
    q: int, r: int, edge: int, grid: "HexGridConfig"
) -> tuple[float, float]:
    """Return midpoint of a hex edge."""
    start, end = edge_endpoints(q, r, edge, grid)
    return (start[0] + end[0]) / 2.0, (start[1] + end[1]) / 2.0


def point_on_edge(
    q: int, r: int, edge: int, t: float, grid: "HexGridConfig"
) -> tuple[float, float]:
    """Return point at fraction t (0..1) along a hex edge."""
    start, end = edge_endpoints(q, r, edge, grid)
    return start[0] + t * (end[0] - start[0]), start[1] + t * (end[1] - start[1])


def nearest_edge(
    x: float, y: float, q: int, r: int, grid: "HexGridConfig"
) -> int:
    """Find nearest edge index to a pixel point on hex (q,r)."""
    best_edge = 0
    best_dist = float("inf")
    for edge in range(6):
        mid = edge_midpoint(q, r, edge, grid)
        dist = (mid[0] - x) ** 2 + (mid[1] - y) ** 2
        if dist < best_dist:
            best_dist = dist
            best_edge = edge
    return best_edge


def axial_distance(q1: int, r1: int, q2: int, r2: int) -> int:
    """Hex distance in axial coordinates."""
    dq = q1 - q2
    dr = r1 - r2
    ds = -dq - dr
    return (abs(dq) + abs(dr) + abs(ds)) // 2


def facing_to_degrees(facing: int, orientation: str) -> float:
    """Convert hex facing (0-11) to rotation degrees; 30° per step."""
    del orientation  # same screen angles; hex grid orientation affects labels only
    # Token artwork / facing arrow is drawn pointing up by default, while
    # facing index 0 is treated as east on the map. Offset by +90° so
    # compass labels line up with the rendered direction on screen.
    return float((((facing % 12) * 30) + 90) % 360)


def facing_labels(orientation: str) -> list[tuple[str, int]]:
    """Human-readable labels for facing 0-11.

    Flat-top: even indices are corners, odd are side midpoints.
    Pointy-top: even indices are side midpoints, odd are corners.
    Side labels use short compass names (N, SE, …).
    """
    if orientation == "flat":
        return [
            ("Corner E", 0),
            ("SE", 1),
            ("Corner SE", 2),
            ("S", 3),
            ("Corner SW", 4),
            ("SW", 5),
            ("Corner W", 6),
            ("NW", 7),
            ("Corner NW", 8),
            ("N", 9),
            ("Corner NE", 10),
            ("NE", 11),
        ]
    return [
        ("E", 0),
        ("Corner NE", 1),
        ("SE", 2),
        ("Corner S", 3),
        ("SW", 4),
        ("Corner SW", 5),
        ("W", 6),
        ("Corner NW", 7),
        ("NW", 8),
        ("Corner N", 9),
        ("NE", 10),
        ("Corner NW", 11),
    ]


def background_target_rect(grid: "HexGridConfig") -> tuple[float, float, float, float]:
    """Return (x, y, width, height) bounding box of the map grid in pixels."""
    min_x, min_y, max_x, max_y = rect_bounds_pixels(grid)
    return min_x, min_y, max_x - min_x, max_y - min_y


def compute_background_layout(
    fit_mode: str,
    native_w: int,
    native_h: int,
    grid: "HexGridConfig",
    scale_x: float = 1.0,
    scale_y: float = 1.0,
    offset_x: float = 0.0,
    offset_y: float = 0.0,
) -> tuple[float, float, float, float]:
    """Return (dest_w, dest_h, pos_x, pos_y) for background placement."""
    bx, by, bw, bh = background_target_rect(grid)
    if native_w <= 0 or native_h <= 0:
        return 0.0, 0.0, bx, by

    if fit_mode == "stretch_grid":
        return bw, bh, bx, by

    if fit_mode == "fit_grid":
        scale = min(bw / native_w, bh / native_h)
        dest_w = native_w * scale
        dest_h = native_h * scale
        pos_x = bx + (bw - dest_w) / 2.0
        pos_y = by + (bh - dest_h) / 2.0
        return dest_w, dest_h, pos_x, pos_y

    # manual
    dest_w = native_w * scale_x
    dest_h = native_h * scale_y
    return dest_w, dest_h, offset_x, offset_y
