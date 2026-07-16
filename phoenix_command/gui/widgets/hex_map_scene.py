"""Hex map scene: renders layers, backgrounds, annotations, and tokens."""

from __future__ import annotations

import base64

from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtGui import QBrush, QColor, QPen, QPixmap, QPolygonF, QTransform
from PyQt6.QtWidgets import (
    QGraphicsEllipseItem,
    QGraphicsItem,
    QGraphicsLineItem,
    QGraphicsPixmapItem,
    QGraphicsPolygonItem,
    QGraphicsScene,
    QGraphicsTextItem,
)

from phoenix_command.gui.utils.hex_geometry import (
    axial_to_pixel,
    background_target_rect,
    compute_background_layout,
    edge_endpoints,
    hex_corners,
    is_in_bounds,
    iter_rect_cells,
    pixel_to_axial,
    point_on_edge,
    rect_bounds_pixels,
)
from phoenix_command.gui.widgets.hex_map_modes import (
    HEX_WALL_ALPHA,
    OBSTACLE_ALPHA,
    TERRAIN_ALPHA,
)
from phoenix_command.gui.widgets.token_graphics import TokenGraphicsItem
from phoenix_command.session.domains.map_state import MapState, is_hex_wall_key
from phoenix_command.session.domains.token_state import TokenState

class HexMapScene(QGraphicsScene):
    """Scene that renders map layers."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.map_state = MapState()
        self.token_state = TokenState()
        self._token_items: dict[str, TokenGraphicsItem] = {}
        self._editable = True
        self._status_by_token: dict[str, str] = {}
        self._selected_token_id: str | None = None
        self.on_token_moved_callback = None
        self.on_token_edit_callback = None
        self.on_token_delete_callback = None
        self.on_token_stair_callback = None
        self.on_token_context_menu_callback = None

    def set_selected_token_id(self, token_id: str | None) -> None:
        self._selected_token_id = token_id
        for tid, item in self._token_items.items():
            item.set_token_selected(tid == token_id)

    def set_token_status(self, status_by_token: dict[str, str]) -> None:
        self._status_by_token = status_by_token

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

    def _add_annotations(self, layer, grid) -> None:
        if not layer.annotations_b64:
            return
        raw = base64.b64decode(layer.annotations_b64)
        pixmap = QPixmap()
        if not pixmap.loadFromData(raw):
            return
        bx, by, bw, bh = background_target_rect(grid)
        item = QGraphicsPixmapItem(pixmap)
        item.setPos(bx, by)
        if pixmap.width() != int(bw) or pixmap.height() != int(bh):
            item.setPixmap(
                pixmap.scaled(
                    int(bw),
                    int(bh),
                    Qt.AspectRatioMode.IgnoreAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
        item.setOpacity(layer.opacity)
        item.setZValue(-50 + layer.elevation)
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
            self._add_annotations(layer, grid)

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

            for key, cond in layer.conditions.items():
                q, r = map(int, key.split(","))
                if not is_in_bounds(q, r, grid):
                    continue
                corners = hex_corners(q, r, grid)
                poly = QPolygonF([QPointF(x, y) for x, y in corners])
                color = QColor(180, 80, 220, int(layer.opacity * 80))
                item = QGraphicsPolygonItem(poly)
                item.setBrush(QBrush(color))
                item.setPen(QPen(QColor(120, 40, 160, 120), 1))
                item.setZValue(layer.elevation + 0.5)
                vis = ", ".join(cond.visibility) if cond.visibility else "clear"
                item.setToolTip(f"Conditions: {vis}")
                self.addItem(item)

            for key, obstacle in layer.obstacles.items():
                q, r = map(int, key.split(","))
                if not is_in_bounds(q, r, grid):
                    continue
                corners = hex_corners(q, r, grid)
                poly = QPolygonF([QPointF(x, y) for x, y in corners])
                color = QColor(120, 60, 20, int(layer.opacity * OBSTACLE_ALPHA))
                item = QGraphicsPolygonItem(poly)
                item.setBrush(QBrush(color))
                item.setPen(QPen(QColor(60, 30, 10), 2))
                item.setToolTip(obstacle.tooltip_text(custom))
                item.setZValue(layer.elevation + 2)
                self.addItem(item)
                cx, cy = axial_to_pixel(q, r, grid)
                label = QGraphicsTextItem(f"H{obstacle.height:.1f}")
                label.setPos(cx - 10, cy - 8)
                label.setZValue(layer.elevation + 3)
                self.addItem(label)

            for key, wall in layer.walls.items():
                if is_hex_wall_key(key):
                    coords = key.rsplit(":", 1)[0]
                    q, r = map(int, coords.split(","))
                    if not is_in_bounds(q, r, grid):
                        continue
                    corners = hex_corners(q, r, grid)
                    poly = QPolygonF([QPointF(x, y) for x, y in corners])
                    color = QColor(50, 50, 55, int(layer.opacity * HEX_WALL_ALPHA))
                    item = QGraphicsPolygonItem(poly)
                    item.setBrush(QBrush(color))
                    item.setPen(QPen(QColor(20, 20, 20), 2))
                    item.setToolTip(wall.tooltip_text(custom))
                    item.setZValue(layer.elevation + 2.5)
                    self.addItem(item)
                    continue
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
                    color = QColor(100, 200, 255) if opening.kind == "window" else QColor(200, 150, 50)
                    if opening.kind == "door":
                        if opening.state == "open":
                            color = QColor(100, 255, 100)
                        elif opening.state == "locked":
                            color = QColor(255, 80, 80)
                    if opening.kind == "window":
                        start_pos = max(0.1, opening.position - 0.18)
                        end_pos = min(0.9, opening.position + 0.18)
                        wx0, wy0 = point_on_edge(q, r, edge, start_pos, grid)
                        wx1, wy1 = point_on_edge(q, r, edge, end_pos, grid)
                        marker = QGraphicsLineItem(wx0, wy0, wx1, wy1)
                        marker.setPen(QPen(color, 4))
                    else:
                        px, py = point_on_edge(q, r, edge, opening.position, grid)
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
                status_text=self._status_by_token.get(tid, ""),
                selected=(tid == self._selected_token_id),
                on_context_menu=self.on_token_context_menu_callback,
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


