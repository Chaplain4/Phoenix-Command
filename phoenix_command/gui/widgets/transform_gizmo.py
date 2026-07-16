"""On-canvas transform gizmo: frame, scale handles, and rotate "shpaga"."""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum

from PyQt6.QtCore import QPointF, QRectF, Qt
from PyQt6.QtGui import QColor, QPainter, QPen, QTransform
from PyQt6.QtWidgets import QGraphicsItem


HANDLE_HALF = 5.0
ROTATE_OFFSET = 28.0
HIT_SLOP = 8.0


class HandleKind(str, Enum):
    BODY = "body"
    TL = "tl"
    TR = "tr"
    BL = "bl"
    BR = "br"
    T = "t"
    B = "b"
    L = "l"
    R = "r"
    ROTATE = "rotate"


@dataclass
class TransformState:
    """Oriented rect: center, size, rotation in degrees (Qt, clockwise-positive)."""

    cx: float
    cy: float
    width: float
    height: float
    rotation: float = 0.0

    def top_left(self) -> tuple[float, float]:
        return self.cx - self.width / 2.0, self.cy - self.height / 2.0


_CORNER_HANDLES = (HandleKind.TL, HandleKind.TR, HandleKind.BR, HandleKind.BL)
_EDGE_HANDLES = (HandleKind.T, HandleKind.R, HandleKind.B, HandleKind.L)

# Local-space unit offsets from center for each handle (before size scale).
_HANDLE_LOCAL: dict[HandleKind, tuple[float, float]] = {
    HandleKind.TL: (-0.5, -0.5),
    HandleKind.TR: (0.5, -0.5),
    HandleKind.BR: (0.5, 0.5),
    HandleKind.BL: (-0.5, 0.5),
    HandleKind.T: (0.0, -0.5),
    HandleKind.R: (0.5, 0.0),
    HandleKind.B: (0.0, 0.5),
    HandleKind.L: (-0.5, 0.0),
}


class TransformGizmoItem(QGraphicsItem):
    """Visual OBB with 8 scale handles and a left-side rotate handle."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._state = TransformState(0.0, 0.0, 40.0, 40.0)
        self._drag_kind: HandleKind | None = None
        self._drag_start_pos = QPointF()
        self._drag_start_state = TransformState(0.0, 0.0, 40.0, 40.0)
        self.setZValue(10000)
        self.setAcceptedMouseButtons(Qt.MouseButton.NoButton)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, False)

    def state(self) -> TransformState:
        return TransformState(
            self._state.cx,
            self._state.cy,
            self._state.width,
            self._state.height,
            self._state.rotation,
        )

    def set_state(self, state: TransformState) -> None:
        self.prepareGeometryChange()
        self._state = TransformState(
            state.cx, state.cy, max(1.0, state.width), max(1.0, state.height), state.rotation
        )
        self.update()

    def boundingRect(self) -> QRectF:
        pad = ROTATE_OFFSET + HANDLE_HALF + HIT_SLOP + 4
        half_w = self._state.width / 2.0 + pad
        half_h = self._state.height / 2.0 + pad
        diag = math.hypot(half_w, half_h)
        # Item lives at scene (0,0); paint draws in scene coords via cx/cy.
        return QRectF(self._state.cx - diag, self._state.cy - diag, diag * 2, diag * 2)

    def paint(self, painter: QPainter, option, widget=None) -> None:
        del option, widget
        painter.save()
        painter.translate(self._state.cx, self._state.cy)
        painter.rotate(self._state.rotation)
        w, h = self._state.width, self._state.height
        pen = QPen(QColor(80, 180, 255), 1.5)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRect(QRectF(-w / 2, -h / 2, w, h))

        # Rotate stem ("shpaga") from left mid-edge.
        lx = -w / 2
        painter.drawLine(QPointF(lx, 0), QPointF(lx - ROTATE_OFFSET, 0))
        self._draw_handle(painter, QPointF(lx - ROTATE_OFFSET, 0))

        for kind in (*_CORNER_HANDLES, *_EDGE_HANDLES):
            ox, oy = _HANDLE_LOCAL[kind]
            self._draw_handle(painter, QPointF(ox * w, oy * h))
        painter.restore()

    @staticmethod
    def _draw_handle(painter: QPainter, local: QPointF) -> None:
        painter.setBrush(QColor(80, 180, 255))
        painter.setPen(QPen(QColor(40, 100, 180), 1))
        painter.drawRect(
            QRectF(
                local.x() - HANDLE_HALF,
                local.y() - HANDLE_HALF,
                HANDLE_HALF * 2,
                HANDLE_HALF * 2,
            )
        )

    def _local_from_scene(self, scene_pos: QPointF) -> QPointF:
        t = QTransform()
        t.translate(self._state.cx, self._state.cy)
        t.rotate(self._state.rotation)
        inv, ok = t.inverted()
        if not ok:
            return QPointF()
        return inv.map(scene_pos)

    def _scene_from_local(self, local: QPointF, state: TransformState | None = None) -> QPointF:
        st = state or self._state
        t = QTransform()
        t.translate(st.cx, st.cy)
        t.rotate(st.rotation)
        return t.map(local)

    def handle_scene_pos(self, kind: HandleKind, state: TransformState | None = None) -> QPointF:
        st = state or self._state
        if kind == HandleKind.ROTATE:
            return self._scene_from_local(QPointF(-st.width / 2 - ROTATE_OFFSET, 0), st)
        if kind == HandleKind.BODY:
            return QPointF(st.cx, st.cy)
        ox, oy = _HANDLE_LOCAL[kind]
        return self._scene_from_local(QPointF(ox * st.width, oy * st.height), st)

    def hit_test(self, scene_pos: QPointF) -> HandleKind | None:
        local = self._local_from_scene(scene_pos)
        w, h = self._state.width, self._state.height
        rotate_local = QPointF(-w / 2 - ROTATE_OFFSET, 0)
        if math.hypot(local.x() - rotate_local.x(), local.y() - rotate_local.y()) <= HIT_SLOP:
            return HandleKind.ROTATE
        for kind in (*_CORNER_HANDLES, *_EDGE_HANDLES):
            ox, oy = _HANDLE_LOCAL[kind]
            hx, hy = ox * w, oy * h
            if abs(local.x() - hx) <= HIT_SLOP and abs(local.y() - hy) <= HIT_SLOP:
                return kind
        if abs(local.x()) <= w / 2 and abs(local.y()) <= h / 2:
            return HandleKind.BODY
        return None

    def begin_drag(self, kind: HandleKind, scene_pos: QPointF) -> None:
        self._drag_kind = kind
        self._drag_start_pos = QPointF(scene_pos)
        self._drag_start_state = self.state()

    def update_drag(self, scene_pos: QPointF) -> TransformState:
        if self._drag_kind is None:
            return self.state()
        kind = self._drag_kind
        start = self._drag_start_state
        if kind == HandleKind.BODY:
            dx = scene_pos.x() - self._drag_start_pos.x()
            dy = scene_pos.y() - self._drag_start_pos.y()
            new = TransformState(
                start.cx + dx, start.cy + dy, start.width, start.height, start.rotation
            )
            self.set_state(new)
            return new
        if kind == HandleKind.ROTATE:
            a0 = math.atan2(
                self._drag_start_pos.y() - start.cy,
                self._drag_start_pos.x() - start.cx,
            )
            a1 = math.atan2(scene_pos.y() - start.cy, scene_pos.x() - start.cx)
            delta_deg = math.degrees(a1 - a0)
            new = TransformState(
                start.cx, start.cy, start.width, start.height, start.rotation + delta_deg
            )
            self.set_state(new)
            return new
        new = self._scale_drag(kind, start, scene_pos)
        self.set_state(new)
        return new

    def end_drag(self) -> TransformState:
        self._drag_kind = None
        return self.state()

    def _scale_drag(
        self, kind: HandleKind, start: TransformState, scene_pos: QPointF
    ) -> TransformState:
        # Work in start-local space so opposite side stays fixed.
        t = QTransform()
        t.translate(start.cx, start.cy)
        t.rotate(start.rotation)
        inv, ok = t.inverted()
        if not ok:
            return start
        local = inv.map(scene_pos)

        min_size = 8.0
        left, right = -start.width / 2, start.width / 2
        top, bottom = -start.height / 2, start.height / 2

        if kind in _CORNER_HANDLES:
            # Opposite corner fixed; uniform scale keeping start aspect ratio.
            fx, fy = {
                HandleKind.TL: (right, bottom),
                HandleKind.TR: (left, bottom),
                HandleKind.BR: (left, top),
                HandleKind.BL: (right, top),
            }[kind]
            sx = abs(local.x() - fx) / start.width if start.width else 1.0
            sy = abs(local.y() - fy) / start.height if start.height else 1.0
            s = max(sx, sy, min_size / max(start.width, 1.0))
            new_w = max(min_size, start.width * s)
            new_h = max(min_size, start.height * s)
            if kind == HandleKind.TL:
                right, bottom = fx, fy
                left, top = right - new_w, bottom - new_h
            elif kind == HandleKind.TR:
                left, bottom = fx, fy
                right, top = left + new_w, bottom - new_h
            elif kind == HandleKind.BR:
                left, top = fx, fy
                right, bottom = left + new_w, top + new_h
            else:  # BL
                right, top = fx, fy
                left, bottom = right - new_w, top + new_h
        else:
            # Edge stretch: opposite edge fixed, one axis changes.
            if kind == HandleKind.L:
                left = min(local.x(), right - min_size)
            elif kind == HandleKind.R:
                right = max(local.x(), left + min_size)
            elif kind == HandleKind.T:
                top = min(local.y(), bottom - min_size)
            elif kind == HandleKind.B:
                bottom = max(local.y(), top + min_size)

        new_w = max(min_size, right - left)
        new_h = max(min_size, bottom - top)
        local_cx = (left + right) / 2.0
        local_cy = (top + bottom) / 2.0
        scene_center = t.map(QPointF(local_cx, local_cy))
        return TransformState(
            scene_center.x(),
            scene_center.y(),
            new_w,
            new_h,
            start.rotation,
        )
