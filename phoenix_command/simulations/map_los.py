"""Map line-of-sight between tokens, including cross-layer and openings."""

from __future__ import annotations

from dataclasses import dataclass, field

from phoenix_command.models.enums import TargetExposure
from phoenix_command.session.domains.impulse_combat_state import TokenCombatRuntime
from phoenix_command.session.domains.map_state import (
    MapLayer,
    MapState,
    WallSegment,
    layer_has_hex_wall,
)
from phoenix_command.session.domains.token_state import TokenPlacement
from phoenix_command.simulations.hex_tactical import line_hexes


@dataclass
class LosResult:
    """Outcome of a LOS check between shooter and target."""

    clear: bool = False
    blocked: bool = False
    through_opening: bool = False
    visible_exposures: list[TargetExposure] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


def _layer(map_state: MapState | None, layer_id: str) -> MapLayer | None:
    if not map_state:
        return None
    return map_state.get_layer(layer_id)


def _hex_obstacle_blocks(layer: MapLayer | None, q: int, r: int) -> bool:
    if not layer:
        return False
    obs = layer.obstacles.get(f"{q},{r}")
    return bool(obs and obs.blocks_los)


def _hex_wall_blocks(layer: MapLayer | None, q: int, r: int) -> bool:
    """Full-hex wall barriers block LOS like dense obstacles."""
    return layer_has_hex_wall(layer, q, r)


def _wall_on_edge(layer: MapLayer | None, q: int, r: int, edge: int) -> WallSegment | None:
    if not layer:
        return None
    return layer.walls.get(f"{q},{r}:{edge}")


def _stance_height_range(stance: str) -> tuple[float, float]:
    if stance == "prone":
        return (0.1, 0.5)
    if stance == "kneeling":
        return (0.5, 1.4)
    return (0.8, 1.8)


def _opening_allows_los(wall: WallSegment, target_rt: TokenCombatRuntime) -> bool:
    """True if wall has an opening that exposes some of the target body."""
    body_low, body_high = _stance_height_range(target_rt.stance)
    for opening in wall.openings:
        if opening.kind == "door" and opening.state == "open":
            return True
        if opening.kind == "window":
            if opening.state == "open":
                return True
            if opening.sill_height <= body_high and opening.head_height >= body_low:
                return True
    return False


def _edge_between(q0: int, r0: int, q1: int, r1: int) -> int | None:
    """Approximate edge index on hex (q0,r0) toward neighbor (q1,r1)."""
    from phoenix_command.simulations.hex_tactical import neighbor_direction_index

    return neighbor_direction_index(q0, r0, q1, r1)


def _stance_exposures(stance: str) -> list[TargetExposure]:
    if stance == "prone":
        return [TargetExposure.PRONE_EXPOSED, TargetExposure.LOW_PRONE, TargetExposure.HEAD]
    if stance == "kneeling":
        return [
            TargetExposure.KNEELING_EXPOSED,
            TargetExposure.HEAD,
            TargetExposure.BODY,
            TargetExposure.ARMS,
        ]
    return [
        TargetExposure.STANDING_EXPOSED,
        TargetExposure.HEAD,
        TargetExposure.BODY,
        TargetExposure.LEGS,
        TargetExposure.ARMS,
    ]


def _cover_exposures() -> list[TargetExposure]:
    return [
        TargetExposure.LOOKING_OVER_COVER,
        TargetExposure.FIRING_OVER_COVER,
        TargetExposure.HEAD,
        TargetExposure.BODY,
        TargetExposure.ARMS,
    ]


def check_los(
    map_state: MapState | None,
    shooter: TokenPlacement,
    target: TokenPlacement,
    target_rt: TokenCombatRuntime | None = None,
) -> LosResult:
    """
    Check LOS from shooter to target across layers.

    Obstacles on intermediate hexes block. Walls without openings block.
    Open/window openings allow through_opening (partial body visible).
    Cross-layer shots require either same (q,r) different elevation (stairs/
    vertical shaft) or a path that is not fully blocked; elevation delta
    alone does not block if horizontal path is clear / through openings.
    """
    notes: list[str] = []
    through_opening = False
    target_rt = target_rt or TokenCombatRuntime()

    shooter_layer = _layer(map_state, shooter.layer_id)
    target_layer = _layer(map_state, target.layer_id)
    elev_s = shooter_layer.elevation if shooter_layer else 0
    elev_t = target_layer.elevation if target_layer else 0
    if elev_s != elev_t:
        notes.append(f"Cross-layer shot (elev {elev_s} → {elev_t})")

    line = line_hexes(shooter.q, shooter.r, target.q, target.r)

    # Use shooter's layer for mid-path obstacles; also check target layer
    # for walls near the target (facade / window).
    for i in range(1, len(line) - 1):
        q, r = line[i]
        if _hex_obstacle_blocks(shooter_layer, q, r) or _hex_obstacle_blocks(target_layer, q, r):
            notes.append(f"LOS blocked by obstacle at ({q},{r})")
            return LosResult(blocked=True, notes=notes)
        if _hex_wall_blocks(shooter_layer, q, r) or _hex_wall_blocks(target_layer, q, r):
            notes.append(f"LOS blocked by hex wall at ({q},{r})")
            return LosResult(blocked=True, notes=notes)

        if i + 1 < len(line):
            nq, nr = line[i + 1]
            edge = _edge_between(q, r, nq, nr)
            if edge is not None:
                for layer in (shooter_layer, target_layer):
                    wall = _wall_on_edge(layer, q, r, edge)
                    if wall is None:
                        continue
                    if _opening_allows_los(wall, target_rt):
                        through_opening = True
                        notes.append(f"LOS through opening at ({q},{r}:{edge})")
                    else:
                        notes.append(f"LOS blocked by wall at ({q},{r}:{edge})")
                        return LosResult(blocked=True, notes=notes)

    # Final approach to target hex: wall on target hex facing shooter
    if len(line) >= 2:
        pq, pr = line[-2]
        tq, tr = line[-1]
        edge = _edge_between(tq, tr, pq, pr)
        if edge is not None and target_layer:
            wall = _wall_on_edge(target_layer, tq, tr, edge)
            if wall is not None:
                if _opening_allows_los(wall, target_rt):
                    through_opening = True
                    notes.append(f"Target behind opening ({tq},{tr}:{edge})")
                else:
                    notes.append(f"Target behind solid wall ({tq},{tr}:{edge})")
                    return LosResult(blocked=True, notes=notes)
        if _hex_wall_blocks(target_layer, tq, tr) and not through_opening:
            notes.append(f"Target behind hex wall ({tq},{tr})")
            return LosResult(blocked=True, notes=notes)

    # Obstacle on target hex itself (partial cover)
    if _hex_obstacle_blocks(target_layer, target.q, target.r):
        through_opening = True
        notes.append("Target hex has LOS-blocking obstacle (cover)")
    elif _hex_wall_blocks(target_layer, target.q, target.r):
        through_opening = True
        notes.append("Target hex has hex wall (cover)")

    if through_opening or elev_s != elev_t:
        exposures = _cover_exposures()
        if elev_s != elev_t and not through_opening:
            # Clear vertical / different floor with open path — still may see full
            exposures = _cover_exposures() + [
                e for e in _stance_exposures(target_rt.stance)
                if e not in (TargetExposure.LEGS,)
            ]
        notes.append("Partial body visible")
        return LosResult(
            clear=True,
            through_opening=True,
            visible_exposures=exposures,
            notes=notes,
        )

    exposures = _stance_exposures(target_rt.stance)
    if target_rt.moved_this_impulse and target_rt.stance == "standing":
        exposures = [TargetExposure.RUNNING] + exposures
    notes.append("Clear LOS")
    return LosResult(clear=True, visible_exposures=exposures, notes=notes)
