"""Explosion damage dialog.

Standalone dialog to calculate shrapnel + concussion damage from any explosive
ammo to characters.  Opened from Combat → Explosion Damage.

The user picks an explosive ammo from all ammo available across all characters,
then selects targets and sets per-target range-from-burst, exposure, orientation,
and blast modifiers.
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QComboBox, QSpinBox, QCheckBox, QPushButton,
                             QTextEdit, QMessageBox, QGroupBox, QFormLayout,
                             QStackedWidget, QListWidget, QWidget)

from phoenix_command.models.character import Character
from phoenix_command.models.enums import (TargetExposure, SituationStanceModifier4B,
                                          VisibilityModifier4C, TargetOrientation,
                                          BlastModifier)
from phoenix_command.models.gear import AmmoType
from phoenix_command.models.hit_result_advanced import ShotParameters
from phoenix_command.simulations.combat_simulator import CombatSimulator


class ExplosionDamageDialog(QDialog):
    """Dialog for calculating explosion damage (shrapnel + concussion).

    Flow:
      Step 1: Select explosive ammo (from all characters' equipment)
      Step 2: Select blast targets + per-target parameters
      Step 3: Results
    """

    def __init__(self, characters: list[Character], parent=None):
        super().__init__(parent)
        self.characters = characters
        self.setWindowTitle("Explosion Damage")
        self.setMinimumSize(750, 650)
        self.current_step = 0
        self.blast_targets: list[Character] = []
        self.blast_target_params: dict = {}
        self.last_results = []

        self._setup_ui()

    # ── UI ────────────────────────────────────────────────────────────────

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        self.step_label = QLabel()
        self.step_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(self.step_label)

        self.stack = QStackedWidget()
        layout.addWidget(self.stack)

        self.stack.addWidget(self._create_ammo_step())      # 0
        self.stack.addWidget(self._create_targets_step())    # 1
        self.stack.addWidget(self._create_results_step())    # 2

        nav = QHBoxLayout()
        self.prev_btn = QPushButton("Previous")
        self.prev_btn.clicked.connect(self._previous_step)
        self.prev_btn.setEnabled(False)
        self.next_btn = QPushButton("Next")
        self.next_btn.clicked.connect(self._next_step)
        self.simulate_btn = QPushButton("Calculate Damage")
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

    # ── Step 1: Ammo selection ────────────────────────────────────────────

    def _create_ammo_step(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        ammo_group = QGroupBox("Explosive Ammunition")
        ammo_layout = QFormLayout()

        self.ammo_combo = QComboBox()
        self._populate_ammo_combo()
        self.ammo_combo.currentIndexChanged.connect(self._on_ammo_changed)
        ammo_layout.addRow("Ammo:", self.ammo_combo)

        self.ammo_info_label = QLabel()
        self.ammo_info_label.setWordWrap(True)
        ammo_layout.addRow("Info:", self.ammo_info_label)

        ammo_group.setLayout(ammo_layout)
        layout.addWidget(ammo_group)

        layout.addStretch()
        self._on_ammo_changed()
        return widget

    # ── Step 2: Targets ───────────────────────────────────────────────────

    def _create_targets_step(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        info = QLabel(
            "Select characters affected by the explosion and configure "
            "their range from the burst point, exposure, and blast modifiers."
        )
        info.setWordWrap(True)
        layout.addWidget(info)

        select_group = QGroupBox("Select Blast Targets")
        select_layout = QVBoxLayout()
        self.targets_list = QListWidget()
        self.targets_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.targets_list.itemSelectionChanged.connect(self._on_targets_changed)
        select_layout.addWidget(self.targets_list)
        select_group.setLayout(select_layout)
        layout.addWidget(select_group)

        params_group = QGroupBox("Target Parameters")
        params_layout = QVBoxLayout()

        self.params_stack = QStackedWidget()
        params_layout.addWidget(self.params_stack)

        nav = QHBoxLayout()
        self.t_prev_btn = QPushButton("Previous Target")
        self.t_prev_btn.clicked.connect(self._prev_target)
        self.t_next_btn = QPushButton("Next Target")
        self.t_next_btn.clicked.connect(self._next_target)
        self.t_label = QLabel()
        nav.addWidget(self.t_prev_btn)
        nav.addWidget(self.t_label)
        nav.addStretch()
        nav.addWidget(self.t_next_btn)
        params_layout.addLayout(nav)

        params_group.setLayout(params_layout)
        layout.addWidget(params_group)

        return widget

    # ── Step 3: Results ───────────────────────────────────────────────────

    def _create_results_step(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        results_group = QGroupBox("Explosion Damage Results")
        results_layout = QVBoxLayout()
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        results_layout.addWidget(self.results_text)

        log_layout = QHBoxLayout()
        self.show_log_btn = QPushButton("Show Detailed Log")
        self.show_log_btn.clicked.connect(self._show_log)
        self.show_log_btn.setEnabled(False)
        log_layout.addWidget(self.show_log_btn)
        log_layout.addStretch()
        results_layout.addLayout(log_layout)

        results_group.setLayout(results_layout)
        layout.addWidget(results_group)

        return widget

    # ── Navigation ────────────────────────────────────────────────────────

    STEP_NAMES = ["1. Explosive Ammo", "2. Blast Targets", "3. Results"]
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
            ammo = self.ammo_combo.currentData()
            if not ammo:
                QMessageBox.warning(self, "Error", "Please select explosive ammunition")
                return
            self._populate_targets_list()

        if self.current_step < 1:
            self.current_step += 1
            self.stack.setCurrentIndex(self.current_step)
            self._update_navigation()

    def _update_navigation(self):
        self.prev_btn.setEnabled(self.current_step > 0)
        self.next_btn.setVisible(self.current_step < 1)
        self.simulate_btn.setVisible(self.current_step == 1)
        self._update_step_label()

    # ── Ammo helpers ──────────────────────────────────────────────────────

    def _populate_ammo_combo(self):
        """Collect all explosive ammo from all characters' equipment."""
        self.ammo_combo.clear()
        seen = set()
        for char in self.characters:
            for item in char.equipment:
                if isinstance(item, AmmoType) and item.explosive_data and id(item) not in seen:
                    seen.add(id(item))
                    self.ammo_combo.addItem(f"{item.name} ({char.name})", item)

    def _on_ammo_changed(self):
        ammo: AmmoType | None = self.ammo_combo.currentData()
        if not ammo or not ammo.explosive_data:
            self.ammo_info_label.setText("No explosive data")
            return

        lines = []
        for ed in ammo.explosive_data:
            rng = "contact" if ed.range_hexes is None else f"{ed.range_hexes} hex"
            lines.append(
                f"Range {rng}: PEN {ed.shrapnel_penetration}, DC {ed.shrapnel_damage_class}, "
                f"BSHC {ed.base_shrapnel_hit_chance}, Concussion {ed.base_concussion}"
            )
        self.ammo_info_label.setText("\n".join(lines))

    # ── Target helpers ────────────────────────────────────────────────────

    def _populate_targets_list(self):
        self.targets_list.clear()
        for char in self.characters:
            self.targets_list.addItem(char.name)

    def _on_targets_changed(self):
        """Rebuild per-target parameter pages."""
        while self.params_stack.count() > 0:
            self.params_stack.removeWidget(self.params_stack.widget(0))
        self.blast_target_params.clear()
        self.blast_targets = []

        for item in self.targets_list.selectedItems():
            name = item.text()
            for char in self.characters:
                if char.name == name:
                    self.blast_targets.append(char)
                    break

        for target in self.blast_targets:
            page = self._create_target_page(target)
            self.params_stack.addWidget(page)

        if self.params_stack.count() > 0:
            self.params_stack.setCurrentIndex(0)
        self._update_target_nav()

    def _create_target_page(self, target: Character):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel(f"<b>Target: {target.name}</b>"))

        form = QFormLayout()

        range_spin = QSpinBox()
        range_spin.setRange(0, 100)
        range_spin.setValue(0)
        range_spin.setToolTip("Range from burst point in hexes (0 = direct contact)")
        form.addRow("Range from burst (hexes):", range_spin)

        exposure_combo = QComboBox()
        for exp in TargetExposure:
            exposure_combo.addItem(exp.name, exp)
        form.addRow("Exposure:", exposure_combo)

        front_check = QCheckBox()
        front_check.setChecked(True)
        form.addRow("Front:", front_check)

        orient_combo = QComboBox()
        for o in TargetOrientation:
            orient_combo.addItem(o.name, o)
        form.addRow("Orientation:", orient_combo)

        blast_list = QListWidget()
        blast_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        for bm in BlastModifier:
            blast_list.addItem(bm.name)
        form.addRow("Blast Modifiers:", blast_list)

        layout.addLayout(form)
        layout.addStretch()

        self.blast_target_params[target] = {
            'range': range_spin,
            'exposure': exposure_combo,
            'front': front_check,
            'orient': orient_combo,
            'blast_mods': blast_list,
        }
        return widget

    def _prev_target(self):
        idx = self.params_stack.currentIndex()
        if idx > 0:
            self.params_stack.setCurrentIndex(idx - 1)
            self._update_target_nav()

    def _next_target(self):
        idx = self.params_stack.currentIndex()
        if idx < self.params_stack.count() - 1:
            self.params_stack.setCurrentIndex(idx + 1)
            self._update_target_nav()

    def _update_target_nav(self):
        idx = self.params_stack.currentIndex()
        count = self.params_stack.count()
        self.t_prev_btn.setEnabled(idx > 0)
        self.t_next_btn.setEnabled(idx < count - 1)
        if 0 <= idx < len(self.blast_targets):
            self.t_label.setText(f"Target {idx + 1} of {count}: {self.blast_targets[idx].name}")
        else:
            self.t_label.setText("")

    # ── Simulate ──────────────────────────────────────────────────────────

    def _simulate(self):
        ammo: AmmoType | None = self.ammo_combo.currentData()
        if not ammo:
            QMessageBox.warning(self, "Error", "Please select explosive ammunition")
            return
        if not self.blast_targets:
            QMessageBox.warning(self, "Error", "Please select at least one blast target")
            return

        targets = []
        ranges_from_burst = []
        exposures = []
        sp_list = []
        front_list = []
        blast_mod_list = []

        for target in self.blast_targets:
            p = self.blast_target_params[target]
            targets.append(target)
            ranges_from_burst.append(p['range'].value())
            exposures.append(p['exposure'].currentData())
            front_list.append(p['front'].isChecked())

            sp = ShotParameters(
                aim_time_ac=0,
                situation_stance_modifiers=[],
                visibility_modifiers=[],
                target_orientation=p['orient'].currentData(),
            )
            sp_list.append(sp)

            bm = []
            for sel in p['blast_mods'].selectedItems():
                bm.append(list(BlastModifier)[p['blast_mods'].row(sel)])
            if not bm:
                bm.append(BlastModifier.IN_THE_OPEN)
            blast_mod_list.append(bm)

        results = CombatSimulator.explosion_damage(
            ammo, targets, ranges_from_burst, exposures, sp_list, front_list, blast_mod_list
        )
        self.last_results = results

        # ── Log to main window ────────────────────────────────────────────
        main_window = self.window()
        while main_window and not hasattr(main_window, 'combat_log'):
            main_window = main_window.parent()

        if main_window and hasattr(main_window, 'combat_log'):
            main_window.combat_log.append_system(
                f"Explosion ({ammo.name}) – {len(targets)} target(s)"
            )
            for result in results:
                main_window._log_shot_result(result)
            if hasattr(main_window, 'combat_zone'):
                main_window.combat_zone.refresh_cards()
            if hasattr(main_window, 'stats_display') and hasattr(main_window, 'character_list'):
                current_row = main_window.character_list.currentRow()
                if current_row >= 0:
                    main_window._on_character_selected(current_row)

        # ── Show results ──────────────────────────────────────────────────
        self.current_step = 2
        self.stack.setCurrentIndex(2)
        self._update_navigation()
        self._display_results(results)
        self.show_log_btn.setEnabled(True)

    # ── Display ───────────────────────────────────────────────────────────

    def _display_results(self, results):
        ammo = self.ammo_combo.currentData()
        text = f"<b>Explosion Damage Results</b> ({ammo.name if ammo else '?'})<br><br>"

        if not results:
            text += "<i>No damage dealt.</i>"
            self.results_text.setHtml(text)
            return

        for result in results:
            target_name = result.target.name if result.target else "Unknown"
            if result.hit and result.damage_result:
                dr = result.damage_result
                text += f"<b>{target_name}</b> – {dr.location.name}: "
                text += f"{dr.damage} damage, {dr.shock} shock<br>"
                if dr.pierced_organs:
                    text += f"&nbsp;&nbsp;Pierced: {', '.join(dr.pierced_organs)}<br>"
                if dr.is_disabled:
                    text += "&nbsp;&nbsp;<b>DISABLED</b><br>"
                if result.incapacitation_effect:
                    text += f"&nbsp;&nbsp;Incap: {result.incapacitation_effect.name}"
                    if result.incapacitation_time_phases:
                        text += f" ({result.incapacitation_time_phases} phases)"
                    text += "<br>"
                if result.recovery:
                    text += f"&nbsp;&nbsp;Healing: {result.recovery.healing_time_in_days:.1f} days<br>"
                text += "<br>"

        self.results_text.setHtml(text)

    def _show_log(self):
        if not self.last_results:
            return
        log_content = self.last_results[0].log or "No log available"

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

