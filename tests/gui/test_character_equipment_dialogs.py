"""CharacterDialog and EquipmentDialog contracts."""

from copy import deepcopy

from phoenix_command.gui.dialogs.character_dialog import CharacterDialog
from phoenix_command.gui.dialogs.equipment_dialog import EquipmentDialog
from phoenix_command.item_database.character_templates import ak74_fighter
from phoenix_command.models.character import Character
from phoenix_command.models.gear import Weapon


def test_character_dialog_new_manual(qapp):
    dlg = CharacterDialog()
    dlg.name_input.setText("Test Rec")
    dlg.str_spin.setValue(12)
    dlg.skl_spin.setValue(5)
    char = dlg.get_character()
    assert char.name == "Test Rec"
    assert char.strength == 12
    assert char.gun_combat_skill_level == 5


def test_character_dialog_edit_loads_and_pd(qapp):
    src = deepcopy(ak74_fighter)
    src.physical_damage_total = 3
    dlg = CharacterDialog(src)
    assert dlg.name_input.text() == src.name
    assert dlg.str_spin.value() == src.strength
    dlg.pd_spin.setValue(11)
    out = dlg.get_character()
    assert out is src
    assert out.physical_damage_total == 11


def test_character_dialog_template_is_deepcopy(qapp):
    dlg = CharacterDialog()
    dlg.tabs.setCurrentIndex(2)
    template = dlg.template_combo.currentData()
    result = dlg.get_character()
    assert result is not None
    assert result is not template
    assert result.name == template.name


def test_equipment_search_add_and_ammo_filter(qapp):
    char = Character(
        name="Empty",
        strength=10,
        intelligence=10,
        will=10,
        health=10,
        agility=10,
        gun_combat_skill_level=3,
    )
    dlg = EquipmentDialog(char)
    assert dlg.weapons_list.count() > 0
    dlg.search_input.setText("zzzz-not-a-weapon")
    hidden = sum(
        1 for i in range(dlg.weapons_list.count()) if dlg.weapons_list.item(i).isHidden()
    )
    assert hidden == dlg.weapons_list.count()
    dlg.search_input.setText("")
    dlg.tabs.setCurrentIndex(0)
    dlg.weapons_list.setCurrentRow(0)
    before = len(char.equipment)
    dlg._add_item()
    assert len(char.equipment) == before + 1

    dlg.tabs.setCurrentIndex(EquipmentDialog.AMMO_TAB_INDEX)
    dlg.ammo_weapon_filter.setChecked(True)
    weapon = next((i for i in char.equipment if isinstance(i, Weapon)), None)
    assert weapon is not None
    compatible = {a.name for a in weapon.ammunition_types}
    visible_ammo = [
        dlg.ammo_list.item(i).text()
        for i in range(dlg.ammo_list.count())
        if not dlg.ammo_list.item(i).isHidden()
    ]
    assert visible_ammo
    assert all(name in compatible for name in visible_ammo)
