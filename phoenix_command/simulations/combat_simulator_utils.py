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
            sab_penalty: int,
            log: List[str]
    ) -> List[tuple[int, int, Character, int, TargetExposure, ShotParameters, bool]]:
        """Redistribute hits proportionally by EAL if total exceeds weapon ROF."""
        total_hits = sum(h[1] for h in target_hits)
        if total_hits <= weapon.full_auto_rof:
            log.append(f"[Redistribute] Total hits {total_hits} <= ROF {weapon.full_auto_rof}, no redistribution needed")
            return target_hits

        log.append(f"[Redistribute] Total hits {total_hits} > ROF {weapon.full_auto_rof}, redistributing...")

        # Calculate EAL for each target
        target_eals = []
        for idx, hits, target, rng, exposure, shot_params, front in target_hits:
            eal = CombatSimulatorUtils.calculate_eal(
                shooter, target, weapon, rng, exposure, shot_params,
                AccuracyModifiers.AUTO_ELEV, []  # Empty log for internal calculation
            ) - sab_penalty
            target_eals.append(eal)
            log.append(f"  Target {target.name}: EAL={eal}")

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

            log.append(f"  Target {target.name}: {hits} -> {new_hits} hits")
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
            salm: Optional[int],
            log: List[str]
    ) -> BurstElevationResult:
        """Check elevation for shotgun burst and get hits."""
        log.append(f"[Shotgun Burst Elevation] Target: {target.name}, Range: {range_hexes}, SALM: {salm}")

        if salm is not None:
            eal = CombatSimulatorUtils.calculate_shotgun_eal(
                shooter, target, weapon, range_hexes, exposure, shot_params, salm, sab_penalty, log
            )
        else:
            eal = CombatSimulatorUtils.calculate_eal(
                shooter, target, weapon, range_hexes, exposure, shot_params, AccuracyModifiers.AUTO_ELEV, log
            ) - sab_penalty
            log.append(f"  SAB penalty: -{sab_penalty}, Final EAL: {eal}")

        return CombatSimulatorUtils.check_elevation_and_calculate_hits(eal, exposure, weapon, arc_of_fire, log)

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
            sab_penalty: int = 0,
            log: List[str] = None
    ) -> int:
        """Calculate EAL for shotgun using larger of Target Size ALM or SALM."""
        if log is None:
            log = []

        target_size_alm = Table4AdvancedOddsOfHitting.get_standard_target_size_modifier_4e(
            exposure, AccuracyModifiers.AUTO_ELEV if sab_penalty else AccuracyModifiers.TARGET_SIZE
        )
        eal_base = CombatSimulatorUtils.calculate_eal(
            shooter, target, weapon, range_hexes, exposure, shot_params,
            AccuracyModifiers.AUTO_ELEV if sab_penalty else AccuracyModifiers.TARGET_SIZE, log
        )

        effective_size_alm = max(target_size_alm, salm)
        result = (eal_base - sab_penalty) - target_size_alm + effective_size_alm

        log.append(f"[Shotgun EAL] Base EAL: {eal_base}, Target Size ALM: {target_size_alm}, SALM: {salm}")
        log.append(f"  Using max({target_size_alm}, {salm}) = {effective_size_alm}")
        log.append(f"  SAB penalty: {sab_penalty}, Final EAL: {result}")

        return result

    @staticmethod
    def check_burst_elevation_and_get_hits(
            shooter: Character,
            target: Character,
            weapon: Weapon,
            range_hexes: int,
            exposure: TargetExposure,
            shot_params: ShotParameters,
            arc_of_fire: float,
            sab_penalty: int,
            log: List[str]
    ) -> BurstElevationResult:
        """Check elevation and calculate hits for burst fire."""
        log.append(f"[Burst Elevation] Target: {target.name}, Range: {range_hexes}")

        eal = CombatSimulatorUtils.calculate_eal(
            shooter, target, weapon, range_hexes, exposure, shot_params,
            AccuracyModifiers.AUTO_ELEV, log
        ) - sab_penalty

        log.append(f"  SAB penalty: -{sab_penalty}, Final EAL: {eal}")

        return CombatSimulatorUtils.check_elevation_and_calculate_hits(eal, exposure, weapon, arc_of_fire, log)

    @staticmethod
    def setup_burst_fire(
            weapon: Weapon,
            target_group: TargetGroup,
            continuous_burst_impulses: int,
            arc_of_fire: Optional[float],
            shooter: Character,
            log: List[str]
    ) -> tuple[int, float]:
        """Setup burst fire parameters and return SAB penalty and arc of fire."""
        from phoenix_command.tables.advanced_rules.effective_min_arc import EffectiveMinimumArc
        
        log.append(f"[Burst Fire Setup] Weapon: {weapon.name}, ROF: {weapon.full_auto_rof}")

        sab_penalty, min_arc = CombatSimulatorUtils.validate_burst_fire_inputs(
            weapon, target_group.targets, target_group.ranges, target_group.exposures,
            target_group.shot_params_list, target_group.is_front_shots, continuous_burst_impulses
        )
        
        log.append(f"  Continuous burst impulses: {continuous_burst_impulses}, SAB penalty: {sab_penalty}")
        log.append(f"  Minimum arc from weapon: {min_arc}")

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
        
        log.append(f"  Stance: {stance}, Moving: {is_moving}, Effective MA: {effective_ma}")

        final_arc = max(arc_of_fire, effective_ma) if arc_of_fire is not None else effective_ma
        log.append(f"  Requested arc: {arc_of_fire}, Final arc of fire: {final_arc}")

        return sab_penalty, final_arc

    @staticmethod
    def calculate_eal(
        shooter: Character,
        target: Character,
        weapon: Weapon,
        range_hexes: int,
        target_exposure: TargetExposure,
        shot_params: ShotParameters,
        target_size_modifier_type: AccuracyModifiers = AccuracyModifiers.TARGET_SIZE,
        log: List[str] = None
    ) -> int:
        """Calculate Effective Accuracy Level (EAL) for a shot."""
        if log is None:
            log = []

        log.append(f"[Calculate EAL] Shooter: {shooter.name} -> Target: {target.name}")
        log.append(f"  Weapon: {weapon.name}, Range: {range_hexes} hexes, Exposure: {target_exposure.name}")

        max_aim_time_impulses = float('inf')
        movement_alm = 0
        if shot_params.target_speed_hex_per_impulse > 0:
            target_movement_alm, target_max_aim = Table4AdvancedOddsOfHitting.get_movement_alm_and_max_aim_time_4d(
                shot_params.target_speed_hex_per_impulse, range_hexes
            )
            movement_alm += target_movement_alm
            max_aim_time_impulses = min(max_aim_time_impulses, target_max_aim)
            log.append(f"  Target moving: {shot_params.target_speed_hex_per_impulse} hex/imp, ALM: {target_movement_alm}, Max aim: {target_max_aim}")

        if shot_params.shooter_speed_hex_per_impulse > 0:
            shooter_movement_alm, _ = Table4AdvancedOddsOfHitting.get_movement_alm_and_max_aim_time_4d(
                shot_params.shooter_speed_hex_per_impulse, range_hexes
            )
            movement_alm += shooter_movement_alm
            max_aim_time_impulses = min(max_aim_time_impulses, 1.0)
            log.append(f"  Shooter moving: {shot_params.shooter_speed_hex_per_impulse} hex/imp, ALM: {shooter_movement_alm}")

        effective_aim_time_ac = shot_params.aim_time_ac
        if max_aim_time_impulses < float('inf'):
            max_ac_per_impulse = max(shooter.impulses)
            max_aim_time_ac = int(max_aim_time_impulses * max_ac_per_impulse)
            effective_aim_time_ac = min(shot_params.aim_time_ac, max_aim_time_ac)
            log.append(f"  Aim time limited: {shot_params.aim_time_ac} -> {effective_aim_time_ac} AC")

        aim_time_alm = weapon.aim_time_modifiers.get(effective_aim_time_ac, 0) + shooter.skill_accuracy_level
        range_alm = Table4AdvancedOddsOfHitting.get_accuracy_level_modifier_by_range_4a(range_hexes)
        
        log.append(f"  Aim time ALM: {weapon.aim_time_modifiers.get(effective_aim_time_ac, 0)} + SAL {shooter.skill_accuracy_level} = {aim_time_alm}")
        log.append(f"  Range ALM (Table 4A): {range_alm}")

        situation_stance_alm = sum(mod.value for mod in shot_params.situation_stance_modifiers)
        visibility_alm = sum(mod.value for mod in shot_params.visibility_modifiers)
        
        log.append(f"  Situation/Stance ALM: {situation_stance_alm} ({[m.name for m in shot_params.situation_stance_modifiers]})")
        log.append(f"  Visibility ALM: {visibility_alm} ({[m.name for m in shot_params.visibility_modifiers]})")

        duck_alm = 0
        if shot_params.reflexive_duck_shooter:
            duck_alm -= 10
            log.append("  Shooter reflexive duck: -10")
        if shot_params.reflexive_duck_target:
            duck_alm -= 5
            log.append("  Target reflexive duck: -5")

        defensive_alm = target.defensive_alm
        log.append(f"  Defensive ALM: {defensive_alm}")

        alm_sum = aim_time_alm + range_alm + situation_stance_alm + visibility_alm + movement_alm + duck_alm + defensive_alm
        log.append(f"  Total ALM sum: {alm_sum}")

        ba = weapon.ballistic_data.get_ballistic_accuracy(range_hexes) if weapon.ballistic_data else float('inf')
        log.append(f"  Ballistic Accuracy limit: {ba}")

        effective_alm = min(ba, alm_sum)
        log.append(f"  Effective ALM: min({ba}, {alm_sum}) = {effective_alm}")

        target_size_alm = Table4AdvancedOddsOfHitting.get_standard_target_size_modifier_4e(
            target_exposure, target_size_modifier_type
        )
        log.append(f"  Target Size ALM (Table 4E, {target_size_modifier_type.name}): {target_size_alm}")

        eal = effective_alm + target_size_alm
        log.append(f"  Final EAL: {effective_alm} + {target_size_alm} = {eal}")

        return eal

    @staticmethod
    def determine_incapacitation(
        target: Character,
        pd_total: int,
        shock: int,
        log: List[str]
    ) -> Optional[IncapacitationEffect]:
        """Determine incapacitation effect."""
        pd_with_shock = pd_total + shock
        
        log.append(f"[Incapacitation Check] PD: {pd_total}, Shock: {shock}, Total: {pd_with_shock}, KO Value: {target.knockout_value}")

        chance = Table8HealingAndRecovery.get_incapacitation_chance(pd_with_shock, target.knockout_value)
        if chance == 0:
            log.append("  No incapacitation chance")
            return None
        
        roll = random.randint(0, 99)
        log.append(f"  Incapacitation chance: {chance}%, Roll: {roll}")

        if roll >= chance:
            log.append(f"  Roll {roll} >= {chance}, no incapacitation")
            return None
        
        effect_roll = random.randint(0, 99)
        effect = Table8HealingAndRecovery.get_incapacitation_effect(pd_with_shock, target.knockout_value, effect_roll)
        log.append(f"  Effect roll: {effect_roll}, Result: {effect.name if effect else 'None'}")

        return effect

    @staticmethod
    def process_hit(
        target: Character,
        ammo: AmmoType,
        range_hexes: int,
        target_exposure: TargetExposure,
        shot_params: ShotParameters,
        is_front_shot: bool,
        log: List[str]
    ):
        """Process a successful hit and calculate damage."""
        log.append(f"[Process Hit] Target: {target.name}, Ammo: {ammo.name}, Range: {range_hexes}")

        location = Table1AdvancedDamageHitLocation.get_hit_location(
            target_exposure, shot_params.target_orientation
        )
        log.append(f"  Hit location: {location.name}")

        pen = ammo.get_pen(range_hexes)
        dc = ammo.get_dc(range_hexes)
        log.append(f"  PEN: {pen}, DC: {dc}")

        epen = pen
        penetrated = True
        blunt_pf = 0
        total_protection = 0
        for item in target.equipment:
            if isinstance(item, Armor):
                total_protection += item.get_protection(location, is_front_shot).get_total_protection()
                protection_data = item.get_protection(location, is_front_shot)
                if protection_data.get_total_protection() > 0:
                    log.append(f"  Armor: {item.name}, Protection: {protection_data.get_total_protection()}")
                    penetrated, remaining_pen = item.process_hit(location, is_front_shot, pen)
                    epen = remaining_pen
                    if not penetrated:
                        blunt_pf = protection_data.get_total_blunt_protection()
                        log.append(f"  Armor NOT penetrated, Blunt PF: {blunt_pf}")
                    else:
                        log.append(f"  Armor penetrated, Remaining PEN: {epen}")
                    break
        
        if not penetrated:
            blunt_damage = Table9ABluntDamage.get_blunt_damage(location, blunt_pf, pen)
            log.append(f"  Blunt damage: {blunt_damage}")
            target.apply_damage(blunt_damage)
            damage_result = AdvancedDamageCalculator.calculate_damage(
                location=location, dc=0, epen=0.0, is_front=is_front_shot
            )
            damage_result.damage = blunt_damage
        else:
            epen = max(0.0, epen)
            if total_protection > epen:
                dc = 1
                log.append("  Protection > EPEN, DC reduced to 1")
            damage_result = AdvancedDamageCalculator.calculate_damage(
                location=location, dc=dc, epen=epen, is_front=is_front_shot
            )
            log.append(f"  Damage: {damage_result.damage}, Shock: {damage_result.shock}")
            if damage_result.pierced_organs:
                log.append(f"  Pierced organs: {damage_result.pierced_organs}")
            target.apply_damage(damage_result.damage)
        
        log.append(f"  Target total PD: {target.physical_damage_total}")

        incap_effect = CombatSimulatorUtils.determine_incapacitation(
            target, target.physical_damage_total, damage_result.shock, log
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
            log.append(f"  Incapacitation time: {incap_time} phases")

        return damage_result, incap_effect, recovery, incap_time
    
    @staticmethod
    def process_target_hits(
        target: Character,
        ammo: AmmoType,
        range_hexes: int,
        exposure: TargetExposure,
        shot_params: ShotParameters,
        is_front_shot: bool,
        hits: int,
        log: List[str]
    ) -> List[ShotResult]:
        """Process multiple hits on a single target."""
        log.append(f"[Process Target Hits] {hits} hits on {target.name}")

        target_results = []
        for i in range(hits):
            hit_log = []
            hit_log.append(f"--- Hit {i+1}/{hits} ---")
            dmg, effect, recovery, time = CombatSimulatorUtils.process_hit(
                target, ammo, range_hexes, exposure, shot_params, is_front_shot, hit_log
            )
            log.extend(hit_log)
            target_results.append(ShotResult(
                hit=True,
                eal=0,
                odds=100,
                roll=0,
                target=target,
                damage_result=dmg,
                incapacitation_effect=effect,
                recovery=recovery,
                incapacitation_time_phases=time,
                log="\n".join(hit_log)
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
        arc_of_fire: float,
        log: List[str]
    ) -> BurstElevationResult:
        """Check elevation and calculate hits for burst fire."""
        odds = Table4AdvancedOddsOfHitting.get_odds_of_hitting_4g(eal, ShotType.BURST)
        roll = random.randint(0, 99)

        log.append(f"  Elevation check: EAL {eal}, Odds {odds}%, Roll {roll}")

        if roll > odds:
            log.append(f"  Miss! Roll {roll} > Odds {odds}")
            return BurstElevationResult(hit=False, eal=eal, odds=odds, roll=roll, hits=0)
        
        auto_width_modifier = Table4AdvancedOddsOfHitting.get_standard_target_size_modifier_4e(
            exposure, AccuracyModifiers.AUTO_WIDTH
        )
        
        hits = Table5AutoPelletShrapnel.get_fire_table_value5a(
            arc_of_fire, weapon.full_auto_rof, auto_width_modifier
        )

        log.append(f"  Hit! Arc: {arc_of_fire}, ROF: {weapon.full_auto_rof}, Width mod: {auto_width_modifier}")
        log.append(f"  Hits from Table 5A: {hits}")

        return BurstElevationResult(hit=hits > 0, eal=eal, odds=odds, roll=roll, hits=hits)

    @staticmethod
    def process_shotgun_pattern(
        ammo: AmmoType,
        targets: List[Character],
        ranges: List[int],
        exposures: List[TargetExposure],
        shot_params_list: List[ShotParameters],
        is_front_shots: List[bool],
        bphc: Optional[str],
        log: List[str]
    ) -> List[ShotResult]:
        """Process shotgun pattern hits for all targets."""
        log.append(f"[Shotgun Pattern] BPHC: {bphc}, Targets: {len(targets)}")

        if bphc is None:
            pellet_hits_data = []
        else:
            pellet_hits_data = CombatSimulatorUtils.calculate_pellet_hits_per_target(
                targets, ranges, exposures, shot_params_list, is_front_shots, bphc, log
            )

        if ammo.pellet_count is not None and pellet_hits_data:
            pellet_hits_data = CombatSimulatorUtils.redistribute_pellets(pellet_hits_data, ammo.pellet_count, log)

        results = []
        for idx, hits, target, rng, exposure, params, front, _ in pellet_hits_data:
            hit_results = CombatSimulatorUtils.process_target_hits(
                target, ammo, rng, exposure, params, front, hits, log
            )
            results.extend(hit_results)

        return results

    @staticmethod
    def calculate_pellet_hits_per_target(
        targets: List[Character],
        ranges: List[int],
        exposures: List[TargetExposure],
        shot_params_list: List[ShotParameters],
        is_front_shots: List[bool],
        bphc: str,
        log: List[str]
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
                log.append(f"  {target.name}: Guaranteed {base_hits}, Size mod {target_size_modifier}, Hits: {pellet_hits}")
            else:
                pellet_hits = Table5AutoPelletShrapnel.get_shrapnel_pellet_hits_5a(
                    int(bphc), False, target_size_modifier
                )
                pellet_roll = random.randint(0, 99)
                log.append(f"  {target.name}: BPHC {bphc}, Size mod {target_size_modifier}, Roll {pellet_roll}, Hits: {pellet_hits}")

            if pellet_hits > 0:
                pellet_hits_data.append((idx, pellet_hits, target, rng, exposure, params, front, pellet_roll))
        
        return pellet_hits_data

    @staticmethod
    def redistribute_pellets(
        pellet_hits_data: List[tuple[int, int, Character, int, TargetExposure, ShotParameters, bool, int]],
        pellet_count: int,
        log: List[str]
    ) -> List[tuple[int, int, Character, int, TargetExposure, ShotParameters, bool, int]]:
        """Redistribute pellet hits if total exceeds pellet count."""
        total_hits = sum(h[1] for h in pellet_hits_data)
        if total_hits <= pellet_count:
            return pellet_hits_data
        
        log.append(f"  Redistributing pellets: {total_hits} > {pellet_count}")

        redistributed = []
        remaining = pellet_count
        for i, (idx, hits, target, rng, exposure, params, front, pellet_roll) in enumerate(pellet_hits_data):
            if i == len(pellet_hits_data) - 1:
                new_hits = remaining
            else:
                new_hits = max(1, int(pellet_count * (hits / total_hits)))
                remaining -= new_hits
            log.append(f"    {target.name}: {hits} -> {new_hits}")
            redistributed.append((idx, new_hits, target, rng, exposure, params, front, pellet_roll))
        return redistributed

    @staticmethod
    def calculate_explosive_eal(
        shooter: Character,
        weapon: Weapon,
        range_hexes: int,
        target_size_alm: int,
        shot_params: ShotParameters,
        log: List[str]
    ) -> int:
        """Calculate EAL for explosive weapon."""
        log.append(f"[Explosive EAL] Weapon: {weapon.name}, Range: {range_hexes}")

        max_aim_time_impulses = float('inf')
        movement_alm = 0
        
        if shot_params.shooter_speed_hex_per_impulse > 0:
            shooter_movement_alm, max_aim_time_impulses = Table4AdvancedOddsOfHitting.get_movement_alm_and_max_aim_time_4d(
                shot_params.shooter_speed_hex_per_impulse, range_hexes
            )
            movement_alm += shooter_movement_alm
            max_aim_time_impulses = min(max_aim_time_impulses, 1.0)
            log.append(f"  Shooter moving: {shot_params.shooter_speed_hex_per_impulse} hex/imp, ALM: {shooter_movement_alm}")

        effective_aim_time_ac = shot_params.aim_time_ac
        if max_aim_time_impulses < float('inf'):
            max_ac_per_impulse = max(shooter.impulses)
            max_aim_time_ac = int(max_aim_time_impulses * max_ac_per_impulse)
            effective_aim_time_ac = min(shot_params.aim_time_ac, max_aim_time_ac)
        
        aim_time_alm = weapon.aim_time_modifiers.get(effective_aim_time_ac, 0) + shooter.skill_accuracy_level
        range_alm = Table4AdvancedOddsOfHitting.get_accuracy_level_modifier_by_range_4a(range_hexes)
        
        log.append(f"  Aim time ALM: {aim_time_alm}, Range ALM: {range_alm}")

        situation_stance_alm = sum(mod.value for mod in shot_params.situation_stance_modifiers)
        visibility_alm = sum(mod.value for mod in shot_params.visibility_modifiers)
        
        log.append(f"  Situation ALM: {situation_stance_alm}, Visibility ALM: {visibility_alm}")

        duck_alm = 0
        if shot_params.reflexive_duck_shooter:
            duck_alm -= 10
            log.append("  Shooter duck: -10")

        alm_sum = aim_time_alm + range_alm + situation_stance_alm + visibility_alm + movement_alm + duck_alm
        
        ba = weapon.ballistic_data.get_ballistic_accuracy(range_hexes) if weapon.ballistic_data else float('inf')
        effective_alm = min(ba, alm_sum)
        
        log.append(f"  ALM sum: {alm_sum}, BA: {ba}, Effective: {effective_alm}")

        eal = effective_alm + target_size_alm
        log.append(f"  Target size ALM: {target_size_alm}, Final EAL: {eal}")

        return eal

    @staticmethod
    def calculate_grenade_eal(
        shooter: Character,
        range_hexes: int,
        target_size_alm: int,
        aim_alm: int,
        situation_stance_modifiers: List,
        visibility_modifiers: List,
        log: List[str]
    ) -> int:
        """Calculate EAL for thrown grenade."""
        log.append(f"[Grenade EAL] Range: {range_hexes}, Aim ALM: {aim_alm}")

        range_alm = Table4AdvancedOddsOfHitting.get_accuracy_level_modifier_by_range_4a(range_hexes)
        situation_stance_alm = sum(mod.value for mod in situation_stance_modifiers)
        visibility_alm = sum(mod.value for mod in visibility_modifiers)
        
        log.append(f"  Range ALM: {range_alm}, Situation: {situation_stance_alm}, Visibility: {visibility_alm}")
        log.append(f"  SAL: {shooter.skill_accuracy_level}")

        alm_sum = aim_alm + shooter.skill_accuracy_level + range_alm + situation_stance_alm + visibility_alm
        eal = alm_sum + target_size_alm

        log.append(f"  ALM sum: {alm_sum}, Target size: {target_size_alm}, EAL: {eal}")

        return eal

    @staticmethod
    def process_shrapnel_hits(
        target: Character,
        ammo: AmmoType,
        range_from_burst: int,
        exposure: TargetExposure,
        shot_params: ShotParameters,
        is_front_shot: bool,
        bshc: str,
        log: List[str]
    ) -> List[ShotResult]:
        """Process shrapnel hits from explosion."""
        log.append(f"[Shrapnel] Target: {target.name}, BSHC: {bshc}, Range: {range_from_burst}")

        target_size_modifier = Table4AdvancedOddsOfHitting.get_standard_target_size_modifier_4e(
            exposure, AccuracyModifiers.AUTO_WIDTH
        )
        if bshc.startswith('*'):
            base_hits = int(bshc[1:])
            is_guaranteed = True
        else:
            base_hits = int(bshc)
            is_guaranteed = False

        shrapnel_hits = Table5AutoPelletShrapnel.get_shrapnel_pellet_hits_5a(
            base_hits, is_guaranteed, target_size_modifier
        )

        log.append(f"  Base: {base_hits}, Guaranteed: {is_guaranteed}, Size mod: {target_size_modifier}, Hits: {shrapnel_hits}")

        if shrapnel_hits == 0:
            log.append("  No shrapnel hits")
            return []

        pen = ammo.get_explosion_pen(range_from_burst)
        dc = ammo.get_explosion_dc(range_from_burst)
        log.append(f"  Shrapnel PEN: {pen}, DC: {dc}")

        results = []
        for i in range(shrapnel_hits):
            hit_log = [f"--- Shrapnel hit {i + 1}/{shrapnel_hits} ---"]

            location = Table1AdvancedDamageHitLocation.get_hit_location(
                exposure, shot_params.target_orientation
            )
            hit_log.append(f"  Location: {location.name}")

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
                        hit_log.append(f"  Armor: {item.name}, Penetrated: {penetrated}")
                        break

            if not penetrated:
                blunt_damage = Table9ABluntDamage.get_blunt_damage(location, blunt_pf, pen)
                target.apply_damage(blunt_damage)
                damage_result = DamageResult(location=location, damage=blunt_damage)
                hit_log.append(f"  Blunt damage: {blunt_damage}")
            else:
                epen = max(0.0, epen)
                effective_dc = 1 if total_protection > epen else dc
                damage_result = AdvancedDamageCalculator.calculate_damage(
                    location=location, dc=effective_dc, epen=epen, is_front=is_front_shot
                )
                target.apply_damage(damage_result.damage)
                hit_log.append(f"  Damage: {damage_result.damage}, Shock: {damage_result.shock}")

            incap_effect = CombatSimulatorUtils.determine_incapacitation(
                target, target.physical_damage_total, damage_result.shock, hit_log
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
                hit_log.append(f"  Incap time: {incap_time} phases")

            log.extend(hit_log)
            results.append(ShotResult(
                hit=True,
                eal=0,
                odds=base_hits if not is_guaranteed else 100,
                roll=0,
                target=target,
                damage_result=damage_result,
                incapacitation_effect=incap_effect,
                recovery=recovery,
                incapacitation_time_phases=incap_time,
                log="\n".join(hit_log)
            ))

        return results

    @staticmethod
    def process_concussion_damage(
        target: Character,
        base_concussion: int,
        blast_modifiers: List[BlastModifier],
        log: List[str]
    ) -> Optional[ShotResult]:
        """Process concussion damage from explosion."""
        log.append(f"[Concussion] Target: {target.name}, Base: {base_concussion}")

        if base_concussion <= 0:
            log.append("  No concussion damage")
            return None

        total_modifier = 1.0
        for modifier in blast_modifiers:
            total_modifier *= modifier.value

        log.append(f"  Blast modifiers: {[m.name for m in blast_modifiers]}, Total: {total_modifier}")

        concussion_damage = int(base_concussion * total_modifier)

        if concussion_damage <= 0:
            log.append("  Final concussion damage: 0")
            return None

        log.append(f"  Concussion damage: {concussion_damage}")
        target.apply_damage(concussion_damage)

        damage_result = DamageResult(
            location=AdvancedHitLocation.MISS,
            damage=concussion_damage,
            shock=0
        )

        incap_effect = CombatSimulatorUtils.determine_incapacitation(
            target, target.physical_damage_total, 0, log
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
            log.append(f"  Incap time: {incap_time} phases")

        return ShotResult(
            hit=True,
            eal=0,
            odds=100,
            roll=0,
            target=target,
            damage_result=damage_result,
            incapacitation_effect=incap_effect,
            recovery=recovery,
            incapacitation_time_phases=incap_time,
            log="\n".join(log)
        )
