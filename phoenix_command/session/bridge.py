"""Bridge between MainWindow UI and GameState."""

from __future__ import annotations

from typing import TYPE_CHECKING

from phoenix_command.session.domains.combat_state import CombatLogEntry, CombatState, CombatZoneState
from phoenix_command.session.domains.impulse_combat_state import ImpulseCombatState
from phoenix_command.session.domains.map_state import MapState
from phoenix_command.session.domains.token_state import TokenState
from phoenix_command.session.game_state import GameState
from phoenix_command.session.serialization import character_from_dict, character_to_dict

if TYPE_CHECKING:
    from phoenix_command.gui.main_window import MainWindow


class GameStateBridge:
    """Capture UI state into GameState and apply GameState back to UI."""

    def __init__(self, state: GameState | None = None) -> None:
        self.state = state or GameState()

    def capture_from_window(self, window: "MainWindow") -> GameState:
        combat = CombatState()
        combat.characters = [
            character_to_dict(c) for c in window.characters
        ]
        shooter = window.combat_zone.get_shooter()
        combat.combat_zone = CombatZoneState(
            shooter_name=shooter.name if shooter else None,
            target_names=[
                t.name for t in window.combat_zone.get_targets()
            ],
        )
        row = window.character_list.currentRow()
        if 0 <= row < len(window.characters):
            combat.selected_character_name = window.characters[row].name
        combat.combat_log = list(window.combat_log.get_log_entries())
        combat.detailed_log = list(window.combat_log.get_detailed_lines())
        self.state.combat = combat

        if hasattr(window, "hex_map_view"):
            self.state.map = window.hex_map_view.get_map_state()
            self.state.tokens = window.hex_map_view.get_token_state()
            self.state.impulse_combat = window.hex_map_view.get_impulse_combat_state()

        return self.state

    def apply_to_window(self, window: "MainWindow") -> None:
        combat = self.state.combat
        window.characters = [
            character_from_dict(c) for c in combat.characters
        ]
        window._refresh_character_list()
        window.combat_zone.clear_all()
        if combat.combat_zone.shooter_name:
            for char in window.characters:
                if char.name == combat.combat_zone.shooter_name:
                    window.combat_zone.shooter_zone.set_character(char)
                    break
        for target_name in combat.combat_zone.target_names:
            for char in window.characters:
                if char.name == target_name:
                    if window.combat_zone.target_zones and not window.combat_zone.target_zones[-1].character:
                        zone = window.combat_zone.target_zones[-1]
                    else:
                        window.combat_zone.add_target_zone()
                        zone = window.combat_zone.target_zones[-1]
                    zone.set_character(char)
                    break
        if combat.selected_character_name:
            for i, char in enumerate(window.characters):
                if char.name == combat.selected_character_name:
                    window.character_list.setCurrentRow(i)
                    break
        window.combat_log.set_log_entries(combat.combat_log, combat.detailed_log)
        window.combat_zone.refresh_cards()

        if hasattr(window, "hex_map_view"):
            window.hex_map_view.set_character_names([c.name for c in window.characters])
            if self.state.map is not None:
                window.hex_map_view.set_map_state(self.state.map)
            else:
                window.hex_map_view.new_map()
            if self.state.tokens is not None:
                window.hex_map_view.set_token_state(self.state.tokens)
            window.hex_map_view.set_impulse_combat_state(self.state.impulse_combat)
            window.hex_map_view.set_session_context(
                role=getattr(window, "_session_role", None),
                player_id=getattr(window, "_player_id", "host"),
                players=self.state.meta.players,
            )

    def apply_remote_state(self, state: GameState, window: "MainWindow") -> None:
        self.state = state
        self.apply_to_window(window)
