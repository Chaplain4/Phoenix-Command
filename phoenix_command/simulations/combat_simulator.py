"""Combat simulation for Phoenix Command."""

import random
from typing import Optional, List

from phoenix_command.models.character import Character
from phoenix_command.models.enums import ShotType, TargetExposure, ExplosiveTarget, SituationStanceModifier4B, BlastModifier
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
        log = []
        log.append("=== SINGLE SHOT ===")
        log.append(f"Shooter: {shooter.name}, Target: {target.name}")
        log.append(f"Weapon: {weapon.name}, Ammo: {ammo.name}")
        log.append(f"Range: {range_hexes} hexes, Exposure: {target_exposure.name}")
        
        eal = CombatSimulatorUtils.calculate_eal(
            shooter, target, weapon, range_hexes, target_exposure, shot_params, log=log
        )
        
        odds = Table4AdvancedOddsOfHitting.get_odds_of_hitting_4g(eal, ShotType.SINGLE)
        roll = random.randint(0, 99)
        hit = roll <= odds
        
        log.append(f"[Hit Check] EAL: {eal}, Odds: {odds}%, Roll: {roll}")
        log.append(f"  Result: {'HIT!' if hit else 'MISS'}")
        
        if not hit:
            return ShotResult(hit=False, eal=eal, odds=odds, roll=roll, target=target, log="\n".join(log))
        
        damage_result, incap_effect, recovery, incap_time = CombatSimulatorUtils.process_hit(
            target, ammo, range_hexes, target_exposure, shot_params, is_front_shot, log
        )
        
        return ShotResult(
            hit=True,
            eal=eal,
            odds=odds,
            roll=roll,
            target=target,
            damage_result=damage_result,
            incapacitation_effect=incap_effect,
            recovery=recovery,
            incapacitation_time_phases=incap_time,
            log="\n".join(log)
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
    ) -> List[ShotResult]:
        """Simulate shotgun shot with pattern hitting multiple targets."""
        log = []
        log.append("=== SHOTGUN SHOT ===")
        log.append(f"Shooter: {shooter.name}, Targets: {[t.name for t in targets]}")
        log.append(f"Primary target: {targets[primary_target_idx].name}")
        
        CombatSimulatorUtils.validate_shotgun_inputs(targets, ranges, exposures, shot_params_list, is_front_shots)
        
        primary_range = ranges[primary_target_idx]
        primary_exposure = exposures[primary_target_idx]
        primary_params = shot_params_list[primary_target_idx]
        
        data = CombatSimulatorUtils.get_shotgun_data_at_range(ammo, primary_range)
        log.append(f"Range: {primary_range}, SALM: {data.shotgun_accuracy_level_modifier}, BPHC: {data.base_pellet_hit_chance}")

        if data.shotgun_accuracy_level_modifier is None:
            log.append("No SALM at range, treating as single shot")
            result = CombatSimulator.single_shot(
                shooter, targets[primary_target_idx], weapon, ammo,
                primary_range, primary_exposure, primary_params, is_front_shots[primary_target_idx]
            )
            return [result]

        eal = CombatSimulatorUtils.calculate_shotgun_eal(
            shooter, targets[primary_target_idx], weapon, primary_range,
            primary_exposure, primary_params, data.shotgun_accuracy_level_modifier, 0, log
        )
        
        odds = Table4AdvancedOddsOfHitting.get_odds_of_hitting_4g(eal, ShotType.SINGLE)
        roll = random.randint(0, 99)
        
        log.append(f"[Pattern Hit Check] EAL: {eal}, Odds: {odds}%, Roll: {roll}")
        
        if roll > odds:
            log.append("  Pattern MISSED")
            return [ShotResult(hit=False, eal=eal, odds=odds, roll=roll, target=targets[primary_target_idx], log="\n".join(log))]

        log.append("  Pattern HIT, processing pellets...")
        
        results = CombatSimulatorUtils.process_shotgun_pattern(
            ammo, targets, ranges, exposures, shot_params_list, is_front_shots, data.base_pellet_hit_chance, log
        )
        
        if not results:
            results = [ShotResult(hit=False, eal=eal, odds=odds, roll=roll, target=targets[primary_target_idx], log="\n".join(log))]
        else:
            if results[0].log:
                results[0] = ShotResult(
                    hit=results[0].hit, eal=eal, odds=odds, roll=roll,
                    target=results[0].target, damage_result=results[0].damage_result,
                    incapacitation_effect=results[0].incapacitation_effect,
                    recovery=results[0].recovery,
                    incapacitation_time_phases=results[0].incapacitation_time_phases,
                    log="\n".join(log) + "\n" + results[0].log
                )
        
        return results

    @staticmethod
    def burst_fire(
        shooter: Character,
        weapon: Weapon,
        ammo: AmmoType,
        target_group: TargetGroup,
        arc_of_fire: Optional[float] = None,
        continuous_burst_impulses: int = 0
    ) -> List[ShotResult]:
        """Simulate automatic burst fire."""
        log = ["=== BURST FIRE ===", f"Shooter: {shooter.name}, Weapon: {weapon.name}",
               f"Targets: {[t.name for t in target_group.targets]}"]

        sab_penalty, arc_of_fire = CombatSimulatorUtils.setup_burst_fire(
            weapon, target_group, continuous_burst_impulses, arc_of_fire, shooter, log
        )

        # Store tuples with (idx, hits, target, rng, exposure, shot_params, front, eal, odds, roll)
        target_hits: List[tuple[int, int, Character, int, TargetExposure, ShotParameters, bool, int, int, int]] = []
        # Store miss results for targets that failed elevation check
        miss_results: List[tuple[Character, int, int, int]] = []  # (target, eal, odds, roll)

        for idx, (target, rng, exposure, shot_params, front) in enumerate(zip(
            target_group.targets, target_group.ranges, target_group.exposures,
            target_group.shot_params_list, target_group.is_front_shots
        )):
            result = CombatSimulatorUtils.check_burst_elevation_and_get_hits(
                shooter, target, weapon, rng, exposure, shot_params, arc_of_fire, sab_penalty, log
            )

            if result.hit and result.hits > 0:
                target_hits.append((idx, result.hits, target, rng, exposure, shot_params, front, result.eal, result.odds, result.roll))
            else:
                # Store miss with actual eal, odds, roll values
                miss_results.append((target, result.eal, result.odds, result.roll))

        # Redistribute hits if needed (keeping eal, odds, roll)
        if target_hits:
            total_hits = sum(h[1] for h in target_hits)
            if total_hits > weapon.full_auto_rof:
                log.append(f"[Redistribute] Total hits {total_hits} > ROF {weapon.full_auto_rof}, redistributing...")
                total_eal = sum(h[7] for h in target_hits)
                redistributed = []
                remaining_rof = weapon.full_auto_rof
                for i, (idx, hits, target, rng, exposure, shot_params, front, eal, odds, roll) in enumerate(target_hits):
                    if i == len(target_hits) - 1:
                        new_hits = remaining_rof
                    else:
                        proportion = eal / total_eal if total_eal > 0 else 1.0 / len(target_hits)
                        new_hits = max(1, int(weapon.full_auto_rof * proportion))
                        remaining_rof -= new_hits
                    log.append(f"  Target {target.name}: {hits} -> {new_hits} hits")
                    redistributed.append((idx, new_hits, target, rng, exposure, shot_params, front, eal, odds, roll))
                target_hits = redistributed

        results = []
        for idx, hits, target, rng, exposure, shot_params, front, eal, odds, roll in target_hits:
            hit_results = CombatSimulatorUtils.process_target_hits(
                target, ammo, rng, exposure, shot_params, front, hits, log,
                eal=eal, odds=odds, roll=roll
            )
            results.extend(hit_results)
        
        # Add header log to first result or create miss results
        if results:
            results[0] = ShotResult(
                hit=results[0].hit, eal=results[0].eal, odds=results[0].odds, roll=results[0].roll,
                target=results[0].target, damage_result=results[0].damage_result,
                incapacitation_effect=results[0].incapacitation_effect,
                recovery=results[0].recovery,
                incapacitation_time_phases=results[0].incapacitation_time_phases,
                log="\n".join(log) + "\n" + (results[0].log or "")
            )
        else:
            # Create miss results with actual eal, odds, roll for each target
            log.append("No targets hit")
            for target, eal, odds, roll in miss_results:
                results.append(ShotResult(
                    hit=False, eal=eal, odds=odds, roll=roll,
                    target=target, log="\n".join(log) if not results else None
                ))
        return results

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
        log = ["=== THREE ROUND BURST ===", f"Shooter: {shooter.name}, Target: {target.name}",
               f"Weapon: {weapon.name}, Range: {range_hexes}"]

        if not weapon.ballistic_data:
            raise ValueError("Weapon must have ballistic_data for three round burst")
        rb3_value = weapon.ballistic_data.get_three_round_burst(range_hexes)
        if rb3_value is None:
            raise ValueError("Weapon must have three_round_burst data")
        
        log.append(f"3RB value: {rb3_value}")
        
        eal = CombatSimulatorUtils.calculate_eal(
            shooter, target, weapon, range_hexes, target_exposure, shot_params, log=log
        )
        
        # Get hit chances from table to record odds (chance to hit at least once)
        available_3rb = sorted(ThreeRoundBurstTable.TABLE_9B.keys())
        target_3rb = min(available_3rb, key=lambda x: abs(x - rb3_value))
        target_eal = max(3, min(28, eal))
        chances = ThreeRoundBurstTable.TABLE_9B[target_3rb][target_eal]
        odds = chances[0]
        hits, roll = ThreeRoundBurstTable.calculate_3rb_hits(eal, rb3_value, log)
        log.append(f"[3RB Result] EAL: {eal}, Odds (1+ hit): {odds}%, Roll: {roll}, Hits: {hits}")
        if hits == 0:
            log.append("  No hits")
            return [ShotResult(hit=False, eal=eal, odds=odds, roll=roll, target=target, log="\n".join(log))]
        results = []
        for i in range(hits):
            hit_log = [f"--- 3RB Hit {i+1}/{hits} ---"]
            damage_result, incap_effect, recovery, incap_time = CombatSimulatorUtils.process_hit(
                target, ammo, range_hexes, target_exposure, shot_params, is_front_shot, hit_log
            )
            log.extend(hit_log)
            results.append(ShotResult(
                hit=True,
                eal=eal,
                odds=odds,
                roll=roll,
                target=target,
                damage_result=damage_result,
                incapacitation_effect=incap_effect,
                recovery=recovery,
                incapacitation_time_phases=incap_time,
                log="\n".join(hit_log)
            ))
        
        # Add header log to first result
        if results:
            results[0] = ShotResult(
                hit=results[0].hit, eal=results[0].eal, odds=results[0].odds, roll=results[0].roll,
                target=results[0].target, damage_result=results[0].damage_result,
                incapacitation_effect=results[0].incapacitation_effect,
                recovery=results[0].recovery,
                incapacitation_time_phases=results[0].incapacitation_time_phases,
                log="\n".join(log)
            )
        
        return results

    @staticmethod
    def shotgun_burst_fire(
            shooter: Character,
            weapon: Weapon,
            ammo: AmmoType,
            primary_target_group: TargetGroup,
            pattern_target_groups: List[TargetGroup],
            arc_of_fire: Optional[float] = None,
            continuous_burst_impulses: int = 0,
    ) -> List[ShotResult]:
        """Simulate fully automatic shotgun burst with patterns hitting multiple targets."""
        log = ["=== SHOTGUN BURST FIRE ===", f"Shooter: {shooter.name}, Weapon: {weapon.name}"]

        sab_penalty, arc_of_fire = CombatSimulatorUtils.setup_burst_fire(
            weapon, primary_target_group, continuous_burst_impulses, arc_of_fire, shooter, log
        )

        pattern_hits: List[
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
                data.shotgun_accuracy_level_modifier, log
            )
            
            if result.hit and result.hits > 0:
                pattern_hits.append((idx, result.hits, target, rng, exposure, params, front))

        pattern_hits = CombatSimulatorUtils.redistribute_hits_by_eal(
            shooter, weapon, pattern_hits, sab_penalty, log
        )

        results = []

        for primary_idx, patterns, target, rng, exposure, params, front in pattern_hits:
            pattern_group = pattern_target_groups[primary_idx]

            all_targets = [target] + pattern_group.targets
            all_ranges = [rng] + pattern_group.ranges
            all_exposures = [exposure] + pattern_group.exposures
            all_params = [params] + pattern_group.shot_params_list
            all_fronts = [front] + pattern_group.is_front_shots

            data = CombatSimulatorUtils.get_shotgun_data_at_range(ammo, rng)

            for pattern_num in range(patterns):
                log.append(f"--- Pattern {pattern_num+1}/{patterns} at {target.name} ---")
                pattern_results = CombatSimulatorUtils.process_shotgun_pattern(
                    ammo, all_targets, all_ranges, all_exposures, all_params, all_fronts,
                    data.base_pellet_hit_chance, log
                )
                results.extend(pattern_results)

        # Add header log to first result or create miss result
        if results:
            results[0] = ShotResult(
                hit=results[0].hit, eal=results[0].eal, odds=results[0].odds, roll=results[0].roll,
                target=results[0].target, damage_result=results[0].damage_result,
                incapacitation_effect=results[0].incapacitation_effect,
                recovery=results[0].recovery,
                incapacitation_time_phases=results[0].incapacitation_time_phases,
                log="\n".join(log) + "\n" + (results[0].log or "")
            )
        else:
            log.append("No targets hit")
            results = [ShotResult(hit=False, eal=0, odds=0, roll=0, target=primary_target_group.targets[0], log="\n".join(log))]

        return results

    @staticmethod
    def explosive_weapon_shot(
        shooter: Character,
        weapon: Weapon,
        range_hexes: int,
        target: ExplosiveTarget,
        shot_params: ShotParameters
    ) -> ExplosiveShotResult:
        """Simulate explosive weapon shot at hex, window, or door."""
        log = ["=== EXPLOSIVE WEAPON SHOT ===", f"Shooter: {shooter.name}, Weapon: {weapon.name}",
               f"Target: {target.name}, Range: {range_hexes}"]

        target_size_alm = target.value
        
        eal = CombatSimulatorUtils.calculate_explosive_eal(
            shooter, weapon, range_hexes, target_size_alm, shot_params, log
        )
        
        odds = Table4AdvancedOddsOfHitting.get_odds_of_hitting_4g(eal, ShotType.SINGLE)
        roll = random.randint(0, 99)
        
        log.append(f"[Hit Check] EAL: {eal}, Odds: {odds}%, Roll: {roll}")
        
        if roll <= odds:
            log.append("  Direct HIT!")
            return ExplosiveShotResult(hit=True, eal=eal, odds=odds, roll=roll, scatter_hexes=0)
        
        log.append("  MISS, calculating scatter...")
        
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
        
        log.append(f"  EAL diff: {eal_diff}, Scatter: {scatter_hexes} hexes, Long: {is_long}")
        
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
        log = ["=== THROWN GRENADE ===", f"Thrower: {shooter.name}, Range: {range_hexes}",
               f"Target: {target.name}, Aim time: {aim_time_ac} AC"]

        target_size_alm = target.value
        aim_alm = Table4AdvancedOddsOfHitting.get_thrown_grenade_aim_alm_4h(aim_time_ac)
        
        log.append(f"Aim ALM (Table 4H): {aim_alm}")
        
        eal = CombatSimulatorUtils.calculate_grenade_eal(
            shooter, range_hexes, target_size_alm, aim_alm,
            situation_stance_modifiers, visibility_modifiers, log
        )
        
        odds = Table4AdvancedOddsOfHitting.get_odds_of_hitting_4g(eal, ShotType.SINGLE)
        roll = random.randint(0, 99)
        
        log.append(f"[Hit Check] EAL: {eal}, Odds: {odds}%, Roll: {roll}")
        
        if roll <= odds:
            log.append("  Direct HIT!")
            return ExplosiveShotResult(hit=True, eal=eal, odds=odds, roll=roll, scatter_hexes=0)
        
        log.append("  MISS, calculating scatter...")
        
        eal_diff = 0
        for test_eal in range(eal + 1, 29):
            test_odds = Table4AdvancedOddsOfHitting.get_odds_of_hitting_4g(test_eal, ShotType.SINGLE)
            if test_odds > roll:
                eal_diff = test_eal - eal
                break
        
        scatter_hexes = Table5AutoPelletShrapnel.get_scatter_distance_5c(eal_diff)
        is_long = random.randint(0, 9) >= 5
        
        log.append(f"  EAL diff: {eal_diff}, Scatter: {scatter_hexes} hexes, Long: {is_long}")
        
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
        log = ["=== AUTO GRENADE LAUNCHER BURST ===", f"Shooter: {shooter.name}, Weapon: {weapon.name}",
               f"Target: {target.name}, Range: {range_hexes}"]

        sab_penalty = 0
        if continuous_burst_impulses > 0:
            if not weapon.sustained_auto_burst:
                raise ValueError("Weapon must have sustained_auto_burst")
            sab_penalty = continuous_burst_impulses * weapon.sustained_auto_burst
        
        log.append(f"Continuous impulses: {continuous_burst_impulses}, SAB penalty: {sab_penalty}")
        
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
        log.append(f"Min arc: {min_arc}, Effective MA: {effective_ma}, Final arc: {final_arc}")
        
        target_size_alm = target.value
        eal = CombatSimulatorUtils.calculate_explosive_eal(
            shooter, weapon, range_hexes, target_size_alm, shot_params, log
        ) - sab_penalty
        
        log.append(f"EAL after SAB: {eal}")
        
        odds = Table4AdvancedOddsOfHitting.get_odds_of_hitting_4g(eal, ShotType.BURST)
        roll = random.randint(0, 99)
        
        log.append(f"[Elevation Check] Odds: {odds}%, Roll: {roll}")
        
        if roll > odds:
            log.append("  Burst MISSED")
            return [ExplosiveShotResult(hit=False, eal=eal, odds=odds, roll=roll, scatter_hexes=0)]
        
        hits = Table5AutoPelletShrapnel.get_fire_table_value5a(
            final_arc, weapon.full_auto_rof, 0, log
        )
        
        log.append(f"  Burst HIT, grenades on target: {hits}")
        
        results = []
        is_long = random.randint(0, 9) >= 5

        for i in range(hits):
            hit_roll = random.randint(0, 99)
            log.append(f"--- Grenade {i+1}/{hits}, Roll: {hit_roll} ---")
            
            if hit_roll <= odds:
                log.append("  Direct hit!")
                results.append(ExplosiveShotResult(hit=True, eal=eal, odds=odds, roll=hit_roll, scatter_hexes=0))
            else:
                eal_diff = 0
                for test_eal in range(eal + 1, 29):
                    test_odds = Table4AdvancedOddsOfHitting.get_odds_of_hitting_4g(test_eal, ShotType.SINGLE)
                    if test_odds > hit_roll:
                        eal_diff = test_eal - eal
                        break
                
                scatter_hexes = Table5AutoPelletShrapnel.get_scatter_distance_5c(eal_diff)
                log.append(f"  Scatter: {scatter_hexes} hexes, Long: {is_long}")

                results.append(ExplosiveShotResult(
                    hit=False, eal=eal, odds=odds, roll=hit_roll,
                    scatter_hexes=scatter_hexes, is_long=is_long
                ))
        
        return results

    @staticmethod
    def explosion_damage(
        ammo: AmmoType,
        targets: List[Character],
        ranges_from_burst: List[int],
        exposures: List[TargetExposure],
        shot_params_list: List[ShotParameters],
        is_front_shots: List[bool],
        blast_modifiers: List[List[BlastModifier]]
    ) -> List[ShotResult]:
        """Calculate explosive damage (shrapnel + concussion) for multiple targets."""
        log = ["=== EXPLOSION DAMAGE ===", f"Ammo: {ammo.name}, Targets: {len(targets)}"]

        if not (len(targets) == len(ranges_from_burst) == len(exposures) ==
                len(shot_params_list) == len(is_front_shots) == len(blast_modifiers)):
            raise ValueError("All input lists must have the same length")

        if not ammo.explosive_data:
            raise ValueError("Ammo must have explosive_data for explosion damage")

        results = []

        for target, range_hex, exposure, params, front, modifiers in zip(
            targets, ranges_from_burst, exposures, shot_params_list, is_front_shots, blast_modifiers
        ):
            log.append(f"\n--- Target: {target.name}, Range: {range_hex} ---")
            
            bshc = ammo.get_base_shrapnel_hit_chance(range_hex)
            base_concussion = ammo.get_base_concussion(range_hex)
            
            log.append(f"  BSHC: {bshc}, Base concussion: {base_concussion}")

            # Process shrapnel hits
            if bshc is not None:
                shrapnel_results = CombatSimulatorUtils.process_shrapnel_hits(
                    target, ammo, range_hex, exposure, params, front, bshc, log
                )
                results.extend(shrapnel_results)

            # Process concussion damage
            if base_concussion is not None and base_concussion > 0:
                concussion_result = CombatSimulatorUtils.process_concussion_damage(
                    target, base_concussion, modifiers, log
                )
                if concussion_result is not None:
                    results.append(concussion_result)

        # Add header log to first result or create empty result
        if results:
            results[0] = ShotResult(
                hit=results[0].hit, eal=results[0].eal, odds=results[0].odds, roll=results[0].roll,
                target=results[0].target, damage_result=results[0].damage_result,
                incapacitation_effect=results[0].incapacitation_effect,
                recovery=results[0].recovery,
                incapacitation_time_phases=results[0].incapacitation_time_phases,
                log="\n".join(log) + "\n" + (results[0].log or "")
            )

        return results
