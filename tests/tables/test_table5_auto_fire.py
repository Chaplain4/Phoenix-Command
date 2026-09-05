"""Regression tests for Table 5A arc-row mapping (book values)."""

from phoenix_command.tables.core.table5_auto_pellet_shrapnel import (
    Table5AutoPelletShrapnel as T5,
)


def test_book_example_arc3_rof7_size3():
    """Book p.31: Arc=3, ROF=7, Auto WTH +3 -> 44."""
    g, p = T5.get_fire_table_probability_5a(3, 7, 3)
    assert g == 0 and p == 44


def test_arc3_rof7_size0():
    """Arc 3 base row (Index 8), ROF 7 -> 29."""
    g, p = T5.get_fire_table_probability_5a(3, 7, 0)
    assert g == 0 and p == 29


def test_arc1_rof3_size0():
    """Arc 1 base (Index 13), ROF 3 -> 25."""
    g, p = T5.get_fire_table_probability_5a(1, 3, 0)
    assert g == 0 and p == 25


def test_arc2_rof7_size0():
    """Arc 2 base (Index 10), ROF 7 -> 38."""
    g, p = T5.get_fire_table_probability_5a(2, 7, 0)
    assert g == 0 and p == 38


def test_arc6_rof3_size0():
    """Arc 6 single key, ROF 3 -> 5."""
    g, p = T5.get_fire_table_probability_5a(6, 3, 0)
    assert g == 0 and p == 5


def test_arc5_rof10_size0():
    """Arc 5 base (Index 4), ROF 10 -> 23."""
    g, p = T5.get_fire_table_probability_5a(5, 10, 0)
    assert g == 0 and p == 23


def test_point_blank_guaranteed():
    """Point blank (arc ~0), ROF 3 -> guaranteed *2 hits."""
    g, p = T5.get_fire_table_probability_5a(0.000001, 3, 0)
    assert g == 2 and p == 0
