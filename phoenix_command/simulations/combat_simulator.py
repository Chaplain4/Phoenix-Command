"""Combat simulation for Phoenix Command."""

import random
from typing import Optional, List

from phoenix_command.models.character import Character
from phoenix_command.models.enums import ShotType, TargetExposure, AccuracyModifiers, IncapacitationEffect
from phoenix_command.models.gear import Weapon, AmmoType, BallisticData
from phoenix_command.models.hit_result_advanced import ShotParameters, ShotResult
from phoenix_command.tables.advanced_damage_tables.advanced_damage_calculator import AdvancedDamageCalculator
from phoenix_command.tables.advanced_damage_tables.table_1_get_hit_location import Table1AdvancedDamageHitLocation
from phoenix_command.tables.core.table4_advanced_odds_of_hitting import Table4AdvancedOddsOfHitting
from phoenix_command.tables.core.table5_auto_pellet_shrapnel import Table5AutoPelletShrapnel
from phoenix_command.tables.core.table8_healing_and_recovery import Table8HealingAndRecovery


class CombatSimulator:
    """Simulates combat between characters."""
    
    @staticmethod
    def _calculate_eal(
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
        
        target_size_alm = Table4AdvancedOddsOfHitting.get_standard_target_size_modifier_4e(
            target_exposure, target_size_modifier_type
        )
        
        duck_alm = 0
        if shot_params.reflexive_duck_shooter:
            duck_alm -= 10
        if shot_params.reflexive_duck_target:
            duck_alm -= 5
        
        defensive_alm = target.defensive_alm
        
        return aim_time_alm + range_alm + situation_stance_alm + visibility_alm + movement_alm + target_size_alm + duck_alm + defensive_alm
    
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
    def _redistribute_hits_by_eal(
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
            eal = CombatSimulator._calculate_eal(
                shooter, target, weapon, rng, exposure, shot_params,
                AccuracyModifiers.AUTO_ELEV
            ) - sab_penalty
            target_eals.append(eal)
        
        # Redistribute hits proportionally to EAL
        total_eal = sum(target_eals)
        redistributed_hits = []
        remaining_rof = weapon.full_auto_rof
        
        for i, (eal, (idx, hits, target, rng, exposure, shot_params, front)) in enumerate(zip(target_eals, target_hits)):
            if i == len(target_eals) - 1:
                new_hits = remaining_rof
            else:
                proportion = eal / total_eal if total_eal > 0 else 1.0 / len(target_eals)
                new_hits = max(1, int(weapon.full_auto_rof * proportion))
                remaining_rof -= new_hits
            
            redistributed_hits.append((idx, new_hits, target, rng, exposure, shot_params, front))
        
        return redistributed_hits
    
    @staticmethod
    def _process_target_hits(
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
            dmg, effect, recovery, time = CombatSimulator._process_hit(
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
    def _validate_burst_fire_inputs(
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
    def _get_shotgun_data_at_range(
            ammo: AmmoType, range_hexes: int
    ) -> BallisticData:
        """Get shotgun SALM, BPHC, and PR at given range."""
        for data in ammo.ballistic_data:
            if range_hexes <= data.range_hexes:
                return data
        raise ValueError("Range exceeds ammo ballistic_data")

    @staticmethod
    def _validate_shotgun_inputs(
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
    def _calculate_shotgun_eal(
        shooter: Character,
        target: Character,
        weapon: Weapon,
        range_hexes: int,
        exposure: TargetExposure,
        shot_params: ShotParameters,
        salm: int
    ) -> int:
        """Calculate EAL for shotgun using larger of Target Size ALM or SALM."""
        target_size_alm = Table4AdvancedOddsOfHitting.get_standard_target_size_modifier_4e(
            exposure, AccuracyModifiers.TARGET_SIZE
        )
        eal_base = CombatSimulator._calculate_eal(
            shooter, target, weapon, range_hexes, exposure, shot_params
        )
        return eal_base - target_size_alm + max(target_size_alm, salm)

    @staticmethod
    def _calculate_pellet_hits_per_target(
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
    def _redistribute_pellets(
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
    def get_shotgun_pattern_radius(ammo: AmmoType, range_hexes: int) -> Optional[float]:
        """Get shotgun pattern radius at given range."""
        return CombatSimulator._get_shotgun_data_at_range(ammo, range_hexes).pattern_radius

    @staticmethod
    def single_shot(
        shooter: Character,
        target: Character,
        weapon: Weapon,
        ammo: AmmoType,
        range_hexes: int,
        target_exposure: TargetExposure,
        shot_params: ShotParameters,
        is_front_shot: bool
    ) -> ShotResult:
        """Simulate a single shot from shooter to target."""
        
        eal = CombatSimulator._calculate_eal(
            shooter, target, weapon, range_hexes, target_exposure, shot_params
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

    @staticmethod
    def shotgun_shot(
        shooter: Character,
        targets: List[Character],
        weapon: Weapon,
        ammo: AmmoType,
        ranges: List[int],
        exposures: List[TargetExposure],
        shot_params_list: List[ShotParameters],
        is_front_shots: List[bool],
        primary_target_idx: int = 0
    ) -> List[List[ShotResult]]:
        """Simulate shotgun shot with pattern hitting multiple targets."""
        CombatSimulator._validate_shotgun_inputs(targets, ranges, exposures, shot_params_list, is_front_shots)
        
        primary_range = ranges[primary_target_idx]
        primary_exposure = exposures[primary_target_idx]
        primary_params = shot_params_list[primary_target_idx]
        
        data = CombatSimulator._get_shotgun_data_at_range(ammo, primary_range)

        if data.shotgun_accuracy_level_modifier is None:
            result = CombatSimulator.single_shot(
                shooter, targets[primary_target_idx], weapon, ammo,
                primary_range, primary_exposure, primary_params, is_front_shots[primary_target_idx]
            )
            return [[result] if i == primary_target_idx else [] for i in range(len(targets))]

        eal = CombatSimulator._calculate_shotgun_eal(
            shooter, targets[primary_target_idx], weapon, primary_range,
            primary_exposure, primary_params, data.shotgun_accuracy_level_modifier
        )
        
        odds = Table4AdvancedOddsOfHitting.get_odds_of_hitting_4g(eal, ShotType.SINGLE)
        roll = random.randint(0, 99)
        
        if roll > odds:
            return [[ShotResult(hit=False, eal=eal, odds=odds, roll=roll)] if i == primary_target_idx else [] for i in range(len(targets))]

        if data.base_pellet_hit_chance is None:
            pellet_hits_data = []
        else:
            pellet_hits_data = CombatSimulator._calculate_pellet_hits_per_target(
                targets, ranges, exposures, shot_params_list, is_front_shots, data.base_pellet_hit_chance
            )

        if ammo.pellet_count is not None and pellet_hits_data:
            pellet_hits_data = CombatSimulator._redistribute_pellets(pellet_hits_data, ammo.pellet_count)

        results = [[] for _ in range(len(targets))]
        for idx, hits, target, rng, exposure, params, front, _ in pellet_hits_data:
            results[idx] = CombatSimulator._process_target_hits(
                target, ammo, rng, exposure, params, front, hits
            )
        
        if not results[primary_target_idx]:
            results[primary_target_idx] = [ShotResult(hit=False, eal=eal, odds=odds, roll=roll)]
        
        return results

    @staticmethod
    def burst_fire(
            shooter: Character,
            targets: List[Character],
            weapon: Weapon,
            ammo: AmmoType,
            ranges: List[int],
            exposures: List[TargetExposure],
            shot_params_list: List[ShotParameters],
            is_front_shots: List[bool],
            arc_of_fire: Optional[float] = None,
            continuous_burst_impulses: int = 0,
    ) -> List[List[ShotResult]]:

        sab_penalty, min_arc = CombatSimulator._validate_burst_fire_inputs(
            weapon, targets, ranges, exposures, shot_params_list, is_front_shots, continuous_burst_impulses
        )
        
        if arc_of_fire is None:
            arc_of_fire = min_arc

        results: List[List[ShotResult]] = []
        
        # Collect hits per target with their EAL for proportional distribution
        target_hits: List[tuple[int, int, Character, int, TargetExposure, ShotParameters, bool]] = []  # (index, hits, target, range, exposure, params, is_front)

        for idx, (target, rng, exposure, shot_params, front) in enumerate(zip(
                targets, ranges, exposures, shot_params_list, is_front_shots
        )):
            eal = CombatSimulator._calculate_eal(
                shooter, target, weapon, rng, exposure, shot_params,
                AccuracyModifiers.AUTO_ELEV
            ) - sab_penalty

            odds = Table4AdvancedOddsOfHitting.get_odds_of_hitting_4g(eal, ShotType.BURST)
            roll = random.randint(0, 99)

            if roll > odds:
                results.append([ShotResult(hit=False, eal=eal, odds=odds, roll=roll)])
                continue
            
            auto_width_modifier = Table4AdvancedOddsOfHitting.get_standard_target_size_modifier_4e(
                exposure, AccuracyModifiers.AUTO_WIDTH
            )
            
            hits = Table5AutoPelletShrapnel.get_fire_table_value5a(
                arc_of_fire, weapon.full_auto_rof, auto_width_modifier
            )

            if hits <= 0:
                results.append([ShotResult(hit=False, eal=eal, odds=0, roll=0)])
            else:
                target_hits.append((idx, hits, target, rng, exposure, shot_params, front))
        
        # Redistribute hits if total exceeds ROF
        target_hits = CombatSimulator._redistribute_hits_by_eal(
            shooter, weapon, target_hits, sab_penalty
        )
        
        # Process hits for each target
        results_dict = {}
        for idx, hits, target, rng, exposure, shot_params, front in target_hits:
            results_dict[idx] = CombatSimulator._process_target_hits(
                target, ammo, rng, exposure, shot_params, front, hits
            )
        
        # Build final results list in original order
        final_results = []
        for idx in range(len(targets)):
            if idx in results_dict:
                final_results.append(results_dict[idx])
            elif idx < len(results):
                final_results.append(results[idx])
        
        return final_results
