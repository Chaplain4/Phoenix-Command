"""Tests for §5.12 Knock Down and §6.9 Recoil Recovery tables."""

from phoenix_command.models.character import Character
from phoenix_command.models.enums import (
    AdvancedHitLocation,
    ArmorMaterial,
    SituationStanceModifier4B,
    TargetExposure,
    TargetOrientation,
    VisibilityModifier4C,
)
from phoenix_command.models.gear import AmmoType, Armor, ArmorLayer, ArmorProtectionData, BallisticData
from phoenix_command.models.hit_result_advanced import ShotParameters
from phoenix_command.simulations.combat_simulator_utils import CombatSimulatorUtils
from phoenix_command.simulations.map_knockdown import (
    apply_knock_down_effects,
    second_shot_aim_bonus,
)
from phoenix_command.session.domains.impulse_combat_state import TokenCombatRuntime
from phoenix_command.tables.advanced_damage_tables.table_1_get_hit_location import (
    Table1AdvancedDamageHitLocation,
)
from phoenix_command.tables.advanced_rules.knock_down import (
    KIND_AC_1,
    KIND_AC_2,
    KIND_OFF_FEET,
    explosive_knock_down,
    infantry_armor_class,
    location_band,
    projectile_knock_down,
)
from phoenix_command.tables.advanced_rules.recoil_recovery import recoil_recovery_ac


def test_projectile_head_kd3_is_minus_2_ac() -> None:
    effect = projectile_knock_down(3, "head")
    assert effect.kind == KIND_AC_2
    assert effect.ac_penalty == 2
    assert not effect.off_feet


def test_projectile_body_19_off_feet() -> None:
    effect = projectile_knock_down(19, "body")
    assert effect.kind == KIND_OFF_FEET
    assert effect.off_feet


def test_location_band_head_and_arm() -> None:
    assert location_band(AdvancedHitLocation.FOREHEAD) == "head"
    assert location_band(AdvancedHitLocation.ARM_FLESH_LEFT) == "arm"
    assert location_band(AdvancedHitLocation.LUNG) == "body"
    assert location_band(AdvancedHitLocation.MISS) is None


def test_explosive_bc52_normal_minus_1() -> None:
    effect = explosive_knock_down(52, "normal")
    assert effect.kind == KIND_AC_1
    assert effect.ac_penalty == 1


def test_explosive_bc52_infantry_minus_1() -> None:
    """Both classes use the same Normal Infantry column."""
    effect = explosive_knock_down(52, "infantry")
    assert effect.kind == KIND_AC_1
    assert effect.ac_penalty == 1


def test_explosive_bc66_minus_2() -> None:
    assert explosive_knock_down(66, "normal").kind == KIND_AC_2
    assert explosive_knock_down(66, "infantry").kind == KIND_AC_2


def test_explosive_bc82_minus_4() -> None:
    from phoenix_command.tables.advanced_rules.knock_down import KIND_AC_4
    assert explosive_knock_down(82, "normal").kind == KIND_AC_4
    assert explosive_knock_down(82, "normal").ac_penalty == 4


def test_explosive_bc90_knock_down() -> None:
    assert explosive_knock_down(90, "normal").kind == KIND_OFF_FEET
    assert explosive_knock_down(90, "normal").off_feet


def test_explosive_bc49_none() -> None:
    assert explosive_knock_down(49, "normal").is_none()


def test_recoil_kd7_skill4_is_1_ac() -> None:
    assert recoil_recovery_ac(7, 4) == 1


def test_recoil_kd1_always_zero() -> None:
    assert recoil_recovery_ac(1, 0) == 0


def _char(**kwargs) -> Character:
    defaults = dict(
        name="T",
        strength=12,
        intelligence=10,
        will=11,
        health=12,
        agility=10,
        gun_combat_skill_level=4,
    )
    defaults.update(kwargs)
    return Character(**defaults)


def test_infantry_armor_class_helmet_only_is_normal_for_concussion() -> None:
    from phoenix_command.item_database.armor import helmet_locs

    c = _char()
    helm = Armor(
        name="Helmet",
        weight=1.0,
        protection={
            (loc, True): ArmorProtectionData(
                layers=[
                    ArmorLayer(
                        material=ArmorMaterial.STEEL,
                        protection_factor=5,
                        blunt_protection_factor=2,
                    )
                ]
            )
            for loc in helmet_locs
        },
    )
    c.add_gear(helm)
    assert infantry_armor_class(c, None) == "normal"


def test_infantry_armor_class_vest_pf_on_heart() -> None:
    c = _char()
    vest = Armor(
        name="Vest",
        weight=5.0,
        protection={
            (AdvancedHitLocation.HEART, True): ArmorProtectionData(
                layers=[
                    ArmorLayer(
                        material=ArmorMaterial.KEVLAR,
                        protection_factor=6,
                        blunt_protection_factor=3,
                    )
                ]
            )
        },
    )
    c.add_gear(vest)
    assert infantry_armor_class(c, None) == "infantry"
    assert infantry_armor_class(c, AdvancedHitLocation.HEART, True) == "infantry"
    assert infantry_armor_class(c, AdvancedHitLocation.ARM_FLESH_LEFT, True) == "normal"


def test_process_hit_armor_stop_still_sets_knock_down(monkeypatch) -> None:
    monkeypatch.setattr(
        Table1AdvancedDamageHitLocation,
        "get_hit_location",
        staticmethod(lambda *_a, **_k: AdvancedHitLocation.FOREHEAD),
    )
    target = _char()
    armor = Armor(
        name="Faceplate",
        weight=1.0,
        protection={
            (AdvancedHitLocation.FOREHEAD, True): ArmorProtectionData(
                layers=[
                    ArmorLayer(
                        material=ArmorMaterial.STEEL,
                        protection_factor=50,
                        blunt_protection_factor=10,
                    )
                ]
            )
        },
    )
    target.add_gear(armor)
    ammo = AmmoType(
        name="Pistol",
        weight=0.0,
        ballistic_data=[
            BallisticData(range_hexes=10, penetration=5.0, damage_class=2),
            BallisticData(range_hexes=100, penetration=5.0, damage_class=2),
        ],
    )
    params = ShotParameters(
        aim_time_ac=2,
        situation_stance_modifiers=[SituationStanceModifier4B.STANDING],
        visibility_modifiers=[VisibilityModifier4C.GOOD_VISIBILITY],
        target_orientation=TargetOrientation.FRONT_REAR,
    )
    log: list[str] = []
    _dmg, _i, _r, _t, kd = CombatSimulatorUtils.process_hit(
        target, ammo, 10, TargetExposure.STANDING_EXPOSED, params, True, log,
        weapon_knock_down=3,
    )
    assert kd is not None
    assert kd.kind == KIND_AC_2
    assert any("Knock down" in line for line in log)


def test_process_concussion_sets_explosive_kd() -> None:
    target = _char()
    log: list[str] = []
    result = CombatSimulatorUtils.process_concussion_damage(target, 52, [], log)
    assert result is not None
    assert result.knock_down is not None
    assert result.knock_down.kind == KIND_AC_1


def test_off_feet_runtime_falling_prone() -> None:
    rt = TokenCombatRuntime(ac_remaining=3.0, stance="standing")
    apply_knock_down_effects(
        rt,
        [projectile_knock_down(19, "body")],
    )
    assert rt.stance == "prone"
    assert rt.knockdown_phase == "falling"
    assert rt.hands_free is False
    assert rt.ac_remaining == 0.0


def test_second_shot_bonus_same_hex() -> None:
    rt = TokenCombatRuntime(
        last_shot_q=1,
        last_shot_r=2,
        last_shot_layer_id="ground",
        firing_stance_held=True,
    )
    assert second_shot_aim_bonus(rt, 1, 2, "ground") == 1
    assert second_shot_aim_bonus(rt, 0, 2, "ground") == 0
    rt.firing_stance_held = False
    assert second_shot_aim_bonus(rt, 1, 2, "ground") == 0
