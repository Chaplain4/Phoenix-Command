"""Main window for Phoenix Command GUI."""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                              QSplitter, QMenuBar, QMenu, QStatusBar, QListWidget)
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
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
        char_menu.addAction("&Import Template")
        char_menu.addAction("&Manage Characters")
        
        combat_menu = menubar.addMenu("C&ombat")
        combat_menu.addAction("&New Combat")
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
        main_splitter.addWidget(self.character_list)
        
        center_splitter = QSplitter(Qt.Orientation.Vertical)
        
        self.work_area = QWidget()
        center_splitter.addWidget(self.work_area)
        
        self.event_log = QListWidget()
        self.event_log.setMaximumHeight(150)
        center_splitter.addWidget(self.event_log)
        
        main_splitter.addWidget(center_splitter)
        
        self.details_panel = QWidget()
        self.details_panel.setMaximumWidth(300)
        main_splitter.addWidget(self.details_panel)
        
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
                self.character_list.addItem(character.name or "Unnamed")
                self.statusBar().showMessage(f"Added character: {character.name or 'Unnamed'}")
