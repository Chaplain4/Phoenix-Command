"""Regression tests for Table 4 lookups (book values)."""

from phoenix_command.models.enums import (
    AccuracyModifiers,
    ShotType,
    TargetExposure,
)
from phoenix_command.tables.core.table4_advanced_odds_of_hitting import (
    Table4AdvancedOddsOfHitting as T4,
)


# --- Table 4G: Odds of Hitting ---

def test_4g_exact_eal_20_single():
    assert T4.get_odds_of_hitting_4g(20, ShotType.SINGLE) == 67


def test_4g_exact_eal_19_single():
    assert T4.get_odds_of_hitting_4g(19, ShotType.SINGLE) == 60


def test_4g_exact_eal_28_single():
    assert T4.get_odds_of_hitting_4g(28, ShotType.SINGLE) == 99


def test_4g_exact_eal_0_single():
    assert T4.get_odds_of_hitting_4g(0, ShotType.SINGLE) == 1


def test_4g_below_min_eal():
    assert T4.get_odds_of_hitting_4g(-22, ShotType.SINGLE) == 0
    assert T4.get_odds_of_hitting_4g(-23, ShotType.SINGLE) == 0


def test_4g_above_max_eal():
    assert T4.get_odds_of_hitting_4g(29, ShotType.SINGLE) == 99


def test_4g_floor_non_exact_eal():
    """EAL -7 is between -6 and -8, floors to -8 -> burst 3."""
    assert T4.get_odds_of_hitting_4g(-7, ShotType.BURST) == 3


def test_4g_burst_eal_20():
    assert T4.get_odds_of_hitting_4g(20, ShotType.BURST) == 82


def test_4g_exact_eal_21_single():
    """Exact EAL must use its own row (bisect_right), not the row above."""
    assert T4.get_odds_of_hitting_4g(21, ShotType.SINGLE) == 74


def test_4g_exact_eal_neg6_burst():
    """EAL -6 is an exact key -> burst 4, must not floor to -8."""
    assert T4.get_odds_of_hitting_4g(-6, ShotType.BURST) == 4


# --- Table 4E: Auto Width (book values from p.63) ---

def test_4e_standing_exposed_auto_width():
    assert T4.get_standard_target_size_modifier_4e(
        TargetExposure.STANDING_EXPOSED, AccuracyModifiers.AUTO_WIDTH
    ) == 1


def test_4e_prone_auto_width():
    assert T4.get_standard_target_size_modifier_4e(
        TargetExposure.PRONE_EXPOSED, AccuracyModifiers.AUTO_WIDTH
    ) == 2


def test_4e_running_auto_width():
    assert T4.get_standard_target_size_modifier_4e(
        TargetExposure.RUNNING, AccuracyModifiers.AUTO_WIDTH
    ) == 1


def test_4e_low_crouch_auto_width():
    assert T4.get_standard_target_size_modifier_4e(
        TargetExposure.LOW_CROUCH, AccuracyModifiers.AUTO_WIDTH
    ) == 2


def test_4e_hands_knees_auto_width():
    assert T4.get_standard_target_size_modifier_4e(
        TargetExposure.HANDS_AND_KNEES_CROUCH, AccuracyModifiers.AUTO_WIDTH
    ) == 1


def test_4e_low_prone_auto_width():
    assert T4.get_standard_target_size_modifier_4e(
        TargetExposure.LOW_PRONE, AccuracyModifiers.AUTO_WIDTH
    ) == 5


def test_4e_head_auto_width():
    assert T4.get_standard_target_size_modifier_4e(
        TargetExposure.HEAD, AccuracyModifiers.AUTO_WIDTH
    ) == -3


def test_4e_kneeling_auto_width_unchanged():
    assert T4.get_standard_target_size_modifier_4e(
        TargetExposure.KNEELING_EXPOSED, AccuracyModifiers.AUTO_WIDTH
    ) == 3


# --- Table 4D: Binary max-aim rule ---

def test_4d_shaded_no_max_aim():
    """Speed 0.5, range 40 -> ALM -5 (shaded), no aim limit."""
    alm, max_aim = T4.get_movement_alm_and_max_aim_time_4d(0.5, 40)
    assert alm == -5
    assert max_aim == float('inf')


def test_4d_unshaded_max_2_impulses():
    """Speed 2.0, range 10 -> ALM -10 (unshaded), max 2 impulses."""
    alm, max_aim = T4.get_movement_alm_and_max_aim_time_4d(2.0, 10)
    assert alm == -10
    assert max_aim == 2


def test_4d_speed_4_range_70():
    """Speed 4.0, range 70 -> ALM -6, unshaded -> max 2."""
    alm, max_aim = T4.get_movement_alm_and_max_aim_time_4d(4.0, 70)
    assert alm == -6
    assert max_aim == 2
