"""process_hit intervening cover PF."""

from phoenix_command.models.character import Character
from phoenix_command.models.enums import (
    SituationStanceModifier4B,
    TargetExposure,
    TargetOrientation,
    VisibilityModifier4C,
)
from phoenix_command.models.gear import AmmoType, BallisticData
from phoenix_command.models.hit_result_advanced import ShotParameters
from phoenix_command.simulations.combat_simulator_utils import CombatSimulatorUtils
from phoenix_command.simulations.map_cover import BarrierCrossing


def _ammo(pen: float = 10.0) -> AmmoType:
    return AmmoType(
        name="Test",
        weight=0.1,
        ballistic_data=[
            BallisticData(range_hexes=10, penetration=pen, damage_class=2),
            BallisticData(range_hexes=100, penetration=pen, damage_class=2),
        ],
    )


def _char() -> Character:
    return Character(
        name="T",
        strength=10,
        intelligence=10,
        will=10,
        health=10,
        agility=10,
        gun_combat_skill_level=4,
    )


def test_manual_cover_pf_stops_round():
    target = _char()
    params = ShotParameters(
        aim_time_ac=2,
        situation_stance_modifiers=[SituationStanceModifier4B.STANDING],
        visibility_modifiers=[VisibilityModifier4C.GOOD_VISIBILITY],
        target_orientation=TargetOrientation.FRONT_REAR,
        cover_pf=20.0,
    )
    log: list[str] = []
    dmg, incap, recovery, incap_time, _kd = CombatSimulatorUtils.process_hit(
        target,
        _ammo(10.0),
        10,
        TargetExposure.STANDING_EXPOSED,
        params,
        True,
        log,
    )
    assert dmg.damage == 0
    assert target.physical_damage_total == 0
    assert any("cover" in line.lower() for line in log)


def test_geometric_cover_pf_logged():
    target = _char()
    barriers = [
        BarrierCrossing(pf=3.0, z_low=0.0, z_high=2.0, label="box", path_t=1.0),
    ]
    params = ShotParameters(
        aim_time_ac=2,
        situation_stance_modifiers=[SituationStanceModifier4B.STANDING],
        visibility_modifiers=[VisibilityModifier4C.GOOD_VISIBILITY],
        target_orientation=TargetOrientation.FRONT_REAR,
        intervening_barriers=barriers,
        shooter_stance="standing",
        target_stance="standing",
    )
    log: list[str] = []
    CombatSimulatorUtils.process_hit(
        target,
        _ammo(10.0),
        10,
        TargetExposure.STANDING_EXPOSED,
        params,
        True,
        log,
    )
    assert any("Intervening cover PF" in line for line in log)
