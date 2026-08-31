"""Map editor dialogs: size, terrain, barriers, token, stair, layers, conditions."""

from phoenix_command.gui.dialogs.map_dialogs import (
    ConditionPaletteDialog,
    CustomBarrierDialog,
    MapLayerManagerDialog,
    MapObstacleDialog,
    MapSizeDialog,
    MapTerrainPaletteDialog,
    MapWallDialog,
    StairDialog,
    TokenDialog,
)
from phoenix_command.session.domains.map_state import (
    HexGridConfig,
    MapLayer,
    MapState,
    Obstacle,
    WallSegment,
)
from phoenix_command.session.domains.token_state import TokenPlacement
from phoenix_command.tables.catalogs.movement_catalog import TERRAIN_PRESETS


def test_map_size_apply_to(qapp):
    grid = HexGridConfig(cols=10, rows=8, orientation="flat", meters_per_hex=1.0)
    dlg = MapSizeDialog(grid)
    dlg.cols_spin.setValue(20)
    dlg.rows_spin.setValue(12)
    idx = dlg.orientation_combo.findData("pointy")
    dlg.orientation_combo.setCurrentIndex(idx)
    dlg.meters_spin.setValue(2.0)
    dlg.apply_to(grid)
    assert grid.cols == 20
    assert grid.rows == 12
    assert grid.orientation == "pointy"
    assert grid.meters_per_hex == 2.0


def test_terrain_palette_open_ground(qapp):
    dlg = MapTerrainPaletteDialog()
    idx = dlg.combo.findData("open")
    dlg.combo.setCurrentIndex(idx)
    preset = TERRAIN_PRESETS["open"]
    assert dlg.preset_id() == "open"
    assert dlg.movement_cost() == preset.movement_cost
    assert dlg.color() == preset.color


def test_obstacle_catalog_and_custom_pf(qapp):
    dlg = MapObstacleDialog()
    glass = dlg.material_combo.findData("window_glass")
    assert glass >= 0
    dlg.material_combo.setCurrentIndex(glass)
    dlg._update_pf()
    assert "transparent" in dlg.vision_label.text().lower()
    assert dlg.get_obstacle().protection_factor is None
    dlg.custom_check.setChecked(True)
    dlg.pf_spin.setValue(8.0)
    obs = dlg.get_obstacle()
    assert obs.protection_factor == 8.0


def test_wall_custom_pf_none_by_default(qapp):
    dlg = MapWallDialog(WallSegment(material="window_glass"))
    dlg._update_pf()
    assert "transparent" in dlg.vision_label.text().lower()
    assert dlg.get_wall().protection_factor is None
    dlg.custom_check.setChecked(True)
    dlg.pf_spin.setValue(12.0)
    assert dlg.get_wall().protection_factor == 12.0


def test_custom_barrier_material(qapp):
    dlg = CustomBarrierDialog()
    dlg.name_edit.setText("Plexi")
    dlg.pf_spin.setValue(2.5)
    dlg.blocks_vision.setChecked(False)
    mat = dlg.get_material()
    assert mat.name == "Plexi"
    assert mat.protection_factor == 2.5
    assert mat.blocks_vision is False


def test_stair_dialog_target_layer(qapp):
    ground = MapLayer(id="g", name="Ground", kind="ground", elevation=0)
    roof = MapLayer(id="r", name="Roof", kind="floor", elevation=3)
    ms = MapState(layers=[ground, roof], active_layer_id="g")
    dlg = StairDialog(ms, "g", 1, 2)
    assert dlg.target_combo.count() == 1
    dlg.label_edit.setText("ladder")
    stair = dlg.get_stair()
    assert stair.target_layer_id == "r"
    assert stair.label == "ladder"


def test_layer_manager_toggle_visible(qapp):
    layer = MapLayer(id="g", name="Ground", visible=True)
    ms = MapState(layers=[layer], active_layer_id="g")
    dlg = MapLayerManagerDialog(ms)
    dlg.list_widget.setCurrentRow(0)
    dlg.visible_check.setChecked(False)
    assert layer.visible is False


def test_layer_manager_ceiling_combo(qapp):
    layer = MapLayer(id="g", name="Ground", kind="ground", has_ceiling=None)
    ms = MapState(layers=[layer], active_layer_id="g")
    dlg = MapLayerManagerDialog(ms)
    dlg.list_widget.setCurrentRow(0)
    yes_idx = dlg.ceiling_combo.findData(True)
    dlg.ceiling_combo.setCurrentIndex(yes_idx)
    assert layer.has_ceiling is True
    no_idx = dlg.ceiling_combo.findData(False)
    dlg.ceiling_combo.setCurrentIndex(no_idx)
    assert layer.has_ceiling is False


def test_token_dialog_get_token(qapp):
    existing = TokenPlacement(token_id="tok1", q=2, r=3, layer_id="g", facing=0)
    dlg = TokenDialog(
        token=existing,
        character_names=["AK-74 Fighter"],
        grid_orientation="flat",
        player_options=[("p1", "Alice")],
        side_options=[("alpha", "Alpha")],
    )
    idx = dlg.char_combo.findData("AK-74 Fighter")
    dlg.char_combo.setCurrentIndex(idx)
    dlg.size_spin.setValue(0.5)
    dlg.side_edit.setText("bravo")
    cidx = dlg.control_combo.findData("p1")
    dlg.control_combo.setCurrentIndex(cidx)
    tok = dlg.get_token()
    assert tok.character_name == "AK-74 Fighter"
    assert tok.size == 0.5
    assert tok.side_id == "bravo"
    assert tok.controlled_by == "p1"
    assert tok.token_id == "tok1"


def test_condition_palette_excludes_default(qapp):
    layer = MapLayer(id="g", name="Ground", default_visibility="GOOD_VISIBILITY")
    dlg = ConditionPaletteDialog(layer)
    override_values = [
        dlg.visibility_combo.itemData(i) for i in range(dlg.visibility_combo.count())
    ]
    assert "" in override_values
    assert "GOOD_VISIBILITY" not in override_values
    night = dlg.default_visibility_combo.findData("NIGHT_FULL_MOON")
    if night >= 0:
        dlg.default_visibility_combo.setCurrentIndex(night)
        chosen = dlg.default_visibility_combo.currentData()
        values = [
            dlg.visibility_combo.itemData(i) for i in range(dlg.visibility_combo.count())
        ]
        assert chosen not in values
    dlg.apply_to_layer()
    assert layer.default_visibility == dlg.default_visibility_name()
