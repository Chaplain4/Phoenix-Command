"""Tests for GameStateBridge capture/apply symmetry."""

from phoenix_command.models.character import Character
from phoenix_command.session.bridge import GameStateBridge
from phoenix_command.session.domains.map_state import MapState
from phoenix_command.session.domains.token_state import TokenPlacement, TokenState
from phoenix_command.session.game_state import GameState


class _FakeCombatZone:
    def __init__(self) -> None:
        self.shooter_zone = _FakeZone()
        self.target_zones = [_FakeZone()]

    def get_shooter(self):
        return self.shooter_zone.character

    def get_targets(self):
        return [z.character for z in self.target_zones if z.character]

    def clear_all(self):
        self.shooter_zone.character = None
        self.target_zones = [_FakeZone()]

    def add_target_zone(self):
        self.target_zones.append(_FakeZone())

    def refresh_cards(self):
        pass


class _FakeZone:
    def __init__(self) -> None:
        self.character = None

    def set_character(self, char):
        self.character = char


class _FakeList:
    def __init__(self) -> None:
        self._row = -1

    def currentRow(self):
        return self._row

    def setCurrentRow(self, row):
        self._row = row


class _FakeLog:
    def __init__(self) -> None:
        self._entries = []
        self._detailed = []

    def get_log_entries(self):
        return list(self._entries)

    def get_detailed_lines(self):
        return list(self._detailed)

    def set_log_entries(self, entries, detailed):
        self._entries = list(entries)
        self._detailed = list(detailed)


class _FakeHexMap:
    def __init__(self) -> None:
        self._map = MapState()
        self._map.ensure_default_layer()
        self._tokens = TokenState()
        self._impulse = None
        self._names = []
        self._session = None

    def get_map_state(self):
        return self._map

    def get_token_state(self):
        return self._tokens

    def get_impulse_combat_state(self):
        from phoenix_command.session.domains.impulse_combat_state import ImpulseCombatState

        return self._impulse or ImpulseCombatState()

    def set_map_state(self, state):
        self._map = state

    def set_token_state(self, state):
        self._tokens = state

    def set_impulse_combat_state(self, state, rebuild=True):
        self._impulse = state

    def set_character_names(self, names):
        self._names = list(names)

    def set_session_context(self, role=None, player_id="host", players=None):
        self._session = (role, player_id, players)

    def new_map(self):
        self._map = MapState()
        self._map.ensure_default_layer()


class _FakeWindow:
    def __init__(self) -> None:
        self.characters = [
            Character(
                name="Alice",
                strength=10,
                intelligence=10,
                will=10,
                health=10,
                agility=10,
                gun_combat_skill_level=3,
            )
        ]
        self.combat_zone = _FakeCombatZone()
        self.character_list = _FakeList()
        self.combat_log = _FakeLog()
        self.hex_map_view = _FakeHexMap()
        self._session_role = "guest"
        self._player_id = "guest-1"
        self._refreshed = False

    def _refresh_character_list(self):
        self._refreshed = True


def test_capture_and_apply_round_trip() -> None:
    window = _FakeWindow()
    window.hex_map_view._tokens.placements["t1"] = TokenPlacement(
        token_id="t1", q=1, r=2, character_name="Alice"
    )
    bridge = GameStateBridge()
    captured = bridge.capture_from_window(window)
    assert len(captured.combat.characters) == 1
    assert captured.tokens is not None
    assert "t1" in captured.tokens.placements

    other = _FakeWindow()
    other.characters = []
    bridge.apply_to_window(other)
    assert len(other.characters) == 1
    assert other.characters[0].name == "Alice"
    assert "t1" in other.hex_map_view._tokens.placements


def test_tokens_none_clears_guest_tokens() -> None:
    window = _FakeWindow()
    window.hex_map_view._tokens.placements["stale"] = TokenPlacement(
        token_id="stale", q=0, r=0
    )
    state = GameState()
    state.tokens = None
    bridge = GameStateBridge(state)
    bridge.apply_to_window(window)
    assert window.hex_map_view._tokens.placements == {}
