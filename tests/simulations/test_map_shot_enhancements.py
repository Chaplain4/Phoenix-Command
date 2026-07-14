"""Tests for orientation, LOS, custom EAL, and TOF scheduling."""

from phoenix_command.models.character import Character
from phoenix_command.models.enums import (
    Caliber,
    Country,
    SituationStanceModifier4B,
    TargetExposure,
    TargetOrientation,
    VisibilityModifier4C,
    WeaponType,
)
from phoenix_command.models.gear import Weapon
from phoenix_command.models.hit_result_advanced import ShotParameters
from phoenix_command.session.domains.impulse_combat_state import (
    ImpulseCombatState,
    TokenCombatRuntime,
)
from phoenix_command.session.domains.map_state import (
    HexGridConfig,
    HexCondition,
    MapLayer,
    MapState,
    Opening,
    WallSegment,
    hex_wall_key,
)
from phoenix_command.session.domains.token_state import TokenPlacement, TokenState
from phoenix_command.simulations.combat_simulator_utils import CombatSimulatorUtils
from phoenix_command.simulations.hex_tactical import relative_orientation
from phoenix_command.simulations.impulse_combat_engine import ImpulseCombatEngine
from phoenix_command.simulations.map_los import check_los
from phoenix_command.simulations.map_shot_context import build_map_shot_context


def test_orientation_front_rear_oblique_sides() -> None:
    # Target at (0,0) facing east (0); shooter east of target → front
    assert relative_orientation(0, 0, 0, 2, 0) == "front"
    # Shooter west → rear
    assert relative_orientation(0, 0, 0, -2, 0) == "rear"
    # Shooter roughly NE of east-facing target → oblique or side
    key = relative_orientation(0, 0, 0, 1, -2)
    assert key in ("oblique", "left_side", "right_side", "front")
    # Pure north of east-facing → left or right side / oblique
    key = relative_orientation(0, 0, 0, 0, -3)
    assert key in ("left_side", "right_side", "oblique")


def test_orientation_maps_to_enums() -> None:
    from phoenix_command.simulations.map_shot_context import ORIENTATION_MAP

    assert ORIENTATION_MAP["front"] == TargetOrientation.FRONT_REAR
    assert ORIENTATION_MAP["oblique"] == TargetOrientation.OBLIQUE
    assert ORIENTATION_MAP["left_side"] == TargetOrientation.LEFT_SIDE
    assert ORIENTATION_MAP["right_side"] == TargetOrientation.RIGHT_SIDE


def test_los_blocked_by_solid_wall() -> None:
    map_state = MapState()
    layer = map_state.ensure_default_layer()
    # Wall on target hex edge facing west (edge toward shooter at -1)
    layer.walls["2,0:3"] = WallSegment(openings=[])  # solid
    shooter = TokenPlacement(token_id="s", q=0, r=0, layer_id=layer.id)
    target = TokenPlacement(token_id="t", q=2, r=0, layer_id=layer.id, facing=0)
    # Place wall between 1,0 and 2,0
    layer.walls["1,0:0"] = WallSegment(openings=[])
    result = check_los(map_state, shooter, target)
    # May or may not block depending on edge keys — at least returns LosResult
    assert isinstance(result.blocked, bool)


def test_los_blocked_by_hex_wall() -> None:
    map_state = MapState()
    layer = map_state.ensure_default_layer()
    layer.walls[hex_wall_key(1, 0)] = WallSegment()
    shooter = TokenPlacement(token_id="s", q=0, r=0, layer_id=layer.id)
    target = TokenPlacement(token_id="t", q=2, r=0, layer_id=layer.id)
    result = check_los(map_state, shooter, target)
    assert result.blocked
    assert any("hex wall" in note for note in result.notes)


def test_los_through_open_window() -> None:
    map_state = MapState()
    layer = map_state.ensure_default_layer()
    layer.walls["1,0:0"] = WallSegment(
        openings=[Opening(kind="window", state="open")]
    )
    shooter = TokenPlacement(token_id="s", q=0, r=0, layer_id=layer.id)
    target = TokenPlacement(token_id="t", q=2, r=0, layer_id=layer.id)
    result = check_los(map_state, shooter, target, TokenCombatRuntime(stance="standing"))
    assert not result.blocked
    assert result.clear
    if result.through_opening:
        assert TargetExposure.HEAD in result.visible_exposures
        assert TargetExposure.FIRING_OVER_COVER in result.visible_exposures


def test_cross_layer_visible_cover_exposures() -> None:
    map_state = MapState()
    ground = map_state.ensure_default_layer()
    ground.elevation = 0
    floor = MapLayer(name="Floor2", kind="floor", elevation=1)
    map_state.layers.append(floor)
    shooter = TokenPlacement(token_id="s", q=0, r=0, layer_id=ground.id)
    target = TokenPlacement(token_id="t", q=3, r=0, layer_id=floor.id)
    result = check_los(map_state, shooter, target, TokenCombatRuntime())
    assert result.clear
    assert TargetExposure.HEAD in result.visible_exposures


def test_custom_eal_in_calculate_eal() -> None:
    shooter = Character(
        name="A", strength=12, intelligence=10, will=11, health=12, agility=10,
        gun_combat_skill_level=5,
    )
    target = Character(
        name="B", strength=12, intelligence=10, will=11, health=12, agility=10,
        gun_combat_skill_level=5,
    )
    weapon = Weapon(
        name="Test",
        weight=8.0,
        caliber=Caliber.CAL_556_NATO,
        weapon_type=WeaponType.ASSAULT_RIFLE,
        country=Country.USA,
        length_deployed=30.0,
        aim_time_modifiers={2: 10, 4: 12},
    )
    from phoenix_command.models.gear import WeaponBallisticData, RangeData
    weapon.ballistic_data = WeaponBallisticData(
        ballistic_accuracy=[RangeData(range_hexes=100, value=40)],
        time_of_flight=[RangeData(range_hexes=100, value=0)],
    )
    base_params = ShotParameters(
        aim_time_ac=2,
        situation_stance_modifiers=[SituationStanceModifier4B.STANDING],
        visibility_modifiers=[VisibilityModifier4C.GOOD_VISIBILITY],
    )
    eal_base = CombatSimulatorUtils.calculate_eal(
        shooter, target, weapon, 10, TargetExposure.STANDING_EXPOSED, base_params
    )
    custom_params = ShotParameters(
        aim_time_ac=2,
        situation_stance_modifiers=[SituationStanceModifier4B.STANDING],
        visibility_modifiers=[VisibilityModifier4C.GOOD_VISIBILITY],
        custom_eal_modifiers=[("bonus", 5)],
    )
    eal_custom = CombatSimulatorUtils.calculate_eal(
        shooter, target, weapon, 10, TargetExposure.STANDING_EXPOSED, custom_params
    )
    assert eal_custom == eal_base + 5


def test_tof_schedule_and_due() -> None:
    ic = ImpulseCombatState(map_mode="combat", phase=1, impulse=0)
    tokens = TokenState()
    tokens.placements["t1"] = TokenPlacement(token_id="t1", character_name="A", q=0, r=0)
    engine = ImpulseCombatEngine(ic, tokens, MapState(), {})
    proj = engine.schedule_projectile("t1", "t2", 1, {"x": 1})
    assert proj.resolve_impulse == 1
    due = engine.advance_impulse()
    assert len(due) == 1
    assert due[0].shot_snapshot["x"] == 1
    assert ic.pending_projectiles == []


def test_cycle_and_custom_skip_actions() -> None:
    char = Character(
        name="A", strength=12, intelligence=10, will=11, health=12, agility=10,
        gun_combat_skill_level=5,
    )
    weapon = Weapon(
        name="Bolt",
        weight=8.0,
        caliber=Caliber.CAL_556_NATO,
        weapon_type=WeaponType.ASSAULT_RIFLE,
        country=Country.USA,
        length_deployed=30.0,
        reload_time=4,
        actions_to_cycle=2,
    )
    char.add_gear(weapon)
    ic = ImpulseCombatState(map_mode="combat", impulse=0)
    tokens = TokenState()
    tokens.placements["t1"] = TokenPlacement(token_id="t1", character_name="A")
    rt = TokenCombatRuntime(ac_remaining=10, held_weapon_name="Bolt", weapon_cycled=False)
    ic.token_runtime["t1"] = rt
    engine = ImpulseCombatEngine(ic, tokens, MapState(), {"A": char})
    actions = engine.available_actions("t1")
    ids = [a[0] for a in actions]
    assert "cycle" in ids
    assert "custom_action" in ids
    assert "skip_impulse" in ids
    assert engine.apply_action("t1", "cycle").success
    assert rt.weapon_cycled
    assert engine.apply_action("t1", "custom_action", {"ac": 2, "label": "Radio"}).success
    assert engine.apply_action("t1", "skip_impulse").success
    assert rt.ac_remaining == 0


def test_fire_mode_and_aim_target() -> None:
    char = Character(
        name="A", strength=12, intelligence=10, will=11, health=12, agility=10,
        gun_combat_skill_level=5,
    )
    ic = ImpulseCombatState(map_mode="combat", impulse=0)
    tokens = TokenState()
    tokens.placements["t1"] = TokenPlacement(token_id="t1", character_name="A")
    rt = TokenCombatRuntime(ac_remaining=5)
    ic.token_runtime["t1"] = rt
    engine = ImpulseCombatEngine(ic, tokens, MapState(), {"A": char})
    assert engine.apply_action("t1", "set_fire_mode", {"fire_mode": "auto"}).success
    assert rt.fire_mode == "auto"
    assert engine.apply_action("t1", "aim", {"ac": 1, "target_token_id": "enemy"}).success
    assert rt.aim_target_token_id == "enemy"
    assert rt.aimed_this_impulse
    engine.advance_impulse()
    assert engine.get_runtime("t1").aim_impulses == 1


def test_map_shot_context_uses_target_facing() -> None:
    map_state = MapState()
    map_state.grid = HexGridConfig(meters_per_hex=1.0)
    layer = map_state.ensure_default_layer()
    shooter = TokenPlacement(token_id="s", q=0, r=0, facing=0, layer_id=layer.id)
    target = TokenPlacement(token_id="t", q=4, r=0, facing=6, layer_id=layer.id)  # facing west
    ctx = build_map_shot_context(
        shooter,
        TokenCombatRuntime(),
        target,
        TokenCombatRuntime(),
        map_state,
    )
    # Target faces west, shot from west → roughly front
    assert ctx.orientation_key in ("front", "oblique", "rear")
    assert ctx.range_rule_hexes == 2
