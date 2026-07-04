"""Tests for map and character file persistence."""

import base64
import json

import pytest

from phoenix_command.models.character import Character
from phoenix_command.session.domains.map_state import BackgroundImage, MapLayer, MapState, TerrainTile
from phoenix_command.session.domains.token_state import TokenPlacement, TokenState
from phoenix_command.session.persistence import (
    CHARACTER_FILE_KIND,
    MAP_FILE_KIND,
    default_character_filename,
    load_character_file,
    load_map_file,
    save_character_file,
    save_map_file,
)


def test_map_file_includes_backgrounds(tmp_path):
    layer = MapLayer(name="Floor")
    layer.background = BackgroundImage(
        data_b64=base64.b64encode(b"pngdata").decode("ascii"),
        fit_mode="stretch_grid",
        scale_x=2.0,
        scale_y=1.5,
    )
    layer.terrain["0,0"] = TerrainTile()
    map_state = MapState(layers=[layer], active_layer_id=layer.id)
    tokens = TokenState(
        placements={
            "t1": TokenPlacement(token_id="t1", q=1, r=2, layer_id=layer.id),
        }
    )
    path = tmp_path / "test_map.json"
    save_map_file(path, map_state, tokens)

    raw = json.loads(path.read_text(encoding="utf-8"))
    assert raw["file_kind"] == MAP_FILE_KIND
    assert raw["map"]["layers"][0]["background"]["data_b64"]

    loaded_map, loaded_tokens = load_map_file(path)
    bg = loaded_map.layers[0].background
    assert bg is not None
    assert bg.fit_mode == "stretch_grid"
    assert bg.scale_x == 2.0
    assert "t1" in loaded_tokens.placements


def test_map_file_rejects_wrong_kind(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text(json.dumps({"file_kind": "other"}), encoding="utf-8")
    with pytest.raises(ValueError, match="Not a map file"):
        load_map_file(path)


def test_character_file_round_trip(tmp_path):
    char = Character(
        name="Alpha",
        strength=10,
        intelligence=10,
        will=10,
        health=10,
        agility=10,
        gun_combat_skill_level=5,
    )
    path = tmp_path / "alpha.json"
    save_character_file(path, char)

    raw = json.loads(path.read_text(encoding="utf-8"))
    assert raw["file_kind"] == CHARACTER_FILE_KIND
    assert raw["character"]["name"] == "Alpha"

    restored = load_character_file(path)
    assert restored.name == "Alpha"
    assert restored.gun_combat_skill_level == 5


def test_default_character_filename():
    assert default_character_filename(Character(
        name="John Doe",
        strength=1, intelligence=1, will=1, health=1, agility=1,
        gun_combat_skill_level=1,
    )).endswith(".json")
