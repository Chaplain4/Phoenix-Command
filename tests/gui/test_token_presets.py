"""Tests for built-in token image presets."""

from phoenix_command.gui.utils.token_presets import (
    TOKEN_FACTIONS,
    list_token_presets,
    list_token_presets_by_faction,
    load_preset_b64,
    load_preset_bytes,
)


def test_list_token_presets():
    presets = list_token_presets()
    assert len(presets) == 30  # 5 factions × 6 weapons
    ids = [p[0] for p in presets]
    assert "assault" in ids
    assert "shotgun" in ids
    assert "militant_assault" in ids
    assert "swat_shotgun" in ids
    assert "criminal_rpg" in ids
    assert "rf_lmg" in ids


def test_presets_grouped_by_faction():
    rows = list_token_presets_by_faction()
    assert len(rows) == len(TOKEN_FACTIONS)
    assert rows[0][0] == "nato"
    nato_ids = [pid for pid, _ in rows[0][2]]
    assert nato_ids == ["assault", "rifle", "smg", "lmg", "shotgun", "rpg"]


def test_load_each_preset_b64():
    for preset_id, _label in list_token_presets():
        raw = load_preset_bytes(preset_id)
        assert raw is not None and len(raw) > 100, preset_id
        b64, mime = load_preset_b64(preset_id)
        assert mime == "image/png"
        assert len(b64) > 50
