import random
from collections import Counter

from phoenix_command.models.enums import TargetExposure, AdvancedHitLocation, TargetOrientation
from phoenix_command.tables.advanced_damage_tables.table_1_get_hit_location import Table1AdvancedDamageHitLocation


class TestTable1AdvancedDamageHitLocation:
    """Tests for hit location determination based on target exposure and orientation."""

    def test_get_hit_location_front_rear_default(self):
        """Test that get_hit_location delegates to front_rear by default."""
        result = Table1AdvancedDamageHitLocation.get_hit_location(
            TargetExposure.STANDING_EXPOSED,
            TargetOrientation.FRONT_REAR
        )
        assert isinstance(result, AdvancedHitLocation)
        assert result != AdvancedHitLocation.MISS

    def test_get_hit_location_oblique(self):
        """Test that get_hit_location delegates to oblique method."""
        result = Table1AdvancedDamageHitLocation.get_hit_location(
            TargetExposure.STANDING_EXPOSED,
            TargetOrientation.OBLIQUE
        )
        assert isinstance(result, AdvancedHitLocation)

    def test_get_hit_location_right_side(self):
        """Test that get_hit_location delegates to right side method."""
        result = Table1AdvancedDamageHitLocation.get_hit_location(
            TargetExposure.STANDING_EXPOSED,
            TargetOrientation.RIGHT_SIDE
        )
        assert isinstance(result, AdvancedHitLocation)

    def test_get_hit_location_left_side(self):
        """Test that get_hit_location delegates to left side method."""
        result = Table1AdvancedDamageHitLocation.get_hit_location(
            TargetExposure.STANDING_EXPOSED,
            TargetOrientation.LEFT_SIDE
        )
        assert isinstance(result, AdvancedHitLocation)


class TestFrontRearHitLocation:
    """Tests for front/rear hit location determination."""

    def test_looking_over_cover_distributions(self):
        """Test that looking over cover generates valid head locations."""
        random.seed(42)
        results = [
            Table1AdvancedDamageHitLocation.get_hit_location_front_rear(
                TargetExposure.LOOKING_OVER_COVER
            )
            for _ in range(100)
        ]

        # Should only get head-related locations
        valid_locations = {
            AdvancedHitLocation.HEAD_GLANCE,
            AdvancedHitLocation.FOREHEAD,
            AdvancedHitLocation.EYE_NOSE,
        }
        assert all(r in valid_locations for r in results)

        # Should get variety of locations (not all the same)
        unique_results = set(results)
        assert len(unique_results) > 1

    def test_firing_over_cover_distributions(self):
        """Test that firing over cover generates valid locations."""
        random.seed(42)
        results = [
            Table1AdvancedDamageHitLocation.get_hit_location_front_rear(
                TargetExposure.FIRING_OVER_COVER
            )
            for _ in range(200)
        ]

        # Should get variety of locations (head, shoulders, arms, weapon)
        unique_results = set(results)
        assert len(unique_results) > 5

        # Should include locations from multiple body areas (not just one area)
        location_names = [loc.name for loc in results]
        has_head = any(name.startswith(('HEAD', 'FOREHEAD', 'EYE', 'MOUTH')) for name in location_names)
        has_arms_shoulders = any(name.startswith(('ARM', 'SHOULDER', 'ELBOW', 'FOREARM')) for name in location_names)

        assert has_head
        assert has_arms_shoulders

    def test_head_exposure_only_head_locations(self):
        """Test that HEAD exposure only generates head/neck locations."""
        random.seed(42)
        results = [
            Table1AdvancedDamageHitLocation.get_hit_location_front_rear(
                TargetExposure.HEAD
            )
            for _ in range(100)
        ]

        # All results should be in the head/neck area (rolls 0-59)
        valid_locations = {
            AdvancedHitLocation.HEAD_GLANCE,
            AdvancedHitLocation.FOREHEAD,
            AdvancedHitLocation.EYE_NOSE,
            AdvancedHitLocation.MOUTH,
            AdvancedHitLocation.NECK_FLESH,
            AdvancedHitLocation.NECK_THROAT,
        }
        assert all(r in valid_locations for r in results)

    def test_body_exposure_only_body_locations(self):
        """Test that BODY exposure only generates torso/arm locations."""
        random.seed(42)
        results = [
            Table1AdvancedDamageHitLocation.get_hit_location_front_rear(
                TargetExposure.BODY
            )
            for _ in range(200)
        ]

        # Should not get head locations
        head_locations = {
            AdvancedHitLocation.HEAD_GLANCE,
            AdvancedHitLocation.FOREHEAD,
            AdvancedHitLocation.EYE_NOSE,
            AdvancedHitLocation.MOUTH,
            AdvancedHitLocation.NECK_FLESH,
            AdvancedHitLocation.NECK_THROAT,
        }
        assert all(r not in head_locations for r in results)

        # Should not get leg locations
        leg_locations = {
            AdvancedHitLocation.HIP_SOCKET_LEFT,
            AdvancedHitLocation.HIP_SOCKET_RIGHT,
            AdvancedHitLocation.THIGH_FLESH_LEFT,
            AdvancedHitLocation.THIGH_FLESH_RIGHT,
            AdvancedHitLocation.KNEE_LEFT,
            AdvancedHitLocation.KNEE_RIGHT,
            AdvancedHitLocation.FOOT_LEFT,
            AdvancedHitLocation.FOOT_RIGHT,
        }
        assert all(r not in leg_locations for r in results)

    def test_legs_exposure_only_leg_locations(self):
        """Test that LEGS exposure only generates leg locations."""
        random.seed(42)
        results = [
            Table1AdvancedDamageHitLocation.get_hit_location_front_rear(
                TargetExposure.LEGS
            )
            for _ in range(200)
        ]

        # All results should be leg-related
        valid_locations = {
            AdvancedHitLocation.HIP_SOCKET_LEFT,
            AdvancedHitLocation.HIP_SOCKET_RIGHT,
            AdvancedHitLocation.LEG_GLANCE_LEFT,
            AdvancedHitLocation.LEG_GLANCE_RIGHT,
            AdvancedHitLocation.THIGH_FLESH_LEFT,
            AdvancedHitLocation.THIGH_FLESH_RIGHT,
            AdvancedHitLocation.THIGH_BONE_LEFT,
            AdvancedHitLocation.THIGH_BONE_RIGHT,
            AdvancedHitLocation.KNEE_LEFT,
            AdvancedHitLocation.KNEE_RIGHT,
            AdvancedHitLocation.SHIN_FLESH_LEFT,
            AdvancedHitLocation.SHIN_FLESH_RIGHT,
            AdvancedHitLocation.SHIN_BONE_LEFT,
            AdvancedHitLocation.SHIN_BONE_RIGHT,
            AdvancedHitLocation.FOOT_LEFT,
            AdvancedHitLocation.FOOT_RIGHT,
        }
        assert all(r in valid_locations for r in results)

    def test_arms_exposure_only_arm_locations(self):
        """Test that ARMS exposure only generates arm/shoulder/weapon locations."""
        random.seed(42)
        results = [
            Table1AdvancedDamageHitLocation.get_hit_location_front_rear(
                TargetExposure.ARMS
            )
            for _ in range(200)
        ]

        # Should get arm/shoulder/weapon locations (rolls 60-166)
        valid_locations = {
            AdvancedHitLocation.SHOULDER_GLANCE_LEFT,
            AdvancedHitLocation.SHOULDER_GLANCE_RIGHT,
            AdvancedHitLocation.SHOULDER_SOCKET_LEFT,
            AdvancedHitLocation.SHOULDER_SOCKET_RIGHT,
            AdvancedHitLocation.SHOULDER_LEFT,
            AdvancedHitLocation.SHOULDER_RIGHT,
            AdvancedHitLocation.ARM_GLANCE_LEFT,
            AdvancedHitLocation.ARM_GLANCE_RIGHT,
            AdvancedHitLocation.ARM_GLANCE_SHOULDER_LEFT,
            AdvancedHitLocation.ARM_GLANCE_SHOULDER_RIGHT,
            AdvancedHitLocation.ARM_FLESH_LEFT,
            AdvancedHitLocation.ARM_FLESH_RIGHT,
            AdvancedHitLocation.ARM_FLESH_SHOULDER_LEFT,
            AdvancedHitLocation.ARM_FLESH_SHOULDER_RIGHT,
            AdvancedHitLocation.ARM_BONE_SHOULDER_LEFT,
            AdvancedHitLocation.ARM_BONE_SHOULDER_RIGHT,
            AdvancedHitLocation.ELBOW_SHOULDER_LEFT,
            AdvancedHitLocation.ELBOW_SHOULDER_RIGHT,
            AdvancedHitLocation.FOREARM_FLESH_LUNG_LEFT,
            AdvancedHitLocation.FOREARM_FLESH_LUNG_RIGHT,
            AdvancedHitLocation.FOREARM_BONE_LUNG_LEFT,
            AdvancedHitLocation.FOREARM_BONE_LUNG_RIGHT,
            AdvancedHitLocation.HAND_BASE_OF_NECK_LEFT,
            AdvancedHitLocation.HAND_BASE_OF_NECK_RIGHT,
            AdvancedHitLocation.WEAPON_CRITICAL,
        }
        assert all(r in valid_locations for r in results)

    def test_standing_exposed_full_body_distribution(self):
        """Test that standing exposed can hit any body location."""
        random.seed(42)
        results = [
            Table1AdvancedDamageHitLocation.get_hit_location_front_rear(
                TargetExposure.STANDING_EXPOSED
            )
            for _ in range(500)
        ]

        # Should get a wide variety of locations from all body parts
        unique_results = set(results)
        assert len(unique_results) > 20

        # Should include some from each major category
        counter = Counter(results)
        has_head = any(loc.name.startswith(('HEAD', 'FOREHEAD', 'EYE', 'MOUTH', 'NECK')) for loc in counter)
        has_torso = any(loc.name.startswith(('LUNG', 'HEART', 'LIVER', 'STOMACH', 'SPINE')) for loc in counter)
        has_legs = any(loc.name.startswith(('THIGH', 'KNEE', 'SHIN', 'FOOT')) for loc in counter)

        assert has_head
        assert has_torso
        assert has_legs


class TestObliqueHitLocation:
    """Tests for oblique hit location determination."""

    def test_oblique_looking_over_cover(self):
        """Test oblique looking over cover generates valid locations."""
        random.seed(42)
        results = [
            Table1AdvancedDamageHitLocation.get_hit_location_oblique(
                TargetExposure.LOOKING_OVER_COVER
            )
            for _ in range(100)
        ]

        valid_locations = {
            AdvancedHitLocation.HEAD_GLANCE,
            AdvancedHitLocation.FOREHEAD_SIDE,
            AdvancedHitLocation.EYE_NOSE,
        }
        assert all(r in valid_locations for r in results)

    def test_oblique_firing_over_cover(self):
        """Test oblique firing over cover generates valid locations."""
        random.seed(42)
        results = [
            Table1AdvancedDamageHitLocation.get_hit_location_oblique(
                TargetExposure.FIRING_OVER_COVER
            )
            for _ in range(200)
        ]

        unique_results = set(results)
        assert len(unique_results) > 5

    def test_oblique_head_exposure(self):
        """Test oblique HEAD exposure only generates head locations."""
        random.seed(42)
        results = [
            Table1AdvancedDamageHitLocation.get_hit_location_oblique(
                TargetExposure.HEAD
            )
            for _ in range(100)
        ]

        valid_locations = {
            AdvancedHitLocation.HEAD_GLANCE,
            AdvancedHitLocation.FOREHEAD_SIDE,
            AdvancedHitLocation.EYE_NOSE,
            AdvancedHitLocation.MOUTH,
            AdvancedHitLocation.NECK_THROAT_SIDE,
            AdvancedHitLocation.NECK_SPINE_SIDE,
        }
        assert all(r in valid_locations for r in results)

    def test_oblique_standing_exposed_full_distribution(self):
        """Test oblique standing exposed generates varied locations."""
        random.seed(42)
        results = [
            Table1AdvancedDamageHitLocation.get_hit_location_oblique(
                TargetExposure.STANDING_EXPOSED
            )
            for _ in range(500)
        ]

        unique_results = set(results)
        assert len(unique_results) > 20

    def test_oblique_has_off_side_shot_side_locations(self):
        """Test that oblique table includes off-side and shot-side specific locations."""
        random.seed(42)
        results = [
            Table1AdvancedDamageHitLocation.get_hit_location_oblique(
                TargetExposure.STANDING_EXPOSED
            )
            for _ in range(500)
        ]

        counter = Counter(results)
        # Oblique should have specific arm locations
        oblique_specific = {
            AdvancedHitLocation.ARM_FLESH_OFF_SIDE,
            AdvancedHitLocation.ARM_FLESH_SHOT_SIDE,
            AdvancedHitLocation.ARM_BONE_OFF_SIDE,
            AdvancedHitLocation.ARM_BONE_SHOT_SIDE,
        }
        assert any(loc in counter for loc in oblique_specific)


class TestSideHitLocation:
    """Tests for side (left/right) hit location determination."""

    def test_right_side_looking_over_cover(self):
        """Test right side looking over cover generates valid locations."""
        random.seed(42)
        results = [
            Table1AdvancedDamageHitLocation.get_hit_location_right_side(
                TargetExposure.LOOKING_OVER_COVER
            )
            for _ in range(100)
        ]

        valid_locations = {
            AdvancedHitLocation.HEAD_GLANCE,
            AdvancedHitLocation.SKULL_SIDE,
            AdvancedHitLocation.EYE_SIDE,
        }
        assert all(r in valid_locations for r in results)

    def test_left_side_looking_over_cover(self):
        """Test left side looking over cover generates valid locations."""
        random.seed(42)
        results = [
            Table1AdvancedDamageHitLocation.get_hit_location_left_side(
                TargetExposure.LOOKING_OVER_COVER
            )
            for _ in range(100)
        ]

        valid_locations = {
            AdvancedHitLocation.HEAD_GLANCE,
            AdvancedHitLocation.SKULL_SIDE,
            AdvancedHitLocation.EYE_SIDE,
        }
        assert all(r in valid_locations for r in results)

    def test_right_side_firing_over_cover(self):
        """Test right side firing over cover generates valid locations."""
        random.seed(42)
        results = [
            Table1AdvancedDamageHitLocation.get_hit_location_right_side(
                TargetExposure.FIRING_OVER_COVER
            )
            for _ in range(200)
        ]

        unique_results = set(results)
        assert len(unique_results) > 5

    def test_right_side_head_exposure(self):
        """Test right side HEAD exposure only generates head locations."""
        random.seed(42)
        results = [
            Table1AdvancedDamageHitLocation.get_hit_location_right_side(
                TargetExposure.HEAD
            )
            for _ in range(100)
        ]

        valid_locations = {
            AdvancedHitLocation.HEAD_GLANCE,
            AdvancedHitLocation.SKULL_SIDE,
            AdvancedHitLocation.EYE_SIDE,
            AdvancedHitLocation.JAW_SIDE,
            AdvancedHitLocation.BASE_OF_SKULL_SIDE,
            AdvancedHitLocation.NECK_THROAT_SIDE,
            AdvancedHitLocation.NECK_SPINE_SIDE,
        }
        assert all(r in valid_locations for r in results)

    def test_side_standing_exposed_full_distribution(self):
        """Test side standing exposed generates varied locations."""
        random.seed(42)
        results = [
            Table1AdvancedDamageHitLocation.get_hit_location_right_side(
                TargetExposure.STANDING_EXPOSED
            )
            for _ in range(500)
        ]

        unique_results = set(results)
        assert len(unique_results) > 20

    def test_side_has_side_specific_organs(self):
        """Test that side tables include side-specific organ locations."""
        random.seed(42)
        results = [
            Table1AdvancedDamageHitLocation.get_hit_location_right_side(
                TargetExposure.STANDING_EXPOSED
            )
            for _ in range(500)
        ]

        counter = Counter(results)
        # Side shots should have specific organ locations
        side_specific = {
            AdvancedHitLocation.LUNG_SIDE,
            AdvancedHitLocation.HEART_SIDE,
            AdvancedHitLocation.SPINE_SIDE,
            AdvancedHitLocation.KIDNEY_SPINE_SIDE,
        }
        assert any(loc in counter for loc in side_specific)

    def test_left_right_symmetry(self):
        """Test that left and right side have similar distributions."""
        random.seed(42)
        left_results = [
            Table1AdvancedDamageHitLocation.get_hit_location_left_side(
                TargetExposure.STANDING_EXPOSED
            )
            for _ in range(500)
        ]

        random.seed(42)
        right_results = [
            Table1AdvancedDamageHitLocation.get_hit_location_right_side(
                TargetExposure.STANDING_EXPOSED
            )
            for _ in range(500)
        ]

        # Both should have similar variety
        left_unique = len(set(left_results))
        right_unique = len(set(right_results))

        # Should be within 20% of each other
        assert abs(left_unique - right_unique) / max(left_unique, right_unique) < 0.2


class TestStatisticalDistribution:
    """Test that random distributions work as expected."""

    def test_randomness_different_runs(self):
        """Test that multiple runs without seed produce different results."""
        results1 = [
            Table1AdvancedDamageHitLocation.get_hit_location_front_rear(
                TargetExposure.STANDING_EXPOSED
            )
            for _ in range(20)
        ]

        results2 = [
            Table1AdvancedDamageHitLocation.get_hit_location_front_rear(
                TargetExposure.STANDING_EXPOSED
            )
            for _ in range(20)
        ]

        # Results should be different (with high probability)
        assert results1 != results2

    def test_all_orientations_return_valid_locations(self):
        """Test that all orientation/exposure combinations return valid locations."""
        random.seed(42)
        exposures = [
            TargetExposure.LOOKING_OVER_COVER,
            TargetExposure.FIRING_OVER_COVER,
            TargetExposure.STANDING_EXPOSED,
            TargetExposure.HEAD,
            TargetExposure.BODY,
            TargetExposure.LEGS,
            TargetExposure.ARMS,
        ]

        orientations = [
            TargetOrientation.FRONT_REAR,
            TargetOrientation.OBLIQUE,
            TargetOrientation.RIGHT_SIDE,
            TargetOrientation.LEFT_SIDE,
        ]

        for exposure in exposures:
            for orientation in orientations:
                result = Table1AdvancedDamageHitLocation.get_hit_location(
                    exposure,
                    orientation
                )
                assert isinstance(result, AdvancedHitLocation)
                assert result != AdvancedHitLocation.MISS

    def test_coverage_front_rear_all_ranges(self):
        """Test that all range boundaries in front/rear table are reachable."""
        random.seed(42)
        results = [
            Table1AdvancedDamageHitLocation.get_hit_location_front_rear(
                TargetExposure.STANDING_EXPOSED
            )
            for _ in range(1000)
        ]

        counter = Counter(results)

        # Check that we hit locations from different ranges
        assert AdvancedHitLocation.HEAD_GLANCE in counter  # 0-4
        assert AdvancedHitLocation.FOREHEAD in counter  # 5-27
        assert AdvancedHitLocation.WEAPON_CRITICAL in counter  # 155-166
        assert AdvancedHitLocation.PELVIS in counter  # 417-533
        assert AdvancedHitLocation.FOOT_RIGHT in counter  # 968-999

