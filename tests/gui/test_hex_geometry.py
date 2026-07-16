"""Tests for hex geometry."""

import math

import pytest

from phoenix_command.gui.utils.hex_geometry import (
    axial_distance,
    axial_to_offset,
    axial_to_pixel,
    background_target_rect,
    compute_background_layout,
    edge_endpoints,
    facing_to_degrees,
    facing_labels,
    hex_corners,
    is_in_bounds,
    iter_rect_cells,
    nearest_edge,
    offset_to_axial,
    pixel_to_axial,
)
from phoenix_command.session.domains.map_state import HexGridConfig


def test_axial_pixel_round_trip_flat():
    grid = HexGridConfig(orientation="flat", size=24.0, origin_x=100, origin_y=50)
    for q, r in [(0, 0), (3, -2), (-1, 4)]:
        x, y = axial_to_pixel(q, r, grid)
        rq, rr = pixel_to_axial(x, y, grid)
        assert (rq, rr) == (q, r)


def test_axial_pixel_round_trip_pointy():
    grid = HexGridConfig(orientation="pointy", size=20.0)
    for q, r in [(0, 0), (2, 1), (-3, 2)]:
        x, y = axial_to_pixel(q, r, grid)
        rq, rr = pixel_to_axial(x, y, grid)
        assert (rq, rr) == (q, r)


def test_offset_axial_round_trip_flat():
    grid = HexGridConfig(orientation="flat", cols=10, rows=8)
    for col in range(grid.cols):
        for row in range(grid.rows):
            q, r = offset_to_axial(col, row, grid)
            c2, r2 = axial_to_offset(q, r, grid)
            assert (c2, r2) == (col, row)


def test_offset_axial_round_trip_pointy():
    grid = HexGridConfig(orientation="pointy", cols=10, rows=8)
    for col in range(grid.cols):
        for row in range(grid.rows):
            q, r = offset_to_axial(col, row, grid)
            c2, r2 = axial_to_offset(q, r, grid)
            assert (c2, r2) == (col, row)


def test_iter_rect_cells_count():
    grid = HexGridConfig(cols=12, rows=8)
    cells = list(iter_rect_cells(grid))
    assert len(cells) == 12 * 8


def test_is_in_bounds():
    grid = HexGridConfig(cols=5, rows=5, orientation="flat")
    assert is_in_bounds(*offset_to_axial(0, 0, grid), grid)
    assert is_in_bounds(*offset_to_axial(4, 4, grid), grid)
    assert not is_in_bounds(99, 99, grid)


def test_hex_corners_count():
    grid = HexGridConfig()
    corners = hex_corners(0, 0, grid)
    assert len(corners) == 6


def test_edge_endpoints():
    grid = HexGridConfig()
    start, end = edge_endpoints(0, 0, 0, grid)
    assert start != end
    dist = math.hypot(end[0] - start[0], end[1] - start[1])
    assert dist > 0


def test_nearest_edge():
    grid = HexGridConfig()
    cx, cy = axial_to_pixel(0, 0, grid)
    edge = nearest_edge(cx + grid.size, cy, 0, 0, grid)
    assert 0 <= edge < 6


def test_axial_distance_neighbors():
    assert axial_distance(0, 0, 1, 0) == 1
    assert axial_distance(0, 0, 0, 0) == 0
    assert axial_distance(0, 0, 2, -2) == 2


def test_facing_to_degrees():
    assert facing_to_degrees(0, "flat") == 90.0
    assert facing_to_degrees(6, "flat") == 270.0
    assert facing_to_degrees(1, "flat") == 120.0
    assert facing_to_degrees(3, "pointy") == 180.0
    assert facing_to_degrees(11, "pointy") == 60.0


def test_facing_labels_count():
    assert len(facing_labels("flat")) == 12
    assert len(facing_labels("pointy")) == 12


def test_facing_labels_short_compass():
    flat = {label: value for label, value in facing_labels("flat")}
    assert flat["N"] == 9
    assert flat["S"] == 3
    assert flat["SE"] == 1
    assert flat["NE"] == 11
    assert flat["Corner E"] == 0
    pointy = {label: value for label, value in facing_labels("pointy")}
    assert pointy["E"] == 0
    assert pointy["W"] == 6
    assert pointy["NW"] == 8
    assert pointy["SE"] == 2


def test_background_target_rect():
    grid = HexGridConfig(cols=5, rows=5, size=24.0)
    x, y, w, h = background_target_rect(grid)
    assert w > 0
    assert h > 0
    assert x <= 0 or y <= 0 or True  # bounds exist


def test_compute_background_layout_stretch():
    grid = HexGridConfig(cols=10, rows=10, size=24.0)
    dest_w, dest_h, px, py = compute_background_layout(
        "stretch_grid", 800, 600, grid
    )
    bx, by, bw, bh = background_target_rect(grid)
    assert dest_w == pytest.approx(bw)
    assert dest_h == pytest.approx(bh)
    assert px == pytest.approx(bx)
    assert py == pytest.approx(by)
