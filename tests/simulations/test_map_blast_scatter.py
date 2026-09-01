"""Tests for map blast scatter placement."""

import random

from phoenix_command.simulations.map_blast import (
    blast_centers_from_results,
    scatter_off_target_in_arc,
)
from phoenix_command.models.hit_result_advanced import ExplosiveShotResult


def test_scatter_off_target_not_on_aim_hex() -> None:
    rng = random.Random(42)
    cq, cr = scatter_off_target_in_arc(10, 0, 0, 0, arc_hexes=2.0, scatter_hexes=1, rng=rng)
    assert (cq, cr) != (10, 0)


def test_blast_centers_off_target_uses_arc_scatter() -> None:
    rng = random.Random(7)
    results = [
        ExplosiveShotResult(
            hit=False,
            eal=5,
            odds=20,
            roll=50,
            scatter_hexes=1,
            off_target=True,
            arc_of_fire=2.0,
        )
    ]
    centers = blast_centers_from_results(5, 0, 0, 0, results, rng=rng)
    assert len(centers) == 1
    assert centers[0] != (5, 0)
