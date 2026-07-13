"""Hex neighbor helpers for tactical movement and orientation."""

from __future__ import annotations

import math

# Flat-top axial directions (E, NE, NW, W, SW, SE)
AXIAL_NEIGHBORS = (
    (1, 0),
    (1, -1),
    (0, -1),
    (-1, 0),
    (-1, 1),
    (0, 1),
)


def axial_neighbors(q: int, r: int) -> list[tuple[int, int, int]]:
    """Return list of (nq, nr, direction_index 0..5)."""
    return [(q + dq, r + dr, i) for i, (dq, dr) in enumerate(AXIAL_NEIGHBORS)]


def neighbor_direction_index(q0: int, r0: int, q1: int, r1: int) -> int | None:
    """Direction index from (q0,r0) to adjacent (q1,r1), or None."""
    dq, dr = q1 - q0, r1 - r0
    for i, (ndq, ndr) in enumerate(AXIAL_NEIGHBORS):
        if dq == ndq and dr == ndr:
            return i
    return None


def facing_to_direction_index(facing: int) -> float:
    """Map 12-step facing to 6-direction index as float (for interpolation)."""
    return (facing % 12) / 2.0


def facing_to_radians(facing: int) -> float:
    """Facing 0-11 to radians (0 = +q / east on flat-top)."""
    return math.radians((facing % 12) * 30)


def classify_movement_base(facing: int, dir_index: int) -> str:
    """
    Classify movement relative to token facing into Table 7A base id.

    facing uses 12 steps (30°); dir_index is 0..5 axial neighbor direction.
    """
    primary = (facing % 12) // 2
    diff = (dir_index - primary) % 6
    if diff == 0:
        return "forward"
    if diff == 3:
        return "backward"
    if diff in (1, 5):
        return "oblique"
    return "sideways"


def line_hexes(q0: int, r0: int, q1: int, r1: int) -> list[tuple[int, int]]:
    """Approximate line of hexes between two axial coordinates."""
    dist = max(abs(q1 - q0), abs(r1 - r0), abs((q1 - q0) + (r1 - r0)))
    if dist == 0:
        return [(q0, r0)]
    results: list[tuple[int, int]] = []
    for i in range(dist + 1):
        t = i / dist
        q = round(q0 + (q1 - q0) * t)
        r = round(r0 + (r1 - r0) * t)
        if not results or results[-1] != (q, r):
            results.append((q, r))
    return results


def _normalize_angle(radians: float) -> float:
    """Normalize to (-pi, pi]."""
    while radians > math.pi:
        radians -= 2 * math.pi
    while radians <= -math.pi:
        radians += 2 * math.pi
    return radians


def relative_orientation(
    target_facing: int,
    target_q: int,
    target_r: int,
    shooter_q: int,
    shooter_r: int,
) -> str:
    """
    Target orientation relative to incoming shot direction.

    Returns one of: front, rear, oblique, left_side, right_side.
    Uses angle between target facing and vector from target toward shooter
    (the face the target presents to the shooter).
    """
    # Direction from target to shooter = which way target is looking at shooter
    dq = shooter_q - target_q
    dr = shooter_r - target_r
    if dq == 0 and dr == 0:
        return "front"
    # Axial to approximate cartesian (flat-top)
    shot_angle = math.atan2(dr * math.sqrt(3) / 2, dq * 1.5 + dr * 0.75)
    facing_angle = facing_to_radians(target_facing)
    # Relative: 0 = shot comes from front of target
    rel = _normalize_angle(shot_angle - facing_angle)
    abs_rel = abs(rel)
    # Front ±45°, rear ±135–180°, sides near ±90°, else oblique
    if abs_rel <= math.pi / 4:
        return "front"
    if abs_rel >= 3 * math.pi / 4:
        return "rear"
    # Side band: ±67.5° to ±112.5° roughly around ±90°
    if abs(abs_rel - math.pi / 2) <= math.pi / 8:
        return "left_side" if rel > 0 else "right_side"
    return "oblique"
