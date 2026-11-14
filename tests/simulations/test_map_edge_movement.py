"""Edge walls / doors block walking; open door syncs opposite edge."""

from phoenix_command.session.domains.map_state import (
    MapLayer,
    MapState,
    Opening,
    WallSegment,
)
from phoenix_command.simulations.map_movement import (
    edge_blocks_movement,
    sync_open_door_opposite,
)
from phoenix_command.simulations.map_route import pathfind_to


def _layer_with_edge_wall(
    *, door_state: str | None = None
) -> MapLayer:
    """Wall on edge 0 of (0,0) toward (1,0); optional door."""
    layer = MapLayer(id="L1", name="Ground")
    openings: list[Opening] = []
    if door_state is not None:
        openings.append(Opening(kind="door", state=door_state))
    layer.walls["0,0:0"] = WallSegment(material="cinder_block", openings=openings)
    return layer


def test_closed_edge_wall_blocks_movement() -> None:
    layer = _layer_with_edge_wall()
    assert edge_blocks_movement(layer, 0, 0, 1, 0) is True
    assert edge_blocks_movement(layer, 1, 0, 0, 0) is True  # opposite lookup


def test_closed_door_blocks_open_door_allows() -> None:
    closed = _layer_with_edge_wall(door_state="closed")
    assert edge_blocks_movement(closed, 0, 0, 1, 0) is True
    opened = _layer_with_edge_wall(door_state="open")
    assert edge_blocks_movement(opened, 0, 0, 1, 0) is False


def test_pathfind_avoids_closed_door() -> None:
    layer = _layer_with_edge_wall(door_state="closed")

    def terrain_fn(_layer, _q, _r, _stance):
        return 0, []

    steps, err = pathfind_to(
        start_q=0,
        start_r=0,
        start_facing=0,
        dest_q=1,
        dest_r=0,
        stance="standing",
        braced=False,
        layer=layer,
        terrain_fn=terrain_fn,
    )
    # Direct edge blocked — either longer path or failure; must not step 0,0→1,0
    assert err is not None or not any(
        s.get("kind") == "hex" and s.get("q") == 1 and s.get("r") == 0 for s in steps[:1]
    )
    if steps:
        # First hex step must not be through the sealed door
        first_hex = next(s for s in steps if s.get("kind") == "hex")
        assert not (first_hex["q"] == 1 and first_hex["r"] == 0)


def test_sync_open_door_opposite() -> None:
    layer = MapLayer(id="L1", name="Ground")
    door_a = Opening(kind="door", state="closed")
    door_b = Opening(kind="door", state="closed")
    layer.walls["0,0:0"] = WallSegment(openings=[door_a])
    layer.walls["1,0:3"] = WallSegment(openings=[door_b])
    door_a.state = "open"
    sync_open_door_opposite(layer, "0,0:0", door_a)
    assert door_b.state == "open"
