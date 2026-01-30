"""Main window for Phoenix Command GUI."""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                              QSplitter, QMenuBar, QMenu, QStatusBar, QListWidget, QLabel)
from PyQt6.QtCore import Qt
from phoenix_command.models.character import Character


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.characters = []
        self.setWindowTitle("Phoenix Command")
        self.setGeometry(100, 100, 1400, 900)
        
        self._create_menu_bar()
        self._create_central_widget()
        self._create_status_bar()
    
    def _create_menu_bar(self):
        """Create menu bar."""
        menubar = self.menuBar()
        
        file_menu = menubar.addMenu("&File")
        file_menu.addAction("&New Session")
        file_menu.addAction("&Load Session")
        file_menu.addAction("&Save Session")
        file_menu.addSeparator()
        file_menu.addAction("E&xit", self.close)
        
        char_menu = menubar.addMenu("&Characters")
        add_char_action = char_menu.addAction("&Add Character")
        add_char_action.triggered.connect(self._add_character)
        edit_char_action = char_menu.addAction("&Edit Character")
        edit_char_action.triggered.connect(self._edit_character)
        equip_action = char_menu.addAction("Manage &Equipment")
        equip_action.triggered.connect(self._manage_equipment)
        char_menu.addSeparator()
        char_menu.addAction("&Import Template")
        
        combat_menu = menubar.addMenu("C&ombat")
        shot_action = combat_menu.addAction("&Single Shot")
        shot_action.triggered.connect(self._single_shot)
        three_rb_action = combat_menu.addAction("&Three Round Burst")
        three_rb_action.triggered.connect(self._three_round_burst)
        combat_menu.addAction("Combat &History")
        
        help_menu = menubar.addMenu("&Help")
        help_menu.addAction("&Documentation")
        help_menu.addAction("&About")
    
    def _create_central_widget(self):
        """Create central widget with panels."""
        central = QWidget()
        self.setCentralWidget(central)
        
        layout = QHBoxLayout(central)
        
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        self.character_list = QListWidget()
        self.character_list.setMaximumWidth(250)
        self.character_list.currentRowChanged.connect(self._on_character_selected)
        main_splitter.addWidget(self.character_list)
        
        center_splitter = QSplitter(Qt.Orientation.Vertical)
        
        self.work_area = QWidget()
        center_splitter.addWidget(self.work_area)
        
        self.event_log = QListWidget()
        self.event_log.setMaximumHeight(150)
        center_splitter.addWidget(self.event_log)
        
        main_splitter.addWidget(center_splitter)
        
        details_widget = QWidget()
        details_layout = QVBoxLayout(details_widget)
        self.details_label = QLabel("Select a character")
        self.details_label.setWordWrap(True)
        self.details_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        details_layout.addWidget(self.details_label)
        details_widget.setMaximumWidth(300)
        main_splitter.addWidget(details_widget)
        
        main_splitter.setStretchFactor(0, 1)
        main_splitter.setStretchFactor(1, 3)
        main_splitter.setStretchFactor(2, 1)
        
        layout.addWidget(main_splitter)
    
    def _create_status_bar(self):
        """Create status bar."""
        self.statusBar().showMessage("Ready")
    
    def _add_character(self):
        """Open character creation dialog."""
        from phoenix_command.gui.dialogs.character_dialog import CharacterDialog
        dialog = CharacterDialog(parent=self)
        if dialog.exec():
            character = dialog.get_character()
            if character:
                self.characters.append(character)
                self._refresh_character_list()
                self.statusBar().showMessage(f"Added character: {character.name}")
    
    def _refresh_character_list(self):
        """Refresh character list display."""
        self.character_list.clear()
        for char in self.characters:
            self.character_list.addItem(char.name)
    
    def _on_character_selected(self, index):
        """Display character details when selected."""
        if 0 <= index < len(self.characters):
            char = self.characters[index]
            details = f"<b>{char.name}</b><br><br>"
            details += f"STR: {char.strength} INT: {char.intelligence} WIL: {char.will}<br>"
            details += f"HLT: {char.health} AGL: {char.agility} SKL: {char.gun_combat_skill_level}<br><br>"
            details += f"Defensive ALM: {char.defensive_alm}<br>"
            details += f"Knockout Value: {char.knockout_value}<br>"
            details += f"Impulses: {char.impulses}<br><br>"
            details += f"<b>Equipment ({len(char.equipment)} items):</b><br>"
            for item in char.equipment:
                details += f"- {item.name} ({item.weight} lbs)<br>"
            details += f"<br>Total Weight: {char.encumbrance:.1f} lbs"
            self.details_label.setText(details)
    
    def _edit_character(self):
        """Edit selected character stats."""
        current_row = self.character_list.currentRow()
        if current_row < 0:
            self.statusBar().showMessage("No character selected")
            return
        
        from phoenix_command.gui.dialogs.character_dialog import CharacterDialog
        char = self.characters[current_row]
        dialog = CharacterDialog(character=char, parent=self)
        if dialog.exec():
            dialog.get_character()
            self._refresh_character_list()
            self._on_character_selected(current_row)
            self.statusBar().showMessage(f"Updated character: {char.name}")
    
    def _manage_equipment(self):
        """Open equipment management dialog."""
        current_row = self.character_list.currentRow()
        if current_row < 0:
            self.statusBar().showMessage("No character selected")
            return
        
        from phoenix_command.gui.dialogs.equipment_dialog import EquipmentDialog
        char = self.characters[current_row]
        dialog = EquipmentDialog(character=char, parent=self)
        dialog.exec()
        self._on_character_selected(current_row)
        self.statusBar().showMessage(f"Equipment updated for {char.name}")
    
    def _single_shot(self):
        """Open single shot dialog."""
        if len(self.characters) < 2:
            self.statusBar().showMessage("Need at least 2 characters for combat")
            return
        
        from phoenix_command.gui.dialogs.shot_dialog import ShotDialog
        dialog = ShotDialog(characters=self.characters, parent=self)
        dialog.exec()
    
    def _three_round_burst(self):
        """Open three round burst dialog."""
        if len(self.characters) < 2:
            self.statusBar().showMessage("Need at least 2 characters for combat")
            return
        
        from phoenix_command.models.gear import Weapon
        has_3rb_weapon = False
        for char in self.characters:
            for item in char.equipment:
                if isinstance(item, Weapon) and item.ballistic_data and item.ballistic_data.three_round_burst:
                    has_3rb_weapon = True
                    break
            if has_3rb_weapon:
                break
        
        if not has_3rb_weapon:
            self.statusBar().showMessage("No character has a weapon with three round burst capability")
            return
        
        from phoenix_command.gui.dialogs.three_round_burst_dialog import ThreeRoundBurstDialog
        dialog = ThreeRoundBurstDialog(characters=self.characters, parent=self)
        dialog.exec()
