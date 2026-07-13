"""Synced map shot preview: auto modifiers, custom EAL, confirm/cancel."""

from __future__ import annotations

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from phoenix_command.models.enums import (
    SituationStanceModifier4B,
    TargetExposure,
    TargetOrientation,
    VisibilityModifier4C,
)
from phoenix_command.session.domains.impulse_combat_state import PendingShotPreview


class MapShotPreviewDialog(QDialog):
    """Show auto-derived shot modifiers; host/shooter can edit before confirm."""

    preview_updated = pyqtSignal(object)  # PendingShotPreview
    confirmed = pyqtSignal(object)
    cancelled = pyqtSignal(str)  # preview_id

    def __init__(
        self,
        preview: PendingShotPreview,
        editable: bool = True,
        parent=None,
    ):
        super().__init__(parent)
        self.setWindowTitle("Shot Preview — Map Combat")
        self.setMinimumSize(560, 640)
        self._preview = preview
        self._editable = editable
        self._setup_ui()
        self._load_preview()
        if not editable:
            self._set_read_only()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)

        self.notes = QTextEdit()
        self.notes.setReadOnly(True)
        self.notes.setMaximumHeight(100)
        layout.addWidget(QLabel("Auto notes:"))
        layout.addWidget(self.notes)

        form = QFormLayout()
        self.range_spin = QSpinBox()
        self.range_spin.setRange(1, 500)
        form.addRow("Range (rule hex):", self.range_spin)

        self.aim_spin = QSpinBox()
        self.aim_spin.setRange(0, 40)
        form.addRow("Aim Time (AC):", self.aim_spin)

        self.exposure_combo = QComboBox()
        form.addRow("Target Exposure:", self.exposure_combo)

        self.orient_combo = QComboBox()
        for o in TargetOrientation:
            self.orient_combo.addItem(o.name, o.name)
        form.addRow("Orientation:", self.orient_combo)

        self.fire_mode_combo = QComboBox()
        for mode in ("single", "3rb", "auto"):
            self.fire_mode_combo.addItem(mode, mode)
        form.addRow("Fire mode:", self.fire_mode_combo)

        self.tof_label = QLabel("0")
        form.addRow("TOF (impulses):", self.tof_label)

        self.weapon_label = QLabel("")
        form.addRow("Weapon:", self.weapon_label)

        layout.addLayout(form)

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

    def _load_preview(self) -> None:
        p = self._preview
        self.notes.setPlainText("\n".join(p.notes))
        self.range_spin.setValue(p.range_hexes)
        self.aim_spin.setValue(p.aim_time_ac)
        self.tof_label.setText(str(p.tof_impulses))
        self.weapon_label.setText(f"{p.weapon_name} / {p.ammo_name}" if p.ammo_name else p.weapon_name)

        self.exposure_combo.clear()
        exposures = p.visible_exposures or [p.selected_exposure or p.exposure]
        for name in exposures:
            self.exposure_combo.addItem(name, name)
        # Also allow current selection even if not in list
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

    def _set_read_only(self) -> None:
        for w in (
            self.range_spin,
            self.aim_spin,
            self.exposure_combo,
            self.orient_combo,
            self.fire_mode_combo,
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

    def _collect(self) -> PendingShotPreview:
        p = self._preview
        p.range_hexes = self.range_spin.value()
        p.aim_time_ac = self.aim_spin.value()
        p.selected_exposure = self.exposure_combo.currentData() or p.selected_exposure
        p.exposure = p.selected_exposure
        p.orientation = self.orient_combo.currentData() or p.orientation
        p.fire_mode = self.fire_mode_combo.currentData() or p.fire_mode
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
        return p

    def _on_apply(self) -> None:
        self.preview_updated.emit(self._collect())

    def _on_confirm(self) -> None:
        p = self._collect()
        p.status = "confirmed"
        self.confirmed.emit(p)
        self.accept()

    def _on_cancel(self) -> None:
        self.cancelled.emit(self._preview.preview_id)
        self.reject()

    def apply_remote_preview(self, preview: PendingShotPreview) -> None:
        self._preview = preview
        self._load_preview()
