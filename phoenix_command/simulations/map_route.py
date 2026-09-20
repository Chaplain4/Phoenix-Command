"""Multi-impulse movement route planning (adjacent chain + A*)."""

from __future__ import annotations

import heapq
from dataclasses import dataclass
from typing import Callable

from phoenix_command.models.character import Character
from phoenix_command.session.domains.impulse_combat_state import TokenCombatRuntime
from phoenix_command.session.domains.map_state import MapLayer, hex_wall_key
from phoenix_command.simulations.hex_tactical import (
    axial_neighbors,
    classify_movement_base,
    direction_index_to_facing,
    neighbor_direction_index,
    shortest_facing_delta,
)
from phoenix_command.tables.catalogs.movement_catalog import compute_movement_cost

METER_SCALE = 0.5
FREE_FACING_STEPS = 2
MAX_FACING_PER_ACTION = 4  # 120°


@dataclass
class RouteEstimate:
    """AC / impulse summary for remaining route steps."""

    remaining_ac: float
    impulses_needed: int
    hex_steps_left: int
    face_steps_left: int

    def label(self) -> str:
        return (
            f"Route: {self.hex_steps_left} hex / {self.remaining_ac:.1f} AC "
            f"/ ~{self.impulses_needed} impulses"
        )


def clear_route(rt: TokenCombatRuntime) -> None:
    rt.route_steps = []
    rt.route_cursor = 0
    rt.route_braced = False


def truncate_from_cursor(rt: TokenCombatRuntime, keep_through_index: int) -> None:
    """Keep steps [0..keep_through_index] inclusive; drop the rest. Cursor stays if still valid."""
    if keep_through_index < 0:
        clear_route(rt)
        return
    rt.route_steps = list(rt.route_steps[: keep_through_index + 1])
    if rt.route_cursor > len(rt.route_steps):
        rt.route_cursor = len(rt.route_steps)


def remaining_steps(rt: TokenCombatRuntime) -> list[dict]:
    if rt.route_cursor >= len(rt.route_steps):
        return []
    return list(rt.route_steps[rt.route_cursor :])


def _hex_cost(
    facing: int,
    dir_idx: int,
    stance: str,
    layer: MapLayer | None,
    tq: int,
    tr: int,
    braced: bool,
    terrain_fn: Callable[[MapLayer | None, int, int, str], tuple[int | None, list[str]]],
) -> float | None:
    terrain_cost, modifier_ids = terrain_fn(layer, tq, tr, stance)
    base_id = classify_movement_base(facing, dir_idx)
    rule_cost = compute_movement_cost(base_id, modifier_ids, terrain_cost)
    if rule_cost < 0:
        return None
    cost = rule_cost * METER_SCALE
    if braced:
        cost += 1.0
    return cost


def _passable(
    layer: MapLayer | None,
    q: int,
    r: int,
) -> bool:
    if not layer:
        return True
    key = f"{q},{r}"
    if key in layer.obstacles and layer.obstacles[key].blocks_movement:
        return False
    if hex_wall_key(q, r) in layer.walls:
        return False
    return True


def facing_steps_for_move(from_facing: int, dir_idx: int) -> list[dict]:
    """Paid facing remainder after free ≤60° on hex enter (queued before hex step)."""
    desired = direction_index_to_facing(dir_idx)
    delta = shortest_facing_delta(from_facing, desired)
    free = max(-FREE_FACING_STEPS, min(FREE_FACING_STEPS, delta))
    remainder = delta - free
    steps: list[dict] = []
    while remainder != 0:
        chunk = max(-MAX_FACING_PER_ACTION, min(MAX_FACING_PER_ACTION, remainder))
        steps.append({"kind": "face", "delta": int(chunk)})
        remainder -= chunk
    return steps


def append_adjacent_hex(
    route: list[dict],
    *,
    from_q: int,
    from_r: int,
    from_facing: int,
    to_q: int,
    to_r: int,
    stance: str,
    braced: bool,
    layer: MapLayer | None,
    terrain_fn: Callable[[MapLayer | None, int, int, str], tuple[int | None, list[str]]],
) -> tuple[list[dict], int, str | None]:
    """
    Append facing + hex step for one adjacent move.

    Returns (new_route, facing_after, error).
    """
    dir_idx = neighbor_direction_index(from_q, from_r, to_q, to_r)
    if dir_idx is None:
        return route, from_facing, "Target is not an adjacent hex"
    if not _passable(layer, to_q, to_r):
        return route, from_facing, "Hex blocked"
    desired = direction_index_to_facing(dir_idx)
    delta = shortest_facing_delta(from_facing, desired)
    free = max(-FREE_FACING_STEPS, min(FREE_FACING_STEPS, delta))
    facing_after_free = (from_facing + free) % 12
    paid = facing_steps_for_move(from_facing, dir_idx)
    # Cost check uses facing after free turn (book: free turn on enter).
    cost = _hex_cost(
        facing_after_free, dir_idx, stance, layer, to_q, to_r, braced, terrain_fn
    )
    if cost is None:
        return route, from_facing, "Impassable terrain"
    new_route = list(route)
    new_route.extend(paid)
    new_route.append(
        {
            "kind": "hex",
            "q": to_q,
            "r": to_r,
            "cost": float(cost),
            "free_delta": int(free),
            "desired_facing": int(desired),
        }
    )
    return new_route, desired, None


def simulate_route_end(
    start_q: int,
    start_r: int,
    start_facing: int,
    steps: list[dict],
) -> tuple[int, int, int]:
    q, r, facing = start_q, start_r, start_facing
    for step in steps:
        kind = step.get("kind")
        if kind == "face":
            facing = (facing + int(step.get("delta", 0))) % 12
        elif kind == "hex":
            free = int(step.get("free_delta", 0))
            facing = (facing + free) % 12
            q = int(step["q"])
            r = int(step["r"])
            if "desired_facing" in step:
                facing = int(step["desired_facing"]) % 12
    return q, r, facing


def pathfind_to(
    *,
    start_q: int,
    start_r: int,
    start_facing: int,
    dest_q: int,
    dest_r: int,
    stance: str,
    braced: bool,
    layer: MapLayer | None,
    terrain_fn: Callable[[MapLayer | None, int, int, str], tuple[int | None, list[str]]],
    max_nodes: int = 4000,
) -> tuple[list[dict], str | None]:
    """A* pathfind; returns route steps (with facing) or error."""
    if (start_q, start_r) == (dest_q, dest_r):
        return [], None
    if not _passable(layer, dest_q, dest_r):
        return [], "Destination blocked"

    def heuristic(q: int, r: int) -> float:
        # axial hex distance
        return (
            abs(q - dest_q)
            + abs(r - dest_r)
            + abs((-q - r) - (-dest_q - dest_r))
        ) / 2.0

    # state: (q, r, facing)
    start = (start_q, start_r, start_facing % 12)
    open_heap: list[tuple[float, float, tuple[int, int, int]]] = []
    heapq.heappush(open_heap, (heuristic(*start[:2]), 0.0, start))
    came_from: dict[tuple[int, int, int], tuple[tuple[int, int, int], list[dict]]] = {}
    g_score: dict[tuple[int, int, int], float] = {start: 0.0}
    visited = 0

    while open_heap and visited < max_nodes:
        _f, g, state = heapq.heappop(open_heap)
        visited += 1
        q, r, facing = state
        if (q, r) == (dest_q, dest_r):
            # reconstruct
            path_steps: list[dict] = []
            cur = state
            chain: list[list[dict]] = []
            while cur in came_from:
                prev, segs = came_from[cur]
                chain.append(segs)
                cur = prev
            for segs in reversed(chain):
                path_steps.extend(segs)
            return path_steps, None

        for nq, nr, dir_idx in axial_neighbors(q, r):
            if not _passable(layer, nq, nr):
                continue
            segs: list[dict] = []
            paid = facing_steps_for_move(facing, dir_idx)
            segs.extend(paid)
            desired = direction_index_to_facing(dir_idx)
            free = max(
                -FREE_FACING_STEPS,
                min(FREE_FACING_STEPS, shortest_facing_delta(facing, desired)),
            )
            facing_after_free = (facing + free) % 12
            cost = _hex_cost(
                facing_after_free, dir_idx, stance, layer, nq, nr, braced, terrain_fn
            )
            if cost is None:
                continue
            segs.append(
                {
                    "kind": "hex",
                    "q": nq,
                    "r": nr,
                    "cost": float(cost),
                    "free_delta": int(free),
                    "desired_facing": int(desired),
                }
            )
            # Paid face AC ≈ 1 per action (catalog); approximate as 0.5 AC per step.
            face_ac = sum(0.5 * abs(int(s.get("delta", 0))) for s in paid)
            # Simpler: 1 AC per paid face action
            face_ac = float(len(paid))
            step_ac = float(cost) + face_ac
            nxt = (nq, nr, desired % 12)
            tentative = g + step_ac
            if tentative + 1e-9 >= g_score.get(nxt, float("inf")):
                continue
            g_score[nxt] = tentative
            came_from[nxt] = (state, segs)
            heapq.heappush(open_heap, (tentative + heuristic(nq, nr), tentative, nxt))

    return [], "No path found"


def estimate_route(
    rt: TokenCombatRuntime,
    char: Character | None,
    *,
    current_impulse: int = 0,
) -> RouteEstimate:
    """Estimate remaining AC and impulses from route_cursor onward."""
    steps = remaining_steps(rt)
    remaining_ac = 0.0
    hex_left = 0
    face_left = 0
    for step in steps:
        kind = step.get("kind")
        if kind == "face":
            face_left += 1
            remaining_ac += 1.0  # facing_change_60_120
        elif kind == "hex":
            hex_left += 1
            remaining_ac += float(step.get("cost", 1.0))

    impulses = [1, 1, 1, 1]
    if char is not None and getattr(char, "impulses", None):
        impulses = [max(0, int(x)) for x in char.impulses]
        if len(impulses) < 4:
            impulses = (impulses + [1, 1, 1, 1])[:4]

    # Start with current remaining AC this impulse, then future impulse allotments.
    pool = max(0.0, float(rt.ac_remaining))
    need = remaining_ac
    impulses_needed = 0
    idx = int(current_impulse) % 4
    # Current impulse first (already have pool)
    if need > 1e-9:
        if pool + 1e-9 >= need:
            impulses_needed = 1 if need > 1e-9 else 0
            need = 0.0
        else:
            need -= pool
            impulses_needed = 1
            idx = (idx + 1) % 4
            guard = 0
            while need > 1e-9 and guard < 64:
                allot = float(impulses[idx % 4])
                if allot <= 0:
                    allot = 1.0
                take = min(allot, need)
                need -= take
                impulses_needed += 1
                idx = (idx + 1) % 4
                guard += 1
    return RouteEstimate(
        remaining_ac=remaining_ac,
        impulses_needed=impulses_needed,
        hex_steps_left=hex_left,
        face_steps_left=face_left,
    )
