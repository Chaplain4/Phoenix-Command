"""Tests for built-in token image presets."""

from phoenix_command.gui.utils.token_presets import (
    list_token_presets,
    load_preset_b64,
    load_preset_bytes,
)


def test_list_token_presets():
    presets = list_token_presets()
    assert len(presets) == 5
    ids = [p[0] for p in presets]
    assert ids == ["assault", "rifle", "smg", "lmg", "rpg"]


def test_load_each_preset_b64():
    for preset_id, _label in list_token_presets():
        raw = load_preset_bytes(preset_id)
        assert raw is not None and len(raw) > 100
        b64, mime = load_preset_b64(preset_id)
        assert mime == "image/png"
        assert len(b64) > 50
