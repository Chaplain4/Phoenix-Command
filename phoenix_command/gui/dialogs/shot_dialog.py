"""Single shot dialog."""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QComboBox, QSpinBox, QCheckBox, QPushButton,
                             QTextEdit, QMessageBox, QGroupBox, QFormLayout,
                             QStackedWidget, QListWidget, QWidget)

from phoenix_command.models.character import Character
from phoenix_command.models.enums import TargetExposure, SituationStanceModifier4B, VisibilityModifier4C, TargetOrientation
from phoenix_command.models.gear import Weapon, AmmoType
from phoenix_command.models.hit_result_advanced import ShotParameters
from phoenix_command.simulations.combat_simulator import CombatSimulator


class ShotDialog(QDialog):
    """Dialog for single shot simulation."""
    
    def __init__(self, characters: list[Character], parent=None):
        super().__init__(parent)
        self.characters = characters
        self.setWindowTitle("Single Shot")
        self.setMinimumSize(700, 600)
        self.current_step = 0
        
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
        self.stack.addWidget(self._create_target_step())
        self.stack.addWidget(self._create_stance_step())
        self.stack.addWidget(self._create_visibility_step())
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
    
    def _create_target_step(self):
        """Step 2: Target & Range."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        target_group = QGroupBox("Target")
        target_layout = QFormLayout()
        self.target_combo = QComboBox()
        target_layout.addRow("Character:", self.target_combo)
        target_group.setLayout(target_layout)
        layout.addWidget(target_group)
        
        params_group = QGroupBox("Basic Parameters")
        params_layout = QFormLayout()
        
        self.range_spin = QSpinBox()
        self.range_spin.setRange(1, 500)
        self.range_spin.setValue(10)
        params_layout.addRow("Range (hexes):", self.range_spin)
        
        self.exposure_combo = QComboBox()
        for exp in TargetExposure:
            self.exposure_combo.addItem(exp.name, exp)
        params_layout.addRow("Target Exposure:", self.exposure_combo)
        
        self.aim_spin = QSpinBox()
        self.aim_spin.setRange(0, 20)
        self.aim_spin.setValue(2)
        params_layout.addRow("Aim Time (AC):", self.aim_spin)
        
        self.front_check = QCheckBox()
        self.front_check.setChecked(True)
        params_layout.addRow("Front Shot:", self.front_check)
        
        self.target_orient_combo = QComboBox()
        for orient in TargetOrientation:
            self.target_orient_combo.addItem(orient.name, orient)
        params_layout.addRow("Target Orientation:", self.target_orient_combo)
        
        params_group.setLayout(params_layout)
        layout.addWidget(params_group)
        
        layout.addStretch()
        return widget
    
    def _create_stance_step(self):
        """Step 3: Stance & Situation modifiers."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        stance_group = QGroupBox("Situation & Stance Modifiers")
        stance_layout = QVBoxLayout()
        stance_layout.addWidget(QLabel("Select all applicable modifiers:"))
        self.stance_list = QListWidget()
        self.stance_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        for stance in SituationStanceModifier4B:
            self.stance_list.addItem(stance.name)
        stance_layout.addWidget(self.stance_list)
        stance_group.setLayout(stance_layout)
        layout.addWidget(stance_group)
        
        return widget
    
    def _create_visibility_step(self):
        """Step 4: Visibility & Movement."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        vis_group = QGroupBox("Visibility Modifiers")
        vis_layout = QVBoxLayout()
        vis_layout.addWidget(QLabel("Select all applicable modifiers:"))
        self.visibility_list = QListWidget()
        self.visibility_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        for vis in VisibilityModifier4C:
            self.visibility_list.addItem(vis.name)
        vis_layout.addWidget(self.visibility_list)
        vis_group.setLayout(vis_layout)
        layout.addWidget(vis_group)
        
        move_group = QGroupBox("Movement")
        move_layout = QFormLayout()
        
        self.shooter_speed_spin = QSpinBox()
        self.shooter_speed_spin.setRange(0, 20)
        self.shooter_speed_spin.setValue(0)
        move_layout.addRow("Shooter Speed (hex/imp):", self.shooter_speed_spin)
        
        self.target_speed_spin = QSpinBox()
        self.target_speed_spin.setRange(0, 20)
        self.target_speed_spin.setValue(0)
        move_layout.addRow("Target Speed (hex/imp):", self.target_speed_spin)
        
        self.shooter_duck_check = QCheckBox()
        move_layout.addRow("Shooter Reflexive Duck:", self.shooter_duck_check)
        
        self.target_duck_check = QCheckBox()
        move_layout.addRow("Target Reflexive Duck:", self.target_duck_check)
        
        move_group.setLayout(move_layout)
        layout.addWidget(move_group)
        
        prob_group = QGroupBox("Hit Probability")
        prob_layout = QVBoxLayout()
        self.prob_label = QLabel("Configure parameters to see probability")
        self.prob_label.setWordWrap(True)
        prob_layout.addWidget(self.prob_label)
        calc_prob_btn = QPushButton("Calculate Probability")
        calc_prob_btn.clicked.connect(self._calculate_probability)
        prob_layout.addWidget(calc_prob_btn)
        prob_group.setLayout(prob_layout)
        layout.addWidget(prob_group)
        
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
        steps = ["1. Shooter & Weapon", "2. Target & Range", "3. Stance & Situation", 
                "4. Visibility & Movement", "5. Results"]
        self.step_label.setText(f"Step {self.current_step + 1} of 5: {steps[self.current_step].split('. ')[1]}")
    
    def _previous_step(self):
        """Go to previous step."""
        if self.current_step > 0:
            self.current_step -= 1
            self.stack.setCurrentIndex(self.current_step)
            self._update_navigation()
    
    def _next_step(self):
        """Go to next step."""
        if self.current_step == 0:
            # Check for pellet ammo and switch to shotgun dialog
            ammo = self.ammo_combo.currentData()
            if ammo and hasattr(ammo, 'pellet_count') and ammo.pellet_count:
                from phoenix_command.gui.dialogs.shotgun_dialog import ShotgunDialog
                shooter = self.shooter_combo.currentData()
                weapon = self.weapon_combo.currentData()
                
                self.accept()
                dialog = ShotgunDialog(self.characters, self.parent())
                # Set shooter, weapon, ammo and go to step 2
                for i in range(dialog.shooter_combo.count()):
                    if dialog.shooter_combo.itemData(i) == shooter:
                        dialog.shooter_combo.setCurrentIndex(i)
                        break
                for i in range(dialog.weapon_combo.count()):
                    if dialog.weapon_combo.itemData(i) == weapon:
                        dialog.weapon_combo.setCurrentIndex(i)
                        break
                for i in range(dialog.ammo_combo.count()):
                    if dialog.ammo_combo.itemData(i) == ammo:
                        dialog.ammo_combo.setCurrentIndex(i)
                        break
                dialog.current_step = 1
                dialog.stack.setCurrentIndex(1)
                dialog._update_navigation()
                if dialog.exec():
                    # Log shotgun results to main window
                    if hasattr(dialog, 'last_results') and hasattr(self.parent(), 'combat_log'):
                        main_window = self.parent()
                        if shooter and weapon:
                            main_window.combat_log.append_system(f"{shooter.name} fires shotgun {weapon.name}")
                        for result in dialog.last_results:
                            main_window._log_shot_result(result)
                return
        
        if self.current_step == 1:
            # Validate range before leaving target step
            ammo = self.ammo_combo.currentData()
            range_hexes = self.range_spin.value()
            
            if ammo and ammo.ballistic_data:
                max_range = max(bd.range_hexes for bd in ammo.ballistic_data if not bd.beyond_max_range)
                if range_hexes > max_range:
                    QMessageBox.warning(self, "Out of Range",
                                       f"Target is beyond effective range for this ammunition.\n"
                                       f"Effective range: {max_range} hexes\n"
                                       f"Target range: {range_hexes} hexes")
                    return
        
        if self.current_step < 3:
            self.current_step += 1
            self.stack.setCurrentIndex(self.current_step)
            self._update_navigation()
    
    def _update_navigation(self):
        """Update navigation buttons."""
        self.prev_btn.setEnabled(self.current_step > 0)
        self.next_btn.setVisible(self.current_step < 3)
        self.simulate_btn.setVisible(self.current_step == 3)
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
                if ammo in shooter_ammo:
                    self.ammo_combo.addItem(ammo.name, ammo)
    
    def _simulate(self):
        """Run single shot simulation."""
        shooter = self.shooter_combo.currentData()
        weapon = self.weapon_combo.currentData()
        ammo = self.ammo_combo.currentData()
        target = self.target_combo.currentData()
        
        if not all([shooter, weapon, ammo, target]):
            QMessageBox.warning(self, "Error", "Please select all parameters")
            return
        
        if hasattr(ammo, 'explosive_data') and ammo.explosive_data:
            QMessageBox.information(self, "Not Implemented",
                                   "Explosive ammunition will be handled separately (coming soon)")
            return
        
        range_hexes = self.range_spin.value()
        exposure = self.exposure_combo.currentData()
        aim_ac = self.aim_spin.value()
        is_front = self.front_check.isChecked()
        
        stance_mods = []
        for item in self.stance_list.selectedItems():
            stance_mods.append(list(SituationStanceModifier4B)[self.stance_list.row(item)])
        
        vis_mods = []
        for item in self.visibility_list.selectedItems():
            vis_mods.append(list(VisibilityModifier4C)[self.visibility_list.row(item)])
        
        target_orient = self.target_orient_combo.currentData()
        shooter_speed = float(self.shooter_speed_spin.value())
        target_speed = float(self.target_speed_spin.value())
        shooter_duck = self.shooter_duck_check.isChecked()
        target_duck = self.target_duck_check.isChecked()
        
        shot_params = ShotParameters(
            aim_time_ac=aim_ac,
            situation_stance_modifiers=stance_mods,
            visibility_modifiers=vis_mods,
            target_orientation=target_orient,
            shooter_speed_hex_per_impulse=shooter_speed,
            target_speed_hex_per_impulse=target_speed,
            reflexive_duck_shooter=shooter_duck,
            reflexive_duck_target=target_duck
        )
        
        result = CombatSimulator.single_shot(
            shooter, target, weapon, ammo, range_hexes, exposure, shot_params, is_front
        )
        
        self.last_result = result

        main_window = self.window()
        while main_window and not hasattr(main_window, 'combat_log'):
            main_window = main_window.parent()

        if main_window and hasattr(main_window, 'combat_log'):
            main_window.combat_log.append_system(f"{shooter.name} shoots {weapon.name} at {target.name}")
            main_window._log_shot_result(result)
            if hasattr(main_window, 'combat_zone'):
                main_window.combat_zone.refresh_cards()
            if hasattr(main_window, 'stats_display') and hasattr(main_window, 'character_list'):
                current_row = main_window.character_list.currentRow()
                if current_row >= 0:
                    main_window._on_character_selected(current_row)

        self.current_step = 4
        self.stack.setCurrentIndex(4)
        self._update_navigation()
        self._display_result(result)
        self.show_log_btn.setEnabled(True)
    
    def _display_result(self, result):
        """Display shot result."""
        text = f"<b>{'HIT' if result.hit else 'MISS'}</b><br><br>"
        text += f"EAL: {result.eal}, Odds: {result.odds}%, Roll: {result.roll}<br><br>"
        
        if result.hit and result.damage_result:
            dr = result.damage_result
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
        
        self.results_text.setHtml(text)
    
    def _show_log(self):
        """Show detailed log in message box."""
        if hasattr(self, 'last_result') and self.last_result.log:
            dialog = QDialog(self)
            dialog.setWindowTitle("Detailed Log")
            dialog.setMinimumSize(600, 400)
            layout = QVBoxLayout(dialog)
            
            log_text = QTextEdit()
            log_text.setReadOnly(True)
            log_text.setPlainText(self.last_result.log)
            layout.addWidget(log_text)
            
            close_btn = QPushButton("Close")
            close_btn.clicked.connect(dialog.accept)
            layout.addWidget(close_btn)
            
            dialog.exec()
    
    def _calculate_probability(self):
        """Calculate and display hit probability."""
        from phoenix_command.simulations.combat_simulator_probabilities import CombatSimulatorProbabilities
        
        shooter = self.shooter_combo.currentData()
        weapon = self.weapon_combo.currentData()
        target = self.target_combo.currentData()
        
        if not all([shooter, weapon, target]):
            self.prob_label.setText("Please select shooter, weapon, and target")
            return
        
        range_hexes = self.range_spin.value()
        exposure = self.exposure_combo.currentData()
        aim_ac = self.aim_spin.value()
        
        stance_mods = []
        for item in self.stance_list.selectedItems():
            stance_mods.append(list(SituationStanceModifier4B)[self.stance_list.row(item)])
        
        vis_mods = []
        for item in self.visibility_list.selectedItems():
            vis_mods.append(list(VisibilityModifier4C)[self.visibility_list.row(item)])
        
        target_orient = self.target_orient_combo.currentData()
        shooter_speed = float(self.shooter_speed_spin.value())
        target_speed = float(self.target_speed_spin.value())
        shooter_duck = self.shooter_duck_check.isChecked()
        target_duck = self.target_duck_check.isChecked()
        
        shot_params = ShotParameters(
            aim_time_ac=aim_ac,
            situation_stance_modifiers=stance_mods,
            visibility_modifiers=vis_mods,
            target_orientation=target_orient,
            shooter_speed_hex_per_impulse=shooter_speed,
            target_speed_hex_per_impulse=target_speed,
            reflexive_duck_shooter=shooter_duck,
            reflexive_duck_target=target_duck
        )
        
        eal, odds = CombatSimulatorProbabilities.calculate_single_shot_probability(
            shooter, target, weapon, range_hexes, exposure, shot_params
        )
        
        self.prob_label.setText(f"<b>EAL:</b> {eal}<br><b>Hit Probability:</b> {odds}%")
