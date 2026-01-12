"""Combat simulation for Phoenix Command."""

import random
from typing import Optional

from phoenix_command.models.character import Character
from phoenix_command.models.enums import ShotType, TargetExposure, AccuracyModifiers, IncapacitationEffect
from phoenix_command.models.gear import Weapon, AmmoType
from phoenix_command.models.hit_result_advanced import ShotParameters, ShotResult
from phoenix_command.tables.advanced_damage_tables.advanced_damage_calculator import AdvancedDamageCalculator
from phoenix_command.tables.advanced_damage_tables.table_1_get_hit_location import Table1AdvancedDamageHitLocation
from phoenix_command.tables.core.table4_advanced_odds_of_hitting import Table4AdvancedOddsOfHitting
from phoenix_command.tables.core.table8_healing_and_recovery import Table8HealingAndRecovery


class CombatSimulator:
    """Simulates combat between characters."""
    
    @staticmethod
    def _calculate_eal(
        shooter: Character,
        weapon: Weapon,
        range_hexes: int,
        target_exposure: TargetExposure,
        shot_params: ShotParameters
    ) -> int:
        """Calculate Effective Accuracy Level (EAL) for a shot."""
        max_aim_time_impulses = float('inf')
        movement_alm = 0
        
        if shot_params.target_speed_hex_per_impulse > 0:
            target_movement_alm, target_max_aim = Table4AdvancedOddsOfHitting.get_movement_alm_and_max_aim_time_4d(
                shot_params.target_speed_hex_per_impulse, range_hexes
            )
            movement_alm += target_movement_alm
            max_aim_time_impulses = min(max_aim_time_impulses, target_max_aim)
        
        if shot_params.shooter_speed_hex_per_impulse > 0:
            shooter_movement_alm, _ = Table4AdvancedOddsOfHitting.get_movement_alm_and_max_aim_time_4d(
                shot_params.shooter_speed_hex_per_impulse, range_hexes
            )
            movement_alm += shooter_movement_alm
            max_aim_time_impulses = min(max_aim_time_impulses, 1.0)
        
        effective_aim_time_ac = shot_params.aim_time_ac
        if max_aim_time_impulses < float('inf'):
            max_ac_per_impulse = max(shooter.impulses)
            max_aim_time_ac = int(max_aim_time_impulses * max_ac_per_impulse)
            effective_aim_time_ac = min(shot_params.aim_time_ac, max_aim_time_ac)
        
        aim_time_alm = weapon.aim_time_modifiers.get(effective_aim_time_ac, 0) + shooter.skill_accuracy_level
        range_alm = Table4AdvancedOddsOfHitting.get_accuracy_level_modifier_by_range_4a(range_hexes)
        stance_alm = shot_params.stance.value
        visibility_alm = shot_params.visibility.value
        target_size_alm = Table4AdvancedOddsOfHitting.get_standard_target_size_modifier_4e(
            target_exposure, AccuracyModifiers.TARGET_SIZE
        )
        
        duck_alm = 0
        if shot_params.reflexive_duck_shooter:
            duck_alm -= 10
        if shot_params.reflexive_duck_target:
            duck_alm -= 5
        
        return aim_time_alm + range_alm + stance_alm + visibility_alm + movement_alm + target_size_alm + duck_alm
    
    @staticmethod
    def _determine_incapacitation(
        target: Character,
        pd_total: int,
        shock: int
    ) -> Optional[IncapacitationEffect]:
        """Determine incapacitation effect."""
        pd_with_shock = pd_total + shock
        
        chance = Table8HealingAndRecovery.get_incapacitation_chance(pd_with_shock, target.knockout_value)
        if chance == 0:
            return None
        
        roll = random.randint(0, 99)
        if roll >= chance:
            return None
        
        effect_roll = random.randint(0, 99)
        return Table8HealingAndRecovery.get_incapacitation_effect(pd_with_shock, target.knockout_value, effect_roll)
    
    @staticmethod
    def _process_hit(
        target: Character,
        ammo: AmmoType,
        range_hexes: int,
        target_exposure: TargetExposure,
        shot_params: ShotParameters,
        is_front_shot: bool
    ):
        """Process a successful hit and calculate damage."""
        location = Table1AdvancedDamageHitLocation.get_hit_location(
            target_exposure, shot_params.target_orientation
        )
        
        armor_key = (location, is_front_shot)
        armor_pf = 0
        if armor_key in target.armor_protection:
            armor_pf, _ = target.armor_protection[armor_key]
        
        pen = ammo.get_pen(range_hexes)
        dc = ammo.get_dc(range_hexes)
        epen = max(0.0, pen - armor_pf)
        
        damage_result = AdvancedDamageCalculator.calculate_damage(
            location=location, dc=dc, epen=epen, is_front=is_front_shot
        )
        
        target.apply_damage(damage_result.damage)
        
        incap_effect = CombatSimulator._determine_incapacitation(
            target, target.physical_damage_total, damage_result.shock
        )
        
        recovery = Table8HealingAndRecovery.get_critical_time_period_and_recovery_chance_8a(
            target.physical_damage_total, target.health
        )
        
        incap_time = None
        if incap_effect:
            modifier = 0
            if incap_effect == IncapacitationEffect.DAZED:
                modifier = -1
            elif incap_effect == IncapacitationEffect.DISORIENTED:
                modifier = -2
            incap_time = Table8HealingAndRecovery.get_incapacitation_time_8b(target.physical_damage_total, modifier)
        
        return damage_result, incap_effect, recovery, incap_time
    
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
        
        eal = CombatSimulator._calculate_eal(
            shooter, weapon, range_hexes, target_exposure, shot_params
        )
        
        odds = Table4AdvancedOddsOfHitting.get_odds_of_hitting_4g(eal, ShotType.SINGLE)
        roll = random.randint(0, 99)
        hit = roll <= odds
        
        if not hit:
            return ShotResult(hit=False, eal=eal, odds=odds, roll=roll)
        
        damage_result, incap_effect, recovery, incap_time = CombatSimulator._process_hit(
            target, ammo, range_hexes, target_exposure, shot_params, is_front_shot
        )
        
        return ShotResult(
            hit=True,
            eal=eal,
            odds=odds,
            roll=roll,
            damage_result=damage_result,
            incapacitation_effect=incap_effect,
            recovery=recovery,
            incapacitation_time_phases=incap_time
        )
