"""Transient ruler overlay for the hex map."""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QColor, QPen
from PyQt6.QtWidgets import QGraphicsEllipseItem, QGraphicsItem, QGraphicsLineItem, QGraphicsTextItem

from phoenix_command.gui.utils.hex_geometry import axial_distance, axial_to_pixel


class RulerOverlayController:
    """Tracks and renders a drag-to-measure ruler."""

    def __init__(self, scene):
        self._scene = scene
        self._drag = False
        self._start: tuple[int, int] | None = None
        self._end: tuple[int, int] | None = None
        self._items: list[QGraphicsItem] = []

    @property
    def dragging(self) -> bool:
        return self._drag

    @property
    def start(self) -> tuple[int, int] | None:
        return self._start

    def begin(self, q: int, r: int) -> None:
        self._drag = True
        self._start = (q, r)
        self._end = (q, r)
        self.draw()

    def update(self, q: int, r: int) -> None:
        if not self._drag or self._start is None:
            return
        self._end = (q, r)
        self.draw()

    def finish(self) -> None:
        self._drag = False
        self._start = None
        self._end = None
        self.clear()

    def clear(self) -> None:
        for item in self._items:
            self._scene.removeItem(item)
        self._items.clear()

    def draw(self) -> None:
        self.clear()
        if not self._drag or self._start is None or self._end is None:
            return
        grid = self._scene.map_state.grid
        q0, r0 = self._start
        q1, r1 = self._end
        x0, y0 = axial_to_pixel(q0, r0, grid)
        x1, y1 = axial_to_pixel(q1, r1, grid)
        dist = axial_distance(q0, r0, q1, r1)
        meters = dist * grid.meters_per_hex
        label = f"{dist} hex / {meters:.1f} m"

        line = QGraphicsLineItem(x0, y0, x1, y1)
        line.setPen(QPen(QColor(255, 200, 0), 2, Qt.PenStyle.DashLine))
        line.setZValue(2000)
        self._scene.addItem(line)
        self._items.append(line)

        for px, py in ((x0, y0), (x1, y1)):
            marker = QGraphicsEllipseItem(px - 4, py - 4, 8, 8)
            marker.setBrush(QBrush(QColor(255, 200, 0)))
            marker.setPen(QPen(QColor(0, 0, 0), 1))
            marker.setZValue(2000)
            self._scene.addItem(marker)
            self._items.append(marker)

        mid_x = (x0 + x1) / 2
        mid_y = (y0 + y1) / 2
        text = QGraphicsTextItem(label)
        text.setPos(mid_x + 5, mid_y - 15)
        text.setDefaultTextColor(QColor(255, 220, 0))
        text.setZValue(2001)
        self._scene.addItem(text)
        self._items.append(text)
