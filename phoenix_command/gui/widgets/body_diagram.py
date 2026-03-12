"""Body diagram visualization widget for Phoenix Command.

Draws a human body outline with highlighted hit zones, armor coverage,
and support for front/rear views and target orientations.
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                              QLabel, QToolTip, QSizePolicy)
from PyQt6.QtGui import (QPainter, QColor, QPen, QBrush, QPolygonF, QPainterPath,
                          QFont)
from PyQt6.QtCore import Qt, QPointF, QRectF, pyqtSignal

from phoenix_command.models.enums import AdvancedHitLocation, TargetExposure, TargetOrientation
from phoenix_command.gui.widgets.body_zones import BODY_ZONES, BodyZone, LOCATION_TO_ZONE

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from phoenix_command.models.character import Character


# ── Color helpers ──────────────────────────────────────────────────────
def _damage_color(damage: int, max_damage: int = 200) -> QColor:
    """Map damage value to a color gradient: green → yellow → red."""
    if damage <= 0:
        return QColor(200, 200, 200, 60)  # transparent grey (no hit)
    ratio = min(damage / max_damage, 1.0)
    if ratio < 0.5:
        # green → yellow
        t = ratio * 2
        r = int(46 + (241 - 46) * t)
        g = int(204 + (196 - 204) * t)
        b = int(113 + (15 - 113) * t)
    else:
        # yellow → red
        t = (ratio - 0.5) * 2
        r = int(241 + (231 - 241) * t)
        g = int(196 + (76 - 196) * t)
        b = int(15 + (60 - 15) * t)
    return QColor(r, g, b, 180)


def _armor_color(protection: float) -> QColor:
    """Map armor protection to a blue shade."""
    if protection <= 0:
        return QColor(0, 0, 0, 0)
    intensity = min(protection / 30.0, 1.0)
    return QColor(52, 152, 219, int(40 + 120 * intensity))


# ── Orientation transforms ─────────────────────────────────────────────
# For different exposures we define which Y range to show and how to scale.
EXPOSURE_CLIP = {
    # (y_min, y_max) — which portion of the 0..1 body to show
    TargetExposure.STANDING_EXPOSED: (0.0, 1.0),
    TargetExposure.RUNNING: (0.0, 1.0),
    TargetExposure.LOW_CROUCH: (0.0, 1.0),
    TargetExposure.KNEELING_EXPOSED: (0.0, 0.70),
    TargetExposure.HANDS_AND_KNEES_CROUCH: (0.0, 0.70),
    TargetExposure.PRONE_EXPOSED: (0.0, 0.50),
    TargetExposure.LOW_PRONE: (0.0, 0.48),
    TargetExposure.LOOKING_OVER_COVER: (0.0, 0.12),
    TargetExposure.FIRING_OVER_COVER: (0.0, 0.28),
    TargetExposure.HEAD: (0.0, 0.12),
    TargetExposure.BODY: (0.12, 0.48),
    TargetExposure.LEGS: (0.48, 1.0),
    TargetExposure.ARMS: (0.16, 0.50),
}


class _BodyCanvas(QWidget):
    """Internal canvas that draws the body diagram."""

    zone_hovered = pyqtSignal(object)  # BodyZone or None

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumSize(160, 240)

        self._is_front: bool = True
        self._exposure: TargetExposure = TargetExposure.STANDING_EXPOSED
        self._orientation: TargetOrientation = TargetOrientation.FRONT_REAR

        # damage per zone (zone index → total damage)
        self._zone_damage: dict[int, int] = {}
        # armor per zone (zone index → protection factor)
        self._zone_armor: dict[int, float] = {}
        # armor blunt per zone (zone index → blunt protection factor)
        self._zone_armor_bpf: dict[int, float] = {}
        # hit counts per zone
        self._zone_hits: dict[int, int] = {}

        self._hovered_zone_idx: Optional[int] = None

        # Pre-build QPainterPaths for hit testing
        self._zone_paths: list[QPainterPath] = []

    # ── public API ─────────────────────────────────────────────────────
    def set_view(self, is_front: bool):
        self._is_front = is_front
        self._rebuild_paths()
        self.update()

    def set_exposure(self, exposure: TargetExposure):
        self._exposure = exposure
        self._rebuild_paths()
        self.update()

    def set_orientation(self, orientation: TargetOrientation):
        self._orientation = orientation
        self.update()

    def set_zone_data(self, zone_damage: dict[int, int],
                      zone_armor: dict[int, float],
                      zone_hits: dict[int, int],
                      zone_armor_bpf: dict[int, float] | None = None):
        self._zone_damage = zone_damage
        self._zone_armor = zone_armor
        self._zone_armor_bpf = zone_armor_bpf or {}
        self._zone_hits = zone_hits
        self.update()

    def clear_data(self):
        self._zone_damage.clear()
        self._zone_armor.clear()
        self._zone_armor_bpf.clear()
        self._zone_hits.clear()
        self.update()

    # ── coordinate mapping ─────────────────────────────────────────────
    def _get_draw_rect(self) -> QRectF:
        """Get the rectangle for drawing (with margins)."""
        margin = 10
        w = self.width() - 2 * margin
        h = self.height() - 2 * margin
        # Keep aspect ratio ~0.4 (body proportions)
        target_ratio = 0.45
        if w / h > target_ratio:
            w = int(h * target_ratio)
        else:
            h = int(w / target_ratio)
        x = (self.width() - w) / 2
        y = (self.height() - h) / 2
        return QRectF(x, y, w, h)

    def _norm_to_pixel(self, nx: float, ny: float, rect: QRectF) -> QPointF:
        """Convert normalized (0..1) body coords to pixel coords, applying exposure clip."""
        y_min, y_max = EXPOSURE_CLIP.get(self._exposure, (0.0, 1.0))
        y_range = y_max - y_min
        if y_range <= 0:
            y_range = 1.0
        # Remap ny from [y_min, y_max] → [0, 1]
        mapped_y = (ny - y_min) / y_range
        px = rect.x() + nx * rect.width()
        py = rect.y() + mapped_y * rect.height()
        return QPointF(px, py)

    def _make_polygon(self, zone: BodyZone, rect: QRectF) -> QPolygonF:
        """Create pixel QPolygonF for a zone."""
        poly = zone.front_polygon if self._is_front else zone.rear_polygon
        points = [self._norm_to_pixel(x, y, rect) for x, y in poly]
        return QPolygonF(points)

    def _is_zone_visible(self, zone: BodyZone) -> bool:
        """Check if zone is within current exposure clip."""
        poly = zone.front_polygon if self._is_front else zone.rear_polygon
        y_min, y_max = EXPOSURE_CLIP.get(self._exposure, (0.0, 1.0))
        # Zone visible if any point is within range (with small tolerance)
        for _, y in poly:
            if y_min - 0.02 <= y <= y_max + 0.02:
                return True
        return False

    def _rebuild_paths(self):
        """Rebuild QPainterPaths for hit testing."""
        rect = self._get_draw_rect()
        self._zone_paths = []
        for zone in BODY_ZONES:
            path = QPainterPath()
            if self._is_zone_visible(zone):
                polygon = self._make_polygon(zone, rect)
                path.addPolygon(polygon)
                path.closeSubpath()
            self._zone_paths.append(path)

    # ── painting ───────────────────────────────────────────────────────
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self._get_draw_rect()

        # Background
        painter.fillRect(self.rect(), QColor(245, 245, 245))

        # Draw body outline
        self._draw_body_outline(painter, rect)

        # Draw zones
        for idx, zone in enumerate(BODY_ZONES):
            if not self._is_zone_visible(zone):
                continue
            polygon = self._make_polygon(zone, rect)
            self._draw_zone(painter, polygon, idx)

        # Draw orientation label
        self._draw_labels(painter, rect)

        painter.end()

    def _draw_body_outline(self, painter: QPainter, rect: QRectF):
        """Draw a subtle body silhouette outline."""
        outline_color = QColor(180, 180, 180)
        pen = QPen(outline_color, 1.5)
        painter.setPen(pen)
        painter.setBrush(QBrush(QColor(225, 225, 225)))

        # Collect all zone polygons to form an outline
        for zone in BODY_ZONES:
            if not self._is_zone_visible(zone):
                continue
            polygon = self._make_polygon(zone, rect)
            painter.drawPolygon(polygon)

    def _draw_zone(self, painter: QPainter, polygon: QPolygonF, zone_idx: int):
        """Draw a single zone with damage coloring and armor overlay."""
        damage = self._zone_damage.get(zone_idx, 0)
        armor = self._zone_armor.get(zone_idx, 0.0)
        hits = self._zone_hits.get(zone_idx, 0)
        is_hovered = (zone_idx == self._hovered_zone_idx)

        # Base fill — damage color
        fill_color = _damage_color(damage)
        if is_hovered:
            fill_color = fill_color.lighter(140)

        painter.setBrush(QBrush(fill_color))

        # Border
        if hits > 0:
            border_color = QColor(40, 40, 40, 220)
            pen_width = 2.0
        elif is_hovered:
            border_color = QColor(80, 80, 80, 180)
            pen_width = 1.5
        else:
            border_color = QColor(160, 160, 160, 140)
            pen_width = 0.8

        painter.setPen(QPen(border_color, pen_width))
        painter.drawPolygon(polygon)

        # Armor overlay — hatching pattern
        if armor > 0:
            armor_col = _armor_color(armor)
            painter.setBrush(QBrush(armor_col, Qt.BrushStyle.BDiagPattern))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawPolygon(polygon)

        # Hit count label
        if hits > 0:
            center = polygon.boundingRect().center()
            painter.setPen(QPen(QColor(30, 30, 30, 230)))
            font = painter.font()
            font.setPointSize(7)
            font.setBold(True)
            painter.setFont(font)
            painter.drawText(
                QRectF(center.x() - 10, center.y() - 6, 20, 12),
                Qt.AlignmentFlag.AlignCenter,
                str(hits)
            )

    def _draw_labels(self, painter: QPainter, rect: QRectF):
        """Draw view / orientation label."""
        painter.setPen(QPen(QColor(80, 80, 80)))
        font = QFont()
        font.setPointSize(9)
        font.setBold(True)
        painter.setFont(font)

        # Left/Right labels
        font.setPointSize(7)
        font.setBold(False)
        painter.setFont(font)
        painter.setPen(QPen(QColor(100, 100, 100)))
        if self._is_front:
            painter.drawText(QRectF(rect.x() - 5, rect.y() + rect.height() * 0.15, 30, 14),
                             Qt.AlignmentFlag.AlignCenter, "R")
            painter.drawText(QRectF(rect.right() - 25, rect.y() + rect.height() * 0.15, 30, 14),
                             Qt.AlignmentFlag.AlignCenter, "L")
        else:
            painter.drawText(QRectF(rect.x() - 5, rect.y() + rect.height() * 0.15, 30, 14),
                             Qt.AlignmentFlag.AlignCenter, "L")
            painter.drawText(QRectF(rect.right() - 25, rect.y() + rect.height() * 0.15, 30, 14),
                             Qt.AlignmentFlag.AlignCenter, "R")

    # ── mouse interaction ──────────────────────────────────────────────
    def mouseMoveEvent(self, event):
        pos = event.position() if hasattr(event, 'position') else event.pos()
        point = QPointF(pos)

        old_idx = self._hovered_zone_idx
        self._hovered_zone_idx = None

        for idx, path in enumerate(self._zone_paths):
            if not path.isEmpty() and path.contains(point):
                self._hovered_zone_idx = idx
                break

        if self._hovered_zone_idx != old_idx:
            self.zone_hovered.emit(
                BODY_ZONES[self._hovered_zone_idx] if self._hovered_zone_idx is not None else None
            )
            self.update()

        # Tooltip
        if self._hovered_zone_idx is not None:
            zone = BODY_ZONES[self._hovered_zone_idx]
            damage = self._zone_damage.get(self._hovered_zone_idx, 0)
            armor = self._zone_armor.get(self._hovered_zone_idx, 0)
            armor_bpf = self._zone_armor_bpf.get(self._hovered_zone_idx, 0)
            hits = self._zone_hits.get(self._hovered_zone_idx, 0)
            tip = f"<b>{zone.name}</b><br>"
            tip += f"Hits: {hits}<br>"
            tip += f"Total damage: {damage}<br>"
            if armor > 0 or armor_bpf > 0:
                tip += f"Ballistic PF: {armor:.0f}<br>"
                tip += f"Blunt PF: {armor_bpf:.0f}"
            QToolTip.showText(event.globalPosition().toPoint(), tip, self)
        else:
            QToolTip.hideText()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._rebuild_paths()


# ═══════════════════════════════════════════════════════════════════════
# Public widget
# ═══════════════════════════════════════════════════════════════════════

class BodyDiagramWidget(QWidget):
    """Complete body diagram widget with canvas (fixed: standing exposed / front)."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._character: Optional['Character'] = None
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)

        # Title
        title = QLabel("Body Diagram")
        title.setStyleSheet("font-weight: bold; font-size: 12px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Canvas (always front / standing exposed)
        self._canvas = _BodyCanvas()
        layout.addWidget(self._canvas, stretch=1)

        # Info label
        self._info_label = QLabel("")
        self._info_label.setStyleSheet("font-size: 10px;")
        self._info_label.setWordWrap(True)
        self._info_label.setMaximumHeight(40)
        layout.addWidget(self._info_label)

        self._canvas.zone_hovered.connect(self._on_zone_hovered)

        # Legend
        legend_layout = QHBoxLayout()
        legend_layout.setSpacing(8)
        self._add_legend_item(legend_layout, QColor(200, 200, 200, 60), "No hit")
        self._add_legend_item(legend_layout, QColor(46, 204, 113, 180), "Light")
        self._add_legend_item(legend_layout, QColor(241, 196, 15, 180), "Medium")
        self._add_legend_item(legend_layout, QColor(231, 76, 60, 180), "Heavy")
        self._add_legend_item(legend_layout, QColor(52, 152, 219, 100), "Armor", pattern=True)
        layout.addLayout(legend_layout)

    def _add_legend_item(self, layout: QHBoxLayout, color: QColor, text: str,
                          pattern: bool = False):
        """Add a small color swatch + label to the legend."""
        swatch = QWidget()
        swatch.setFixedSize(12, 12)
        style = f"background-color: rgba({color.red()},{color.green()},{color.blue()},{color.alpha()});"
        style += "border: 1px solid #999;"
        swatch.setStyleSheet(style)
        layout.addWidget(swatch)
        lbl = QLabel(text)
        lbl.setStyleSheet("font-size: 9px;")
        layout.addWidget(lbl)

    # ── public API ─────────────────────────────────────────────────────
    def set_character(self, character: 'Character'):
        """Set character and update diagram with their hit history and armor."""
        self._character = character
        self._update_from_character()

    def clear(self):
        """Clear the diagram."""
        self._character = None
        self._canvas.clear_data()
        self._info_label.setText("")

    def refresh(self):
        """Refresh data from current character."""
        if self._character:
            self._update_from_character()

    # ── private ────────────────────────────────────────────────────────
    def _update_from_character(self):
        """Recalculate zone data from character's hit_history and armor."""
        if not self._character:
            self._canvas.clear_data()
            return

        zone_damage: dict[int, int] = {}
        zone_hits: dict[int, int] = {}
        zone_armor: dict[int, float] = {}
        zone_armor_bpf: dict[int, float] = {}

        # Process hit history
        if hasattr(self._character, 'hit_history'):
            for dr in self._character.hit_history:
                if dr.location == AdvancedHitLocation.MISS:
                    continue
                zone = LOCATION_TO_ZONE.get(dr.location)
                if zone is None:
                    continue
                idx = BODY_ZONES.index(zone)
                zone_damage[idx] = zone_damage.get(idx, 0) + dr.damage
                zone_hits[idx] = zone_hits.get(idx, 0) + 1

        # Process armor (front only)
        armor_prot = self._character.armor_protection
        for (loc, is_front_armor), (pf, bpf) in armor_prot.items():
            if not is_front_armor:
                continue
            zone = LOCATION_TO_ZONE.get(loc)
            if zone is None:
                continue
            idx = BODY_ZONES.index(zone)
            zone_armor[idx] = max(zone_armor.get(idx, 0), pf)
            zone_armor_bpf[idx] = max(zone_armor_bpf.get(idx, 0), bpf)

        self._canvas.set_zone_data(zone_damage, zone_armor, zone_hits, zone_armor_bpf)


    def _on_zone_hovered(self, zone: Optional[BodyZone]):
        if zone is None:
            self._info_label.setText("")
            return

        locations_str = ", ".join(loc.name for loc in zone.locations[:3])
        if len(zone.locations) > 3:
            locations_str += f" (+{len(zone.locations) - 3} more)"
        self._info_label.setText(f"<b>{zone.name}</b>: {locations_str}")

