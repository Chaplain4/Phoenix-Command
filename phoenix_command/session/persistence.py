"""Save and load GameState, maps, and characters to local JSON files."""

from __future__ import annotations

import json
import re
from pathlib import Path

from phoenix_command.models.character import Character
from phoenix_command.session.domains.map_state import MapState
from phoenix_command.session.domains.token_state import TokenState
from phoenix_command.session.game_state import GameState
from phoenix_command.session.serialization import (
    character_from_dict,
    character_to_dict,
    game_state_from_json,
    game_state_to_json,
)

MAP_FILE_KIND = "phoenix_command_map"
CHARACTER_FILE_KIND = "phoenix_command_character"
MAP_SCHEMA_VERSION = 2
CHARACTER_SCHEMA_VERSION = 1


def linked_character_names(token_state: TokenState | None) -> set[str]:
    """Character names referenced by token placements on the map."""
    if token_state is None:
        return set()
    return {
        name
        for placement in token_state.placements.values()
        if (name := placement.character_name)
    }


def save_game_state(path: str | Path, state: GameState) -> None:
    Path(path).write_text(game_state_to_json(state), encoding="utf-8")


def load_game_state(path: str | Path) -> GameState:
    return game_state_from_json(Path(path).read_text(encoding="utf-8"))


def save_map_file(
    path: str | Path,
    map_state: MapState,
    token_state: TokenState | None = None,
    characters: dict[str, Character] | None = None,
) -> None:
    """Save hex map with layer backgrounds, token placements, and linked characters."""
    tokens = token_state or TokenState()
    linked = linked_character_names(tokens)
    char_payload: dict[str, dict] = {}
    if characters and linked:
        for name in sorted(linked):
            char = characters.get(name)
            if char is not None:
                char_payload[name] = character_to_dict(char)
    payload = {
        "file_kind": MAP_FILE_KIND,
        "schema_version": MAP_SCHEMA_VERSION,
        "map": map_state.to_dict(),
        "tokens": tokens.to_dict(),
        "characters": char_payload,
    }
    Path(path).write_text(json.dumps(payload, indent=2), encoding="utf-8")


def load_map_file(
    path: str | Path,
) -> tuple[MapState, TokenState, dict[str, Character]]:
    """Load hex map file; backgrounds are embedded as base64 in layer data."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("file_kind") not in (MAP_FILE_KIND, None):
        raise ValueError(f"Not a map file (file_kind={data.get('file_kind')!r})")
    if data.get("schema_version", 1) > MAP_SCHEMA_VERSION:
        raise ValueError(
            f"Unsupported map schema version {data.get('schema_version')}"
        )
    map_state = MapState.from_dict(data.get("map", {}))
    tokens = TokenState.from_dict(data.get("tokens", {}))
    characters = {
        name: character_from_dict(char_data)
        for name, char_data in data.get("characters", {}).items()
    }
    return map_state, tokens, characters


def save_character_file(path: str | Path, character: Character) -> None:
    """Save a single character with equipment and hit history."""
    payload = {
        "file_kind": CHARACTER_FILE_KIND,
        "schema_version": CHARACTER_SCHEMA_VERSION,
        "character": character_to_dict(character),
    }
    Path(path).write_text(json.dumps(payload, indent=2), encoding="utf-8")


def load_character_file(path: str | Path) -> Character:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("file_kind") not in (CHARACTER_FILE_KIND, None):
        raise ValueError(f"Not a character file (file_kind={data.get('file_kind')!r})")
    if data.get("schema_version", 1) > CHARACTER_SCHEMA_VERSION:
        raise ValueError(
            f"Unsupported character schema version {data.get('schema_version')}"
        )
    char_data = data.get("character")
    if not char_data:
        raise ValueError("Character file missing 'character' data")
    return character_from_dict(char_data)


def default_character_filename(character: Character) -> str:
    safe = re.sub(r"[^\w\-]+", "_", character.name.strip()) or "character"
    return f"{safe}.json"
