"""Combat mode toolbar for hex map (impulse clock, actions)."""

from __future__ import annotations

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSpinBox,
    QWidget,
)

from phoenix_command.session.domains.impulse_combat_state import ImpulseCombatState


class CombatMapBar(QWidget):
    """Phase/impulse display and token action controls."""

    map_mode_changed = pyqtSignal(str)
    advance_impulse_requested = pyqtSignal()
    combat_action_requested = pyqtSignal(str, str, dict)  # token_id, action, args
    token_selected = pyqtSignal(str)
    declare_shot_requested = pyqtSignal(str)  # shooter token_id

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._is_host = True
        self._impulse_combat = ImpulseCombatState()
        self._available_actions: list[tuple[str, str, float | str]] = []
        self._selected_token_id: str | None = None

        layout = QHBoxLayout(self)
        layout.setContentsMargins(4, 2, 4, 2)

        self._edit_btn = QPushButton("Edit")
        self._edit_btn.setCheckable(True)
        self._edit_btn.setChecked(True)
        self._edit_btn.clicked.connect(lambda: self._set_mode("edit"))
        layout.addWidget(self._edit_btn)

        self._combat_btn = QPushButton("Combat")
        self._combat_btn.setCheckable(True)
        self._combat_btn.clicked.connect(lambda: self._set_mode("combat"))
        layout.addWidget(self._combat_btn)

        layout.addWidget(QLabel("|"))

        self._phase_label = QLabel("Phase 1")
        layout.addWidget(self._phase_label)
        self._impulse_label = QLabel("Impulse 1/4")
        layout.addWidget(self._impulse_label)

        self._next_impulse_btn = QPushButton("Next Impulse")
        self._next_impulse_btn.clicked.connect(self.advance_impulse_requested.emit)
        layout.addWidget(self._next_impulse_btn)

        layout.addWidget(QLabel("|"))

        self._token_combo = QComboBox()
        self._token_combo.currentIndexChanged.connect(self._on_token_changed)
        layout.addWidget(QLabel("Token:"))
        layout.addWidget(self._token_combo)

        self._status_label = QLabel("")
        self._status_label.setMinimumWidth(200)
        self._status_label.setToolTip("AC remaining this impulse (and move progress)")
        layout.addWidget(self._status_label)

        self._action_combo = QComboBox()
        layout.addWidget(QLabel("Action:"))
        layout.addWidget(self._action_combo)

        self._aim_spin = QSpinBox()
        self._aim_spin.setRange(1, 20)
        self._aim_spin.setValue(1)
        layout.addWidget(QLabel("AC:"))
        layout.addWidget(self._aim_spin)

        self._fire_mode_combo = QComboBox()
        for mode in ("single", "3rb", "auto"):
            self._fire_mode_combo.addItem(mode, mode)
        layout.addWidget(self._fire_mode_combo)

        self._do_action_btn = QPushButton("Do Action")
        self._do_action_btn.clicked.connect(self._emit_action)
        layout.addWidget(self._do_action_btn)

        self._shot_btn = QPushButton("Declare Shot")
        self._shot_btn.clicked.connect(self._emit_declare_shot)
        layout.addWidget(self._shot_btn)

        layout.addStretch()
        self.setVisible(False)

    def set_host(self, is_host: bool) -> None:
        self._is_host = is_host
        self._next_impulse_btn.setEnabled(is_host)
        self._edit_btn.setEnabled(is_host)
        self._combat_btn.setEnabled(is_host)

    def set_impulse_combat(self, state: ImpulseCombatState) -> None:
        self._impulse_combat = state
        in_combat = state.map_mode == "combat"
        self.setVisible(in_combat or self._is_host)
        self._edit_btn.setChecked(state.map_mode == "edit")
        self._combat_btn.setChecked(in_combat)
        self._phase_label.setText(f"Phase {state.phase}")
        self._impulse_label.setText(f"Impulse {state.impulse + 1}/4")
        self._refresh_status()

    def _refresh_status(self) -> None:
        rt = self._impulse_combat.token_runtime.get(self._selected_token_id or "")
        if rt:
            self._status_label.setText(rt.status_label())
            idx = self._fire_mode_combo.findData(rt.fire_mode)
            if idx >= 0:
                self._fire_mode_combo.blockSignals(True)
                self._fire_mode_combo.setCurrentIndex(idx)
                self._fire_mode_combo.blockSignals(False)
        else:
            self._status_label.setText("")

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

    def _set_mode(self, mode: str) -> None:
        if not self._is_host:
            return
        self.map_mode_changed.emit(mode)

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
        if action_id == "set_fire_mode":
            args["fire_mode"] = self._fire_mode_combo.currentData()
        self.combat_action_requested.emit(self._selected_token_id, action_id, args)

    def _emit_declare_shot(self) -> None:
        if self._selected_token_id:
            self.declare_shot_requested.emit(self._selected_token_id)
