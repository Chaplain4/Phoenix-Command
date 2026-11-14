"""Canonical hex edge frame: GUI edges match engine neighbors / LOS."""

from phoenix_command.gui.utils.hex_geometry import (
    axial_to_pixel,
    edge_midpoint,
    nearest_edge,
    pixel_to_axial,
)
from phoenix_command.session.domains.map_state import (
    MapLayer,
    MapState,
    WallSegment,
)
from phoenix_command.session.domains.token_state import TokenPlacement
from phoenix_command.simulations.hex_frame import (
    EDGE_NEIGHBORS,
    canonical_edge_key,
    edge_toward,
    engine_edge_to_gui,
    facing_for_edge,
    line_hexes,
    migrate_wall_keys_engine_to_gui,
    neighbor_hex,
    opposite_edge,
    wall_on_edge,
)
from phoenix_command.simulations.map_cover import gather_barrier_crossings
from phoenix_command.simulations.map_los import check_los


def test_edge_k_neighbor_matches_gui_flat_and_pointy():
    from phoenix_command.session.domains.map_state import HexGridConfig

    for orientation in ("flat", "pointy"):
        grid = HexGridConfig(orientation=orientation, size=24.0)
        for k in range(6):
            dq, dr = EDGE_NEIGHBORS[orientation][k]
            nq, nr = 5 + dq, 5 + dr
            mx, my = edge_midpoint(5, 5, k, grid)
            # Reflect center across midpoint → should land in neighbor
            cx, cy = axial_to_pixel(5, 5, grid)
            rx, ry = 2 * mx - cx, 2 * my - cy
            aq, ar = pixel_to_axial(rx, ry, grid)
            assert (aq, ar) == (nq, nr), f"{orientation} edge {k}"
            assert edge_toward(5, 5, nq, nr, orientation) == k
            assert nearest_edge(mx, my, 5, 5, grid) == k


def test_opposite_edge_midpoints_coincide():
    from phoenix_command.session.domains.map_state import HexGridConfig

    grid = HexGridConfig(orientation="flat", size=24.0)
    for k in range(6):
        nq, nr = neighbor_hex(3, 3, k, "flat")
        m1 = edge_midpoint(3, 3, k, grid)
        m2 = edge_midpoint(nq, nr, opposite_edge(k), grid)
        assert abs(m1[0] - m2[0]) < 1e-6
        assert abs(m1[1] - m2[1]) < 1e-6


def test_line_hexes_adjacent_steps_are_neighbors():
    for q1, r1 in [(8, 0), (0, 8), (5, 5), (-4, 7), (3, -6)]:
        line = line_hexes(0, 0, q1, r1)
        for a, b in zip(line, line[1:]):
            assert edge_toward(a[0], a[1], b[0], b[1]) is not None, (a, b)


def test_line_hexes_vertex_case_includes_bridge():
    # (0,0)→(1,1) is distance 2; must not jump directly.
    line = line_hexes(0, 0, 1, 1)
    assert len(line) >= 3
    assert line[0] == (0, 0)
    assert line[-1] == (1, 1)


def test_los_blocked_for_all_six_edges_both_key_sides():
    for edge in range(6):
        for side in ("a", "b"):
            layer = MapLayer(id="g", name="Ground")
            nq, nr = neighbor_hex(0, 0, edge)
            if side == "a":
                key = f"0,0:{edge}"
            else:
                key = f"{nq},{nr}:{opposite_edge(edge)}"
            layer.walls[key] = WallSegment(
                material="wall_cinder_block", height=2.5, protection_factor=4.0
            )
            ms = MapState(layers=[layer], active_layer_id="g")
            shooter = TokenPlacement(token_id="s", q=0, r=0, layer_id="g")
            target = TokenPlacement(token_id="t", q=nq, r=nr, layer_id="g")
            los = check_los(ms, shooter, target, pen=None)
            assert los.blocked is True, f"edge={edge} side={side}"


def test_no_double_pf_same_layer():
    layer = MapLayer(id="g", name="Ground")
    layer.walls["0,0:0"] = WallSegment(
        material="wall_cinder_block", height=2.5, protection_factor=4.0
    )
    ms = MapState(layers=[layer], active_layer_id="g")
    shooter = TokenPlacement(token_id="s", q=0, r=0, layer_id="g")
    target = TokenPlacement(token_id="t", q=1, r=0, layer_id="g")
    crossings = gather_barrier_crossings(ms, shooter, target)
    wall_hits = [c for c in crossings if "Wall" in c.label]
    assert len(wall_hits) == 1
    assert wall_hits[0].pf == 4.0


def test_default_wall_material_pf():
    assert WallSegment().resolved_pf() > 0


def test_wall_on_edge_both_sides():
    layer = MapLayer(id="g", name="Ground")
    layer.walls["1,0:3"] = WallSegment(material="wall_cinder_block")
    found = wall_on_edge(layer, 0, 0, 0)
    assert found is not None
    assert found[0] == "1,0:3"


def test_canonical_edge_key_stable():
    a = canonical_edge_key(0, 0, 0)
    b = canonical_edge_key(1, 0, 3)
    assert a == b


def test_migrate_engine_keys_flat():
    # Engine edge 5 = (0,+1) S → GUI edge 1
    walls = {"5,5:5": WallSegment(material="wall_cinder_block")}
    out = migrate_wall_keys_engine_to_gui(walls, "flat")
    assert "5,5:1" in out
    assert engine_edge_to_gui(5, "flat") == 1


def test_facing_for_edge_flat_sides():
    # Flat: edges map to odd facings (side midpoints)
    assert facing_for_edge(0, "flat") == 1
    assert facing_for_edge(1, "flat") == 3


def test_looks_like_engine_paired_keys():
    from phoenix_command.simulations.hex_frame import looks_like_engine_edge_keys

    # Dual-written engine sides for edge 5 (S legacy) / opposite 2
    walls = {
        "5,5:5": WallSegment(),
        "5,6:2": WallSegment(),
        "0,0:1": WallSegment(),
        "1,-1:4": WallSegment(),
    }
    assert looks_like_engine_edge_keys(walls, "flat") is True


def test_map_load_without_convention_does_not_remap():
    # Even dual-written engine-looking pairs are left alone on load.
    raw = {
        "grid": {"orientation": "flat", "cols": 20, "rows": 20},
        "active_layer_id": "g",
        "layers": [
            {
                "id": "g",
                "name": "Ground",
                "walls": {
                    "5,5:5": {"material": "wall_cinder_block", "height": 2.5},
                    "5,6:2": {"material": "wall_cinder_block", "height": 2.5},
                },
            }
        ],
    }
    ms = MapState.from_dict(raw)
    assert ms.edge_convention == "screen_cw_v1"
    assert ms.edge_convention_explicit is False
    assert set(ms.layers[0].walls) == {"5,5:5", "5,6:2"}
    # Open→save must not stamp the field (else CLI migrate becomes a no-op).
    assert "edge_convention" not in ms.to_dict()


def test_map_save_keeps_explicit_convention():
    raw = {
        "grid": {"orientation": "flat"},
        "edge_convention": "screen_cw_v1",
        "active_layer_id": "g",
        "layers": [{"id": "g", "name": "Ground", "walls": {}}],
    }
    ms = MapState.from_dict(raw)
    assert ms.edge_convention_explicit is True
    assert ms.to_dict()["edge_convention"] == "screen_cw_v1"


def test_map_roundtrip_keeps_edge_keys_migrated_from():
    raw = {
        "grid": {"orientation": "flat"},
        "edge_convention": "screen_cw_v1",
        "edge_keys_migrated_from": "engine",
        "active_layer_id": "g",
        "layers": [{"id": "g", "name": "Ground", "walls": {}}],
    }
    ms = MapState.from_dict(raw)
    assert ms.edge_keys_migrated_from == "engine"
    assert ms.to_dict()["edge_keys_migrated_from"] == "engine"


def test_gui_flat_room_h2_not_remapped_on_load():
    """Editor one-sided perimeter of a flat W×2 room must survive load."""
    # Room covering axial (0,0)-(3,0) and (0,1)-(3,1): outer edges only (GUI style).
    walls: dict = {}
    # North side of top row (flat edge 4 = N)
    for q in range(4):
        walls[f"{q},0:4"] = {"material": "wall_cinder_block", "height": 2.5}
    # South side of bottom row (flat edge 1 = S)
    for q in range(4):
        walls[f"{q},1:1"] = {"material": "wall_cinder_block", "height": 2.5}
    # West / east ends
    walls["0,0:3"] = {"material": "wall_cinder_block", "height": 2.5}
    walls["0,1:3"] = {"material": "wall_cinder_block", "height": 2.5}
    walls["3,0:0"] = {"material": "wall_cinder_block", "height": 2.5}
    walls["3,1:0"] = {"material": "wall_cinder_block", "height": 2.5}
    before = set(walls)
    raw = {
        "grid": {"orientation": "flat", "cols": 20, "rows": 20},
        "active_layer_id": "g",
        "layers": [{"id": "g", "name": "Ground", "walls": walls}],
    }
    ms = MapState.from_dict(raw)
    assert ms.edge_convention == "screen_cw_v1"
    assert set(ms.layers[0].walls) == before


def test_migrate_cli_keeps_session_schema_and_is_idempotent(tmp_path):
    import json
    import subprocess
    import sys
    from pathlib import Path

    session = {
        "schema_version": 1,
        "map": {
            "grid": {"orientation": "flat"},
            "active_layer_id": "g",
            "layers": [
                {
                    "id": "g",
                    "name": "Ground",
                    "walls": {
                        "5,5:5": {"material": "wall_cinder_block", "height": 2.5},
                        "5,6:2": {"material": "wall_cinder_block", "height": 2.5},
                    },
                }
            ],
        },
        "tokens": {},
    }
    path = tmp_path / "session.json"
    path.write_text(json.dumps(session), encoding="utf-8")
    tool = Path(__file__).resolve().parents[2] / "tools" / "migrate_edge_convention.py"
    subprocess.check_call(
        [sys.executable, str(tool), "--from", "engine", "--inplace", str(path)]
    )
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["schema_version"] == 1
    assert data["map"]["edge_convention"] == "screen_cw_v1"
    assert data["map"]["edge_keys_migrated_from"] == "engine"
    assert "5,5:1" in data["map"]["layers"][0]["walls"]
    keys_after_first = set(data["map"]["layers"][0]["walls"])
    subprocess.check_call(
        [sys.executable, str(tool), "--from", "engine", "--inplace", str(path)]
    )
    data2 = json.loads(path.read_text(encoding="utf-8"))
    assert data2["schema_version"] == 1
    assert set(data2["map"]["layers"][0]["walls"]) == keys_after_first

    # Poisoned stamp: screen_cw_v1 but keys still engine — --force recovers.
    poisoned = {
        "schema_version": 1,
        "map": {
            "grid": {"orientation": "flat"},
            "edge_convention": "screen_cw_v1",
            "active_layer_id": "g",
            "layers": [
                {
                    "id": "g",
                    "name": "Ground",
                    "walls": {
                        "5,5:5": {"material": "wall_cinder_block", "height": 2.5},
                        "5,6:2": {"material": "wall_cinder_block", "height": 2.5},
                    },
                }
            ],
        },
        "tokens": {},
    }
    path2 = tmp_path / "poisoned.json"
    path2.write_text(json.dumps(poisoned), encoding="utf-8")
    subprocess.check_call(
        [
            sys.executable,
            str(tool),
            "--from",
            "engine",
            "--force",
            "--inplace",
            str(path2),
        ]
    )
    data3 = json.loads(path2.read_text(encoding="utf-8"))
    assert "5,5:1" in data3["map"]["layers"][0]["walls"]
    assert "5,5:5" not in data3["map"]["layers"][0]["walls"]
    assert data3["map"]["edge_keys_migrated_from"] == "engine"
    keys_after_force = set(data3["map"]["layers"][0]["walls"])
    # Second --force blocked by edge_keys_migrated_from, not by pair heuristic.
    out = subprocess.check_output(
        [
            sys.executable,
            str(tool),
            "--from",
            "engine",
            "--force",
            "--inplace",
            str(path2),
        ],
        text=True,
    )
    assert "refusing --force" in out
    data4 = json.loads(path2.read_text(encoding="utf-8"))
    assert set(data4["map"]["layers"][0]["walls"]) == keys_after_force

    # Single-sided engine wall + wrong stamp: --force still remaps (no heuristic).
    single = {
        "schema_version": 1,
        "map": {
            "grid": {"orientation": "flat"},
            "edge_convention": "screen_cw_v1",
            "active_layer_id": "g",
            "layers": [
                {
                    "id": "g",
                    "name": "Ground",
                    "walls": {
                        "5,5:5": {"material": "wall_cinder_block", "height": 2.5},
                    },
                }
            ],
        },
        "tokens": {},
    }
    path3 = tmp_path / "single.json"
    path3.write_text(json.dumps(single), encoding="utf-8")
    subprocess.check_call(
        [
            sys.executable,
            str(tool),
            "--from",
            "engine",
            "--force",
            "--inplace",
            str(path3),
        ]
    )
    data5 = json.loads(path3.read_text(encoding="utf-8"))
    assert "5,5:1" in data5["map"]["layers"][0]["walls"]
    assert "5,5:5" not in data5["map"]["layers"][0]["walls"]
    assert data5["map"]["edge_keys_migrated_from"] == "engine"
