"""Shared Cover PF control for fire dialogs (§3.8 intervening cover)."""

from __future__ import annotations

from PyQt6.QtWidgets import QDoubleSpinBox, QFormLayout, QLabel, QWidget


def add_cover_pf_controls(layout: QFormLayout) -> QDoubleSpinBox:
    """
    Add Cover PF spinbox to a form layout.

    Returns the spinbox (default 0 = no intervening cover).
    """
    hint = QLabel("Subtracted from PEN after hit location (0 = none)")
    hint.setWordWrap(True)
    spin = QDoubleSpinBox()
    spin.setRange(0.0, 20000.0)
    spin.setDecimals(1)
    spin.setValue(0.0)
    spin.setToolTip(
        "Intervening cover Protection Factor (Table 7C). "
        "Applied after hit location; EPEN = PEN − cover PF − armor."
    )
    layout.addRow("Cover PF:", spin)
    layout.addRow("", hint)
    return spin


def cover_pf_value(spin: QDoubleSpinBox | None) -> float:
    if spin is None:
        return 0.0
    return float(spin.value())
