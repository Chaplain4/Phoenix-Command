"""Hex map view and editor widget."""

from __future__ import annotations

from PyQt6.QtCore import QPointF, Qt, QTimer, pyqtSignal
from PyQt6.QtGui import (
    QBrush,
    QColor,
    QCursor,
    QPainter,
    QPen,
    QWheelEvent,
)
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QGraphicsRectItem,
    QGraphicsView,
    QHBoxLayout,
    QLabel,
    QMenu,
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
    clamp_token_display_size,
    degrees_to_facing,
    hex_corners,
    is_in_bounds,
    iter_offset_rect,
    nearest_edge,
    pixel_to_axial,
    pixel_to_offset,
)
from phoenix_command.gui.widgets.editor_category_panel import EditorCategoryPanel
from phoenix_command.gui.widgets.hex_map_annotations import AnnotationOverlayController
from phoenix_command.gui.widgets.combat_map_bar import CombatMapBar
from phoenix_command.gui.widgets.hex_map_modes import (
    CATEGORY_MODES,
    SIDE_COLORS,
    ZOOM_MAX,
    ZOOM_MIN,
    ZOOM_STEP,
    EditMode,
    EditorCategory,
)
from phoenix_command.gui.widgets.map_mode_panel import MapModePanel
from phoenix_command.gui.widgets.hex_map_ruler import RulerOverlayController
from phoenix_command.gui.widgets.hex_map_scene import HexMapScene
from phoenix_command.gui.widgets.token_graphics import TokenGraphicsItem
from phoenix_command.gui.widgets.transform_gizmo import (
    HandleKind,
    TransformGizmoItem,
    TransformState,
)
from phoenix_command.gui.widgets.wrapping_toolbar import WrappingToolbar
from phoenix_command.session.domains.impulse_combat_state import ImpulseCombatState
from phoenix_command.session.domains.map_state import (
    HexCondition,
    MapState,
    Obstacle,
    Opening,
    TerrainTile,
    WallSegment,
    hex_wall_key,
)
from phoenix_command.session.domains.player_info import PlayerInfo
from phoenix_command.session.domains.token_state import TokenPlacement, TokenState
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
        self._bg_selected = False
        self._gizmo: TransformGizmoItem | None = None
        self._gizmo_target: str | None = None  # "background" | "token" | None
        self._gizmo_dragging = False

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
        self._rubber_scene_start: QPointF | None = None
        self._rubber_scene_end: QPointF | None = None

        # Middle-button pan state
        self._panning = False
        self._pan_start = QPointF()

        self._impulse_combat = ImpulseCombatState()
        self._session_role: str | None = None
        self._player_id = "host"
        self._players: list[PlayerInfo] = []
        self._condition_visibility = ""
        self._pick_move_token_id: str | None = None
        self._pick_move_action: str | None = None
        self._combat_callbacks = None  # set by main window

        self._scene = HexMapScene()
        self._annotations = AnnotationOverlayController(self._scene)
        self._ruler = RulerOverlayController(self._scene)
        self._scene.on_token_moved_callback = self._emit_map_changed
        self._scene.on_token_edit_callback = self._edit_token_item
        self._scene.on_token_delete_callback = self._delete_token_item
        self._scene.on_token_stair_callback = self._token_move_via_stair
        self._scene.on_token_context_menu_callback = self._show_token_context_menu
        self._view = QGraphicsView(self._scene)
        self._view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self._view.setDragMode(QGraphicsView.DragMode.NoDrag)
        self._view.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self._map_container = QWidget(self)
        self._map_container.setContentsMargins(0, 0, 0, 0)
        self._map_layout = QHBoxLayout(self._map_container)
        self._map_layout.setContentsMargins(0, 0, 0, 0)
        self._map_layout.addWidget(self._view)
        self._category_panel = EditorCategoryPanel(self._set_category, self._map_container)
        self._map_mode_panel = MapModePanel(self._map_container)
        self._map_container.installEventFilter(self)

        self._setup_toolbar()
        self._combat_bar = CombatMapBar()
        self._map_mode_panel.map_mode_changed.connect(self._on_map_mode_changed)
        self._combat_bar.advance_impulse_requested.connect(self.advance_impulse_requested.emit)
        self._combat_bar.combat_action_requested.connect(self._on_combat_action)
        self._combat_bar.token_selected.connect(self._on_combat_token_selected)
        self._combat_bar.declare_shot_requested.connect(self.declare_shot_requested.emit)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._toolbar)
        layout.addWidget(self._combat_bar)
        layout.addWidget(self._map_container)

        self._scene.map_state.ensure_default_layer()
        self._scene._update_scene_rect()
        self._rebuild_scene()
        self._apply_category_visibility()
        self._position_category_panel()

    def _setup_toolbar(self) -> None:
        self._toolbar = WrappingToolbar()

        mode_labels = [
            ("Select", EditMode.SELECT),
            ("Brush", EditMode.ANNOTATE_BRUSH),
            ("Annot. Eraser", EditMode.ANNOTATE_ERASER),
            ("Terrain", EditMode.TERRAIN),
            ("Eraser", EditMode.TERRAIN_ERASER),
            ("Condition", EditMode.CONDITION),
            ("Obstacle", EditMode.OBSTACLE),
            ("Wall", EditMode.WALL),
            ("Window", EditMode.WINDOW),
            ("Door", EditMode.DOOR),
            ("Token", EditMode.TOKEN),
            ("Stair", EditMode.STAIR),
            ("Ruler", EditMode.RULER),
            ("Eraser", EditMode.ERASER),
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
            ("Visibility...", self._open_condition_palette, "conditions"),
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
        if obj is self._map_container:
            if event.type() in (event.Type.Resize, event.Type.Show):
                QTimer.singleShot(0, self._position_category_panel)
            return super().eventFilter(obj, event)

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
            if event.button() == Qt.MouseButton.LeftButton and (
                self._mode == EditMode.RULER or self._can_edit_map()
            ):
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
            if (self._mode == EditMode.RULER or self._can_edit_map()) and (
                self._painting
                or self._rubber_drag
                or self._ruler.dragging
                or self._annotations.painting
                or self._gizmo_dragging
            ):
                pos = self._view.mapToScene(event.position().toPoint())
                return self._on_lmb_move(pos.x(), pos.y())

        if et == event.Type.MouseButtonRelease:
            if event.button() == Qt.MouseButton.MiddleButton and self._panning:
                self._panning = False
                return True
            if event.button() == Qt.MouseButton.LeftButton and (
                self._mode == EditMode.RULER
                or self._can_edit_map()
                or self._annotations.painting
                or self._rubber_drag
                or self._painting
                or self._gizmo_dragging
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
        self._refresh_gizmo()
        return True

    # --- Mouse handlers ---

    def _can_edit_map(self) -> bool:
        if self._impulse_combat.map_mode == "combat":
            return self._pick_move_token_id is not None
        return self._editable

    def _on_lmb_press(self, x: float, y: float) -> bool:
        grid = self._scene.map_state.grid
        q, r = pixel_to_axial(x, y, grid)

        # Background may extend outside the hex grid.
        if (
            self._impulse_combat.map_mode != "combat"
            and self._mode == EditMode.SELECT
            and self._category == EditorCategory.MAP
        ):
            return self._on_map_select_press(x, y)

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

        if self._mode == EditMode.RULER:
            self._ruler.begin(q, r)
            return True

        if self._impulse_combat.map_mode == "combat":
            return self._on_combat_lmb(q, r)

        if self._mode == EditMode.ANNOTATE_BRUSH:
            self._annotations.start_brush(x, y)
            return True

        if self._mode == EditMode.ANNOTATE_ERASER:
            self._rubber_drag = True
            self._rubber_kind = "annotate_erase"
            self._rubber_scene_start = QPointF(x, y)
            self._rubber_scene_end = QPointF(x, y)
            self._show_annotation_rubber_band(x, y, x, y)
            return True

        if self._mode == EditMode.SELECT:
            return self._on_token_select_press(x, y, q, r)

        if self._mode == EditMode.TERRAIN:
            col, row = pixel_to_offset(x, y, grid)
            self._rubber_drag = True
            self._rubber_kind = "terrain"
            self._rubber_start = (col, row)
            self._show_rubber_band(col, row, col, row)
            return True

        if self._mode == EditMode.TERRAIN_ERASER:
            col, row = pixel_to_offset(x, y, grid)
            self._rubber_drag = True
            self._rubber_kind = "terrain_erase"
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
            self._rubber_kind = "objects_erase"
            self._rubber_start = (col, row)
            self._show_rubber_band(col, row, col, row)
            return True

        if self._mode == EditMode.TOKEN:
            self._place_token(q, r)
            return True

        if self._mode == EditMode.STAIR:
            self._place_stair(q, r)
            return True

        if self._mode in (EditMode.WALL, EditMode.WINDOW, EditMode.DOOR):
            self._painting = True
            self._dirty = False
            self._last_cell = None
            self._last_edge = None
            self._paint_at(x, y, q, r)
            return True

        if self._mode == EditMode.CONDITION:
            col, row = pixel_to_offset(x, y, grid)
            self._rubber_drag = True
            self._rubber_kind = "condition"
            self._rubber_start = (col, row)
            self._show_rubber_band(col, row, col, row)
            return True

        return False

    def _on_lmb_move(self, x: float, y: float) -> bool:
        grid = self._scene.map_state.grid

        if self._gizmo_dragging and self._gizmo is not None:
            state = self._gizmo.update_drag(QPointF(x, y))
            self._apply_gizmo_live(state)
            return True

        if self._annotations.painting:
            self._annotations.continue_brush(x, y)
            return True

        if self._rubber_drag and self._rubber_kind == "annotate_erase" and self._rubber_scene_start is not None:
            self._rubber_scene_end = QPointF(x, y)
            self._show_annotation_rubber_band(
                self._rubber_scene_start.x(),
                self._rubber_scene_start.y(),
                x,
                y,
            )
            return True

        if self._rubber_drag and self._rubber_start is not None:
            col, row = pixel_to_offset(x, y, grid)
            c0, r0 = self._rubber_start
            self._show_rubber_band(c0, r0, col, row)
            return True

        if self._ruler.dragging and self._ruler.start is not None:
            q, r = pixel_to_axial(x, y, grid)
            if is_in_bounds(q, r, grid):
                self._ruler.update(q, r)
            return True

        if self._painting:
            q, r = pixel_to_axial(x, y, grid)
            if is_in_bounds(q, r, grid):
                self._paint_at(x, y, q, r)
            return True

        return False

    def _on_lmb_release(self) -> bool:
        if self._gizmo_dragging and self._gizmo is not None:
            state = self._gizmo.end_drag()
            self._gizmo_dragging = False
            self._commit_gizmo(state)
            return True

        if self._annotations.painting:
            if self._annotations.finish():
                self._rebuild_scene()
                self.map_changed.emit()
            return True

        if self._rubber_drag and self._rubber_kind == "annotate_erase" and self._rubber_scene_start is not None:
            self._remove_rubber_band()
            start = self._rubber_scene_start
            end = self._rubber_scene_end or start
            self._rubber_drag = False
            self._rubber_scene_start = None
            self._rubber_scene_end = None
            self._rubber_kind = None
            self._erase_annotations_rect(start.x(), start.y(), end.x(), end.y())
            self.map_changed.emit()
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
            elif kind == "terrain_erase":
                self._erase_terrain_rect(c0, r0, c1, r1)
            elif kind == "obstacle":
                self._fill_obstacle_rect(c0, r0, c1, r1)
            elif kind == "wall_hex":
                self._fill_wall_hex_rect(c0, r0, c1, r1)
            elif kind == "objects_erase":
                self._erase_objects_rect(c0, r0, c1, r1)
            elif kind == "condition":
                self._fill_condition_rect(c0, r0, c1, r1)
            self._rebuild_scene()
            self.map_changed.emit()
            return True

        if self._ruler.dragging:
            self._ruler.finish()
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

    def _show_annotation_rubber_band(self, x0: float, y0: float, x1: float, y1: float) -> None:
        self._remove_rubber_band()
        rect = QGraphicsRectItem(
            min(x0, x1),
            min(y0, y1),
            abs(x1 - x0),
            abs(y1 - y0),
        )
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
            opening = self._window_opening_for_hex(q, r)
            existing = next((item for item in wall.openings if item.kind == "window"), None)
            if existing is None:
                wall.openings.append(opening)
            else:
                existing.state = opening.state
                existing.position = opening.position
                existing.sill_height = opening.sill_height
                existing.head_height = opening.head_height
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
            door = next((item for item in wall.openings if item.kind == "door"), None)
            if door is None:
                wall.openings.append(Opening(kind="door", state=self._door_state, position=0.5))
            else:
                states = ["closed", "open", "locked"]
                idx = states.index(door.state) if door.state in states else 0
                door.state = states[(idx + 1) % len(states)]
            layer.walls[wall_key] = wall
            self._last_edge = edge_key
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

    def _fill_condition_rect(self, c0: int, r0: int, c1: int, r1: int) -> None:
        grid = self._scene.map_state.grid
        layer = self._scene.map_state.get_active_layer()
        for q, r in iter_offset_rect(c0, r0, c1, r1, grid):
            key = f"{q},{r}"
            if self._condition_visibility and self._condition_visibility != layer.default_visibility:
                layer.conditions[key] = HexCondition(visibility=[self._condition_visibility])
            else:
                layer.conditions.pop(key, None)

    def _erase_terrain_rect(self, c0: int, r0: int, c1: int, r1: int) -> None:
        grid = self._scene.map_state.grid
        layer = self._scene.map_state.get_active_layer()
        for q, r in iter_offset_rect(c0, r0, c1, r1, grid):
            key = f"{q},{r}"
            layer.terrain.pop(key, None)
            layer.conditions.pop(key, None)

    def _erase_objects_rect(self, c0: int, r0: int, c1: int, r1: int) -> None:
        grid = self._scene.map_state.grid
        layer = self._scene.map_state.get_active_layer()
        for q, r in iter_offset_rect(c0, r0, c1, r1, grid):
            key = f"{q},{r}"
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
        self._refresh_gizmo()

    def _on_map_select_press(self, x: float, y: float) -> bool:
        if self._gizmo is not None and self._gizmo_target == "background":
            kind = self._gizmo.hit_test(QPointF(x, y))
            if kind is not None:
                self._gizmo.begin_drag(kind, QPointF(x, y))
                self._gizmo_dragging = True
                return True
        if self._scene.hit_active_background(x, y):
            self._bg_selected = True
            self._selected_token_id = None
            self._scene.set_selected_token_id(None)
            self._refresh_gizmo()
            if self._gizmo is not None:
                kind = self._gizmo.hit_test(QPointF(x, y)) or HandleKind.BODY
                self._gizmo.begin_drag(kind, QPointF(x, y))
                self._gizmo_dragging = True
            return True
        self._bg_selected = False
        self._clear_gizmo()
        return True

    def _on_token_select_press(self, x: float, y: float, q: int, r: int) -> bool:
        if self._gizmo is not None and self._gizmo_target == "token":
            kind = self._gizmo.hit_test(QPointF(x, y))
            if kind is not None:
                self._gizmo.begin_drag(kind, QPointF(x, y))
                self._gizmo_dragging = True
                return True
        self._select_token_at(q, r)
        if self._selected_token_id and self._gizmo is not None:
            kind = self._gizmo.hit_test(QPointF(x, y)) or HandleKind.BODY
            self._gizmo.begin_drag(kind, QPointF(x, y))
            self._gizmo_dragging = True
        return True

    def _token_transform_state(self, token_id: str) -> TransformState | None:
        item = self._scene._token_items.get(token_id)
        if item is None:
            return None
        w, h = item.display_size()
        cx = item.pos().x() + w / 2.0
        cy = item.pos().y() + h / 2.0
        return TransformState(cx, cy, w, h, item.rotation())

    def _ensure_gizmo(self) -> TransformGizmoItem:
        if self._gizmo is None:
            self._gizmo = TransformGizmoItem()
            self._scene.addItem(self._gizmo)
        elif self._gizmo.scene() is None:
            self._scene.addItem(self._gizmo)
        return self._gizmo

    def _clear_gizmo(self) -> None:
        self._gizmo_dragging = False
        self._gizmo_target = None
        if self._gizmo is not None:
            if self._gizmo.scene() is not None:
                self._scene.removeItem(self._gizmo)
            self._gizmo = None

    def _refresh_gizmo(self) -> None:
        """Show/hide transform gizmo based on category, mode, and selection."""
        if (
            not self._editable
            or self._impulse_combat.map_mode == "combat"
            or self._mode != EditMode.SELECT
        ):
            self._clear_gizmo()
            self._scene.set_use_token_selection_ring(True)
            return

        if self._category == EditorCategory.MAP and self._bg_selected:
            state = self._scene.background_transform_state()
            if state is None:
                self._bg_selected = False
                self._clear_gizmo()
                return
            gizmo = self._ensure_gizmo()
            gizmo.set_state(state)
            self._gizmo_target = "background"
            self._scene.set_use_token_selection_ring(True)
            return

        if self._category == EditorCategory.TOKENS and self._selected_token_id:
            state = self._token_transform_state(self._selected_token_id)
            if state is None:
                self._clear_gizmo()
                self._scene.set_use_token_selection_ring(True)
                return
            gizmo = self._ensure_gizmo()
            gizmo.set_state(state)
            self._gizmo_target = "token"
            # Gizmo replaces the yellow ring in Tokens/Select.
            self._scene.set_use_token_selection_ring(False)
            return

        self._clear_gizmo()
        self._scene.set_use_token_selection_ring(True)

    def _apply_gizmo_live(self, state: TransformState) -> None:
        if self._gizmo_target == "background":
            self._scene.apply_background_visual(
                state.cx, state.cy, state.width, state.height, state.rotation
            )
            return
        if self._gizmo_target == "token" and self._selected_token_id:
            item = self._scene._token_items.get(self._selected_token_id)
            if item is None:
                return
            grid = self._scene.map_state.grid
            # Clamp display size to one hex during live drag.
            diameter = grid.size * 2.0
            max_dim = max(state.width, state.height)
            if max_dim > diameter and max_dim > 0:
                factor = diameter / max_dim
                state = TransformState(
                    state.cx,
                    state.cy,
                    state.width * factor,
                    state.height * factor,
                    state.rotation,
                )
                self._gizmo.set_state(state)
            item.apply_pixmap_size(state.width, state.height)
            item.setPos(state.cx - state.width / 2.0, state.cy - state.height / 2.0)
            item.set_preview_rotation(state.rotation)

    def _commit_gizmo(self, state: TransformState) -> None:
        if self._gizmo_target == "background":
            if self._scene.commit_background_from_transform(
                state.cx, state.cy, state.width, state.height, state.rotation
            ):
                self.map_changed.emit()
            self._refresh_gizmo()
            return
        if self._gizmo_target == "token" and self._selected_token_id:
            item = self._scene._token_items.get(self._selected_token_id)
            if item is None:
                return
            grid = self._scene.map_state.grid
            token = item.token
            # Convert pixel size back to size + scale_x/y, then clamp.
            base = max(1e-6, grid.size * 2.0 * token.size)
            scale_x = state.width / base
            scale_y = state.height / base
            size, scale_x, scale_y = clamp_token_display_size(
                token.size, scale_x, scale_y, grid.size
            )
            token.size = size
            token.scale_x = scale_x
            token.scale_y = scale_y
            token.facing = degrees_to_facing(state.rotation, grid.orientation)
            # Snap center to hex.
            q, r = pixel_to_axial(state.cx, state.cy, grid)
            if not is_in_bounds(q, r, grid):
                q, r = token.q, token.r
            token.q = q
            token.r = r
            self._scene.token_state.placements[token.token_id] = token
            self._rebuild_scene()
            self.map_changed.emit()
            return
        self._refresh_gizmo()

    def _erase_annotations_rect(self, x0: float, y0: float, x1: float, y1: float) -> None:
        if self._annotations.erase_rect(x0, y0, x1, y1):
            self._rebuild_scene()

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
            if existing:
                target_layer = self._scene.map_state.get_layer(existing.target_layer_id)
                if target_layer:
                    target_layer.stairs.pop(key, None)
            stair = dialog.get_stair()
            layer.stairs[key] = stair
            target_layer = self._scene.map_state.get_layer(stair.target_layer_id)
            if target_layer:
                target_layer.stairs[key] = type(stair)(
                    target_layer_id=layer.id,
                    label=stair.label,
                    source_layer_id=layer.id,
                )
            self._rebuild_scene()
            self.map_changed.emit()

    def _rebuild_scene(self) -> None:
        self._ruler.clear()
        self._annotations.invalidate()
        # Gizmo is a scene item — cleared by rebuild(); drop dangling ref.
        self._gizmo = None
        self._gizmo_dragging = False
        self._scene.rebuild()
        self._refresh_gizmo()

    def _emit_map_changed(self) -> None:
        self.map_changed.emit()
        self._refresh_gizmo()

    def _show_token_context_menu(self, item: TokenGraphicsItem) -> None:
        """Show token menu from the widget (not inside QGraphicsItem) — avoids Windows crash."""
        if not self._editable or self._impulse_combat.map_mode == "combat":
            return
        tid = item.token.token_id
        menu = QMenu(self)
        edit_act = menu.addAction("Edit...")
        delete_act = menu.addAction("Delete")
        stair_act = menu.addAction("Move via stair...")
        has_stair = bool(self._token_move_via_stair(item.token, choose_only=True))
        stair_act.setEnabled(has_stair)
        action = menu.exec(QCursor.pos())
        if action == edit_act:
            QTimer.singleShot(0, lambda: self._edit_token_by_id(tid))
        elif action == delete_act:
            QTimer.singleShot(0, lambda: self._delete_token_by_id(tid))
        elif action == stair_act:
            QTimer.singleShot(0, lambda: self._stair_token_by_id(tid))

    def _edit_token_by_id(self, token_id: str) -> None:
        item = self._scene._token_items.get(token_id)
        if item:
            self._edit_token_item(item)

    def _delete_token_by_id(self, token_id: str) -> None:
        item = self._scene._token_items.get(token_id)
        if item:
            self._delete_token_item(item)

    def _stair_token_by_id(self, token_id: str) -> None:
        placement = self._scene.token_state.placements.get(token_id)
        if placement:
            self._token_move_via_stair(placement, choose_only=False)

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
        self._category_panel.set_category(category)
        if category != EditorCategory.MAP:
            self._bg_selected = False
        modes = CATEGORY_MODES[category]
        if self._mode not in modes:
            self._set_mode(modes[0])
        else:
            self._apply_category_visibility()
            self._update_token_movability()
            self._refresh_gizmo()

    def _apply_category_visibility(self) -> None:
        self._category_panel.set_category(self._category)
        allowed = set(CATEGORY_MODES[self._category])
        for mode, btn in self._mode_buttons.items():
            btn.setVisible(mode in allowed)
        show_objects = self._category == EditorCategory.OBJECTS
        self._edge_btn.setVisible(show_objects)
        self._hex_btn.setVisible(show_objects)
        self._door_state_btn.setVisible(show_objects and self._mode == EditMode.DOOR)
        self._dialog_buttons["terrain"].setVisible(self._category == EditorCategory.TERRAIN)
        self._dialog_buttons["conditions"].setVisible(self._category == EditorCategory.TERRAIN)
        self._dialog_buttons["obstacle"].setVisible(show_objects)
        self._dialog_buttons["wall"].setVisible(show_objects)

    def _update_token_movability(self) -> None:
        # Token ItemIsMovable only when not using gizmo-driven Select transforms.
        token_movable = (
            self._editable
            and self._impulse_combat.map_mode != "combat"
            and self._category == EditorCategory.TOKENS
            and self._mode != EditMode.SELECT
        )
        self._scene.set_editable(token_movable)

    def _set_mode(self, mode: EditMode) -> None:
        if self._ruler.dragging:
            self._ruler.finish()
        # Keep current category when the mode is already valid there (SELECT is shared).
        if mode not in CATEGORY_MODES.get(self._category, []):
            for cat, modes in CATEGORY_MODES.items():
                if mode in modes:
                    self._category = cat
                    self._category_panel.set_category(cat)
                    break
        if self._category != EditorCategory.MAP:
            self._bg_selected = False
        self._mode = mode
        for m, btn in self._mode_buttons.items():
            btn.setChecked(m == mode)
        self._apply_category_visibility()
        self._update_token_movability()
        self._refresh_gizmo()

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
        self._sync_combat_toolbar_state(editable and not in_combat)
        self._category_panel.setVisible(editable and not in_combat)
        self._map_mode_panel.set_host(self._session_role != "guest")
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
        self._update_token_movability()
        self._toolbar.setVisible(not in_combat)
        self._sync_combat_toolbar_state(self._editable and not in_combat)
        self._category_panel.setVisible(self._editable and not in_combat)
        self._map_mode_panel.set_mode(state.map_mode)
        self._map_mode_panel.set_host(self._session_role != "guest")
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
        self._map_mode_panel.set_host(not is_guest)
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
        self._update_token_movability()
        self._toolbar.setVisible(not in_combat)
        self._sync_combat_toolbar_state(self._editable and not in_combat)
        self._category_panel.setVisible(self._editable and not in_combat)
        self._map_mode_panel.set_mode(mode)
        self._refresh_combat_ui()
        self._refresh_gizmo()

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
        layer = self._scene.map_state.get_active_layer()
        dialog = ConditionPaletteDialog(layer, parent=self)
        if dialog.exec():
            dialog.apply_to_layer()
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
        self._ruler.finish()
        self._scene._update_scene_rect()
        self._refresh_layer_combo()
        self._hide_inactive_check.setChecked(False)
        self._rebuild_scene()
        self._zoom_reset()
        self.map_changed.emit()

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self._position_category_panel()

    def showEvent(self, event) -> None:
        super().showEvent(event)
        QTimer.singleShot(0, self._position_category_panel)

    def _position_category_panel(self) -> None:
        if not hasattr(self, "_category_panel") or not hasattr(self, "_map_container"):
            return
        category_panel = self._category_panel
        category_panel.adjustSize()
        category_panel.move(8, max(8, self._map_container.height() - category_panel.height() - 8))
        category_panel.raise_()
        if hasattr(self, "_map_mode_panel"):
            mode_panel = self._map_mode_panel
            mode_panel.adjustSize()
            vbar = self._view.verticalScrollBar()
            hbar = self._view.horizontalScrollBar()
            right_inset = vbar.sizeHint().width() + 8 if vbar.isVisible() else 8
            bottom_inset = hbar.sizeHint().height() + 8 if hbar.isVisible() else 8
            mode_panel.move(
                max(8, self._map_container.width() - mode_panel.width() - right_inset),
                max(8, self._map_container.height() - mode_panel.height() - bottom_inset),
            )
            mode_panel.raise_()

    def _sync_combat_toolbar_state(self, editor_enabled: bool) -> None:
        self._toolbar.setEnabled(editor_enabled)
        self._mode_buttons[EditMode.RULER].setEnabled(True)

    def _window_opening_for_hex(self, q: int, r: int) -> Opening:
        layer = self._scene.map_state.get_active_layer()
        hex_wall = layer.walls.get(hex_wall_key(q, r))
        if hex_wall is None:
            return Opening(kind="window", state="closed", position=0.5)
        head_height = min(max(1.2, hex_wall.height - 0.3), hex_wall.height)
        sill_height = min(0.9, max(0.2, head_height - 0.6))
        return Opening(
            kind="window",
            state="open",
            position=0.5,
            sill_height=sill_height,
            head_height=head_height,
        )
