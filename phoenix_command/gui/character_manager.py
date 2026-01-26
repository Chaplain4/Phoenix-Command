"""Character manager for managing the list of characters."""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget, QListWidgetItem
from PyQt6.QtCore import pyqtSignal
from phoenix_command.models.character import Character
from phoenix_command.gui.dialogs.character_dialog import CharacterDialog


class CharacterManager(QWidget):
    """Widget for managing characters."""
    
    character_selected = pyqtSignal(Character)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.characters = []
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup UI components."""
        layout = QVBoxLayout(self)
        
        add_btn = QPushButton("Add Character")
        add_btn.clicked.connect(self._add_character)
        layout.addWidget(add_btn)
        
        self.list_widget = QListWidget()
        self.list_widget.currentItemChanged.connect(self._on_selection_changed)
        layout.addWidget(self.list_widget)
        
        remove_btn = QPushButton("Remove Character")
        remove_btn.clicked.connect(self._remove_character)
        layout.addWidget(remove_btn)
    
    def _add_character(self):
        """Add a new character."""
        dialog = CharacterDialog(parent=self)
        if dialog.exec():
            character = dialog.get_character()
            if character:
                self.characters.append(character)
                self._refresh_list()
    
    def _remove_character(self):
        """Remove selected character."""
        current = self.list_widget.currentRow()
        if current >= 0:
            del self.characters[current]
            self._refresh_list()
    
    def _refresh_list(self):
        """Refresh the character list."""
        self.list_widget.clear()
        for char in self.characters:
            name = char.name or "Unnamed"
            item = QListWidgetItem(f"{name} (SKL {char.gun_combat_skill_level})")
            self.list_widget.addItem(item)
    
    def _on_selection_changed(self, current, previous):
        """Handle selection change."""
        if current:
            idx = self.list_widget.row(current)
            if 0 <= idx < len(self.characters):
                self.character_selected.emit(self.characters[idx])
