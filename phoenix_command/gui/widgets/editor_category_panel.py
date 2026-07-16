"""Compact overlay widget for top-level map editor categories."""

from __future__ import annotations

from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QFrame, QPushButton, QVBoxLayout

from phoenix_command.gui.widgets.hex_map_modes import EditorCategory


class EditorCategoryPanel(QFrame):
    """Compact overlay for top-level editor categories."""

    def __init__(self, on_select, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setAutoFillBackground(True)
        pal = self.palette()
        pal.setColor(self.backgroundRole(), QColor(30, 30, 30, 200))
        self.setPalette(pal)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        self._buttons: dict[EditorCategory, QPushButton] = {}
        for label, cat in [
            ("Map", EditorCategory.MAP),
            ("Terrain", EditorCategory.TERRAIN),
            ("Objects", EditorCategory.OBJECTS),
            ("Tokens", EditorCategory.TOKENS),
        ]:
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, c=cat: on_select(c))
            layout.addWidget(btn)
            self._buttons[cat] = btn
        self.setFixedWidth(96)

    def set_category(self, category: EditorCategory) -> None:
        for cat, btn in self._buttons.items():
            btn.setChecked(cat == category)
