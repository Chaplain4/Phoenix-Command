"""Automatic grenade launcher burst dialog.

Handles burst fire from automatic grenade launchers using
CombatSimulator.automatic_grenade_launcher_burst().
Each grenade that hits the area gets its own hit/scatter result.
Explosion damage is calculated separately via Combat → Explosion Damage.
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QComboBox, QSpinBox, QCheckBox, QPushButton,
                             QTextEdit, QMessageBox, QGroupBox, QFormLayout,
                             QStackedWidget, QListWidget, QWidget, QDoubleSpinBox)

from phoenix_command.models.character import Character
from phoenix_command.models.enums import (SituationStanceModifier4B,
                                          VisibilityModifier4C, ExplosiveTarget)
from phoenix_command.models.gear import Weapon, AmmoType
from phoenix_command.models.hit_result_advanced import ShotParameters, ExplosiveShotResult
from phoenix_command.simulations.combat_simulator import CombatSimulator

from typing import List


class AutoGrenadeLauncherDialog(QDialog):
    """Dialog for automatic grenade launcher burst simulation.

    Flow:
      Step 1: Shooter, weapon (full-auto + explosive ammo)
      Step 2: Target type, range, arc of fire, continuous burst
      Step 3: Stance & visibility modifiers  +  hit probability
      Step 4: Results (per-grenade hit / scatter)
    """

    def __init__(self, characters: list[Character], parent=None):
        super().__init__(parent)
        self.characters = characters
        self.setWindowTitle("Auto Grenade Launcher Burst")
        self.setMinimumSize(750, 650)
        self.current_step = 0
        self.last_results: List[ExplosiveShotResult] = []

        self._setup_ui()

    # ── UI setup ──────────────────────────────────────────────────────────

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        self.step_label = QLabel()
        self.step_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(self.step_label)

        self.stack = QStackedWidget()
        layout.addWidget(self.stack)

        self.stack.addWidget(self._create_shooter_step())      # 0
        self.stack.addWidget(self._create_target_step())       # 1
        self.stack.addWidget(self._create_modifiers_step())    # 2
        self.stack.addWidget(self._create_results_step())      # 3

        nav = QHBoxLayout()
        self.prev_btn = QPushButton("Previous")
        self.prev_btn.clicked.connect(self._previous_step)
        self.prev_btn.setEnabled(False)
        self.next_btn = QPushButton("Next")
        self.next_btn.clicked.connect(self._next_step)
        self.simulate_btn = QPushButton("Fire Burst")
        self.simulate_btn.clicked.connect(self._simulate)
        self.simulate_btn.setVisible(False)
        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.accept)

        nav.addWidget(self.prev_btn)
        nav.addStretch()
        nav.addWidget(self.next_btn)
        nav.addWidget(self.simulate_btn)
        nav.addWidget(self.close_btn)
        layout.addLayout(nav)

        self._update_step_label()
        self._on_shooter_changed()

    # ── Step 1: Shooter & Weapon ──────────────────────────────────────────

    def _create_shooter_step(self):
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

        weapon_group = QGroupBox("Weapon (Full Auto + Explosive)")
        weapon_layout = QFormLayout()
        self.weapon_combo = QComboBox()
        self.weapon_combo.currentIndexChanged.connect(self._on_weapon_changed)
        weapon_layout.addRow("Weapon:", self.weapon_combo)
        self.weapon_info_label = QLabel()
        self.weapon_info_label.setWordWrap(True)
        weapon_layout.addRow("Info:", self.weapon_info_label)
        weapon_group.setLayout(weapon_layout)
        layout.addWidget(weapon_group)

        ammo_group = QGroupBox("Ammunition (Explosive)")
        ammo_layout = QFormLayout()
        self.ammo_combo = QComboBox()
        ammo_layout.addRow("Ammo:", self.ammo_combo)
        ammo_group.setLayout(ammo_layout)
        layout.addWidget(ammo_group)

        layout.addStretch()
        return widget

    # ── Step 2: Target, range, arc, continuous burst ──────────────────────

    def _create_target_step(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        target_group = QGroupBox("Target")
        target_layout = QFormLayout()

        self.target_combo = QComboBox()
        for et in ExplosiveTarget:
            self.target_combo.addItem(et.name, et)
        target_layout.addRow("Target Type:", self.target_combo)

        self.range_spin = QSpinBox()
        self.range_spin.setRange(1, 500)
        self.range_spin.setValue(10)
        target_layout.addRow("Range (hexes):", self.range_spin)

        target_group.setLayout(target_layout)
        layout.addWidget(target_group)

        params_group = QGroupBox("Burst Parameters")
        params_layout = QFormLayout()

        self.aim_spin = QSpinBox()
        self.aim_spin.setRange(0, 20)
        self.aim_spin.setValue(2)
        params_layout.addRow("Aim Time (AC):", self.aim_spin)

        self.continuous_burst_spin = QSpinBox()
        self.continuous_burst_spin.setRange(0, 10)
        self.continuous_burst_spin.setValue(0)
        self.continuous_burst_spin.setToolTip("Number of impulses of continuous burst fire (SAB penalty)")
        params_layout.addRow("Continuous Burst Impulses:", self.continuous_burst_spin)

        self.arc_auto_check = QCheckBox("Use minimum effective arc")
        self.arc_auto_check.setChecked(True)
        self.arc_auto_check.stateChanged.connect(self._on_arc_auto_changed)
        params_layout.addRow(self.arc_auto_check)

        self.arc_spin = QDoubleSpinBox()
        self.arc_spin.setRange(0.1, 2000.0)
        self.arc_spin.setValue(1.0)
        self.arc_spin.setSuffix(" hexes")
        self.arc_spin.setEnabled(False)
        params_layout.addRow("Custom Arc:", self.arc_spin)

        params_group.setLayout(params_layout)
        layout.addWidget(params_group)

        move_group = QGroupBox("Shooter Movement")
        move_layout = QFormLayout()

        self.shooter_speed_spin = QSpinBox()
        self.shooter_speed_spin.setRange(0, 20)
        self.shooter_speed_spin.setValue(0)
        move_layout.addRow("Shooter Speed (hex/imp):", self.shooter_speed_spin)

        self.shooter_duck_check = QCheckBox()
        move_layout.addRow("Shooter Reflexive Duck:", self.shooter_duck_check)

        move_group.setLayout(move_layout)
        layout.addWidget(move_group)

        layout.addStretch()
        return widget

    # ── Step 3: Stance & visibility + probability ─────────────────────────

    def _create_modifiers_step(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        stance_group = QGroupBox("Situation & Stance Modifiers")
        stance_layout = QVBoxLayout()
        stance_layout.addWidget(QLabel("Select all applicable modifiers:"))
        self.stance_list = QListWidget()
        self.stance_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        for s in SituationStanceModifier4B:
            self.stance_list.addItem(s.name)
        stance_layout.addWidget(self.stance_list)
        stance_group.setLayout(stance_layout)
        layout.addWidget(stance_group)

        vis_group = QGroupBox("Visibility Modifiers")
        vis_layout = QVBoxLayout()
        self.visibility_list = QListWidget()
        self.visibility_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        for v in VisibilityModifier4C:
            self.visibility_list.addItem(v.name)
        vis_layout.addWidget(self.visibility_list)
        vis_group.setLayout(vis_layout)
        layout.addWidget(vis_group)

        prob_group = QGroupBox("Hit Probability")
        prob_layout = QVBoxLayout()
        self.prob_label = QLabel("Configure parameters to see probability")
        self.prob_label.setWordWrap(True)
        prob_layout.addWidget(self.prob_label)
        calc_btn = QPushButton("Calculate Probability")
        calc_btn.clicked.connect(self._calculate_probability)
        prob_layout.addWidget(calc_btn)
        prob_group.setLayout(prob_layout)
        layout.addWidget(prob_group)

        return widget

    # ── Step 4: Results ───────────────────────────────────────────────────

    def _create_results_step(self):
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

        info_label = QLabel(
            "<i>To calculate explosion damage to characters, use "
            "Combat \u2192 Explosion Damage after this dialog.</i>"
        )
        info_label.setWordWrap(True)
        layout.addWidget(info_label)

        return widget

    # ── Navigation ────────────────────────────────────────────────────────

    STEP_NAMES = [
        "1. Shooter & Weapon",
        "2. Target & Parameters",
        "3. Modifiers & Probability",
        "4. Results",
    ]
    TOTAL_STEPS = len(STEP_NAMES)

    def _update_step_label(self):
        self.step_label.setText(
            f"Step {self.current_step + 1} of {self.TOTAL_STEPS}: "
            f"{self.STEP_NAMES[self.current_step].split('. ', 1)[1]}"
        )

    def _previous_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.stack.setCurrentIndex(self.current_step)
            self._update_navigation()

    def _next_step(self):
        if self.current_step == 0:
            weapon = self.weapon_combo.currentData()
            ammo = self.ammo_combo.currentData()
            if not weapon or not ammo:
                QMessageBox.warning(self, "Error", "Please select weapon and ammunition")
                return
            if not ammo.explosive_data:
                QMessageBox.warning(self, "Error", "Selected ammo has no explosive data")
                return

        if self.current_step < 2:
            self.current_step += 1
            self.stack.setCurrentIndex(self.current_step)
            self._update_navigation()

    def _update_navigation(self):
        self.prev_btn.setEnabled(self.current_step > 0)
        self.next_btn.setVisible(self.current_step < 2)
        self.simulate_btn.setVisible(self.current_step == 2)
        self._update_step_label()

    # ── Callbacks ─────────────────────────────────────────────────────────

    def _on_shooter_changed(self):
        self.weapon_combo.clear()
        shooter = self.shooter_combo.currentData()
        if shooter:
            weapons = [item for item in shooter.equipment if isinstance(item, Weapon)]
            for w in weapons:
                if w.full_auto and w.full_auto_rof:
                    self.weapon_combo.addItem(f"{w.name} (ROF: {w.full_auto_rof})", w)
        self._on_weapon_changed()

    def _on_weapon_changed(self):
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
                    info += f", Min Arc: {min_arc}\u00b0"
            self.weapon_info_label.setText(info)
        else:
            self.weapon_info_label.setText("")

        if weapon and shooter:
            shooter_ammo = [item for item in shooter.equipment if isinstance(item, AmmoType)]
            for ammo in weapon.ammunition_types:
                if ammo in shooter_ammo and ammo.explosive_data:
                    self.ammo_combo.addItem(ammo.name, ammo)

    def _on_arc_auto_changed(self, state):
        self.arc_spin.setEnabled(not state)

    # ── ShotParameters builder ────────────────────────────────────────────

    def _build_shot_params(self) -> ShotParameters:
        stance_mods = []
        for item in self.stance_list.selectedItems():
            stance_mods.append(list(SituationStanceModifier4B)[self.stance_list.row(item)])

        vis_mods = []
        for item in self.visibility_list.selectedItems():
            vis_mods.append(list(VisibilityModifier4C)[self.visibility_list.row(item)])

        return ShotParameters(
            aim_time_ac=self.aim_spin.value(),
            situation_stance_modifiers=stance_mods,
            visibility_modifiers=vis_mods,
            shooter_speed_hex_per_impulse=float(self.shooter_speed_spin.value()),
            reflexive_duck_shooter=self.shooter_duck_check.isChecked(),
        )

    # ── Probability ───────────────────────────────────────────────────────

    def _calculate_probability(self):
        from phoenix_command.simulations.combat_simulator_probabilities import CombatSimulatorProbabilities

        shooter = self.shooter_combo.currentData()
        weapon = self.weapon_combo.currentData()
        if not shooter or not weapon:
            self.prob_label.setText("Please select shooter and weapon")
            return

        range_hexes = self.range_spin.value()
        explosive_target = self.target_combo.currentData()
        shot_params = self._build_shot_params()
        arc_of_fire = None if self.arc_auto_check.isChecked() else self.arc_spin.value()
        continuous_burst = self.continuous_burst_spin.value()

        eal, elevation_odds, effective_arc, grenades_info = (
            CombatSimulatorProbabilities.calculate_auto_grenade_launcher_probability(
                shooter, weapon, range_hexes, explosive_target, shot_params,
                arc_of_fire, continuous_burst
            )
        )

        self.prob_label.setText(
            f"<b>EAL:</b> {eal}<br>"
            f"<b>Elevation Hit Probability:</b> {elevation_odds}%<br>"
            f"<b>Effective Arc:</b> {effective_arc:.2f} hexes<br>"
            f"<b>Grenades on target:</b> {grenades_info}"
        )

    # ── Simulate ──────────────────────────────────────────────────────────

    def _simulate(self):
        shooter = self.shooter_combo.currentData()
        weapon = self.weapon_combo.currentData()
        ammo = self.ammo_combo.currentData()
        if not all([shooter, weapon, ammo]):
            QMessageBox.warning(self, "Error", "Please select shooter, weapon and ammo")
            return

        range_hexes = self.range_spin.value()
        explosive_target = self.target_combo.currentData()
        shot_params = self._build_shot_params()
        arc_of_fire = None if self.arc_auto_check.isChecked() else self.arc_spin.value()
        continuous_burst = self.continuous_burst_spin.value()

        results = CombatSimulator.automatic_grenade_launcher_burst(
            shooter, weapon, range_hexes, explosive_target, shot_params,
            arc_of_fire, continuous_burst
        )
        self.last_results = results

        # ── Log to main window ────────────────────────────────────────────
        main_window = self.window()
        while main_window and not hasattr(main_window, 'combat_log'):
            main_window = main_window.parent()

        if main_window and hasattr(main_window, 'combat_log'):
            main_window.combat_log.append_system(
                f"{shooter.name} fires AGL burst {weapon.name} ({ammo.name}) "
                f"at {explosive_target.name} (range {range_hexes})"
            )
            # First result may be elevation miss
            if len(results) == 1 and results[0].elevation_failed:
                main_window.combat_log.append_miss(
                    f"Burst MISSED elevation (Roll: {results[0].roll} vs {results[0].odds}%) "
                    f"– Scatter {results[0].scatter_hexes} hexes "
                    f"({'long' if results[0].is_long else 'short'})"
                )
            else:
                direct = sum(1 for r in results if r.hit)
                scattered = sum(1 for r in results if not r.hit)
                main_window.combat_log.append_hit(
                    f"{len(results)} grenades on target: {direct} direct hit(s), {scattered} scattered"
                )
            if hasattr(main_window, 'combat_zone'):
                main_window.combat_zone.refresh_cards()

        # ── Show results ──────────────────────────────────────────────────
        self.current_step = 3
        self.stack.setCurrentIndex(3)
        self._update_navigation()
        self._display_results(results)
        self.show_log_btn.setEnabled(True)

    # ── Display ───────────────────────────────────────────────────────────

    def _display_results(self, results: List[ExplosiveShotResult]):
        text = "<b>Auto Grenade Launcher Burst Results</b><br><br>"

        if not results:
            text += "<i>No results.</i>"
            self.results_text.setHtml(text)
            return

        first = results[0]
        text += f"<b>EAL:</b> {first.eal}, <b>Odds:</b> {first.odds}%<br><br>"

        # Elevation miss
        if len(results) == 1 and first.elevation_failed:
            text += (
                f"<b style='color:red;'>Burst MISSED elevation</b><br>"
                f"Roll: {first.roll} vs {first.odds}%<br>"
                f"Scatter: <b>{first.scatter_hexes}</b> hexes "
                f"({'long' if first.is_long else 'short'})<br>"
            )
        else:
            text += f"<b>Grenades on target:</b> {len(results)}<br><br>"
            for i, r in enumerate(results):
                text += f"<b>Grenade {i + 1}:</b> "
                if r.hit:
                    text += "<span style='color:green;'>Direct HIT</span>"
                else:
                    text += (
                        f"<span style='color:orange;'>Scatter {r.scatter_hexes} hexes "
                        f"({'long' if r.is_long else 'short'})</span>"
                    )
                text += f" (Roll: {r.roll})<br>"

        text += (
            "<br><i>Use Combat \u2192 Explosion Damage to calculate "
            "shrapnel / concussion damage to characters.</i>"
        )
        self.results_text.setHtml(text)

    def _show_log(self):
        if not self.last_results:
            return

        lines = []
        first = self.last_results[0]

        # Elevation miss: single result with elevation_failed=True
        if len(self.last_results) == 1 and first.elevation_failed:
            lines.append(
                f"Burst MISSED elevation check\n"
                f"EAL={first.eal}, Odds={first.odds}%, Roll={first.roll}\n"
                f"Scatter: {first.scatter_hexes} hexes ({'long' if first.is_long else 'short'})"
            )
        else:
            lines.append(f"EAL={first.eal}, Elevation Odds={first.odds}%")
            lines.append(f"Grenades on target: {len(self.last_results)}\n")
            for i, r in enumerate(self.last_results):
                if r.hit:
                    lines.append(
                        f"Grenade {i + 1}: Direct HIT (Roll: {r.roll})"
                    )
                else:
                    lines.append(
                        f"Grenade {i + 1}: Scatter {r.scatter_hexes} hexes "
                        f"({'long' if r.is_long else 'short'}) (Roll: {r.roll})"
                    )

        log_content = "\n".join(lines)

        dialog = QDialog(self)
        dialog.setWindowTitle("Detailed Log")
        dialog.setMinimumSize(600, 400)
        layout = QVBoxLayout(dialog)

        log_text = QTextEdit()
        log_text.setReadOnly(True)
        log_text.setPlainText(log_content)
        layout.addWidget(log_text)

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)

        dialog.exec()

