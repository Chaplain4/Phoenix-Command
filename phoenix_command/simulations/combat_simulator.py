"""Combat simulation for Phoenix Command."""

import random
from collections import defaultdict
from typing import Optional, List

from phoenix_command.models.character import Character
from phoenix_command.models.enums import ShotType, TargetExposure, ExplosiveTarget, SituationStanceModifier4B
from phoenix_command.models.gear import Weapon, AmmoType
from phoenix_command.models.hit_result_advanced import ShotParameters, ShotResult, TargetGroup, ExplosiveShotResult
from phoenix_command.simulations.combat_simulator_utils import CombatSimulatorUtils
from phoenix_command.tables.advanced_rules.effective_min_arc import EffectiveMinimumArc
from phoenix_command.tables.advanced_rules.three_round_burst import ThreeRoundBurstTable
from phoenix_command.tables.core.table4_advanced_odds_of_hitting import Table4AdvancedOddsOfHitting
from phoenix_command.tables.core.table5_auto_pellet_shrapnel import Table5AutoPelletShrapnel


class CombatSimulator:
    """Simulates combat between characters."""

    @staticmethod
    def get_shotgun_pattern_radius(ammo: AmmoType, range_hexes: int) -> Optional[float]:
        """Get shotgun pattern radius at given range."""
        return CombatSimulatorUtils.get_shotgun_data_at_range(ammo, range_hexes).pattern_radius

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
        
        eal = CombatSimulatorUtils.calculate_eal(
            shooter, target, weapon, range_hexes, target_exposure, shot_params
        )
        
        odds = Table4AdvancedOddsOfHitting.get_odds_of_hitting_4g(eal, ShotType.SINGLE)
        roll = random.randint(0, 99)
        hit = roll <= odds
        
        if not hit:
            return ShotResult(hit=False, eal=eal, odds=odds, roll=roll)
        
        damage_result, incap_effect, recovery, incap_time = CombatSimulatorUtils.process_hit(
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
        CombatSimulatorUtils.validate_shotgun_inputs(targets, ranges, exposures, shot_params_list, is_front_shots)
        
        primary_range = ranges[primary_target_idx]
        primary_exposure = exposures[primary_target_idx]
        primary_params = shot_params_list[primary_target_idx]
        
        data = CombatSimulatorUtils.get_shotgun_data_at_range(ammo, primary_range)

        if data.shotgun_accuracy_level_modifier is None:
            result = CombatSimulator.single_shot(
                shooter, targets[primary_target_idx], weapon, ammo,
                primary_range, primary_exposure, primary_params, is_front_shots[primary_target_idx]
            )
            return [[result] if i == primary_target_idx else [] for i in range(len(targets))]

        eal = CombatSimulatorUtils.calculate_shotgun_eal(
            shooter, targets[primary_target_idx], weapon, primary_range,
            primary_exposure, primary_params, data.shotgun_accuracy_level_modifier
        )
        
        odds = Table4AdvancedOddsOfHitting.get_odds_of_hitting_4g(eal, ShotType.SINGLE)
        roll = random.randint(0, 99)
        
        if roll > odds:
            return [[ShotResult(hit=False, eal=eal, odds=odds, roll=roll)] if i == primary_target_idx else [] for i in range(len(targets))]

        results = CombatSimulatorUtils.process_shotgun_pattern(
            ammo, targets, ranges, exposures, shot_params_list, is_front_shots, data.base_pellet_hit_chance
        )
        
        if not results[primary_target_idx]:
            results[primary_target_idx] = [ShotResult(hit=False, eal=eal, odds=odds, roll=roll)]
        
        return results

    @staticmethod
    def burst_fire(
        shooter: Character,
        weapon: Weapon,
        ammo: AmmoType,
        target_group: TargetGroup,
        arc_of_fire: Optional[float] = None,
        continuous_burst_impulses: int = 0
    ) -> dict[Character, list[ShotResult]]:
        """Simulate automatic burst fire."""
        sab_penalty, arc_of_fire = CombatSimulatorUtils.setup_burst_fire(
            weapon, target_group, continuous_burst_impulses, arc_of_fire, shooter
        )

        target_hits: List[tuple[int, int, Character, int, TargetExposure, ShotParameters, bool]] = []

        for idx, (target, rng, exposure, shot_params, front) in enumerate(zip(
            target_group.targets, target_group.ranges, target_group.exposures,
            target_group.shot_params_list, target_group.is_front_shots
        )):
            result = CombatSimulatorUtils.check_burst_elevation_and_get_hits(
                shooter, target, weapon, rng, exposure, shot_params, arc_of_fire, sab_penalty
            )

            if result.hit and result.hits > 0:
                target_hits.append((idx, result.hits, target, rng, exposure, shot_params, front))
        
        target_hits = CombatSimulatorUtils.redistribute_hits_by_eal(
            shooter, weapon, target_hits, sab_penalty
        )
        
        character_results = defaultdict(list)
        for idx, hits, target, rng, exposure, shot_params, front in target_hits:
            results = CombatSimulatorUtils.process_target_hits(
                target, ammo, rng, exposure, shot_params, front, hits
            )
            character_results[target].extend(results)
        
        return dict(character_results)

    @staticmethod
    def three_round_burst(
        shooter: Character,
        target: Character,
        weapon: Weapon,
        ammo: AmmoType,
        range_hexes: int,
        target_exposure: TargetExposure,
        shot_params: ShotParameters,
        is_front_shot: bool
    ) -> List[ShotResult]:
        """Simulate a three round burst from shooter to target."""
        if not weapon.ballistic_data:
            raise ValueError("Weapon must have ballistic_data for three round burst")
        rb3_value = weapon.ballistic_data.get_three_round_burst(range_hexes)
        if rb3_value is None:
            raise ValueError("Weapon must have three_round_burst data")
        eal = CombatSimulatorUtils.calculate_eal(
            shooter, target, weapon, range_hexes, target_exposure, shot_params
        )
        hits = ThreeRoundBurstTable.calculate_3rb_hits(eal, rb3_value)
        if hits == 0:
            return [ShotResult(hit=False, eal=eal, odds=0, roll=0)]
        results = []
        for _ in range(hits):
            damage_result, incap_effect, recovery, incap_time = CombatSimulatorUtils.process_hit(
                target, ammo, range_hexes, target_exposure, shot_params, is_front_shot
            )
            results.append(ShotResult(
                hit=True,
                eal=eal,
                odds=100,
                roll=0,
                damage_result=damage_result,
                incapacitation_effect=incap_effect,
                recovery=recovery,
                incapacitation_time_phases=incap_time
            ))
        return results

    @staticmethod
    def shotgun_burst_fire(
            shooter: Character,
            weapon: Weapon,
            ammo: AmmoType,
            primary_target_group: TargetGroup,
            pattern_target_groups: list[TargetGroup],
            arc_of_fire: Optional[float] = None,
            continuous_burst_impulses: int = 0,
    ) -> dict[Character, list[ShotResult]]:
        """Simulate fully automatic shotgun burst with patterns hitting multiple targets."""
        sab_penalty, arc_of_fire = CombatSimulatorUtils.setup_burst_fire(
            weapon, primary_target_group, continuous_burst_impulses, arc_of_fire, shooter
        )

        pattern_hits: list[
            tuple[int, int, Character, int, TargetExposure, ShotParameters, bool]
        ] = []

        for idx, (target, rng, exposure, params, front) in enumerate(
            zip(
                primary_target_group.targets,
                primary_target_group.ranges,
                primary_target_group.exposures,
                primary_target_group.shot_params_list,
                primary_target_group.is_front_shots,
            )
        ):
            data = CombatSimulatorUtils.get_shotgun_data_at_range(ammo, rng)
            
            result = CombatSimulatorUtils.check_shotgun_burst_elevation_and_get_hits(
                shooter, target, weapon, rng, exposure, params, arc_of_fire, sab_penalty,
                data.shotgun_accuracy_level_modifier
            )
            
            if result.hit and result.hits > 0:
                pattern_hits.append((idx, result.hits, target, rng, exposure, params, front))

        pattern_hits = CombatSimulatorUtils.redistribute_hits_by_eal(
            shooter, weapon, pattern_hits, sab_penalty
        )

        character_results = defaultdict(list)

        for primary_idx, patterns, target, rng, exposure, params, front in pattern_hits:
            pattern_group = pattern_target_groups[primary_idx]

            all_targets = [target] + pattern_group.targets
            all_ranges = [rng] + pattern_group.ranges
            all_exposures = [exposure] + pattern_group.exposures
            all_params = [params] + pattern_group.shot_params_list
            all_fronts = [front] + pattern_group.is_front_shots

            data = CombatSimulatorUtils.get_shotgun_data_at_range(ammo, rng)

            for _ in range(patterns):
                pattern_result = CombatSimulatorUtils.process_shotgun_pattern(
                    ammo, all_targets, all_ranges, all_exposures, all_params, all_fronts,
                    data.base_pellet_hit_chance
                )
                for char, results in zip(all_targets, pattern_result):
                    character_results[char].extend(results)

        return dict(character_results)

    @staticmethod
    def explosive_weapon_shot(
        shooter: Character,
        weapon: Weapon,
        ammo: AmmoType,
        range_hexes: int,
        target: ExplosiveTarget,
        shot_params: ShotParameters
    ) -> ExplosiveShotResult:
        """Simulate explosive weapon shot at hex, window, or door."""
        target_size_alm = target.value
        
        eal = CombatSimulatorUtils.calculate_explosive_eal(
            shooter, weapon, range_hexes, target_size_alm, shot_params
        )
        
        odds = Table4AdvancedOddsOfHitting.get_odds_of_hitting_4g(eal, ShotType.SINGLE)
        roll = random.randint(0, 99)
        
        if roll <= odds:
            return ExplosiveShotResult(hit=True, eal=eal, odds=odds, roll=roll, scatter_hexes=0)
        
        eal_diff = 0
        for test_eal in range(eal + 1, 29):
            test_odds = Table4AdvancedOddsOfHitting.get_odds_of_hitting_4g(test_eal, ShotType.SINGLE)
            if test_odds > roll:
                eal_diff = test_eal - eal
                break
        
        scatter_hexes = Table5AutoPelletShrapnel.get_scatter_distance_5c(eal_diff)
        
        if scatter_hexes == 1:
            is_long = random.randint(1, 6) > 3
        else:
            is_long = random.randint(0, 9) >= 5
        
        return ExplosiveShotResult(
            hit=False, eal=eal, odds=odds, roll=roll,
            scatter_hexes=scatter_hexes, is_long=is_long
        )

    @staticmethod
    def thrown_grenade(
        shooter: Character,
        range_hexes: int,
        target: ExplosiveTarget,
        aim_time_ac: int,
        situation_stance_modifiers: List,
        visibility_modifiers: List
    ) -> ExplosiveShotResult:
        """Simulate thrown grenade at hex, window, or door."""
        target_size_alm = target.value
        aim_alm = Table4AdvancedOddsOfHitting.get_thrown_grenade_aim_alm_4h(aim_time_ac)
        
        eal = CombatSimulatorUtils.calculate_grenade_eal(
            shooter, range_hexes, target_size_alm, aim_alm,
            situation_stance_modifiers, visibility_modifiers
        )
        
        odds = Table4AdvancedOddsOfHitting.get_odds_of_hitting_4g(eal, ShotType.SINGLE)
        roll = random.randint(0, 99)
        
        if roll <= odds:
            return ExplosiveShotResult(hit=True, eal=eal, odds=odds, roll=roll, scatter_hexes=0)
        
        eal_diff = 0
        for test_eal in range(eal + 1, 29):
            test_odds = Table4AdvancedOddsOfHitting.get_odds_of_hitting_4g(test_eal, ShotType.SINGLE)
            if test_odds > roll:
                eal_diff = test_eal - eal
                break
        
        scatter_hexes = Table5AutoPelletShrapnel.get_scatter_distance_5c(eal_diff)

        is_long = random.randint(0, 9) >= 5
        
        return ExplosiveShotResult(
            hit=False, eal=eal, odds=odds, roll=roll,
            scatter_hexes=scatter_hexes, is_long=is_long
        )

    @staticmethod
    def automatic_grenade_launcher_burst(
        shooter: Character,
        weapon: Weapon,
        range_hexes: int,
        target: ExplosiveTarget,
        shot_params: ShotParameters,
        arc_of_fire: Optional[float] = None,
        continuous_burst_impulses: int = 0
    ) -> List[ExplosiveShotResult]:
        """Simulate automatic grenade launcher burst."""
        
        sab_penalty = 0
        if continuous_burst_impulses > 0:
            if not weapon.sustained_auto_burst:
                raise ValueError("Weapon must have sustained_auto_burst")
            sab_penalty = continuous_burst_impulses * weapon.sustained_auto_burst
        
        min_arc = weapon.ballistic_data.get_minimum_arc(range_hexes)
        if min_arc is None:
            raise ValueError("Weapon must have minimum_arc")
        
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
        
        final_arc = max(arc_of_fire, effective_ma) if arc_of_fire is not None else effective_ma
        
        target_size_alm = target.value
        eal = CombatSimulatorUtils.calculate_explosive_eal(
            shooter, weapon, range_hexes, target_size_alm, shot_params
        ) - sab_penalty
        
        odds = Table4AdvancedOddsOfHitting.get_odds_of_hitting_4g(eal, ShotType.BURST)
        roll = random.randint(0, 99)
        
        if roll > odds:
            return [ExplosiveShotResult(hit=False, eal=eal, odds=odds, roll=roll, scatter_hexes=0)]
        
        hits = Table5AutoPelletShrapnel.get_fire_table_value5a(
            final_arc, weapon.full_auto_rof, 0
        )
        
        results = []

        is_long = random.randint(0, 9) >= 5

        for _ in range(hits):
            hit_roll = random.randint(0, 99)
            if hit_roll <= odds:
                results.append(ExplosiveShotResult(hit=True, eal=eal, odds=odds, roll=hit_roll, scatter_hexes=0))
            else:
                eal_diff = 0
                for test_eal in range(eal + 1, 29):
                    test_odds = Table4AdvancedOddsOfHitting.get_odds_of_hitting_4g(test_eal, ShotType.SINGLE)
                    if test_odds > hit_roll:
                        eal_diff = test_eal - eal
                        break
                
                scatter_hexes = Table5AutoPelletShrapnel.get_scatter_distance_5c(eal_diff)
                

                results.append(ExplosiveShotResult(
                    hit=False, eal=eal, odds=odds, roll=hit_roll,
                    scatter_hexes=scatter_hexes, is_long=is_long
                ))
        
        return results
