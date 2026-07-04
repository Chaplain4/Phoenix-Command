"""Hex map view and editor widget."""

from __future__ import annotations

import base64
from enum import Enum

from PyQt6.QtCore import QPointF, Qt, pyqtSignal
from PyQt6.QtGui import (
    QBrush,
    QColor,
    QFont,
    QPainter,
    QPen,
    QPixmap,
    QPolygonF,
    QTransform,
    QWheelEvent,
)
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QGraphicsEllipseItem,
    QGraphicsItem,
    QGraphicsLineItem,
    QGraphicsPixmapItem,
    QGraphicsPolygonItem,
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsTextItem,
    QGraphicsView,
    QLabel,
    QMenu,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from phoenix_command.gui.widgets.wrapping_toolbar import WrappingToolbar

from phoenix_command.gui.dialogs.map_dialogs import (
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
    compute_background_layout,
    edge_endpoints,
    facing_to_degrees,
    hex_corners,
    is_in_bounds,
    iter_offset_rect,
    iter_rect_cells,
    nearest_edge,
    pixel_to_axial,
    pixel_to_offset,
    point_on_edge,
    rect_bounds_pixels,
)
from phoenix_command.session.domains.map_state import (
    LayerStair,
    MapState,
    Obstacle,
    Opening,
    TerrainTile,
    WallSegment,
)
from phoenix_command.session.domains.token_state import TokenPlacement, TokenState
from phoenix_command.tables.catalogs.movement_catalog import TERRAIN_PRESETS

ZOOM_MIN = 0.2
ZOOM_MAX = 5.0
ZOOM_STEP = 1.15
TERRAIN_ALPHA = 120


class EditMode(str, Enum):
    SELECT = "select"
    TERRAIN = "terrain"
    OBSTACLE = "obstacle"
    WALL = "wall"
    WINDOW = "window"
    DOOR = "door"
    TOKEN = "token"
    STAIR = "stair"
    RULER = "ruler"
    ERASER = "eraser"


class TokenGraphicsItem(QGraphicsPixmapItem):
    """Draggable token on the map."""

    def __init__(
        self,
        token: TokenPlacement,
        grid_size: float,
        orientation: str,
        editable: bool,
        on_moved,
        on_edit,
        on_delete,
        on_stair,
    ):
        super().__init__()
        self.token = token
        self._grid_size = grid_size
        self._orientation = orientation
        self._editable = editable
        self._on_moved = on_moved
        self._on_edit = on_edit
        self._on_delete = on_delete
        self._on_stair = on_stair
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, editable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setAcceptHoverEvents(editable)
        self._load_pixmap()
        self._label = QGraphicsTextItem(token.label or token.character_name or "", self)
        self._label.setDefaultTextColor(QColor("white"))
        font = QFont()
        font.setPointSize(8)
        self._label.setFont(font)
        self._label.setPos(-20, self._grid_size * token.size)
        self._facing_arrow = self._make_facing_arrow()
        self._apply_facing()

    def _make_facing_arrow(self) -> QGraphicsPolygonItem:
        size = self._grid_size * self.token.size * 0.35
        tri = QPolygonF([
            QPointF(0, -size),
            QPointF(-size * 0.5, 0),
            QPointF(size * 0.5, 0),
        ])
        arrow = QGraphicsPolygonItem(tri, self)
        arrow.setBrush(QBrush(QColor(255, 220, 0)))
        arrow.setPen(QPen(QColor(80, 60, 0), 1))
        arrow.setPos(self.pixmap().width() / 2, self.pixmap().height() / 2)
        return arrow

    def _load_pixmap(self):
        if self.token.image_b64:
            raw = base64.b64decode(self.token.image_b64)
            pixmap = QPixmap()
            pixmap.loadFromData(raw)
            size = int(self._grid_size * 2 * self.token.size)
            self.setPixmap(pixmap.scaled(size, size, Qt.AspectRatioMode.KeepAspectRatio,
                                         Qt.TransformationMode.SmoothTransformation))
        else:
            size = int(self._grid_size * 2 * self.token.size)
            pixmap = QPixmap(size, size)
            pixmap.fill(QColor("#4a90e2"))
            self.setPixmap(pixmap)

    def _apply_facing(self):
        self.setTransformOriginPoint(self.boundingRect().center())
        self.setRotation(facing_to_degrees(self.token.facing, self._orientation))
        if self._facing_arrow:
            self._facing_arrow.setPos(self.pixmap().width() / 2, self.pixmap().height() / 2)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if self._on_moved:
            self._on_moved(self)

    def mouseDoubleClickEvent(self, event):
        if self._editable and self._on_edit:
            self._on_edit(self)
            event.accept()
            return
        super().mouseDoubleClickEvent(event)

    def contextMenuEvent(self, event):
        if not self._editable:
            return
        menu = QMenu()
        edit_act = menu.addAction("Edit...")
        delete_act = menu.addAction("Delete")
        stair_act = menu.addAction("Move via stair...")
        stair_act.setEnabled(bool(self._on_stair and self._on_stair(self.token, choose_only=True)))
        action = menu.exec(event.screenPos())
        if action == edit_act and self._on_edit:
            self._on_edit(self)
        elif action == delete_act and self._on_delete:
            self._on_delete(self)
        elif action == stair_act and self._on_stair:
            self._on_stair(self.token, choose_only=False)


class HexMapScene(QGraphicsScene):
    """Scene that renders map layers."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.map_state = MapState()
        self.token_state = TokenState()
        self._token_items: dict[str, TokenGraphicsItem] = {}
        self._editable = True
        self.on_token_moved_callback = None
        self.on_token_edit_callback = None
        self.on_token_delete_callback = None
        self.on_token_stair_callback = None

    def set_editable(self, editable: bool) -> None:
        self._editable = editable
        for item in self._token_items.values():
            item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, editable)

    def set_map_state(self, map_state: MapState) -> None:
        self.map_state = map_state
        self.map_state.ensure_default_layer()
        self._update_scene_rect()
        self.rebuild()

    def _update_scene_rect(self) -> None:
        min_x, min_y, max_x, max_y = rect_bounds_pixels(self.map_state.grid)
        margin = self.map_state.grid.size * 2
        self.setSceneRect(min_x - margin, min_y - margin,
                          max_x - min_x + 2 * margin, max_y - min_y + 2 * margin)

    def set_token_state(self, token_state: TokenState) -> None:
        self.token_state = token_state
        self.rebuild()

    def _add_background(self, layer, grid) -> None:
        if not layer.background or not layer.background.data_b64:
            return
        raw = base64.b64decode(layer.background.data_b64)
        pixmap = QPixmap()
        pixmap.loadFromData(raw)
        bg = layer.background
        dest_w, dest_h, pos_x, pos_y = compute_background_layout(
            bg.fit_mode,
            pixmap.width(),
            pixmap.height(),
            grid,
            scale_x=bg.scale_x,
            scale_y=bg.scale_y,
            offset_x=bg.offset_x,
            offset_y=bg.offset_y,
        )
        if dest_w <= 0 or dest_h <= 0:
            return
        scaled = pixmap.scaled(
            int(dest_w),
            int(dest_h),
            Qt.AspectRatioMode.IgnoreAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        item = QGraphicsPixmapItem(scaled)
        item.setPos(pos_x, pos_y)
        item.setOpacity(bg.opacity)
        if bg.rotation:
            center = QPointF(pos_x + dest_w / 2, pos_y + dest_h / 2)
            transform = QTransform()
            transform.translate(center.x(), center.y())
            transform.rotate(bg.rotation)
            transform.translate(-center.x(), -center.y())
            item.setTransform(transform)
        item.setZValue(-100 + layer.elevation)
        self.addItem(item)

    def rebuild(self) -> None:
        self.clear()
        self._token_items.clear()
        grid = self.map_state.grid
        active = self.map_state.get_active_layer()
        custom = self.map_state.custom_barriers
        hide_inactive = self.map_state.hide_inactive_layers

        for layer in sorted(self.map_state.layers, key=lambda layer: layer.elevation):
            if not layer.visible:
                continue
            if hide_inactive and layer.id != active.id:
                continue
            layer_alpha = int(layer.opacity * 255)
            is_active = layer.id == active.id
            terrain_alpha = int(layer.opacity * TERRAIN_ALPHA) if is_active else int(layer.opacity * TERRAIN_ALPHA // 2)

            self._add_background(layer, grid)

            for key, tile in layer.terrain.items():
                q, r = map(int, key.split(","))
                if not is_in_bounds(q, r, grid):
                    continue
                corners = hex_corners(q, r, grid)
                poly = QPolygonF([QPointF(x, y) for x, y in corners])
                color = QColor(tile.color)
                color.setAlpha(terrain_alpha)
                item = QGraphicsPolygonItem(poly)
                item.setBrush(QBrush(color))
                item.setPen(QPen(QColor(80, 80, 80, 60), 1))
                item.setZValue(layer.elevation)
                self.addItem(item)
                if tile.movement_cost > 0:
                    cx, cy = axial_to_pixel(q, r, grid)
                    text = QGraphicsTextItem(str(tile.movement_cost))
                    text.setPos(cx - 5, cy - 8)
                    text.setDefaultTextColor(QColor(0, 0, 0, 200))
                    text.setZValue(layer.elevation + 1)
                    self.addItem(text)

            for key, obstacle in layer.obstacles.items():
                q, r = map(int, key.split(","))
                if not is_in_bounds(q, r, grid):
                    continue
                cx, cy = axial_to_pixel(q, r, grid)
                size = grid.size * 0.6
                item = QGraphicsEllipseItem(cx - size / 2, cy - size / 2, size, size)
                item.setBrush(QBrush(QColor(120, 60, 20, layer_alpha)))
                item.setPen(QPen(QColor(60, 30, 10), 2))
                item.setToolTip(obstacle.tooltip_text(custom))
                item.setZValue(layer.elevation + 2)
                self.addItem(item)
                label = QGraphicsTextItem(f"H{obstacle.height:.1f}")
                label.setPos(cx - 10, cy - 8)
                label.setZValue(layer.elevation + 3)
                self.addItem(label)

            for key, wall in layer.walls.items():
                coords, edge_s = key.rsplit(":", 1)
                q, r = map(int, coords.split(","))
                if not is_in_bounds(q, r, grid):
                    continue
                edge = int(edge_s)
                start, end = edge_endpoints(q, r, edge, grid)
                line = QGraphicsLineItem(start[0], start[1], end[0], end[1])
                pen = QPen(QColor(40, 40, 40, layer_alpha), 4)
                line.setPen(pen)
                line.setToolTip(wall.tooltip_text(custom))
                line.setZValue(layer.elevation + 4)
                self.addItem(line)
                for opening in wall.openings:
                    px, py = point_on_edge(q, r, edge, opening.position, grid)
                    color = QColor(100, 200, 255) if opening.kind == "window" else QColor(200, 150, 50)
                    if opening.kind == "door":
                        if opening.state == "open":
                            color = QColor(100, 255, 100)
                        elif opening.state == "locked":
                            color = QColor(255, 80, 80)
                    marker = QGraphicsEllipseItem(px - 4, py - 4, 8, 8)
                    marker.setBrush(QBrush(color))
                    marker.setPen(QPen(QColor(0, 0, 0), 1))
                    marker.setZValue(layer.elevation + 5)
                    self.addItem(marker)

            for key, stair in layer.stairs.items():
                q, r = map(int, key.split(","))
                if not is_in_bounds(q, r, grid):
                    continue
                cx, cy = axial_to_pixel(q, r, grid)
                size = grid.size * 0.45
                item = QGraphicsPolygonItem(self._stair_polygon(cx, cy, size))
                item.setBrush(QBrush(QColor(180, 100, 255, layer_alpha)))
                item.setPen(QPen(QColor(80, 40, 120), 2))
                target = self.map_state.get_layer(stair.target_layer_id)
                target_name = target.name if target else stair.target_layer_id
                tip = stair.label or f"Stair → {target_name}"
                item.setToolTip(tip)
                item.setZValue(layer.elevation + 2)
                self.addItem(item)
                label = QGraphicsTextItem("⇅")
                label.setPos(cx - 6, cy - 10)
                label.setDefaultTextColor(QColor(255, 255, 255))
                label.setZValue(layer.elevation + 3)
                self.addItem(label)

        for tid, token in self.token_state.placements.items():
            if token.layer_id and token.layer_id != active.id:
                continue
            if not is_in_bounds(token.q, token.r, grid):
                continue
            cx, cy = axial_to_pixel(token.q, token.r, grid)
            item = TokenGraphicsItem(
                token,
                grid.size,
                grid.orientation,
                self._editable,
                self._on_token_moved,
                self.on_token_edit_callback,
                self.on_token_delete_callback,
                self.on_token_stair_callback,
            )
            item.setPos(cx - item.pixmap().width() / 2, cy - item.pixmap().height() / 2)
            item.setZValue(1000)
            self.addItem(item)
            self._token_items[tid] = item

        self._draw_grid()

    @staticmethod
    def _stair_polygon(cx: float, cy: float, size: float) -> QPolygonF:
        return QPolygonF([
            QPointF(cx - size, cy + size * 0.3),
            QPointF(cx + size, cy + size * 0.3),
            QPointF(cx + size * 0.5, cy - size),
            QPointF(cx - size * 0.5, cy - size),
        ])

    def _draw_grid(self) -> None:
        grid = self.map_state.grid
        for q, r in iter_rect_cells(grid):
            corners = hex_corners(q, r, grid)
            poly = QPolygonF([QPointF(x, y) for x, y in corners])
            item = QGraphicsPolygonItem(poly)
            item.setBrush(QBrush(QColor(0, 0, 0, 0)))
            item.setPen(QPen(QColor(100, 100, 100, 80), 1))
            item.setZValue(500)
            self.addItem(item)

    def _on_token_moved(self, item: TokenGraphicsItem) -> None:
        grid = self.map_state.grid
        cx = item.pos().x() + item.pixmap().width() / 2
        cy = item.pos().y() + item.pixmap().height() / 2
        q, r = pixel_to_axial(cx, cy, grid)
        if not is_in_bounds(q, r, grid):
            q, r = item.token.q, item.token.r
        item.token.q = q
        item.token.r = r
        px, py = axial_to_pixel(q, r, grid)
        item.setPos(px - item.pixmap().width() / 2, py - item.pixmap().height() / 2)
        if item.token.token_id in self.token_state.placements:
            self.token_state.placements[item.token.token_id] = item.token
        if self.on_token_moved_callback:
            self.on_token_moved_callback()


class HexMapView(QWidget):
    """Hex map editor widget with toolbar."""

    map_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._mode = EditMode.SELECT
        self._terrain_preset = "open"
        self._obstacle_template = Obstacle()
        self._wall_template = WallSegment()
        self._door_state = "closed"
        self._editable = True
        self._character_names: list[str] = []
        self._zoom = 1.0

        # Drag-paint state
        self._painting = False
        self._last_cell: tuple[int, int] | None = None
        self._last_edge: tuple[str, int] | None = None
        self._dirty = False

        # Rubber-band terrain state
        self._terrain_drag = False
        self._terrain_start: tuple[int, int] | None = None
        self._terrain_end: tuple[int, int] | None = None
        self._rubber_band: QGraphicsRectItem | None = None

        # Middle-button pan state
        self._panning = False
        self._pan_start = QPointF()

        # Ruler state (transient overlay while LMB held)
        self._ruler_drag = False
        self._ruler_start: tuple[int, int] | None = None
        self._ruler_end: tuple[int, int] | None = None
        self._ruler_items: list[QGraphicsItem] = []

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
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._toolbar)
        layout.addWidget(self._view)

        self._scene.map_state.ensure_default_layer()
        self._scene._update_scene_rect()
        self._rebuild_scene()

    def _setup_toolbar(self) -> None:
        self._toolbar = WrappingToolbar()
        modes = [
            ("Select", EditMode.SELECT),
            ("Terrain", EditMode.TERRAIN),
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
        for label, mode in modes:
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, m=mode: self._set_mode(m))
            self._toolbar.add_widget(btn)
            self._mode_buttons[mode] = btn
        self._mode_buttons[EditMode.SELECT].setChecked(True)

        self._toolbar.add_separator()
        self._layer_combo = QComboBox()
        self._layer_combo.currentIndexChanged.connect(self._on_layer_changed)
        self._toolbar.add_widget(QLabel("Layer:"))
        self._toolbar.add_widget(self._layer_combo)

        self._hide_inactive_check = QCheckBox("Hide inactive")
        self._hide_inactive_check.toggled.connect(self._on_hide_inactive_toggled)
        self._toolbar.add_widget(self._hide_inactive_check)

        for label, slot in [
            ("Layers...", self._open_layer_manager),
            ("Terrain...", self._open_terrain_palette),
            ("Obstacle...", self._open_obstacle_dialog),
            ("Wall...", self._open_wall_dialog),
            ("Map Size...", self._open_map_size_dialog),
        ]:
            btn = QPushButton(label)
            btn.clicked.connect(slot)
            self._toolbar.add_widget(btn)

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
            if event.button() == Qt.MouseButton.LeftButton and self._editable:
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
            if self._editable and (self._painting or self._terrain_drag or self._ruler_drag):
                pos = self._view.mapToScene(event.position().toPoint())
                return self._on_lmb_move(pos.x(), pos.y())

        if et == event.Type.MouseButtonRelease:
            if event.button() == Qt.MouseButton.MiddleButton and self._panning:
                self._panning = False
                return True
            if event.button() == Qt.MouseButton.LeftButton and self._editable:
                return self._on_lmb_release()

        return super().eventFilter(obj, event)

    def wheelEvent(self, event: QWheelEvent) -> None:
        super().wheelEvent(event)

    # --- Mouse handlers ---

    def _on_lmb_press(self, x: float, y: float) -> bool:
        grid = self._scene.map_state.grid
        q, r = pixel_to_axial(x, y, grid)
        if not is_in_bounds(q, r, grid):
            return True

        if self._mode == EditMode.TERRAIN:
            col, row = pixel_to_offset(x, y, grid)
            self._terrain_drag = True
            self._terrain_start = (col, row)
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

        if self._mode in (EditMode.OBSTACLE, EditMode.WALL, EditMode.WINDOW,
                          EditMode.DOOR, EditMode.ERASER):
            self._painting = True
            self._dirty = False
            self._last_cell = None
            self._last_edge = None
            self._paint_at(x, y, q, r)
            return True

        return False

    def _on_lmb_move(self, x: float, y: float) -> bool:
        grid = self._scene.map_state.grid

        if self._terrain_drag and self._terrain_start is not None:
            col, row = pixel_to_offset(x, y, grid)
            c0, r0 = self._terrain_start
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
        if self._terrain_drag and self._terrain_start is not None:
            self._remove_rubber_band()
            c0, r0 = self._terrain_start
            c1, r1 = self._terrain_end if self._terrain_end else self._terrain_start
            self._fill_terrain_rect(c0, r0, c1, r1)
            self._terrain_drag = False
            self._terrain_start = None
            self._terrain_end = None
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
        self._terrain_end = (c1, r1)
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
        if self._mode in (EditMode.OBSTACLE, EditMode.ERASER) and self._last_cell == (q, r):
            return

        grid = self._scene.map_state.grid
        layer = self._scene.map_state.get_active_layer()
        key = f"{q},{r}"

        if self._mode == EditMode.OBSTACLE:
            layer.obstacles[key] = Obstacle(
                height=self._obstacle_template.height,
                material=self._obstacle_template.material,
                thickness=self._obstacle_template.thickness,
                protection_factor=self._obstacle_template.protection_factor,
                blocks_movement=self._obstacle_template.blocks_movement,
                blocks_los=self._obstacle_template.blocks_los,
            )
            self._last_cell = (q, r)
            self._dirty = True
            self._rebuild_scene()

        elif self._mode == EditMode.WALL:
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

        elif self._mode == EditMode.ERASER:
            if self._last_cell == (q, r):
                return
            layer.terrain.pop(key, None)
            layer.obstacles.pop(key, None)
            layer.stairs.pop(key, None)
            edge = nearest_edge(x, y, q, r, grid)
            layer.walls.pop(f"{q},{r}:{edge}", None)
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

    def _place_token(self, q: int, r: int) -> None:
        import uuid
        layer = self._scene.map_state.get_active_layer()
        dialog = TokenDialog(
            character_names=self._character_names,
            grid_orientation=self._scene.map_state.grid.orientation,
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
        self._scene.token_state.placements.pop(item.token.token_id, None)
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

    def _set_mode(self, mode: EditMode) -> None:
        if self._ruler_drag:
            self._ruler_drag = False
            self._ruler_start = None
            self._ruler_end = None
            self._clear_ruler_overlay()
        self._mode = mode
        for m, btn in self._mode_buttons.items():
            btn.setChecked(m == mode)

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
        self._scene.set_editable(editable)
        self._toolbar.setEnabled(editable)

    def set_character_names(self, names: list[str]) -> None:
        self._character_names = names

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
