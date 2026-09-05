"""Map incapacitation, disables, CTP survival, HT/20 CA (§2.7–2.10 / §5.13)."""

from phoenix_command.models.character import Character
from phoenix_command.models.enums import (
    AdvancedHitLocation,
    Caliber,
    Country,
    IncapacitationEffect,
    MedicalAid,
    SituationStanceModifier4B,
    WeaponType,
)
from phoenix_command.models.gear import Weapon
from phoenix_command.models.hit_result_advanced import DamageResult, ShotResult
from phoenix_command.models.recovery import Recovery
from phoenix_command.session.domains.impulse_combat_state import ImpulseCombatState, TokenCombatRuntime
from phoenix_command.session.domains.map_state import MapState
from phoenix_command.session.domains.token_state import TokenPlacement, TokenState
from phoenix_command.simulations.impulse_combat_engine import ImpulseCombatEngine
from phoenix_command.simulations.map_wounds import (
    apply_disable_flags,
    apply_recovery_to_runtime,
    apply_shot_wounds,
    can_fire_weapon,
    can_perform_action,
    effective_impulse_ac,
    merge_incapacitation,
    one_hand_alm_for_shot,
    resolve_ctp_if_due,
    tick_incap_phase,
    wound_ca_penalty_from_healing_days,
)


def _char(name: str = "T", health: int = 12) -> Character:
    return Character(
        name=name,
        strength=12,
        intelligence=10,
        will=11,
        health=health,
        agility=10,
        gun_combat_skill_level=5,
    )


def _rifle() -> Weapon:
    return Weapon(
        name="Test Rifle",
        weight=8.0,
        caliber=Caliber.CAL_556_NATO,
        weapon_type=WeaponType.ASSAULT_RIFLE,
        country=Country.USA,
        length_deployed=30.0,
        reload_time=6,
    )


def _pistol() -> Weapon:
    return Weapon(
        name="Test Pistol",
        weight=2.0,
        caliber=Caliber.CAL_9MM_PARABELLUM,
        weapon_type=WeaponType.AUTOMATIC_PISTOL,
        country=Country.USA,
        length_deployed=8.0,
        reload_time=4,
    )


def _engine(char: Character | None = None) -> tuple[ImpulseCombatEngine, TokenPlacement]:
    char = char or _char()
    ic = ImpulseCombatState(map_mode="combat", phase=1, impulse=0)
    tokens = TokenState()
    tok = TokenPlacement(token_id="t1", character_name=char.name, q=0, r=0)
    tokens.placements["t1"] = tok
    ic.token_runtime["t1"] = TokenCombatRuntime(ac_remaining=2.0)
    engine = ImpulseCombatEngine(ic, tokens, MapState(), {char.name: char})
    return engine, tok


def test_merge_never_downgrades() -> None:
    assert merge_incapacitation("Stunned", IncapacitationEffect.DISORIENTED) == "Stunned"
    assert merge_incapacitation("Knocked Out", IncapacitationEffect.DAZED) == "Knocked Out"
    assert merge_incapacitation("Dazed", IncapacitationEffect.STUNNED) == "Stunned"
    assert merge_incapacitation(None, IncapacitationEffect.DAZED) == "Dazed"


def test_ctp_zero_instant_dead() -> None:
    rt = TokenCombatRuntime()
    recovery = Recovery(
        healing_time_in_days=99,
        aid_data={MedicalAid.NO_AID: (0, None)},
    )
    apply_recovery_to_runtime(rt, recovery, abs_impulse=4)
    assert rt.is_dead is True
    assert rt.ctp_resolved is True


def test_ctp_expire_rr_fail_and_pass() -> None:
    rt = TokenCombatRuntime(
        wound_onset_abs_impulse=0,
        ctp_deadline_abs_impulse=4,
        recovery_rr=50,
        ctp_resolved=False,
    )
    msg = resolve_ctp_if_due(rt, abs_impulse=4, rng=_FixedRng(60))
    assert "dead" in msg.lower()
    assert rt.is_dead is True

    rt2 = TokenCombatRuntime(
        wound_onset_abs_impulse=0,
        ctp_deadline_abs_impulse=4,
        recovery_rr=50,
        ctp_resolved=False,
    )
    msg2 = resolve_ctp_if_due(rt2, abs_impulse=4, rng=_FixedRng(40))
    assert "survived" in msg2.lower()
    assert rt2.is_dead is False
    assert rt2.ctp_deadline_abs_impulse is None


def test_ctp_expire_no_rr_autodeath() -> None:
    rt = TokenCombatRuntime(
        wound_onset_abs_impulse=0,
        ctp_deadline_abs_impulse=2,
        recovery_rr=None,
        ctp_resolved=False,
    )
    msg = resolve_ctp_if_due(rt, abs_impulse=2)
    assert "dead" in msg.lower()
    assert rt.is_dead is True


def test_ctp_restart_after_survive() -> None:
    rt = TokenCombatRuntime(
        wound_onset_abs_impulse=0,
        ctp_deadline_abs_impulse=None,
        recovery_rr=None,
        ctp_resolved=True,
        is_dead=False,
    )
    recovery = Recovery(
        healing_time_in_days=10,
        aid_data={MedicalAid.NO_AID: (5, 70)},
    )
    apply_recovery_to_runtime(rt, recovery, abs_impulse=20)
    assert rt.ctp_resolved is False
    assert rt.wound_onset_abs_impulse == 20
    assert rt.ctp_deadline_abs_impulse == 20 + 5 * 4
    assert rt.recovery_rr == 70


def test_ctp_new_damage_never_extends() -> None:
    rt = TokenCombatRuntime(
        wound_onset_abs_impulse=0,
        ctp_deadline_abs_impulse=40,
        recovery_rr=80,
        ctp_resolved=False,
    )
    # Candidate from shorter CTP (2 phases → deadline 8) must shrink
    short = Recovery(
        healing_time_in_days=30,
        aid_data={MedicalAid.NO_AID: (2, 40)},
    )
    apply_recovery_to_runtime(rt, short, abs_impulse=3)
    assert rt.wound_onset_abs_impulse == 0
    assert rt.ctp_deadline_abs_impulse == 8
    assert rt.recovery_rr == 40

    # Candidate longer than current deadline must not extend
    long = Recovery(
        healing_time_in_days=10,
        aid_data={MedicalAid.NO_AID: (50, 90)},
    )
    apply_recovery_to_runtime(rt, long, abs_impulse=4)
    assert rt.ctp_deadline_abs_impulse == 8


def test_ctp_aid_upgrade_may_extend() -> None:
    rt = TokenCombatRuntime(
        wound_onset_abs_impulse=0,
        ctp_deadline_abs_impulse=8,
        medical_aid="First Aid",
        ctp_resolved=False,
    )
    recovery = Recovery(
        healing_time_in_days=20,
        aid_data={
            MedicalAid.NO_AID: (2, 40),
            MedicalAid.FIRST_AID: (100, 90),
        },
    )
    apply_recovery_to_runtime(rt, recovery, abs_impulse=1, allow_ctp_extend=True)
    assert rt.ctp_deadline_abs_impulse == 400


class _FixedRng:
    def __init__(self, value: int) -> None:
        self.value = value

    def randint(self, a: int, b: int) -> int:
        return self.value


def test_disable_arm_one_hand_alm() -> None:
    rt = TokenCombatRuntime(disabled_arm_left=True)
    assert one_hand_alm_for_shot(rt, _rifle()) == SituationStanceModifier4B.FIRING_RIFLE_WITH_ONE_HAND
    assert one_hand_alm_for_shot(rt, _pistol()) == SituationStanceModifier4B.FIRING_PISTOL_WITH_ONE_HAND
    rt.disabled_arm_right = True
    assert one_hand_alm_for_shot(rt, _rifle()) is None
    ok, _ = can_fire_weapon(rt)
    assert ok is False


def test_disable_leg_crawl_and_spine_blocks() -> None:
    rt = TokenCombatRuntime()
    apply_disable_flags(rt, AdvancedHitLocation.THIGH_BONE_LEFT)
    assert rt.disabled_leg is True
    assert rt.stance == "prone"
    blocked = can_perform_action(rt, "prone_to_standing")
    assert blocked is not None and not blocked.success

    rt2 = TokenCombatRuntime()
    apply_disable_flags(rt2, AdvancedHitLocation.NECK_SPINE_SIDE)
    assert rt2.disabled_head_spine is True
    assert can_perform_action(rt2, "move") is not None
    assert can_fire_weapon(rt2)[0] is False


def test_ht20_ca_penalty_book_example() -> None:
    assert wound_ca_penalty_from_healing_days(41) == 2.0
    rt = TokenCombatRuntime(
        incap_effect="Stunned",
        incap_remaining_phases=1,
        healing_days=41,
    )
    tick_incap_phase(rt)
    assert rt.incap_effect is None
    assert rt.wound_ca_penalty == 2.0
    assert effective_impulse_ac(5.0, rt) == 3.0


def test_refill_zero_for_dead_and_ko() -> None:
    engine, _ = _engine()
    rt = engine.get_runtime("t1")
    rt.is_dead = True
    engine.refill_impulse_ac()
    assert rt.ac_remaining == 0.0

    rt.is_dead = False
    rt.incap_effect = "Knocked Out"
    engine.refill_impulse_ac()
    assert rt.ac_remaining == 0.0


def test_apply_shot_wounds_sets_incap() -> None:
    engine, tok = _engine()
    char = engine.characters[tok.character_name]
    result = ShotResult(
        hit=True,
        eal=10,
        odds=50,
        roll=10,
        target=char,
        damage_result=DamageResult(
            location=AdvancedHitLocation.ARM_BONE_SHOULDER_LEFT,
            damage=5,
            is_disabled=True,
        ),
        incapacitation_effect=IncapacitationEffect.STUNNED,
        incapacitation_time_phases=3,
        recovery=Recovery(
            healing_time_in_days=20,
            aid_data={MedicalAid.NO_AID: (100, 80)},
        ),
    )
    apply_shot_wounds(
        [result],
        engine.tokens,
        engine.impulse_combat.token_runtime,
        engine.characters,
        abs_impulse=0,
    )
    rt = engine.get_runtime("t1")
    assert rt.disabled_arm_left is True
    assert rt.incap_effect == "Stunned"
    assert rt.incap_remaining_phases == 3
    assert rt.ctp_deadline_abs_impulse == 400


def test_set_medical_aid_host_action() -> None:
    engine, _ = _engine()
    char = engine.characters["T"]
    char.physical_damage_total = 20
    rt = engine.get_runtime("t1")
    rt.wound_onset_abs_impulse = 0
    result = engine.apply_action(
        "t1", "set_medical_aid", {"medical_aid": "First Aid"}, is_host=True
    )
    assert result.success
    assert rt.medical_aid == "First Aid"
    guest = engine.apply_action(
        "t1", "set_medical_aid", {"medical_aid": "Aid Station"}, player_id="p1", is_host=False
    )
    assert not guest.success


def test_ko_blocks_duck() -> None:
    rt = TokenCombatRuntime(incap_effect="Knocked Out", ac_remaining=0)
    blocked = can_perform_action(rt, "duck")
    assert blocked is not None and not blocked.success
    assert can_perform_action(rt, "skip_impulse") is None


def test_flee_geometry_blocks_closing_move() -> None:
    from phoenix_command.simulations.map_wounds import move_closes_on_enemy

    tokens = TokenState()
    tokens.placements["a"] = TokenPlacement(
        token_id="a", character_name="A", q=0, r=0, side_id="alpha"
    )
    tokens.placements["b"] = TokenPlacement(
        token_id="b", character_name="B", q=2, r=0, side_id="bravo"
    )
    runtime = {"a": TokenCombatRuntime(), "b": TokenCombatRuntime()}
    # Toward enemy (east)
    assert move_closes_on_enemy(0, 0, 1, 0, "alpha", "a", tokens, runtime) is True
    # Away / lateral west
    assert move_closes_on_enemy(0, 0, -1, 0, "alpha", "a", tokens, runtime) is False


def test_engine_disoriented_cannot_close() -> None:
    engine, tok = _engine()
    enemy = TokenPlacement(
        token_id="e1", character_name="Enemy", q=2, r=0, side_id="bravo"
    )
    engine.tokens.placements["e1"] = enemy
    engine.impulse_combat.token_runtime["e1"] = TokenCombatRuntime()
    tok.side_id = "alpha"
    rt = engine.get_runtime("t1")
    rt.incap_effect = "Disoriented"
    rt.ac_remaining = 5.0
    bad = engine.apply_action("t1", "move", {"target_q": 1, "target_r": 0})
    assert not bad.success
    good = engine.apply_action("t1", "move", {"target_q": -1, "target_r": 0})
    assert good.success
