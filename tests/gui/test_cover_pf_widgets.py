"""Cover PF helper widget."""

from PyQt6.QtWidgets import QDoubleSpinBox, QFormLayout, QWidget

from phoenix_command.gui.dialogs.cover_pf_controls import add_cover_pf_controls, cover_pf_value


def test_cover_pf_default_and_value(qapp):
    host = QWidget()
    layout = QFormLayout(host)
    spin = add_cover_pf_controls(layout)
    assert isinstance(spin, QDoubleSpinBox)
    assert spin.value() == 0.0
    assert cover_pf_value(spin) == 0.0
    spin.setValue(4.5)
    assert cover_pf_value(spin) == 4.5


def test_cover_pf_value_none():
    assert cover_pf_value(None) == 0.0
