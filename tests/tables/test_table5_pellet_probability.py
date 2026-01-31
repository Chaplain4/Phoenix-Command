"""Tests for Table 5A pellet hit probability calculations."""

import pytest
from phoenix_command.tables.core.table5_auto_pellet_shrapnel import Table5AutoPelletShrapnel


class TestPelletHitProbability:
    """Test pellet hit probability calculations."""

    def test_guaranteed_hits_no_modifier(self):
        """Test guaranteed hits with no size modifier."""
        guaranteed, probability = Table5AutoPelletShrapnel.get_pellet_hit_probability_5a(25, True, 0)
        assert guaranteed == 25
        assert probability == 0

    def test_guaranteed_hits_positive_modifier(self):
        """Test guaranteed hits with positive size modifier (larger target)."""
        # Base 25 is at index 3, with +2 modifier goes to index 1 (44 hits)
        guaranteed, probability = Table5AutoPelletShrapnel.get_pellet_hit_probability_5a(25, True, 2)
        assert guaranteed == 44
        assert probability == 0

    def test_guaranteed_hits_negative_modifier(self):
        """Test guaranteed hits with negative size modifier (smaller target)."""
        # Base 25 is at index 3, with -2 modifier goes to index 5 (14 hits)
        guaranteed, probability = Table5AutoPelletShrapnel.get_pellet_hit_probability_5a(25, True, -2)
        assert guaranteed == 14
        assert probability == 0

    def test_probabilistic_hits_no_modifier(self):
        """Test probabilistic hits with no size modifier."""
        guaranteed, probability = Table5AutoPelletShrapnel.get_pellet_hit_probability_5a(49, False, 0)
        assert guaranteed == 0
        assert probability == 49

    def test_probabilistic_hits_positive_modifier(self):
        """Test probabilistic hits with positive size modifier (larger target)."""
        # Base 49 is at index 17, with +1 modifier goes to index 16 (65%)
        guaranteed, probability = Table5AutoPelletShrapnel.get_pellet_hit_probability_5a(49, False, 1)
        assert guaranteed == 0
        assert probability == 65

    def test_probabilistic_hits_negative_modifier(self):
        """Test probabilistic hits with negative size modifier (smaller target)."""
        # Base 49 is at index 17, with -1 modifier goes to index 18 (37%)
        guaranteed, probability = Table5AutoPelletShrapnel.get_pellet_hit_probability_5a(49, False, -1)
        assert guaranteed == 0
        assert probability == 37

    def test_probabilistic_to_guaranteed_transition(self):
        """Test transition from probabilistic to guaranteed with large positive modifier."""
        # Base 49 is at index 17, with +3 modifier goes to index 14 (1 guaranteed hit)
        guaranteed, probability = Table5AutoPelletShrapnel.get_pellet_hit_probability_5a(49, False, 3)
        assert guaranteed == 1
        assert probability == 0

    def test_probabilistic_to_guaranteed_transition_large(self):
        """Test transition from probabilistic to guaranteed with very large positive modifier."""
        # Base 37 is at index 18, with +10 modifier goes to index 8 (6 guaranteed hits)
        guaranteed, probability = Table5AutoPelletShrapnel.get_pellet_hit_probability_5a(37, False, 10)
        assert guaranteed == 6
        assert probability == 0

    def test_guaranteed_stays_guaranteed_with_negative_modifier(self):
        """Test that guaranteed hits stay guaranteed even with negative modifier."""
        # Base 5 is at index 9, with -5 modifier goes to index 14 (1 guaranteed hit)
        guaranteed, probability = Table5AutoPelletShrapnel.get_pellet_hit_probability_5a(5, True, -5)
        assert guaranteed == 1
        assert probability == 0

    def test_probabilistic_minimum_with_large_negative_modifier(self):
        """Test probabilistic hits with very large negative modifier (very small target)."""
        # Base 87 is at index 15, with -10 modifier goes to index 25 (4%)
        guaranteed, probability = Table5AutoPelletShrapnel.get_pellet_hit_probability_5a(87, False, -10)
        assert guaranteed == 0
        assert probability == 4

    def test_probabilistic_zero_with_extreme_negative_modifier(self):
        """Test probabilistic hits reaching zero with extreme negative modifier."""
        # Base 87 is at index 15, with -15 modifier goes to index 30 (0%)
        guaranteed, probability = Table5AutoPelletShrapnel.get_pellet_hit_probability_5a(87, False, -15)
        assert guaranteed == 0
        assert probability == 0

    def test_guaranteed_maximum_with_large_positive_modifier(self):
        """Test guaranteed hits reaching maximum with large positive modifier."""
        # Base 14 is at index 5, with +5 modifier goes to index 0 (58 hits)
        guaranteed, probability = Table5AutoPelletShrapnel.get_pellet_hit_probability_5a(14, True, 5)
        assert guaranteed == 58
        assert probability == 0

    def test_bphc_42_with_size_mod_2(self):
        """Test BPHC=42 with size_modifier=2 (FIRING_OVER_COVER case)."""
        # Base 42 should find index 18 (37), with +2 goes to 16 (87%)
        guaranteed, probability = Table5AutoPelletShrapnel.get_pellet_hit_probability_5a(42, False, 2)
        assert guaranteed == 0
        assert probability == 87

    def test_bphc_42_with_size_mod_3(self):
        """Test BPHC=42 with size_modifier=3 (BODY case)."""
        # Base 42 should find index 17 (49), with +3 goes to 14 (1 guaranteed)
        guaranteed, probability = Table5AutoPelletShrapnel.get_pellet_hit_probability_5a(42, False, 3)
        assert guaranteed == 1
        assert probability == 0

    def test_bphc_42_with_size_mod_4(self):
        """Test BPHC=42 with size_modifier=4 (transition to guaranteed)."""
        # Base 42 should find index 17 (49), with +4 goes to 13 (2 guaranteed)
        guaranteed, probability = Table5AutoPelletShrapnel.get_pellet_hit_probability_5a(42, False, 4)
        assert guaranteed == 2
        assert probability == 0


class TestShrapnelPelletHitsConsistency:
    """Test that get_shrapnel_pellet_hits_5a behaves consistently with probability method."""

    def test_guaranteed_hits_returns_value(self):
        """Test that guaranteed hits always return the guaranteed value."""
        # With guaranteed hits, should always return the value (no randomness)
        result = Table5AutoPelletShrapnel.get_shrapnel_pellet_hits_5a(25, True, 0)
        assert result == 25

    def test_probabilistic_to_guaranteed_returns_guaranteed(self):
        """Test that crossing to guaranteed area returns guaranteed value."""
        # BPHC=42 with size_mod=4 should cross to guaranteed and return 2
        result = Table5AutoPelletShrapnel.get_shrapnel_pellet_hits_5a(42, False, 4)
        assert result == 2

    def test_large_guaranteed_with_positive_modifier(self):
        """Test large guaranteed hits with positive modifier."""
        result = Table5AutoPelletShrapnel.get_shrapnel_pellet_hits_5a(14, True, 5)
        assert result == 58
