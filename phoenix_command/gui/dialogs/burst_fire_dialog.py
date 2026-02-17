"""Burst fire dialog."""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QComboBox, QSpinBox, QCheckBox, QPushButton,
                             QTextEdit, QMessageBox, QGroupBox, QFormLayout,
                             QStackedWidget, QListWidget, QWidget, QDoubleSpinBox)

from phoenix_command.models.character import Character
from phoenix_command.models.enums import TargetExposure, SituationStanceModifier4B, VisibilityModifier4C, TargetOrientation
from phoenix_command.models.gear import Weapon, AmmoType
from phoenix_command.models.hit_result_advanced import ShotParameters, TargetGroup
from phoenix_command.simulations.combat_simulator import CombatSimulator
from phoenix_command.simulations.combat_simulator_probabilities import CombatSimulatorProbabilities


class BurstFireDialog(QDialog):
    """Dialog for burst fire simulation."""

    def __init__(self, characters: list[Character], parent=None):
        super().__init__(parent)
        self.characters = characters
        self.setWindowTitle("Burst Fire")
        self.setMinimumSize(750, 650)
        self.current_step = 0
        self.selected_targets = []
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

        self.stack.addWidget(self._create_shooter_step())      # Step 1: Shooter & Weapon
        self.stack.addWidget(self._create_common_params_step()) # Step 2: Common parameters
        self.stack.addWidget(self._create_targets_step())       # Step 3: Select targets & arc
        self.stack.addWidget(self._create_target_params_step()) # Step 4: Per-target parameters
        self.stack.addWidget(self._create_results_step())       # Step 5: Results

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

        weapon_group = QGroupBox("Weapon (Full Auto capable)")
        weapon_layout = QFormLayout()
        self.weapon_combo = QComboBox()
        self.weapon_combo.currentIndexChanged.connect(self._on_weapon_changed)
        weapon_layout.addRow("Weapon:", self.weapon_combo)

        self.weapon_info_label = QLabel()
        self.weapon_info_label.setWordWrap(True)
        weapon_layout.addRow("Info:", self.weapon_info_label)
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

    def _create_common_params_step(self):
        """Step 2: Common parameters (shooter-related)."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        common_group = QGroupBox("Common Parameters (Shooter)")
        common_layout = QFormLayout()

        self.common_aim_spin = QSpinBox()
        self.common_aim_spin.setRange(0, 20)
        self.common_aim_spin.setValue(2)
        common_layout.addRow("Aim Time (AC):", self.common_aim_spin)

        self.continuous_burst_spin = QSpinBox()
        self.continuous_burst_spin.setRange(0, 10)
        self.continuous_burst_spin.setValue(0)
        self.continuous_burst_spin.setToolTip("Number of impulses of continuous burst fire (SAB penalty)")
        common_layout.addRow("Continuous Burst Impulses:", self.continuous_burst_spin)

        common_group.setLayout(common_layout)
        layout.addWidget(common_group)

        stance_group = QGroupBox("Situation & Stance Modifiers")
        stance_layout = QVBoxLayout()
        stance_layout.addWidget(QLabel("Select all applicable modifiers:"))
        self.common_stance_list = QListWidget()
        self.common_stance_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        for stance in SituationStanceModifier4B:
            self.common_stance_list.addItem(stance.name)
        stance_layout.addWidget(self.common_stance_list)
        stance_group.setLayout(stance_layout)
        layout.addWidget(stance_group)

        vis_group = QGroupBox("Visibility Modifiers")
        vis_layout = QVBoxLayout()
        self.common_vis_list = QListWidget()
        self.common_vis_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        for vis in VisibilityModifier4C:
            self.common_vis_list.addItem(vis.name)
        vis_layout.addWidget(self.common_vis_list)
        vis_group.setLayout(vis_layout)
        layout.addWidget(vis_group)

        move_group = QGroupBox("Shooter Movement")
        move_layout = QFormLayout()
        self.common_shooter_speed_spin = QSpinBox()
        self.common_shooter_speed_spin.setRange(0, 20)
        self.common_shooter_speed_spin.setValue(0)
        move_layout.addRow("Shooter Speed (hex/imp):", self.common_shooter_speed_spin)

        self.common_shooter_duck_check = QCheckBox()
        move_layout.addRow("Shooter Reflexive Duck:", self.common_shooter_duck_check)
        move_group.setLayout(move_layout)
        layout.addWidget(move_group)

        return widget

    def _create_targets_step(self):
        """Step 3: Select targets and arc of fire."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        targets_group = QGroupBox("Select Targets")
        targets_layout = QVBoxLayout()
        targets_layout.addWidget(QLabel("Select one or more targets for the burst:"))
        self.targets_list = QListWidget()
        self.targets_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        targets_layout.addWidget(self.targets_list)
        targets_group.setLayout(targets_layout)
        layout.addWidget(targets_group)

        arc_group = QGroupBox("Arc of Fire")
        arc_layout = QFormLayout()

        self.arc_auto_check = QCheckBox("Use minimum effective arc")
        self.arc_auto_check.setChecked(True)
        self.arc_auto_check.stateChanged.connect(self._on_arc_auto_changed)
        arc_layout.addRow(self.arc_auto_check)

        self.arc_spin = QDoubleSpinBox()
        self.arc_spin.setRange(0.1, 2000.0)
        self.arc_spin.setValue(1.0)
        self.arc_spin.setSuffix(" hexes")
        self.arc_spin.setEnabled(False)
        arc_layout.addRow("Custom Arc:", self.arc_spin)

        self.arc_info_label = QLabel("Arc will be calculated based on weapon and stance")
        self.arc_info_label.setWordWrap(True)
        arc_layout.addRow("", self.arc_info_label)

        arc_group.setLayout(arc_layout)
        layout.addWidget(arc_group)

        layout.addStretch()
        return widget

    def _create_target_params_step(self):
        """Step 4: Per-target parameters."""
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
        self.target_label = QLabel()
        nav.addWidget(self.target_prev_btn)
        nav.addWidget(self.target_label)
        nav.addStretch()
        nav.addWidget(self.target_next_btn)
        target_layout.addLayout(nav)

        target_group.setLayout(target_layout)
        layout.addWidget(target_group)

        # Probability display section
        prob_group = QGroupBox("Target Hit Probability")
        prob_layout = QVBoxLayout()
        self.target_prob_label = QLabel("Configure parameters to see probability")
        self.target_prob_label.setWordWrap(True)
        prob_layout.addWidget(self.target_prob_label)
        calc_prob_btn = QPushButton("Calculate Probability for Current Target")
        calc_prob_btn.clicked.connect(self._calculate_target_probability)
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
        steps = ["1. Shooter & Weapon", "2. Common Parameters", "3. Select Targets",
                "4. Target Parameters", "5. Results"]
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
            # Validate weapon selection
            weapon = self.weapon_combo.currentData()
            if not weapon:
                QMessageBox.warning(self, "Error", "Please select a weapon")
                return
            if not weapon.full_auto or not weapon.full_auto_rof:
                QMessageBox.warning(self, "Error", "Selected weapon is not full auto capable")
                return

            # Check for pellet ammo and switch to shotgun burst fire dialog
            ammo = self.ammo_combo.currentData()
            if ammo and hasattr(ammo, 'pellet_count') and ammo.pellet_count:
                from phoenix_command.gui.dialogs.shotgun_burst_fire_dialog import ShotgunBurstFireDialog
                shooter = self.shooter_combo.currentData()

                self.accept()
                dialog = ShotgunBurstFireDialog(
                    self.characters, self.parent(),
                    preset_shooter=shooter, preset_weapon=weapon, preset_ammo=ammo
                )
                # Set shooter, weapon, ammo
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
                # Go to step 2 (common parameters)
                dialog.current_step = 1
                dialog.stack.setCurrentIndex(1)
                dialog._update_navigation()
                dialog.exec()
                return

        if self.current_step == 2:
            # Validate target selection
            selected = self.targets_list.selectedItems()
            if not selected:
                QMessageBox.warning(self, "Error", "Please select at least one target")
                return
            self._build_params_pages()

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

        if self.current_step == 2:
            self._populate_targets_list()

    def _on_shooter_changed(self):
        """Update weapon list when shooter changes."""
        self.weapon_combo.clear()
        shooter = self.shooter_combo.currentData()
        if shooter:
            weapons = [item for item in shooter.equipment if isinstance(item, Weapon)]
            for weapon in weapons:
                # Only show full auto capable weapons
                if weapon.full_auto and weapon.full_auto_rof:
                    self.weapon_combo.addItem(f"{weapon.name} (ROF: {weapon.full_auto_rof})", weapon)

        self._on_weapon_changed()

    def _on_weapon_changed(self):
        """Update ammo list and info when weapon changes."""
        self.ammo_combo.clear()
        weapon = self.weapon_combo.currentData()
        shooter = self.shooter_combo.currentData()

        if weapon:
            info = f"ROF: {weapon.full_auto_rof}"
            if weapon.sustained_auto_burst:
                info += f", SAB: {weapon.sustained_auto_burst}"
            if weapon.ballistic_data:
                min_arc = weapon.ballistic_data.get_minimum_arc(10)
                if min_arc:
                    info += f", Min Arc: {min_arc}°"
            self.weapon_info_label.setText(info)
        else:
            self.weapon_info_label.setText("")

        if weapon and shooter and hasattr(weapon, 'ammunition_types'):
            shooter_ammo = [item for item in shooter.equipment if isinstance(item, AmmoType)]
            for ammo in weapon.ammunition_types:
                if ammo in shooter_ammo:
                    self.ammo_combo.addItem(ammo.name, ammo)

    def _on_arc_auto_changed(self, state):
        """Toggle custom arc input."""
        self.arc_spin.setEnabled(not state)

    def _populate_targets_list(self):
        """Populate targets list."""
        self.targets_list.clear()
        shooter = self.shooter_combo.currentData()

        for char in self.characters:
            if char != shooter:
                self.targets_list.addItem(char.name)

    def _build_params_pages(self):
        """Build parameter pages for each selected target."""
        # Clear existing pages
        while self.params_stack.count() > 0:
            self.params_stack.removeWidget(self.params_stack.widget(0))

        self.target_params.clear()
        self.selected_targets = []

        shooter = self.shooter_combo.currentData()

        for item in self.targets_list.selectedItems():
            char_name = item.text()
            for char in self.characters:
                if char.name == char_name and char != shooter:
                    self.selected_targets.append(char)
                    break

        for target in self.selected_targets:
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
        range_spin.setValue(10)
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

        layout.addStretch()
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
        count = self.params_stack.count()
        self.target_prev_btn.setEnabled(idx > 0)
        self.target_next_btn.setEnabled(idx < count - 1)
        if count > 0 and idx < len(self.selected_targets):
            self.target_label.setText(f"Target {idx + 1} of {count}: {self.selected_targets[idx].name}")

    def _simulate(self):
        """Run burst fire simulation."""
        shooter = self.shooter_combo.currentData()
        weapon = self.weapon_combo.currentData()
        ammo = self.ammo_combo.currentData()

        if not all([shooter, weapon, ammo]) or not self.selected_targets:
            QMessageBox.warning(self, "Error", "Please select all parameters and targets")
            return

        # Get common parameters
        aim_ac = self.common_aim_spin.value()
        continuous_burst = self.continuous_burst_spin.value()

        stance_mods = []
        for item in self.common_stance_list.selectedItems():
            stance_mods.append(list(SituationStanceModifier4B)[self.common_stance_list.row(item)])

        vis_mods = []
        for item in self.common_vis_list.selectedItems():
            vis_mods.append(list(VisibilityModifier4C)[self.common_vis_list.row(item)])

        shooter_speed = float(self.common_shooter_speed_spin.value())
        shooter_duck = self.common_shooter_duck_check.isChecked()

        # Get arc of fire
        arc_of_fire = None if self.arc_auto_check.isChecked() else self.arc_spin.value()

        # Build target group
        targets = []
        ranges = []
        exposures = []
        shot_params_list = []
        is_front_shots = []

        for target in self.selected_targets:
            params = self.target_params[target]

            targets.append(target)
            ranges.append(params['range'].value())
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

        target_group = TargetGroup(
            targets=targets,
            ranges=ranges,
            exposures=exposures,
            shot_params_list=shot_params_list,
            is_front_shots=is_front_shots
        )

        results = CombatSimulator.burst_fire(
            shooter, weapon, ammo, target_group, arc_of_fire, continuous_burst
        )

        self.last_results = results

        # Сразу логируем и обновляем карточки в главном окне
        main_window = self.window()
        while main_window and not hasattr(main_window, 'combat_log'):
            main_window = main_window.parent()

        if main_window and hasattr(main_window, 'combat_log'):
            target_names = ", ".join([t.name for t in targets])
            main_window.combat_log.append_system(f"{shooter.name} fires burst from {weapon.name} at {target_names}")
            for result in results:
                main_window._log_shot_result(result)
            if hasattr(main_window, 'combat_zone'):
                main_window.combat_zone.refresh_cards()
            # Обновляем отображение характеристик
            if hasattr(main_window, 'stats_display') and hasattr(main_window, 'character_list'):
                current_row = main_window.character_list.currentRow()
                if current_row >= 0:
                    main_window._on_character_selected(current_row)

        self.current_step = 4
        self.stack.setCurrentIndex(4)
        self._update_navigation()
        self._display_results(results)
        self.show_log_btn.setEnabled(True)

    def _display_results(self, results):
        """Display burst fire results."""
        text = "<b>Burst Fire Results</b><br><br>"

        hits_by_target = {}
        for result in results:
            if result.hit and result.target:
                target_name = result.target.name
                if target_name not in hits_by_target:
                    hits_by_target[target_name] = []
                hits_by_target[target_name].append(result)

        total_hits = sum(len(h) for h in hits_by_target.values())
        text += f"Total hits: {total_hits}<br><br>"

        if not hits_by_target:
            text += "<b>No targets hit</b><br>"
        else:
            for target_name, target_results in hits_by_target.items():
                text += f"<b>{target_name}</b>: {len(target_results)} hits<br>"

                for i, result in enumerate(target_results):
                    if result.damage_result:
                        dr = result.damage_result
                        text += f"  Hit {i+1}: {dr.location.name} - {dr.damage} damage, {dr.shock} shock"

                        if dr.pierced_organs:
                            text += f" (Pierced: {', '.join(dr.pierced_organs)})"

                        if dr.is_disabled:
                            text += " <b>[DISABLED]</b>"

                        text += "<br>"

                        if result.incapacitation_effect:
                            text += f"    Incap: {result.incapacitation_effect.name}"
                            if result.incapacitation_time_phases:
                                text += f" ({result.incapacitation_time_phases} phases)"
                            text += "<br>"

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

    def _calculate_target_probability(self):
        """Calculate and display the hit probability for the current target."""
        idx = self.params_stack.currentIndex()
        if idx < 0 or idx >= len(self.selected_targets):
            self.target_prob_label.setText("No target selected")
            return

        shooter = self.shooter_combo.currentData()
        weapon = self.weapon_combo.currentData()

        if not shooter or not weapon:
            self.target_prob_label.setText("Please select shooter and weapon")
            return

        target = self.selected_targets[idx]
        params = self.target_params[target]

        # Get common parameters
        aim_ac = self.common_aim_spin.value()
        continuous_burst = self.continuous_burst_spin.value()

        stance_mods = []
        for item in self.common_stance_list.selectedItems():
            stance_mods.append(list(SituationStanceModifier4B)[self.common_stance_list.row(item)])

        vis_mods = []
        for item in self.common_vis_list.selectedItems():
            vis_mods.append(list(VisibilityModifier4C)[self.common_vis_list.row(item)])

        shooter_speed = float(self.common_shooter_speed_spin.value())
        shooter_duck = self.common_shooter_duck_check.isChecked()

        # Get arc of fire
        arc_of_fire = None if self.arc_auto_check.isChecked() else self.arc_spin.value()

        # Build shot parameters
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

        range_hexes = params['range'].value()
        exposure = params['exposure'].currentData()

        # Calculate probability using the proper method
        eal, elevation_odds, effective_arc, hits_info = CombatSimulatorProbabilities.calculate_burst_fire_probabilities(
            shooter, target, weapon, range_hexes, exposure, shot_params, arc_of_fire, continuous_burst
        )

        text = f"<b>Target: {target.name}</b><br>"
        text += f"<b>EAL:</b> {eal}<br>"
        text += f"<b>Elevation Hit Probability:</b> {elevation_odds}%<br>"
        text += f"<b>Effective Arc:</b> {effective_arc:.2f} hexes<br>"
        text += f"<b>Hits (if elevation succeeds):</b> {hits_info}"

        self.target_prob_label.setText(text)
