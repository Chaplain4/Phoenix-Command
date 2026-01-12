"""Combat simulation for Phoenix Command."""

import random

from phoenix_command.models.character import Character
from phoenix_command.models.enums import ShotType, TargetExposure, AccuracyModifiers
from phoenix_command.models.gear import Weapon, AmmoType
from phoenix_command.models.hit_result_advanced import ShotParameters, ShotResult
from phoenix_command.tables.advanced_damage_tables.advanced_damage_calculator import AdvancedDamageCalculator
from phoenix_command.tables.advanced_damage_tables.table_1_get_hit_location import Table1AdvancedDamageHitLocation
from phoenix_command.tables.core.table4_advanced_odds_of_hitting import Table4AdvancedOddsOfHitting


class CombatSimulator:
    """Simulates combat between characters."""
    
    @staticmethod
    def single_shot(
        shooter: Character,
        target: Character,
        weapon: Weapon,
        ammo: AmmoType,
        range_hexes: int,
        target_exposure: TargetExposure,
        shot_params: ShotParameters,
        is_front_shot: bool = True
    ) -> ShotResult:
        """Simulate a single shot from shooter to target."""
        
        # Get weapon ballistic data at range
        pen = ammo.get_pen(range_hexes)
        dc = ammo.get_dc(range_hexes)
        
        # Calculate EAL (Effective Accuracy Level)
        # Aim Time ALM = weapon aim time modifier + shooter SAL
        aim_time_alm = weapon.aim_time_modifiers.get(shot_params.aim_time_ac, 0) + shooter.skill_accuracy_level
        
        # Range ALM
        range_alm = Table4AdvancedOddsOfHitting.get_accuracy_level_modifier_by_range_4a(range_hexes)
        
        # Stance/Situation ALM
        stance_alm = shot_params.stance.value
        
        # Visibility ALM
        visibility_alm = shot_params.visibility.value
        
        # Movement ALM
        movement_alm = 0
        if shot_params.target_speed_hex_per_impulse > 0:
            movement_alm, _ = Table4AdvancedOddsOfHitting.get_movement_alm_and_max_aim_time_4d(
                shot_params.target_speed_hex_per_impulse, range_hexes
            )
        
        if shot_params.shooter_speed_hex_per_impulse > 0:
            shooter_movement_alm, _ = Table4AdvancedOddsOfHitting.get_movement_alm_and_max_aim_time_4d(
                shot_params.shooter_speed_hex_per_impulse, range_hexes
            )
            movement_alm += shooter_movement_alm
        
        # Target Size ALM
        target_size_alm = Table4AdvancedOddsOfHitting.get_standard_target_size_modifier_4e(
            target_exposure,
            AccuracyModifiers.TARGET_SIZE
        )
        
        # Reflexive Duck modifiers
        duck_alm = 0
        if shot_params.reflexive_duck_shooter:
            duck_alm -= 10
        if shot_params.reflexive_duck_target:
            duck_alm -= 5
        
        # Sum all ALMs to get EAL
        eal = (aim_time_alm + range_alm + stance_alm + visibility_alm + 
               movement_alm + target_size_alm + duck_alm)
        
        # Get Odds of Hitting
        odds = Table4AdvancedOddsOfHitting.get_odds_of_hitting_4g(eal, ShotType.SINGLE)
        
        # Roll to hit
        roll = random.randint(0, 99)
        hit = roll <= odds
        
        if not hit:
            return ShotResult(hit=False, eal=eal, odds=odds, roll=roll)
        
        # Determine hit location
        location = Table1AdvancedDamageHitLocation.get_hit_location(
            target_exposure,
            shot_params.target_orientation
        )
        
        # Get armor protection at hit location
        armor_key = (location, is_front_shot)
        armor_pf = 0
        if armor_key in target.armor_protection:
            armor_pf, _ = target.armor_protection[armor_key]
        
        # Calculate EPEN
        epen = max(0.0, pen - armor_pf)
        
        # Calculate damage
        damage_result = AdvancedDamageCalculator.calculate_damage(
            location=location,
            dc=dc,
            epen=epen,
            is_front=is_front_shot
        )
        
        return ShotResult(
            hit=True,
            eal=eal,
            odds=odds,
            roll=roll,
            damage_result=damage_result
        )
