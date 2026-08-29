"""Tests for intervening barrier / cover PF geometry."""

from phoenix_command.models.enums import AdvancedHitLocation
from phoenix_command.session.domains.map_state import (
    MapLayer,
    MapState,
    Obstacle,
    Opening,
    WallSegment,
)
from phoenix_command.session.domains.token_state import TokenPlacement
from phoenix_command.simulations.map_cover import (
    BarrierCrossing,
    classify_cover_for_shot,
    cover_pf_for_location,
    gather_barrier_crossings,
    location_height_band,
)
from phoenix_command.simulations.map_los import check_los
from phoenix_command.tables.catalogs.barrier_catalog import (
    resolve_blocks_vision,
    resolve_protection_factor,
)


def _map_with_wall_between() -> tuple[MapState, TokenPlacement, TokenPlacement]:
    layer = MapLayer(id="g", name="Ground")
    # Shooter at (0,0), target at (2,0); wall on edge of (1,0) toward (2,0)
    layer.walls["1,0:1"] = WallSegment(
        material="wall_wood_interior_plaster",
        thickness=1.0,
        height=1.2,
        protection_factor=2.0,
    )
    ms = MapState(layers=[layer], active_layer_id="g")
    shooter = TokenPlacement(token_id="s", q=0, r=0, layer_id="g", character_name="A")
    target = TokenPlacement(token_id="t", q=2, r=0, layer_id="g", character_name="B")
    return ms, shooter, target


def test_glass_does_not_block_vision():
    assert resolve_blocks_vision("bullet_proof_glass") is False
    assert resolve_blocks_vision("window_glass") is False
    assert resolve_blocks_vision("wall_brick_6") is True


def test_window_glass_pf_low():
    assert resolve_protection_factor("window_glass", 0.25) < 1.0


def test_gather_obstacle_on_target_hex():
    layer = MapLayer(id="g", name="Ground")
    layer.obstacles["1,0"] = Obstacle(
        height=1.0,
        material="common_furniture",
        protection_factor=1.0,
        blocks_los=None,
    )
    ms = MapState(layers=[layer], active_layer_id="g")
    shooter = TokenPlacement(token_id="s", q=0, r=0, layer_id="g")
    target = TokenPlacement(token_id="t", q=1, r=0, layer_id="g")
    crossings = gather_barrier_crossings(ms, shooter, target)
    assert crossings
    assert any(c.pf == 1.0 for c in crossings)


def test_low_wall_hits_shin_not_forehead():
    crossings = [
        BarrierCrossing(pf=5.0, z_low=0.0, z_high=1.3, label="low wall", path_t=1.0),
    ]
    shin_pf = cover_pf_for_location(
        crossings, AdvancedHitLocation.SHIN_FLESH_LEFT, "standing", "standing"
    )
    head_pf = cover_pf_for_location(
        crossings, AdvancedHitLocation.FOREHEAD, "standing", "standing"
    )
    assert shin_pf >= 5.0
    assert head_pf == 0.0


def test_location_height_band_ordering():
    lo, hi = location_height_band(AdvancedHitLocation.FOREHEAD, "standing")
    shin_lo, shin_hi = location_height_band(AdvancedHitLocation.SHIN_FLESH_LEFT, "standing")
    assert hi > shin_hi  # forehead higher than shin


def test_classify_opaque_blocking_without_pen():
    crossings = [
        BarrierCrossing(
            pf=100.0, z_low=0.0, z_high=2.5, label="brick", blocks_vision=True, path_t=0.5
        ),
    ]
    analysis = classify_cover_for_shot(
        crossings, pen=None, target_stance="standing", shooter_stance="standing"
    )
    assert analysis.blocked is True


def test_classify_nonblocking_when_pen_exceeds_pf():
    crossings = [
        BarrierCrossing(
            pf=1.0, z_low=0.0, z_high=2.5, label="furniture", blocks_vision=True, path_t=0.5
        ),
    ]
    analysis = classify_cover_for_shot(
        crossings, pen=10.0, target_stance="standing", shooter_stance="standing"
    )
    assert analysis.blocked is False
    assert analysis.nonblocking is True


def test_classify_transparent_glass_clear_silhouette():
    crossings = [
        BarrierCrossing(
            pf=8.0,
            z_low=0.0,
            z_high=2.5,
            label="glass",
            blocks_vision=False,
            path_t=0.5,
        ),
    ]
    analysis = classify_cover_for_shot(
        crossings, pen=4.0, target_stance="standing", shooter_stance="standing"
    )
    assert analysis.blocked is False
    assert analysis.clear_silhouette is True


def test_check_los_uses_cover_for_furniture():
    layer = MapLayer(id="g", name="Ground")
    layer.obstacles["1,0"] = Obstacle(
        height=2.0,
        material="common_furniture",
        protection_factor=1.0,
    )
    ms = MapState(layers=[layer], active_layer_id="g")
    shooter = TokenPlacement(token_id="s", q=0, r=0, layer_id="g")
    target = TokenPlacement(token_id="t", q=2, r=0, layer_id="g")
    # Without pen: opaque mid obstacle blocks
    los = check_los(ms, shooter, target, pen=None)
    assert los.blocked is True
    # With high pen: nonblocking / clear engagement
    los2 = check_los(ms, shooter, target, pen=50.0)
    assert los2.blocked is False


def test_open_window_removes_sill_to_head_band():
    layer = MapLayer(id="g", name="Ground")
    layer.walls["0,0:1"] = WallSegment(
        material="wall_cinder_block",
        height=2.5,
        protection_factor=4.0,
        openings=[Opening(kind="window", state="open", sill_height=0.9, head_height=2.1)],
    )
    ms = MapState(layers=[layer], active_layer_id="g")
    # Adjacent hexes so wall edge is on path
    shooter = TokenPlacement(token_id="s", q=0, r=0, layer_id="g")
    target = TokenPlacement(token_id="t", q=1, r=0, layer_id="g")
    crossings = gather_barrier_crossings(ms, shooter, target)
    # Mid-height of open window should not be covered by any solid slab
    covered_at_15 = any(c.z_low <= 1.5 <= c.z_high for c in crossings)
    assert covered_at_15 is False
