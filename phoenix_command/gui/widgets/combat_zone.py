"""Combat zone widget for managing combat participants."""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from phoenix_command.models.character import Character
from phoenix_command.gui.widgets.character_card import CharacterCard


class DropZone(QWidget):
    """Drop zone for character cards."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.character = None
        self.card = None
        self.setAcceptDrops(True)
        self.setMinimumHeight(120)
        self.setMinimumWidth(160)
        self.setStyleSheet("background-color: #f0f0f0; border: 2px dashed #999;")
        
        self.layout = QVBoxLayout(self)
        self.placeholder = QLabel("Drop character here")
        self.placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.placeholder)
    
    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
            self.setStyleSheet("background-color: #d0e8f0; border: 2px solid #4a90e2;")
    
    def dragLeaveEvent(self, event):
        if not self.character:
            self.setStyleSheet("background-color: #f0f0f0; border: 2px dashed #999;")
    
    def dropEvent(self, event):
        char_name = event.mimeData().text()
        main_window = self.window()
        if hasattr(main_window, 'characters'):
            for char in main_window.characters:
                if char.name == char_name:
                    self.set_character(char)
                    event.acceptProposedAction()
                    return
    
    def set_character(self, character: Character):
        if self.card:
            self.layout.removeWidget(self.card)
            self.card.deleteLater()
        self.placeholder.hide()
        
        self.character = character
        self.card = CharacterCard(character)
        self.layout.addWidget(self.card)
        self.setStyleSheet("background-color: #e8f4f8; border: 2px solid #4a90e2;")
        
        parent = self.parent()
        if isinstance(parent, CombatZoneWidget):
            parent.add_target_zone()
    
    def clear(self):
        if self.card:
            self.layout.removeWidget(self.card)
            self.card.deleteLater()
            self.card = None
        self.character = None
        self.placeholder.show()
        self.setStyleSheet("background-color: #f0f0f0; border: 2px dashed #999;")


class CombatZoneWidget(QWidget):
    """Combat zone with shooter and targets areas."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        
        shooter_label = QLabel("Shooter:")
        shooter_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        layout.addWidget(shooter_label)
        
        self.shooter_zone = DropZone()
        layout.addWidget(self.shooter_zone)
        
        targets_label = QLabel("Targets:")
        targets_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        layout.addWidget(targets_label)
        
        self.targets_layout = QHBoxLayout()
        self.target_zones = []
        self.add_target_zone()
        self.targets_layout.addStretch()
        layout.addLayout(self.targets_layout)
        
        buttons_layout = QHBoxLayout()
        simulate_btn = QPushButton("Simulate")
        simulate_btn.clicked.connect(self._simulate)
        buttons_layout.addWidget(simulate_btn)
        clear_btn = QPushButton("Clear All")
        clear_btn.clicked.connect(self.clear_all)
        buttons_layout.addWidget(clear_btn)
        buttons_layout.addStretch()
        layout.addLayout(buttons_layout)
        
        layout.addStretch()
    
    def _simulate(self):
        """Show menu to select combat type."""
        from PyQt6.QtWidgets import QMessageBox, QMenu
        from PyQt6.QtGui import QCursor
        from phoenix_command.models.gear import Weapon
        
        shooter = self.get_shooter()
        targets = self.get_targets()
        
        if not shooter:
            QMessageBox.warning(self, "No Shooter", "Please select a shooter")
            return
        
        if not targets:
            QMessageBox.warning(self, "No Targets", "Please select at least one target")
            return
        
        menu = QMenu(self)
        menu.addAction("Single Shot")
        
        has_3rb = False
        has_burst = False
        for item in shooter.equipment:
            if isinstance(item, Weapon) and item.ballistic_data:
                if item.ballistic_data.three_round_burst:
                    has_3rb = True
                if item.ballistic_data.minimum_arc:
                    has_burst = True
        
        if has_3rb:
            menu.addAction("Three Round Burst")
        if has_burst:
            menu.addAction("Burst Fire")
        
        action = menu.exec(QCursor.pos())
        if not action:
            return
        
        main_window = self.window()
        if action.text() == "Single Shot" and hasattr(main_window, '_single_shot'):
            main_window._single_shot()
        elif action.text() == "Three Round Burst" and hasattr(main_window, '_three_round_burst'):
            main_window._three_round_burst()
        elif action.text() == "Burst Fire":
            QMessageBox.information(self, "Not Implemented", "Burst Fire coming soon")
    
    def clear_all(self):
        self.shooter_zone.clear()
        for zone in self.target_zones:
            zone.clear()
        while len(self.target_zones) > 1:
            zone = self.target_zones.pop()
            self.targets_layout.removeWidget(zone)
            zone.deleteLater()
    
    def add_target_zone(self):
        if not self.target_zones or self.target_zones[-1].character:
            zone = DropZone(self)
            self.target_zones.append(zone)
            self.targets_layout.insertWidget(len(self.target_zones) - 1, zone)
    
    def get_shooter(self):
        return self.shooter_zone.character
    
    def get_targets(self):
        return [zone.character for zone in self.target_zones if zone.character]
