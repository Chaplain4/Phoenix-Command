"""Tests for map-derived shot context."""

from phoenix_command.session.domains.impulse_combat_state import TokenCombatRuntime
from phoenix_command.session.domains.map_state import HexGridConfig, HexCondition, MapLayer, MapState
from phoenix_command.session.domains.token_state import TokenPlacement
from phoenix_command.models.enums import VisibilityModifier4C
from phoenix_command.simulations.map_shot_context import build_map_shot_context


def test_range_converts_meters_to_rule_hexes() -> None:
    map_state = MapState()
    map_state.grid = HexGridConfig(meters_per_hex=1.0)
    shooter = TokenPlacement(token_id="s", q=0, r=0, facing=0)
    target = TokenPlacement(token_id="t", q=4, r=0, facing=6)
    ctx = build_map_shot_context(
        shooter,
        TokenCombatRuntime(),
        target,
        TokenCombatRuntime(),
        map_state,
    )
    assert ctx.range_rule_hexes == 2


def test_visibility_from_hex_conditions() -> None:
    map_state = MapState()
    layer = map_state.ensure_default_layer()
    layer.conditions["2,0"] = HexCondition(visibility=["SMOKE_HAZE_FOG"])
    shooter = TokenPlacement(token_id="s", q=0, r=0, layer_id=layer.id)
    target = TokenPlacement(token_id="t", q=4, r=0, layer_id=layer.id)
    ctx = build_map_shot_context(
        shooter,
        TokenCombatRuntime(),
        target,
        TokenCombatRuntime(),
        map_state,
    )
    assert VisibilityModifier4C.SMOKE_HAZE_FOG in ctx.shot_params.visibility_modifiers


def test_braced_stance_modifier() -> None:
    from phoenix_command.models.enums import SituationStanceModifier4B

    shooter = TokenPlacement(token_id="s", q=0, r=0)
    target = TokenPlacement(token_id="t", q=2, r=0)
    shooter_rt = TokenCombatRuntime(stance="kneeling", braced=True)
    ctx = build_map_shot_context(
        shooter,
        shooter_rt,
        target,
        TokenCombatRuntime(),
        MapState(),
    )
    assert SituationStanceModifier4B.KNEELING_AND_BRACED in ctx.shot_params.situation_stance_modifiers
