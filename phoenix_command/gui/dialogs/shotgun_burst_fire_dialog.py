"""Shotgun burst fire dialog."""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QComboBox, QSpinBox, QCheckBox, QPushButton,
                             QTextEdit, QMessageBox, QGroupBox, QFormLayout,
                             QStackedWidget, QListWidget, QWidget, QDoubleSpinBox)

from phoenix_command.models.character import Character
from phoenix_command.models.enums import TargetExposure, SituationStanceModifier4B, VisibilityModifier4C, TargetOrientation
from phoenix_command.models.gear import Weapon, AmmoType
from phoenix_command.models.hit_result_advanced import ShotParameters, TargetGroup
from phoenix_command.simulations.combat_simulator import CombatSimulator


class ShotgunBurstFireDialog(QDialog):
    """Dialog for shotgun burst fire simulation (full auto with pellet ammo)."""

    def __init__(self, characters: list[Character], parent=None,
                 preset_shooter=None, preset_weapon=None, preset_ammo=None):
        super().__init__(parent)
        self.characters = characters
        self.setWindowTitle("Shotgun Burst Fire")
        self.setMinimumSize(800, 700)
        self.current_step = 0
        self.primary_targets = []  # Primary targets in burst arc
        self.primary_target_params = {}  # Parameters for primary targets
        self.pattern_targets = {}  # Secondary targets for each primary target {primary: [secondaries]}
        self.pattern_target_params = {}  # Parameters for secondary targets {target: params}

        # Preset values from burst fire dialog
        self.preset_shooter = preset_shooter
        self.preset_weapon = preset_weapon
        self.preset_ammo = preset_ammo

        self._setup_ui()

    def _setup_ui(self):
        """Setup UI components."""
        layout = QVBoxLayout(self)

        self.step_label = QLabel()
        self.step_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(self.step_label)

        self.stack = QStackedWidget()
        layout.addWidget(self.stack)

        # Steps:
        # 1. Shooter & Weapon (can be preset)
        # 2. Common parameters (shooter-related)
        # 3. Select primary targets & arc (like burst fire)
        # 4. Primary target parameters
        # 5. Secondary targets selection (per primary, like shotgun)
        # 6. Secondary target parameters
        # 7. Results

        self.stack.addWidget(self._create_shooter_step())           # Step 1
        self.stack.addWidget(self._create_common_params_step())     # Step 2
        self.stack.addWidget(self._create_primary_targets_step())   # Step 3
        self.stack.addWidget(self._create_primary_params_step())    # Step 4
        self.stack.addWidget(self._create_secondary_targets_step()) # Step 5
        self.stack.addWidget(self._create_secondary_params_step())  # Step 6
        self.stack.addWidget(self._create_results_step())           # Step 7

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

        # Apply presets if provided
        if self.preset_shooter:
            for i in range(self.shooter_combo.count()):
                if self.shooter_combo.itemData(i) == self.preset_shooter:
                    self.shooter_combo.setCurrentIndex(i)
                    break

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

        weapon_group = QGroupBox("Weapon (Full Auto with Shotgun Ammo)")
        weapon_layout = QFormLayout()
        self.weapon_combo = QComboBox()
        self.weapon_combo.currentIndexChanged.connect(self._on_weapon_changed)
        weapon_layout.addRow("Weapon:", self.weapon_combo)

        self.weapon_info_label = QLabel()
        self.weapon_info_label.setWordWrap(True)
        weapon_layout.addRow("Info:", self.weapon_info_label)
        weapon_group.setLayout(weapon_layout)
        layout.addWidget(weapon_group)

        ammo_group = QGroupBox("Ammunition (Pellet)")
        ammo_layout = QFormLayout()
        self.ammo_combo = QComboBox()
        self.ammo_combo.currentIndexChanged.connect(self._on_ammo_changed)
        ammo_layout.addRow("Ammo:", self.ammo_combo)

        self.ammo_info_label = QLabel()
        self.ammo_info_label.setWordWrap(True)
        ammo_layout.addRow("Info:", self.ammo_info_label)
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

    def _create_primary_targets_step(self):
        """Step 3: Select primary targets and arc of fire."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        info_label = QLabel("Select primary targets in the burst arc (each will receive a shotgun pattern):")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)

        targets_group = QGroupBox("Select Primary Targets")
        targets_layout = QVBoxLayout()
        self.primary_targets_list = QListWidget()
        self.primary_targets_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        targets_layout.addWidget(self.primary_targets_list)
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

    def _create_primary_params_step(self):
        """Step 4: Per-primary-target parameters."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        target_group = QGroupBox("Primary Target Parameters")
        target_layout = QVBoxLayout()

        self.primary_params_stack = QStackedWidget()
        target_layout.addWidget(self.primary_params_stack)

        nav = QHBoxLayout()
        self.primary_prev_btn = QPushButton("Previous Target")
        self.primary_prev_btn.clicked.connect(self._prev_primary_target)
        self.primary_next_btn = QPushButton("Next Target")
        self.primary_next_btn.clicked.connect(self._next_primary_target)
        self.primary_target_label = QLabel()
        nav.addWidget(self.primary_prev_btn)
        nav.addWidget(self.primary_target_label)
        nav.addStretch()
        nav.addWidget(self.primary_next_btn)
        target_layout.addLayout(nav)

        target_group.setLayout(target_layout)
        layout.addWidget(target_group)

        # Pattern radius info
        pattern_group = QGroupBox("Shotgun Pattern Info")
        pattern_layout = QVBoxLayout()
        self.pattern_info_label = QLabel("Pattern radius will be shown based on range")
        self.pattern_info_label.setWordWrap(True)
        pattern_layout.addWidget(self.pattern_info_label)
        pattern_group.setLayout(pattern_layout)
        layout.addWidget(pattern_group)

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

    def _create_secondary_targets_step(self):
        """Step 5: Select secondary targets for each primary target's pattern."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        info_label = QLabel("Select secondary targets within each primary target's shotgun pattern radius:")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)

        self.secondary_targets_stack = QStackedWidget()
        layout.addWidget(self.secondary_targets_stack)

        nav = QHBoxLayout()
        self.secondary_group_prev_btn = QPushButton("Previous Primary")
        self.secondary_group_prev_btn.clicked.connect(self._prev_secondary_group)
        self.secondary_group_next_btn = QPushButton("Next Primary")
        self.secondary_group_next_btn.clicked.connect(self._next_secondary_group)
        self.secondary_group_label = QLabel()
        nav.addWidget(self.secondary_group_prev_btn)
        nav.addWidget(self.secondary_group_label)
        nav.addStretch()
        nav.addWidget(self.secondary_group_next_btn)
        layout.addLayout(nav)

        return widget

    def _create_secondary_params_step(self):
        """Step 6: Per-secondary-target parameters."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        target_group = QGroupBox("Secondary Target Parameters")
        target_layout = QVBoxLayout()

        self.secondary_params_stack = QStackedWidget()
        target_layout.addWidget(self.secondary_params_stack)

        nav = QHBoxLayout()
        self.secondary_prev_btn = QPushButton("Previous Target")
        self.secondary_prev_btn.clicked.connect(self._prev_secondary_target)
        self.secondary_next_btn = QPushButton("Next Target")
        self.secondary_next_btn.clicked.connect(self._next_secondary_target)
        self.secondary_target_label = QLabel()
        nav.addWidget(self.secondary_prev_btn)
        nav.addWidget(self.secondary_target_label)
        nav.addStretch()
        nav.addWidget(self.secondary_next_btn)
        target_layout.addLayout(nav)

        target_group.setLayout(target_layout)
        layout.addWidget(target_group)

        return widget

    def _create_results_step(self):
        """Step 7: Results display."""
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
        steps = ["1. Shooter & Weapon", "2. Common Parameters", "3. Primary Targets",
                "4. Primary Target Params", "5. Secondary Targets", "6. Secondary Target Params", "7. Results"]
        self.step_label.setText(f"Step {self.current_step + 1} of 7: {steps[self.current_step].split('. ')[1]}")

    def _previous_step(self):
        """Go to previous step."""
        if self.current_step > 0:
            self.current_step -= 1
            self.stack.setCurrentIndex(self.current_step)
            self._update_navigation()

    def _next_step(self):
        """Go to next step."""
        if self.current_step == 0:
            # Validate weapon and ammo selection
            weapon = self.weapon_combo.currentData()
            ammo = self.ammo_combo.currentData()
            if not weapon:
                QMessageBox.warning(self, "Error", "Please select a weapon")
                return
            if not weapon.full_auto or not weapon.full_auto_rof:
                QMessageBox.warning(self, "Error", "Selected weapon is not full auto capable")
                return
            if not ammo or not ammo.pellet_count:
                QMessageBox.warning(self, "Error", "Please select pellet ammunition")
                return

        if self.current_step == 2:
            # Validate primary target selection
            selected = self.primary_targets_list.selectedItems()
            if not selected:
                QMessageBox.warning(self, "Error", "Please select at least one primary target")
                return
            self._build_primary_params_pages()

        if self.current_step == 3:
            # Build secondary targets selection pages
            self._build_secondary_targets_pages()

        if self.current_step == 4:
            # Build secondary params pages
            self._build_secondary_params_pages()

        if self.current_step < 5:
            self.current_step += 1
            self.stack.setCurrentIndex(self.current_step)
            self._update_navigation()

    def _update_navigation(self):
        """Update navigation buttons."""
        self.prev_btn.setEnabled(self.current_step > 0)
        self.next_btn.setVisible(self.current_step < 5)
        self.simulate_btn.setVisible(self.current_step == 5)
        self._update_step_label()

        if self.current_step == 2:
            self._populate_primary_targets_list()

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

        # Apply preset weapon if available
        if self.preset_weapon:
            for i in range(self.weapon_combo.count()):
                if self.weapon_combo.itemData(i) == self.preset_weapon:
                    self.weapon_combo.setCurrentIndex(i)
                    break

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
                # Only show pellet ammo
                if ammo in shooter_ammo and hasattr(ammo, 'pellet_count') and ammo.pellet_count:
                    self.ammo_combo.addItem(ammo.name, ammo)

        self._on_ammo_changed()

        # Apply preset ammo if available
        if self.preset_ammo:
            for i in range(self.ammo_combo.count()):
                if self.ammo_combo.itemData(i) == self.preset_ammo:
                    self.ammo_combo.setCurrentIndex(i)
                    break

    def _on_ammo_changed(self):
        """Update ammo info when ammo changes."""
        ammo = self.ammo_combo.currentData()
        if ammo:
            info = f"Pellet count: {ammo.pellet_count}"
            if ammo.ballistic_data:
                for bd in ammo.ballistic_data:
                    if bd.pattern_radius is not None:
                        info += f"\nPattern radius at {bd.range_hexes} hex: {bd.pattern_radius}"
                        break
            self.ammo_info_label.setText(info)
        else:
            self.ammo_info_label.setText("")

    def _on_arc_auto_changed(self, state):
        """Toggle custom arc input."""
        self.arc_spin.setEnabled(not state)

    def _populate_primary_targets_list(self):
        """Populate primary targets list."""
        self.primary_targets_list.clear()
        shooter = self.shooter_combo.currentData()

        for char in self.characters:
            if char != shooter:
                self.primary_targets_list.addItem(char.name)

    def _build_primary_params_pages(self):
        """Build parameter pages for each primary target."""
        # Clear existing pages
        while self.primary_params_stack.count() > 0:
            self.primary_params_stack.removeWidget(self.primary_params_stack.widget(0))

        self.primary_target_params.clear()
        self.primary_targets = []

        shooter = self.shooter_combo.currentData()

        for item in self.primary_targets_list.selectedItems():
            char_name = item.text()
            for char in self.characters:
                if char.name == char_name and char != shooter:
                    self.primary_targets.append(char)
                    break

        for target in self.primary_targets:
            page = self._create_primary_target_params_page(target)
            self.primary_params_stack.addWidget(page)

        self.primary_params_stack.setCurrentIndex(0)
        self._update_primary_target_nav()

    def _create_primary_target_params_page(self, target: Character):
        """Create parameter page for a primary target."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        layout.addWidget(QLabel(f"<b>Primary Target: {target.name}</b>"))

        params_group = QGroupBox("Target Parameters")
        params_layout = QFormLayout()

        range_spin = QSpinBox()
        range_spin.setRange(1, 500)
        range_spin.setValue(10)
        range_spin.valueChanged.connect(lambda: self._update_pattern_info_for_target(target))
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

        self.primary_target_params[target] = {
            'range': range_spin,
            'exposure': exposure_combo,
            'front': front_check,
            'orient': orient_combo,
            'target_speed': target_speed_spin,
            'target_duck': target_duck_check
        }

        layout.addStretch()
        return widget

    def _update_pattern_info_for_target(self, target: Character):
        """Update pattern info when range changes."""
        if target not in self.primary_target_params:
            return

        ammo = self.ammo_combo.currentData()
        range_hexes = self.primary_target_params[target]['range'].value()

        if ammo and ammo.ballistic_data:
            for bd in ammo.ballistic_data:
                if range_hexes <= bd.range_hexes:
                    if bd.pattern_radius is not None:
                        self.pattern_info_label.setText(
                            f"Pattern radius at {range_hexes} hex: {bd.pattern_radius} hexes"
                        )
                    else:
                        self.pattern_info_label.setText("No pattern data at this range")
                    return
            self.pattern_info_label.setText("Out of range")

    def _prev_primary_target(self):
        """Go to previous primary target."""
        idx = self.primary_params_stack.currentIndex()
        if idx > 0:
            self.primary_params_stack.setCurrentIndex(idx - 1)
            self._update_primary_target_nav()

    def _next_primary_target(self):
        """Go to next primary target."""
        idx = self.primary_params_stack.currentIndex()
        if idx < self.primary_params_stack.count() - 1:
            self.primary_params_stack.setCurrentIndex(idx + 1)
            self._update_primary_target_nav()

    def _update_primary_target_nav(self):
        """Update primary target navigation buttons."""
        idx = self.primary_params_stack.currentIndex()
        count = self.primary_params_stack.count()
        self.primary_prev_btn.setEnabled(idx > 0)
        self.primary_next_btn.setEnabled(idx < count - 1)
        if count > 0 and idx < len(self.primary_targets):
            self.primary_target_label.setText(f"Primary {idx + 1} of {count}: {self.primary_targets[idx].name}")
            self._update_pattern_info_for_target(self.primary_targets[idx])

    def _build_secondary_targets_pages(self):
        """Build secondary target selection pages for each primary target."""
        # Clear existing pages
        while self.secondary_targets_stack.count() > 0:
            self.secondary_targets_stack.removeWidget(self.secondary_targets_stack.widget(0))

        self.pattern_targets.clear()
        self.secondary_lists = {}  # Store list widgets for each primary

        shooter = self.shooter_combo.currentData()
        ammo = self.ammo_combo.currentData()

        for primary in self.primary_targets:
            page = QWidget()
            layout = QVBoxLayout(page)

            range_hexes = self.primary_target_params[primary]['range'].value()
            pattern_radius = None
            if ammo and ammo.ballistic_data:
                for bd in ammo.ballistic_data:
                    if range_hexes <= bd.range_hexes:
                        pattern_radius = bd.pattern_radius
                        break

            layout.addWidget(QLabel(f"<b>Primary: {primary.name}</b>"))
            if pattern_radius:
                layout.addWidget(QLabel(f"Pattern radius: {pattern_radius} hexes"))
            layout.addWidget(QLabel("Select secondary targets within pattern:"))

            secondary_list = QListWidget()
            secondary_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)

            # Add all other characters except shooter and this primary
            for char in self.characters:
                if char != shooter and char != primary:
                    secondary_list.addItem(char.name)

            layout.addWidget(secondary_list)
            self.secondary_lists[primary] = secondary_list

            self.secondary_targets_stack.addWidget(page)

        self.secondary_targets_stack.setCurrentIndex(0)
        self._update_secondary_group_nav()

    def _prev_secondary_group(self):
        """Go to previous primary's secondary selection."""
        idx = self.secondary_targets_stack.currentIndex()
        if idx > 0:
            self.secondary_targets_stack.setCurrentIndex(idx - 1)
            self._update_secondary_group_nav()

    def _next_secondary_group(self):
        """Go to next primary's secondary selection."""
        idx = self.secondary_targets_stack.currentIndex()
        if idx < self.secondary_targets_stack.count() - 1:
            self.secondary_targets_stack.setCurrentIndex(idx + 1)
            self._update_secondary_group_nav()

    def _update_secondary_group_nav(self):
        """Update secondary group navigation buttons."""
        idx = self.secondary_targets_stack.currentIndex()
        count = self.secondary_targets_stack.count()
        self.secondary_group_prev_btn.setEnabled(idx > 0)
        self.secondary_group_next_btn.setEnabled(idx < count - 1)
        if count > 0 and idx < len(self.primary_targets):
            self.secondary_group_label.setText(f"Primary {idx + 1} of {count}: {self.primary_targets[idx].name}")

    def _build_secondary_params_pages(self):
        """Build parameter pages for all secondary targets."""
        # Clear existing pages
        while self.secondary_params_stack.count() > 0:
            self.secondary_params_stack.removeWidget(self.secondary_params_stack.widget(0))

        self.pattern_targets.clear()
        self.pattern_target_params.clear()
        self.all_secondary_targets = []  # Flat list for navigation

        shooter = self.shooter_combo.currentData()

        # Collect secondary targets for each primary
        for primary in self.primary_targets:
            secondary_list = self.secondary_lists.get(primary)
            if secondary_list:
                secondaries = []
                for item in secondary_list.selectedItems():
                    char_name = item.text()
                    for char in self.characters:
                        if char.name == char_name and char != shooter:
                            secondaries.append(char)
                            self.all_secondary_targets.append((primary, char))
                            break
                self.pattern_targets[primary] = secondaries

        # Create parameter pages for all secondary targets
        for primary, secondary in self.all_secondary_targets:
            page = self._create_secondary_target_params_page(primary, secondary)
            self.secondary_params_stack.addWidget(page)

        if self.secondary_params_stack.count() == 0:
            # No secondary targets - create empty page
            empty_page = QWidget()
            empty_layout = QVBoxLayout(empty_page)
            empty_layout.addWidget(QLabel("No secondary targets selected."))
            empty_layout.addStretch()
            self.secondary_params_stack.addWidget(empty_page)

        self.secondary_params_stack.setCurrentIndex(0)
        self._update_secondary_target_nav()

    def _create_secondary_target_params_page(self, primary: Character, secondary: Character):
        """Create parameter page for a secondary target."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        layout.addWidget(QLabel(f"<b>Secondary Target: {secondary.name}</b>"))
        layout.addWidget(QLabel(f"(In pattern of: {primary.name})"))

        params_group = QGroupBox("Target Parameters")
        params_layout = QFormLayout()

        # Use primary's range as default
        primary_range = self.primary_target_params[primary]['range'].value()

        range_spin = QSpinBox()
        range_spin.setRange(1, 500)
        range_spin.setValue(primary_range)
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

        self.pattern_target_params[secondary] = {
            'range': range_spin,
            'exposure': exposure_combo,
            'front': front_check,
            'orient': orient_combo,
            'target_speed': target_speed_spin,
            'target_duck': target_duck_check,
            'primary': primary
        }

        layout.addStretch()
        return widget

    def _prev_secondary_target(self):
        """Go to previous secondary target."""
        idx = self.secondary_params_stack.currentIndex()
        if idx > 0:
            self.secondary_params_stack.setCurrentIndex(idx - 1)
            self._update_secondary_target_nav()

    def _next_secondary_target(self):
        """Go to next secondary target."""
        idx = self.secondary_params_stack.currentIndex()
        if idx < self.secondary_params_stack.count() - 1:
            self.secondary_params_stack.setCurrentIndex(idx + 1)
            self._update_secondary_target_nav()

    def _update_secondary_target_nav(self):
        """Update secondary target navigation buttons."""
        idx = self.secondary_params_stack.currentIndex()
        count = self.secondary_params_stack.count()
        self.secondary_prev_btn.setEnabled(idx > 0)
        self.secondary_next_btn.setEnabled(idx < count - 1)
        if self.all_secondary_targets and idx < len(self.all_secondary_targets):
            primary, secondary = self.all_secondary_targets[idx]
            self.secondary_target_label.setText(
                f"Secondary {idx + 1} of {count}: {secondary.name} (in {primary.name}'s pattern)"
            )
        else:
            self.secondary_target_label.setText("No secondary targets")

    def _simulate(self):
        """Run shotgun burst fire simulation."""
        shooter = self.shooter_combo.currentData()
        weapon = self.weapon_combo.currentData()
        ammo = self.ammo_combo.currentData()

        if not all([shooter, weapon, ammo]) or not self.primary_targets:
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

        # Build primary target group
        primary_targets = []
        primary_ranges = []
        primary_exposures = []
        primary_shot_params_list = []
        primary_is_front_shots = []

        for target in self.primary_targets:
            params = self.primary_target_params[target]

            primary_targets.append(target)
            primary_ranges.append(params['range'].value())
            primary_exposures.append(params['exposure'].currentData())
            primary_is_front_shots.append(params['front'].isChecked())

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
            primary_shot_params_list.append(shot_params)

        primary_target_group = TargetGroup(
            targets=primary_targets,
            ranges=primary_ranges,
            exposures=primary_exposures,
            shot_params_list=primary_shot_params_list,
            is_front_shots=primary_is_front_shots
        )

        # Build pattern target groups (one per primary target)
        pattern_target_groups = []
        for primary in self.primary_targets:
            secondaries = self.pattern_targets.get(primary, [])

            secondary_targets = []
            secondary_ranges = []
            secondary_exposures = []
            secondary_shot_params_list = []
            secondary_is_front_shots = []

            for secondary in secondaries:
                params = self.pattern_target_params[secondary]

                secondary_targets.append(secondary)
                secondary_ranges.append(params['range'].value())
                secondary_exposures.append(params['exposure'].currentData())
                secondary_is_front_shots.append(params['front'].isChecked())

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
                secondary_shot_params_list.append(shot_params)

            pattern_group = TargetGroup(
                targets=secondary_targets,
                ranges=secondary_ranges,
                exposures=secondary_exposures,
                shot_params_list=secondary_shot_params_list,
                is_front_shots=secondary_is_front_shots
            )
            pattern_target_groups.append(pattern_group)

        # Run simulation
        results = CombatSimulator.shotgun_burst_fire(
            shooter, weapon, ammo, primary_target_group, pattern_target_groups,
            arc_of_fire, continuous_burst
        )

        self.last_results = results

        # Log and update main window
        main_window = self.window()
        while main_window and not hasattr(main_window, 'combat_log'):
            main_window = main_window.parent()

        if main_window and hasattr(main_window, 'combat_log'):
            target_names = ", ".join([t.name for t in primary_targets])
            main_window.combat_log.append_system(
                f"{shooter.name} fires shotgun burst from {weapon.name} at {target_names}"
            )
            for result in results:
                main_window._log_shot_result(result)
            if hasattr(main_window, 'combat_zone'):
                main_window.combat_zone.refresh_cards()
            if hasattr(main_window, 'stats_display') and hasattr(main_window, 'character_list'):
                current_row = main_window.character_list.currentRow()
                if current_row >= 0:
                    main_window._on_character_selected(current_row)

        self.current_step = 6
        self.stack.setCurrentIndex(6)
        self._update_navigation()
        self._display_results(results)
        self.show_log_btn.setEnabled(True)

    def _display_results(self, results):
        """Display shotgun burst fire results."""
        text = "<b>Shotgun Burst Fire Results</b><br><br>"

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
        """Calculate and display the hit probability for the current primary target."""
        from phoenix_command.simulations.combat_simulator_probabilities import CombatSimulatorProbabilities

        idx = self.primary_params_stack.currentIndex()
        if idx < 0 or idx >= len(self.primary_targets):
            self.target_prob_label.setText("No target selected")
            return

        shooter = self.shooter_combo.currentData()
        weapon = self.weapon_combo.currentData()
        ammo = self.ammo_combo.currentData()

        if not shooter or not weapon or not ammo:
            self.target_prob_label.setText("Please select shooter, weapon, and ammo")
            return

        target = self.primary_targets[idx]
        params = self.primary_target_params[target]

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

        # Calculate probability using the shotgun burst fire method
        eal, elevation_odds, effective_arc, patterns_info, pellet_info = CombatSimulatorProbabilities.calculate_shotgun_burst_fire_probabilities(
            shooter, target, weapon, ammo, range_hexes, exposure, shot_params, arc_of_fire, continuous_burst
        )

        text = f"<b>Target: {target.name}</b><br>"
        text += f"<b>EAL:</b> {eal}<br>"
        text += f"<b>Elevation Hit Probability:</b> {elevation_odds}%<br>"
        text += f"<b>Effective Arc:</b> {effective_arc:.2f} hexes<br>"
        text += f"<b>Patterns (if elevation succeeds):</b> {patterns_info}<br>"
        text += f"<b>Pellet Hits:</b> {pellet_info}"

        self.target_prob_label.setText(text)
