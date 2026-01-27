"""Equipment management dialog."""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTabWidget,
                              QWidget, QListWidget, QTextEdit, QPushButton,
                              QLabel, QSplitter, QLineEdit)
from PyQt6.QtCore import Qt
from phoenix_command.models.character import Character
from phoenix_command.models.gear import Weapon, Armor, AmmoType, Grenade, Gear


class EquipmentDialog(QDialog):
    """Dialog for managing character equipment."""
    
    def __init__(self, character: Character, parent=None):
        super().__init__(parent)
        self.character = character
        self.setWindowTitle(f"Equipment - {character.name}")
        self.setMinimumSize(900, 600)
        self._setup_ui()
        self._load_items()
    
    def _setup_ui(self):
        """Setup UI components."""
        layout = QHBoxLayout(self)
        
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.addWidget(QLabel("<b>Item Database</b>"))
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search...")
        self.search_input.textChanged.connect(self._filter_items)
        left_layout.addWidget(self.search_input)
        
        self.tabs = QTabWidget()
        self.weapons_list = QListWidget()
        self.armor_list = QListWidget()
        self.ammo_list = QListWidget()
        self.grenades_list = QListWidget()
        self.gear_list = QListWidget()
        
        self.tabs.addTab(self.weapons_list, "Weapons")
        self.tabs.addTab(self.armor_list, "Armor")
        self.tabs.addTab(self.ammo_list, "Ammo")
        self.tabs.addTab(self.grenades_list, "Grenades")
        self.tabs.addTab(self.gear_list, "Equipment")
        
        left_layout.addWidget(self.tabs)
        
        add_btn = QPushButton("Add to Character →")
        add_btn.clicked.connect(self._add_item)
        left_layout.addWidget(add_btn)
        
        splitter.addWidget(left_widget)
        
        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)
        center_layout.addWidget(QLabel("<b>Item Details</b>"))
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        center_layout.addWidget(self.details_text)
        splitter.addWidget(center_widget)
        
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.addWidget(QLabel("<b>Character Equipment</b>"))
        
        self.equipment_list = QListWidget()
        right_layout.addWidget(self.equipment_list)
        
        self.weight_label = QLabel()
        right_layout.addWidget(self.weight_label)
        
        remove_btn = QPushButton("Remove Selected")
        remove_btn.clicked.connect(self._remove_item)
        right_layout.addWidget(remove_btn)
        
        splitter.addWidget(right_widget)
        
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 2)
        splitter.setStretchFactor(2, 1)
        
        layout.addWidget(splitter)
        
        for lst in [self.weapons_list, self.armor_list, self.ammo_list, 
                    self.grenades_list, self.gear_list]:
            lst.currentItemChanged.connect(self._show_item_details)
        
        self._refresh_equipment_list()
    
    def _load_items(self):
        """Load items from database."""
        from phoenix_command.item_database import weapons, armor, grenades, equipment
        
        self.all_weapons = []
        self.all_armor = armor.armor if hasattr(armor, 'armor') else []
        self.all_grenades = grenades.grenades if hasattr(grenades, 'grenades') else []
        self.all_equipment = equipment.EQUIPMENT_LIST if hasattr(equipment, 'EQUIPMENT_LIST') else []
        self.all_ammo = []
        
        if hasattr(weapons, '__dict__'):
            for name, obj in weapons.__dict__.items():
                if isinstance(obj, Weapon):
                    self.all_weapons.append(obj)
                    self.all_ammo.extend(obj.ammunition_types)
        
        self._populate_lists()
    
    def _populate_lists(self):
        """Populate item lists."""
        self.weapons_list.clear()
        for weapon in self.all_weapons:
            self.weapons_list.addItem(weapon.name)
        
        self.armor_list.clear()
        for armor in self.all_armor:
            self.armor_list.addItem(armor.name)
        
        self.ammo_list.clear()
        seen_ammo = set()
        for ammo in self.all_ammo:
            if ammo.name not in seen_ammo:
                self.ammo_list.addItem(ammo.name)
                seen_ammo.add(ammo.name)
        
        self.grenades_list.clear()
        for grenade in self.all_grenades:
            self.grenades_list.addItem(grenade.name)
        
        self.gear_list.clear()
        for gear in self.all_equipment:
            self.gear_list.addItem(gear.name)
    
    def _filter_items(self):
        """Filter items based on search."""
        search = self.search_input.text().lower()
        current_tab = self.tabs.currentIndex()
        
        lists = [self.weapons_list, self.armor_list, self.ammo_list, 
                 self.grenades_list, self.gear_list]
        
        for i, lst in enumerate(lists):
            for j in range(lst.count()):
                item = lst.item(j)
                item.setHidden(search not in item.text().lower())
    
    def _show_item_details(self, current, previous):
        """Show details of selected item."""
        if not current:
            return
        
        item_name = current.text()
        current_tab = self.tabs.currentIndex()
        
        item = None
        if current_tab == 0:
            item = next((w for w in self.all_weapons if w.name == item_name), None)
        elif current_tab == 1:
            item = next((a for a in self.all_armor if a.name == item_name), None)
        elif current_tab == 2:
            item = next((a for a in self.all_ammo if a.name == item_name), None)
        elif current_tab == 3:
            item = next((g for g in self.all_grenades if g.name == item_name), None)
        elif current_tab == 4:
            item = next((g for g in self.all_equipment if g.name == item_name), None)
        
        if item:
            details = f"<b>{item.name}</b><br><br>"
            details += f"Weight: {item.weight} lbs<br>"
            if hasattr(item, 'description') and item.description:
                details += f"<br>{item.description}<br>"
            
            if isinstance(item, Weapon):
                details += f"<br>Type: {item.weapon_type.value}<br>"
                details += f"Caliber: {item.caliber.value}<br>"
                if item.full_auto:
                    details += f"Full Auto ROF: {item.full_auto_rof}<br>"
            
            self.details_text.setHtml(details)
    
    def _add_item(self):
        """Add selected item to character."""
        current_tab = self.tabs.currentIndex()
        lists = [self.weapons_list, self.armor_list, self.ammo_list,
                 self.grenades_list, self.gear_list]
        
        current_list = lists[current_tab]
        current_item = current_list.currentItem()
        
        if not current_item:
            return
        
        item_name = current_item.text()
        item = None
        
        if current_tab == 0:
            item = next((w for w in self.all_weapons if w.name == item_name), None)
        elif current_tab == 1:
            item = next((a for a in self.all_armor if a.name == item_name), None)
        elif current_tab == 2:
            item = next((a for a in self.all_ammo if a.name == item_name), None)
        elif current_tab == 3:
            item = next((g for g in self.all_grenades if g.name == item_name), None)
        elif current_tab == 4:
            item = next((g for g in self.all_equipment if g.name == item_name), None)
        
        if item:
            self.character.add_gear(item)
            self._refresh_equipment_list()
    
    def _remove_item(self):
        """Remove selected item from character."""
        current_row = self.equipment_list.currentRow()
        if 0 <= current_row < len(self.character.equipment):
            self.character.remove_gear(self.character.equipment[current_row])
            self._refresh_equipment_list()
    
    def _refresh_equipment_list(self):
        """Refresh character equipment list."""
        self.equipment_list.clear()
        for item in self.character.equipment:
            self.equipment_list.addItem(f"{item.name} ({item.weight} lbs)")
        
        self.weight_label.setText(f"<b>Total Weight: {self.character.encumbrance:.1f} lbs</b>")
