"""Editor category panel, map mode, combat bar, CATEGORY_MODES."""

from phoenix_command.gui.widgets.combat_map_bar import CombatMapBar
from phoenix_command.gui.widgets.editor_category_panel import EditorCategoryPanel
from phoenix_command.gui.widgets.hex_map_modes import CATEGORY_MODES, EditMode, EditorCategory
from phoenix_command.gui.widgets.map_mode_panel import MapModePanel
from phoenix_command.session.domains.impulse_combat_state import ImpulseCombatState


def test_category_modes_cover_all_edit_modes():
    covered: set[EditMode] = set()
    for modes in CATEGORY_MODES.values():
        covered.update(modes)
    assert covered == set(EditMode)


def test_editor_category_panel_set_and_click(qapp):
    seen: list[EditorCategory] = []
    panel = EditorCategoryPanel(seen.append)
    panel.set_category(EditorCategory.TERRAIN)
    assert panel._buttons[EditorCategory.TERRAIN].isChecked()
    assert not panel._buttons[EditorCategory.MAP].isChecked()
    panel._buttons[EditorCategory.OBJECTS].click()
    assert seen[-1] == EditorCategory.OBJECTS


def test_map_mode_panel_host_and_guest(qapp):
    panel = MapModePanel()
    modes: list[str] = []
    panel.map_mode_changed.connect(modes.append)
    panel.set_host(True)
    panel._combat_btn.click()
    assert modes[-1] == "combat"
    panel.set_host(False)
    assert not panel._edit_btn.isEnabled()
    modes.clear()
    panel._edit_btn.click()
    assert modes == []


def test_combat_map_bar_impulse_and_actions(qapp):
    bar = CombatMapBar()
    assert not bar.isVisible()
    state = ImpulseCombatState(map_mode="combat", phase=2, impulse=1)
    bar.set_impulse_combat(state)
    assert bar.isVisible()
    assert "Phase 2" in bar._phase_label.text()
    assert "Impulse 2/4" in bar._impulse_label.text()

    bar.set_host(False)
    assert not bar._next_impulse_btn.isEnabled()
    bar.set_host(True)

    bar.set_tokens({"t1": "Rifleman"})
    bar.select_token("t1")
    bar.set_available_actions([("aim", "Aim", 2)])
    bar._aim_spin.setValue(4)
    actions: list[tuple] = []
    bar.combat_action_requested.connect(lambda tid, act, args: actions.append((tid, act, args)))
    shots: list[str] = []
    bar.declare_shot_requested.connect(shots.append)
    bar._emit_action()
    assert actions == [("t1", "aim", {"ac": 4})]
    bar._emit_declare_shot()
    assert shots == ["t1"]
