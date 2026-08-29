"""Intervening cover geometry: barrier crossings, height bands, cover PF."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from phoenix_command.models.enums import AdvancedHitLocation, TargetExposure
from phoenix_command.session.domains.impulse_combat_state import TokenCombatRuntime
from phoenix_command.session.domains.map_state import (
    MapLayer,
    MapState,
    Obstacle,
    WallSegment,
    hex_wall_key,
    layer_has_hex_wall,
)
from phoenix_command.session.domains.token_state import TokenPlacement
from phoenix_command.simulations.hex_tactical import line_hexes, neighbor_direction_index
from phoenix_command.tables.catalogs.barrier_catalog import (
    resolve_blocks_vision,
    resolve_protection_factor,
)


def stance_height_range(stance: str) -> tuple[float, float]:
    if stance == "prone":
        return (0.1, 0.5)
    if stance == "kneeling":
        return (0.5, 1.4)
    return (0.8, 1.8)


def muzzle_height(stance: str) -> float:
    if stance == "prone":
        return 0.25
    if stance == "kneeling":
        return 0.95
    return 1.5


def _normalized_y_for_location(location: AdvancedHitLocation) -> tuple[float, float]:
    """Normalized body Y (0=head top, 1=feet) from body zone polygons."""
    try:
        from phoenix_command.gui.widgets.body_zones import LOCATION_TO_ZONE
    except Exception:
        LOCATION_TO_ZONE = {}
    zone = LOCATION_TO_ZONE.get(location)
    if zone is None:
        return (0.3, 0.5)
    ys = [p[1] for p in zone.front_polygon]
    if not ys:
        return (0.3, 0.5)
    return (min(ys), max(ys))


def location_height_band(
    location: AdvancedHitLocation,
    target_stance: str,
) -> tuple[float, float]:
    """Absolute height band (m AGL) for a hit location given target stance."""
    body_low, body_high = stance_height_range(target_stance)
    span = max(0.01, body_high - body_low)
    y0, y1 = _normalized_y_for_location(location)
    # Body diagram Y increases downward; map to height decreasing from body_high.
    h_high = body_high - y0 * span
    h_low = body_high - y1 * span
    if h_low > h_high:
        h_low, h_high = h_high, h_low
    return (h_low, h_high)


@dataclass
class BarrierCrossing:
    """A vertical slab of material crossed by the line of fire."""

    pf: float
    z_low: float
    z_high: float
    label: str
    blocks_vision: bool = True
    # Fraction along shooter→target hex line (0 at shooter, 1 at target)
    path_t: float = 0.5

    def to_dict(self) -> dict[str, Any]:
        return {
            "pf": self.pf,
            "z_low": self.z_low,
            "z_high": self.z_high,
            "label": self.label,
            "blocks_vision": self.blocks_vision,
            "path_t": self.path_t,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "BarrierCrossing":
        return cls(
            pf=float(data.get("pf", 0)),
            z_low=float(data.get("z_low", 0)),
            z_high=float(data.get("z_high", 0)),
            label=str(data.get("label", "")),
            blocks_vision=bool(data.get("blocks_vision", True)),
            path_t=float(data.get("path_t", 0.5)),
        )


@dataclass
class CoverAnalysis:
    """Pre-shot cover classification for odds / exposure."""

    blocked: bool = False
    clear_silhouette: bool = True
    through_cover: bool = False
    nonblocking: bool = False
    visible_exposures: list[TargetExposure] = field(default_factory=list)
    crossings: list[BarrierCrossing] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    estimated_cover_pf: float = 0.0


def _layer(map_state: MapState | None, layer_id: str) -> MapLayer | None:
    if not map_state:
        return None
    return map_state.get_layer(layer_id)


def _custom(map_state: MapState | None) -> dict:
    return map_state.custom_barriers if map_state else {}


def _wall_slabs(
    wall: WallSegment,
    path_t: float,
    label_prefix: str,
    custom: dict,
) -> list[BarrierCrossing]:
    """Solid wall bands minus open openings; closed openings keep material PF."""
    pf = wall.resolved_pf(custom)
    blocks_vision = resolve_blocks_vision(wall.material, custom)
    height = max(0.0, float(wall.height))
    if height <= 0:
        return []

    # Start with full solid, punch open gaps
    solid: list[tuple[float, float]] = [(0.0, height)]
    for opening in wall.openings:
        if opening.state == "open":
            if opening.kind == "door":
                gap_lo, gap_hi = 0.0, height
            else:
                gap_lo, gap_hi = opening.sill_height, opening.head_height
            solid = _subtract_interval(solid, gap_lo, gap_hi)
        else:
            # Closed window/door: sill–head still material (glass/door leaf)
            pass

    out: list[BarrierCrossing] = []
    for z0, z1 in solid:
        if z1 - z0 < 0.01:
            continue
        out.append(
            BarrierCrossing(
                pf=pf,
                z_low=z0,
                z_high=z1,
                label=f"{label_prefix} PF={pf:.1f}",
                blocks_vision=blocks_vision,
                path_t=path_t,
            )
        )
    return out


def _subtract_interval(
    bands: list[tuple[float, float]],
    gap_lo: float,
    gap_hi: float,
) -> list[tuple[float, float]]:
    result: list[tuple[float, float]] = []
    for a, b in bands:
        if gap_hi <= a or gap_lo >= b:
            result.append((a, b))
            continue
        if gap_lo > a:
            result.append((a, min(b, gap_lo)))
        if gap_hi < b:
            result.append((max(a, gap_hi), b))
    return [(a, b) for a, b in result if b - a > 0.01]


def _obstacle_crossing(
    obs: Obstacle,
    path_t: float,
    label: str,
    custom: dict,
) -> BarrierCrossing | None:
    h = max(0.0, float(obs.height))
    if h <= 0:
        return None
    return BarrierCrossing(
        pf=obs.resolved_pf(custom),
        z_low=0.0,
        z_high=h,
        label=label,
        blocks_vision=obs.resolved_blocks_vision(custom),
        path_t=path_t,
    )


def gather_barrier_crossings(
    map_state: MapState | None,
    shooter: TokenPlacement,
    target: TokenPlacement,
) -> list[BarrierCrossing]:
    """Collect material slabs along shooter→target hex line."""
    if not map_state:
        return []
    custom = _custom(map_state)
    shooter_layer = _layer(map_state, shooter.layer_id)
    target_layer = _layer(map_state, target.layer_id)
    line = line_hexes(shooter.q, shooter.r, target.q, target.r)
    if len(line) < 2:
        return []
    n_seg = max(1, len(line) - 1)
    crossings: list[BarrierCrossing] = []

    for i in range(1, len(line) - 1):
        q, r = line[i]
        path_t = i / n_seg
        for layer, tag in ((shooter_layer, "mid"), (target_layer, "mid-tgt")):
            if layer is None:
                continue
            obs = layer.obstacles.get(f"{q},{r}")
            if obs is not None:
                c = _obstacle_crossing(obs, path_t, f"Obstacle ({q},{r})", custom)
                if c:
                    crossings.append(c)
            if layer_has_hex_wall(layer, q, r):
                wall = layer.walls.get(hex_wall_key(q, r))
                if wall:
                    crossings.extend(
                        _wall_slabs(wall, path_t, f"Hex wall ({q},{r})", custom)
                    )
            if i + 1 < len(line):
                nq, nr = line[i + 1]
                edge = neighbor_direction_index(q, r, nq, nr)
                if edge is not None:
                    wall = layer.walls.get(f"{q},{r}:{edge}")
                    if wall is not None:
                        crossings.extend(
                            _wall_slabs(
                                wall, path_t, f"Wall ({q},{r}:{edge})", custom
                            )
                        )

    # Final edge into target hex
    if len(line) >= 2 and target_layer:
        pq, pr = line[-2]
        tq, tr = line[-1]
        path_t = (len(line) - 1) / n_seg
        edge = neighbor_direction_index(tq, tr, pq, pr)
        if edge is not None:
            wall = target_layer.walls.get(f"{tq},{tr}:{edge}")
            if wall is not None:
                crossings.extend(
                    _wall_slabs(wall, path_t, f"Facade ({tq},{tr}:{edge})", custom)
                )
        if layer_has_hex_wall(target_layer, tq, tr):
            wall = target_layer.walls.get(hex_wall_key(tq, tr))
            if wall:
                crossings.extend(
                    _wall_slabs(wall, path_t, f"Hex wall cover ({tq},{tr})", custom)
                )
        obs = target_layer.obstacles.get(f"{tq},{tr}")
        if obs is not None:
            c = _obstacle_crossing(
                obs, path_t, f"Cover obstacle ({tq},{tr})", custom
            )
            if c:
                crossings.append(c)

    return crossings


def _ray_height_at(
    muzzle: float,
    part_mid: float,
    path_t: float,
) -> float:
    t = max(0.0, min(1.0, path_t))
    return muzzle + (part_mid - muzzle) * t


def _slab_intersects(crossing: BarrierCrossing, z: float) -> bool:
    return crossing.z_low <= z <= crossing.z_high


def cover_pf_for_location(
    crossings: list[BarrierCrossing],
    location: AdvancedHitLocation,
    target_stance: str,
    shooter_stance: str,
) -> float:
    """Sum PF of solid slabs intersected by muzzle→hit-location ray."""
    if not crossings:
        return 0.0
    h_lo, h_hi = location_height_band(location, target_stance)
    part_mid = (h_lo + h_hi) / 2.0
    muzzle = muzzle_height(shooter_stance)
    total = 0.0
    for c in crossings:
        z = _ray_height_at(muzzle, part_mid, c.path_t)
        if _slab_intersects(c, z):
            total += c.pf
    return total


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


def classify_cover_for_shot(
    crossings: list[BarrierCrossing],
    *,
    pen: float | None,
    target_stance: str,
    shooter_stance: str,
    moved: bool = False,
) -> CoverAnalysis:
    """
    Classify LOF vs body height samples.

    Without pen: optical rules only (opaque slabs block vision unless cleared over).
    With pen: opaque + PF>=PEN is ballistic block; PF<PEN is nonblocking.
    """
    notes: list[str] = []
    for c in crossings:
        vision = "opaque" if c.blocks_vision else "transparent"
        notes.append(f"{c.label} [{c.z_low:.1f}-{c.z_high:.1f}m, {vision}]")

    body_low, body_high = stance_height_range(target_stance)
    muzzle = muzzle_height(shooter_stance)
    samples = [
        body_low + (body_high - body_low) * f
        for f in (0.1, 0.3, 0.5, 0.7, 0.9)
    ]

    any_clear = False
    any_penetrable = False
    any_opaque_block = False
    max_pf_on_body = 0.0

    for part_z in samples:
        vision_blocked = False
        ballistic_pf = 0.0
        for c in crossings:
            z = _ray_height_at(muzzle, part_z, c.path_t)
            if not _slab_intersects(c, z):
                continue
            ballistic_pf += c.pf
            if c.blocks_vision:
                vision_blocked = True
        max_pf_on_body = max(max_pf_on_body, ballistic_pf)

        if not vision_blocked:
            any_clear = True
            continue

        # Opaque material on this sample
        if pen is None:
            any_opaque_block = True
            continue
        if ballistic_pf <= 0:
            any_clear = True
        elif pen > ballistic_pf:
            any_penetrable = True
        else:
            any_opaque_block = True

    analysis = CoverAnalysis(
        crossings=list(crossings),
        notes=notes,
        estimated_cover_pf=max_pf_on_body,
    )

    if any_clear:
        if any_opaque_block or any_penetrable:
            # Partial clear over/around opaque cover
            analysis.through_cover = True
            analysis.clear_silhouette = False
            analysis.visible_exposures = _cover_exposures()
            analysis.notes.append("Partial body visible over/through cover")
        else:
            # Fully clear optically (may still have transparent glass PF on hit)
            analysis.clear_silhouette = True
            exposures = _stance_exposures(target_stance)
            if moved and target_stance == "standing":
                exposures = [TargetExposure.RUNNING] + exposures
            analysis.visible_exposures = exposures
            analysis.notes.append("Clear silhouette")
        return analysis

    if any_penetrable or (pen is not None and max_pf_on_body > 0 and pen > max_pf_on_body):
        # Nonblocking: full stance exposure, PF on hits behind material
        analysis.nonblocking = True
        analysis.through_cover = True
        analysis.clear_silhouette = False
        analysis.visible_exposures = _stance_exposures(target_stance)
        analysis.notes.append("Nonblocking cover (PEN > PF); full target size")
        return analysis

    # Fully opaque / blocking with no clear band
    analysis.blocked = True
    analysis.clear_silhouette = False
    analysis.notes.append("LOS blocked by opaque cover")
    return analysis
