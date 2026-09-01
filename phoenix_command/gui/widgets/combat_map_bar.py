"""Combat mode toolbar for hex map (impulse clock, actions)."""

from __future__ import annotations

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from phoenix_command.session.domains.impulse_combat_state import ImpulseCombatState


class CombatMapBar(QWidget):
    """Phase/impulse display and token action controls."""

    advance_impulse_requested = pyqtSignal()
    combat_action_requested = pyqtSignal(str, str, dict)  # token_id, action, args
    token_selected = pyqtSignal(str)
    declare_shot_requested = pyqtSignal(str)  # shooter token_id
    ruler_requested = pyqtSignal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._is_host = True
        self._impulse_combat = ImpulseCombatState()
        self._available_actions: list[tuple[str, str, float | str]] = []
        self._selected_token_id: str | None = None

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setMaximumHeight(72)
        scroll.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        inner = QWidget()
        layout = QVBoxLayout(inner)
        layout.setContentsMargins(4, 2, 4, 2)
        layout.setSpacing(2)

        row1 = QHBoxLayout()
        row1.setContentsMargins(0, 0, 0, 0)
        row2 = QHBoxLayout()
        row2.setContentsMargins(0, 0, 0, 0)

        self._phase_label = QLabel("Phase 1")
        row1.addWidget(self._phase_label)
        self._impulse_label = QLabel("Impulse 1/4")
        row1.addWidget(self._impulse_label)

        self._next_impulse_btn = QPushButton("Next Impulse")
        self._next_impulse_btn.clicked.connect(self.advance_impulse_requested.emit)
        row1.addWidget(self._next_impulse_btn)

        row1.addWidget(QLabel("|"))

        self._token_combo = QComboBox()
        self._token_combo.setSizeAdjustPolicy(
            QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon
        )
        self._token_combo.setMinimumContentsLength(6)
        self._token_combo.currentIndexChanged.connect(self._on_token_changed)
        row1.addWidget(QLabel("Token:"))
        row1.addWidget(self._token_combo)

        self._status_label = QLabel("")
        self._status_label.setMinimumWidth(0)
        self._status_label.setMaximumWidth(220)
        self._status_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self._status_label.setToolTip("AC remaining this impulse (and pending progress)")
        row1.addWidget(self._status_label)
        row1.addStretch()

        self._action_combo = QComboBox()
        self._action_combo.setSizeAdjustPolicy(
            QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon
        )
        self._action_combo.setMinimumContentsLength(10)
        row2.addWidget(QLabel("Action:"))
        row2.addWidget(self._action_combo)

        self._aim_spin = QSpinBox()
        self._aim_spin.setRange(1, 20)
        self._aim_spin.setValue(1)
        row2.addWidget(QLabel("AC:"))
        row2.addWidget(self._aim_spin)

        self._fire_mode_combo = QComboBox()
        for mode in ("single", "3rb", "auto"):
            self._fire_mode_combo.addItem(mode, mode)
        self._fire_mode_combo.currentIndexChanged.connect(self._on_fire_mode_changed)
        row2.addWidget(self._fire_mode_combo)

        self._do_action_btn = QPushButton("Do Action")
        self._do_action_btn.clicked.connect(self._emit_action)
        row2.addWidget(self._do_action_btn)

        self._duck_btn = QPushButton("Duck")
        self._duck_btn.setToolTip("Defensive Duck (0 AC). Interrupts pending actions and aim.")
        self._duck_btn.clicked.connect(self._emit_duck)
        row2.addWidget(self._duck_btn)

        self._abandon_btn = QPushButton("Abandon")
        self._abandon_btn.setToolTip("Abandon unfinished action (progress lost).")
        self._abandon_btn.clicked.connect(self._emit_abandon)
        self._abandon_btn.setEnabled(False)
        row2.addWidget(self._abandon_btn)

        self._shot_btn = QPushButton("Declare Shot")
        self._shot_btn.clicked.connect(self._emit_declare_shot)
        row2.addWidget(self._shot_btn)

        self._ruler_btn = QPushButton("Ruler")
        self._ruler_btn.clicked.connect(self.ruler_requested.emit)
        row2.addWidget(self._ruler_btn)

        row2.addStretch()
        layout.addLayout(row1)
        layout.addLayout(row2)
        scroll.setWidget(inner)
        outer.addWidget(scroll)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setMinimumWidth(0)
        self.setVisible(False)

    def set_host(self, is_host: bool) -> None:
        self._is_host = is_host
        self._next_impulse_btn.setEnabled(is_host)

    def set_impulse_combat(self, state: ImpulseCombatState) -> None:
        self._impulse_combat = state
        in_combat = state.map_mode == "combat"
        self.setVisible(in_combat)
        self._phase_label.setText(f"Phase {state.phase}")
        self._impulse_label.setText(f"Impulse {state.impulse + 1}/4")
        self._refresh_status()

    def _refresh_status(self) -> None:
        rt = self._impulse_combat.token_runtime.get(self._selected_token_id or "")
        if rt:
            full = rt.status_label()
            self._status_label.setText(full)
            self._status_label.setToolTip(full)
            metrics = self._status_label.fontMetrics()
            elided = metrics.elidedText(full, Qt.TextElideMode.ElideRight, 220)
            self._status_label.setText(elided)
            self._abandon_btn.setEnabled(rt.has_pending())
            idx = self._fire_mode_combo.findData(rt.fire_mode)
            if idx >= 0:
                self._fire_mode_combo.blockSignals(True)
                self._fire_mode_combo.setCurrentIndex(idx)
                self._fire_mode_combo.blockSignals(False)
        else:
            self._status_label.setText("")
            self._status_label.setToolTip("AC remaining this impulse (and pending progress)")
            self._abandon_btn.setEnabled(False)

    def set_tokens(self, token_labels: dict[str, str]) -> None:
        current = self._token_combo.currentData()
        self._token_combo.blockSignals(True)
        self._token_combo.clear()
        for tid, label in token_labels.items():
            self._token_combo.addItem(label, tid)
        if current:
            idx = self._token_combo.findData(current)
            if idx >= 0:
                self._token_combo.setCurrentIndex(idx)
        self._token_combo.blockSignals(False)

    def set_available_actions(
        self, actions: list[tuple[str, str, float | str]]
    ) -> None:
        self._available_actions = actions
        self._action_combo.clear()
        for action_id, label, cost in actions:
            cost_str = f" ({cost} AC)" if isinstance(cost, (int, float)) else ""
            self._action_combo.addItem(f"{label}{cost_str}", action_id)

    def select_token(self, token_id: str) -> None:
        idx = self._token_combo.findData(token_id)
        if idx >= 0:
            self._token_combo.blockSignals(True)
            self._token_combo.setCurrentIndex(idx)
            self._token_combo.blockSignals(False)
        self._selected_token_id = token_id
        self._refresh_status()
        if token_id:
            self.token_selected.emit(token_id)

    def _on_token_changed(self) -> None:
        tid = self._token_combo.currentData()
        self._selected_token_id = tid
        self._refresh_status()
        if tid:
            self.token_selected.emit(tid)

    def _on_fire_mode_changed(self) -> None:
        """Apply fire mode immediately (no separate Set Fire Mode action)."""
        if not self._is_host or not self._selected_token_id:
            return
        mode = self._fire_mode_combo.currentData()
        if not mode:
            return
        rt = self._impulse_combat.token_runtime.get(self._selected_token_id)
        if rt and rt.fire_mode == mode:
            return
        self.combat_action_requested.emit(
            self._selected_token_id, "set_fire_mode", {"fire_mode": mode}
        )

    def _emit_action(self) -> None:
        if not self._selected_token_id:
            return
        action_id = self._action_combo.currentData()
        if not action_id:
            return
        args: dict = {}
        if action_id in ("aim", "custom_action"):
            args["ac"] = self._aim_spin.value()
            if action_id == "custom_action":
                args["label"] = "Custom"
        self.combat_action_requested.emit(self._selected_token_id, action_id, args)

    def _emit_duck(self) -> None:
        if self._selected_token_id:
            self.combat_action_requested.emit(self._selected_token_id, "duck", {})

    def _emit_abandon(self) -> None:
        if self._selected_token_id:
            self.combat_action_requested.emit(
                self._selected_token_id, "abandon_pending", {}
            )

    def _emit_declare_shot(self) -> None:
        if self._selected_token_id:
            self.declare_shot_requested.emit(self._selected_token_id)
