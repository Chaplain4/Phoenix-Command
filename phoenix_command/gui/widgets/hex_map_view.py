"""Hex map view and editor widget."""

from __future__ import annotations

import base64

from PyQt6.QtCore import QBuffer, QByteArray, QIODevice, QPointF, Qt, pyqtSignal
from PyQt6.QtGui import (
    QBrush,
    QColor,
    QImage,
    QPainter,
    QPen,
    QWheelEvent,
)
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QGraphicsEllipseItem,
    QGraphicsItem,
    QGraphicsLineItem,
    QGraphicsRectItem,
    QGraphicsTextItem,
    QGraphicsView,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from phoenix_command.gui.dialogs.map_dialogs import (
    ConditionPaletteDialog,
    MapLayerManagerDialog,
    MapObstacleDialog,
    MapSizeDialog,
    MapTerrainPaletteDialog,
    MapWallDialog,
    StairDialog,
    TokenDialog,
)
from phoenix_command.gui.utils.hex_geometry import (
    axial_distance,
    axial_to_pixel,
    background_target_rect,
    hex_corners,
    is_in_bounds,
    iter_offset_rect,
    nearest_edge,
    pixel_to_axial,
    pixel_to_offset,
)
from phoenix_command.gui.widgets.combat_map_bar import CombatMapBar
from phoenix_command.gui.widgets.hex_map_modes import (
    ANNOTATION_BRUSH_SIZE,
    CATEGORY_MODES,
    SIDE_COLORS,
    ZOOM_MAX,
    ZOOM_MIN,
    ZOOM_STEP,
    EditMode,
    EditorCategory,
)
from phoenix_command.gui.widgets.hex_map_scene import HexMapScene
from phoenix_command.gui.widgets.token_graphics import TokenGraphicsItem
from phoenix_command.gui.widgets.wrapping_toolbar import WrappingToolbar
from phoenix_command.session.domains.impulse_combat_state import ImpulseCombatState
from phoenix_command.session.domains.map_state import (
    HexCondition,
    Obstacle,
    Opening,
    TerrainTile,
    WallSegment,
    hex_wall_key,
)
from phoenix_command.session.domains.player_info import PlayerInfo
from phoenix_command.session.domains.token_state import TokenPlacement
from phoenix_command.tables.catalogs.movement_catalog import TERRAIN_PRESETS

__all__ = [
    "CATEGORY_MODES",
    "EditMode",
    "EditorCategory",
    "HexMapScene",
    "HexMapView",
    "SIDE_COLORS",
    "TokenGraphicsItem",
]

class HexMapView(QWidget):
    """Hex map editor widget with toolbar."""

    map_changed = pyqtSignal()
    combat_action_requested = pyqtSignal(str, str, dict)
    advance_impulse_requested = pyqtSignal()
    map_mode_changed = pyqtSignal(str)
    declare_shot_requested = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._category = EditorCategory.TOKENS
        self._mode = EditMode.SELECT
        self._placement_style = "edge"  # "edge" | "hex" for walls/obstacles object tools
        self._terrain_preset = "open"
        self._obstacle_template = Obstacle()
        self._wall_template = WallSegment()
        self._door_state = "closed"
        self._editable = True
        self._character_names: list[str] = []
        self._zoom = 1.0
        self._selected_token_id: str | None = None

        # Drag-paint state
        self._painting = False
        self._last_cell: tuple[int, int] | None = None
        self._last_edge: tuple[str, int] | None = None
        self._dirty = False

        # Rubber-band fill/erase state (terrain, obstacle, wall-hex, eraser)
        self._rubber_drag = False
        self._rubber_start: tuple[int, int] | None = None
        self._rubber_end: tuple[int, int] | None = None
        self._rubber_band: QGraphicsRectItem | None = None
        self._rubber_kind: str | None = None  # terrain | obstacle | wall_hex | erase

        # Annotation stroke state
        self._annotate_painting = False
        self._annotate_image: QImage | None = None
        self._annotate_origin: tuple[float, float] = (0.0, 0.0)
        self._annotate_last: QPointF | None = None

        # Middle-button pan state
        self._panning = False
        self._pan_start = QPointF()

        # Ruler state (transient overlay while LMB held)
        self._ruler_drag = False
        self._ruler_start: tuple[int, int] | None = None
        self._ruler_end: tuple[int, int] | None = None
        self._ruler_items: list[QGraphicsItem] = []

        self._impulse_combat = ImpulseCombatState()
        self._session_role: str | None = None
        self._player_id = "host"
        self._players: list[PlayerInfo] = []
        self._condition_visibility = ""
        self._pick_move_token_id: str | None = None
        self._pick_move_action: str | None = None
        self._combat_callbacks = None  # set by main window

        self._scene = HexMapScene()
        self._scene.on_token_moved_callback = self._emit_map_changed
        self._scene.on_token_edit_callback = self._edit_token_item
        self._scene.on_token_delete_callback = self._delete_token_item
        self._scene.on_token_stair_callback = self._token_move_via_stair
        self._view = QGraphicsView(self._scene)
        self._view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self._view.setDragMode(QGraphicsView.DragMode.NoDrag)
        self._view.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)

        self._setup_toolbar()
        self._combat_bar = CombatMapBar()
        self._combat_bar.map_mode_changed.connect(self._on_map_mode_changed)
        self._combat_bar.advance_impulse_requested.connect(self.advance_impulse_requested.emit)
        self._combat_bar.combat_action_requested.connect(self._on_combat_action)
        self._combat_bar.token_selected.connect(self._on_combat_token_selected)
        self._combat_bar.declare_shot_requested.connect(self.declare_shot_requested.emit)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._toolbar)
        layout.addWidget(self._combat_bar)
        layout.addWidget(self._view)

        self._scene.map_state.ensure_default_layer()
        self._scene._update_scene_rect()
        self._rebuild_scene()
        self._apply_category_visibility()

    def _setup_toolbar(self) -> None:
        self._toolbar = WrappingToolbar()

        self._category_buttons: dict[EditorCategory, QPushButton] = {}
        for label, cat in [
            ("Map", EditorCategory.MAP),
            ("Terrain", EditorCategory.TERRAIN),
            ("Objects", EditorCategory.OBJECTS),
            ("Tokens", EditorCategory.TOKENS),
        ]:
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, c=cat: self._set_category(c))
            self._toolbar.add_widget(btn)
            self._category_buttons[cat] = btn
        self._category_buttons[EditorCategory.TOKENS].setChecked(True)

        self._toolbar.add_separator()

        mode_labels = [
            ("Select", EditMode.SELECT),
            ("Brush", EditMode.ANNOTATE_BRUSH),
            ("Annot. Eraser", EditMode.ANNOTATE_ERASER),
            ("Terrain", EditMode.TERRAIN),
            ("Obstacle", EditMode.OBSTACLE),
            ("Wall", EditMode.WALL),
            ("Window", EditMode.WINDOW),
            ("Door", EditMode.DOOR),
            ("Token", EditMode.TOKEN),
            ("Stair", EditMode.STAIR),
            ("Ruler", EditMode.RULER),
            ("Eraser", EditMode.ERASER),
            ("Condition", EditMode.CONDITION),
        ]
        self._mode_buttons: dict[EditMode, QPushButton] = {}
        for label, mode in mode_labels:
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, m=mode: self._set_mode(m))
            self._toolbar.add_widget(btn)
            self._mode_buttons[mode] = btn
        self._mode_buttons[EditMode.SELECT].setChecked(True)

        self._toolbar.add_separator()
        self._edge_btn = QPushButton("Edge")
        self._edge_btn.setCheckable(True)
        self._edge_btn.setChecked(True)
        self._edge_btn.clicked.connect(lambda: self._set_placement_style("edge"))
        self._toolbar.add_widget(self._edge_btn)
        self._hex_btn = QPushButton("Hex")
        self._hex_btn.setCheckable(True)
        self._hex_btn.clicked.connect(lambda: self._set_placement_style("hex"))
        self._toolbar.add_widget(self._hex_btn)

        self._toolbar.add_separator()
        self._layer_combo = QComboBox()
        self._layer_combo.currentIndexChanged.connect(self._on_layer_changed)
        self._toolbar.add_widget(QLabel("Layer:"))
        self._toolbar.add_widget(self._layer_combo)

        self._hide_inactive_check = QCheckBox("Hide inactive")
        self._hide_inactive_check.toggled.connect(self._on_hide_inactive_toggled)
        self._toolbar.add_widget(self._hide_inactive_check)

        self._dialog_buttons: dict[str, QPushButton] = {}
        for label, slot, key in [
            ("Layers...", self._open_layer_manager, "layers"),
            ("Terrain...", self._open_terrain_palette, "terrain"),
            ("Conditions...", self._open_condition_palette, "conditions"),
            ("Obstacle...", self._open_obstacle_dialog, "obstacle"),
            ("Wall...", self._open_wall_dialog, "wall"),
            ("Map Size...", self._open_map_size_dialog, "map_size"),
        ]:
            btn = QPushButton(label)
            btn.clicked.connect(slot)
            self._toolbar.add_widget(btn)
            self._dialog_buttons[key] = btn

        self._door_state_btn = QPushButton("Door: closed")
        self._door_state_btn.clicked.connect(self._cycle_door_state)
        self._toolbar.add_widget(self._door_state_btn)

        self._toolbar.add_separator()
        for label, slot in [
            ("Zoom +", lambda: self._apply_zoom(ZOOM_STEP)),
            ("Zoom -", lambda: self._apply_zoom(1 / ZOOM_STEP)),
            ("Reset", self._zoom_reset),
            ("Fit", self._zoom_fit),
        ]:
            btn = QPushButton(label)
            btn.clicked.connect(slot)
            self._toolbar.add_widget(btn)
        self._zoom_label = QLabel("100%")
        self._toolbar.add_widget(self._zoom_label)

        self._view.viewport().installEventFilter(self)

    # --- Zoom ---

    def _apply_zoom(self, factor: float) -> None:
        new_zoom = self._zoom * factor
        new_zoom = max(ZOOM_MIN, min(ZOOM_MAX, new_zoom))
        actual = new_zoom / self._zoom
        self._zoom = new_zoom
        self._view.scale(actual, actual)
        self._update_zoom_label()

    def _zoom_reset(self) -> None:
        self._view.resetTransform()
        self._zoom = 1.0
        self._update_zoom_label()

    def _zoom_fit(self) -> None:
        self._view.fitInView(self._scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        self._zoom = self._view.transform().m11()
        self._update_zoom_label()

    def _update_zoom_label(self) -> None:
        self._zoom_label.setText(f"{int(self._zoom * 100)}%")

    # --- Event filter ---

    def eventFilter(self, obj, event):
        if obj is not self._view.viewport():
            return super().eventFilter(obj, event)

        et = event.type()

        if et == event.Type.Wheel:
            if self._try_rotate_selected_token(event):
                return True
            delta = event.angleDelta().y()
            factor = ZOOM_STEP if delta > 0 else 1 / ZOOM_STEP
            self._apply_zoom(factor)
            return True

        if et == event.Type.MouseButtonPress:
            pos = self._view.mapToScene(event.position().toPoint())
            if event.button() == Qt.MouseButton.MiddleButton:
                self._panning = True
                self._pan_start = event.position()
                return True
            if event.button() == Qt.MouseButton.LeftButton and self._can_edit_map():
                return self._on_lmb_press(pos.x(), pos.y())
            if event.button() == Qt.MouseButton.LeftButton and self._impulse_combat.map_mode == "combat":
                return self._on_lmb_press(pos.x(), pos.y())

        if et == event.Type.MouseMove:
            if self._panning:
                delta = event.position() - self._pan_start
                self._pan_start = event.position()
                self._view.horizontalScrollBar().setValue(
                    self._view.horizontalScrollBar().value() - int(delta.x())
                )
                self._view.verticalScrollBar().setValue(
                    self._view.verticalScrollBar().value() - int(delta.y())
                )
                return True
            if self._can_edit_map() and (
                self._painting or self._rubber_drag or self._ruler_drag or self._annotate_painting
            ):
                pos = self._view.mapToScene(event.position().toPoint())
                return self._on_lmb_move(pos.x(), pos.y())

        if et == event.Type.MouseButtonRelease:
            if event.button() == Qt.MouseButton.MiddleButton and self._panning:
                self._panning = False
                return True
            if event.button() == Qt.MouseButton.LeftButton and (
                self._can_edit_map() or self._annotate_painting or self._rubber_drag or self._painting
            ):
                return self._on_lmb_release()

        return super().eventFilter(obj, event)

    def wheelEvent(self, event: QWheelEvent) -> None:
        super().wheelEvent(event)

    def _try_rotate_selected_token(self, event) -> bool:
        """Rotate selected token with mouse wheel in Tokens mode (edit). Ctrl still zooms."""
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            return False
        if not self._editable or self._impulse_combat.map_mode == "combat":
            return False
        if self._category != EditorCategory.TOKENS:
            return False
        if not self._selected_token_id:
            return False
        item = self._scene._token_items.get(self._selected_token_id)
        if item is None:
            return False
        scene_pos = self._view.mapToScene(event.position().toPoint())
        # Only rotate when pointer is near the selected token
        if not item.contains(item.mapFromScene(scene_pos)):
            # Allow rotate anytime a token is selected in tokens mode
            pass
        delta = 1 if event.angleDelta().y() > 0 else -1
        item.apply_facing_delta(delta)
        self._scene.token_state.placements[item.token.token_id] = item.token
        self.map_changed.emit()
        return True

    # --- Mouse handlers ---

    def _can_edit_map(self) -> bool:
        if self._impulse_combat.map_mode == "combat":
            return self._pick_move_token_id is not None
        return self._editable

    def _on_lmb_press(self, x: float, y: float) -> bool:
        grid = self._scene.map_state.grid
        q, r = pixel_to_axial(x, y, grid)
        if not is_in_bounds(q, r, grid):
            return True

        if self._pick_move_token_id and self._pick_move_action:
            self.combat_action_requested.emit(
                self._pick_move_token_id,
                self._pick_move_action,
                {"target_q": q, "target_r": r},
            )
            self._pick_move_token_id = None
            self._pick_move_action = None
            return True

        if self._impulse_combat.map_mode == "combat":
            return self._on_combat_lmb(q, r)

        if self._mode in (EditMode.ANNOTATE_BRUSH, EditMode.ANNOTATE_ERASER):
            self._start_annotation_stroke(x, y)
            return True

        if self._mode == EditMode.SELECT:
            self._select_token_at(q, r)
            return True

        if self._mode == EditMode.TERRAIN:
            col, row = pixel_to_offset(x, y, grid)
            self._rubber_drag = True
            self._rubber_kind = "terrain"
            self._rubber_start = (col, row)
            self._show_rubber_band(col, row, col, row)
            return True

        if self._mode == EditMode.OBSTACLE:
            col, row = pixel_to_offset(x, y, grid)
            self._rubber_drag = True
            self._rubber_kind = "obstacle"
            self._rubber_start = (col, row)
            self._show_rubber_band(col, row, col, row)
            return True

        if self._mode == EditMode.WALL and self._placement_style == "hex":
            col, row = pixel_to_offset(x, y, grid)
            self._rubber_drag = True
            self._rubber_kind = "wall_hex"
            self._rubber_start = (col, row)
            self._show_rubber_band(col, row, col, row)
            return True

        if self._mode == EditMode.ERASER:
            col, row = pixel_to_offset(x, y, grid)
            self._rubber_drag = True
            self._rubber_kind = "erase"
            self._rubber_start = (col, row)
            self._show_rubber_band(col, row, col, row)
            return True

        if self._mode == EditMode.TOKEN:
            self._place_token(q, r)
            return True

        if self._mode == EditMode.STAIR:
            self._place_stair(q, r)
            return True

        if self._mode == EditMode.RULER:
            self._ruler_drag = True
            self._ruler_start = (q, r)
            self._ruler_end = (q, r)
            self._draw_ruler_overlay()
            return True

        if self._mode in (EditMode.WALL, EditMode.WINDOW, EditMode.DOOR, EditMode.CONDITION):
            self._painting = True
            self._dirty = False
            self._last_cell = None
            self._last_edge = None
            self._paint_at(x, y, q, r)
            return True

        return False

    def _on_lmb_move(self, x: float, y: float) -> bool:
        grid = self._scene.map_state.grid

        if self._annotate_painting:
            self._continue_annotation_stroke(x, y)
            return True

        if self._rubber_drag and self._rubber_start is not None:
            col, row = pixel_to_offset(x, y, grid)
            c0, r0 = self._rubber_start
            self._show_rubber_band(c0, r0, col, row)
            return True

        if self._ruler_drag and self._ruler_start is not None:
            q, r = pixel_to_axial(x, y, grid)
            if is_in_bounds(q, r, grid):
                self._ruler_end = (q, r)
            self._draw_ruler_overlay()
            return True

        if self._painting:
            q, r = pixel_to_axial(x, y, grid)
            if is_in_bounds(q, r, grid):
                self._paint_at(x, y, q, r)
            return True

        return False

    def _on_lmb_release(self) -> bool:
        if self._annotate_painting:
            self._finish_annotation_stroke()
            return True

        if self._rubber_drag and self._rubber_start is not None:
            self._remove_rubber_band()
            c0, r0 = self._rubber_start
            c1, r1 = self._rubber_end if self._rubber_end else self._rubber_start
            kind = self._rubber_kind
            self._rubber_drag = False
            self._rubber_start = None
            self._rubber_end = None
            self._rubber_kind = None
            if kind == "terrain":
                self._fill_terrain_rect(c0, r0, c1, r1)
            elif kind == "obstacle":
                self._fill_obstacle_rect(c0, r0, c1, r1)
            elif kind == "wall_hex":
                self._fill_wall_hex_rect(c0, r0, c1, r1)
            elif kind == "erase":
                self._erase_objects_rect(c0, r0, c1, r1)
            self._rebuild_scene()
            self.map_changed.emit()
            return True

        if self._ruler_drag:
            self._ruler_drag = False
            self._ruler_start = None
            self._ruler_end = None
            self._clear_ruler_overlay()
            return True

        if self._painting:
            self._painting = False
            if self._dirty:
                self._rebuild_scene()
                self.map_changed.emit()
            self._last_cell = None
            self._last_edge = None
            return True

        return False

    # --- Rubber band ---

    def _show_rubber_band(self, c0: int, r0: int, c1: int, r1: int) -> None:
        self._rubber_end = (c1, r1)
        grid = self._scene.map_state.grid
        self._remove_rubber_band()

        from phoenix_command.gui.utils.hex_geometry import offset_to_axial

        all_corners: list[tuple[float, float]] = []
        for col in range(min(c0, c1), max(c0, c1) + 1):
            for row in range(min(r0, r1), max(r0, r1) + 1):
                if 0 <= col < grid.cols and 0 <= row < grid.rows:
                    q, r = offset_to_axial(col, row, grid)
                    all_corners.extend(hex_corners(q, r, grid))

        if not all_corners:
            return
        xs = [c[0] for c in all_corners]
        ys = [c[1] for c in all_corners]
        rect = QGraphicsRectItem(min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys))
        rect.setPen(QPen(QColor(0, 120, 255), 2, Qt.PenStyle.DashLine))
        rect.setBrush(QBrush(QColor(0, 120, 255, 40)))
        rect.setZValue(2000)
        self._scene.addItem(rect)
        self._rubber_band = rect

    def _remove_rubber_band(self) -> None:
        if self._rubber_band is not None:
            self._scene.removeItem(self._rubber_band)
            self._rubber_band = None

    # --- Painting ---

    def _paint_at(self, x: float, y: float, q: int, r: int) -> None:
        grid = self._scene.map_state.grid
        layer = self._scene.map_state.get_active_layer()
        key = f"{q},{r}"

        if self._mode == EditMode.WALL:
            if self._placement_style == "hex":
                if self._last_cell == (q, r):
                    return
                layer.walls[hex_wall_key(q, r)] = WallSegment(
                    material=self._wall_template.material,
                    thickness=self._wall_template.thickness,
                    height=self._wall_template.height,
                    protection_factor=self._wall_template.protection_factor,
                )
                self._last_cell = (q, r)
                self._dirty = True
                self._rebuild_scene()
                return
            edge = nearest_edge(x, y, q, r, grid)
            edge_key = (key, edge)
            if self._last_edge == edge_key:
                return
            wall_key = f"{q},{r}:{edge}"
            layer.walls[wall_key] = WallSegment(
                material=self._wall_template.material,
                thickness=self._wall_template.thickness,
                height=self._wall_template.height,
                protection_factor=self._wall_template.protection_factor,
            )
            self._last_edge = edge_key
            self._dirty = True
            self._rebuild_scene()

        elif self._mode == EditMode.WINDOW:
            edge = nearest_edge(x, y, q, r, grid)
            edge_key = (key, edge)
            if self._last_edge == edge_key:
                return
            wall_key = f"{q},{r}:{edge}"
            wall = layer.walls.get(wall_key, WallSegment())
            wall.openings.append(Opening(kind="window", state="closed", position=0.5))
            layer.walls[wall_key] = wall
            self._last_edge = edge_key
            self._dirty = True
            self._rebuild_scene()

        elif self._mode == EditMode.DOOR:
            edge = nearest_edge(x, y, q, r, grid)
            edge_key = (key, edge)
            if self._last_edge == edge_key:
                return
            wall_key = f"{q},{r}:{edge}"
            wall = layer.walls.get(wall_key, WallSegment())
            wall.openings.append(Opening(kind="door", state=self._door_state, position=0.5))
            layer.walls[wall_key] = wall
            self._last_edge = edge_key
            self._dirty = True
            self._rebuild_scene()

        elif self._mode == EditMode.CONDITION:
            if self._last_cell == (q, r):
                return
            if self._condition_visibility:
                layer.conditions[key] = HexCondition(visibility=[self._condition_visibility])
            else:
                layer.conditions.pop(key, None)
            self._last_cell = (q, r)
            self._dirty = True
            self._rebuild_scene()

    def _fill_terrain_rect(self, c0: int, r0: int, c1: int, r1: int) -> None:
        grid = self._scene.map_state.grid
        layer = self._scene.map_state.get_active_layer()
        preset = TERRAIN_PRESETS.get(self._terrain_preset, TERRAIN_PRESETS["open"])
        for q, r in iter_offset_rect(c0, r0, c1, r1, grid):
            key = f"{q},{r}"
            layer.terrain[key] = TerrainTile(
                terrain_type=preset.id,
                movement_cost=preset.movement_cost,
                color=preset.color,
            )

    def _fill_obstacle_rect(self, c0: int, r0: int, c1: int, r1: int) -> None:
        grid = self._scene.map_state.grid
        layer = self._scene.map_state.get_active_layer()
        tpl = self._obstacle_template
        for q, r in iter_offset_rect(c0, r0, c1, r1, grid):
            layer.obstacles[f"{q},{r}"] = Obstacle(
                height=tpl.height,
                material=tpl.material,
                thickness=tpl.thickness,
                protection_factor=tpl.protection_factor,
                blocks_movement=tpl.blocks_movement,
                blocks_los=tpl.blocks_los,
            )

    def _fill_wall_hex_rect(self, c0: int, r0: int, c1: int, r1: int) -> None:
        grid = self._scene.map_state.grid
        layer = self._scene.map_state.get_active_layer()
        tpl = self._wall_template
        for q, r in iter_offset_rect(c0, r0, c1, r1, grid):
            layer.walls[hex_wall_key(q, r)] = WallSegment(
                material=tpl.material,
                thickness=tpl.thickness,
                height=tpl.height,
                protection_factor=tpl.protection_factor,
            )

    def _erase_objects_rect(self, c0: int, r0: int, c1: int, r1: int) -> None:
        grid = self._scene.map_state.grid
        layer = self._scene.map_state.get_active_layer()
        for q, r in iter_offset_rect(c0, r0, c1, r1, grid):
            key = f"{q},{r}"
            layer.terrain.pop(key, None)
            layer.obstacles.pop(key, None)
            layer.stairs.pop(key, None)
            layer.conditions.pop(key, None)
            layer.walls.pop(hex_wall_key(q, r), None)
            for edge in range(6):
                layer.walls.pop(f"{q},{r}:{edge}", None)

    def _select_token_at(self, q: int, r: int) -> None:
        active = self._scene.map_state.get_active_layer()
        found: str | None = None
        for tid, tok in self._scene.token_state.placements.items():
            if tok.q == q and tok.r == r and (not tok.layer_id or tok.layer_id == active.id):
                found = tid
                break
        self._selected_token_id = found
        self._scene.set_selected_token_id(found)
        if found:
            self._impulse_combat.selected_token_id = found

    # --- Annotations (Map mode) ---

    def _ensure_annotation_image(self) -> tuple[QImage, float, float]:
        grid = self._scene.map_state.grid
        layer = self._scene.map_state.get_active_layer()
        bx, by, bw, bh = background_target_rect(grid)
        w, h = max(1, int(bw)), max(1, int(bh))
        if self._annotate_image is not None and self._annotate_image.width() == w and self._annotate_image.height() == h:
            return self._annotate_image, bx, by
        img = QImage(w, h, QImage.Format.Format_ARGB32_Premultiplied)
        img.fill(Qt.GlobalColor.transparent)
        if layer.annotations_b64:
            raw = base64.b64decode(layer.annotations_b64)
            loaded = QImage()
            if loaded.loadFromData(raw):
                img = loaded.convertToFormat(QImage.Format.Format_ARGB32_Premultiplied)
                if img.width() != w or img.height() != h:
                    img = img.scaled(w, h, Qt.AspectRatioMode.IgnoreAspectRatio,
                                     Qt.TransformationMode.SmoothTransformation)
        self._annotate_image = img
        self._annotate_origin = (bx, by)
        return img, bx, by

    def _start_annotation_stroke(self, x: float, y: float) -> None:
        img, bx, by = self._ensure_annotation_image()
        self._annotate_painting = True
        self._annotate_last = QPointF(x - bx, y - by)
        self._stamp_annotation(self._annotate_last.x(), self._annotate_last.y())
        del img

    def _continue_annotation_stroke(self, x: float, y: float) -> None:
        if not self._annotate_painting or self._annotate_last is None:
            return
        bx, by = self._annotate_origin
        cur = QPointF(x - bx, y - by)
        self._stroke_annotation(self._annotate_last, cur)
        self._annotate_last = cur

    def _stamp_annotation(self, lx: float, ly: float) -> None:
        if self._annotate_image is None:
            return
        painter = QPainter(self._annotate_image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if self._mode == EditMode.ANNOTATE_ERASER:
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
            painter.setBrush(QBrush(QColor(0, 0, 0, 0)))
            painter.setPen(Qt.PenStyle.NoPen)
            r = ANNOTATION_BRUSH_SIZE
            painter.drawEllipse(QPointF(lx, ly), r, r)
        else:
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)
            painter.setPen(QPen(QColor(20, 20, 20, 220), ANNOTATION_BRUSH_SIZE,
                                Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
            painter.drawPoint(QPointF(lx, ly))
        painter.end()

    def _stroke_annotation(self, a: QPointF, b: QPointF) -> None:
        if self._annotate_image is None:
            return
        painter = QPainter(self._annotate_image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if self._mode == EditMode.ANNOTATE_ERASER:
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
            pen = QPen(QColor(0, 0, 0, 0), ANNOTATION_BRUSH_SIZE * 2,
                       Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)
        else:
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)
            painter.setPen(QPen(QColor(20, 20, 20, 220), ANNOTATION_BRUSH_SIZE,
                                Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        painter.drawLine(a, b)
        painter.end()

    def _finish_annotation_stroke(self) -> None:
        self._annotate_painting = False
        self._annotate_last = None
        if self._annotate_image is None:
            return
        layer = self._scene.map_state.get_active_layer()
        ba = QByteArray()
        buf = QBuffer(ba)
        buf.open(QIODevice.OpenModeFlag.WriteOnly)
        self._annotate_image.save(buf, "PNG")
        buf.close()
        layer.annotations_b64 = base64.b64encode(bytes(ba)).decode("ascii")
        layer.annotations_mime = "image/png"
        self._rebuild_scene()
        self.map_changed.emit()

    def _place_token(self, q: int, r: int) -> None:
        import uuid
        layer = self._scene.map_state.get_active_layer()
        dialog = TokenDialog(
            character_names=self._character_names,
            grid_orientation=self._scene.map_state.grid.orientation,
            player_options=self._player_options(),
            side_options=self._side_options(),
            parent=self,
        )
        dialog._q = q
        dialog._r = r
        dialog._layer_id = layer.id
        if dialog.exec():
            token = dialog.get_token()
            token.q = q
            token.r = r
            token.layer_id = layer.id
            self._scene.token_state.placements[token.token_id] = token
            self._rebuild_scene()
            self.map_changed.emit()

    def _place_stair(self, q: int, r: int) -> None:
        layer = self._scene.map_state.get_active_layer()
        key = f"{q},{r}"
        existing = layer.stairs.get(key)
        dialog = StairDialog(
            self._scene.map_state,
            layer.id,
            q,
            r,
            existing=existing,
            parent=self,
        )
        if dialog.exec():
            layer.stairs[key] = dialog.get_stair()
            self._rebuild_scene()
            self.map_changed.emit()

    def _clear_ruler_overlay(self) -> None:
        for item in self._ruler_items:
            self._scene.removeItem(item)
        self._ruler_items.clear()

    def _draw_ruler_overlay(self) -> None:
        self._clear_ruler_overlay()
        if not self._ruler_drag or self._ruler_start is None or self._ruler_end is None:
            return
        grid = self._scene.map_state.grid
        q0, r0 = self._ruler_start
        q1, r1 = self._ruler_end
        x0, y0 = axial_to_pixel(q0, r0, grid)
        x1, y1 = axial_to_pixel(q1, r1, grid)
        dist = axial_distance(q0, r0, q1, r1)
        meters = dist * grid.meters_per_hex
        label = f"{dist} hex / {meters:.1f} m"

        line = QGraphicsLineItem(x0, y0, x1, y1)
        line.setPen(QPen(QColor(255, 200, 0), 2, Qt.PenStyle.DashLine))
        line.setZValue(2000)
        self._scene.addItem(line)
        self._ruler_items.append(line)

        for px, py in ((x0, y0), (x1, y1)):
            marker = QGraphicsEllipseItem(px - 4, py - 4, 8, 8)
            marker.setBrush(QBrush(QColor(255, 200, 0)))
            marker.setPen(QPen(QColor(0, 0, 0), 1))
            marker.setZValue(2000)
            self._scene.addItem(marker)
            self._ruler_items.append(marker)

        mid_x = (x0 + x1) / 2
        mid_y = (y0 + y1) / 2
        text = QGraphicsTextItem(label)
        text.setPos(mid_x + 5, mid_y - 15)
        text.setDefaultTextColor(QColor(255, 220, 0))
        text.setZValue(2001)
        self._scene.addItem(text)
        self._ruler_items.append(text)

    def _rebuild_scene(self) -> None:
        self._ruler_items.clear()
        self._scene.rebuild()

    def _emit_map_changed(self) -> None:
        self.map_changed.emit()

    def _edit_token_item(self, item: TokenGraphicsItem) -> None:
        dialog = TokenDialog(
            token=item.token,
            character_names=self._character_names,
            grid_orientation=self._scene.map_state.grid.orientation,
            player_options=self._player_options(),
            side_options=self._side_options(),
            parent=self,
        )
        if dialog.exec():
            updated = dialog.get_token()
            updated.q = item.token.q
            updated.r = item.token.r
            updated.layer_id = item.token.layer_id
            self._scene.token_state.placements[updated.token_id] = updated
            self._rebuild_scene()
            self.map_changed.emit()

    def _delete_token_item(self, item: TokenGraphicsItem) -> None:
        tid = item.token.token_id
        self._scene.token_state.placements.pop(tid, None)
        if self._selected_token_id == tid:
            self._selected_token_id = None
            self._scene.set_selected_token_id(None)
            if tid == self._impulse_combat.selected_token_id:
                self._impulse_combat.selected_token_id = None
        self._rebuild_scene()
        self.map_changed.emit()

    def _token_move_via_stair(self, token: TokenPlacement, choose_only: bool = False) -> bool:
        layer = self._scene.map_state.get_active_layer()
        key = f"{token.q},{token.r}"
        stairs = layer.stairs.get(key)
        if not stairs:
            return False
        if choose_only:
            return True

        stair_list = [stairs]
        if len(stair_list) == 1:
            target_id = stair_list[0].target_layer_id
        else:
            from PyQt6.QtWidgets import QInputDialog
            names = []
            ids = []
            for s in stair_list:
                target = self._scene.map_state.get_layer(s.target_layer_id)
                names.append(target.name if target else s.target_layer_id)
                ids.append(s.target_layer_id)
            choice, ok = QInputDialog.getItem(
                self, "Move via stair", "Select destination:", names, 0, False
            )
            if not ok:
                return True
            target_id = ids[names.index(choice)]

        token.layer_id = target_id
        self._scene.map_state.active_layer_id = target_id
        self._scene.token_state.placements[token.token_id] = token
        self._refresh_layer_combo()
        self._rebuild_scene()
        self.map_changed.emit()
        return True

    # --- Mode / dialogs ---

    def _set_placement_style(self, style: str) -> None:
        self._placement_style = style
        self._edge_btn.setChecked(style == "edge")
        self._hex_btn.setChecked(style == "hex")

    def _set_category(self, category: EditorCategory) -> None:
        self._category = category
        for c, btn in self._category_buttons.items():
            btn.setChecked(c == category)
        modes = CATEGORY_MODES[category]
        if self._mode not in modes:
            self._set_mode(modes[0])
        else:
            self._apply_category_visibility()

    def _apply_category_visibility(self) -> None:
        allowed = set(CATEGORY_MODES[self._category])
        for mode, btn in self._mode_buttons.items():
            btn.setVisible(mode in allowed)
        show_objects = self._category == EditorCategory.OBJECTS
        self._edge_btn.setVisible(show_objects)
        self._hex_btn.setVisible(show_objects)
        self._door_state_btn.setVisible(show_objects and self._mode == EditMode.DOOR)
        self._dialog_buttons["terrain"].setVisible(self._category == EditorCategory.TERRAIN)
        self._dialog_buttons["conditions"].setVisible(show_objects)
        self._dialog_buttons["obstacle"].setVisible(show_objects)
        self._dialog_buttons["wall"].setVisible(show_objects)

    def _set_mode(self, mode: EditMode) -> None:
        if self._ruler_drag:
            self._ruler_drag = False
            self._ruler_start = None
            self._ruler_end = None
            self._clear_ruler_overlay()
        # Switch category if mode belongs to another
        for cat, modes in CATEGORY_MODES.items():
            if mode in modes:
                self._category = cat
                for c, btn in self._category_buttons.items():
                    btn.setChecked(c == cat)
                break
        self._mode = mode
        for m, btn in self._mode_buttons.items():
            btn.setChecked(m == mode)
        self._apply_category_visibility()
        # Tokens movable only in Tokens category while editable
        token_movable = (
            self._editable
            and self._impulse_combat.map_mode != "combat"
            and self._category == EditorCategory.TOKENS
        )
        self._scene.set_editable(token_movable)

    def _cycle_door_state(self) -> None:
        states = ["closed", "open", "locked"]
        idx = states.index(self._door_state)
        self._door_state = states[(idx + 1) % len(states)]
        self._door_state_btn.setText(f"Door: {self._door_state}")

    def _on_layer_changed(self, index: int) -> None:
        if index < 0:
            return
        layer_id = self._layer_combo.itemData(index)
        if layer_id:
            self._scene.map_state.active_layer_id = layer_id
            self._rebuild_scene()

    def _on_hide_inactive_toggled(self, checked: bool) -> None:
        self._scene.map_state.hide_inactive_layers = checked
        self._rebuild_scene()
        self.map_changed.emit()

    def _refresh_layer_combo(self) -> None:
        self._layer_combo.blockSignals(True)
        self._layer_combo.clear()
        for layer in self._scene.map_state.layers:
            self._layer_combo.addItem(layer.name, layer.id)
        active = self._scene.map_state.get_active_layer()
        idx = self._layer_combo.findData(active.id)
        if idx >= 0:
            self._layer_combo.setCurrentIndex(idx)
        self._layer_combo.blockSignals(False)

    def _open_layer_manager(self) -> None:
        dialog = MapLayerManagerDialog(self._scene.map_state, parent=self)
        dialog.exec()
        self._refresh_layer_combo()
        self._scene._update_scene_rect()
        self._rebuild_scene()
        self.map_changed.emit()

    def _open_terrain_palette(self) -> None:
        dialog = MapTerrainPaletteDialog(parent=self)
        if dialog.exec():
            self._terrain_preset = dialog.preset_id()
            self._set_mode(EditMode.TERRAIN)

    def _open_obstacle_dialog(self) -> None:
        dialog = MapObstacleDialog(self._obstacle_template, self._scene.map_state, parent=self)
        if dialog.exec():
            self._obstacle_template = dialog.get_obstacle()

    def _open_wall_dialog(self) -> None:
        dialog = MapWallDialog(self._wall_template, self._scene.map_state, parent=self)
        if dialog.exec():
            self._wall_template = dialog.get_wall()

    def _open_map_size_dialog(self) -> None:
        dialog = MapSizeDialog(self._scene.map_state.grid, parent=self)
        if dialog.exec():
            dialog.apply_to(self._scene.map_state.grid)
            self._scene._update_scene_rect()
            self._rebuild_scene()
            self._zoom_fit()
            self.map_changed.emit()

    def set_editable(self, editable: bool) -> None:
        self._editable = editable
        in_combat = self._impulse_combat.map_mode == "combat"
        token_movable = (
            editable
            and not in_combat
            and self._category == EditorCategory.TOKENS
        )
        self._scene.set_editable(token_movable)
        self._toolbar.setEnabled(editable and not in_combat)
        self._combat_bar.set_host(self._session_role != "guest")
        self._refresh_combat_ui()

    def set_character_names(self, names: list[str]) -> None:
        self._character_names = names

    def get_impulse_combat_state(self) -> ImpulseCombatState:
        return self._impulse_combat

    def set_impulse_combat_state(self, state: ImpulseCombatState) -> None:
        self._impulse_combat = state
        self._impulse_combat.selected_token_id = state.selected_token_id
        status = {
            tid: rt.status_label()
            for tid, rt in state.token_runtime.items()
        }
        self._scene.set_token_status(status)
        if state.selected_token_id:
            self._selected_token_id = state.selected_token_id
            self._scene.set_selected_token_id(state.selected_token_id)
        self._refresh_combat_ui()
        in_combat = state.map_mode == "combat"
        token_movable = (
            self._editable
            and not in_combat
            and self._category == EditorCategory.TOKENS
        )
        self._scene.set_editable(token_movable)
        self._toolbar.setEnabled(self._editable and not in_combat)
        self._rebuild_scene()

    def set_session_context(
        self,
        role: str | None,
        player_id: str,
        players: list[PlayerInfo] | None = None,
    ) -> None:
        self._session_role = role
        self._player_id = player_id
        self._players = players or []
        is_guest = role == "guest"
        self._combat_bar.set_host(not is_guest)
        self._refresh_combat_ui()

    def set_action_provider(self, provider) -> None:
        """Callable(token_id) -> list of (action_id, label, cost)."""
        self._combat_callbacks = provider
        self._refresh_combat_ui()

    def _refresh_combat_ui(self) -> None:
        self._combat_bar.set_impulse_combat(self._impulse_combat)
        labels: dict[str, str] = {}
        for tid, tok in self._scene.token_state.placements.items():
            if self._session_role == "guest" and tok.controlled_by != self._player_id:
                continue
            label = tok.label or tok.character_name or tid[:8]
            if tok.side_id:
                label = f"[{tok.side_id}] {label}"
            labels[tid] = label
        self._combat_bar.set_tokens(labels)
        sel = self._impulse_combat.selected_token_id
        if not sel or sel not in labels:
            sel = next(iter(labels), None)
            if sel:
                self._impulse_combat.selected_token_id = sel
        if sel:
            self._selected_token_id = sel
            self._scene.set_selected_token_id(sel)
            self._combat_bar.select_token(sel)
            if self._combat_callbacks:
                self._combat_bar.set_available_actions(self._combat_callbacks(sel))
        else:
            self._combat_bar.set_available_actions([])

    def _on_map_mode_changed(self, mode: str) -> None:
        self._impulse_combat.map_mode = mode
        self.map_mode_changed.emit(mode)
        in_combat = mode == "combat"
        token_movable = (
            self._editable
            and not in_combat
            and self._category == EditorCategory.TOKENS
        )
        self._scene.set_editable(token_movable)
        self._toolbar.setEnabled(self._editable and not in_combat)
        self._refresh_combat_ui()

    def _on_combat_action(self, token_id: str, action: str, args: dict) -> None:
        if action in ("move", "movement_while_braced"):
            self._pick_move_token_id = token_id
            self._pick_move_action = action
            return
        self.combat_action_requested.emit(token_id, action, args)

    def _on_combat_token_selected(self, token_id: str) -> None:
        self._impulse_combat.selected_token_id = token_id
        self._selected_token_id = token_id
        self._scene.set_selected_token_id(token_id)
        if self._combat_callbacks:
            self._combat_bar.set_available_actions(self._combat_callbacks(token_id))
        rt = self._impulse_combat.token_runtime.get(token_id)
        if rt:
            self._combat_bar.set_impulse_combat(self._impulse_combat)

    def _on_combat_lmb(self, q: int, r: int) -> bool:
        active = self._scene.map_state.get_active_layer()
        for tid, tok in self._scene.token_state.placements.items():
            if tok.q != q or tok.r != r:
                continue
            if tok.layer_id and tok.layer_id != active.id:
                continue
            if self._session_role == "guest" and tok.controlled_by != self._player_id:
                continue
            self._impulse_combat.selected_token_id = tid
            self._selected_token_id = tid
            self._scene.set_selected_token_id(tid)
            self._combat_bar.select_token(tid)
            if self._combat_callbacks:
                self._combat_bar.set_available_actions(self._combat_callbacks(tid))
            return True
        return False

    def _open_condition_palette(self) -> None:
        dialog = ConditionPaletteDialog(parent=self)
        if dialog.exec():
            self._condition_visibility = dialog.visibility_name()
            self._set_mode(EditMode.CONDITION)

    def _player_options(self) -> list[tuple[str, str]]:
        return [(p.player_id, p.display_name) for p in self._players if not p.is_host]

    def _side_options(self) -> list[tuple[str, str]]:
        return list(self._impulse_combat.sides.items())

    def get_map_state(self) -> MapState:
        return self._scene.map_state

    def get_token_state(self) -> TokenState:
        return self._scene.token_state

    def set_map_state(self, map_state: MapState | None) -> None:
        if map_state is None:
            map_state = MapState()
        self._scene.set_map_state(map_state)
        self._hide_inactive_check.blockSignals(True)
        self._hide_inactive_check.setChecked(map_state.hide_inactive_layers)
        self._hide_inactive_check.blockSignals(False)
        self._refresh_layer_combo()

    def set_token_state(self, token_state: TokenState | None) -> None:
        if token_state is None:
            token_state = TokenState()
        self._scene.set_token_state(token_state)

    def new_map(self) -> None:
        self._scene.map_state = MapState()
        self._scene.map_state.ensure_default_layer()
        self._scene.token_state = TokenState()
        self._ruler_drag = False
        self._ruler_start = None
        self._ruler_end = None
        self._ruler_items.clear()
        self._scene._update_scene_rect()
        self._refresh_layer_combo()
        self._hide_inactive_check.setChecked(False)
        self._rebuild_scene()
        self._zoom_reset()
        self.map_changed.emit()
