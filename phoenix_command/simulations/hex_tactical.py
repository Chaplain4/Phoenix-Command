"""Hex neighbor helpers for tactical movement and orientation.

Canonical edge/facing math lives in ``hex_frame`` (GUI screen-CW numbering).
This module re-exports the common API for existing imports.
"""

from __future__ import annotations

from phoenix_command.simulations.hex_frame import (
    EDGE_NEIGHBORS,
    LEGACY_ENGINE_NEIGHBORS,
    apply_free_facing,
    axial_neighbors,
    bearing,
    classify_movement_base,
    direction_index_to_facing,
    edge_toward,
    facing_for_edge,
    facing_to_radians,
    line_hexes,
    neighbor_direction_index,
    relative_orientation,
    shortest_facing_delta,
)

# Default flat-top neighbor order (GUI screen-CW). Prefer edge_neighbors(orientation).
AXIAL_NEIGHBORS = EDGE_NEIGHBORS["flat"]

__all__ = [
    "AXIAL_NEIGHBORS",
    "EDGE_NEIGHBORS",
    "LEGACY_ENGINE_NEIGHBORS",
    "apply_free_facing",
    "axial_neighbors",
    "bearing",
    "classify_movement_base",
    "direction_index_to_facing",
    "edge_toward",
    "facing_for_edge",
    "facing_to_radians",
    "line_hexes",
    "neighbor_direction_index",
    "relative_orientation",
    "shortest_facing_delta",
]
