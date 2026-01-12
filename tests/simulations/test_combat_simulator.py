"""Tests for combat simulation."""

from phoenix_command.models.enums import (
    Caliber, WeaponType, Country, TargetExposure,
    ShooterStance, VisibilityModifier4C
)
from phoenix_command.models.gear import Weapon, AmmoType, BallisticData, WeaponBallisticData, RangeData
from phoenix_command.models.hit_result_advanced import ShotParameters
from phoenix_command.simulations.character_generator import CharacterGenerator
from phoenix_command.simulations.combat_simulator import CombatSimulator


def test_basic_shot_miss():
    """Test a basic shot that misses."""
    shooter = CharacterGenerator.generate_character(
        gun_combat_skill_level=1,
        strength=10,
        agility=10
    )
    
    target = CharacterGenerator.generate_character(
        gun_combat_skill_level=3,
        strength=12,
        agility=12
    )
    
    # Create simple weapon
    weapon = Weapon(
        name="Test Rifle",
        weight=8.0,
        caliber=Caliber.CAL_762_NATO,
        weapon_type=WeaponType.ASSAULT_RIFLE,
        country=Country.USA,
        length_deployed=40.0,
        aim_time_modifiers={1: -10, 2: -5, 3: 0, 4: 5},
        ballistic_data=WeaponBallisticData(
            ballistic_accuracy=[RangeData(10, 10.0), RangeData(50, 5.0)],
            time_of_flight=[RangeData(10, 0.1), RangeData(50, 0.5)]
        )
    )
    
    ammo = AmmoType(
        name="7.62mm FMJ",
        weight=0.5,
        ballistic_data=[
            BallisticData(range_hexes=10, penetration=15.0, damage_class=6),
            BallisticData(range_hexes=50, penetration=12.0, damage_class=6)
        ]
    )
    
    shot_params = ShotParameters(
        aim_time_ac=1,
        stance=ShooterStance.STANDING,
        visibility=VisibilityModifier4C.GOOD_VISIBILITY
    )
    
    # Shoot at long range with poor aim - likely to miss
    result = CombatSimulator.single_shot(
        shooter=shooter,
        target=target,
        weapon=weapon,
        ammo=ammo,
        range_hexes=100,
        target_exposure=TargetExposure.STANDING_EXPOSED,
        shot_params=shot_params
    )
    
    assert result.eal is not None
    assert result.odds >= 0
    assert result.roll >= 0


def test_basic_shot_hit():
    """Test a shot that hits."""
    shooter = CharacterGenerator.generate_character(
        gun_combat_skill_level=10,
        strength=15,
        agility=15
    )
    
    target = CharacterGenerator.generate_character(
        gun_combat_skill_level=3,
        strength=12,
        agility=12
    )
    
    weapon = Weapon(
        name="Test Rifle",
        weight=8.0,
        caliber=Caliber.CAL_762_NATO,
        weapon_type=WeaponType.ASSAULT_RIFLE,
        country=Country.USA,
        length_deployed=40.0,
        aim_time_modifiers={1: -5, 2: 0, 3: 5, 4: 10, 5: 15},
        ballistic_data=WeaponBallisticData(
            ballistic_accuracy=[RangeData(10, 15.0), RangeData(50, 10.0)],
            time_of_flight=[RangeData(10, 0.1), RangeData(50, 0.5)]
        )
    )
    
    ammo = AmmoType(
        name="7.62mm FMJ",
        weight=0.5,
        ballistic_data=[
            BallisticData(range_hexes=10, penetration=18.0, damage_class=7),
            BallisticData(range_hexes=50, penetration=15.0, damage_class=7)
        ]
    )
    
    shot_params = ShotParameters(
        aim_time_ac=5,
        stance=ShooterStance.PRONE,
        visibility=VisibilityModifier4C.GOOD_VISIBILITY
    )
    
    # Close range, good aim - force hit by setting high skill
    result = CombatSimulator.single_shot(
        shooter=shooter,
        target=target,
        weapon=weapon,
        ammo=ammo,
        range_hexes=5,
        target_exposure=TargetExposure.STANDING_EXPOSED,
        shot_params=shot_params
    )
    
    # Verify result structure
    assert isinstance(result.hit, bool)
    assert result.eal is not None
    
    if result.hit:
        assert result.damage_result is not None
        assert result.damage_result.location is not None
        assert result.damage_result.damage >= 0
