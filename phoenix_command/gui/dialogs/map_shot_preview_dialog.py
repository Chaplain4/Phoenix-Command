"""Synced map shot preview: multi-target, aim hex, custom EAL, confirm/cancel."""

from __future__ import annotations

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
)

from phoenix_command.models.enums import (
    SituationStanceModifier4B,
    TargetOrientation,
    VisibilityModifier4C,
)
from phoenix_command.session.domains.impulse_combat_state import PendingShotPreview


class MapShotPreviewDialog(QDialog):
    """Show auto-derived shot modifiers; host/shooter can edit before confirm."""

    preview_updated = pyqtSignal(object)  # PendingShotPreview
    confirmed = pyqtSignal(object)
    cancelled = pyqtSignal(str)  # preview_id
    pick_aim_hex_requested = pyqtSignal()
    overlay_refresh_requested = pyqtSignal(object)  # PendingShotPreview

    def __init__(
        self,
        preview: PendingShotPreview,
        editable: bool = True,
        token_labels: dict[str, str] | None = None,
        *,
        aim_accumulated: int = 0,
        is_hip_fire: bool = False,
        ammo_options: list[str] | None = None,
        parent=None,
    ):
        super().__init__(parent)
        self.setWindowTitle("Shot Preview — Map Combat")
        self.setMinimumSize(600, 720)
        self._preview = preview
        self._editable = editable
        self._token_labels = token_labels or {}
        self._aim_accumulated = aim_accumulated
        self._is_hip_fire = is_hip_fire
        self._ammo_options = ammo_options or []
        self._setup_ui()
        self._load_preview()
        if not editable:
            self._set_read_only()

    def _label_for(self, token_id: str) -> str:
        return self._token_labels.get(token_id, token_id)

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)

        self.kind_label = QLabel("")
        layout.addWidget(self.kind_label)

        self.notes = QTextEdit()
        self.notes.setReadOnly(True)
        self.notes.setMaximumHeight(80)
        layout.addWidget(QLabel("Auto notes:"))
        layout.addWidget(self.notes)

        form = QFormLayout()
        self.range_spin = QSpinBox()
        self.range_spin.setRange(1, 500)
        form.addRow("Range (rule hex):", self.range_spin)

        self.aim_spin = QSpinBox()
        self.aim_spin.setRange(0, 40)
        form.addRow("Aim Time (AC):", self.aim_spin)
        self._aim_hint = QLabel("")
        form.addRow("", self._aim_hint)

        self.exposure_combo = QComboBox()
        form.addRow("Target Exposure:", self.exposure_combo)

        self.orient_combo = QComboBox()
        for o in TargetOrientation:
            self.orient_combo.addItem(o.name, o.name)
        form.addRow("Orientation:", self.orient_combo)

        self.fire_mode_combo = QComboBox()
        for mode in ("single", "3rb", "auto"):
            self.fire_mode_combo.addItem(mode, mode)
        self.fire_mode_combo.currentIndexChanged.connect(self._on_mode_changed)
        form.addRow("Fire mode:", self.fire_mode_combo)

        self.arc_spin = QDoubleSpinBox()
        self.arc_spin.setRange(0.0, 50.0)
        self.arc_spin.setDecimals(1)
        self.arc_spin.setSpecialValueText("auto min")
        form.addRow("Arc of fire:", self.arc_spin)

        self.cont_burst_spin = QSpinBox()
        self.cont_burst_spin.setRange(0, 20)
        form.addRow("Continuous burst impulses:", self.cont_burst_spin)

        self.aim_hex_label = QLabel("—")
        aim_row = QHBoxLayout()
        aim_row.addWidget(self.aim_hex_label)
        self.pick_aim_btn = QPushButton("Pick aim hex")
        self.pick_aim_btn.clicked.connect(self.pick_aim_hex_requested.emit)
        aim_row.addWidget(self.pick_aim_btn)
        form.addRow("Aim hex:", aim_row)

        self.tof_label = QLabel("0")
        form.addRow("TOF (impulses):", self.tof_label)

        self.weapon_label = QLabel("")
        form.addRow("Weapon:", self.weapon_label)

        self.ammo_combo = QComboBox()
        self.ammo_combo.currentIndexChanged.connect(self._on_ammo_changed)
        form.addRow("Ammo:", self.ammo_combo)

        self.cover_notes = QTextEdit()
        self.cover_notes.setReadOnly(True)
        self.cover_notes.setMaximumHeight(60)
        form.addRow("Cover:", self.cover_notes)

        self.manual_cover_pf = QDoubleSpinBox()
        self.manual_cover_pf.setRange(0.0, 20000.0)
        self.manual_cover_pf.setDecimals(1)
        self.manual_cover_pf.setSpecialValueText("auto (geometry)")
        self.manual_cover_pf.setValue(0.0)
        self.manual_cover_pf.setToolTip(
            "0 = use map geometry per hit location; >0 forces fixed Cover PF"
        )
        form.addRow("Manual Cover PF:", self.manual_cover_pf)

        layout.addLayout(form)

        layout.addWidget(QLabel("Primary targets:"))
        self.target_list = QListWidget()
        self.target_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.target_list.itemSelectionChanged.connect(self._emit_overlay)
        layout.addWidget(self.target_list)

        layout.addWidget(QLabel("Secondary (pattern) targets:"))
        self.secondary_list = QListWidget()
        self.secondary_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        layout.addWidget(self.secondary_list)

        layout.addWidget(QLabel("Stance modifiers:"))
        self.stance_list = QListWidget()
        self.stance_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        for s in SituationStanceModifier4B:
            self.stance_list.addItem(s.name)
        layout.addWidget(self.stance_list)

        layout.addWidget(QLabel("Visibility modifiers:"))
        self.vis_list = QListWidget()
        self.vis_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        for v in VisibilityModifier4C:
            self.vis_list.addItem(v.name)
        layout.addWidget(self.vis_list)

        layout.addWidget(QLabel("Custom EAL modifiers:"))
        self.custom_table = QTableWidget(0, 2)
        self.custom_table.setHorizontalHeaderLabels(["Label", "ALM"])
        layout.addWidget(self.custom_table)
        custom_row = QHBoxLayout()
        self.custom_label = QLineEdit()
        self.custom_label.setPlaceholderText("Label")
        self.custom_alm = QSpinBox()
        self.custom_alm.setRange(-50, 50)
        add_custom = QPushButton("Add")
        add_custom.clicked.connect(self._add_custom)
        rem_custom = QPushButton("Remove")
        rem_custom.clicked.connect(self._remove_custom)
        custom_row.addWidget(self.custom_label)
        custom_row.addWidget(self.custom_alm)
        custom_row.addWidget(add_custom)
        custom_row.addWidget(rem_custom)
        layout.addLayout(custom_row)

        buttons = QDialogButtonBox()
        self.confirm_btn = buttons.addButton("Confirm Shot", QDialogButtonBox.ButtonRole.AcceptRole)
        self.cancel_btn = buttons.addButton("Cancel", QDialogButtonBox.ButtonRole.RejectRole)
        self.apply_btn = buttons.addButton("Apply Edits", QDialogButtonBox.ButtonRole.ActionRole)
        self.confirm_btn.clicked.connect(self._on_confirm)
        self.cancel_btn.clicked.connect(self._on_cancel)
        self.apply_btn.clicked.connect(self._on_apply)
        layout.addWidget(buttons)

    def _on_mode_changed(self) -> None:
        self._update_mode_visibility()

    def _on_ammo_changed(self) -> None:
        if not self._editable or not self._ammo_options:
            return
        name = self.ammo_combo.currentData()
        if name:
            self._preview.ammo_name = name
            self.preview_updated.emit(self._collect())

    def _update_mode_visibility(self) -> None:
        kind = self._preview.fire_kind or "single"
        mode = self.fire_mode_combo.currentData() or self._preview.fire_mode
        is_area = kind in ("grenade", "agl", "explosive")
        is_burst = kind in ("burst", "shotgun_burst") or mode == "auto"
        is_shotgun = kind in ("shotgun", "shotgun_burst")
        self.arc_spin.setVisible(is_burst or kind == "agl")
        self.cont_burst_spin.setVisible(is_burst or kind == "agl")
        # Find form labels — widgets stay; pick aim for area
        self.pick_aim_btn.setVisible(is_area)
        self.aim_hex_label.setVisible(True)
        self.secondary_list.setVisible(is_shotgun)
        multi = is_burst or is_area or is_shotgun
        self.target_list.setSelectionMode(
            QListWidget.SelectionMode.MultiSelection
            if multi
            else QListWidget.SelectionMode.SingleSelection
        )
        self.kind_label.setText(f"Fire kind: {kind} (mode={mode})")

    def _load_preview(self) -> None:
        p = self._preview
        self.notes.setPlainText("\n".join(p.notes))
        self.range_spin.setValue(p.range_hexes)
        self.aim_spin.setValue(p.aim_time_ac)
        if self._is_hip_fire:
            self.aim_spin.setValue(1)
            self.aim_spin.setEnabled(False)
            self._aim_hint.setText("Hip fire — 1 AC aim time for EAL (−6 ALM)")
        elif self._aim_accumulated > 0:
            self.aim_spin.setMaximum(self._aim_accumulated)
            self.aim_spin.setEnabled(self._editable)
            self._aim_hint.setText(f"Aim AC spent on target: {self._aim_accumulated}")
        else:
            self.aim_spin.setEnabled(self._editable)
            self._aim_hint.setText("")
        self.tof_label.setText(str(p.tof_impulses))
        self.weapon_label.setText(p.weapon_name)
        self.ammo_combo.blockSignals(True)
        self.ammo_combo.clear()
        if self._ammo_options:
            for name in self._ammo_options:
                self.ammo_combo.addItem(name, name)
            if p.ammo_name:
                aidx = self.ammo_combo.findData(p.ammo_name)
                if aidx >= 0:
                    self.ammo_combo.setCurrentIndex(aidx)
            self.ammo_combo.setEnabled(self._editable and len(self._ammo_options) > 1)
        elif p.ammo_name:
            self.ammo_combo.addItem(p.ammo_name, p.ammo_name)
            self.ammo_combo.setEnabled(False)
        else:
            self.ammo_combo.addItem("—", "")
            self.ammo_combo.setEnabled(False)
        self.ammo_combo.blockSignals(False)
        cover_lines = list(p.cover_notes or [])
        if p.estimated_cover_pf:
            cover_lines.append(f"Estimated max cover PF on body ≈ {p.estimated_cover_pf:.1f}")
        self.cover_notes.setPlainText("\n".join(cover_lines) if cover_lines else "(none)")
        if p.manual_cover_pf is not None and p.manual_cover_pf > 0:
            self.manual_cover_pf.setValue(float(p.manual_cover_pf))
        else:
            self.manual_cover_pf.setValue(0.0)
        if p.arc_of_fire is None:
            self.arc_spin.setValue(0.0)
        else:
            self.arc_spin.setValue(float(p.arc_of_fire))
        self.cont_burst_spin.setValue(p.continuous_burst_impulses)
        if p.aim_q is not None and p.aim_r is not None:
            self.aim_hex_label.setText(f"({p.aim_q}, {p.aim_r})")
        else:
            self.aim_hex_label.setText("—")

        self.exposure_combo.clear()
        exposures = p.visible_exposures or [p.selected_exposure or p.exposure]
        for name in exposures:
            self.exposure_combo.addItem(name, name)
        if p.selected_exposure and self.exposure_combo.findData(p.selected_exposure) < 0:
            self.exposure_combo.addItem(p.selected_exposure, p.selected_exposure)
        idx = self.exposure_combo.findData(p.selected_exposure or p.exposure)
        if idx >= 0:
            self.exposure_combo.setCurrentIndex(idx)

        oidx = self.orient_combo.findData(p.orientation)
        if oidx >= 0:
            self.orient_combo.setCurrentIndex(oidx)
        midx = self.fire_mode_combo.findData(p.fire_mode)
        if midx >= 0:
            self.fire_mode_combo.setCurrentIndex(midx)

        self.target_list.clear()
        selected = set(p.primary_ids())
        # Show all known targets from per_target + primary
        all_ids = list(dict.fromkeys(list(p.primary_ids()) + list(p.per_target.keys())))
        for tid in all_ids:
            item = QListWidgetItem(self._label_for(tid))
            item.setData(256, tid)  # Qt.UserRole
            self.target_list.addItem(item)
            item.setSelected(tid in selected)

        self.secondary_list.clear()
        sec_selected: set[str] = set()
        for secs in p.secondary_by_primary.values():
            sec_selected.update(secs)
        for tid in sec_selected:
            item = QListWidgetItem(self._label_for(tid))
            item.setData(256, tid)
            self.secondary_list.addItem(item)
            item.setSelected(True)
        # Also offer other pattern candidates already in per_target but not primary
        for tid in p.per_target:
            if tid in selected or tid in sec_selected:
                continue
            item = QListWidgetItem(self._label_for(tid))
            item.setData(256, tid)
            self.secondary_list.addItem(item)

        for i in range(self.stance_list.count()):
            item = self.stance_list.item(i)
            item.setSelected(item.text() in p.stance_mods)
        for i in range(self.vis_list.count()):
            item = self.vis_list.item(i)
            item.setSelected(item.text() in p.visibility_mods)

        self.custom_table.setRowCount(0)
        for entry in p.custom_eal_modifiers:
            label = entry.get("label", "") if isinstance(entry, dict) else str(entry[0])
            alm = entry.get("alm", 0) if isinstance(entry, dict) else int(entry[1])
            row = self.custom_table.rowCount()
            self.custom_table.insertRow(row)
            self.custom_table.setItem(row, 0, QTableWidgetItem(label))
            self.custom_table.setItem(row, 1, QTableWidgetItem(str(alm)))

        self._update_mode_visibility()
        self._emit_overlay()

    def _set_read_only(self) -> None:
        for w in (
            self.range_spin,
            self.aim_spin,
            self.exposure_combo,
            self.orient_combo,
            self.fire_mode_combo,
            self.arc_spin,
            self.cont_burst_spin,
            self.pick_aim_btn,
            self.target_list,
            self.secondary_list,
            self.stance_list,
            self.vis_list,
            self.custom_table,
            self.custom_label,
            self.custom_alm,
            self.apply_btn,
            self.confirm_btn,
        ):
            w.setEnabled(False)

    def _add_custom(self) -> None:
        label = self.custom_label.text().strip() or "custom"
        row = self.custom_table.rowCount()
        self.custom_table.insertRow(row)
        self.custom_table.setItem(row, 0, QTableWidgetItem(label))
        self.custom_table.setItem(row, 1, QTableWidgetItem(str(self.custom_alm.value())))
        self.custom_label.clear()

    def _remove_custom(self) -> None:
        row = self.custom_table.currentRow()
        if row >= 0:
            self.custom_table.removeRow(row)

    def set_aim_hex(self, q: int, r: int, layer_id: str = "") -> None:
        self._preview.aim_q = q
        self._preview.aim_r = r
        if layer_id:
            self._preview.aim_layer_id = layer_id
        self.aim_hex_label.setText(f"({q}, {r})")
        self._emit_overlay()

    def _selected_ids(self, list_widget: QListWidget) -> list[str]:
        ids = []
        for i in range(list_widget.count()):
            item = list_widget.item(i)
            if item.isSelected():
                tid = item.data(256)
                if tid:
                    ids.append(tid)
        return ids

    def _collect(self) -> PendingShotPreview:
        p = self._preview
        p.range_hexes = self.range_spin.value()
        p.aim_time_ac = self.aim_spin.value()
        p.selected_exposure = self.exposure_combo.currentData() or p.selected_exposure
        p.exposure = p.selected_exposure
        p.orientation = self.orient_combo.currentData() or p.orientation
        p.fire_mode = self.fire_mode_combo.currentData() or p.fire_mode
        if self._ammo_options:
            p.ammo_name = self.ammo_combo.currentData() or p.ammo_name
        arc_val = self.arc_spin.value()
        p.arc_of_fire = None if arc_val <= 0 else float(arc_val)
        p.continuous_burst_impulses = self.cont_burst_spin.value()

        primaries = self._selected_ids(self.target_list)
        if primaries:
            p.target_token_ids = primaries
            p.target_token_id = primaries[0]
        secondaries = self._selected_ids(self.secondary_list)
        if p.fire_kind in ("shotgun", "shotgun_burst") or secondaries:
            # Attach all secondaries to first primary for single shotgun;
            # for burst, distribute same list to each primary (editable simplification)
            if p.fire_kind == "shotgun_burst" and len(primaries) > 1:
                p.secondary_by_primary = {pid: list(secondaries) for pid in primaries}
            elif primaries:
                p.secondary_by_primary = {primaries[0]: list(secondaries)}
            else:
                p.secondary_by_primary = {}

        p.stance_mods = [
            self.stance_list.item(i).text()
            for i in range(self.stance_list.count())
            if self.stance_list.item(i).isSelected()
        ]
        p.visibility_mods = [
            self.vis_list.item(i).text()
            for i in range(self.vis_list.count())
            if self.vis_list.item(i).isSelected()
        ]
        customs = []
        for row in range(self.custom_table.rowCount()):
            lab = self.custom_table.item(row, 0)
            alm = self.custom_table.item(row, 1)
            if lab and alm:
                try:
                    customs.append({"label": lab.text(), "alm": int(alm.text())})
                except ValueError:
                    pass
        p.custom_eal_modifiers = customs
        mcp = float(self.manual_cover_pf.value())
        p.manual_cover_pf = mcp if mcp > 0 else None
        return p

    def _emit_overlay(self) -> None:
        self.overlay_refresh_requested.emit(self._collect() if self._editable else self._preview)

    def _on_apply(self) -> None:
        p = self._collect()
        self.preview_updated.emit(p)
        self.overlay_refresh_requested.emit(p)

    def _on_confirm(self) -> None:
        p = self._collect()
        p.status = "confirmed"
        self.confirmed.emit(p)
        self.accept()

    def _on_cancel(self) -> None:
        self.cancelled.emit(self._preview.preview_id)
        self.reject()

    def apply_remote_preview(
        self,
        preview: PendingShotPreview,
        *,
        aim_accumulated: int | None = None,
        is_hip_fire: bool | None = None,
    ) -> None:
        self._preview = preview
        if aim_accumulated is not None:
            self._aim_accumulated = aim_accumulated
        if is_hip_fire is not None:
            self._is_hip_fire = is_hip_fire
        self._load_preview()

    def closeEvent(self, event) -> None:
        self.overlay_refresh_requested.emit(None)
        super().closeEvent(event)
