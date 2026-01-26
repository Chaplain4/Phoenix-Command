"""Character card widget for displaying character information."""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt
from phoenix_command.models.character import Character


class CharacterCard(QWidget):
    """Widget displaying character information."""
    
    def __init__(self, character: Character, parent=None):
        super().__init__(parent)
        self.character = character
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        
        name_label = QLabel(f"<b>{self.character.name or 'Unnamed'}</b>")
        layout.addWidget(name_label)
        
        stats_text = (
            f"STR: {self.character.strength} INT: {self.character.intelligence} "
            f"WIL: {self.character.will}<br>"
            f"HLT: {self.character.health} AGL: {self.character.agility} "
            f"SKL: {self.character.gun_combat_skill_level}"
        )
        stats_label = QLabel(stats_text)
        stats_label.setWordWrap(True)
        layout.addWidget(stats_label)
        
        hp_label = QLabel(f"HP: {self.character.health - self.character.physical_damage_total}/{self.character.health}")
        layout.addWidget(hp_label)
        
        status = "Healthy"
        if self.character.physical_damage_total > 0:
            status = "Wounded"
        status_label = QLabel(f"Status: {status}")
        layout.addWidget(status_label)
        
        layout.addStretch()
