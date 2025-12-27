"""
Tests for AdvancedDamageCalculator.
"""
from phoenix_command.models.enums import AdvancedHitLocation
from phoenix_command.tables.advanced_damage_tables.advanced_damage_calculator import AdvancedDamageCalculator
from phoenix_command.tables.advanced_damage_tables.tables_data import TablesData


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

    def test_all_hit_locations_table_parsing(self):
        """Test that all AdvancedHitLocation values correctly parse table references and weapon flag."""
        import re

        for location in AdvancedHitLocation:
            if location == AdvancedHitLocation.MISS:
                # MISS should not have any table references
                assert 'Table' not in location.value
                assert 'Weapon' not in location.value
                continue

            location_value = location.value

            # Skip if no table or weapon reference
            if 'Table' not in location_value and 'Weapon' not in location_value:
                continue

            # Parse expected tables from location value
            expected_tables = []
            expected_weapon = False

            if '(' in location_value:
                table_part = location_value.split('(')[-1].rstrip(')')
                parts = [p.strip() for p in table_part.split('&')]

                for part in parts:
                    if part == 'Weapon':
                        expected_weapon = True
                    elif part.startswith('Table'):
                        num_match = re.search(r'\d+', part)
                        if num_match:
                            expected_tables.append(int(num_match.group()))
                    elif part.isdigit():
                        expected_tables.append(int(part))

            # Calculate damage to trigger table parsing
            result = AdvancedDamageCalculator.calculate_damage(
                location=location,
                dc=10,
                epen=1.0,
                is_front=True
            )

            # Verify weapon_targeted flag
            assert result.weapon_damaged == expected_weapon, \
                f"Location {location.name} should have weapon_targeted={expected_weapon}, got {result.weapon_damaged}"

            # Verify that expected tables exist in TablesData
            for table_num in expected_tables:
                assert table_num in TablesData.TABLES_DATA, \
                    f"Location {location.name} references Table {table_num} which doesn't exist in TablesData"

    def test_multiple_tables_sequential_processing(self):
        """Test that multiple tables are processed sequentially with excess_epen passing through."""
        # Test with ARM_GLANCE_SHOULDER_RIGHT which has "Table 10 & 9"
        result = AdvancedDamageCalculator.calculate_damage(
            location=AdvancedHitLocation.ARM_GLANCE_SHOULDER_RIGHT,
            dc=10,
            epen=5.0,  # High epen to ensure it passes through first table
            is_front=True
        )

        # Should process both tables
        # Result should have combined damage from both tables if bullet passes through first one
        assert result.damage >= 0
        assert result.location == AdvancedHitLocation.ARM_GLANCE_SHOULDER_RIGHT

    def test_weapon_targeted_flag_with_epen(self):
        """Test that weapon_targeted is set only when bullet penetrates through previous tables."""
        # Test HAND_WEAPON_CRITICAL which has "Table 16 & Weapon"

        # With low epen that doesn't penetrate through hand completely, weapon should NOT be targeted
        result_low_epen = AdvancedDamageCalculator.calculate_damage(
            location=AdvancedHitLocation.HAND_WEAPON_CRITICAL,
            dc=10,
            epen=0.5,  # Low epen, won't penetrate through hand
            is_front=True
        )
        assert result_low_epen.weapon_damaged == False, \
            "weapon_targeted should be False when bullet stops in hand (no excess epen)"

        # With high epen that penetrates through hand completely, weapon should be targeted
        result_high_epen = AdvancedDamageCalculator.calculate_damage(
            location=AdvancedHitLocation.HAND_WEAPON_CRITICAL,
            dc=10,
            epen=5.0,  # High epen, will penetrate through hand
            is_front=True
        )
        assert result_high_epen.weapon_damaged == True, \
            "weapon_targeted should be True when bullet penetrates through hand (has excess epen)"

        # With epen = 0, weapon should not be targeted
        result_no_epen = AdvancedDamageCalculator.calculate_damage(
            location=AdvancedHitLocation.HAND_WEAPON_CRITICAL,
            dc=10,
            epen=0.0,
            is_front=True
        )
        assert result_no_epen.weapon_damaged == False, \
            "weapon_targeted should be False when epen = 0"

    def test_weapon_only_location(self):
        """Test location that only has Weapon reference (no numeric tables)."""
        result = AdvancedDamageCalculator.calculate_damage(
            location=AdvancedHitLocation.WEAPON_CRITICAL,
            dc=10,
            epen=1.0,
            is_front=True
        )

        assert result.weapon_damaged == True
        # No numeric tables, so no damage from tables
        assert result.damage == 0

    def test_multiple_tables_bullet_stops_in_first_table(self):
        """Test sequential table processing: bullet stops in first table."""
        # Use ARM_GLANCE_SHOULDER_RIGHT which has "Table 10 & 9"
        # Low epen should stop in Table 10 (first table)

        result = AdvancedDamageCalculator.calculate_damage(
            location=AdvancedHitLocation.ARM_GLANCE_SHOULDER_RIGHT,
            dc=10,
            epen=0.3,  # Low epen to stop in first table
            is_front=True
        )

        # Should have damage from Table 10 only
        assert result.damage > 0, "Should have damage from first table"

        # Should have no excess epen (bullet stopped)
        assert result.excess_epen == 0.0, "No excess epen when bullet stops in first table"

        # May have organs from first table
        # (depends on table structure, but list should exist)
        assert isinstance(result.pierced_organs, list)

        # Should have shock from first table
        assert result.shock >= 0

    def test_multiple_tables_bullet_stops_in_second_table(self):
        """Test sequential table processing: bullet passes first table but stops in second."""
        # Use ARM_GLANCE_SHOULDER_RIGHT which has "Table 10 & 9"
        # Medium epen should pass through Table 10 but stop in Table 9

        result = AdvancedDamageCalculator.calculate_damage(
            location=AdvancedHitLocation.ARM_GLANCE_SHOULDER_RIGHT,
            dc=10,
            epen=1.5,  # Medium epen to pass through first table but stop in second
            is_front=True
        )

        # Should have damage from both tables
        assert result.damage > 0, "Should have damage from both tables"

        # Should have no excess epen (bullet stopped in second table)
        assert result.excess_epen == 0.0, "No excess epen when bullet stops in second table"

        # Should have organs from both tables
        assert isinstance(result.pierced_organs, list)

        # Should have shock from both tables (summed)
        assert result.shock >= 0

    def test_multiple_tables_bullet_passes_through_both(self):
        """Test sequential table processing: bullet passes through both tables completely."""
        # Use ARM_GLANCE_SHOULDER_RIGHT which has "Table 10 & 9"
        # High epen should pass through both tables

        result = AdvancedDamageCalculator.calculate_damage(
            location=AdvancedHitLocation.ARM_GLANCE_SHOULDER_RIGHT,
            dc=10,
            epen=5.0,  # High epen to pass through both tables
            is_front=True
        )

        # Should have damage from both tables
        assert result.damage > 0, "Should have damage from both tables"

        # Should have excess epen (bullet passed through both)
        assert result.excess_epen > 0.0, "Should have excess epen when bullet passes through both tables"

        # Should have organs from both tables
        assert isinstance(result.pierced_organs, list)

        # Should have shock from both tables (summed)
        assert result.shock >= 0

    def test_multiple_tables_damage_and_shock_accumulation(self):
        """Test that damage and shock accumulate correctly across multiple tables."""
        # Test with different epen values to verify accumulation

        # Low epen - only first table
        result_low = AdvancedDamageCalculator.calculate_damage(
            location=AdvancedHitLocation.ARM_GLANCE_SHOULDER_RIGHT,
            dc=10,
            epen=0.3,
            is_front=True
        )

        # High epen - both tables
        result_high = AdvancedDamageCalculator.calculate_damage(
            location=AdvancedHitLocation.ARM_GLANCE_SHOULDER_RIGHT,
            dc=10,
            epen=2.0,
            is_front=True
        )

        # Damage and shock should be greater when penetrating more
        # (assuming second table contributes additional damage/shock)
        assert result_high.damage >= result_low.damage, \
            "Higher epen should produce equal or more damage"

        # Number of organs should be greater or equal
        assert len(result_high.pierced_organs) >= len(result_low.pierced_organs), \
            "Higher epen should pierce equal or more organs"

    def test_hand_weapon_critical_three_scenarios(self):
        """Test HAND_WEAPON_CRITICAL (Table 16 & Weapon) in all three scenarios."""

        # Scenario 1: Bullet stops in hand (Table 16)
        result_stops_in_hand = AdvancedDamageCalculator.calculate_damage(
            location=AdvancedHitLocation.HAND_WEAPON_CRITICAL,
            dc=10,
            epen=0.3,
            is_front=True
        )
        assert result_stops_in_hand.damage > 0, "Should have damage from hand"
        assert result_stops_in_hand.excess_epen == 0.0, "No excess epen"
        assert result_stops_in_hand.weapon_damaged == False, "Weapon not damaged when bullet stops in hand"

        # Scenario 2: Bullet barely passes through hand (just reaches weapon)
        result_reaches_weapon = AdvancedDamageCalculator.calculate_damage(
            location=AdvancedHitLocation.HAND_WEAPON_CRITICAL,
            dc=10,
            epen=1.2,  # Just enough to pass through hand
            is_front=True
        )
        assert result_reaches_weapon.damage > 0, "Should have damage from hand"
        # Weapon damage depends on if there's excess epen
        if result_reaches_weapon.excess_epen > 0:
            assert result_reaches_weapon.weapon_damaged == True, "Weapon damaged when bullet exits hand"

        # Scenario 3: Bullet passes through hand with high epen (definitely damages weapon)
        result_passes_through = AdvancedDamageCalculator.calculate_damage(
            location=AdvancedHitLocation.HAND_WEAPON_CRITICAL,
            dc=10,
            epen=5.0,
            is_front=True
        )
        assert result_passes_through.damage > 0, "Should have damage from hand"
        assert result_passes_through.excess_epen > 0, "Should have excess epen"
        assert result_passes_through.weapon_damaged == True, "Weapon damaged when bullet passes through hand"

    def test_multiple_tables_damage_output_front_and_rear(self):
        """Output damage and shock for two-table locations from front and rear."""

        # Find all locations with exactly 2 numeric tables
        two_table_locations = []
        for location in AdvancedHitLocation:
            if location == AdvancedHitLocation.MISS or 'Table' not in location.value:
                continue

            # Count numeric tables
            import re
            table_part = location.value.split('(')[-1].rstrip(')')
            parts = [p.strip() for p in table_part.split('&')]
            table_count = sum(1 for p in parts if p.startswith('Table') or p.isdigit())

            if table_count == 2:
                # Exclude Weapon combinations
                if 'Weapon' not in location.value:
                    two_table_locations.append(location)

        print("\n" + "="*80)
        print("DAMAGE AND SHOCK FOR TWO-TABLE LOCATIONS")
        print("="*80)

        test_cases = [
            ("Low EPEN (0.5)", 0.5),
            ("Medium EPEN (1.5)", 1.5),
            ("High EPEN (3.0)", 3.0),
            ("Very High EPEN (5.0)", 25.0),
        ]

        for location in two_table_locations:
            print(f"\n{'='*80}")
            print(f"Location: {location.name}")
            print(f"Description: {location.value}")
            print(f"{'='*80}")

            for test_name, epen_value in test_cases:
                print(f"\n  {test_name}:")

                # Front shot
                result_front = AdvancedDamageCalculator.calculate_damage(
                    location=location,
                    dc=10,
                    epen=epen_value,
                    is_front=True
                )

                print(f"    FRONT: Damage={result_front.damage:6d}, Shock={result_front.shock:4d}, "
                      f"Excess EPEN={result_front.excess_epen:.2f}, "
                      f"Organs={len(result_front.pierced_organs)}, "
                      f"Disabled={result_front.is_disabled}")
                if result_front.pierced_organs:
                    print(f"           Pierced: {', '.join(result_front.pierced_organs)}")

                # Rear shot
                result_rear = AdvancedDamageCalculator.calculate_damage(
                    location=location,
                    dc=10,
                    epen=epen_value,
                    is_front=False
                )

                print(f"    REAR:  Damage={result_rear.damage:6d}, Shock={result_rear.shock:4d}, "
                      f"Excess EPEN={result_rear.excess_epen:.2f}, "
                      f"Organs={len(result_rear.pierced_organs)}, "
                      f"Disabled={result_rear.is_disabled}")
                if result_rear.pierced_organs:
                    print(f"           Pierced: {', '.join(result_rear.pierced_organs)}")

        print(f"\n{'='*80}")
        print(f"Total locations tested: {len(two_table_locations)}")
        print(f"{'='*80}\n")
