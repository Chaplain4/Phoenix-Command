"""Helpers for annotation overlay editing on the hex map."""

from __future__ import annotations

import base64

from PyQt6.QtCore import QBuffer, QByteArray, QIODevice, QPointF, Qt
from PyQt6.QtGui import QBrush, QColor, QImage, QPainter, QPen, QPixmap
from PyQt6.QtWidgets import QGraphicsPixmapItem

from phoenix_command.gui.utils.hex_geometry import background_target_rect
from phoenix_command.gui.widgets.hex_map_modes import ANNOTATION_BRUSH_SIZE


class AnnotationOverlayController:
    """Manages annotation image, live preview, and persistence."""

    def __init__(self, scene):
        self._scene = scene
        self._annotate_image: QImage | None = None
        self._annotate_origin: tuple[float, float] = (0.0, 0.0)
        self._annotate_last: QPointF | None = None
        self._annotate_live_item: QGraphicsPixmapItem | None = None
        self._painting = False

    @property
    def painting(self) -> bool:
        return self._painting

    def clear_preview(self) -> None:
        if self._annotate_live_item is not None:
            self._scene.removeItem(self._annotate_live_item)
            self._annotate_live_item = None

    def invalidate(self) -> None:
        self.clear_preview()
        self._annotate_image = None
        self._annotate_last = None
        self._painting = False

    def ensure_image(self) -> tuple[QImage, float, float]:
        grid = self._scene.map_state.grid
        layer = self._scene.map_state.get_active_layer()
        bx, by, bw, bh = background_target_rect(grid)
        w, h = max(1, int(bw)), max(1, int(bh))
        if (
            self._annotate_image is not None
            and self._annotate_image.width() == w
            and self._annotate_image.height() == h
        ):
            return self._annotate_image, bx, by

        img = QImage(w, h, QImage.Format.Format_ARGB32_Premultiplied)
        img.fill(Qt.GlobalColor.transparent)
        if layer.annotations_b64:
            raw = base64.b64decode(layer.annotations_b64)
            loaded = QImage()
            if loaded.loadFromData(raw):
                img = loaded.convertToFormat(QImage.Format.Format_ARGB32_Premultiplied)
                if img.width() != w or img.height() != h:
                    img = img.scaled(
                        w,
                        h,
                        Qt.AspectRatioMode.IgnoreAspectRatio,
                        Qt.TransformationMode.SmoothTransformation,
                    )
        self._annotate_image = img
        self._annotate_origin = (bx, by)
        return img, bx, by

    def start_brush(self, x: float, y: float) -> None:
        img, bx, by = self.ensure_image()
        self._painting = True
        self._annotate_last = QPointF(x - bx, y - by)
        self._stamp(self._annotate_last.x(), self._annotate_last.y())
        self.refresh_preview()
        del img

    def continue_brush(self, x: float, y: float) -> None:
        if not self._painting or self._annotate_last is None:
            return
        bx, by = self._annotate_origin
        cur = QPointF(x - bx, y - by)
        self._stroke(self._annotate_last, cur)
        self._annotate_last = cur
        self.refresh_preview()

    def finish(self) -> bool:
        self._painting = False
        self._annotate_last = None
        if self._annotate_image is None:
            return False
        layer = self._scene.map_state.get_active_layer()
        ba = QByteArray()
        buf = QBuffer(ba)
        buf.open(QIODevice.OpenModeFlag.WriteOnly)
        self._annotate_image.save(buf, "PNG")
        buf.close()
        layer.annotations_b64 = base64.b64encode(bytes(ba)).decode("ascii")
        layer.annotations_mime = "image/png"
        self.clear_preview()
        return True

    def erase_rect(self, x0: float, y0: float, x1: float, y1: float) -> bool:
        img, bx, by = self.ensure_image()
        left = int(min(x0, x1) - bx)
        top = int(min(y0, y1) - by)
        width = max(1, int(abs(x1 - x0)))
        height = max(1, int(abs(y1 - y0)))
        painter = QPainter(img)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
        painter.fillRect(left, top, width, height, QColor(0, 0, 0, 0))
        painter.end()
        self.refresh_preview()
        return self.finish()

    def refresh_preview(self) -> None:
        if self._annotate_image is None:
            return
        if self._annotate_live_item is None:
            self._annotate_live_item = QGraphicsPixmapItem()
            layer = self._scene.map_state.get_active_layer()
            self._annotate_live_item.setOpacity(layer.opacity)
            self._annotate_live_item.setZValue(-49 + layer.elevation)
            self._scene.addItem(self._annotate_live_item)
        bx, by = self._annotate_origin
        self._annotate_live_item.setPos(bx, by)
        self._annotate_live_item.setPixmap(QPixmap.fromImage(self._annotate_image))

    def _stamp(self, lx: float, ly: float) -> None:
        if self._annotate_image is None:
            return
        painter = QPainter(self._annotate_image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)
        painter.setPen(
            QPen(
                QColor(20, 20, 20, 220),
                ANNOTATION_BRUSH_SIZE,
                Qt.PenStyle.SolidLine,
                Qt.PenCapStyle.RoundCap,
            )
        )
        painter.drawPoint(QPointF(lx, ly))
        painter.end()

    def _stroke(self, a: QPointF, b: QPointF) -> None:
        if self._annotate_image is None:
            return
        painter = QPainter(self._annotate_image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)
        painter.setPen(
            QPen(
                QColor(20, 20, 20, 220),
                ANNOTATION_BRUSH_SIZE,
                Qt.PenStyle.SolidLine,
                Qt.PenCapStyle.RoundCap,
            )
        )
        painter.drawLine(a, b)
        painter.end()
