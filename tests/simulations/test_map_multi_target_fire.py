"""Tests for map multi-target fire helpers and dispatch."""

from unittest.mock import MagicMock, patch

from phoenix_command.models.character import Character
from phoenix_command.models.enums import (
    Caliber,
    Country,
    WeaponType,
)
from phoenix_command.models.gear import AmmoType, Weapon
from phoenix_command.models.hit_result_advanced import ShotResult
from phoenix_command.session.domains.impulse_combat_state import PendingShotPreview
from phoenix_command.session.domains.map_state import MapState
from phoenix_command.session.domains.token_state import TokenPlacement, TokenState
from phoenix_command.simulations.map_fire_dispatch import (
    build_snapshot,
    dispatch_map_fire,
    enrich_preview_targets,
    preview_from_snapshot,
)
from phoenix_command.simulations.map_fire_targets import (
    infer_fire_kind,
    tokens_in_arc,
    tokens_in_blast,
    tokens_in_pattern,
)


def _char(name: str) -> Character:
    return Character(
        name=name,
        strength=12,
        intelligence=10,
        will=11,
        health=12,
        agility=10,
        gun_combat_skill_level=5,
    )


def _weapon(name: str = "AR") -> Weapon:
    return Weapon(
        name=name,
        weight=8.0,
        caliber=Caliber.CAL_556_NATO,
        weapon_type=WeaponType.ASSAULT_RIFLE,
        country=Country.USA,
        length_deployed=30.0,
        aim_time_modifiers={2: 10},
        full_auto=True,
        full_auto_rof=5,
        sustained_auto_burst=1,
    )


def _ammo(name: str = "Ball") -> AmmoType:
    return AmmoType(name=name, weight=0.5)


def _tokens_line() -> tuple[TokenState, TokenPlacement]:
    """Shooter at (0,0) facing east; enemies at (2,0) and (3,0); friend at (1,1)."""
    tokens = TokenState()
    shooter = TokenPlacement(
        token_id="s", character_name="Shooter", q=0, r=0, facing=0, side_id="alpha"
    )
    e1 = TokenPlacement(
        token_id="e1", character_name="Enemy1", q=2, r=0, facing=6, side_id="bravo"
    )
    e2 = TokenPlacement(
        token_id="e2", character_name="Enemy2", q=3, r=0, facing=6, side_id="bravo"
    )
    friend = TokenPlacement(
        token_id="f1", character_name="Friend", q=1, r=1, facing=0, side_id="alpha"
    )
    behind = TokenPlacement(
        token_id="b1", character_name="Behind", q=-2, r=0, facing=0, side_id="bravo"
    )
    for t in (shooter, e1, e2, friend, behind):
        tokens.placements[t.token_id] = t
    return tokens, shooter


def test_tokens_in_arc_includes_forward_enemies() -> None:
    tokens, shooter = _tokens_line()
    map_state = MapState()
    map_state.ensure_default_layer()
    infos = tokens_in_arc(shooter, tokens, map_state, {}, half_angle_deg=45)
    ids = {i.token_id for i in infos}
    assert "e1" in ids
    assert "e2" in ids
    assert "f1" not in ids  # same side
    assert "b1" not in ids  # behind facing


def test_tokens_in_pattern_radius() -> None:
    tokens, shooter = _tokens_line()
    map_state = MapState()
    map_state.ensure_default_layer()
    # Center on e1; e2 is 1 hex away at 1m/hex → within 2m
    ids = tokens_in_pattern(2, 0, 2.0, tokens, map_state, shooter=shooter, exclude_ids={"e1"})
    assert "e2" in ids
    assert "e1" not in ids
    assert "s" not in ids


def test_tokens_in_blast() -> None:
    tokens, shooter = _tokens_line()
    map_state = MapState()
    map_state.ensure_default_layer()
    hits = tokens_in_blast(2, 0, 3.0, tokens, map_state, shooter=shooter)
    ids = [tid for tid, _ in hits]
    assert "e1" in ids
    assert "e2" in ids


def test_pending_shot_preview_multi_round_trip() -> None:
    preview = PendingShotPreview(
        preview_id="p1",
        shooter_token_id="s",
        target_token_id="e1",
        proposed_by="host",
        fire_mode="auto",
        fire_kind="burst",
        target_token_ids=["e1", "e2"],
        secondary_by_primary={"e1": ["e2"]},
        aim_q=4,
        aim_r=1,
        aim_layer_id="L1",
        arc_of_fire=2.5,
        continuous_burst_impulses=1,
        per_target={"e1": {"range_hexes": 3, "exposure": "STANDING_EXPOSED"}},
    )
    restored = PendingShotPreview.from_dict(preview.to_dict())
    assert restored.target_token_ids == ["e1", "e2"]
    assert restored.secondary_by_primary["e1"] == ["e2"]
    assert restored.aim_q == 4 and restored.aim_r == 1
    assert restored.arc_of_fire == 2.5
    assert restored.fire_kind == "burst"
    assert restored.primary_ids() == ["e1", "e2"]


def test_legacy_preview_fills_target_token_ids() -> None:
    data = {
        "preview_id": "x",
        "shooter_token_id": "s",
        "target_token_id": "t1",
        "proposed_by": "host",
    }
    p = PendingShotPreview.from_dict(data)
    assert p.primary_ids() == ["t1"]


def test_infer_fire_kind_auto_burst() -> None:
    w = _weapon("Rifle")
    a = _ammo()
    assert infer_fire_kind("auto", w, a) == "burst"
    assert infer_fire_kind("3rb", w, a) == "3rb"
    assert infer_fire_kind("single", w, a) == "single"


def test_build_snapshot_and_preview_roundtrip() -> None:
    preview = PendingShotPreview(
        preview_id="p",
        shooter_token_id="s",
        target_token_id="e1",
        proposed_by="host",
        fire_kind="burst",
        fire_mode="auto",
        target_token_ids=["e1", "e2"],
        per_target={"e1": {"range_hexes": 2}},
    )
    snap = build_snapshot(preview, "Shooter", {"e1": "Enemy1", "e2": "Enemy2"})
    assert snap["kind"] == "burst"
    assert snap["target_token_ids"] == ["e1", "e2"]
    restored = preview_from_snapshot(snap, "s", "e1")
    assert restored.fire_kind == "burst"
    assert restored.target_token_ids == ["e1", "e2"]


def test_dispatch_burst_builds_target_group() -> None:
    tokens, shooter_tok = _tokens_line()
    chars = {
        "Shooter": _char("Shooter"),
        "Enemy1": _char("Enemy1"),
        "Enemy2": _char("Enemy2"),
    }
    weapon = _weapon()
    ammo = _ammo()
    preview = PendingShotPreview(
        preview_id="p",
        shooter_token_id="s",
        target_token_id="e1",
        proposed_by="host",
        fire_mode="auto",
        fire_kind="burst",
        target_token_ids=["e1", "e2"],
        stance_mods=["STANDING"],
        visibility_mods=["GOOD_VISIBILITY"],
        per_target={
            "e1": {"range_hexes": 2, "exposure": "STANDING_EXPOSED", "orientation": "FRONT_REAR", "is_front": True},
            "e2": {"range_hexes": 3, "exposure": "STANDING_EXPOSED", "orientation": "FRONT_REAR", "is_front": True},
        },
    )

    captured = {}

    def fake_burst(shooter, weapon, ammo, target_group, arc_of_fire=None, continuous_burst_impulses=0):
        captured["group"] = target_group
        captured["arc"] = arc_of_fire
        return [
            ShotResult(hit=False, eal=0, odds=0, roll=99, target=target_group.targets[0], log="burst")
        ]

    with patch(
        "phoenix_command.simulations.map_fire_dispatch.CombatSimulator.burst_fire",
        side_effect=fake_burst,
    ):
        with patch(
            "phoenix_command.simulations.map_fire_dispatch.filter_ids_by_los",
            side_effect=lambda *a, **k: (["e1", "e2"], []),
        ):
            outcome = dispatch_map_fire(
                preview,
                chars["Shooter"],
                weapon,
                ammo,
                tokens,
                chars,
                MapState(),
                {},
            )
    assert outcome.kind == "burst"
    assert "group" in captured
    assert len(captured["group"].targets) == 2
    assert captured["group"].ranges == [2, 3]


def test_tof_multi_los_miss_one_target() -> None:
    tokens, _ = _tokens_line()
    chars = {
        "Shooter": _char("Shooter"),
        "Enemy1": _char("Enemy1"),
        "Enemy2": _char("Enemy2"),
    }
    weapon = _weapon()
    ammo = _ammo()
    preview = PendingShotPreview(
        preview_id="p",
        shooter_token_id="s",
        target_token_id="e1",
        proposed_by="host",
        fire_mode="auto",
        fire_kind="burst",
        target_token_ids=["e1", "e2"],
        stance_mods=["STANDING"],
        visibility_mods=["GOOD_VISIBILITY"],
        per_target={
            "e1": {"range_hexes": 2, "exposure": "STANDING_EXPOSED", "orientation": "FRONT_REAR", "is_front": True},
            "e2": {"range_hexes": 3, "exposure": "STANDING_EXPOSED", "orientation": "FRONT_REAR", "is_front": True},
        },
    )

    def fake_burst(shooter, weapon, ammo, target_group, arc_of_fire=None, continuous_burst_impulses=0):
        return [
            ShotResult(hit=False, eal=0, odds=0, roll=99, target=t, log="ok")
            for t in target_group.targets
        ]

    with patch(
        "phoenix_command.simulations.map_fire_dispatch.CombatSimulator.burst_fire",
        side_effect=fake_burst,
    ):
        with patch(
            "phoenix_command.simulations.map_fire_dispatch.filter_ids_by_los",
            side_effect=lambda *a, **k: (["e1"], ["e2"]),
        ):
            outcome = dispatch_map_fire(
                preview,
                chars["Shooter"],
                weapon,
                ammo,
                tokens,
                chars,
                MapState(),
                {},
            )
    assert any("e2" in r or "Enemy2" in r for r in outcome.miss_reasons)
    assert len(outcome.shot_results) == 1


def test_enrich_preview_sets_burst_targets() -> None:
    tokens, shooter = _tokens_line()
    map_state = MapState()
    map_state.ensure_default_layer()
    for tok in tokens.placements.values():
        tok.layer_id = map_state.layers[0].id
    preview = PendingShotPreview(
        preview_id="p",
        shooter_token_id="s",
        target_token_id="e1",
        proposed_by="host",
        fire_mode="auto",
    )
    weapon = _weapon()
    ammo = _ammo()
    enriched = enrich_preview_targets(
        preview, shooter, tokens, map_state, {}, weapon, ammo
    )
    assert enriched.fire_kind == "burst"
    assert "e1" in enriched.target_token_ids or "e2" in enriched.target_token_ids
