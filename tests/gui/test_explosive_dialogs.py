"""Explosive / grenade / AGL / explosion dialogs: construct and simulate via stubs."""

from unittest.mock import MagicMock

from phoenix_command.gui.dialogs.auto_grenade_launcher_dialog import AutoGrenadeLauncherDialog
from phoenix_command.gui.dialogs.explosion_damage_dialog import ExplosionDamageDialog
from phoenix_command.gui.dialogs.explosive_weapon_dialog import ExplosiveWeaponDialog
from phoenix_command.gui.dialogs.thrown_grenade_dialog import ThrownGrenadeDialog
from phoenix_command.models.character import Character
from phoenix_command.models.enums import SituationStanceModifier4B
from phoenix_command.models.hit_result_advanced import ExplosiveShotResult, ShotParameters
from phoenix_command.simulations.combat_simulator import CombatSimulator
from tests.gui.conftest import ensure_ammo_combo


def _explosive_result():
    return ExplosiveShotResult(hit=True, eal=10, odds=50, roll=20, scatter_hexes=0)


def test_thrown_grenade_construct_and_simulate(grenade_pair, monkeypatch):
    called = []

    def fake_throw(*args, **kwargs):
        called.append(args)
        return _explosive_result()

    monkeypatch.setattr(CombatSimulator, "thrown_grenade", staticmethod(fake_throw))
    dlg = ThrownGrenadeDialog(grenade_pair)
    assert dlg.grenade_combo.count() >= 1
    dlg._simulate()
    assert called


def test_thrown_grenade_empty_combo_does_not_crash(qapp, monkeypatch):
    warn = MagicMock()
    monkeypatch.setattr(
        "phoenix_command.gui.dialogs.thrown_grenade_dialog.QMessageBox.warning",
        warn,
    )
    empty = Character(
        name="Unarmed",
        strength=10,
        intelligence=10,
        will=10,
        health=10,
        agility=10,
        gun_combat_skill_level=1,
    )
    dlg = ThrownGrenadeDialog([empty])
    assert dlg.grenade_combo.count() == 0
    dlg._simulate()
    warn.assert_called()


def test_explosive_weapon_shot_params_and_simulate(rpg_pair, monkeypatch):
    captured: list[ShotParameters] = []

    def fake_shot(shooter, weapon, range_hexes, explosive_target, shot_params):
        captured.append(shot_params)
        return _explosive_result()

    monkeypatch.setattr(CombatSimulator, "explosive_weapon_shot", staticmethod(fake_shot))
    monkeypatch.setattr(
        "phoenix_command.gui.dialogs.explosive_weapon_dialog.QMessageBox.warning",
        MagicMock(),
    )
    dlg = ExplosiveWeaponDialog(rpg_pair)
    ensure_ammo_combo(dlg, explosive=True)
    dlg.stance_list.item(0).setSelected(True)
    params = dlg._build_shot_params()
    assert SituationStanceModifier4B.STANDING in params.situation_stance_modifiers or params.situation_stance_modifiers
    dlg._simulate()
    assert captured


def test_agl_construct_and_simulate(agl_pair, monkeypatch):
    captured: list[ShotParameters] = []

    def fake_agl(shooter, weapon, range_hexes, explosive_target, shot_params, arc_of_fire=None, continuous_burst_impulses=0):
        captured.append(shot_params)
        return [_explosive_result()]

    monkeypatch.setattr(
        CombatSimulator, "automatic_grenade_launcher_burst", staticmethod(fake_agl)
    )
    monkeypatch.setattr(
        "phoenix_command.gui.dialogs.auto_grenade_launcher_dialog.QMessageBox.warning",
        MagicMock(),
    )
    dlg = AutoGrenadeLauncherDialog(agl_pair)
    ensure_ammo_combo(dlg, explosive=True)
    dlg._simulate()
    assert captured


def test_explosion_damage_construct_and_simulate(grenade_pair, monkeypatch):
    called = []

    def fake_dmg(*args, **kwargs):
        called.append(True)
        return []

    monkeypatch.setattr(CombatSimulator, "explosion_damage", staticmethod(fake_dmg))
    monkeypatch.setattr(
        "phoenix_command.gui.dialogs.explosion_damage_dialog.QMessageBox.warning",
        MagicMock(),
    )
    dlg = ExplosionDamageDialog(grenade_pair)
    assert dlg.ammo_combo.count() >= 1
    dlg._populate_targets_list()
    dlg.targets_list.item(0).setSelected(True)
    dlg._on_targets_changed()
    assert dlg.blast_targets
    dlg._simulate()
    assert called
