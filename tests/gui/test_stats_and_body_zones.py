"""Stats display and body-zone mapping."""

from phoenix_command.gui.widgets.body_zones import BODY_ZONES, LOCATION_TO_ZONE, _mirror_x
from phoenix_command.gui.widgets.stats_display import StatsDisplayWidget
from phoenix_command.models.enums import AdvancedHitLocation


def test_stats_display_set_and_clear(rifle_pair):
    char = rifle_pair[0]
    w = StatsDisplayWidget()
    w.set_character(char)
    assert w.name_label.text() == char.name
    assert w.str_label.text() == str(char.strength)
    assert w.skl_label.text() == str(char.gun_combat_skill_level)
    assert w.def_alm_label.text() == str(char.defensive_alm)
    w.set_character(None)
    assert w.name_label.text() == "Select a character"
    assert w.str_label.text() == "-"


def test_body_zones_polygons_and_mapping():
    assert BODY_ZONES
    for zone in BODY_ZONES:
        assert zone.front_polygon
        assert zone.rear_polygon
        for loc in zone.locations:
            assert loc in LOCATION_TO_ZONE
    mirrored = _mirror_x([(0.25, 0.1), (0.4, 0.2)])
    assert mirrored[0][0] == 0.75
    assert mirrored[1][0] == 0.6
    mapped = set(LOCATION_TO_ZONE)
    assert mapped
    # Locations used by the diagram must be real enum members.
    for loc in mapped:
        assert isinstance(loc, AdvancedHitLocation)
