"""Explosive weapon shot dialog.

Only handles the shot itself (hit / scatter).
Explosion damage is calculated separately via ExplosionDamageDialog.
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QComboBox, QSpinBox, QCheckBox, QPushButton,
                             QTextEdit, QMessageBox, QGroupBox, QFormLayout,
                             QStackedWidget, QListWidget, QWidget)

from phoenix_command.models.character import Character
from phoenix_command.models.enums import (SituationStanceModifier4B,
                                          VisibilityModifier4C, ExplosiveTarget)
from phoenix_command.models.gear import Weapon, AmmoType
from phoenix_command.models.hit_result_advanced import ShotParameters, ExplosiveShotResult
from phoenix_command.simulations.combat_simulator import CombatSimulator


class ExplosiveWeaponDialog(QDialog):
    """Dialog for explosive weapon shot simulation (hit / scatter only).

    Flow:
      Step 1: Shooter, weapon, ammo
      Step 2: Target type (HEX/WINDOW/DOOR), range, movement
      Step 3: Stance & visibility modifiers  +  hit probability
      Step 4: Results (hit or scatter direction / distance)
    """

    def __init__(self, characters: list[Character], parent=None):
        super().__init__(parent)
        self.characters = characters
        self.setWindowTitle("Explosive Weapon Shot")
        self.setMinimumSize(750, 650)
        self.current_step = 0
        self.last_explosive_result: ExplosiveShotResult | None = None

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
        self.stack.addWidget(self._create_target_type_step())   # 1
        self.stack.addWidget(self._create_modifiers_step())     # 2
        self.stack.addWidget(self._create_results_step())       # 3

        nav = QHBoxLayout()
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

        weapon_group = QGroupBox("Weapon")
        weapon_layout = QFormLayout()
        self.weapon_combo = QComboBox()
        self.weapon_combo.currentIndexChanged.connect(self._on_weapon_changed)
        weapon_layout.addRow("Weapon:", self.weapon_combo)
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

    # ── Step 2: Target type & Range ───────────────────────────────────────

    def _create_target_type_step(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        target_group = QGroupBox("Explosive Target")
        target_layout = QFormLayout()

        self.explosive_target_combo = QComboBox()
        for et in ExplosiveTarget:
            self.explosive_target_combo.addItem(et.name, et)
        target_layout.addRow("Target Type:", self.explosive_target_combo)

        self.range_spin = QSpinBox()
        self.range_spin.setRange(1, 500)
        self.range_spin.setValue(10)
        target_layout.addRow("Range (hexes):", self.range_spin)

        target_group.setLayout(target_layout)
        layout.addWidget(target_group)

        move_group = QGroupBox("Shooter Parameters")
        move_layout = QFormLayout()

        self.aim_spin = QSpinBox()
        self.aim_spin.setRange(0, 20)
        self.aim_spin.setValue(2)
        move_layout.addRow("Aim Time (AC):", self.aim_spin)

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

    # ── Step 3: Stance & Visibility + probability ─────────────────────────

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
        "2. Target Type & Range",
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

    # ── Shooter / weapon / ammo callbacks ─────────────────────────────────

    def _on_shooter_changed(self):
        self.weapon_combo.clear()
        shooter = self.shooter_combo.currentData()
        if shooter:
            weapons = [item for item in shooter.equipment if isinstance(item, Weapon)]
            for w in weapons:
                self.weapon_combo.addItem(w.name, w)
        self._on_weapon_changed()

    def _on_weapon_changed(self):
        self.ammo_combo.clear()
        weapon = self.weapon_combo.currentData()
        shooter = self.shooter_combo.currentData()
        if weapon and shooter:
            shooter_ammo = [item for item in shooter.equipment if isinstance(item, AmmoType)]
            for ammo in weapon.ammunition_types:
                if ammo in shooter_ammo and ammo.explosive_data:
                    self.ammo_combo.addItem(ammo.name, ammo)

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
        explosive_target = self.explosive_target_combo.currentData()
        shot_params = self._build_shot_params()

        eal, odds = CombatSimulatorProbabilities.calculate_explosive_weapon_probability(
            shooter, weapon, range_hexes, explosive_target, shot_params
        )

        self.prob_label.setText(
            f"<b>EAL:</b> {eal}<br>"
            f"<b>Hit Probability:</b> {odds}%"
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
        explosive_target = self.explosive_target_combo.currentData()
        shot_params = self._build_shot_params()

        explosive_result = CombatSimulator.explosive_weapon_shot(
            shooter, weapon, range_hexes, explosive_target, shot_params
        )
        self.last_explosive_result = explosive_result

        # ── Logging to main window ────────────────────────────────────────
        main_window = self.window()
        while main_window and not hasattr(main_window, 'combat_log'):
            main_window = main_window.parent()

        if main_window and hasattr(main_window, 'combat_log'):
            main_window.combat_log.append_system(
                f"{shooter.name} fires {weapon.name} ({ammo.name}) "
                f"at {explosive_target.name} (range {range_hexes})"
            )
            if explosive_result.hit:
                main_window.combat_log.append_hit(
                    f"Direct HIT! (Roll: {explosive_result.roll} vs {explosive_result.odds}%)"
                )
            else:
                main_window.combat_log.append_miss(
                    f"MISS \u2013 Scatter {explosive_result.scatter_hexes} hexes "
                    f"({'long' if explosive_result.is_long else 'short'}) "
                    f"(Roll: {explosive_result.roll} vs {explosive_result.odds}%)"
                )
            if hasattr(main_window, 'combat_zone'):
                main_window.combat_zone.refresh_cards()

        # ── Show results ──────────────────────────────────────────────────
        self.current_step = 3
        self.stack.setCurrentIndex(3)
        self._update_navigation()
        self._display_results(explosive_result)
        self.show_log_btn.setEnabled(True)

    # ── Display helpers ───────────────────────────────────────────────────

    def _display_results(self, r: ExplosiveShotResult):
        text = "<b>Explosive Weapon Shot Results</b><br><br>"
        text += f"<b>EAL:</b> {r.eal}, <b>Odds:</b> {r.odds}%, <b>Roll:</b> {r.roll}<br><br>"

        if r.hit:
            text += "<b style='color:green;'>Direct HIT!</b><br>"
        else:
            text += (
                f"<b style='color:red;'>MISS</b><br>"
                f"Scatter: <b>{r.scatter_hexes}</b> hexes "
                f"({'long' if r.is_long else 'short'})<br>"
            )

        text += (
            "<br><i>Use Combat \u2192 Explosion Damage to calculate "
            "shrapnel / concussion damage to characters.</i>"
        )
        self.results_text.setHtml(text)

    def _show_log(self):
        if not self.last_explosive_result:
            return
        r = self.last_explosive_result
        log_text_content = (
            f"EAL: {r.eal}, Odds: {r.odds}%, Roll: {r.roll}\n"
            f"Hit: {r.hit}, Scatter: {r.scatter_hexes} hexes, Long: {r.is_long}"
        )

        dialog = QDialog(self)
        dialog.setWindowTitle("Detailed Log")
        dialog.setMinimumSize(600, 400)
        layout = QVBoxLayout(dialog)

        log_text = QTextEdit()
        log_text.setReadOnly(True)
        log_text.setPlainText(log_text_content)
        layout.addWidget(log_text)

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)

        dialog.exec()
