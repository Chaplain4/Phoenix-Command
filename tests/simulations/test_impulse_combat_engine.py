"""Tests for impulse combat action engine."""

from phoenix_command.models.character import Character
from phoenix_command.models.enums import Caliber, Country, WeaponType
from phoenix_command.models.gear import Weapon
from phoenix_command.session.domains.impulse_combat_state import ImpulseCombatState, TokenCombatRuntime
from phoenix_command.session.domains.map_state import MapState, TerrainTile
from phoenix_command.session.domains.token_state import TokenPlacement, TokenState
from phoenix_command.simulations.impulse_combat_engine import ImpulseCombatEngine, METER_SCALE


def _fighter() -> Character:
    return Character(
        name="Fighter",
        strength=12,
        intelligence=10,
        will=11,
        health=12,
        agility=10,
        gun_combat_skill_level=5,
    )


def _engine(
    ac: float = 1.0,
    stance: str = "standing",
) -> tuple[ImpulseCombatEngine, TokenPlacement]:
    ic = ImpulseCombatState(map_mode="combat", impulse=0)
    tokens = TokenState()
    tok = TokenPlacement(
        token_id="t1",
        character_name="Fighter",
        q=0,
        r=0,
        facing=0,
    )
    tokens.placements["t1"] = tok
    rt = TokenCombatRuntime(ac_remaining=ac, stance=stance)
    ic.token_runtime["t1"] = rt
    char = _fighter()
    weapon = Weapon(
        name="Test Rifle",
        weight=8.0,
        caliber=Caliber.CAL_556_NATO,
        weapon_type=WeaponType.ASSAULT_RIFLE,
        country=Country.USA,
        length_deployed=30.0,
        reload_time=6,
        actions_to_cycle=2,
    )
    char.add_gear(weapon)
    engine = ImpulseCombatEngine(ic, tokens, MapState(), {"Fighter": char})
    engine.get_runtime("t1").held_weapon_name = "Test Rifle"
    return engine, tok


def test_refill_impulse_ac() -> None:
    engine, _ = _engine()
    engine.refill_impulse_ac()
    assert engine.get_runtime("t1").ac_remaining == float(_fighter().impulses[0])


def test_half_hex_move_progress() -> None:
    engine, tok = _engine(ac=0.5)
    result = engine.apply_action("t1", "move", {"target_q": -1, "target_r": 0})
    assert result.success
    rt = engine.get_runtime("t1")
    assert rt.ac_remaining == 0.0
    assert rt.move_progress > 0
    assert tok.q == 0


def test_complete_move_after_second_impulse() -> None:
    engine, tok = _engine(ac=0.5)
    engine.apply_action("t1", "move", {"target_q": -1, "target_r": 0})
    engine.refill_impulse_ac()
    result = engine.apply_action("t1", "move", {"target_q": -1, "target_r": 0})
    assert result.success
    assert tok.q == -1
    assert engine.get_runtime("t1").move_progress == 0.0


def test_braced_move_sets_braced() -> None:
    engine, tok = _engine(ac=2.0)
    engine.apply_action("t1", "movement_while_braced", {"target_q": 1, "target_r": 0})
    assert tok.q == 1
    assert engine.get_runtime("t1").braced is True


def test_aim_cap_when_moved() -> None:
    engine, _ = _engine(ac=10.0)
    engine.apply_action("t1", "move", {"target_q": 1, "target_r": 0})
    max_ac = float(_fighter().impulses[0])
    result = engine.apply_action("t1", "aim", {"ac": max_ac + 5})
    assert result.success
    assert engine.get_runtime("t1").aim_ac_this_impulse <= max_ac


def test_reload_cost() -> None:
    engine, _ = _engine(ac=10.0)
    result = engine.apply_action("t1", "reload", {})
    assert result.success
    assert engine.get_runtime("t1").ac_remaining == 4.0


def test_cycle_cost() -> None:
    engine, _ = _engine(ac=5.0)
    result = engine.apply_action("t1", "cycle", {})
    assert result.success
    assert engine.get_runtime("t1").ac_remaining == 3.0
    assert engine.get_runtime("t1").weapon_cycled is True


def test_meter_scale_halves_rulebook_cost() -> None:
    assert METER_SCALE == 0.5


def test_falling_blocks_aim() -> None:
    engine, _ = _engine(ac=5.0)
    rt = engine.get_runtime("t1")
    rt.knockdown_phase = "falling"
    result = engine.apply_action("t1", "aim", {"ac": 1})
    assert not result.success
    assert "off feet" in result.message.lower()


def test_recover_pays_recoil_then_aim() -> None:
    engine, _ = _engine(ac=5.0)
    rt = engine.get_runtime("t1")
    rt.recoil_ac_owed = 1.0
    result = engine.apply_action("t1", "aim", {"ac": 2})
    assert result.success
    assert rt.recoil_ac_owed == 0.0
    assert rt.ac_remaining == 2.0  # 5 - 1 recover - 2 aim


def test_recover_hands_after_grounded() -> None:
    engine, _ = _engine(ac=5.0)
    rt = engine.get_runtime("t1")
    rt.knockdown_phase = "grounded"
    rt.hands_free = False
    rt.stance = "prone"
    blocked = engine.apply_action("t1", "aim", {"ac": 1})
    assert not blocked.success
    ok = engine.apply_action("t1", "recover_hands", {})
    assert ok.success
    assert rt.hands_free is True
    assert rt.ac_remaining == 2.0


def test_move_breaks_firing_stance() -> None:
    engine, _ = _engine(ac=5.0)
    rt = engine.get_runtime("t1")
    rt.firing_stance_held = True
    engine.apply_action("t1", "move", {"target_q": 1, "target_r": 0})
    assert rt.firing_stance_held is False


def test_refill_promotes_falling_to_grounded() -> None:
    engine, _ = _engine()
    rt = engine.get_runtime("t1")
    rt.knockdown_phase = "falling"
    engine.refill_impulse_ac()
    assert rt.knockdown_phase == "grounded"
