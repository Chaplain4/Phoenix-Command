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


def test_close_event_emits_cancelled_once(qapp):
    dlg = MapShotPreviewDialog(_preview(), editable=True)
    cancelled: list[str] = []
    dlg.cancelled.connect(cancelled.append)
    dlg.close()
    assert cancelled == ["p1"]
    assert dlg._cancel_emitted is True
    dlg.close()
    assert cancelled == ["p1"]


def test_cancel_button_then_close_does_not_double_emit(qapp):
    dlg = MapShotPreviewDialog(_preview(), editable=True)
    cancelled: list[str] = []
    dlg.cancelled.connect(cancelled.append)
    dlg._on_cancel()
    assert cancelled == ["p1"]
    dlg.close()
    assert cancelled == ["p1"]


def test_accept_after_confirm_does_not_emit_cancelled(qapp):
    dlg = MapShotPreviewDialog(_preview(), editable=True)
    cancelled: list[str] = []
    dlg.cancelled.connect(cancelled.append)
    dlg.accept_after_confirm()
    assert cancelled == []


def test_load_preview_preserves_custom_eal_modifiers(qapp):
    """Opening the dialog must not wipe Hit-before-fire customs via early _collect."""
    preview = _preview(
        custom_eal_modifiers=[
            {"label": "Hit before fire (§5.7)", "alm": -10},
        ],
        target_token_ids=["t"],
        per_target={"t": {"range_hexes": 3}},
    )
    dlg = MapShotPreviewDialog(preview, editable=True)
    assert dlg.custom_table.rowCount() == 1
    assert dlg.custom_table.item(0, 0).text() == "Hit before fire (§5.7)"
    assert dlg.custom_table.item(0, 1).text() == "-10"
    collected = dlg._collect()
    assert any(
        c.get("alm") == -10 and "Hit before fire" in c.get("label", "")
        for c in collected.custom_eal_modifiers
    )
    dlg.close()
