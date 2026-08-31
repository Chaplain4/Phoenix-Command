"""Offscreen Qt app for widget tests. Must set the platform before Qt imports."""

from __future__ import annotations

import os
from copy import deepcopy

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest
from PyQt6.QtWidgets import QApplication

from phoenix_command.item_database.character_templates import (
    ak74_fighter,
    auto_grenade_fighter,
    auto_shotgun_fighter,
    dragunov_fighter,
    m16a2_fighter,
    rpg_fighter,
    rpk_74_fighter,
    shotgun_fighter,
)
from phoenix_command.models.character import Character
from phoenix_command.models.gear import AmmoType, Weapon


@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


def _clone(template: Character) -> Character:
    return deepcopy(template)


@pytest.fixture
def rifle_pair(qapp) -> list[Character]:
    return [_clone(ak74_fighter), _clone(dragunov_fighter)]


@pytest.fixture
def burst_pair(qapp) -> list[Character]:
    return [_clone(rpk_74_fighter), _clone(ak74_fighter)]


@pytest.fixture
def shotgun_pair(qapp) -> list[Character]:
    return [_clone(shotgun_fighter), _clone(ak74_fighter)]


@pytest.fixture
def auto_shotgun_pair(qapp) -> list[Character]:
    return [_clone(auto_shotgun_fighter), _clone(ak74_fighter)]


@pytest.fixture
def three_rb_pair(qapp) -> list[Character]:
    return [_clone(m16a2_fighter), _clone(ak74_fighter)]


@pytest.fixture
def rpg_pair(qapp) -> list[Character]:
    return [_clone(rpg_fighter), _clone(ak74_fighter)]


@pytest.fixture
def grenade_pair(qapp) -> list[Character]:
    return [_clone(ak74_fighter), _clone(dragunov_fighter)]


@pytest.fixture
def agl_pair(qapp) -> list[Character]:
    return [_clone(auto_grenade_fighter), _clone(ak74_fighter)]


def ensure_ammo_combo(dialog, pellet: bool = False, explosive: bool = False) -> None:
    """Fill ammo combo when identity checks against deep-copied equipment fail."""
    current = dialog.ammo_combo.currentData()
    if current is not None:
        if pellet and not getattr(current, "pellet_count", None):
            current = None
        elif explosive and not getattr(current, "explosive_data", None):
            current = None
        else:
            return
    dialog.ammo_combo.clear()
    shooter = dialog.shooter_combo.currentData()
    weapon = dialog.weapon_combo.currentData()
    if not shooter or not weapon:
        return
    names = {a.name for a in getattr(weapon, "ammunition_types", []) or []}
    all_ammo = [item for item in shooter.equipment if isinstance(item, AmmoType)]
    candidates = [a for a in all_ammo if a.name in names] if names else list(all_ammo)
    if not candidates:
        candidates = all_ammo
    if pellet:
        pellet_ones = [a for a in candidates if getattr(a, "pellet_count", None)]
        if pellet_ones:
            candidates = pellet_ones
    if explosive:
        exp_ones = [a for a in candidates if getattr(a, "explosive_data", None)]
        if exp_ones:
            candidates = exp_ones
    if candidates:
        dialog.ammo_combo.addItem(candidates[0].name, candidates[0])


def select_shooter_named(dialog, name: str) -> None:
    idx = dialog.shooter_combo.findText(name)
    if idx >= 0:
        dialog.shooter_combo.setCurrentIndex(idx)


def first_weapon(character: Character) -> Weapon | None:
    for item in character.equipment:
        if isinstance(item, Weapon):
            return item
    return None
