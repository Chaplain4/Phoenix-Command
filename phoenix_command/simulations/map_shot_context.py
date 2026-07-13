"""Build ShotParameters and range from map token positions."""

from __future__ import annotations

from dataclasses import dataclass, field

from phoenix_command.gui.utils.hex_geometry import axial_distance
from phoenix_command.models.enums import (
    SituationStanceModifier4B,
    TargetExposure,
    TargetOrientation,
    VisibilityModifier4C,
)
from phoenix_command.models.hit_result_advanced import ShotParameters
from phoenix_command.session.domains.impulse_combat_state import TokenCombatRuntime
from phoenix_command.session.domains.map_state import MapLayer, MapState, rules_hexes
from phoenix_command.session.domains.token_state import TokenPlacement
from phoenix_command.simulations.hex_tactical import line_hexes, relative_orientation
from phoenix_command.simulations.map_los import LosResult, check_los


@dataclass
class MapShotContext:
    """Auto-derived shot inputs from tactical map."""

    range_rule_hexes: int
    shot_params: ShotParameters
    target_exposure: TargetExposure
    is_front_shot: bool
    visibility_notes: list[str]
    visible_exposures: list[TargetExposure] = field(default_factory=list)
    los: LosResult | None = None
    orientation_key: str = "front"


STANCE_TO_EXPOSURE = {
    "standing": TargetExposure.STANDING_EXPOSED,
    "kneeling": TargetExposure.KNEELING_EXPOSED,
    "prone": TargetExposure.PRONE_EXPOSED,
}

STANCE_TO_SITUATION = {
    ("standing", False): SituationStanceModifier4B.STANDING,
    ("standing", True): SituationStanceModifier4B.STANDING_AND_BRACED,
    ("kneeling", False): SituationStanceModifier4B.KNEELING,
    ("kneeling", True): SituationStanceModifier4B.KNEELING_AND_BRACED,
    ("prone", False): SituationStanceModifier4B.PRONE,
    ("prone", True): SituationStanceModifier4B.PRONE_AND_BRACED,
}

ORIENTATION_MAP = {
    "front": TargetOrientation.FRONT_REAR,
    "rear": TargetOrientation.FRONT_REAR,
    "oblique": TargetOrientation.OBLIQUE,
    "left_side": TargetOrientation.LEFT_SIDE,
    "right_side": TargetOrientation.RIGHT_SIDE,
}


def _get_layer(map_state: MapState | None, layer_id: str) -> MapLayer | None:
    if not map_state:
        return None
    return map_state.get_layer(layer_id)


def _collect_visibility(
    map_state: MapState | None,
    shooter: TokenPlacement,
    target: TokenPlacement,
    hexes: list[tuple[int, int]],
) -> list[VisibilityModifier4C]:
    modifiers: list[VisibilityModifier4C] = []
    seen: set[str] = set()
    layers = []
    if map_state:
        for lid in {shooter.layer_id, target.layer_id}:
            layer = _get_layer(map_state, lid)
            if layer:
                layers.append(layer)
    for layer in layers:
        for q, r in hexes:
            cond = layer.conditions.get(f"{q},{r}")
            if not cond:
                continue
            for vis_name in cond.visibility:
                if vis_name in seen:
                    continue
                seen.add(vis_name)
                try:
                    modifiers.append(VisibilityModifier4C[vis_name])
                except KeyError:
                    pass
    if not modifiers:
        modifiers.append(VisibilityModifier4C.GOOD_VISIBILITY)
    return modifiers


def build_map_shot_context(
    shooter: TokenPlacement,
    shooter_rt: TokenCombatRuntime,
    target: TokenPlacement,
    target_rt: TokenCombatRuntime,
    map_state: MapState | None,
) -> MapShotContext:
    """Derive range and shot modifiers from token positions on the map."""
    meters = (
        axial_distance(shooter.q, shooter.r, target.q, target.r)
        * (map_state.grid.meters_per_hex if map_state else 1.0)
    )
    range_hexes = max(1, round(rules_hexes(meters)))

    shooter_speed = shooter_rt.hexes_moved_this_impulse
    target_speed = target_rt.hexes_moved_this_impulse

    stance_mod = STANCE_TO_SITUATION.get(
        (shooter_rt.stance, shooter_rt.braced),
        SituationStanceModifier4B.STANDING,
    )

    line = line_hexes(shooter.q, shooter.r, target.q, target.r)
    visibility = _collect_visibility(map_state, shooter, target, line)

    los = check_los(map_state, shooter, target, target_rt)

    rel = relative_orientation(
        target.facing, target.q, target.r, shooter.q, shooter.r
    )
    orientation = ORIENTATION_MAP.get(rel, TargetOrientation.FRONT_REAR)
    is_front = rel == "front"

    if los.blocked or not los.visible_exposures:
        exposure = TargetExposure.LOOKING_OVER_COVER
        visible = []
    elif los.through_opening:
        exposure = TargetExposure.FIRING_OVER_COVER
        visible = list(los.visible_exposures)
    else:
        exposure = STANCE_TO_EXPOSURE.get(target_rt.stance, TargetExposure.STANDING_EXPOSED)
        if TargetExposure.RUNNING in los.visible_exposures:
            exposure = TargetExposure.RUNNING
        visible = list(los.visible_exposures)

    aim_ac = max(1, int(shooter_rt.aim_ac_accumulated)) if shooter_rt.aim_ac_accumulated else 2
    if shooter_rt.aim_impulses > 0 and shooter_rt.aim_target_token_id:
        # Prefer accumulated aim when tracking a specific target
        aim_ac = max(aim_ac, int(shooter_rt.aim_ac_accumulated) or aim_ac)

    shot_params = ShotParameters(
        aim_time_ac=aim_ac,
        situation_stance_modifiers=[stance_mod],
        visibility_modifiers=visibility,
        target_orientation=orientation,
        shooter_speed_hex_per_impulse=shooter_speed,
        target_speed_hex_per_impulse=target_speed,
    )

    notes = [f"Range {range_hexes} rule hex ({meters:.1f} m)"]
    notes.extend(los.notes)
    if shooter_rt.moved_this_impulse:
        notes.append("Shooter moved this impulse")
    if shooter_rt.aim_impulses:
        notes.append(f"Aimed {shooter_rt.aim_impulses} impulse(s) at target")

    return MapShotContext(
        range_rule_hexes=range_hexes,
        shot_params=shot_params,
        target_exposure=exposure,
        is_front_shot=is_front,
        visibility_notes=notes,
        visible_exposures=visible,
        los=los,
        orientation_key=rel,
    )
