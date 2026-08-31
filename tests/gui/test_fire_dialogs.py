"""Fire dialog construction, wizard nav, Cover PF → ShotParameters."""

from unittest.mock import MagicMock

from tests.gui.conftest import ensure_ammo_combo

from phoenix_command.gui.dialogs.burst_fire_dialog import BurstFireDialog
from phoenix_command.gui.dialogs.shot_dialog import ShotDialog
from phoenix_command.gui.dialogs.shotgun_burst_fire_dialog import ShotgunBurstFireDialog
from phoenix_command.gui.dialogs.shotgun_dialog import ShotgunDialog
from phoenix_command.gui.dialogs.three_round_burst_dialog import ThreeRoundBurstDialog
from phoenix_command.models.hit_result_advanced import ShotParameters, ShotResult
from phoenix_command.simulations.combat_simulator import CombatSimulator


def _dummy_shot_result(target=None):
    return ShotResult(
        hit=False,
        eal=10,
        odds=20,
        roll=50,
        target=target,
        log="test",
    )


def test_shot_dialog_wizard_and_weapons(rifle_pair):
    dlg = ShotDialog(rifle_pair)
    assert dlg.stack.currentIndex() == 0
    assert dlg.weapon_combo.count() >= 1
    dlg.next_btn.click()
    assert dlg.stack.currentIndex() == 1
    dlg.prev_btn.click()
    assert dlg.stack.currentIndex() == 0


def test_shot_dialog_cover_pf_to_simulator(rifle_pair, monkeypatch):
    captured: list[ShotParameters] = []

    def fake_single_shot(shooter, target, weapon, ammo, range_hexes, exposure, shot_params, is_front):
        captured.append(shot_params)
        return _dummy_shot_result(target)

    monkeypatch.setattr(
        "phoenix_command.gui.dialogs.shot_dialog.CombatSimulator.single_shot",
        fake_single_shot,
    )
    monkeypatch.setattr(
        "phoenix_command.gui.dialogs.shot_dialog.QMessageBox.warning",
        MagicMock(),
    )
    dlg = ShotDialog(rifle_pair)
    ensure_ammo_combo(dlg)
    assert dlg.ammo_combo.currentData() is not None
    assert dlg.target_combo.currentData() is not None
    dlg.cover_pf_spin.setValue(7.5)
    dlg._simulate()
    assert captured
    assert captured[0].cover_pf == 7.5


def test_three_round_burst_cover_pf(three_rb_pair, monkeypatch):
    captured: list[ShotParameters] = []

    def fake_3rb(shooter, target, weapon, ammo, range_hexes, exposure, shot_params, is_front):
        captured.append(shot_params)
        return [_dummy_shot_result(target)]

    monkeypatch.setattr(CombatSimulator, "three_round_burst", staticmethod(fake_3rb))
    monkeypatch.setattr(
        "phoenix_command.gui.dialogs.three_round_burst_dialog.QMessageBox.warning",
        MagicMock(),
    )
    dlg = ThreeRoundBurstDialog(three_rb_pair)
    ensure_ammo_combo(dlg)
    assert hasattr(dlg, "cover_pf_spin")
    dlg.cover_pf_spin.setValue(3.0)
    dlg._simulate()
    assert captured
    assert captured[0].cover_pf == 3.0


def test_burst_fire_cover_pf_after_target_page(burst_pair, monkeypatch):
    captured: list[ShotParameters] = []

    def fake_burst(shooter, weapon, ammo, target_group, arc_of_fire, continuous_burst):
        captured.extend(target_group.shot_params_list)
        return [_dummy_shot_result(target_group.targets[0])]

    monkeypatch.setattr(CombatSimulator, "burst_fire", staticmethod(fake_burst))
    monkeypatch.setattr(
        "phoenix_command.gui.dialogs.burst_fire_dialog.QMessageBox.warning",
        MagicMock(),
    )
    dlg = BurstFireDialog(burst_pair)
    ensure_ammo_combo(dlg)
    dlg._populate_targets_list()
    assert dlg.targets_list.count() >= 1
    dlg.targets_list.item(0).setSelected(True)
    dlg._build_params_pages()
    assert hasattr(dlg, "cover_pf_spin")
    dlg.cover_pf_spin.setValue(5.0)
    dlg._simulate()
    assert captured
    assert captured[0].cover_pf == 5.0


def test_shotgun_dialog_cover_pf(shotgun_pair, monkeypatch):
    captured: list[ShotParameters] = []

    def fake_shotgun(shooter, targets, weapon, ammo, ranges, exposures, shot_params_list, is_front_shots, primary_target_idx=0):
        captured.extend(shot_params_list)
        return [_dummy_shot_result(targets[0])]

    monkeypatch.setattr(
        "phoenix_command.gui.dialogs.shotgun_dialog.CombatSimulator.shotgun_shot",
        fake_shotgun,
    )
    monkeypatch.setattr(
        "phoenix_command.gui.dialogs.shotgun_dialog.QMessageBox.warning",
        MagicMock(),
    )
    dlg = ShotgunDialog(shotgun_pair)
    ensure_ammo_combo(dlg, pellet=True)
    assert dlg.ammo_combo.currentData() is not None
    dlg._build_params_pages()
    assert hasattr(dlg, "cover_pf_spin")
    dlg.cover_pf_spin.setValue(2.5)
    dlg._simulate()
    assert captured
    assert captured[0].cover_pf == 2.5


def test_shotgun_burst_cover_pf(auto_shotgun_pair, monkeypatch):
    captured: list[ShotParameters] = []

    def fake_sb(shooter, weapon, ammo, primary_group, pattern_groups, arc_of_fire, continuous_burst):
        captured.extend(primary_group.shot_params_list)
        return [_dummy_shot_result(primary_group.targets[0])]

    monkeypatch.setattr(CombatSimulator, "shotgun_burst_fire", staticmethod(fake_sb))
    monkeypatch.setattr(
        "phoenix_command.gui.dialogs.shotgun_burst_fire_dialog.QMessageBox.warning",
        MagicMock(),
    )
    dlg = ShotgunBurstFireDialog(auto_shotgun_pair)
    ensure_ammo_combo(dlg, pellet=True)
    dlg._populate_primary_targets_list()
    dlg.primary_targets_list.item(0).setSelected(True)
    dlg._build_primary_params_pages()
    assert hasattr(dlg, "cover_pf_spin")
    dlg.cover_pf_spin.setValue(1.5)
    dlg._simulate()
    assert captured
    assert captured[0].cover_pf == 1.5
