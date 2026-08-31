"""Regression tests for manual-test-map-combat remediation."""

from phoenix_command.models.character import Character
from phoenix_command.models.gear import Grenade
from phoenix_command.models.enums import Country, GrenadeType
from phoenix_command.session.domains.impulse_combat_state import (
    ImpulseCombatState,
    PendingShotPreview,
    TokenCombatRuntime,
)
from phoenix_command.session.domains.token_state import TokenPlacement, TokenState
from phoenix_command.session.domains.map_state import MapState, WallSegment, hex_wall_key
from phoenix_command.simulations.impulse_combat_engine import ImpulseCombatEngine
from phoenix_command.simulations.map_fire_dispatch import enrich_preview_targets, filter_ids_by_los
from phoenix_command.simulations.map_fire_targets import (
    default_ammo_for_weapon,
    infer_fire_kind,
    is_pellet_ammo,
)
from phoenix_command.simulations.map_los import check_los
from phoenix_command.item_database.weapons import spas12


def test_enrich_preview_targets_grenade_no_name_error() -> None:
    grenade = Grenade(
        name="Test Grenade",
        country=Country.USSR,
        grenade_type=GrenadeType.FRAG,
        weight=1.0,
        length=4.0,
        arm_time=2,
        fuse_length=1,
        range=10,
    )
    preview = PendingShotPreview(
        preview_id="p1",
        shooter_token_id="s",
        target_token_id="t",
        proposed_by="host",
    )
    ms = MapState()
    layer = ms.ensure_default_layer()
    shooter = TokenPlacement(token_id="s", q=0, r=0, layer_id=layer.id, character_name="G")
    target = TokenPlacement(token_id="t", q=3, r=0, layer_id=layer.id, character_name="T")
    tokens = TokenState(placements={"s": shooter, "t": target})
    result = enrich_preview_targets(
        preview, shooter, tokens, ms, {}, grenade, grenade
    )
    assert result.fire_kind in ("grenade", "agl", "explosive")
    assert result.target_token_ids


def test_filter_ids_by_los_respects_pen() -> None:
    ms = MapState()
    layer = ms.ensure_default_layer()
    layer.walls[hex_wall_key(1, 0)] = WallSegment()
    shooter = TokenPlacement(token_id="s", q=0, r=0, layer_id=layer.id)
    target = TokenPlacement(token_id="t", q=2, r=0, layer_id=layer.id)
    tokens = TokenState(placements={"s": shooter, "t": target})
    clear_optical, blocked_optical = filter_ids_by_los(
        shooter, ["t"], tokens, ms, {}, ammo=None
    )
    assert "t" in blocked_optical
    assert clear_optical == []
    from phoenix_command.item_database.weapons import ammo_556nato_m16a2_fmj

    clear_pen, _ = filter_ids_by_los(
        shooter, ["t"], tokens, ms, {}, ammo=ammo_556nato_m16a2_fmj
    )
    assert "t" in clear_pen
    pen = float(ammo_556nato_m16a2_fmj.get_pen(2))
    assert not check_los(ms, shooter, target, pen=pen).blocked


def test_enrich_preview_targets_grenade_none_range_hexes() -> None:
    """Contact band (range_hexes=None) must not crash max blast radius (O1)."""
    from phoenix_command.item_database.grenades import rgd_5

    preview = PendingShotPreview(
        preview_id="p1",
        shooter_token_id="s",
        target_token_id="t",
        proposed_by="host",
        aim_q=3,
        aim_r=0,
    )
    ms = MapState()
    layer = ms.ensure_default_layer()
    shooter = TokenPlacement(token_id="s", q=0, r=0, layer_id=layer.id, character_name="G")
    target = TokenPlacement(token_id="t", q=3, r=0, layer_id=layer.id, character_name="T")
    tokens = TokenState(placements={"s": shooter, "t": target})
    result = enrich_preview_targets(
        preview, shooter, tokens, ms, {}, rgd_5, rgd_5
    )
    assert result.fire_kind == "grenade"
    assert "t" in result.target_token_ids


def test_grenade_ammo_has_no_get_pen() -> None:
    """Grenade as ammo must not be passed to get_pen (O1 retest)."""
    grenade = Grenade(
        name="Test Grenade",
        country=Country.USSR,
        grenade_type=GrenadeType.FRAG,
        weight=1.0,
        length=4.0,
        arm_time=3,
        fuse_length=1,
        range=10,
    )
    assert not hasattr(grenade, "get_pen")
    pen = None
    if hasattr(grenade, "get_pen"):
        pen = float(grenade.get_pen(1))
    assert pen is None


def test_default_ammo_prefers_pellets_for_shotgun() -> None:
    auto_ammo = default_ammo_for_weapon(spas12, "auto")
    single_ammo = default_ammo_for_weapon(spas12, "single")
    assert auto_ammo is not None and single_ammo is not None
    assert is_pellet_ammo(auto_ammo)
    assert is_pellet_ammo(single_ammo)
    assert infer_fire_kind("single", spas12, single_ammo) == "shotgun"


def test_grenade_hold_survives_phase_advance() -> None:
    ic = ImpulseCombatState(map_mode="combat", impulse=3, phase=1)
    tokens = TokenState()
    tok = TokenPlacement(token_id="t1", character_name="G", q=0, r=0)
    tokens.placements["t1"] = tok
    char = Character(
        name="G",
        strength=14,
        intelligence=14,
        will=12,
        health=12,
        agility=14,
        gun_combat_skill_level=10,
    )
    from phoenix_command.item_database.grenades import rgd_5
    char.add_gear(rgd_5)
    ic.token_runtime["t1"] = TokenCombatRuntime(ac_remaining=1.0, held_grenade_name=rgd_5.name)
    engine = ImpulseCombatEngine(ic, tokens, MapState(), {"G": char})
    engine.advance_impulse()
    rt = engine.get_runtime("t1")
    assert rt.held_grenade_name == rgd_5.name
    assert ic.phase == 2
    assert ic.impulse == 0


def test_default_ammo_prefers_pellets_for_auto() -> None:
    auto_ammo = default_ammo_for_weapon(spas12, "auto")
    assert auto_ammo is not None
    assert is_pellet_ammo(auto_ammo)


def test_kneeling_to_standing_available() -> None:
    ic = ImpulseCombatState(map_mode="combat")
    tokens = TokenState()
    tok = TokenPlacement(token_id="t1", character_name="F", q=0, r=0)
    tokens.placements["t1"] = tok
    char = Character(
        name="F",
        strength=10,
        intelligence=10,
        will=10,
        health=10,
        agility=10,
        gun_combat_skill_level=3,
    )
    ic.token_runtime["t1"] = TokenCombatRuntime(ac_remaining=2.0, stance="kneeling")
    engine = ImpulseCombatEngine(ic, tokens, MapState(), {"F": char})
    actions = dict((a[0], a) for a in engine.available_actions("t1"))
    assert "kneeling_to_standing" in actions
    result = engine.apply_action("t1", "kneeling_to_standing", {}, "host", True)
    assert result.success
    assert engine.get_runtime("t1").stance == "standing"


def test_qa_p_mid_fixture_recoil() -> None:
    import json
    from pathlib import Path
    from phoenix_command.session.game_state import GameState

    data = json.loads(Path("tests/fixtures/qa-p-mid.json").read_text(encoding="utf-8"))
    state = GameState.from_dict(data)
    rt = state.impulse_combat.token_runtime["t1"]
    assert rt.recoil_ac_owed == 1.0
    assert state.impulse_combat.token_runtime["t2"].balance_ac_owed == 2.0


def test_refill_clears_move_progress() -> None:
    ic = ImpulseCombatState(map_mode="combat", impulse=0)
    tokens = TokenState()
    tok = TokenPlacement(token_id="t1", character_name="F", q=0, r=0)
    tokens.placements["t1"] = tok
    char = Character(
        name="F",
        strength=10,
        intelligence=10,
        will=10,
        health=10,
        agility=10,
        gun_combat_skill_level=3,
    )
    rt = TokenCombatRuntime(ac_remaining=0.5, move_progress=0.29, move_target_q=1, move_target_r=0)
    ic.token_runtime["t1"] = rt
    engine = ImpulseCombatEngine(ic, tokens, MapState(), {"F": char})
    engine.advance_impulse()
    rt2 = engine.get_runtime("t1")
    assert rt2.move_progress == 0.0
    assert rt2.move_target_q is None
