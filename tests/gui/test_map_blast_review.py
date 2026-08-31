"""Map blast review dialog and app settings."""

from phoenix_command.gui.app_settings import (
    get_show_blast_modifier_dialog,
    set_show_blast_modifier_dialog,
)
from phoenix_command.gui.dialogs.map_blast_review_dialog import MapBlastReviewDialog
from phoenix_command.models.enums import BlastModifier
from phoenix_command.session.domains.token_state import TokenPlacement, TokenState
from phoenix_command.simulations.map_blast import (
    BlastPassSpec,
    BlastVictimSpec,
    PendingBlastPackage,
)
from PyQt6.QtCore import QSettings
from PyQt6.QtWidgets import QDialog


def test_blast_review_setting_roundtrip(tmp_path, monkeypatch, qapp):
    ini = str(tmp_path / "prefs.ini")

    def fake_settings():
        return QSettings(ini, QSettings.Format.IniFormat)

    monkeypatch.setattr("phoenix_command.gui.app_settings._settings", fake_settings)
    assert get_show_blast_modifier_dialog() is True
    set_show_blast_modifier_dialog(False)
    assert get_show_blast_modifier_dialog() is False
    set_show_blast_modifier_dialog(True)
    assert get_show_blast_modifier_dialog() is True


def test_map_blast_review_dialog_overrides(qapp):
    tokens = TokenState()
    tokens.placements["e1"] = TokenPlacement(
        token_id="e1", character_name="Enemy1", q=1, r=0
    )
    package = PendingBlastPackage(
        passes=[
            BlastPassSpec(
                center_q=0,
                center_r=0,
                hit=True,
                victims=[
                    BlastVictimSpec(
                        token_id="e1",
                        range_hex=1,
                        dist_m=2.0,
                        derived_mods=[BlastModifier.IN_THE_OPEN, BlastModifier.PRONE],
                    )
                ],
            )
        ]
    )
    dlg = MapBlastReviewDialog(package, tokens)
    assert dlg.mod_overrides()["e1"] == [
        BlastModifier.IN_THE_OPEN,
        BlastModifier.PRONE,
    ]
    dlg.accept()
    assert dlg.result() == QDialog.DialogCode.Accepted
