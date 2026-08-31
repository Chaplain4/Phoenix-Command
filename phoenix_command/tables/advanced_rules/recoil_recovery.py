"""§6.9 Recoil Recovery Time (AC) after a single shot. LEG10203 p.11."""

from __future__ import annotations

# Rows: largest KD threshold ≤ weapon KD.
# Columns: skill 0, 1, 2, 3, 4, 5, 6, 7–8, 9–10, 11–12, 13+.
_KD_ROWS: tuple[int, ...] = (1, 2, 3, 4, 5, 7, 10, 14)
_TABLE: dict[int, tuple[int, ...]] = {
    1: (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    2: (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    3: (2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0),
    4: (2, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0),
    5: (2, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0),
    7: (3, 2, 1, 1, 1, 1, 1, 1, 0, 0, 0),
    10: (3, 3, 2, 1, 1, 1, 1, 1, 1, 0, 0),
    14: (3, 3, 3, 2, 1, 1, 1, 1, 1, 1, 0),
}


def _skill_column(gun_combat_skill_level: int) -> int:
    s = max(0, int(gun_combat_skill_level))
    if s <= 6:
        return s
    if s <= 8:
        return 7
    if s <= 10:
        return 8
    if s <= 12:
        return 9
    return 10


def _kd_row(kd: int) -> int:
    value = int(kd)
    chosen = _KD_ROWS[0]
    for threshold in _KD_ROWS:
        if value >= threshold:
            chosen = threshold
        else:
            break
    return chosen


def recoil_recovery_ac(kd: int, gun_combat_skill_level: int) -> int:
    """AC that must be spent after a single shot before next aim or cock."""
    if kd <= 0:
        return 0
    row = _TABLE[_kd_row(kd)]
    return int(row[_skill_column(gun_combat_skill_level)])
