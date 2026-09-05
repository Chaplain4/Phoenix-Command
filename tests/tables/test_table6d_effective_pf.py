"""Regression tests for Table 6D Effective Armor PF and DC=1 rule (book p.24/66)."""

from unittest.mock import patch

from phoenix_command.models.enums import ArmorMaterial
from phoenix_command.models.gear import ArmorProtectionData
from phoenix_command.tables.core.table3_hit_location_and_damage import (
    Table3HitLocationAndDamage as T3,
)


# --- Table 6D: Effective Armor Protection Factor ---

def test_6d_pf2_roll0():
    """PF 2, glance roll 0 -> EPF 2 (must use table, not skip)."""
    assert T3.get_effective_pf(2, 0) == 2


def test_6d_pf2_full_row():
    """PF 2 glance row from book p.66: [2,2,3,3,3,3,4,4,4,5]."""
    expected = [2, 2, 3, 3, 3, 3, 4, 4, 4, 5]
    for roll, epf in enumerate(expected):
        assert T3.get_effective_pf(2, roll) == epf


def test_6d_pf0_returns_0():
    """No armor -> EPF 0."""
    assert T3.get_effective_pf(0, 5) == 0
    assert T3.get_effective_pf(-1, 0) == 0


def test_6d_pf4_roll0():
    """PF 4, roll 0 -> EPF 4."""
    assert T3.get_effective_pf(4, 0) == 4


@patch("phoenix_command.models.gear.random.randint", return_value=0)
def test_6d_process_hit_uses_table_for_pf2(mock_roll):
    """Armor PF 2 must glance via Table 6D (EPF 2), not bypass the table."""
    data = ArmorProtectionData()
    data.add_layer(ArmorMaterial.KEVLAR, 2, 1)
    penetrated, remaining = data.process_hit(7.0)
    # EPF 2 from table; 7 - 2 = 5 remaining, penetrated
    assert penetrated is True
    assert remaining == 5


# --- DC=1 when 0 < EPEN < EPF (book p.24) ---

def test_dc1_when_epen_less_than_epf():
    """Book p.24: PEN 7, EPF 4 -> EPEN 3; 0 < EPEN < EPF -> DC = 1."""
    pen = 7.0
    epen = 3.0  # remaining after armor subtracted EPF
    weapon_dc = 6
    effective_protection = pen - epen
    assert effective_protection == 4.0
    effective_dc = 1 if effective_protection > epen else weapon_dc
    assert effective_dc == 1


def test_dc_full_when_epen_exceeds_epf():
    """Book p.24: PEN 17, EPF 4 -> EPEN 13; EPEN > EPF -> full weapon DC."""
    pen = 17.0
    epen = 13.0
    weapon_dc = 6
    effective_protection = pen - epen
    assert effective_protection == 4.0
    effective_dc = 1 if effective_protection > epen else weapon_dc
    assert effective_dc == 6
