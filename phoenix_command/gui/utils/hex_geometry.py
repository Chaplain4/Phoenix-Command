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
