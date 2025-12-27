"""
Test for table 64 (SHIN_BONE_SIDE_LEFT/RIGHT).

Table contains:
- EPEN thresholds: [0.1, 0.2, 1.1, 1.9, 2.8, 3.7, 4.6, 8.8, 8.9, 9.1, 9.2]
- Shock: {1.1: 10, 1.9: 15, 2.8: 20, 3.7: 30, 4.6: 40, 8.8: 80}
- Organs:
    - (0.1, 0.2, "Flesh", False)
    - (1.1, 8.8, "Tibia", True) - disables location
    - (8.9, 9.2, "Flesh", False)
"""

import pytest
from phoenix_command.models.enums import AdvancedHitLocation
from phoenix_command.tables.advanced_damage_tables.advanced_damage_calculator import AdvancedDamageCalculator


def test_table64_front_shot_before_first_threshold():
    """Test front shot before first threshold (EPEN < 0.1)"""
    location = AdvancedHitLocation.SHIN_BONE_SIDE_LEFT

    result = AdvancedDamageCalculator.calculate_damage(location, dc=10, epen=0.0, is_front=True)
    assert result.damage == 0
    assert result.shock == 0
    assert result.pierced_organs == []
    assert result.is_disabled is False
    assert result.excess_epen == 0.0


def test_table64_front_shot_flesh_only():
    """Test front shot through first Flesh layer (0.1-0.2)"""
    location = AdvancedHitLocation.SHIN_BONE_SIDE_LEFT

    result = AdvancedDamageCalculator.calculate_damage(location, dc=10, epen=0.1, is_front=True)
    assert result.damage == 68
    assert result.shock == 0
    assert result.pierced_organs == ["Flesh"]
    assert result.is_disabled is False
    assert result.excess_epen == 0.0

    result = AdvancedDamageCalculator.calculate_damage(location, dc=10, epen=0.2, is_front=True)
    assert result.damage == 114
    assert result.shock == 0
    assert result.pierced_organs == ["Flesh"]
    assert result.is_disabled is False


def test_table64_front_shot_tibia_entry():
    """Test front shot entering Tibia (EPEN=1.1)"""
    location = AdvancedHitLocation.SHIN_BONE_SIDE_LEFT

    result = AdvancedDamageCalculator.calculate_damage(location, dc=10, epen=1.1, is_front=True)
    assert result.damage == 175
    assert result.shock == 10
    assert result.pierced_organs == ["Flesh", "Tibia"]
    assert result.is_disabled is True
    assert result.excess_epen == 0.0

    result = AdvancedDamageCalculator.calculate_damage(location, dc=5, epen=1.1, is_front=True)
    assert result.damage == 10
    assert result.shock == 10
    assert result.is_disabled is True


def test_table64_front_shot_tibia_progressive_shock():
    """Test progressive shock increase through Tibia"""
    location = AdvancedHitLocation.SHIN_BONE_SIDE_LEFT

    result = AdvancedDamageCalculator.calculate_damage(location, dc=10, epen=1.9, is_front=True)
    assert result.damage == 175
    assert result.shock == 15
    assert result.is_disabled is True

    result = AdvancedDamageCalculator.calculate_damage(location, dc=10, epen=2.8, is_front=True)
    assert result.damage == 175
    assert result.shock == 20

    result = AdvancedDamageCalculator.calculate_damage(location, dc=10, epen=3.7, is_front=True)
    assert result.damage == 175
    assert result.shock == 30

    result = AdvancedDamageCalculator.calculate_damage(location, dc=10, epen=4.6, is_front=True)
    assert result.damage == 175
    assert result.shock == 40

    result = AdvancedDamageCalculator.calculate_damage(location, dc=10, epen=8.8, is_front=True)
    assert result.damage == 175
    assert result.shock == 80
    assert result.is_disabled is True


def test_table64_front_shot_exit_flesh():
    """Test front shot exiting through rear Flesh layer"""
    location = AdvancedHitLocation.SHIN_BONE_SIDE_LEFT

    result = AdvancedDamageCalculator.calculate_damage(location, dc=10, epen=8.9, is_front=True)
    assert result.damage == 175
    assert result.shock == 80
    assert result.pierced_organs == ["Flesh", "Tibia", "Flesh"]
    assert result.is_disabled is True

    result = AdvancedDamageCalculator.calculate_damage(location, dc=10, epen=9.2, is_front=True)
    assert result.damage == 175
    assert result.shock == 80
    assert result.pierced_organs == ["Flesh", "Tibia", "Flesh"]
    assert result.is_disabled is True
    assert result.excess_epen == 0.0


def test_table64_front_shot_overpenetration():
    """Test overpenetration with excess EPEN"""
    location = AdvancedHitLocation.SHIN_BONE_SIDE_LEFT

    result = AdvancedDamageCalculator.calculate_damage(location, dc=10, epen=9.5, is_front=True)
    assert result.damage == 175
    assert result.shock == 80
    assert result.is_disabled is True
    assert result.excess_epen == pytest.approx(0.3, abs=1e-6)

    result = AdvancedDamageCalculator.calculate_damage(location, dc=10, epen=10.0, is_front=True)
    assert result.excess_epen == pytest.approx(0.8, abs=1e-6)


def test_table64_rear_shot_before_first_threshold():
    """Test rear shot before first threshold"""
    location = AdvancedHitLocation.SHIN_BONE_SIDE_LEFT

    result = AdvancedDamageCalculator.calculate_damage(location, dc=10, epen=0.0, is_front=False)
    assert result.damage == 0
    assert result.shock == 0
    assert result.pierced_organs == []
    assert result.is_disabled is False


def test_table64_rear_shot_rear_flesh():
    """Test rear shot through rear Flesh layer"""
    location = AdvancedHitLocation.SHIN_BONE_SIDE_LEFT

    result = AdvancedDamageCalculator.calculate_damage(location, dc=3, epen=0.1, is_front=False)
    assert result.damage == 12
    assert result.shock == 0
    assert result.pierced_organs == ["Flesh"]
    assert result.is_disabled is False


def test_table64_rear_shot_into_tibia():
    """Test rear shot entering Tibia"""
    location = AdvancedHitLocation.SHIN_BONE_SIDE_LEFT

    result = AdvancedDamageCalculator.calculate_damage(location, dc=10, epen=1.1, is_front=False)
    assert result.damage == 0
    assert result.shock == 40
    assert result.pierced_organs == ["Flesh", "Tibia"]
    assert result.is_disabled is True


def test_table64_rear_shot_progressive_damage():
    """Test progressive damage increase with rear shot"""
    location = AdvancedHitLocation.SHIN_BONE_SIDE_LEFT

    result = AdvancedDamageCalculator.calculate_damage(location, dc=10, epen=4.6, is_front=False)
    assert result.shock == 40
    assert result.is_disabled is True

    result = AdvancedDamageCalculator.calculate_damage(location, dc=10, epen=8.8, is_front=False)
    assert result.damage == 61
    assert result.shock == 80
    assert result.is_disabled is True


def test_table64_rear_shot_through_all_flesh():
    """Test rear shot through all Flesh layers"""
    location = AdvancedHitLocation.SHIN_BONE_SIDE_LEFT

    result = AdvancedDamageCalculator.calculate_damage(location, dc=10, epen=9.1, is_front=False)
    assert result.damage == 175
    assert result.shock == 80
    assert result.pierced_organs == ["Flesh", "Tibia", "Flesh"]
    assert result.is_disabled is True

    result = AdvancedDamageCalculator.calculate_damage(location, dc=10, epen=9.2, is_front=False)
    assert result.damage == 175
    assert result.shock == 80


def test_table64_rear_shot_overpenetration():
    """Test rear shot overpenetration with excess EPEN"""
    location = AdvancedHitLocation.SHIN_BONE_SIDE_LEFT

    result = AdvancedDamageCalculator.calculate_damage(location, dc=10, epen=9.5, is_front=False)
    assert result.excess_epen == pytest.approx(0.3, abs=1e-6)

    result = AdvancedDamageCalculator.calculate_damage(location, dc=10, epen=10.0, is_front=False)
    assert result.excess_epen == pytest.approx(0.8, abs=1e-6)


def test_table64_dc_scaling():
    """Test damage scaling for different DC values"""
    location = AdvancedHitLocation.SHIN_BONE_SIDE_LEFT

    result = AdvancedDamageCalculator.calculate_damage(location, dc=1, epen=1.1, is_front=True)
    assert result.damage == 1
    assert result.shock == 10

    result = AdvancedDamageCalculator.calculate_damage(location, dc=5, epen=1.1, is_front=True)
    assert result.damage == 10

    result = AdvancedDamageCalculator.calculate_damage(location, dc=10, epen=1.1, is_front=True)
    assert result.damage == 175


def test_table64_front_shot_dc_variations_flesh():
    """Test various DC values for Flesh (EPEN=0.1)"""
    location = AdvancedHitLocation.SHIN_BONE_SIDE_LEFT

    result = AdvancedDamageCalculator.calculate_damage(location, dc=1, epen=0.1, is_front=True)
    assert result.damage == 0
    assert result.shock == 0

    result = AdvancedDamageCalculator.calculate_damage(location, dc=2, epen=0.1, is_front=True)
    assert result.damage == 0

    result = AdvancedDamageCalculator.calculate_damage(location, dc=3, epen=0.1, is_front=True)
    assert result.damage == 1

    result = AdvancedDamageCalculator.calculate_damage(location, dc=4, epen=0.1, is_front=True)
    assert result.damage == 1

    result = AdvancedDamageCalculator.calculate_damage(location, dc=7, epen=0.1, is_front=True)
    assert result.damage == 8


def test_table64_front_shot_dc_variations_at_threshold_02():
    """Test various DC values at EPEN=0.2 threshold"""
    location = AdvancedHitLocation.SHIN_BONE_SIDE_LEFT

    result = AdvancedDamageCalculator.calculate_damage(location, dc=1, epen=0.2, is_front=True)
    assert result.damage == 0
    assert result.shock == 0

    result = AdvancedDamageCalculator.calculate_damage(location, dc=2, epen=0.2, is_front=True)
    assert result.damage == 1

    result = AdvancedDamageCalculator.calculate_damage(location, dc=5, epen=0.2, is_front=True)
    assert result.damage == 4

    result = AdvancedDamageCalculator.calculate_damage(location, dc=9, epen=0.2, is_front=True)
    assert result.damage == 53


def test_table64_front_shot_between_flesh_and_tibia():
    """Test EPEN between Flesh and Tibia (0.5)"""
    location = AdvancedHitLocation.SHIN_BONE_SIDE_LEFT

    result = AdvancedDamageCalculator.calculate_damage(location, dc=10, epen=0.5, is_front=True)
    assert result.damage == 114
    assert result.shock == 0
    assert result.pierced_organs == ["Flesh"]
    assert result.is_disabled is False


def test_table64_front_shot_tibia_dc_variations():
    """Test various DC values when entering Tibia (EPEN=1.1)"""
    location = AdvancedHitLocation.SHIN_BONE_SIDE_LEFT

    result = AdvancedDamageCalculator.calculate_damage(location, dc=1, epen=1.1, is_front=True)
    assert result.damage == 1
    assert result.shock == 10
    assert result.is_disabled is True

    result = AdvancedDamageCalculator.calculate_damage(location, dc=3, epen=1.1, is_front=True)
    assert result.damage == 3
    assert result.shock == 10

    result = AdvancedDamageCalculator.calculate_damage(location, dc=6, epen=1.1, is_front=True)
    assert result.damage == 14
    assert result.shock == 10

    result = AdvancedDamageCalculator.calculate_damage(location, dc=9, epen=1.1, is_front=True)
    assert result.damage == 130
    assert result.shock == 10


def test_table64_front_shot_tibia_intermediate():
    """Test intermediate value within Tibia (EPEN=1.5)"""
    location = AdvancedHitLocation.SHIN_BONE_SIDE_LEFT

    result = AdvancedDamageCalculator.calculate_damage(location, dc=10, epen=1.5, is_front=True)
    assert result.damage == 175
    assert result.shock == 10
    assert result.pierced_organs == ["Flesh", "Tibia"]
    assert result.is_disabled is True


def test_table64_front_shot_shock_progression_dc_variations():
    """Test shock progression with various DC values"""
    location = AdvancedHitLocation.SHIN_BONE_SIDE_LEFT

    result = AdvancedDamageCalculator.calculate_damage(location, dc=3, epen=1.9, is_front=True)
    assert result.damage == 5
    assert result.shock == 15
    assert result.is_disabled is True

    result = AdvancedDamageCalculator.calculate_damage(location, dc=5, epen=2.8, is_front=True)
    assert result.damage == 27
    assert result.shock == 20

    result = AdvancedDamageCalculator.calculate_damage(location, dc=7, epen=3.7, is_front=True)
    assert result.damage == 136
    assert result.shock == 30

    result = AdvancedDamageCalculator.calculate_damage(location, dc=4, epen=4.6, is_front=True)
    assert result.damage == 31
    assert result.shock == 40


def test_table64_front_shot_intermediate_values():
    """Test intermediate values between shock thresholds"""
    location = AdvancedHitLocation.SHIN_BONE_SIDE_LEFT

    result = AdvancedDamageCalculator.calculate_damage(location, dc=10, epen=2.0, is_front=True)
    assert result.shock == 15
    assert result.is_disabled is True

    result = AdvancedDamageCalculator.calculate_damage(location, dc=10, epen=3.0, is_front=True)
    assert result.shock == 20

    result = AdvancedDamageCalculator.calculate_damage(location, dc=10, epen=4.0, is_front=True)
    assert result.shock == 30

    result = AdvancedDamageCalculator.calculate_damage(location, dc=10, epen=5.0, is_front=True)
    assert result.shock == 40


def test_table64_front_shot_max_shock():
    """Test maximum shock with various DC values"""
    location = AdvancedHitLocation.SHIN_BONE_SIDE_LEFT

    result = AdvancedDamageCalculator.calculate_damage(location, dc=1, epen=8.8, is_front=True)
    assert result.damage == 3
    assert result.shock == 80
    assert result.is_disabled is True

    result = AdvancedDamageCalculator.calculate_damage(location, dc=3, epen=8.8, is_front=True)
    assert result.damage == 37
    assert result.shock == 80

    result = AdvancedDamageCalculator.calculate_damage(location, dc=5, epen=8.8, is_front=True)
    assert result.damage == 129
    assert result.shock == 80


def test_table64_front_shot_transition_to_exit_flesh():
    """Test transition to exit Flesh layer"""
    location = AdvancedHitLocation.SHIN_BONE_SIDE_LEFT

    result = AdvancedDamageCalculator.calculate_damage(location, dc=10, epen=8.85, is_front=True)
    assert result.pierced_organs == ["Flesh", "Tibia"]
    assert result.shock == 80

    result = AdvancedDamageCalculator.calculate_damage(location, dc=10, epen=8.9, is_front=True)
    assert result.pierced_organs == ["Flesh", "Tibia", "Flesh"]
    assert result.shock == 80

    result = AdvancedDamageCalculator.calculate_damage(location, dc=10, epen=9.0, is_front=True)
    assert result.pierced_organs == ["Flesh", "Tibia", "Flesh"]
    assert result.damage == 175


def test_table64_front_shot_exit_flesh_dc_variations():
    """Test exit through rear Flesh with various DC values"""
    location = AdvancedHitLocation.SHIN_BONE_SIDE_LEFT

    result = AdvancedDamageCalculator.calculate_damage(location, dc=2, epen=8.9, is_front=True)
    assert result.damage == 15
    assert result.shock == 80

    result = AdvancedDamageCalculator.calculate_damage(location, dc=4, epen=8.9, is_front=True)
    assert result.damage == 109

    result = AdvancedDamageCalculator.calculate_damage(location, dc=1, epen=9.1, is_front=True)
    assert result.damage == 8

    result = AdvancedDamageCalculator.calculate_damage(location, dc=3, epen=9.1, is_front=True)
    assert result.damage == 96


def test_table64_front_shot_final_threshold():
    """Test final threshold and overpenetration"""
    location = AdvancedHitLocation.SHIN_BONE_SIDE_LEFT

    result = AdvancedDamageCalculator.calculate_damage(location, dc=10, epen=9.15, is_front=True)
    assert result.excess_epen == 0.0
    assert result.shock == 80

    result = AdvancedDamageCalculator.calculate_damage(location, dc=2, epen=9.2, is_front=True)
    assert result.damage == 31
    assert result.excess_epen == 0.0

    result = AdvancedDamageCalculator.calculate_damage(location, dc=3, epen=9.2, is_front=True)
    assert result.damage == 108


def test_table64_rear_shot_initial_flesh():
    """Test rear shot through initial Flesh layer"""
    location = AdvancedHitLocation.SHIN_BONE_SIDE_LEFT

    result = AdvancedDamageCalculator.calculate_damage(location, dc=1, epen=0.05, is_front=False)
    assert result.damage == 1
    assert result.shock == 0
    assert result.pierced_organs == ["Flesh"]
    assert result.is_disabled is False

    result = AdvancedDamageCalculator.calculate_damage(location, dc=3, epen=0.05, is_front=False)
    assert result.damage == 12

    result = AdvancedDamageCalculator.calculate_damage(location, dc=2, epen=0.15, is_front=False)
    assert result.damage == 16
    assert result.shock == 0

    result = AdvancedDamageCalculator.calculate_damage(location, dc=4, epen=0.15, is_front=False)
    assert result.damage == 66


def test_table64_rear_shot_into_tibia_variations():
    """Test rear shot into Tibia with various EPEN and DC"""
    location = AdvancedHitLocation.SHIN_BONE_SIDE_LEFT

    result = AdvancedDamageCalculator.calculate_damage(location, dc=2, epen=0.5, is_front=False)
    assert result.damage == 27
    assert result.shock == 40
    assert result.is_disabled is True

    result = AdvancedDamageCalculator.calculate_damage(location, dc=5, epen=0.5, is_front=False)
    assert result.damage == 122
    assert result.shock == 40

    result = AdvancedDamageCalculator.calculate_damage(location, dc=3, epen=1.1, is_front=False)
    assert result.damage == 93
    assert result.shock == 40

    result = AdvancedDamageCalculator.calculate_damage(location, dc=6, epen=1.1, is_front=False)
    assert result.damage == 96
    assert result.shock == 40


def test_table64_rear_shot_tibia_all_ranges():
    """Test rear shot through entire Tibia range"""
    location = AdvancedHitLocation.SHIN_BONE_SIDE_LEFT

    for epen in [0.5, 1.1, 1.5, 1.9, 2.0, 2.8, 3.0, 3.7, 4.0, 4.6]:
        result = AdvancedDamageCalculator.calculate_damage(location, dc=10, epen=epen, is_front=False)
        assert result.shock == 40, f"EPEN={epen} should give shock=40"
        assert result.is_disabled is True


def test_table64_rear_shot_increased_shock():
    """Test shock increase with rear shot"""
    location = AdvancedHitLocation.SHIN_BONE_SIDE_LEFT

    result = AdvancedDamageCalculator.calculate_damage(location, dc=2, epen=5.0, is_front=False)
    assert result.damage == 28
    assert result.shock == 50
    assert result.is_disabled is True

    result = AdvancedDamageCalculator.calculate_damage(location, dc=5, epen=5.0, is_front=False)
    assert result.damage == 136
    assert result.shock == 50


def test_table64_rear_shot_max_shock_variations():
    """Test maximum shock with rear shot at various DC"""
    location = AdvancedHitLocation.SHIN_BONE_SIDE_LEFT

    result = AdvancedDamageCalculator.calculate_damage(location, dc=1, epen=8.8, is_front=False)
    assert result.damage == 9
    assert result.shock == 80

    result = AdvancedDamageCalculator.calculate_damage(location, dc=3, epen=8.8, is_front=False)
    assert result.damage == 107
    assert result.shock == 80

    result = AdvancedDamageCalculator.calculate_damage(location, dc=7, epen=8.8, is_front=False)
    assert result.damage == 161
    assert result.shock == 80

    result = AdvancedDamageCalculator.calculate_damage(location, dc=10, epen=8.8, is_front=False)
    assert result.damage == 61
    assert result.shock == 80


def test_table64_rear_shot_transition_zones():
    """Test transition zones with rear shot"""
    location = AdvancedHitLocation.SHIN_BONE_SIDE_LEFT

    result = AdvancedDamageCalculator.calculate_damage(location, dc=5, epen=8.85, is_front=False)
    assert result.pierced_organs == ["Flesh", "Tibia"]
    assert result.damage == 171

    result = AdvancedDamageCalculator.calculate_damage(location, dc=5, epen=8.9, is_front=False)
    assert result.damage == 171

    result = AdvancedDamageCalculator.calculate_damage(location, dc=5, epen=9.0, is_front=False)
    assert result.pierced_organs == ["Flesh", "Tibia", "Flesh"]
    assert result.damage == 173


def test_table64_rear_shot_full_penetration():
    """Test full penetration with rear shot"""
    location = AdvancedHitLocation.SHIN_BONE_SIDE_LEFT

    result = AdvancedDamageCalculator.calculate_damage(location, dc=2, epen=9.1, is_front=False)
    assert result.damage == 31
    assert result.shock == 80
    assert result.pierced_organs == ["Flesh", "Tibia", "Flesh"]

    result = AdvancedDamageCalculator.calculate_damage(location, dc=4, epen=9.1, is_front=False)
    assert result.damage == 175

    result = AdvancedDamageCalculator.calculate_damage(location, dc=3, epen=9.2, is_front=False)
    assert result.damage == 108
    assert result.excess_epen == 0.0


def test_table64_rear_shot_overpenetration_variations():
    """Test excess EPEN with rear shot at various DC"""
    location = AdvancedHitLocation.SHIN_BONE_SIDE_LEFT

    result = AdvancedDamageCalculator.calculate_damage(location, dc=1, epen=9.5, is_front=False)
    assert result.damage == 9
    assert result.excess_epen == pytest.approx(0.3, abs=1e-6)

    result = AdvancedDamageCalculator.calculate_damage(location, dc=5, epen=9.5, is_front=False)
    assert result.damage == 175
    assert result.excess_epen == pytest.approx(0.3, abs=1e-6)

    result = AdvancedDamageCalculator.calculate_damage(location, dc=3, epen=10.0, is_front=False)
    assert result.damage == 108
    assert result.excess_epen == pytest.approx(0.8, abs=1e-6)


def test_table64_comprehensive_visual():
    """
    Visual test to verify all table 64 values.
    This test outputs complete table for manual verification.
    """

    location = AdvancedHitLocation.SHIN_BONE_SIDE_LEFT

    test_epen_values = [
        0.0, 0.05, 0.1, 0.15, 0.2, 0.5, 1.1, 1.5, 1.9, 2.0,
        2.8, 3.0, 3.7, 4.0, 4.6, 5.0, 8.8, 8.85, 8.9, 9.0,
        9.1, 9.15, 9.2, 9.5, 10.0,
    ]

    all_dc_values = list(range(1, 11))

    print("\n" + "="*150)
    print("TABLE 64: SHIN_BONE_SIDE_LEFT - FRONT SHOT (is_front=True)")
    print("="*150)

    header = f"{'EPEN':<8} | {'DC':<3} | {'Damage':<7} | {'Shock':<6} | {'Organs':<40} | {'Disabled':<9} | {'Excess EPEN':<12}"
    print(header)
    print("-" * 150)

    for epen in test_epen_values:
        for dc in all_dc_values:
            result = AdvancedDamageCalculator.calculate_damage(
                location=location,
                dc=dc,
                epen=epen,
                is_front=True
            )

            organs_str = ", ".join(result.pierced_organs) if result.pierced_organs else "-"
            if len(organs_str) > 40:
                organs_str = organs_str[:37] + "..."

            disabled_str = "Yes" if result.is_disabled else "No"
            excess_str = f"{result.excess_epen:.2f}" if result.excess_epen > 0 else "-"

            print(f"{epen:<8.2f} | {dc:<3} | {result.damage:<7} | {result.shock:<6} | {organs_str:<40} | {disabled_str:<9} | {excess_str:<12}")

    print("\n" + "="*150)
    print("TABLE 64: SHIN_BONE_SIDE_LEFT - REAR SHOT (is_front=False)")
    print("="*150)
    print(header)
    print("-" * 150)

    for epen in test_epen_values:
        for dc in all_dc_values:
            result = AdvancedDamageCalculator.calculate_damage(
                location=location,
                dc=dc,
                epen=epen,
                is_front=False
            )

            organs_str = ", ".join(result.pierced_organs) if result.pierced_organs else "-"
            if len(organs_str) > 40:
                organs_str = organs_str[:37] + "..."

            disabled_str = "Yes" if result.is_disabled else "No"
            excess_str = f"{result.excess_epen:.2f}" if result.excess_epen > 0 else "-"

            print(f"{epen:<8.2f} | {dc:<3} | {result.damage:<7} | {result.shock:<6} | {organs_str:<40} | {disabled_str:<9} | {excess_str:<12}")

    print("\n" + "="*150)
    print("\nTable 64 - Expected behavior:")
    print("- Organs: Flesh (0.1-0.2), Tibia [CRITICAL] (1.1-8.8), Flesh (8.9-9.2)")
    print("- Shock thresholds: 1.1→10, 1.9→15, 2.8→20, 3.7→30, 4.6→40, 8.8→80")
    print("- is_disabled should be True when bullet passes through Tibia (1.1-8.8)")
    print("- Excess EPEN appears when bullet completely penetrates (epen > 9.2)")
    print("="*150)


if __name__ == "__main__":
    test_table64_comprehensive_visual()
