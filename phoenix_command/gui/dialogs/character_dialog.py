"""Character creation and editing dialog."""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTabWidget,
                             QWidget, QLabel, QSpinBox, QLineEdit, QPushButton,
                             QComboBox, QTextEdit, QFormLayout, QGroupBox)

from phoenix_command.item_database.character_templates import character_templates
from phoenix_command.models.character import Character
from phoenix_command.simulations.character_generator import CharacterGenerator


class CharacterDialog(QDialog):
    """Dialog for creating or editing a character."""
    
    def __init__(self, character: Character = None, parent=None):
        super().__init__(parent)
        self.character = character
        self.setWindowTitle("Edit Character" if character else "New Character")
        self.setMinimumSize(500, 500)

        self._setup_ui()
        
        if character:
            self._load_character_data()
    
    def _setup_ui(self):
        """Setup UI components."""
        layout = QVBoxLayout(self)
        
        self.tabs = QTabWidget()
        
        self.tabs.addTab(self._create_manual_tab(), "Manual")
        
        if not self.character:
            self.tabs.addTab(self._create_random_tab(), "Random")
            self.tabs.addTab(self._create_template_tab(), "Template")
        
        layout.addWidget(self.tabs)
        
        buttons = QHBoxLayout()
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        buttons.addStretch()
        buttons.addWidget(ok_btn)
        buttons.addWidget(cancel_btn)
        layout.addLayout(buttons)
    
    def _create_manual_tab(self):
        """Create manual input tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Basic attributes group
        attrs_group = QGroupBox("Attributes")
        attrs_layout = QFormLayout(attrs_group)

        self.name_input = QLineEdit()
        attrs_layout.addRow("Name:", self.name_input)

        self.str_spin = QSpinBox()
        self.str_spin.setRange(1, 20)
        self.str_spin.setValue(10)
        attrs_layout.addRow("Strength:", self.str_spin)

        self.int_spin = QSpinBox()
        self.int_spin.setRange(1, 20)
        self.int_spin.setValue(10)
        attrs_layout.addRow("Intelligence:", self.int_spin)

        self.wil_spin = QSpinBox()
        self.wil_spin.setRange(1, 20)
        self.wil_spin.setValue(10)
        attrs_layout.addRow("Will:", self.wil_spin)

        self.hlt_spin = QSpinBox()
        self.hlt_spin.setRange(1, 20)
        self.hlt_spin.setValue(10)
        attrs_layout.addRow("Health:", self.hlt_spin)

        self.agl_spin = QSpinBox()
        self.agl_spin.setRange(1, 20)
        self.agl_spin.setValue(10)
        attrs_layout.addRow("Agility:", self.agl_spin)

        self.skl_spin = QSpinBox()
        self.skl_spin.setRange(1, 10)
        self.skl_spin.setValue(3)
        attrs_layout.addRow("Gun Combat Skill:", self.skl_spin)

        layout.addWidget(attrs_group)

        # Damage and status group (only for editing existing character)
        if self.character:
            status_group = QGroupBox("Damage & Status")
            status_layout = QFormLayout(status_group)

            self.pd_spin = QSpinBox()
            self.pd_spin.setRange(0, 999)
            self.pd_spin.setValue(0)
            self.pd_spin.valueChanged.connect(self._update_status_display)
            status_layout.addRow("Physical Damage:", self.pd_spin)

            # Status display
            self.status_label = QLabel()
            self.status_label.setStyleSheet("font-weight: bold;")
            status_layout.addRow("Status:", self.status_label)

            # Quick damage buttons
            damage_btns = QHBoxLayout()
            heal_btn = QPushButton("Heal All")
            heal_btn.clicked.connect(lambda: self.pd_spin.setValue(0))
            damage_btns.addWidget(heal_btn)

            add_5_btn = QPushButton("+5 Damage")
            add_5_btn.clicked.connect(lambda: self.pd_spin.setValue(self.pd_spin.value() + 5))
            damage_btns.addWidget(add_5_btn)

            add_10_btn = QPushButton("+10 Damage")
            add_10_btn.clicked.connect(lambda: self.pd_spin.setValue(self.pd_spin.value() + 10))
            damage_btns.addWidget(add_10_btn)

            status_layout.addRow("", damage_btns)

            layout.addWidget(status_group)

        # Derived stats group
        derived_group = QGroupBox("Derived Stats")
        derived_layout = QVBoxLayout(derived_group)
        self.derived_label = QLabel()
        self._update_derived_stats()
        derived_layout.addWidget(self.derived_label)
        layout.addWidget(derived_group)

        for spin in [self.str_spin, self.int_spin, self.wil_spin, 
                     self.hlt_spin, self.agl_spin, self.skl_spin]:
            spin.valueChanged.connect(self._update_derived_stats)
        
        layout.addStretch()
        return widget
    
    def _update_status_display(self):
        """Update status display based on physical damage."""
        if not hasattr(self, 'status_label'):
            return

        pd = self.pd_spin.value()
        knockout_value = int(0.5 * self.wil_spin.value() * self.skl_spin.value())

        if pd == 0:
            status = "Healthy"
            color = "#27ae60"  # green
        elif pd < knockout_value:
            status = f"Wounded (KO at {knockout_value})"
            color = "#f39c12"  # yellow
        else:
            status = "Seriously Wounded"
            color = "#e67e22"  # orange

        self.status_label.setText(status)
        self.status_label.setStyleSheet(f"font-weight: bold; color: {color};")

    def _create_random_tab(self):
        """Create random generation tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        roll_btn = QPushButton("Roll Random Character")
        roll_btn.clicked.connect(self._roll_random)
        layout.addWidget(roll_btn)
        
        self.random_display = QTextEdit()
        self.random_display.setReadOnly(True)
        layout.addWidget(self.random_display)
        
        self.random_name = QLineEdit()
        layout.addWidget(QLabel("Name:"))
        layout.addWidget(self.random_name)
        
        return widget
    
    def _create_template_tab(self):
        """Create template selection tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        self.template_combo = QComboBox()
        for i, template in enumerate(character_templates):
            self.template_combo.addItem(template.name, template)
        layout.addWidget(QLabel("Select Template:"))
        layout.addWidget(self.template_combo)
        
        self.template_preview = QTextEdit()
        self.template_preview.setReadOnly(True)
        layout.addWidget(self.template_preview)
        
        self.template_combo.currentIndexChanged.connect(self._update_template_preview)
        self._update_template_preview()
        
        return widget
    
    def _update_derived_stats(self):
        """Update derived stats display."""
        temp_char = Character(
            strength=self.str_spin.value(),
            intelligence=self.int_spin.value(),
            will=self.wil_spin.value(),
            health=self.hlt_spin.value(),
            agility=self.agl_spin.value(),
            gun_combat_skill_level=self.skl_spin.value()
        )
        
        text = (f"Defensive ALM: {temp_char.defensive_alm}\n"
                f"Knockout Value: {temp_char.knockout_value}\n"
                f"Impulses: {temp_char.impulses}")
        self.derived_label.setText(text)
    
    def _roll_random(self):
        """Roll random character."""
        char = CharacterGenerator.generate_character(gun_combat_skill_level=5)
        
        text = (f"Strength: {char.strength}\n"
                f"Intelligence: {char.intelligence}\n"
                f"Will: {char.will}\n"
                f"Health: {char.health}\n"
                f"Agility: {char.agility}\n"
                f"Gun Combat Skill: {char.gun_combat_skill_level}")
        
        self.random_display.setText(text)
        self.random_result = char
    
    def _update_template_preview(self):
        """Update template preview."""
        template = self.template_combo.currentData()
        if template:
            text = (f"Strength: {template.strength}\n"
                    f"Intelligence: {template.intelligence}\n"
                    f"Will: {template.will}\n"
                    f"Health: {template.health}\n"
                    f"Agility: {template.agility}\n"
                    f"Gun Combat Skill: {template.gun_combat_skill_level}\n\n"
                    f"Equipment: {len(template.equipment)} items")
            self.template_preview.setText(text)
    
    def get_character(self) -> Character:
        """Get the created/edited character."""
        if self.character:
            self.character.name = self.name_input.text() or self.character.name
            self.character.strength = self.str_spin.value()
            self.character.intelligence = self.int_spin.value()
            self.character.will = self.wil_spin.value()
            self.character.health = self.hlt_spin.value()
            self.character.agility = self.agl_spin.value()
            self.character.gun_combat_skill_level = self.skl_spin.value()
            # Update physical damage if editing
            if hasattr(self, 'pd_spin'):
                self.character.physical_damage_total = self.pd_spin.value()
            return self.character
        
        current_tab = self.tabs.currentIndex()
        
        if current_tab == 0:
            char = Character(
                strength=self.str_spin.value(),
                intelligence=self.int_spin.value(),
                will=self.wil_spin.value(),
                health=self.hlt_spin.value(),
                agility=self.agl_spin.value(),
                gun_combat_skill_level=self.skl_spin.value()
            )
            char.name = self.name_input.text() or "Unnamed"
            return char
        
        elif current_tab == 1:
            if hasattr(self, 'random_result'):
                char = self.random_result
                char.name = self.random_name.text() or "Unnamed"
                return char
        
        elif current_tab == 2:
            template = self.template_combo.currentData()
            if template:
                import copy
                return copy.deepcopy(template)
        
        return None
    
    def _load_character_data(self):
        """Load existing character data into manual tab."""
        if self.character:
            self.name_input.setText(self.character.name or "")
            self.str_spin.setValue(self.character.strength)
            self.int_spin.setValue(self.character.intelligence)
            self.wil_spin.setValue(self.character.will)
            self.hlt_spin.setValue(self.character.health)
            self.agl_spin.setValue(self.character.agility)
            self.skl_spin.setValue(self.character.gun_combat_skill_level)

            # Load physical damage if editing
            if hasattr(self, 'pd_spin'):
                self.pd_spin.setValue(self.character.physical_damage_total)
                self._update_status_display()
