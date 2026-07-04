"""Tests for map state serialization."""

import base64

import pytest

from phoenix_command.session.domains.map_state import (
    BackgroundImage,
    CustomBarrierMaterial,
    HexGridConfig,
    LayerStair,
    MapLayer,
    MapState,
    Obstacle,
    Opening,
    TerrainTile,
    WallSegment,
    rules_hexes,
)
from phoenix_command.session.domains.token_state import TokenPlacement, TokenState
from phoenix_command.session.game_state import GameState
from phoenix_command.session.sync_protocol import apply_message_to_state, make_full_state_message
from phoenix_command.tables.catalogs.action_catalog import ActionCatalogState
from phoenix_command.tables.catalogs.barrier_catalog import resolve_protection_factor
from phoenix_command.tables.catalogs.movement_catalog import TERRAIN_PRESETS


def test_map_state_round_trip():
    layer = MapLayer(name="Floor 1", kind="floor", elevation=1)
    layer.terrain["0,0"] = TerrainTile("open", 1, "#88cc88")
    layer.obstacles["1,0"] = Obstacle(height=2.0, material="steel", thickness=1.0)
    layer.walls["0,1:2"] = WallSegment(
        material="cinder_block",
        thickness=8.0,
        height=2.5,
        openings=[Opening(kind="door", state="locked", position=0.5)],
    )
    layer.background = BackgroundImage(
        data_b64=base64.b64encode(b"fakepng").decode("ascii"),
        mime="image/png",
    )
    state = MapState(
        grid=HexGridConfig(meters_per_hex=1.0),
        layers=[layer],
        active_layer_id=layer.id,
        custom_barriers={
            "custom_x": CustomBarrierMaterial("custom_x", "Mystery Wall", 42.0),
        },
    )
    restored = MapState.from_dict(state.to_dict())
    assert restored.grid.meters_per_hex == 1.0
    assert len(restored.layers) == 1
    assert restored.layers[0].terrain["0,0"].movement_cost == 1
    assert restored.layers[0].obstacles["1,0"].material == "steel"
    assert restored.layers[0].walls["0,1:2"].openings[0].state == "locked"
    assert restored.custom_barriers["custom_x"].protection_factor == 42.0


def test_map_state_legacy_migration():
    legacy = {"width": 10, "height": 10, "hexes": {"0,0": 1}, "obstacles": {"1,1": "wall"}}
    state = MapState.from_dict(legacy)
    assert len(state.layers) == 1
    assert "0,0" in state.layers[0].terrain
    assert "1,1" in state.layers[0].obstacles


def test_token_state_round_trip():
    token = TokenPlacement(
        token_id="t1",
        character_name="Soldier",
        layer_id="layer1",
        q=3,
        r=4,
        image_b64=base64.b64encode(b"token").decode("ascii"),
        label="Alpha",
        size=1.2,
    )
    state = TokenState(placements={"t1": token})
    restored = TokenState.from_dict(state.to_dict())
    assert restored.placements["t1"].q == 3
    assert restored.placements["t1"].image_b64


def test_token_facing_legacy_migration():
    legacy = {"token_id": "t1", "facing": 3}
    tok = TokenPlacement.from_dict(legacy)
    assert tok.facing == 6

    modern = {"token_id": "t2", "facing": 3, "facing_resolution": 12}
    tok2 = TokenPlacement.from_dict(modern)
    assert tok2.facing == 3


def test_token_facing_round_trip():
    token = TokenPlacement(token_id="t1", facing=7)
    restored = TokenPlacement.from_dict(token.to_dict())
    assert restored.facing == 7
    assert token.to_dict()["facing_resolution"] == 12


def test_full_state_with_map_and_tokens():
    gs = GameState()
    gs.map = MapState()
    gs.map.ensure_default_layer()
    gs.tokens = TokenState()
    gs.tokens.placements["t1"] = TokenPlacement(token_id="t1", q=0, r=0)
    msg = make_full_state_message(gs)
    applied = apply_message_to_state(GameState(), msg)
    assert applied.map is not None
    assert applied.tokens is not None
    assert "t1" in applied.tokens.placements


def test_rules_hexes():
    assert rules_hexes(4.0) == 2.0
    assert rules_hexes(10.0) == 5.0


def test_barrier_pf_fixed():
    pf = resolve_protection_factor("door_interior_wood", 1.0)
    assert pf == pytest.approx(0.3)


def test_barrier_pf_interpolation():
    pf = resolve_protection_factor("steel", 0.375)
    assert 16 < pf < 42


def test_barrier_custom_material():
    custom = {"custom_x": CustomBarrierMaterial("custom_x", "Test", 99.0)}
    pf = resolve_protection_factor("custom_x", 1.0, custom)
    assert pf == 99.0


def test_action_catalog_custom():
    catalog = ActionCatalogState()
    action = catalog.add_custom_action("Reload under fire", 5)
    restored = ActionCatalogState.from_dict(catalog.to_dict())
    assert action.id in restored.custom_actions
    assert restored.custom_actions[action.id].cost == 5


def test_builtin_open_door_action():
    from phoenix_command.tables.catalogs.action_catalog import BUILTIN_ACTIONS
    assert BUILTIN_ACTIONS["open_door"].cost == 3


def test_terrain_presets():
    assert TERRAIN_PRESETS["impassable"].movement_cost == -1


def test_hex_grid_config_cols_rows_round_trip():
    grid = HexGridConfig(cols=30, rows=15, orientation="pointy")
    restored = HexGridConfig.from_dict(grid.to_dict())
    assert restored.cols == 30
    assert restored.rows == 15
    assert restored.orientation == "pointy"


def test_wall_resolved_pf_from_catalog():
    wall = WallSegment(material="door_interior_wood", thickness=1.0)
    assert wall.resolved_pf() == pytest.approx(0.3)


def test_wall_resolved_pf_override():
    wall = WallSegment(material="steel", thickness=1.0, protection_factor=999.0)
    assert wall.resolved_pf() == 999.0


def test_obstacle_resolved_pf():
    obs = Obstacle(material="common_furniture", thickness=1.0)
    assert obs.resolved_pf() == pytest.approx(1.0)


def test_background_image_extended_round_trip():
    bg = BackgroundImage(
        data_b64="abc",
        fit_mode="stretch_grid",
        scale_x=1.5,
        scale_y=2.0,
        rotation=45.0,
    )
    restored = BackgroundImage.from_dict(bg.to_dict())
    assert restored.fit_mode == "stretch_grid"
    assert restored.scale_x == 1.5
    assert restored.scale_y == 2.0
    assert restored.rotation == 45.0


def test_background_image_legacy_scale():
    data = {"data_b64": "x", "scale": 2.5}
    bg = BackgroundImage.from_dict(data)
    assert bg.scale_x == 2.5
    assert bg.scale_y == 2.5
    assert bg.fit_mode == "manual"


def test_layer_stair_round_trip():
    stair = LayerStair(target_layer_id="layer-b", label="Upstairs")
    layer = MapLayer()
    layer.stairs["0,0"] = stair
    restored = MapLayer.from_dict(layer.to_dict())
    assert restored.stairs["0,0"].target_layer_id == "layer-b"
    assert restored.stairs["0,0"].label == "Upstairs"


def test_map_state_hide_inactive_layers():
    state = MapState(hide_inactive_layers=True)
    state.ensure_default_layer()
    restored = MapState.from_dict(state.to_dict())
    assert restored.hide_inactive_layers is True


def test_map_state_legacy_hide_inactive_default():
    layer = MapLayer()
    data = {"grid": {}, "layers": [layer.to_dict()], "active_layer_id": layer.id}
    state = MapState.from_dict(data)
    assert state.hide_inactive_layers is False
