"""Save and load GameState to local JSON files."""

from __future__ import annotations

from pathlib import Path

from phoenix_command.session.game_state import GameState
from phoenix_command.session.serialization import game_state_from_json, game_state_to_json


def save_game_state(path: str | Path, state: GameState) -> None:
    Path(path).write_text(game_state_to_json(state), encoding="utf-8")


def load_game_state(path: str | Path) -> GameState:
    return game_state_from_json(Path(path).read_text(encoding="utf-8"))
