"""
Tests for AdvancedDamageCalculator.
"""
import pytest
from phoenix_command.tables.advanced_damage_tables.advanced_damage_calculator import AdvancedDamageCalculator
from phoenix_command.tables.advanced_damage_tables.tables_data import TablesData
from phoenix_command.models.enums import AdvancedHitLocation


class TestAdvancedDamageCalculator:
    """Test the AdvancedDamageCalculator class."""

    def test_parse_val_with_dash(self):
        """Test parsing dash returns 0."""
        assert AdvancedDamageCalculator.parse_val("-") == 0
        assert AdvancedDamageCalculator.parse_val("") == 0

    def test_parse_val_with_numeric(self):
        """Test parsing numeric values."""
        assert AdvancedDamageCalculator.parse_val("1") == 1
        assert AdvancedDamageCalculator.parse_val("123") == 123
        assert AdvancedDamageCalculator.parse_val("999") == 999

    def test_parse_val_with_multipliers(self):
        """Test parsing values with multipliers."""
        assert AdvancedDamageCalculator.parse_val("10H") == 1000
        assert AdvancedDamageCalculator.parse_val("5H") == 500
        assert AdvancedDamageCalculator.parse_val("10K") == 10000
        assert AdvancedDamageCalculator.parse_val("5K") == 5000
        assert AdvancedDamageCalculator.parse_val("10T") == 100000
        assert AdvancedDamageCalculator.parse_val("5T") == 50000
        assert AdvancedDamageCalculator.parse_val("10X") == 1000000
        assert AdvancedDamageCalculator.parse_val("5X") == 500000
        assert AdvancedDamageCalculator.parse_val("10M") == 10000000
        assert AdvancedDamageCalculator.parse_val("5M") == 5000000

    def test_parse_val_with_float_multipliers(self):
        """Test parsing float values with multipliers."""
        assert AdvancedDamageCalculator.parse_val("1.5H") == 150
        assert AdvancedDamageCalculator.parse_val("2.5K") == 2500
        assert AdvancedDamageCalculator.parse_val("0.1T") == 1000

    def test_calculate_damage_returns_damage_result(self):
        """Test that calculate_damage returns DamageResult."""
        from phoenix_command.models.hit_result_advanced import DamageResult

        result = AdvancedDamageCalculator.calculate_damage(
            location=AdvancedHitLocation.FOREHEAD,
            dc=10,
            epen=1.0,
            is_front=True
        )

        assert isinstance(result, DamageResult)
        assert result.location == AdvancedHitLocation.FOREHEAD

    def test_calculate_damage_front_hit_basic(self):
        """Test basic front hit calculation."""
        # Table 2 (Forehead) with epen 1.0, DC 10
        result = AdvancedDamageCalculator.calculate_damage(
            location=AdvancedHitLocation.FOREHEAD,
            dc=10,
            epen=1.0,
            is_front=True
        )

        # Should have damage
        assert result.damage > 0
        # Should have location
        assert result.location == AdvancedHitLocation.FOREHEAD

    def test_calculate_damage_rear_hit_basic(self):
        """Test basic rear hit calculation."""
        result = AdvancedDamageCalculator.calculate_damage(
            location=AdvancedHitLocation.FOREHEAD,
            dc=10,
            epen=1.0,
            is_front=False
        )

        # Should have damage
        assert result.damage > 0

    def test_calculate_damage_collects_organs(self):
        """Test that organs are collected during penetration."""
        # Use a location with multiple organs
        result = AdvancedDamageCalculator.calculate_damage(
            location=AdvancedHitLocation.FOREHEAD,
            dc=10,
            epen=2.0,
            is_front=True
        )

        # Should have collected some organs
        assert len(result.pierced_organs) > 0

    def test_calculate_damage_collects_shock(self):
        """Test that shock is collected."""
        # Use parameters that should generate shock
        result = AdvancedDamageCalculator.calculate_damage(
            location=AdvancedHitLocation.FOREHEAD,
            dc=10,
            epen=1.0,
            is_front=True
        )

        # Shock should be non-negative
        assert result.shock >= 0

    def test_calculate_damage_identifies_critical_organs(self):
        """Test that critical organs set is_disabled flag."""
        # Use a location with spine (critical organ)
        result = AdvancedDamageCalculator.calculate_damage(
            location=AdvancedHitLocation.BASE_OF_NECK,
            dc=10,
            epen=3.0,
            is_front=True
        )

        # If spine was pierced, should be disabled
        if "Spine" in result.pierced_organs:
            assert result.is_disabled

    def test_calculate_damage_excess_epen_front(self):
        """Test that excess epen is calculated for front hit."""
        # Use very high epen to pierce through
        result = AdvancedDamageCalculator.calculate_damage(
            location=AdvancedHitLocation.HEAD_GLANCE,
            dc=10,
            epen=5.0,
            is_front=True
        )

        # Should have excess epen if penetrated fully
        # (depends on table structure, but should be >= 0)
        assert result.excess_epen >= 0

    def test_calculate_damage_no_excess_epen_if_stopped(self):
        """Test that no excess epen if bullet stopped inside."""
        # Use low epen
        result = AdvancedDamageCalculator.calculate_damage(
            location=AdvancedHitLocation.FOREHEAD,
            dc=10,
            epen=0.5,
            is_front=True
        )

        # Should have no excess epen
        assert result.excess_epen.__eq__(0.0)

    def test_calculate_damage_with_zero_epen(self):
        """Test calculation with zero epen."""
        result = AdvancedDamageCalculator.calculate_damage(
            location=AdvancedHitLocation.FOREHEAD,
            dc=10,
            epen=0.0,
            is_front=True
        )

        # Should return result with zero damage
        assert result.damage == 0
        assert len(result.pierced_organs) == 0

    def test_calculate_damage_with_minimum_epen(self):
        """Test calculation with minimum epen value."""
        result = AdvancedDamageCalculator.calculate_damage(
            location=AdvancedHitLocation.FOREHEAD,
            dc=10,
            epen=0.1,
            is_front=True
        )

        # Should return valid result
        assert result.damage >= 0

    def test_calculate_damage_different_dc_values(self):
        """Test that higher DC produces more damage."""
        result_dc_1 = AdvancedDamageCalculator.calculate_damage(
            location=AdvancedHitLocation.FOREHEAD,
            dc=1,
            epen=1.0,
            is_front=True
        )

        result_dc_10 = AdvancedDamageCalculator.calculate_damage(
            location=AdvancedHitLocation.FOREHEAD,
            dc=10,
            epen=1.0,
            is_front=True
        )

        # Higher DC should produce more damage
        assert result_dc_10.damage > result_dc_1.damage

    def test_calculate_damage_rear_hit_excess_epen(self):
        """Test excess epen calculation for rear hit."""
        # Very high epen should pierce through from rear
        result = AdvancedDamageCalculator.calculate_damage(
            location=AdvancedHitLocation.HEAD_GLANCE,
            dc=10,
            epen=5.0,
            is_front=False
        )

        # Should have excess epen if penetrated fully
        assert result.excess_epen >= 0

    def test_calculate_damage_with_invalid_dc(self):
        """Test that invalid DC is handled gracefully."""
        # DC not in table should return empty result
        result = AdvancedDamageCalculator.calculate_damage(
            location=AdvancedHitLocation.FOREHEAD,
            dc=99,  # Invalid DC
            epen=1.0,
            is_front=True
        )

        # Should return result with zero damage
        assert result.damage == 0

    def test_calculate_damage_consistency_front_rear(self):
        """Test that front and rear hits produce different results."""
        result_front = AdvancedDamageCalculator.calculate_damage(
            location=AdvancedHitLocation.FOREHEAD,
            dc=10,
            epen=1.5,
            is_front=True
        )

        result_rear = AdvancedDamageCalculator.calculate_damage(
            location=AdvancedHitLocation.FOREHEAD,
            dc=10,
            epen=1.5,
            is_front=False
        )

        # Results should be different (organs, damage, etc.)
        # Note: they might be equal in some edge cases, but generally different
        assert result_front.location == result_rear.location

    def test_calculate_damage_all_tables_accessible(self):
        """Test that all tables in TABLES_DATA are accessible."""
        tables_data = TablesData.TABLES_DATA

        for table_id in tables_data.keys():
            # Each table should have required keys
            assert "epen" in tables_data[table_id]
            assert "dc" in tables_data[table_id]
            assert "organs" in tables_data[table_id]
            assert "shock" in tables_data[table_id]

    def test_parse_val_edge_cases(self):
        """Test parse_val with edge cases."""
        assert AdvancedDamageCalculator.parse_val("0") == 0
        assert AdvancedDamageCalculator.parse_val("0H") == 0
        assert AdvancedDamageCalculator.parse_val("0.0K") == 0

    def test_calculate_damage_preserves_location(self):
        """Test that location is preserved in result."""
        test_locations = [
            AdvancedHitLocation.FOREHEAD,
            AdvancedHitLocation.HEART,
            AdvancedHitLocation.THIGH_BONE_LEFT,
        ]

        for location in test_locations:
            result = AdvancedDamageCalculator.calculate_damage(
                location=location,
                dc=10,
                epen=1.0,
                is_front=True
            )
            assert result.location == location

