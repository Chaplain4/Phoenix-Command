"""HexMapView: category toolbar, map/token round-trip, editable and combat bar."""

from phoenix_command.gui.widgets.hex_map_modes import CATEGORY_MODES, EditMode, EditorCategory
from phoenix_command.gui.widgets.hex_map_view import HexMapView
from phoenix_command.session.domains.impulse_combat_state import ImpulseCombatState
from phoenix_command.session.domains.map_state import MapLayer, MapState, WallSegment
from phoenix_command.session.domains.token_state import TokenPlacement, TokenState


def test_category_toolbar_visibility(qapp):
    view = HexMapView()
    for cat in EditorCategory:
        view._set_category(cat)
        allowed = set(CATEGORY_MODES[cat])
        for mode, btn in view._mode_buttons.items():
            assert (not btn.isHidden()) is (mode in allowed)
        objects = cat == EditorCategory.OBJECTS
        assert (not view._edge_btn.isHidden()) is objects
        assert (not view._hex_btn.isHidden()) is objects


def test_map_and_token_state_round_trip(qapp):
    view = HexMapView()
    layer = MapLayer(id="g", name="Ground")
    layer.walls["1,0:1"] = WallSegment(material="wall_brick_6", thickness=6.0, height=2.0)
    ms = MapState(layers=[layer], active_layer_id="g")
    ts = TokenState(
        placements={
            "tok": TokenPlacement(
                token_id="tok",
                character_name="AK-74 Fighter",
                layer_id="g",
                q=2,
                r=1,
            )
        }
    )
    view.set_map_state(ms)
    view.set_token_state(ts)
    got_map = view.get_map_state()
    got_tok = view.get_token_state()
    assert "1,0:1" in got_map.get_active_layer().walls
    assert "tok" in got_tok.placements
    assert got_tok.placements["tok"].q == 2


def test_set_editable_false_hides_category(qapp):
    view = HexMapView()
    view.set_editable(False)
    assert not view._category_panel.isVisible()
    assert not view._toolbar.isEnabled()


def test_combat_mode_shows_combat_bar(qapp):
    view = HexMapView()
    state = ImpulseCombatState(map_mode="combat", phase=1, impulse=0)
    view.set_impulse_combat_state(state)
    assert not view._combat_bar.isHidden()
    assert view._toolbar.isHidden()
