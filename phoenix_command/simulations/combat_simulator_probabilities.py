"""Probability calculations for combat simulation."""

from typing import List, Tuple, Optional

from phoenix_command.models.character import Character
from phoenix_command.models.enums import TargetExposure, ShotType, AccuracyModifiers, SituationStanceModifier4B
from phoenix_command.models.gear import Weapon, AmmoType
from phoenix_command.models.hit_result_advanced import ShotParameters
from phoenix_command.simulations.combat_simulator_utils import CombatSimulatorUtils
from phoenix_command.tables.advanced_rules.effective_min_arc import EffectiveMinimumArc
from phoenix_command.tables.advanced_rules.three_round_burst import ThreeRoundBurstTable
from phoenix_command.tables.core.table4_advanced_odds_of_hitting import Table4AdvancedOddsOfHitting
from phoenix_command.tables.core.table5_auto_pellet_shrapnel import Table5AutoPelletShrapnel


class CombatSimulatorProbabilities:
    """Calculate probabilities for combat actions."""

    @staticmethod
    def calculate_single_shot_probability(
        shooter: Character,
        target: Character,
        weapon: Weapon,
        range_hexes: int,
        target_exposure: TargetExposure,
        shot_params: ShotParameters
    ) -> Tuple[int, int]:
        """Calculate hit probability for single shot.
        
        Returns:
            Tuple of (eal, odds_percent)
        """
        eal = CombatSimulatorUtils.calculate_eal(
            shooter, target, weapon, range_hexes, target_exposure, shot_params
        )
        odds = Table4AdvancedOddsOfHitting.get_odds_of_hitting_4g(eal, ShotType.SINGLE)
        return eal, odds

    @staticmethod
    def calculate_shotgun_probabilities(
        shooter: Character,
        target: Character,
        weapon: Weapon,
        ammo: AmmoType,
        range_hexes: int,
        target_exposure: TargetExposure,
        shot_params: ShotParameters
    ) -> Tuple[int, int, str, str]:
        """Calculate shotgun pattern hit probability and pellet hits.
        
        Returns:
            Tuple of (eal, pattern_odds_percent, bphc, pellet_info)
            where pellet_info is formatted string like "5 guaranteed" or "37% chance"
        """
        data = CombatSimulatorUtils.get_shotgun_data_at_range(ammo, range_hexes)
        
        if data.shotgun_accuracy_level_modifier is None:
            eal = CombatSimulatorUtils.calculate_eal(
                shooter, target, weapon, range_hexes, target_exposure, shot_params
            )
            odds = Table4AdvancedOddsOfHitting.get_odds_of_hitting_4g(eal, ShotType.SINGLE)
            return eal, odds, None, "1 hit"
        
        eal = CombatSimulatorUtils.calculate_shotgun_eal(
            shooter, target, weapon, range_hexes, target_exposure, shot_params,
            data.shotgun_accuracy_level_modifier, 0
        )
        odds = Table4AdvancedOddsOfHitting.get_odds_of_hitting_4g(eal, ShotType.SINGLE)
        
        target_size_modifier = Table4AdvancedOddsOfHitting.get_standard_target_size_modifier_4e(
            target_exposure, AccuracyModifiers.AUTO_WIDTH
        )
        
        bphc = data.base_pellet_hit_chance
        if bphc:
            if bphc.startswith('*'):
                base_hits = int(bphc[1:])
                guaranteed, probability = Table5AutoPelletShrapnel.get_pellet_hit_probability_5a(
                    base_hits, True, target_size_modifier
                )
                if probability > 0:
                    pellet_info = f"{guaranteed} guaranteed + {probability}% chance"
                else:
                    pellet_info = f"{guaranteed} guaranteed"
            else:
                base_value = int(bphc)
                guaranteed, probability = Table5AutoPelletShrapnel.get_pellet_hit_probability_5a(
                    base_value, False, target_size_modifier
                )
                if guaranteed > 0:
                    if probability > 0:
                        pellet_info = f"{guaranteed} guaranteed + {probability}% chance"
                    else:
                        pellet_info = f"{guaranteed} guaranteed"
                else:
                    pellet_info = f"{probability}% chance"
        else:
            pellet_info = "0"
        
        return eal, odds, bphc, pellet_info

    @staticmethod
    def calculate_three_round_burst_probabilities(
        shooter: Character,
        target: Character,
        weapon: Weapon,
        range_hexes: int,
        target_exposure: TargetExposure,
        shot_params: ShotParameters
    ) -> Tuple[int, List[Tuple[int, int]]]:
        """Calculate three round burst hit probabilities.
        
        Returns:
            Tuple of (eal, hit_probabilities) where hit_probabilities is list of (hits, probability_percent)
        """
        if not weapon.ballistic_data:
            return 0, []
        
        rb3_value = weapon.ballistic_data.get_three_round_burst(range_hexes)
        if rb3_value is None:
            return 0, []
        
        eal = CombatSimulatorUtils.calculate_eal(
            shooter, target, weapon, range_hexes, target_exposure, shot_params
        )
        
        available_3rb = sorted(ThreeRoundBurstTable.TABLE_9B.keys())
        target_3rb = min(available_3rb, key=lambda x: abs(x - rb3_value))
        target_eal = max(3, min(28, eal))
        chances = ThreeRoundBurstTable.TABLE_9B[target_3rb][target_eal]
        
        probabilities = []
        
        if len(chances) == 1:
            prob_1_hit = chances[0]
            prob_0_hits = 100 - prob_1_hit
            if prob_0_hits > 0:
                probabilities.append((0, prob_0_hits))
            probabilities.append((1, prob_1_hit))
        elif len(chances) == 2:
            prob_2_hits = chances[1]
            prob_1_hit = chances[0] - chances[1]
            prob_0_hits = 100 - chances[0]
            if prob_0_hits > 0:
                probabilities.append((0, prob_0_hits))
            if prob_1_hit > 0:
                probabilities.append((1, prob_1_hit))
            if prob_2_hits > 0:
                probabilities.append((2, prob_2_hits))
        elif len(chances) == 3:
            prob_3_hits = chances[2]
            prob_2_hits = chances[1] - chances[2]
            prob_1_hit = chances[0] - chances[1]
            prob_0_hits = 100 - chances[0]
            if prob_0_hits > 0:
                probabilities.append((0, prob_0_hits))
            if prob_1_hit > 0:
                probabilities.append((1, prob_1_hit))
            if prob_2_hits > 0:
                probabilities.append((2, prob_2_hits))
            if prob_3_hits > 0:
                probabilities.append((3, prob_3_hits))
        
        return eal, probabilities

    @staticmethod
    def calculate_burst_fire_probabilities(
        shooter: Character,
        target: Character,
        weapon: Weapon,
        range_hexes: int,
        target_exposure: TargetExposure,
        shot_params: ShotParameters,
        arc_of_fire: Optional[float] = None,
        continuous_burst_impulses: int = 0
    ) -> Tuple[int, int, float, str]:
        """Calculate burst fire hit probability and expected hits for a single target.

        Args:
            shooter: Shooter character
            target: Target character
            weapon: Full auto weapon
            range_hexes: Range in hexes
            target_exposure: Target exposure
            shot_params: Shot parameters
            arc_of_fire: Custom arc of fire (None for auto calculation)
            continuous_burst_impulses: Number of impulses of continuous burst (SAB penalty)

        Returns:
            Tuple of (eal, elevation_odds_percent, effective_arc, hits_info)
            where hits_info is formatted string like "5 guaranteed" or "37% chance of 1 hit"
        """
        if not weapon.full_auto or not weapon.full_auto_rof:
            return 0, 0, 0.0, "N/A"

        if not weapon.ballistic_data:
            return 0, 0, 0.0, "N/A"

        # Calculate SAB penalty
        sab_penalty = 0
        if continuous_burst_impulses > 0 and weapon.sustained_auto_burst:
            sab_penalty = continuous_burst_impulses * weapon.sustained_auto_burst

        # Calculate minimum arc
        min_arc = weapon.ballistic_data.get_minimum_arc(range_hexes)
        if min_arc is None:
            return 0, 0, 0.0, "N/A"

        # Determine stance
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

        # Calculate EAL for elevation check
        eal = CombatSimulatorUtils.calculate_eal(
            shooter, target, weapon, range_hexes, target_exposure, shot_params,
            AccuracyModifiers.AUTO_ELEV
        ) - sab_penalty

        # Get elevation odds
        elevation_odds = Table4AdvancedOddsOfHitting.get_odds_of_hitting_4g(eal, ShotType.BURST)

        # Get target width modifier
        auto_width_modifier = Table4AdvancedOddsOfHitting.get_standard_target_size_modifier_4e(
            target_exposure, AccuracyModifiers.AUTO_WIDTH
        )

        # Get hits probability from Table 5A
        guaranteed_hits, probability = Table5AutoPelletShrapnel.get_fire_table_probability_5a(
            final_arc, weapon.full_auto_rof, auto_width_modifier
        )

        if guaranteed_hits > 0:
            hits_info = f"{guaranteed_hits} guaranteed"
        elif probability > 0:
            hits_info = f"{probability}% chance of 1 hit"
        else:
            hits_info = "0 hits"

        return eal, elevation_odds, final_arc, hits_info

