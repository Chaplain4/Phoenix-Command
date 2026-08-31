"""MapShotPreviewDialog cover PF, fire-kind visibility, confirm."""

from phoenix_command.gui.dialogs.map_shot_preview_dialog import MapShotPreviewDialog
from phoenix_command.session.domains.impulse_combat_state import PendingShotPreview


def _preview(**kwargs) -> PendingShotPreview:
    data = dict(
        preview_id="p1",
        shooter_token_id="s",
        target_token_id="t",
        proposed_by="host",
        fire_kind="single",
        fire_mode="single",
        estimated_cover_pf=4.0,
        cover_notes=["wall wood"],
        target_token_ids=["t"],
    )
    data.update(kwargs)
    return PendingShotPreview(**data)


def test_estimated_and_manual_cover_pf(qapp):
    dlg = MapShotPreviewDialog(_preview(), editable=True)
    assert "4.0" in dlg.cover_notes.toPlainText()
    collected = dlg._collect()
    assert collected.manual_cover_pf is None
    dlg.manual_cover_pf.setValue(6.0)
    collected = dlg._collect()
    assert collected.manual_cover_pf == 6.0


def test_mode_visibility_burst_shotgun_area(qapp):
    burst = MapShotPreviewDialog(_preview(fire_kind="burst", fire_mode="auto"), editable=True)
    assert not burst.arc_spin.isHidden()
    assert not burst.cont_burst_spin.isHidden()
    assert burst.pick_aim_btn.isHidden()

    shotgun = MapShotPreviewDialog(_preview(fire_kind="shotgun"), editable=True)
    assert not shotgun.secondary_list.isHidden()

    area = MapShotPreviewDialog(_preview(fire_kind="grenade"), editable=True)
    assert not area.pick_aim_btn.isHidden()


def test_read_only_disables_edits(qapp):
    dlg = MapShotPreviewDialog(_preview(), editable=False)
    assert not dlg.range_spin.isEnabled()
    assert not dlg.confirm_btn.isEnabled()
    assert not dlg.apply_btn.isEnabled()


def test_confirm_sets_status(qapp):
    dlg = MapShotPreviewDialog(_preview(), editable=True)
    confirmed: list[PendingShotPreview] = []
    dlg.confirmed.connect(confirmed.append)
    dlg._on_confirm()
    assert confirmed
    assert confirmed[0].status == "confirmed"
