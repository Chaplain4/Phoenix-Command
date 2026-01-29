"""Shotgun shot dialog."""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QComboBox, QSpinBox, QCheckBox, QPushButton,
                             QTextEdit, QMessageBox, QGroupBox, QFormLayout,
                             QStackedWidget, QListWidget, QWidget)

from phoenix_command.models.character import Character
from phoenix_command.models.enums import TargetExposure, SituationStanceModifier4B, VisibilityModifier4C, TargetOrientation
from phoenix_command.models.gear import Weapon, AmmoType
from phoenix_command.models.hit_result_advanced import ShotParameters
from phoenix_command.simulations.combat_simulator import CombatSimulator


class ShotgunDialog(QDialog):
    """Dialog for shotgun shot simulation."""
    
    def __init__(self, characters: list[Character], parent=None):
        super().__init__(parent)
        self.characters = characters
        self.setWindowTitle("Shotgun Shot")
        self.setMinimumSize(700, 600)
        self.current_step = 0
        self.secondary_targets = []
        self.target_params = {}
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup UI components."""
        layout = QVBoxLayout(self)
        
        self.step_label = QLabel()
        self.step_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(self.step_label)
        
        self.stack = QStackedWidget()
        layout.addWidget(self.stack)
        
        self.stack.addWidget(self._create_shooter_step())
        self.stack.addWidget(self._create_primary_target_step())
        self.stack.addWidget(self._create_secondary_targets_step())
        self.stack.addWidget(self._create_common_params_step())
        self.stack.addWidget(self._create_target_params_step())
        self.stack.addWidget(self._create_results_step())
        
        nav_layout = QHBoxLayout()
        self.prev_btn = QPushButton("Previous")
        self.prev_btn.clicked.connect(self._previous_step)
        self.prev_btn.setEnabled(False)
        self.next_btn = QPushButton("Next")
        self.next_btn.clicked.connect(self._next_step)
        self.simulate_btn = QPushButton("Simulate")
        self.simulate_btn.clicked.connect(self._simulate)
        self.simulate_btn.setVisible(False)
        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.accept)
        
        nav_layout.addWidget(self.prev_btn)
        nav_layout.addStretch()
        nav_layout.addWidget(self.next_btn)
        nav_layout.addWidget(self.simulate_btn)
        nav_layout.addWidget(self.close_btn)
        layout.addLayout(nav_layout)
        
        self._update_step_label()
        self._on_shooter_changed()
    
    def _create_shooter_step(self):
        """Step 1: Shooter & Weapon selection."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        shooter_group = QGroupBox("Shooter")
        shooter_layout = QFormLayout()
        self.shooter_combo = QComboBox()
        for char in self.characters:
            self.shooter_combo.addItem(char.name, char)
        self.shooter_combo.currentIndexChanged.connect(self._on_shooter_changed)
        shooter_layout.addRow("Character:", self.shooter_combo)
        shooter_group.setLayout(shooter_layout)
        layout.addWidget(shooter_group)
        
        weapon_group = QGroupBox("Weapon")
        weapon_layout = QFormLayout()
        self.weapon_combo = QComboBox()
        self.weapon_combo.currentIndexChanged.connect(self._on_weapon_changed)
        weapon_layout.addRow("Weapon:", self.weapon_combo)
        weapon_group.setLayout(weapon_layout)
        layout.addWidget(weapon_group)
        
        ammo_group = QGroupBox("Ammunition")
        ammo_layout = QFormLayout()
        self.ammo_combo = QComboBox()
        ammo_layout.addRow("Ammo:", self.ammo_combo)
        ammo_group.setLayout(ammo_layout)
        layout.addWidget(ammo_group)
        
        layout.addStretch()
        return widget
    
    def _create_primary_target_step(self):
        """Step 2: Primary target & Range."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        target_group = QGroupBox("Primary Target")
        target_layout = QFormLayout()
        self.target_combo = QComboBox()
        target_layout.addRow("Character:", self.target_combo)
        target_group.setLayout(target_layout)
        layout.addWidget(target_group)
        
        range_group = QGroupBox("Range")
        range_layout = QFormLayout()
        self.range_spin = QSpinBox()
        self.range_spin.setRange(1, 500)
        self.range_spin.setValue(10)
        self.range_spin.valueChanged.connect(self._update_pattern_info)
        range_layout.addRow("Range (hexes):", self.range_spin)
        self.pattern_label = QLabel()
        range_layout.addRow("Pattern Radius:", self.pattern_label)
        range_group.setLayout(range_layout)
        layout.addWidget(range_group)
        
        layout.addStretch()
        return widget
    
    def _create_secondary_targets_step(self):
        """Step 3: Select secondary targets in pattern."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        info_label = QLabel("Select additional targets within pattern radius:")
        layout.addWidget(info_label)
        
        self.secondary_list = QListWidget()
        self.secondary_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        layout.addWidget(self.secondary_list)
        
        return widget
    
    def _create_common_params_step(self):
        """Step 4: Common parameters (shooter-related)."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        common_group = QGroupBox("Common Parameters (Shooter)")
        common_layout = QFormLayout()
        
        self.common_aim_spin = QSpinBox()
        self.common_aim_spin.setRange(0, 20)
        self.common_aim_spin.setValue(2)
        common_layout.addRow("Aim Time (AC):", self.common_aim_spin)
        
        self.common_stance_list = QListWidget()
        self.common_stance_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        for stance in SituationStanceModifier4B:
            self.common_stance_list.addItem(stance.name)
        common_layout.addRow("Stance:", self.common_stance_list)
        
        self.common_vis_list = QListWidget()
        self.common_vis_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        for vis in VisibilityModifier4C:
            self.common_vis_list.addItem(vis.name)
        common_layout.addRow("Visibility:", self.common_vis_list)
        
        self.common_shooter_speed_spin = QSpinBox()
        self.common_shooter_speed_spin.setRange(0, 20)
        self.common_shooter_speed_spin.setValue(0)
        common_layout.addRow("Shooter Speed (hex/imp):", self.common_shooter_speed_spin)
        
        self.common_shooter_duck_check = QCheckBox()
        common_layout.addRow("Shooter Reflexive Duck:", self.common_shooter_duck_check)
        
        common_group.setLayout(common_layout)
        layout.addWidget(common_group)
        layout.addStretch()
        
        return widget
    
    def _create_target_params_step(self):
        """Step 5: Per-target parameters."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        target_group = QGroupBox("Target-Specific Parameters")
        target_layout = QVBoxLayout()
        
        self.params_stack = QStackedWidget()
        target_layout.addWidget(self.params_stack)
        
        nav = QHBoxLayout()
        self.target_prev_btn = QPushButton("Previous Target")
        self.target_prev_btn.clicked.connect(self._prev_target)
        self.target_next_btn = QPushButton("Next Target")
        self.target_next_btn.clicked.connect(self._next_target)
        nav.addWidget(self.target_prev_btn)
        nav.addStretch()
        nav.addWidget(self.target_next_btn)
        target_layout.addLayout(nav)
        
        target_group.setLayout(target_layout)
        layout.addWidget(target_group)
        
        return widget
    
    def _create_results_step(self):
        """Step 5: Results display."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        results_group = QGroupBox("Results")
        results_layout = QVBoxLayout()
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        results_layout.addWidget(self.results_text)
        
        log_btn_layout = QHBoxLayout()
        self.show_log_btn = QPushButton("Show Detailed Log")
        self.show_log_btn.clicked.connect(self._show_log)
        self.show_log_btn.setEnabled(False)
        log_btn_layout.addWidget(self.show_log_btn)
        log_btn_layout.addStretch()
        results_layout.addLayout(log_btn_layout)
        
        results_group.setLayout(results_layout)
        layout.addWidget(results_group)
        
        return widget
    
    def _update_step_label(self):
        """Update step indicator."""
        steps = ["1. Shooter & Weapon", "2. Primary Target", "3. Secondary Targets", 
                "4. Common Parameters", "5. Target Parameters", "6. Results"]
        self.step_label.setText(f"Step {self.current_step + 1} of 6: {steps[self.current_step].split('. ')[1]}")
    
    def _previous_step(self):
        """Go to previous step."""
        if self.current_step > 0:
            self.current_step -= 1
            self.stack.setCurrentIndex(self.current_step)
            self._update_navigation()
    
    def _next_step(self):
        """Go to next step."""
        if self.current_step == 1:
            ammo = self.ammo_combo.currentData()
            range_hexes = self.range_spin.value()
            
            if ammo and ammo.ballistic_data:
                max_range = max(bd.range_hexes for bd in ammo.ballistic_data if not bd.beyond_max_range)
                if range_hexes > max_range:
                    QMessageBox.warning(self, "Out of Range",
                                       f"Target is beyond effective range.\\nMax: {max_range}, Current: {range_hexes}")
                    return
            
            self._populate_secondary_targets()
        
        if self.current_step == 3:
            self._build_params_pages()
        
        if self.current_step < 4:
            self.current_step += 1
            self.stack.setCurrentIndex(self.current_step)
            self._update_navigation()
    
    def _update_navigation(self):
        """Update navigation buttons."""
        self.prev_btn.setEnabled(self.current_step > 0)
        self.next_btn.setVisible(self.current_step < 4)
        self.simulate_btn.setVisible(self.current_step == 4)
        self._update_step_label()
    
    def _on_shooter_changed(self):
        """Update weapon list when shooter changes."""
        self.weapon_combo.clear()
        shooter = self.shooter_combo.currentData()
        if shooter:
            weapons = [item for item in shooter.equipment if isinstance(item, Weapon)]
            for weapon in weapons:
                self.weapon_combo.addItem(weapon.name, weapon)
            
            if hasattr(self, 'target_combo'):
                self.target_combo.clear()
                for char in self.characters:
                    if char != shooter:
                        self.target_combo.addItem(char.name, char)
        
        self._on_weapon_changed()
    
    def _on_weapon_changed(self):
        """Update ammo list when weapon changes."""
        self.ammo_combo.clear()
        weapon = self.weapon_combo.currentData()
        shooter = self.shooter_combo.currentData()
        if weapon and shooter and hasattr(weapon, 'ammunition_types'):
            shooter_ammo = [item for item in shooter.equipment if isinstance(item, AmmoType)]
            for ammo in weapon.ammunition_types:
                if ammo in shooter_ammo and hasattr(ammo, 'pellet_count') and ammo.pellet_count:
                    self.ammo_combo.addItem(ammo.name, ammo)
        self._update_pattern_info()
    
    def _update_pattern_info(self):
        """Update pattern radius display."""
        ammo = self.ammo_combo.currentData()
        range_hexes = self.range_spin.value()
        
        if ammo and ammo.ballistic_data:
            for bd in ammo.ballistic_data:
                if range_hexes <= bd.range_hexes:
                    if bd.pattern_radius is not None:
                        self.pattern_label.setText(f"{bd.pattern_radius} hexes")
                    else:
                        self.pattern_label.setText("N/A")
                    return
            self.pattern_label.setText("N/A")
    
    def _populate_secondary_targets(self):
        """Populate secondary targets list."""
        self.secondary_list.clear()
        shooter = self.shooter_combo.currentData()
        primary = self.target_combo.currentData()
        
        for char in self.characters:
            if char != shooter and char != primary:
                self.secondary_list.addItem(char.name)
    
    def _build_params_pages(self):
        """Build parameter pages for each target."""
        while self.params_stack.count() > 0:
            self.params_stack.removeWidget(self.params_stack.widget(0))
        
        self.target_params.clear()
        
        primary = self.target_combo.currentData()
        targets = [primary]
        
        for item in self.secondary_list.selectedItems():
            char_name = item.text()
            for char in self.characters:
                if char.name == char_name and char != self.shooter_combo.currentData():
                    targets.append(char)
                    break
        
        self.secondary_targets = targets[1:]
        
        for target in targets:
            page = self._create_target_params_page(target)
            self.params_stack.addWidget(page)
        
        self.params_stack.setCurrentIndex(0)
        self._update_target_nav()
    
    def _create_target_params_page(self, target: Character):
        """Create parameter page for a target."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        layout.addWidget(QLabel(f"<b>Target: {target.name}</b>"))
        
        params_group = QGroupBox("Target Parameters")
        params_layout = QFormLayout()
        
        range_spin = QSpinBox()
        range_spin.setRange(1, 500)
        range_spin.setValue(self.range_spin.value())
        params_layout.addRow("Range (hexes):", range_spin)
        
        exposure_combo = QComboBox()
        for exp in TargetExposure:
            exposure_combo.addItem(exp.name, exp)
        params_layout.addRow("Exposure:", exposure_combo)
        
        front_check = QCheckBox()
        front_check.setChecked(True)
        params_layout.addRow("Front Shot:", front_check)
        
        orient_combo = QComboBox()
        for orient in TargetOrientation:
            orient_combo.addItem(orient.name, orient)
        params_layout.addRow("Orientation:", orient_combo)
        
        target_speed_spin = QSpinBox()
        target_speed_spin.setRange(0, 20)
        target_speed_spin.setValue(0)
        params_layout.addRow("Target Speed (hex/imp):", target_speed_spin)
        
        target_duck_check = QCheckBox()
        params_layout.addRow("Target Reflexive Duck:", target_duck_check)
        
        params_group.setLayout(params_layout)
        layout.addWidget(params_group)
        
        self.target_params[target] = {
            'range': range_spin,
            'exposure': exposure_combo,
            'front': front_check,
            'orient': orient_combo,
            'target_speed': target_speed_spin,
            'target_duck': target_duck_check
        }
        
        return widget
    
    def _prev_target(self):
        """Go to previous target."""
        idx = self.params_stack.currentIndex()
        if idx > 0:
            self.params_stack.setCurrentIndex(idx - 1)
            self._update_target_nav()
    
    def _next_target(self):
        """Go to next target."""
        idx = self.params_stack.currentIndex()
        if idx < self.params_stack.count() - 1:
            self.params_stack.setCurrentIndex(idx + 1)
            self._update_target_nav()
    
    def _update_target_nav(self):
        """Update target navigation buttons."""
        idx = self.params_stack.currentIndex()
        self.target_prev_btn.setEnabled(idx > 0)
        self.target_next_btn.setEnabled(idx < self.params_stack.count() - 1)
    
    def _simulate(self):
        """Run shotgun simulation."""
        shooter = self.shooter_combo.currentData()
        weapon = self.weapon_combo.currentData()
        ammo = self.ammo_combo.currentData()
        primary = self.target_combo.currentData()
        
        targets = [primary] + self.secondary_targets
        ranges = []
        exposures = []
        shot_params_list = []
        is_front_shots = []
        
        # Get common parameters
        aim_ac = self.common_aim_spin.value()
        
        stance_mods = []
        for item in self.common_stance_list.selectedItems():
            stance_mods.append(list(SituationStanceModifier4B)[self.common_stance_list.row(item)])
        
        vis_mods = []
        for item in self.common_vis_list.selectedItems():
            vis_mods.append(list(VisibilityModifier4C)[self.common_vis_list.row(item)])
        
        shooter_speed = float(self.common_shooter_speed_spin.value())
        shooter_duck = self.common_shooter_duck_check.isChecked()
        
        # Build parameters for each target
        for target in targets:
            params = self.target_params[target]
            
            range_hexes = params['range'].value()
            if ammo.ballistic_data:
                max_range = max(bd.range_hexes for bd in ammo.ballistic_data if not bd.beyond_max_range)
                if range_hexes > max_range:
                    QMessageBox.warning(self, "Out of Range",
                                       f"{target.name} is beyond effective range.\\nMax: {max_range}, Current: {range_hexes}")
                    return
            
            ranges.append(range_hexes)
            exposures.append(params['exposure'].currentData())
            is_front_shots.append(params['front'].isChecked())
            
            shot_params = ShotParameters(
                aim_time_ac=aim_ac,
                situation_stance_modifiers=stance_mods,
                visibility_modifiers=vis_mods,
                target_orientation=params['orient'].currentData(),
                shooter_speed_hex_per_impulse=shooter_speed,
                target_speed_hex_per_impulse=float(params['target_speed'].value()),
                reflexive_duck_shooter=shooter_duck,
                reflexive_duck_target=params['target_duck'].isChecked()
            )
            shot_params_list.append(shot_params)
        
        results = CombatSimulator.shotgun_shot(
            shooter, targets, weapon, ammo, ranges, exposures, shot_params_list, is_front_shots, 0
        )
        
        self.last_results = results
        self.current_step = 5
        self.stack.setCurrentIndex(5)
        self._update_navigation()
        self._display_results(results)
        self.show_log_btn.setEnabled(True)
    
    def _display_results(self, results):
        """Display shotgun results."""
        text = f"<b>Shotgun Shot Results</b><br><br>"
        text += f"Total hits: {len([r for r in results if r.hit])}<br><br>"
        
        for i, result in enumerate(results):
            if result.hit and result.damage_result:
                dr = result.damage_result
                text += f"<b>Hit {i+1} - {result.target.name}</b><br>"
                text += f"<b>Hit Location:</b> {dr.location.name}<br>"
                text += f"<b>Damage:</b> {dr.damage}, <b>Shock:</b> {dr.shock}<br>"
                
                if dr.pierced_organs:
                    text += f"<b>Pierced Organs:</b> {', '.join(dr.pierced_organs)}<br>"
                
                if dr.is_disabled:
                    text += "<b>Target DISABLED</b><br>"
                
                text += "<br>"
                
                if result.incapacitation_effect:
                    text += f"<b>Incapacitation:</b> {result.incapacitation_effect.name}<br>"
                    if result.incapacitation_time_phases:
                        text += f"<b>Duration:</b> {result.incapacitation_time_phases} phases<br>"
                    text += "<br>"
                
                if result.recovery:
                    text += "<b>Recovery Data:</b><br>"
                    text += f"Healing Time: {result.recovery.healing_time_in_days:.1f} days<br>"
                    for aid, (ctp, chance) in result.recovery.aid_data.items():
                        if ctp is not None and chance is not None:
                            ctp_hours = ctp / 1800 if ctp >= 1800 else ctp / 30
                            ctp_unit = "hours" if ctp >= 1800 else "minutes"
                            text += f"{aid.name}: CTP {ctp_hours:.1f} {ctp_unit}, Recovery {chance}%<br>"
                    text += "<br>"
        
        self.results_text.setHtml(text)
    
    def _show_log(self):
        """Show detailed log."""
        if hasattr(self, 'last_results') and self.last_results:
            dialog = QDialog(self)
            dialog.setWindowTitle("Detailed Log")
            dialog.setMinimumSize(600, 400)
            layout = QVBoxLayout(dialog)
            
            log_text = QTextEdit()
            log_text.setReadOnly(True)
            log_text.setPlainText(self.last_results[0].log if self.last_results[0].log else "No log available")
            layout.addWidget(log_text)
            
            close_btn = QPushButton("Close")
            close_btn.clicked.connect(dialog.accept)
            layout.addWidget(close_btn)
            
            dialog.exec()
