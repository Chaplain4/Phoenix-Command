"""Combat zone placement without DnD."""

from phoenix_command.gui.widgets.combat_zone import CombatZoneWidget


def test_shooter_targets_remove_and_clear(rifle_pair):
    a, b = rifle_pair
    zone = CombatZoneWidget()
    zone.shooter_zone.set_character(a)
    zone.target_zones[0].set_character(b)
    assert zone.get_shooter() is a
    assert [t.name for t in zone.get_targets()] == [b.name]
    zone.remove_character(b.name)
    assert zone.get_targets() == []
    zone.target_zones[0].set_character(b)
    zone.clear_all()
    assert zone.get_shooter() is None
    assert len(zone.target_zones) == 1
    assert zone.target_zones[0].character is None
