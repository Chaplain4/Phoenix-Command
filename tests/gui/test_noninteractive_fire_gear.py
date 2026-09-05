"""Guest shot path: noninteractive gear pick and nack keep-open."""

from __future__ import annotations

from phoenix_command.gui.dialogs.map_shot_preview_dialog import MapShotPreviewDialog
from phoenix_command.gui.main_window import MainWindow
from phoenix_command.item_database.grenades import m67
from phoenix_command.models.gear import Weapon
from phoenix_command.session.domains.impulse_combat_state import (
    PendingShotPreview,
    TokenCombatRuntime,
)


def test_prompt_fire_gear_noninteractive_prefers_held_weapon(qapp, rifle_pair):
    win = MainWindow()
    char = rifle_pair[0]
    char.add_gear(m67)
    weapons = [i for i in char.equipment if isinstance(i, Weapon)]
    assert weapons
    held = weapons[0].name
    rt = TokenCombatRuntime(held_weapon_name=held)
    weapon, grenade = win._prompt_fire_gear(char, rt, interactive=False)
    assert grenade is None
    assert weapon is not None
    assert weapon.name == held
    win.close()


def test_prompt_fire_gear_noninteractive_first_weapon_without_held(qapp, rifle_pair):
    win = MainWindow()
    char = rifle_pair[0]
    char.add_gear(m67)
    rt = TokenCombatRuntime()
    weapon, grenade = win._prompt_fire_gear(char, rt, interactive=False)
    assert grenade is None
    assert isinstance(weapon, Weapon)
    win.close()


def test_reject_confirm_keep_open_leaves_dialog(qapp):
    preview = PendingShotPreview(
        preview_id="p1",
        shooter_token_id="s",
        target_token_id="t",
        proposed_by="guest-1",
        fire_kind="single",
        fire_mode="single",
        status="confirmed",
    )
    dlg = MapShotPreviewDialog(preview, editable=True)
    dlg.reject_confirm_keep_open("Not enough AC")
    assert preview.status == "open"
    assert "Not enough AC" in dlg.windowTitle()
    assert dlg.confirm_btn.isEnabled()
    dlg.close()
