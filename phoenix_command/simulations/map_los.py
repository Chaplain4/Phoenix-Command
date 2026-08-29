"""Map line-of-sight between tokens, including cover / intervening barriers."""

from __future__ import annotations

from dataclasses import dataclass, field

from phoenix_command.models.enums import TargetExposure
from phoenix_command.session.domains.impulse_combat_state import TokenCombatRuntime
from phoenix_command.session.domains.map_state import MapState
from phoenix_command.session.domains.token_state import TokenPlacement
from phoenix_command.simulations.map_cover import (
    CoverAnalysis,
    classify_cover_for_shot,
    gather_barrier_crossings,
    stance_height_range,
)


@dataclass
class LosResult:
    """Outcome of a LOS check between shooter and target."""

    clear: bool = False
    blocked: bool = False
    through_opening: bool = False
    visible_exposures: list[TargetExposure] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    cover: CoverAnalysis | None = None


def check_los(
    map_state: MapState | None,
    shooter: TokenPlacement,
    target: TokenPlacement,
    target_rt: TokenCombatRuntime | None = None,
    *,
    pen: float | None = None,
    shooter_stance: str | None = None,
) -> LosResult:
    """
    Check LOS from shooter to target using intervening barrier geometry.

    Optical transparency (glass) does not block vision; ballistic Blocking vs
    Nonblocking uses PEN vs cover PF when ``pen`` is provided.
    """
    target_rt = target_rt or TokenCombatRuntime()
    shooter_st = shooter_stance or "standing"
    notes: list[str] = []

    if map_state:
        s_layer = map_state.get_layer(shooter.layer_id)
        t_layer = map_state.get_layer(target.layer_id)
        elev_s = s_layer.elevation if s_layer else 0
        elev_t = t_layer.elevation if t_layer else 0
        if elev_s != elev_t:
            notes.append(f"Cross-layer shot (elev {elev_s} → {elev_t})")

    crossings = gather_barrier_crossings(map_state, shooter, target)
    analysis = classify_cover_for_shot(
        crossings,
        pen=pen,
        target_stance=target_rt.stance,
        shooter_stance=shooter_st,
        moved=bool(target_rt.moved_this_impulse),
    )
    notes.extend(analysis.notes)

    if analysis.blocked:
        return LosResult(
            blocked=True,
            notes=notes,
            cover=analysis,
        )

    through = analysis.through_cover or analysis.nonblocking
    return LosResult(
        clear=True,
        through_opening=through,
        visible_exposures=list(analysis.visible_exposures),
        notes=notes,
        cover=analysis,
    )


# Re-export for callers/tests that imported stance helper from map_los
_stance_height_range = stance_height_range
