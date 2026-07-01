"""Dialogs for hex map editing."""

from __future__ import annotations

import base64
import uuid
from pathlib import Path

from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QListWidget,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from phoenix_command.session.domains.map_state import (
    BackgroundImage,
    CustomBarrierMaterial,
    HexGridConfig,
    MapLayer,
    MapState,
    Obstacle,
    Opening,
    WallSegment,
)
from phoenix_command.session.domains.token_state import TokenPlacement
from phoenix_command.tables.catalogs.action_catalog import (
    BUILTIN_ACTIONS,
    ActionCatalogState,
)
from phoenix_command.tables.catalogs.barrier_catalog import (
    BUILTIN_BARRIERS,
    resolve_protection_factor,
)
from phoenix_command.tables.catalogs.movement_catalog import TERRAIN_PRESETS


def load_image_as_b64(path: str) -> tuple[str, str]:
    data = Path(path).read_bytes()
    suffix = Path(path).suffix.lower()
    mime = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".bmp": "image/bmp",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }.get(suffix, "image/png")
    return base64.b64encode(data).decode("ascii"), mime


class MapTerrainPaletteDialog(QDialog):
    """Select terrain preset for brush."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Terrain Palette")
        self._preset_id = "open"
        layout = QVBoxLayout(self)
        self.combo = QComboBox()
        for pid, preset in TERRAIN_PRESETS.items():
            self.combo.addItem(f"{preset.name} (cost {preset.movement_cost})", pid)
        self.combo.currentIndexChanged.connect(self._on_change)
        layout.addWidget(self.combo)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _on_change(self):
        self._preset_id = self.combo.currentData()

    def preset_id(self) -> str:
        return self._preset_id

    def movement_cost(self) -> int:
        preset = TERRAIN_PRESETS.get(self._preset_id)
        return preset.movement_cost if preset else 1

    def color(self) -> str:
        preset = TERRAIN_PRESETS.get(self._preset_id)
        return preset.color if preset else "#88cc88"


class MapSizeDialog(QDialog):
    """Configure rectangular map dimensions in hexes."""

    def __init__(self, grid: HexGridConfig, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Map Size")
        layout = QFormLayout(self)

        self.cols_spin = QSpinBox()
        self.cols_spin.setRange(1, 200)
        self.cols_spin.setValue(grid.cols)
        layout.addRow("Columns (hexes):", self.cols_spin)

        self.rows_spin = QSpinBox()
        self.rows_spin.setRange(1, 200)
        self.rows_spin.setValue(grid.rows)
        layout.addRow("Rows (hexes):", self.rows_spin)

        self.orientation_combo = QComboBox()
        self.orientation_combo.addItem("Flat-top (odd-q)", "flat")
        self.orientation_combo.addItem("Pointy-top (odd-r)", "pointy")
        idx = self.orientation_combo.findData(grid.orientation)
        if idx >= 0:
            self.orientation_combo.setCurrentIndex(idx)
        layout.addRow("Orientation:", self.orientation_combo)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def apply_to(self, grid: HexGridConfig) -> None:
        grid.cols = self.cols_spin.value()
        grid.rows = self.rows_spin.value()
        grid.orientation = self.orientation_combo.currentData()


class MapObstacleDialog(QDialog):
    """Configure obstacle properties."""

    def __init__(self, obstacle: Obstacle | None = None, map_state: MapState | None = None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Obstacle Properties")
        self._map_state = map_state or MapState()
        obs = obstacle or Obstacle()
        layout = QFormLayout(self)

        self.height_spin = QDoubleSpinBox()
        self.height_spin.setRange(0.1, 50.0)
        self.height_spin.setValue(obs.height)
        layout.addRow("Height (m):", self.height_spin)

        self.material_combo = QComboBox()
        for bid, barrier in sorted(BUILTIN_BARRIERS.items(), key=lambda x: x[1].name):
            self.material_combo.addItem(barrier.name, bid)
        for cid, custom in self._map_state.custom_barriers.items():
            self.material_combo.addItem(f"{custom.name} (custom)", cid)
        idx = self.material_combo.findData(obs.material)
        if idx >= 0:
            self.material_combo.setCurrentIndex(idx)
        layout.addRow("Material:", self.material_combo)

        self.thickness_spin = QDoubleSpinBox()
        self.thickness_spin.setRange(0.01, 100.0)
        self.thickness_spin.setValue(obs.thickness)
        layout.addRow("Thickness (inches):", self.thickness_spin)

        self.custom_check = QCheckBox("Custom protection factor")
        self.custom_check.setChecked(obs.protection_factor is not None)
        layout.addRow(self.custom_check)

        self.pf_spin = QDoubleSpinBox()
        self.pf_spin.setRange(0.0, 20000.0)
        self.pf_spin.setValue(obs.protection_factor or 1.0)
        layout.addRow("Protection Factor:", self.pf_spin)

        self.pf_label = QLabel()
        layout.addRow("Computed PF:", self.pf_label)

        self.blocks_movement = QCheckBox()
        self.blocks_movement.setChecked(obs.blocks_movement)
        layout.addRow("Blocks Movement:", self.blocks_movement)

        self.blocks_los = QCheckBox()
        self.blocks_los.setChecked(obs.blocks_los)
        layout.addRow("Blocks LOS:", self.blocks_los)

        self.material_combo.currentIndexChanged.connect(self._update_pf)
        self.thickness_spin.valueChanged.connect(self._update_pf)
        self.custom_check.toggled.connect(self._update_pf)
        self._update_pf()

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def _update_pf(self):
        if self.custom_check.isChecked():
            self.pf_label.setText("(custom)")
            return
        mat = self.material_combo.currentData()
        pf = resolve_protection_factor(mat, self.thickness_spin.value(), self._map_state.custom_barriers)
        self.pf_label.setText(f"{pf:.1f}")

    def get_obstacle(self) -> Obstacle:
        pf = self.pf_spin.value() if self.custom_check.isChecked() else None
        return Obstacle(
            height=self.height_spin.value(),
            material=self.material_combo.currentData(),
            thickness=self.thickness_spin.value(),
            protection_factor=pf,
            blocks_movement=self.blocks_movement.isChecked(),
            blocks_los=self.blocks_los.isChecked(),
        )


class MapWallDialog(QDialog):
    """Configure wall segment properties."""

    def __init__(self, wall: WallSegment | None = None, map_state: MapState | None = None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Wall Properties")
        self._map_state = map_state or MapState()
        wall = wall or WallSegment()
        layout = QFormLayout(self)

        self.material_combo = QComboBox()
        for bid, barrier in sorted(BUILTIN_BARRIERS.items(), key=lambda x: x[1].name):
            self.material_combo.addItem(barrier.name, bid)
        for cid, custom in self._map_state.custom_barriers.items():
            self.material_combo.addItem(f"{custom.name} (custom)", cid)
        idx = self.material_combo.findData(wall.material)
        if idx >= 0:
            self.material_combo.setCurrentIndex(idx)
        layout.addRow("Material:", self.material_combo)

        self.thickness_spin = QDoubleSpinBox()
        self.thickness_spin.setRange(0.01, 100.0)
        self.thickness_spin.setValue(wall.thickness)
        layout.addRow("Thickness (inches):", self.thickness_spin)

        self.height_spin = QDoubleSpinBox()
        self.height_spin.setRange(0.1, 20.0)
        self.height_spin.setValue(wall.height)
        layout.addRow("Height (m):", self.height_spin)

        self.custom_check = QCheckBox("Custom protection factor")
        self.custom_check.setChecked(wall.protection_factor is not None)
        layout.addRow(self.custom_check)

        self.pf_spin = QDoubleSpinBox()
        self.pf_spin.setRange(0.0, 20000.0)
        self.pf_spin.setValue(wall.protection_factor or 1.0)
        layout.addRow("Protection Factor:", self.pf_spin)

        self.pf_label = QLabel()
        layout.addRow("Computed PF:", self.pf_label)

        self.material_combo.currentIndexChanged.connect(self._update_pf)
        self.thickness_spin.valueChanged.connect(self._update_pf)
        self.custom_check.toggled.connect(self._update_pf)
        self._update_pf()

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def _update_pf(self):
        if self.custom_check.isChecked():
            self.pf_label.setText("(custom)")
            return
        mat = self.material_combo.currentData()
        pf = resolve_protection_factor(mat, self.thickness_spin.value(), self._map_state.custom_barriers)
        self.pf_label.setText(f"{pf:.1f}")

    def get_wall(self) -> WallSegment:
        pf = self.pf_spin.value() if self.custom_check.isChecked() else None
        return WallSegment(
            material=self.material_combo.currentData(),
            thickness=self.thickness_spin.value(),
            height=self.height_spin.value(),
            protection_factor=pf,
        )


class MapLayerManagerDialog(QDialog):
    """Manage map layers."""

    def __init__(self, map_state: MapState, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Layer Manager")
        self._map_state = map_state
        layout = QVBoxLayout(self)

        self.list_widget = QListWidget()
        for layer in map_state.layers:
            self.list_widget.addItem(f"{layer.name} ({layer.kind}, elev {layer.elevation})")
        layout.addWidget(self.list_widget)

        btn_row = QHBoxLayout()
        add_btn = QPushButton("Add Layer")
        add_btn.clicked.connect(self._add_layer)
        btn_row.addWidget(add_btn)
        rename_btn = QPushButton("Rename")
        rename_btn.clicked.connect(self._rename_layer)
        btn_row.addWidget(rename_btn)
        bg_btn = QPushButton("Load Background")
        bg_btn.clicked.connect(self._load_background)
        btn_row.addWidget(bg_btn)
        remove_btn = QPushButton("Remove")
        remove_btn.clicked.connect(self._remove_layer)
        btn_row.addWidget(remove_btn)
        layout.addLayout(btn_row)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.rejected.connect(self.reject)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)

    def _current_layer(self) -> MapLayer | None:
        row = self.list_widget.currentRow()
        if 0 <= row < len(self._map_state.layers):
            return self._map_state.layers[row]
        return None

    def _add_layer(self):
        name, ok = QInputDialog.getText(self, "New Layer", "Layer name:", text="New Layer")
        if not ok or not name:
            return
        layer = MapLayer(name=name, kind="floor", elevation=len(self._map_state.layers))
        self._map_state.layers.append(layer)
        self.list_widget.addItem(f"{layer.name} ({layer.kind}, elev {layer.elevation})")

    def _rename_layer(self):
        layer = self._current_layer()
        if not layer:
            return
        name, ok = QInputDialog.getText(self, "Rename Layer", "Layer name:", text=layer.name)
        if ok and name:
            layer.name = name
            self.list_widget.currentItem().setText(f"{layer.name} ({layer.kind}, elev {layer.elevation})")

    def _load_background(self):
        layer = self._current_layer()
        if not layer:
            return
        path, _ = QFileDialog.getOpenFileName(
            self, "Load Background", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif *.webp)"
        )
        if not path:
            return
        data_b64, mime = load_image_as_b64(path)
        layer.background = BackgroundImage(data_b64=data_b64, mime=mime)
        QMessageBox.information(self, "Background", f"Background loaded for layer '{layer.name}'")

    def _remove_layer(self):
        layer = self._current_layer()
        if not layer or len(self._map_state.layers) <= 1:
            return
        self._map_state.layers.remove(layer)
        self.list_widget.takeItem(self.list_widget.currentRow())


class TokenDialog(QDialog):
    """Configure token placement."""

    def __init__(
        self,
        token: TokenPlacement | None = None,
        character_names: list[str] | None = None,
        parent=None,
    ):
        super().__init__(parent)
        self.setWindowTitle("Token Properties")
        tok = token or TokenPlacement(token_id=str(uuid.uuid4()))
        layout = QFormLayout(self)

        self.label_edit = QLineEdit(tok.label)
        layout.addRow("Label:", self.label_edit)

        self.char_combo = QComboBox()
        self.char_combo.addItem("(none)", None)
        for name in character_names or []:
            self.char_combo.addItem(name, name)
        if tok.character_name:
            idx = self.char_combo.findData(tok.character_name)
            if idx >= 0:
                self.char_combo.setCurrentIndex(idx)
        layout.addRow("Character:", self.char_combo)

        self.size_spin = QDoubleSpinBox()
        self.size_spin.setRange(0.3, 3.0)
        self.size_spin.setSingleStep(0.1)
        self.size_spin.setValue(tok.size)
        layout.addRow("Size (hexes):", self.size_spin)

        self.facing_spin = QSpinBox()
        self.facing_spin.setRange(0, 5)
        self.facing_spin.setValue(tok.facing)
        layout.addRow("Facing (0-5):", self.facing_spin)

        self._image_b64 = tok.image_b64
        self._image_mime = tok.image_mime
        self.image_label = QLabel("No image" if not tok.image_b64 else "Image loaded")
        layout.addRow("Image:", self.image_label)
        load_btn = QPushButton("Load Image...")
        load_btn.clicked.connect(self._load_image)
        layout.addRow(load_btn)

        self._token_id = tok.token_id
        self._layer_id = tok.layer_id
        self._q = tok.q
        self._r = tok.r

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def _load_image(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Load Token Image", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif *.webp)"
        )
        if not path:
            return
        self._image_b64, self._image_mime = load_image_as_b64(path)
        self.image_label.setText(Path(path).name)

    def get_token(self) -> TokenPlacement:
        return TokenPlacement(
            token_id=self._token_id,
            character_name=self.char_combo.currentData(),
            layer_id=self._layer_id,
            q=self._q,
            r=self._r,
            facing=self.facing_spin.value(),
            image_b64=self._image_b64,
            image_mime=self._image_mime,
            label=self.label_edit.text(),
            size=self.size_spin.value(),
        )


class ActionCatalogDialog(QDialog):
    """View action catalog and add custom actions."""

    def __init__(self, catalog: ActionCatalogState, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Action Catalog (Table 7B)")
        self._catalog = catalog
        layout = QVBoxLayout(self)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Name", "Category", "Cost"])
        self._refresh_table()
        layout.addWidget(self.table)

        add_btn = QPushButton("Add Custom Action...")
        add_btn.clicked.connect(self._add_custom)
        layout.addWidget(add_btn)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _refresh_table(self):
        actions = self._catalog.get_all_actions()
        self.table.setRowCount(len(actions))
        for row, action in enumerate(actions):
            self.table.setItem(row, 0, QTableWidgetItem(action.name))
            cat = getattr(action, "category", "Custom")
            self.table.setItem(row, 1, QTableWidgetItem(cat))
            cost = action.cost if isinstance(action.cost, str) else str(action.cost)
            self.table.setItem(row, 2, QTableWidgetItem(cost))

    def _add_custom(self):
        name, ok = QInputDialog.getText(self, "Custom Action", "Action name:")
        if not ok or not name:
            return
        cost, ok = QInputDialog.getInt(self, "Custom Action", "Action cost:", 1, 1, 999)
        if not ok:
            return
        self._catalog.add_custom_action(name, cost)
        self._refresh_table()


class CustomBarrierDialog(QDialog):
    """Add custom barrier material."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Custom Barrier Material")
        layout = QFormLayout(self)
        self.name_edit = QLineEdit()
        layout.addRow("Name:", self.name_edit)
        self.pf_spin = QDoubleSpinBox()
        self.pf_spin.setRange(0.0, 20000.0)
        self.pf_spin.setValue(1.0)
        layout.addRow("Protection Factor:", self.pf_spin)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def get_material(self) -> CustomBarrierMaterial:
        return CustomBarrierMaterial(
            id=f"custom_{uuid.uuid4().hex[:8]}",
            name=self.name_edit.text(),
            protection_factor=self.pf_spin.value(),
        )
