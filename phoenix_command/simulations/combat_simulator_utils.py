"""Utility functions for combat simulation."""

import random
from typing import Optional, List

from phoenix_command.models.character import Character
from phoenix_command.models.enums import ShotType, TargetExposure, AccuracyModifiers, IncapacitationEffect, SituationStanceModifier4B, BlastModifier, AdvancedHitLocation
from phoenix_command.models.gear import Weapon, AmmoType, BallisticData, Armor
from phoenix_command.models.hit_result_advanced import ShotParameters, ShotResult, TargetGroup, BurstElevationResult, DamageResult
from phoenix_command.tables.advanced_damage_tables.advanced_damage_calculator import AdvancedDamageCalculator
from phoenix_command.tables.advanced_damage_tables.table_1_get_hit_location import Table1AdvancedDamageHitLocation
from phoenix_command.tables.advanced_rules.blunt_damage import Table9ABluntDamage
from phoenix_command.tables.core.table4_advanced_odds_of_hitting import Table4AdvancedOddsOfHitting
from phoenix_command.tables.core.table5_auto_pellet_shrapnel import Table5AutoPelletShrapnel
from phoenix_command.tables.core.table8_healing_and_recovery import Table8HealingAndRecovery


class CombatSimulatorUtils:
    """Utility methods for combat simulation."""

    @staticmethod
    def redistribute_hits_by_eal(
            shooter: Character,
            weapon: Weapon,
            target_hits: List[tuple[int, int, Character, int, TargetExposure, ShotParameters, bool]],
            sab_penalty: int
    ) -> List[tuple[int, int, Character, int, TargetExposure, ShotParameters, bool]]:
        """Redistribute hits proportionally by EAL if total exceeds weapon ROF."""
        total_hits = sum(h[1] for h in target_hits)
        if total_hits <= weapon.full_auto_rof:
            return target_hits

        # Calculate EAL for each target
        target_eals = []
        for idx, hits, target, rng, exposure, shot_params, front in target_hits:
            eal = CombatSimulatorUtils.calculate_eal(
                shooter, target, weapon, rng, exposure, shot_params,
                AccuracyModifiers.AUTO_ELEV
            ) - sab_penalty
            target_eals.append(eal)

        # Redistribute hits proportionally to EAL
        total_eal = sum(target_eals)
        redistributed_hits = []
        remaining_rof = weapon.full_auto_rof

        for i, (eal, (idx, hits, target, rng, exposure, shot_params, front)) in enumerate(
                zip(target_eals, target_hits)):
            if i == len(target_eals) - 1:
                new_hits = remaining_rof
            else:
                proportion = eal / total_eal if total_eal > 0 else 1.0 / len(target_eals)
                new_hits = max(1, int(weapon.full_auto_rof * proportion))
                remaining_rof -= new_hits

            redistributed_hits.append((idx, new_hits, target, rng, exposure, shot_params, front))

        return redistributed_hits

    @staticmethod
    def check_shotgun_burst_elevation_and_get_hits(
            shooter: Character,
            target: Character,
            weapon: Weapon,
            range_hexes: int,
            exposure: TargetExposure,
            shot_params: ShotParameters,
            arc_of_fire: float,
            sab_penalty: int,
            salm: Optional[int]
    ) -> BurstElevationResult:
        """Check elevation for shotgun burst and get hits."""
        if salm is not None:
            eal = CombatSimulatorUtils.calculate_shotgun_eal(
                shooter, target, weapon, range_hexes, exposure, shot_params, salm, sab_penalty
            )
        else:
            eal = CombatSimulatorUtils.calculate_eal(
                shooter, target, weapon, range_hexes, exposure, shot_params, AccuracyModifiers.AUTO_ELEV
            ) - sab_penalty

        return CombatSimulatorUtils.check_elevation_and_calculate_hits(eal, exposure, weapon, arc_of_fire)

    @staticmethod
    def get_shotgun_data_at_range(
            ammo: AmmoType, range_hexes: int
    ) -> BallisticData:
        """Get shotgun SALM, BPHC, and PR at given range."""
        for data in ammo.ballistic_data:
            if range_hexes <= data.range_hexes:
                return data
        raise ValueError("Range exceeds ammo ballistic_data")

    @staticmethod
    def validate_shotgun_inputs(
            targets: List[Character],
            ranges: List[int],
            exposures: List[TargetExposure],
            shot_params_list: List[ShotParameters],
            is_front_shots: List[bool]
    ) -> None:
        """Validate shotgun shot inputs."""
        if not (len(targets) == len(ranges) == len(exposures) == len(shot_params_list) == len(is_front_shots)):
            raise ValueError("Input lists must have same length")

    @staticmethod
    def calculate_shotgun_eal(
            shooter: Character,
            target: Character,
            weapon: Weapon,
            range_hexes: int,
            exposure: TargetExposure,
            shot_params: ShotParameters,
            salm: int,
            sab_penalty: int = 0
    ) -> int:
        """Calculate EAL for shotgun using larger of Target Size ALM or SALM."""
        target_size_alm = Table4AdvancedOddsOfHitting.get_standard_target_size_modifier_4e(
            exposure, AccuracyModifiers.AUTO_ELEV if sab_penalty else AccuracyModifiers.TARGET_SIZE
        )
        eal_base = CombatSimulatorUtils.calculate_eal(
            shooter, target, weapon, range_hexes, exposure, shot_params,
            AccuracyModifiers.AUTO_ELEV if sab_penalty else AccuracyModifiers.TARGET_SIZE
        )
        return (eal_base - sab_penalty) - target_size_alm + max(target_size_alm, salm)

    @staticmethod
    def check_burst_elevation_and_get_hits(
            shooter: Character,
            target: Character,
            weapon: Weapon,
            range_hexes: int,
            exposure: TargetExposure,
            shot_params: ShotParameters,
            arc_of_fire: float,
            sab_penalty: int
    ) -> BurstElevationResult:
        """Check elevation and calculate hits for burst fire."""
        eal = CombatSimulatorUtils.calculate_eal(
            shooter, target, weapon, range_hexes, exposure, shot_params,
            AccuracyModifiers.AUTO_ELEV
        ) - sab_penalty

        return CombatSimulatorUtils.check_elevation_and_calculate_hits(eal, exposure, weapon, arc_of_fire)

    @staticmethod
    def setup_burst_fire(
            weapon: Weapon,
            target_group: TargetGroup,
            continuous_burst_impulses: int,
            arc_of_fire: Optional[float],
            shooter: Character
    ) -> tuple[int, float]:
        """Setup burst fire parameters and return SAB penalty and arc of fire."""
        from phoenix_command.tables.advanced_rules.effective_min_arc import EffectiveMinimumArc
        
        sab_penalty, min_arc = CombatSimulatorUtils.validate_burst_fire_inputs(
            weapon, target_group.targets, target_group.ranges, target_group.exposures,
            target_group.shot_params_list, target_group.is_front_shots, continuous_burst_impulses
        )
        
        shot_params = target_group.shot_params_list[0]

        stance = None
        for mod in shot_params.situation_stance_modifiers:
            if mod in (SituationStanceModifier4B.STANDING, SituationStanceModifier4B.STANDING_AND_BRACED,
                      SituationStanceModifier4B.KNEELING, SituationStanceModifier4B.KNEELING_AND_BRACED,
                      SituationStanceModifier4B.PRONE, SituationStanceModifier4B.PRONE_AND_BRACED,
                      SituationStanceModifier4B.FIRING_FROM_THE_HIP):
                stance = mod
                break
        
        is_moving = shot_params.shooter_speed_hex_per_impulse > 0
        
        effective_ma = EffectiveMinimumArc().get_effective_ma(
            min_arc, weapon.weapon_type, stance, shooter.strength, False, is_moving
        )
        
        return sab_penalty, max(arc_of_fire, effective_ma) if arc_of_fire is not None else effective_ma
    
    @staticmethod
    def calculate_eal(
        shooter: Character,
        target: Character,
        weapon: Weapon,
        range_hexes: int,
        target_exposure: TargetExposure,
        shot_params: ShotParameters,
        target_size_modifier_type: AccuracyModifiers = AccuracyModifiers.TARGET_SIZE
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
        
        situation_stance_alm = sum(mod.value for mod in shot_params.situation_stance_modifiers)
        visibility_alm = sum(mod.value for mod in shot_params.visibility_modifiers)
        
        duck_alm = 0
        if shot_params.reflexive_duck_shooter:
            duck_alm -= 10
        if shot_params.reflexive_duck_target:
            duck_alm -= 5
        
        defensive_alm = target.defensive_alm

        alm_sum = aim_time_alm + range_alm + situation_stance_alm + visibility_alm + movement_alm + duck_alm + defensive_alm

        ba = weapon.ballistic_data.get_ballistic_accuracy(range_hexes) if weapon.ballistic_data else float('inf')

        effective_alm = min(ba, alm_sum)

        target_size_alm = Table4AdvancedOddsOfHitting.get_standard_target_size_modifier_4e(
            target_exposure, target_size_modifier_type
        )
        
        return effective_alm + target_size_alm
    
    @staticmethod
    def determine_incapacitation(
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
    def process_hit(
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
        
        pen = ammo.get_pen(range_hexes)
        dc = ammo.get_dc(range_hexes)
        
        epen = pen
        penetrated = True
        blunt_pf = 0
        total_protection = 0
        for item in target.equipment:
            if isinstance(item, Armor):
                total_protection += item.get_protection(location, is_front_shot).get_total_protection()
                protection_data = item.get_protection(location, is_front_shot)
                if protection_data.get_total_protection() > 0:
                    penetrated, remaining_pen = item.process_hit(location, is_front_shot, pen)
                    epen = remaining_pen
                    if not penetrated:
                        blunt_pf = protection_data.get_total_blunt_protection()
                    break
        
        if not penetrated:
            blunt_damage = Table9ABluntDamage.get_blunt_damage(location, blunt_pf, pen)
            target.apply_damage(blunt_damage)
            damage_result = AdvancedDamageCalculator.calculate_damage(
                location=location, dc=0, epen=0.0, is_front=is_front_shot
            )
            damage_result.damage = blunt_damage
        else:
            epen = max(0.0, epen)
            if total_protection > epen:
                dc = 1
            damage_result = AdvancedDamageCalculator.calculate_damage(
                location=location, dc=dc, epen=epen, is_front=is_front_shot
            )
            target.apply_damage(damage_result.damage)
        
        incap_effect = CombatSimulatorUtils.determine_incapacitation(
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
    def process_target_hits(
        target: Character,
        ammo: AmmoType,
        range_hexes: int,
        exposure: TargetExposure,
        shot_params: ShotParameters,
        is_front_shot: bool,
        hits: int
    ) -> List[ShotResult]:
        """Process multiple hits on a single target."""
        target_results = []
        for _ in range(hits):
            dmg, effect, recovery, time = CombatSimulatorUtils.process_hit(
                target, ammo, range_hexes, exposure, shot_params, is_front_shot
            )
            target_results.append(ShotResult(
                hit=True,
                eal=0,
                odds=100,
                roll=0,
                damage_result=dmg,
                incapacitation_effect=effect,
                recovery=recovery,
                incapacitation_time_phases=time,
            ))
        return target_results
    
    @staticmethod
    def validate_burst_fire_inputs(
        weapon: Weapon,
        targets: List[Character],
        ranges: List[int],
        exposures: List[TargetExposure],
        shot_params_list: List[ShotParameters],
        is_front_shots: List[bool],
        continuous_burst_impulses: int
    ) -> tuple[int, float]:
        """Validate burst fire inputs and return SAB penalty and arc of fire."""
        if not weapon.full_auto or not weapon.full_auto_rof:
            raise ValueError("Weapon must be full auto capable")
        
        if not weapon.ballistic_data:
            raise ValueError("Weapon must have ballistic_data for burst fire")
        
        if not (len(targets) == len(ranges) == len(exposures) == len(shot_params_list) == len(is_front_shots)):
            raise ValueError("Input lists must have same length")
        
        sab_penalty = 0
        if continuous_burst_impulses > 0:
            if not weapon.sustained_auto_burst:
                raise ValueError("Weapon must have sustained_auto_burst for continuous fire")
            sab_penalty = continuous_burst_impulses * weapon.sustained_auto_burst
        
        min_arc = weapon.ballistic_data.get_minimum_arc(ranges[0])
        if min_arc is None:
            raise ValueError("Weapon ballistic_data must have minimum_arc")
        
        return sab_penalty, min_arc

    @staticmethod
    def check_elevation_and_calculate_hits(
        eal: int,
        exposure: TargetExposure,
        weapon: Weapon,
        arc_of_fire: float
    ) -> BurstElevationResult:
        """Check elevation and calculate hits for burst fire."""
        odds = Table4AdvancedOddsOfHitting.get_odds_of_hitting_4g(eal, ShotType.BURST)
        roll = random.randint(0, 99)

        if roll > odds:
            return BurstElevationResult(hit=False, eal=eal, odds=odds, roll=roll, hits=0)
        
        auto_width_modifier = Table4AdvancedOddsOfHitting.get_standard_target_size_modifier_4e(
            exposure, AccuracyModifiers.AUTO_WIDTH
        )
        
        hits = Table5AutoPelletShrapnel.get_fire_table_value5a(
            arc_of_fire, weapon.full_auto_rof, auto_width_modifier
        )

        return BurstElevationResult(hit=hits > 0, eal=eal, odds=odds, roll=roll, hits=hits)

    @staticmethod
    def process_shotgun_pattern(
        ammo: AmmoType,
        targets: List[Character],
        ranges: List[int],
        exposures: List[TargetExposure],
        shot_params_list: List[ShotParameters],
        is_front_shots: List[bool],
        bphc: Optional[str]
    ) -> List[List[ShotResult]]:
        """Process shotgun pattern hits for all targets."""
        if bphc is None:
            pellet_hits_data = []
        else:
            pellet_hits_data = CombatSimulatorUtils.calculate_pellet_hits_per_target(
                targets, ranges, exposures, shot_params_list, is_front_shots, bphc
            )

        if ammo.pellet_count is not None and pellet_hits_data:
            pellet_hits_data = CombatSimulatorUtils.redistribute_pellets(pellet_hits_data, ammo.pellet_count)

        results = [[] for _ in range(len(targets))]
        for idx, hits, target, rng, exposure, params, front, _ in pellet_hits_data:
            results[idx] = CombatSimulatorUtils.process_target_hits(
                target, ammo, rng, exposure, params, front, hits
            )
        
        return results

    @staticmethod
    def calculate_pellet_hits_per_target(
        targets: List[Character],
        ranges: List[int],
        exposures: List[TargetExposure],
        shot_params_list: List[ShotParameters],
        is_front_shots: List[bool],
        bphc: str
    ) -> List[tuple[int, int, Character, int, TargetExposure, ShotParameters, bool, int]]:
        """Calculate pellet hits for each target in pattern."""
        pellet_hits_data = []
        
        for idx, (target, rng, exposure, params, front) in enumerate(zip(targets, ranges, exposures, shot_params_list, is_front_shots)):
            target_size_modifier = Table4AdvancedOddsOfHitting.get_standard_target_size_modifier_4e(
                exposure, AccuracyModifiers.AUTO_WIDTH
            )
            
            if bphc.startswith('*'):
                base_hits = int(bphc[1:])
                pellet_hits = Table5AutoPelletShrapnel.get_shrapnel_pellet_hits_5a(
                    base_hits, True, target_size_modifier
                )
                pellet_roll = 100
            else:
                pellet_hits = Table5AutoPelletShrapnel.get_shrapnel_pellet_hits_5a(
                    int(bphc), False, target_size_modifier
                )
                pellet_roll = random.randint(0, 99)
            
            if pellet_hits > 0:
                pellet_hits_data.append((idx, pellet_hits, target, rng, exposure, params, front, pellet_roll))
        
        return pellet_hits_data

    @staticmethod
    def redistribute_pellets(
        pellet_hits_data: List[tuple[int, int, Character, int, TargetExposure, ShotParameters, bool, int]],
        pellet_count: int
    ) -> List[tuple[int, int, Character, int, TargetExposure, ShotParameters, bool, int]]:
        """Redistribute pellet hits if total exceeds pellet count."""
        total_hits = sum(h[1] for h in pellet_hits_data)
        if total_hits <= pellet_count:
            return pellet_hits_data
        
        redistributed = []
        remaining = pellet_count
        for i, (idx, hits, target, rng, exposure, params, front, pellet_roll) in enumerate(pellet_hits_data):
            if i == len(pellet_hits_data) - 1:
                new_hits = remaining
            else:
                new_hits = max(1, int(pellet_count * (hits / total_hits)))
                remaining -= new_hits
            redistributed.append((idx, new_hits, target, rng, exposure, params, front, pellet_roll))
        return redistributed

    @staticmethod
    def calculate_explosive_eal(
        shooter: Character,
        weapon: Weapon,
        range_hexes: int,
        target_size_alm: int,
        shot_params: ShotParameters
    ) -> int:
        """Calculate EAL for explosive weapon."""
        max_aim_time_impulses = float('inf')
        movement_alm = 0
        
        if shot_params.shooter_speed_hex_per_impulse > 0:
            shooter_movement_alm, max_aim_time_impulses = Table4AdvancedOddsOfHitting.get_movement_alm_and_max_aim_time_4d(
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
        
        situation_stance_alm = sum(mod.value for mod in shot_params.situation_stance_modifiers)
        visibility_alm = sum(mod.value for mod in shot_params.visibility_modifiers)
        
        duck_alm = 0
        if shot_params.reflexive_duck_shooter:
            duck_alm -= 10
        
        alm_sum = aim_time_alm + range_alm + situation_stance_alm + visibility_alm + movement_alm + duck_alm
        
        ba = weapon.ballistic_data.get_ballistic_accuracy(range_hexes) if weapon.ballistic_data else float('inf')
        effective_alm = min(ba, alm_sum)
        
        return effective_alm + target_size_alm

    @staticmethod
    def calculate_grenade_eal(
        shooter: Character,
        range_hexes: int,
        target_size_alm: int,
        aim_alm: int,
        situation_stance_modifiers: List,
        visibility_modifiers: List
    ) -> int:
        """Calculate EAL for thrown grenade."""
        range_alm = Table4AdvancedOddsOfHitting.get_accuracy_level_modifier_by_range_4a(range_hexes)
        situation_stance_alm = sum(mod.value for mod in situation_stance_modifiers)
        visibility_alm = sum(mod.value for mod in visibility_modifiers)
        
        alm_sum = aim_alm + shooter.skill_accuracy_level + range_alm + situation_stance_alm + visibility_alm
        
        return alm_sum + target_size_alm

    @staticmethod
    def process_shrapnel_hits(
        target: Character,
        ammo: AmmoType,
        range_from_burst: int,
        exposure: TargetExposure,
        shot_params: ShotParameters,
        is_front_shot: bool,
        bshc: str
    ) -> List[ShotResult]:
        """
        Process shrapnel hits from explosion.
        """
        target_size_modifier = Table4AdvancedOddsOfHitting.get_standard_target_size_modifier_4e(
            exposure, AccuracyModifiers.AUTO_WIDTH
        )
        if bshc.startswith('*'):
            base_hits = int(bshc[1:])
            is_guaranteed = True
        else:
            base_hits = int(bshc)
            is_guaranteed = False

        # Calculate shrapnel hits using Table 5A
        shrapnel_hits = Table5AutoPelletShrapnel.get_shrapnel_pellet_hits_5a(
            base_hits, is_guaranteed, target_size_modifier
        )

        if shrapnel_hits == 0:
            return []

        # Get shrapnel PEN and DC from explosive_data
        pen = ammo.get_explosion_pen(range_from_burst)
        dc = ammo.get_explosion_dc(range_from_burst)

        results = []
        for _ in range(shrapnel_hits):
            # Get hit location
            location = Table1AdvancedDamageHitLocation.get_hit_location(
                exposure, shot_params.target_orientation
            )

            # Process armor
            epen = pen
            penetrated = True
            blunt_pf = 0
            total_protection = 0

            for item in target.equipment:
                if isinstance(item, Armor):
                    protection_data = item.get_protection(location, is_front_shot)
                    if protection_data and protection_data.get_total_protection() > 0:
                        total_protection += protection_data.get_total_protection()
                        penetrated, remaining_pen = item.process_hit(location, is_front_shot, pen)
                        epen = remaining_pen
                        if not penetrated:
                            blunt_pf = protection_data.get_total_blunt_protection()
                        break

            # Calculate damage
            if not penetrated:
                blunt_damage = Table9ABluntDamage.get_blunt_damage(location, blunt_pf, pen)
                target.apply_damage(blunt_damage)
                damage_result = DamageResult(location=location, damage=blunt_damage)
            else:
                epen = max(0.0, epen)
                effective_dc = 1 if total_protection > epen else dc
                damage_result = AdvancedDamageCalculator.calculate_damage(
                    location=location, dc=effective_dc, epen=epen, is_front=is_front_shot
                )
                target.apply_damage(damage_result.damage)

            # Determine incapacitation
            incap_effect = CombatSimulatorUtils.determine_incapacitation(
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
                incap_time = Table8HealingAndRecovery.get_incapacitation_time_8b(
                    target.physical_damage_total, modifier
                )

            results.append(ShotResult(
                hit=True,
                eal=0,
                odds=base_hits if not is_guaranteed else 100,
                roll=0,
                damage_result=damage_result,
                incapacitation_effect=incap_effect,
                recovery=recovery,
                incapacitation_time_phases=incap_time
            ))

        return results

    @staticmethod
    def process_concussion_damage(
        target: Character,
        base_concussion: int,
        blast_modifiers: List[BlastModifier]
    ) -> Optional[ShotResult]:
        """
        Process concussion damage from explosion.
        """
        if base_concussion <= 0:
            return None

        # Calculate total blast modifier (multiply all modifiers together)
        total_modifier = 1.0
        for modifier in blast_modifiers:
            total_modifier *= modifier.value

        # Calculate concussion damage
        concussion_damage = int(base_concussion * total_modifier)

        if concussion_damage <= 0:
            return None

        # Apply damage to target
        target.apply_damage(concussion_damage)

        # Create damage result with MISS location (concussion has no specific hit location)
        damage_result = DamageResult(
            location=AdvancedHitLocation.MISS,
            damage=concussion_damage,
            shock=0
        )

        # Determine incapacitation from concussion
        incap_effect = CombatSimulatorUtils.determine_incapacitation(
            target, target.physical_damage_total, 0
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
            incap_time = Table8HealingAndRecovery.get_incapacitation_time_8b(
                target.physical_damage_total, modifier
            )

        return ShotResult(
            hit=True,
            eal=0,
            odds=100,
            roll=0,
            damage_result=damage_result,
            incapacitation_effect=incap_effect,
            recovery=recovery,
            incapacitation_time_phases=incap_time
        )
