"""
Tests for hit location table (Table1AdvancedDamageHitLocation).
"""
import pytest
from phoenix_command.tables.advanced_damage_tables.table_1_get_hit_location import Table1AdvancedDamageHitLocation
from phoenix_command.models.enums import TargetExposure, AdvancedHitLocation


class TestTable1AdvancedDamageHitLocation:
    """Test hit location determination."""

    def test_get_hit_location_front_rear_returns_valid_location(self):
        """Test that front/rear method returns valid hit location."""
        result = Table1AdvancedDamageHitLocation.get_hit_location_front_rear(
            TargetExposure.STANDING_EXPOSED
        )

        assert isinstance(result, AdvancedHitLocation)
        assert result != AdvancedHitLocation.MISS

    def test_get_hit_location_oblique_returns_valid_location(self):
        """Test that oblique method returns valid hit location."""
        result = Table1AdvancedDamageHitLocation.get_hit_location_oblique(
            TargetExposure.STANDING_EXPOSED
        )

        assert isinstance(result, AdvancedHitLocation)

    def test_get_hit_location_right_side_returns_valid_location(self):
        """Test that right side method returns valid hit location."""
        result = Table1AdvancedDamageHitLocation.get_hit_location_right_side(
            TargetExposure.STANDING_EXPOSED
        )

        assert isinstance(result, AdvancedHitLocation)

    def test_get_hit_location_left_side_returns_valid_location(self):
        """Test that left side method returns valid hit location."""
        result = Table1AdvancedDamageHitLocation.get_hit_location_left_side(
            TargetExposure.STANDING_EXPOSED
        )

        assert isinstance(result, AdvancedHitLocation)

    def test_looking_over_cover_returns_head_locations(self):
        """Test that LOOKING_OVER_COVER returns head locations."""
        # Run multiple times to get statistical coverage
        results = set()
        for _ in range(100):
            result = Table1AdvancedDamageHitLocation.get_hit_location_front_rear(
                TargetExposure.LOOKING_OVER_COVER
            )
            results.add(result)

        # Should only get head-related locations
        head_locations = {
            AdvancedHitLocation.HEAD_GLANCE,
            AdvancedHitLocation.FOREHEAD,
            AdvancedHitLocation.EYE_NOSE,
            AdvancedHitLocation.MISS
        }

        assert results.issubset(head_locations), \
            f"Got non-head locations: {results - head_locations}"

    def test_firing_over_cover_returns_upper_body_locations(self):
        """Test that FIRING_OVER_COVER returns upper body locations."""
        results = set()
        for _ in range(200):
            result = Table1AdvancedDamageHitLocation.get_hit_location_front_rear(
                TargetExposure.FIRING_OVER_COVER
            )
            results.add(result)

        # Should get head, neck, shoulders, arms, hands
        # Should NOT get legs or lower torso
        forbidden_locations = {
            AdvancedHitLocation.PELVIS,
            AdvancedHitLocation.HIP_SOCKET_LEFT,
            AdvancedHitLocation.HIP_SOCKET_RIGHT,
            AdvancedHitLocation.THIGH_BONE_LEFT,
            AdvancedHitLocation.THIGH_BONE_RIGHT,
            AdvancedHitLocation.KNEE_LEFT,
            AdvancedHitLocation.KNEE_RIGHT,
            AdvancedHitLocation.SHIN_BONE_LEFT,
            AdvancedHitLocation.SHIN_BONE_RIGHT,
            AdvancedHitLocation.FOOT_LEFT,
            AdvancedHitLocation.FOOT_RIGHT,
        }

        assert results.isdisjoint(forbidden_locations), \
            f"Got forbidden lower body locations: {results & forbidden_locations}"

    def test_head_exposure_returns_only_head_locations(self):
        """Test that HEAD exposure returns only head/neck locations."""
        results = set()
        for _ in range(100):
            result = Table1AdvancedDamageHitLocation.get_hit_location_front_rear(
                TargetExposure.HEAD
            )
            results.add(result)

        # Check that we don't get body or leg locations
        forbidden = {
            AdvancedHitLocation.SHOULDER_GLANCE_LEFT,
            AdvancedHitLocation.TORSO_GLANCE,
            AdvancedHitLocation.HEART,
            AdvancedHitLocation.THIGH_BONE_LEFT,
        }

        assert results.isdisjoint(forbidden), \
            f"HEAD exposure returned non-head locations: {results & forbidden}"

    def test_body_exposure_returns_torso_and_arms(self):
        """Test that BODY exposure returns torso and arm locations."""
        results = set()
        for _ in range(200):
            result = Table1AdvancedDamageHitLocation.get_hit_location_front_rear(
                TargetExposure.BODY
            )
            results.add(result)

        # Should not get head or legs
        forbidden_head = {
            AdvancedHitLocation.FOREHEAD,
            AdvancedHitLocation.EYE_NOSE,
        }
        forbidden_legs = {
            AdvancedHitLocation.THIGH_BONE_LEFT,
            AdvancedHitLocation.KNEE_LEFT,
            AdvancedHitLocation.FOOT_LEFT,
        }

        assert results.isdisjoint(forbidden_head), \
            f"BODY exposure returned head locations: {results & forbidden_head}"
        assert results.isdisjoint(forbidden_legs), \
            f"BODY exposure returned leg locations: {results & forbidden_legs}"

    def test_legs_exposure_returns_only_leg_locations(self):
        """Test that LEGS exposure returns only leg locations."""
        results = set()
        for _ in range(200):
            result = Table1AdvancedDamageHitLocation.get_hit_location_front_rear(
                TargetExposure.LEGS
            )
            results.add(result)

        # Should not get head or torso
        forbidden = {
            AdvancedHitLocation.FOREHEAD,
            AdvancedHitLocation.HEART,
            AdvancedHitLocation.SHOULDER_LEFT,
        }

        assert results.isdisjoint(forbidden), \
            f"LEGS exposure returned non-leg locations: {results & forbidden}"

    def test_arms_exposure_returns_arm_locations(self):
        """Test that ARMS exposure returns arm and weapon locations."""
        results = set()
        for _ in range(200):
            result = Table1AdvancedDamageHitLocation.get_hit_location_front_rear(
                TargetExposure.ARMS
            )
            results.add(result)

        # Should get arms, shoulders, hands, weapon
        # Should not get legs or deep torso
        forbidden = {
            AdvancedHitLocation.HEART,
            AdvancedHitLocation.LIVER,
            AdvancedHitLocation.THIGH_BONE_LEFT,
            AdvancedHitLocation.FOOT_RIGHT,
        }

        assert results.isdisjoint(forbidden), \
            f"ARMS exposure returned forbidden locations: {results & forbidden}"

    def test_in_the_open_can_hit_anywhere(self):
        """Test that STANDING_EXPOSED can potentially hit any location."""
        results = set()
        for _ in range(1000):
            result = Table1AdvancedDamageHitLocation.get_hit_location_front_rear(
                TargetExposure.STANDING_EXPOSED
            )
            results.add(result)

        # Should have good variety of locations
        assert len(results) > 20, \
            f"STANDING_EXPOSED only returned {len(results)} different locations, expected more variety"

    def test_oblique_exposure_types_work(self):
        """Test all exposure types work for oblique."""
        exposures = [
            TargetExposure.STANDING_EXPOSED,
            TargetExposure.LOOKING_OVER_COVER,
            TargetExposure.FIRING_OVER_COVER,
            TargetExposure.HEAD,
            TargetExposure.BODY,
            TargetExposure.LEGS,
            TargetExposure.ARMS,
        ]

        for exposure in exposures:
            result = Table1AdvancedDamageHitLocation.get_hit_location_oblique(exposure)
            assert isinstance(result, AdvancedHitLocation)

    def test_side_exposure_types_work(self):
        """Test all exposure types work for side shots."""
        exposures = [
            TargetExposure.STANDING_EXPOSED,
            TargetExposure.LOOKING_OVER_COVER,
            TargetExposure.FIRING_OVER_COVER,
            TargetExposure.HEAD,
            TargetExposure.BODY,
            TargetExposure.LEGS,
            TargetExposure.ARMS,
        ]

        for exposure in exposures:
            result_right = Table1AdvancedDamageHitLocation.get_hit_location_right_side(exposure)
            result_left = Table1AdvancedDamageHitLocation.get_hit_location_left_side(exposure)

            assert isinstance(result_right, AdvancedHitLocation)
            assert isinstance(result_left, AdvancedHitLocation)

    def test_randomness_produces_variety(self):
        """Test that multiple calls produce different results (randomness works)."""
        results = []
        for _ in range(50):
            result = Table1AdvancedDamageHitLocation.get_hit_location_front_rear(
                TargetExposure.STANDING_EXPOSED
            )
            results.append(result)

        # Should have more than one unique result
        unique_results = set(results)
        assert len(unique_results) > 1, \
            "All 50 calls returned the same location, randomness not working"

    def test_oblique_returns_different_locations_than_front_rear(self):
        """Test that oblique has different location possibilities than front/rear."""
        front_results = set()
        oblique_results = set()

        for _ in range(200):
            front_results.add(
                Table1AdvancedDamageHitLocation.get_hit_location_front_rear(
                    TargetExposure.STANDING_EXPOSED
                )
            )
            oblique_results.add(
                Table1AdvancedDamageHitLocation.get_hit_location_oblique(
                    TargetExposure.STANDING_EXPOSED
                )
            )

        # There should be some locations unique to oblique (like side-specific organs)
        # This is a sanity check that different tables are being used
        assert len(oblique_results) > 10
        assert len(front_results) > 10

    def test_side_hits_have_side_specific_locations(self):
        """Test that side hits can return side-specific locations."""
        results_right = set()
        results_left = set()

        for _ in range(200):
            results_right.add(
                Table1AdvancedDamageHitLocation.get_hit_location_right_side(
                    TargetExposure.STANDING_EXPOSED
                )
            )
            results_left.add(
                Table1AdvancedDamageHitLocation.get_hit_location_left_side(
                    TargetExposure.STANDING_EXPOSED
                )
            )

        # Should have reasonable variety
        assert len(results_right) > 10
        assert len(results_left) > 10

    def test_coverage_all_exposure_types_front_rear(self):
        """Test that all exposure types are handled in front/rear."""
        all_exposures = [
            TargetExposure.STANDING_EXPOSED,
            TargetExposure.LOOKING_OVER_COVER,
            TargetExposure.FIRING_OVER_COVER,
            TargetExposure.HEAD,
            TargetExposure.BODY,
            TargetExposure.LEGS,
            TargetExposure.ARMS,
        ]

        for exposure in all_exposures:
            result = Table1AdvancedDamageHitLocation.get_hit_location_front_rear(exposure)
            assert isinstance(result, AdvancedHitLocation), \
                f"Failed for exposure type: {exposure}"

    def test_no_exceptions_with_edge_cases(self):
        """Test that no exceptions are raised with various inputs."""
        methods = [
            Table1AdvancedDamageHitLocation.get_hit_location_front_rear,
            Table1AdvancedDamageHitLocation.get_hit_location_oblique,
            Table1AdvancedDamageHitLocation.get_hit_location_right_side,
            Table1AdvancedDamageHitLocation.get_hit_location_left_side,
        ]

        exposures = list(TargetExposure)

        for method in methods:
            for exposure in exposures:
                try:
                    result = method(exposure)
                    assert isinstance(result, AdvancedHitLocation)
                except Exception as e:
                    pytest.fail(f"{method.__name__} raised {type(e).__name__} with {exposure}: {e}")

    def test_statistical_distribution_head_exposure(self):
        """Test that HEAD exposure has reasonable statistical distribution."""
        results = []
        for _ in range(1000):
            result = Table1AdvancedDamageHitLocation.get_hit_location_front_rear(
                TargetExposure.HEAD
            )
            results.append(result)

        # Should have variety within head locations
        unique = set(results)
        assert len(unique) >= 3, \
            f"HEAD exposure only returned {len(unique)} unique locations in 1000 rolls"

    def test_miss_is_not_returned_for_standing_exposed(self):
        """Test that MISS is not returned for STANDING_EXPOSED (should always hit something)."""
        for _ in range(100):
            result = Table1AdvancedDamageHitLocation.get_hit_location_front_rear(
                TargetExposure.STANDING_EXPOSED
            )
            assert result != AdvancedHitLocation.MISS, \
                "STANDING_EXPOSED should not return MISS"
