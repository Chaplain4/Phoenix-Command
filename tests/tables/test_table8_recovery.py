"""Regression tests for Table 8 healing/recovery (book values)."""

from phoenix_command.tables.core.table8_healing_and_recovery import (
    Table8HealingAndRecovery as T8,
)
from phoenix_command.models.enums import MedicalAid


# --- Table 8B: Incapacitation Time ---

def test_8b_pd0_row_exists(monkeypatch):
    """PD 0 row: roll 0 -> 1 phase."""
    monkeypatch.setattr("random.randint", lambda a, b: 0)
    assert T8.get_incapacitation_time_8b(0) == 1


def test_8b_pd0_roll9(monkeypatch):
    """PD 0 row: roll 9 -> 11 phases."""
    monkeypatch.setattr("random.randint", lambda a, b: 9)
    assert T8.get_incapacitation_time_8b(0) == 11


def test_8b_pd50_roll0(monkeypatch):
    monkeypatch.setattr("random.randint", lambda a, b: 0)
    assert T8.get_incapacitation_time_8b(50) == 4


def test_8b_pd300_roll0(monkeypatch):
    """PD 300, roll 0 -> 10 min = 300 phases."""
    monkeypatch.setattr("random.randint", lambda a, b: 0)
    assert T8.get_incapacitation_time_8b(300) == 300


def test_8b_pd300_roll6(monkeypatch):
    """PD 300, roll 6-7 -> 2h = 3600 phases."""
    monkeypatch.setattr("random.randint", lambda a, b: 6)
    assert T8.get_incapacitation_time_8b(300) == 3600


def test_8b_pd1000_roll9(monkeypatch):
    """PD 1000, roll 9 -> 6d = 259200 phases."""
    monkeypatch.setattr("random.randint", lambda a, b: 9)
    assert T8.get_incapacitation_time_8b(1000) == 259200


def test_8b_pd30_uses_row0(monkeypatch):
    """PD 30 < 50, falls into the 0 row."""
    monkeypatch.setattr("random.randint", lambda a, b: 0)
    assert T8.get_incapacitation_time_8b(30) == 1


def test_8b_pd52_roll2(monkeypatch):
    """Book p.54: PD 52, roll 2 -> PD 50 row, col 1-2 -> 15 phases."""
    monkeypatch.setattr("random.randint", lambda a, b: 2)
    assert T8.get_incapacitation_time_8b(52) == 15


# --- Table 8A: Next-lower lookup ---

def test_8a_floor_lookup():
    """Lookup is floor-based: PD*10/health between two rows picks the lower.
    lookup = physical_damage * 10 / target_health.
    """
    # PD=70, health=10 -> lookup=70 -> row 70 exact (healing 50 days)
    recovery = T8.get_critical_time_period_and_recovery_chance_8a(70, 10)
    assert recovery.healing_time_in_days == 50.0

    # PD=75, health=10 -> lookup=75 -> between 70 and 80, floors to 70
    recovery2 = T8.get_critical_time_period_and_recovery_chance_8a(75, 10)
    assert recovery2.healing_time_in_days == 50.0

    # PD=80, health=10 -> lookup=80 -> row 80 exact (healing 51 days)
    recovery3 = T8.get_critical_time_period_and_recovery_chance_8a(80, 10)
    assert recovery3.healing_time_in_days == 51.0


def test_8a_low_pd():
    """Very low PD -> row 5."""
    recovery = T8.get_critical_time_period_and_recovery_chance_8a(0.5, 10)
    # 0.5*10/10 = 5 -> row 5
    assert recovery.healing_time_in_days == 17.0


def test_8a_dt15_trent_example():
    """Book p.18: DT 15 -> HT 30 days, No Aid CTP 72h = 129600 phases."""
    # PD=18, health=12 -> DT = 18*10/12 = 15
    recovery = T8.get_critical_time_period_and_recovery_chance_8a(18, 12)
    assert recovery.healing_time_in_days == 30.0
    ctp, rr = recovery.aid_data[MedicalAid.NO_AID]
    assert ctp == 72 * 1800  # 72 hours in phases
    assert rr == 85


def test_8a_dt34_floors_to_30():
    """Book p.18: DT 34 uses next-lower DT 30 row (HT 41), not nearest 35 (HT 43)."""
    # PD=34, health=10 -> lookup=34 -> floors to row 30
    recovery = T8.get_critical_time_period_and_recovery_chance_8a(34, 10)
    assert recovery.healing_time_in_days == 41.0
