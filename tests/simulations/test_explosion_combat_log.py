"""Explosion ShotResult tagging for Combat Log (blast / shrapnel)."""

from unittest.mock import patch

from phoenix_command.item_database.grenades import m67, of_hg_78
from phoenix_command.models.character import Character
from phoenix_command.models.enums import (
    AdvancedHitLocation,
    IncapacitationEffect,
    SituationStanceModifier4B,
    TargetExposure,
    TargetOrientation,
    VisibilityModifier4C,
)
from phoenix_command.models.hit_result_advanced import DamageResult, ShotParameters
from phoenix_command.session.domains.impulse_combat_state import TokenCombatRuntime
from phoenix_command.simulations.combat_simulator_utils import CombatSimulatorUtils
from phoenix_command.simulations.map_wounds import apply_incap_to_runtime


def _char(name: str = "T") -> Character:
    return Character(
        name=name,
        strength=12,
        intelligence=10,
        will=11,
        health=12,
        agility=10,
        gun_combat_skill_level=5,
    )


def _params() -> ShotParameters:
    return ShotParameters(
        aim_time_ac=1,
        situation_stance_modifiers=[SituationStanceModifier4B.STANDING],
        visibility_modifiers=[VisibilityModifier4C.GOOD_VISIBILITY],
        target_orientation=TargetOrientation.FRONT_REAR,
    )


def test_concussion_uses_blast_damage_location() -> None:
    log: list[str] = []
    result = CombatSimulatorUtils.process_concussion_damage(_char(), 100, [], log)
    assert result is not None
    assert result.damage_source == "blast"
    assert result.damage_result is not None
    assert result.damage_result.location == AdvancedHitLocation.BLAST_DAMAGE


def test_shrapnel_zero_hits_with_chance_emits_miss() -> None:
    with patch(
        "phoenix_command.simulations.combat_simulator_utils."
        "Table5AutoPelletShrapnel.get_shrapnel_pellet_hits_5a",
        return_value=0,
    ):
        results = CombatSimulatorUtils.process_shrapnel_hits(
            _char(),
            m67,
            range_from_burst=1,
            exposure=TargetExposure.STANDING_EXPOSED,
            shot_params=_params(),
            is_front_shot=True,
            bshc="10",
            log=[],
        )
    assert len(results) == 1
    assert results[0].hit is False
    assert results[0].damage_source == "shrapnel"


def test_shrapnel_bshc_zero_emits_nothing() -> None:
    with patch(
        "phoenix_command.simulations.combat_simulator_utils."
        "Table5AutoPelletShrapnel.get_shrapnel_pellet_hits_5a",
        return_value=0,
    ):
        results = CombatSimulatorUtils.process_shrapnel_hits(
            _char(),
            of_hg_78,
            range_from_burst=1,
            exposure=TargetExposure.STANDING_EXPOSED,
            shot_params=_params(),
            is_front_shot=True,
            bshc="0",
            log=[],
        )
    assert results == []


def test_shrapnel_incap_does_not_downgrade_across_fragments() -> None:
    """BUG-03: later milder rolls must not appear on ShotResult / Combat Log."""
    effects = [
        IncapacitationEffect.KNOCKED_OUT,
        IncapacitationEffect.DAZED,
        IncapacitationEffect.DISORIENTED,
    ]

    def _fake_incap(target, pd_total, shock, log):
        return effects.pop(0) if effects else None

    with (
        patch(
            "phoenix_command.simulations.combat_simulator_utils."
            "Table5AutoPelletShrapnel.get_shrapnel_pellet_hits_5a",
            return_value=3,
        ),
        patch(
            "phoenix_command.simulations.combat_simulator_utils."
            "Table1AdvancedDamageHitLocation.get_hit_location",
            return_value=AdvancedHitLocation.TORSO_GLANCE,
        ),
        patch(
            "phoenix_command.simulations.combat_simulator_utils."
            "AdvancedDamageCalculator.calculate_damage",
            return_value=DamageResult(
                location=AdvancedHitLocation.TORSO_GLANCE, damage=5, shock=2
            ),
        ),
        patch(
            "phoenix_command.simulations.combat_simulator_utils."
            "CombatSimulatorUtils.determine_incapacitation",
            side_effect=_fake_incap,
        ),
        patch(
            "phoenix_command.simulations.combat_simulator_utils."
            "Table8HealingAndRecovery.get_incapacitation_time_8b",
            return_value=10,
        ),
    ):
        results = CombatSimulatorUtils.process_shrapnel_hits(
            _char(),
            m67,
            range_from_burst=0,
            exposure=TargetExposure.STANDING_EXPOSED,
            shot_params=_params(),
            is_front_shot=True,
            bshc="*3",
            log=[],
        )

    assert len(results) == 3
    assert results[0].incapacitation_effect == IncapacitationEffect.KNOCKED_OUT
    assert results[1].incapacitation_effect is None
    assert results[2].incapacitation_effect is None


def test_blast_incap_clamped_by_prior_shrapnel_ko() -> None:
    with patch(
        "phoenix_command.simulations.combat_simulator_utils."
        "CombatSimulatorUtils.determine_incapacitation",
        return_value=IncapacitationEffect.DAZED,
    ), patch(
        "phoenix_command.simulations.combat_simulator_utils."
        "Table8HealingAndRecovery.get_incapacitation_time_8b",
        return_value=4,
    ):
        result = CombatSimulatorUtils.process_concussion_damage(
            _char(),
            100,
            [],
            [],
            prior_incap=IncapacitationEffect.KNOCKED_OUT,
            prior_incap_time=12,
        )
    assert result is not None
    assert result.damage_source == "blast"
    assert result.incapacitation_effect is None


def test_apply_incap_equal_severity_keeps_longer_time() -> None:
    rt = TokenCombatRuntime()
    assert apply_incap_to_runtime(rt, IncapacitationEffect.KNOCKED_OUT, 20)
    assert rt.incap_remaining_phases == 20
    assert apply_incap_to_runtime(rt, IncapacitationEffect.KNOCKED_OUT, 5)
    assert rt.incap_remaining_phases == 20
    assert apply_incap_to_runtime(rt, IncapacitationEffect.DAZED, 99) is False
    assert rt.incap_effect == IncapacitationEffect.KNOCKED_OUT.value
    assert rt.incap_remaining_phases == 20
