"""Stats display widget for character details."""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox, QFormLayout
from PyQt6.QtCore import Qt
from phoenix_command.models.character import Character


class StatsDisplayWidget(QWidget):
    """Widget for displaying character stats and derived characteristics."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.character = None
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.name_label = QLabel("Select a character")
        self.name_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(self.name_label)
        
        attrs_group = QGroupBox("Attributes")
        attrs_layout = QFormLayout()
        self.str_label = QLabel("-")
        self.int_label = QLabel("-")
        self.wil_label = QLabel("-")
        self.hlt_label = QLabel("-")
        self.agl_label = QLabel("-")
        self.skl_label = QLabel("-")
        attrs_layout.addRow("STR:", self.str_label)
        attrs_layout.addRow("INT:", self.int_label)
        attrs_layout.addRow("WIL:", self.wil_label)
        attrs_layout.addRow("HLT:", self.hlt_label)
        attrs_layout.addRow("AGL:", self.agl_label)
        attrs_layout.addRow("SKL:", self.skl_label)
        attrs_group.setLayout(attrs_layout)
        layout.addWidget(attrs_group)
        
        derived_group = QGroupBox("Derived Stats")
        derived_layout = QFormLayout()
        self.def_alm_label = QLabel("-")
        self.ko_label = QLabel("-")
        self.imp_label = QLabel("-")
        self.enc_label = QLabel("-")
        self.pd_label = QLabel("-")
        derived_layout.addRow("Defensive ALM:", self.def_alm_label)
        derived_layout.addRow("Knockout Value:", self.ko_label)
        derived_layout.addRow("Impulses:", self.imp_label)
        derived_layout.addRow("Encumbrance:", self.enc_label)
        derived_layout.addRow("Physical Damage:", self.pd_label)
        derived_group.setLayout(derived_layout)
        layout.addWidget(derived_group)
        
        equip_group = QGroupBox("Equipment")
        equip_layout = QVBoxLayout()
        self.equip_label = QLabel("No equipment")
        self.equip_label.setWordWrap(True)
        equip_layout.addWidget(self.equip_label)
        equip_group.setLayout(equip_layout)
        layout.addWidget(equip_group)
        
        layout.addStretch()
    
    def set_character(self, character: Character):
        """Update display with character data."""
        self.character = character
        if character:
            self.name_label.setText(character.name)
            self.str_label.setText(str(character.strength))
            self.int_label.setText(str(character.intelligence))
            self.wil_label.setText(str(character.will))
            self.hlt_label.setText(str(character.health))
            self.agl_label.setText(str(character.agility))
            self.skl_label.setText(str(character.gun_combat_skill_level))
            
            self.def_alm_label.setText(str(character.defensive_alm))
            self.ko_label.setText(str(character.knockout_value))
            self.imp_label.setText(str(character.impulses))
            self.enc_label.setText(f"{character.encumbrance:.1f} lbs")
            self.pd_label.setText(str(character.physical_damage_total))
            
            if character.equipment:
                equip_text = ""
                for item in character.equipment:
                    equip_text += f"• {item.name} ({item.weight} lbs)\n"
                self.equip_label.setText(equip_text.strip())
            else:
                self.equip_label.setText("No equipment")
        else:
            self.clear()
    
    def clear(self):
        """Clear all displayed data."""
        self.character = None
        self.name_label.setText("Select a character")
        self.str_label.setText("-")
        self.int_label.setText("-")
        self.wil_label.setText("-")
        self.hlt_label.setText("-")
        self.agl_label.setText("-")
        self.skl_label.setText("-")
        self.def_alm_label.setText("-")
        self.ko_label.setText("-")
        self.imp_label.setText("-")
        self.enc_label.setText("-")
        self.pd_label.setText("-")
        self.equip_label.setText("No equipment")
