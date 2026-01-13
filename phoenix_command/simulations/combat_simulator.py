"""Combat simulation for Phoenix Command."""

import random
from typing import Optional, List

from phoenix_command.models.character import Character
from phoenix_command.models.enums import ShotType, TargetExposure
from phoenix_command.models.gear import Weapon, AmmoType
from phoenix_command.models.hit_result_advanced import ShotParameters, ShotResult, TargetGroup
from phoenix_command.simulations.combat_simulator_utils import CombatSimulatorUtils
from phoenix_command.tables.core.table4_advanced_odds_of_hitting import Table4AdvancedOddsOfHitting


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
        from collections import defaultdict
        
        sab_penalty, arc_of_fire = CombatSimulatorUtils.setup_burst_fire(
            weapon, target_group, continuous_burst_impulses, arc_of_fire
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
        from collections import defaultdict
        
        sab_penalty, arc_of_fire = CombatSimulatorUtils.setup_burst_fire(
            weapon, primary_target_group, continuous_burst_impulses, arc_of_fire
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
