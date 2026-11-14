"""Hex movement passability: obstacles, hex walls, and edge walls/doors."""

from __future__ import annotations

from phoenix_command.session.domains.map_state import MapLayer, Opening, WallSegment, hex_wall_key
from phoenix_command.simulations.hex_frame import (
    neighbor_direction_index,
    neighbor_hex,
    opposite_edge,
    wall_on_edge,
)


def _wall_allows_passage(wall: WallSegment) -> bool:
    """True if an open door on this segment lets infantry cross."""
    for opening in wall.openings:
        if opening.kind == "door" and opening.state == "open":
            return True
    return False


def edge_blocks_movement(
    layer: MapLayer | None,
    from_q: int,
    from_r: int,
    to_q: int,
    to_r: int,
    orientation: str = "flat",
) -> bool:
    """True if an edge wall/door between adjacent hexes blocks walking."""
    dir_idx = neighbor_direction_index(from_q, from_r, to_q, to_r, orientation)
    if dir_idx is None:
        return False
    found = wall_on_edge(layer, from_q, from_r, dir_idx, orientation)
    if found is None:
        return False
    _key, wall = found
    return not _wall_allows_passage(wall)


def hex_blocks_destination(layer: MapLayer | None, q: int, r: int) -> bool:
    """Obstacle or solid hex-wall on the destination hex."""
    if not layer:
        return False
    key = f"{q},{r}"
    if key in layer.obstacles and layer.obstacles[key].blocks_movement:
        return True
    if hex_wall_key(q, r) in layer.walls:
        return True
    return False


def sync_open_door_opposite(
    layer: MapLayer | None,
    wall_key: str,
    opening: Opening,
    orientation: str = "flat",
) -> None:
    """Mirror door state onto the opposite-edge door opening if present."""
    if layer is None or opening.kind != "door":
        return
    try:
        coord, edge_s = wall_key.rsplit(":", 1)
        q_s, r_s = coord.split(",")
        q, r, edge = int(q_s), int(r_s), int(edge_s)
    except (ValueError, AttributeError):
        return
    nq, nr = neighbor_hex(q, r, edge, orientation)
    opp_key = f"{nq},{nr}:{opposite_edge(edge)}"
    opp_wall = layer.walls.get(opp_key)
    if opp_wall is None:
        return
    for other in opp_wall.openings:
        if other.kind == "door":
            other.state = opening.state
            return
