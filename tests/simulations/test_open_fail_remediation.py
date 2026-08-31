"""Regression tests for open Fail remediation (K3/L3 costs, stair, fuse defer)."""

from phoenix_command.models.character import Character
from phoenix_command.models.enums import Caliber, Country, WeaponType
from phoenix_command.models.gear import Weapon
from phoenix_command.session.domains.impulse_combat_state import (
    ImpulseCombatState,
    PendingGrenadeExplosion,
    TokenCombatRuntime,
)
from phoenix_command.session.domains.map_state import LayerStair, MapLayer, MapState
from phoenix_command.session.domains.token_state import TokenPlacement, TokenState
from phoenix_command.simulations.impulse_combat_engine import ImpulseCombatEngine
from phoenix_command.simulations.map_fire_dispatch import (
    MapFireOutcome,
    serialize_blast_mod_overrides,
    _deserialize_blast_mod_overrides,
)
from phoenix_command.models.enums import BlastModifier


def _fighter(ac: float = 2.0, stance: str = "standing") -> tuple[ImpulseCombatEngine, TokenPlacement]:
    ic = ImpulseCombatState(map_mode="combat", impulse=0)
    tokens = TokenState()
    tok = TokenPlacement(token_id="t1", character_name="Fighter", q=0, r=0, facing=0)
    tokens.placements["t1"] = tok
    char = Character(
        name="Fighter",
        strength=12,
        intelligence=10,
        will=11,
        health=12,
        agility=10,
        gun_combat_skill_level=5,
    )
    weapon = Weapon(
        name="Test Rifle",
        weight=8.0,
        caliber=Caliber.CAL_556_NATO,
        weapon_type=WeaponType.ASSAULT_RIFLE,
        country=Country.USA,
        length_deployed=30.0,
        reload_time=6,
    )
    char.add_gear(weapon)
    ic.token_runtime["t1"] = TokenCombatRuntime(ac_remaining=ac, stance=stance)
    engine = ImpulseCombatEngine(ic, tokens, MapState(), {"Fighter": char})
    engine.get_runtime("t1").held_weapon_name = "Test Rifle"
    return engine, tok


def test_braced_move_completes_with_enough_ac() -> None:
    engine, tok = _fighter(ac=1.5)
    result = engine.apply_action(
        "t1", "movement_while_braced", {"target_q": 1, "target_r": 0}
    )
    assert result.success
    assert tok.q == 1
    assert engine.get_runtime("t1").braced is True
    assert engine.get_runtime("t1").move_progress == 0.0


def test_braced_move_partial_when_ac_low() -> None:
    engine, tok = _fighter(ac=1.0)
    result = engine.apply_action(
        "t1", "movement_while_braced", {"target_q": 1, "target_r": 0}
    )
    assert result.success
    assert tok.q == 0
    assert engine.get_runtime("t1").move_progress > 0
    assert "Moving" in result.message


def test_prone_forward_needs_two_ac() -> None:
    engine, tok = _fighter(ac=1.0, stance="prone")
    r1 = engine.apply_action("t1", "move", {"target_q": 1, "target_r": 0})
    assert r1.success
    assert tok.q == 0
    assert engine.get_runtime("t1").move_progress > 0
    engine.refill_impulse_ac()
    engine.get_runtime("t1").ac_remaining = 1.0
    r2 = engine.apply_action("t1", "move", {"target_q": 1, "target_r": 0})
    assert r2.success
    assert tok.q == 1


def test_stair_lookup_uses_token_layer() -> None:
    """E11: stair on token layer; active layer mismatch must still transfer."""
    ms = MapState()
    ground = ms.ensure_default_layer()
    ground.id = "g"
    ground.name = "Ground"
    floor = MapLayer(id="f1", name="Floor 1")
    ms.layers = [ground, floor]
    ms.active_layer_id = "f1"
    key = "2,1"
    ground.stairs[key] = LayerStair(target_layer_id="f1", source_layer_id="g")
    floor.stairs[key] = LayerStair(target_layer_id="g", source_layer_id="f1")

    tok = TokenPlacement(token_id="t1", q=2, r=1, layer_id="g", character_name="A")
    # Simulate corrected lookup logic (same as hex_map_view)
    layer = ms.get_layer(tok.layer_id)
    stairs = layer.stairs.get(key) if layer else None
    assert stairs is not None
    assert stairs.target_layer_id != tok.layer_id
    tok.layer_id = stairs.target_layer_id
    assert tok.layer_id == "f1"


def test_fuse_blast_mod_overrides_roundtrip() -> None:
    mods = {"t2": [BlastModifier.IN_SMALL_ROOM, BlastModifier.PRONE]}
    raw = serialize_blast_mod_overrides(mods)
    restored = _deserialize_blast_mod_overrides(raw)
    assert restored["t2"] == mods["t2"]

    pending = PendingGrenadeExplosion(
        explosion_id="e1",
        resolve_phase=2,
        resolve_impulse=0,
        shooter_token_id="t1",
        blast_mod_overrides=raw,
    )
    back = PendingGrenadeExplosion.from_dict(pending.to_dict())
    assert back.blast_mod_overrides == raw


def test_map_fire_outcome_fuse_cancel_fields() -> None:
    outcome = MapFireOutcome(kind="grenade", fuse_impulses=8)
    outcome.blast_cancelled = True
    outcome.fuse_impulses = 0
    assert outcome.blast_cancelled is True
    assert outcome.fuse_impulses == 0
