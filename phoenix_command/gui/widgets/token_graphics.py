"""Token graphics item for the hex map."""

from __future__ import annotations

import base64

from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtGui import QBrush, QColor, QFont, QPen, QPixmap, QPolygonF
from PyQt6.QtWidgets import (
    QGraphicsEllipseItem,
    QGraphicsItem,
    QGraphicsPixmapItem,
    QGraphicsPolygonItem,
    QGraphicsTextItem,
)

from phoenix_command.gui.utils.hex_geometry import facing_to_degrees
from phoenix_command.session.domains.token_state import TokenPlacement


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
        status_text: str = "",
        selected: bool = False,
        on_context_menu=None,
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
        self._on_context_menu = on_context_menu
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, editable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setAcceptHoverEvents(editable)
        self._load_pixmap()
        base = token.label or token.character_name or ""
        self._label = QGraphicsTextItem(base, self)
        self._label.setDefaultTextColor(QColor("white"))
        self._label.setAcceptedMouseButtons(Qt.MouseButton.NoButton)
        font = QFont()
        font.setPointSize(8)
        self._label.setFont(font)
        self._label.setPos(-20, self._grid_size * token.size)
        self._status = None
        if status_text:
            self.setToolTip(status_text)
            self._status = QGraphicsTextItem(status_text, self)
            self._status.setDefaultTextColor(QColor(200, 255, 200))
            self._status.setAcceptedMouseButtons(Qt.MouseButton.NoButton)
            sf = QFont()
            sf.setPointSize(6)
            self._status.setFont(sf)
            self._status.setPos(-24, self._grid_size * token.size + 14)
        self._selection_ring = self._make_selection_ring()
        self._facing_arrow = self._make_facing_arrow()
        self._apply_facing()
        self.set_token_selected(selected)

    def _make_selection_ring(self) -> QGraphicsEllipseItem:
        w = self.pixmap().width()
        h = self.pixmap().height()
        pad = 4
        ring = QGraphicsEllipseItem(-pad, -pad, w + pad * 2, h + pad * 2, self)
        ring.setPen(QPen(QColor(255, 220, 0), 3))
        ring.setBrush(QBrush(QColor(0, 0, 0, 0)))
        ring.setZValue(10)
        ring.setVisible(False)
        ring.setAcceptedMouseButtons(Qt.MouseButton.NoButton)
        return ring

    def _make_facing_arrow(self) -> QGraphicsPolygonItem:
        size = self._grid_size * self.token.size * 0.45
        tri = QPolygonF([
            QPointF(0, -size * 1.4),
            QPointF(-size * 0.55, 0),
            QPointF(size * 0.55, 0),
        ])
        arrow = QGraphicsPolygonItem(tri, self)
        arrow.setBrush(QBrush(QColor(255, 220, 0)))
        arrow.setPen(QPen(QColor(80, 60, 0), 1))
        arrow.setPos(self.pixmap().width() / 2, self.pixmap().height() / 2)
        arrow.setZValue(20)
        arrow.setAcceptedMouseButtons(Qt.MouseButton.NoButton)
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
        # Hit-test opaque pixels only so transparent corners don't steal clicks
        self.setShapeMode(QGraphicsPixmapItem.ShapeMode.MaskShape)

    def _apply_facing(self):
        self.setTransformOriginPoint(self.boundingRect().center())
        self.setRotation(facing_to_degrees(self.token.facing, self._orientation))
        if self._facing_arrow:
            self._facing_arrow.setPos(self.pixmap().width() / 2, self.pixmap().height() / 2)

    def set_token_selected(self, selected: bool) -> None:
        self.setSelected(selected)
        if self._selection_ring:
            self._selection_ring.setVisible(selected)
        if self._facing_arrow:
            color = QColor(255, 240, 80) if selected else QColor(255, 220, 0)
            self._facing_arrow.setBrush(QBrush(color))
            self._facing_arrow.setPen(QPen(QColor(80, 60, 0), 2 if selected else 1))

    def apply_facing_delta(self, delta: int) -> None:
        self.token.facing = (self.token.facing + delta) % 12
        self._apply_facing()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if event.button() == Qt.MouseButton.LeftButton and self._on_moved:
            self._on_moved(self)

    def mouseDoubleClickEvent(self, event):
        if self._editable and self._on_edit:
            self._on_edit(self)
            event.accept()
            return
        super().mouseDoubleClickEvent(event)

    def contextMenuEvent(self, event):
        """Defer menu to HexMapView — nested QMenu.exec here crashes on Windows."""
        if not self._editable:
            event.ignore()
            return
        event.accept()
        if self._on_context_menu:
            self._on_context_menu(self)
