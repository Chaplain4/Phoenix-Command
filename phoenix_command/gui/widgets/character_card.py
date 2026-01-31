"""Character card widget with drag support."""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt, QMimeData
from PyQt6.QtGui import QDrag
from phoenix_command.models.character import Character


class CharacterCard(QFrame):
    """Compact character card with drag support."""
    
    def __init__(self, character: Character, parent=None):
        super().__init__(parent)
        self.character = character
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        self.setLineWidth(2)
        self.setMinimumSize(120, 80)
        self.setMaximumSize(150, 100)
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        
        name_label = QLabel(self.character.name)
        name_label.setStyleSheet("font-weight: bold;")
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(name_label)
        
        pd_label = QLabel(f"PD: {self.character.physical_damage_total}")
        pd_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(pd_label)
        
        status = "Healthy"
        if self.character.physical_damage_total > 0:
            status = "Wounded"
        status_label = QLabel(status)
        status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(status_label)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setText(self.character.name)
            drag.setMimeData(mime_data)
            drag.exec(Qt.DropAction.CopyAction)
