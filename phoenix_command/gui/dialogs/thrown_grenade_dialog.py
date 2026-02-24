"""Thrown grenade dialog.

Handles the grenade throw (hit / scatter).
Explosion damage is calculated separately via Combat → Explosion Damage.
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QComboBox, QSpinBox, QPushButton,
                             QTextEdit, QMessageBox, QGroupBox, QFormLayout,
                             QStackedWidget, QListWidget, QWidget)

from phoenix_command.models.character import Character
from phoenix_command.models.enums import (SituationStanceModifier4B,
                                          VisibilityModifier4C, ExplosiveTarget)
from phoenix_command.models.gear import Grenade
from phoenix_command.models.hit_result_advanced import ExplosiveShotResult
from phoenix_command.simulations.combat_simulator import CombatSimulator


class ThrownGrenadeDialog(QDialog):
    """Dialog for thrown grenade simulation (hit / scatter only).

    Flow:
      Step 1: Thrower & grenade selection
      Step 2: Target type, range, aim time, modifiers  +  hit probability
      Step 3: Results (hit or scatter direction / distance)
    """

    def __init__(self, characters: list[Character], parent=None):
        super().__init__(parent)
        self.characters = characters
        self.setWindowTitle("Thrown Grenade")
        self.setMinimumSize(700, 600)
        self.current_step = 0
        self.last_result: ExplosiveShotResult | None = None

        self._setup_ui()

    # ── UI setup ──────────────────────────────────────────────────────────

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        self.step_label = QLabel()
        self.step_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(self.step_label)

        self.stack = QStackedWidget()
        layout.addWidget(self.stack)

        self.stack.addWidget(self._create_thrower_step())     # 0
        self.stack.addWidget(self._create_params_step())      # 1
        self.stack.addWidget(self._create_results_step())     # 2

        nav = QHBoxLayout()
        self.prev_btn = QPushButton("Previous")
        self.prev_btn.clicked.connect(self._previous_step)
        self.prev_btn.setEnabled(False)
        self.next_btn = QPushButton("Next")
        self.next_btn.clicked.connect(self._next_step)
        self.simulate_btn = QPushButton("Throw")
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
        self._on_thrower_changed()

    # ── Step 1: Thrower & Grenade ─────────────────────────────────────────

    def _create_thrower_step(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        thrower_group = QGroupBox("Thrower")
        thrower_layout = QFormLayout()
        self.thrower_combo = QComboBox()
        for char in self.characters:
            self.thrower_combo.addItem(char.name, char)
        self.thrower_combo.currentIndexChanged.connect(self._on_thrower_changed)
        thrower_layout.addRow("Character:", self.thrower_combo)
        thrower_group.setLayout(thrower_layout)
        layout.addWidget(thrower_group)

        grenade_group = QGroupBox("Grenade")
        grenade_layout = QFormLayout()
        self.grenade_combo = QComboBox()
        self.grenade_combo.currentIndexChanged.connect(self._on_grenade_changed)
        grenade_layout.addRow("Grenade:", self.grenade_combo)
        self.grenade_info_label = QLabel()
        self.grenade_info_label.setWordWrap(True)
        grenade_layout.addRow("Info:", self.grenade_info_label)
        grenade_group.setLayout(grenade_layout)
        layout.addWidget(grenade_group)

        layout.addStretch()
        return widget

    # ── Step 2: Target, range, modifiers ──────────────────────────────────

    def _create_params_step(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        target_group = QGroupBox("Target")
        target_layout = QFormLayout()

        self.target_combo = QComboBox()
        for et in ExplosiveTarget:
            self.target_combo.addItem(et.name, et)
        target_layout.addRow("Target Type:", self.target_combo)

        self.range_spin = QSpinBox()
        self.range_spin.setRange(1, 100)
        self.range_spin.setValue(5)
        target_layout.addRow("Range (hexes):", self.range_spin)

        self.aim_spin = QSpinBox()
        self.aim_spin.setRange(1, 20)
        self.aim_spin.setValue(2)
        target_layout.addRow("Aim Time (AC):", self.aim_spin)

        target_group.setLayout(target_layout)
        layout.addWidget(target_group)

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

    # ── Step 3: Results ───────────────────────────────────────────────────

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
        "1. Thrower & Grenade",
        "2. Target & Modifiers",
        "3. Results",
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
            grenade = self.grenade_combo.currentData()
            if not grenade:
                QMessageBox.warning(self, "Error", "Please select a grenade")
                return
            # Pre-set max range from grenade
            self.range_spin.setMaximum(grenade.range if isinstance(grenade.range, int) else grenade.range.stop - 1)

        if self.current_step == 1:
            grenade = self.grenade_combo.currentData()
            range_hexes = self.range_spin.value()
            max_range = grenade.range if isinstance(grenade.range, int) else grenade.range.stop - 1
            if range_hexes > max_range:
                QMessageBox.warning(
                    self, "Out of Range",
                    f"Grenade max throwing range: {max_range} hexes\n"
                    f"Current range: {range_hexes} hexes"
                )
                return

        if self.current_step < 1:
            self.current_step += 1
            self.stack.setCurrentIndex(self.current_step)
            self._update_navigation()

    def _update_navigation(self):
        self.prev_btn.setEnabled(self.current_step > 0)
        self.next_btn.setVisible(self.current_step < 1)
        self.simulate_btn.setVisible(self.current_step == 1)
        self._update_step_label()

    # ── Thrower / grenade callbacks ───────────────────────────────────────

    def _on_thrower_changed(self):
        self.grenade_combo.clear()
        thrower = self.thrower_combo.currentData()
        if thrower:
            grenades = [item for item in thrower.equipment if isinstance(item, Grenade)]
            for g in grenades:
                self.grenade_combo.addItem(g.name, g)
        self._on_grenade_changed()

    def _on_grenade_changed(self):
        grenade: Grenade | None = self.grenade_combo.currentData()
        if not grenade:
            self.grenade_info_label.setText("")
            return
        max_range = grenade.range if isinstance(grenade.range, int) else grenade.range.stop - 1
        fuse = f"{grenade.fuse_length} impulses" if grenade.fuse_length > 0 else "impact fuse"
        self.grenade_info_label.setText(
            f"Type: {grenade.grenade_type.value}\n"
            f"Weight: {grenade.weight} lbs\n"
            f"Max range: {max_range} hexes\n"
            f"Arm time: {grenade.arm_time} impulses\n"
            f"Fuse: {fuse}"
        )

    # ── Helpers ───────────────────────────────────────────────────────────

    def _get_stance_mods(self):
        mods = []
        for item in self.stance_list.selectedItems():
            mods.append(list(SituationStanceModifier4B)[self.stance_list.row(item)])
        return mods

    def _get_vis_mods(self):
        mods = []
        for item in self.visibility_list.selectedItems():
            mods.append(list(VisibilityModifier4C)[self.visibility_list.row(item)])
        return mods

    # ── Probability ───────────────────────────────────────────────────────

    def _calculate_probability(self):
        from phoenix_command.simulations.combat_simulator_probabilities import CombatSimulatorProbabilities

        thrower = self.thrower_combo.currentData()
        if not thrower:
            self.prob_label.setText("Please select thrower")
            return

        explosive_target = self.target_combo.currentData()
        range_hexes = self.range_spin.value()
        aim_ac = self.aim_spin.value()

        eal, odds = CombatSimulatorProbabilities.calculate_thrown_grenade_probability(
            thrower, range_hexes, explosive_target, aim_ac,
            self._get_stance_mods(), self._get_vis_mods()
        )

        self.prob_label.setText(
            f"<b>EAL:</b> {eal}<br>"
            f"<b>Hit Probability:</b> {odds}%"
        )

    # ── Simulate ──────────────────────────────────────────────────────────

    def _simulate(self):
        thrower = self.thrower_combo.currentData()
        grenade = self.grenade_combo.currentData()
        if not thrower or not grenade:
            QMessageBox.warning(self, "Error", "Please select thrower and grenade")
            return

        explosive_target = self.target_combo.currentData()
        range_hexes = self.range_spin.value()
        aim_ac = self.aim_spin.value()
        stance_mods = self._get_stance_mods()
        vis_mods = self._get_vis_mods()

        result = CombatSimulator.thrown_grenade(
            thrower, range_hexes, explosive_target,
            aim_ac, stance_mods, vis_mods
        )
        self.last_result = result

        # ── Logging to main window ────────────────────────────────────────
        main_window = self.window()
        while main_window and not hasattr(main_window, 'combat_log'):
            main_window = main_window.parent()

        if main_window and hasattr(main_window, 'combat_log'):
            main_window.combat_log.append_system(
                f"{thrower.name} throws {grenade.name} "
                f"at {explosive_target.name} (range {range_hexes})"
            )
            if result.hit:
                main_window.combat_log.append_hit(
                    f"Direct HIT! (Roll: {result.roll} vs {result.odds}%)"
                )
            else:
                main_window.combat_log.append_miss(
                    f"MISS \u2013 Scatter {result.scatter_hexes} hexes "
                    f"({'long' if result.is_long else 'short'}) "
                    f"(Roll: {result.roll} vs {result.odds}%)"
                )
            if hasattr(main_window, 'combat_zone'):
                main_window.combat_zone.refresh_cards()

        # ── Show results ──────────────────────────────────────────────────
        self.current_step = 2
        self.stack.setCurrentIndex(2)
        self._update_navigation()
        self._display_results(result)
        self.show_log_btn.setEnabled(True)

    # ── Display helpers ───────────────────────────────────────────────────

    def _display_results(self, r: ExplosiveShotResult):
        grenade = self.grenade_combo.currentData()
        grenade_name = grenade.name if grenade else "?"
        text = f"<b>Thrown Grenade Results</b> ({grenade_name})<br><br>"
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
        if not self.last_result:
            return
        r = self.last_result
        log_content = (
            f"EAL: {r.eal}, Odds: {r.odds}%, Roll: {r.roll}\n"
            f"Hit: {r.hit}, Scatter: {r.scatter_hexes} hexes, Long: {r.is_long}"
        )

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

