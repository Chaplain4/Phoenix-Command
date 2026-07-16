"""Overlay widget for switching between edit and combat map modes."""

from __future__ import annotations

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QFrame, QPushButton, QVBoxLayout


class MapModePanel(QFrame):
    """Compact overlay for Edit/Combat mode switching."""

    map_mode_changed = pyqtSignal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._is_host = True
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setAutoFillBackground(True)
        pal = self.palette()
        pal.setColor(self.backgroundRole(), QColor(30, 30, 30, 200))
        self.setPalette(pal)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        self._edit_btn = QPushButton("Edit")
        self._edit_btn.setCheckable(True)
        self._edit_btn.setChecked(True)
        self._edit_btn.clicked.connect(lambda: self._set_mode("edit"))
        layout.addWidget(self._edit_btn)

        self._combat_btn = QPushButton("Combat")
        self._combat_btn.setCheckable(True)
        self._combat_btn.clicked.connect(lambda: self._set_mode("combat"))
        layout.addWidget(self._combat_btn)

        self.setFixedWidth(96)

    def set_host(self, is_host: bool) -> None:
        self._is_host = is_host
        self._edit_btn.setEnabled(is_host)
        self._combat_btn.setEnabled(is_host)

    def set_mode(self, mode: str) -> None:
        self._edit_btn.setChecked(mode == "edit")
        self._combat_btn.setChecked(mode == "combat")

    def _set_mode(self, mode: str) -> None:
        if not self._is_host:
            return
        self.map_mode_changed.emit(mode)
