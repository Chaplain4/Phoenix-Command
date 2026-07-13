"""Serialization tests for impulse combat domain."""

from phoenix_command.session.domains.impulse_combat_state import ImpulseCombatState, TokenCombatRuntime
from phoenix_command.session.domains.player_info import PlayerInfo
from phoenix_command.session.domains.session_meta import SessionMeta
from phoenix_command.session.domains.token_state import TokenPlacement
from phoenix_command.session.domains.map_state import HexCondition, MapLayer
from phoenix_command.session.game_state import GameState


def test_impulse_combat_round_trip() -> None:
    ic = ImpulseCombatState(
        map_mode="combat",
        phase=2,
        impulse=1,
        sides={"alpha": "Alpha"},
        token_runtime={"t1": TokenCombatRuntime(ac_remaining=1.5, braced=True)},
        selected_token_id="t1",
    )
    restored = ImpulseCombatState.from_dict(ic.to_dict())
    assert restored.map_mode == "combat"
    assert restored.phase == 2
    assert restored.token_runtime["t1"].ac_remaining == 1.5
    assert restored.token_runtime["t1"].braced is True


def test_token_side_and_control() -> None:
    tok = TokenPlacement(
        token_id="t1",
        side_id="alpha",
        controlled_by="guest-0",
    )
    data = tok.to_dict()
    restored = TokenPlacement.from_dict(data)
    assert restored.side_id == "alpha"
    assert restored.controlled_by == "guest-0"


def test_session_meta_players() -> None:
    meta = SessionMeta(
        host_name="Host",
        players=[
            PlayerInfo("host", "Host", is_host=True),
            PlayerInfo("guest-0", "Alice", is_host=False),
        ],
        connected_guests=["Alice"],
    )
    restored = SessionMeta.from_dict(meta.to_dict())
    assert len(restored.players) == 2
    assert restored.get_player("guest-0").display_name == "Alice"


def test_hex_condition_on_layer() -> None:
    layer = MapLayer()
    layer.conditions["1,2"] = HexCondition(visibility=["DUSK"], tags=["smoke"])
    data = layer.to_dict()
    restored = MapLayer.from_dict(data)
    assert restored.conditions["1,2"].visibility == ["DUSK"]


def test_game_state_includes_impulse_combat() -> None:
    state = GameState()
    state.impulse_combat.map_mode = "combat"
    restored = GameState.from_dict(state.to_dict())
    assert restored.impulse_combat.map_mode == "combat"
