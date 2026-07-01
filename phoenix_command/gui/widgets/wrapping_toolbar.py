"""Toolbar that wraps widgets onto multiple rows when space is tight."""

from __future__ import annotations

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QSizePolicy, QVBoxLayout, QWidget


class WrappingToolbar(QWidget):
    """Multi-row toolbar: items flow to the next line instead of an overflow menu."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._main_layout = QVBoxLayout(self)
        self._main_layout.setContentsMargins(2, 2, 2, 2)
        self._main_layout.setSpacing(2)
        self._items: list[QWidget] = []

    def add_widget(self, widget: QWidget) -> None:
        widget.setParent(self)
        self._items.append(widget)
        self._schedule_relayout()

    def add_separator(self) -> None:
        line = QFrame(self)
        line.setFrameShape(QFrame.Shape.VLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        line.setFixedWidth(2)
        line.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.add_widget(line)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self._schedule_relayout()

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self._schedule_relayout()

    def setEnabled(self, enabled: bool) -> None:
        super().setEnabled(enabled)
        for item in self._items:
            item.setEnabled(enabled)

    def _schedule_relayout(self) -> None:
        QTimer.singleShot(0, self._relayout)

    def _relayout(self) -> None:
        available = max(200, self.width() - 8)

        while self._main_layout.count():
            row = self._main_layout.takeAt(0)
            if row.layout() is not None:
                row.layout().deleteLater()

        for item in self._items:
            item.setParent(self)

        current_row = QHBoxLayout()
        current_row.setContentsMargins(0, 0, 0, 0)
        current_row.setSpacing(4)
        current_width = 0
        rows: list[QHBoxLayout] = [current_row]

        for item in self._items:
            w = max(item.sizeHint().width(), item.minimumSizeHint().width()) + 6
            if current_width + w > available and current_row.count() > 0:
                current_row = QHBoxLayout()
                current_row.setContentsMargins(0, 0, 0, 0)
                current_row.setSpacing(4)
                rows.append(current_row)
                current_width = 0
            current_row.addWidget(item)
            current_width += w

        for row in rows:
            row.addStretch()
            self._main_layout.addLayout(row)
