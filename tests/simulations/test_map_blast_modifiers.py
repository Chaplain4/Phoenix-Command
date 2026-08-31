"""Table 5B blast modifiers from map geometry, tags, and armor."""

from types import SimpleNamespace

from phoenix_command.item_database.armor import iotv, mich_tc2000
from phoenix_command.models.character import Character
from phoenix_command.models.enums import BlastModifier
from phoenix_command.models.gear import ExplosiveData
from phoenix_command.models.hit_result_advanced import ExplosiveShotResult
from phoenix_command.session.domains.impulse_combat_state import TokenCombatRuntime
from phoenix_command.session.domains.map_state import (
    MapLayer,
    MapState,
    Obstacle,
    Opening,
    TerrainTile,
    WallSegment,
)
from phoenix_command.session.domains.token_state import TokenPlacement
from phoenix_command.simulations.hex_tactical import AXIAL_NEIGHBORS
from phoenix_command.simulations.map_blast import (
    blast_centers_from_results,
    concussion_radius_hexes,
    count_enclosure_rays,
    derive_blast_modifiers,
    has_combat_suit_protection,
    layer_has_ceiling,
    scatter_blast_hex,
)


def _char(name: str = "Vic") -> Character:
    return Character(
        name=name,
        strength=12,
        intelligence=10,
        will=11,
        health=12,
        agility=10,
        gun_combat_skill_level=5,
    )


def _map(
    kind: str = "ground",
    elevation: int = 0,
    has_ceiling: bool | None = None,
) -> tuple[MapState, MapLayer]:
    layer = MapLayer(
        id="g", name="Ground", kind=kind, elevation=elevation, has_ceiling=has_ceiling
    )
    return MapState(layers=[layer], active_layer_id="g"), layer


def _tok(q: int = 0, r: int = 0, tid: str = "v") -> TokenPlacement:
    return TokenPlacement(
        token_id=tid, q=q, r=r, layer_id="g", character_name="Vic"
    )


def _brick() -> WallSegment:
    return WallSegment(material="wall_brick_6", thickness=8.0, height=2.5)


def _put_edge_walls(layer: MapLayer, q: int, r: int, dirs: list[int], openings=None) -> None:
    for d in dirs:
        wall = _brick()
        if openings:
            wall.openings = list(openings)
        layer.walls[f"{q},{r}:{d}"] = wall


def _env_only(mods: list[BlastModifier]) -> list[BlastModifier]:
    env = {
        BlastModifier.UNDERWATER,
        BlastModifier.IN_SMALL_ROOM,
        BlastModifier.IN_OPEN_TRENCH,
        BlastModifier.IN_THE_OPEN,
    }
    return [m for m in mods if m in env]


def _tiny_concussion_ammo(max_hex: int = 2):
    return SimpleNamespace(
        explosive_data=[
            ExplosiveData(
                range_hexes=0, shrapnel_penetration=0, shrapnel_damage_class=0,
                base_shrapnel_hit_chance="0", base_concussion=100,
            ),
            ExplosiveData(
                range_hexes=max_hex, shrapnel_penetration=0, shrapnel_damage_class=0,
                base_shrapnel_hit_chance="0", base_concussion=10,
            ),
            ExplosiveData(
                range_hexes=max_hex + 5, shrapnel_penetration=0, shrapnel_damage_class=0,
                base_shrapnel_hit_chance="0", base_concussion=0,
            ),
        ],
    )


def test_scatter_zero_stays_on_aim() -> None:
    assert scatter_blast_hex(4, 1, 0, 0, 0, True) == (4, 1)


def test_scatter_long_along_shot_axis() -> None:
    assert scatter_blast_hex(3, 0, 0, 0, 2, True) == (5, 0)


def test_scatter_short_against_shot_axis() -> None:
    assert scatter_blast_hex(3, 0, 0, 0, 2, False) == (1, 0)


def test_blast_centers_hit_uses_aim() -> None:
    expl = ExplosiveShotResult(hit=True, eal=10, odds=50, roll=10, scatter_hexes=3, is_long=True)
    assert blast_centers_from_results(2, 0, 0, 0, [expl]) == [(2, 0)]


def test_blast_centers_miss_uses_scatter() -> None:
    expl = ExplosiveShotResult(hit=False, eal=10, odds=50, roll=90, scatter_hexes=2, is_long=True)
    assert blast_centers_from_results(3, 0, 0, 0, [expl]) == [(5, 0)]


def test_concussion_radius_hexes() -> None:
    assert concussion_radius_hexes(_tiny_concussion_ammo(2)) == 2
    assert concussion_radius_hexes(_tiny_concussion_ammo(5)) == 5


def test_layer_has_ceiling_auto_and_override() -> None:
    assert layer_has_ceiling(MapLayer(kind="floor")) is True
    assert layer_has_ceiling(MapLayer(kind="basement")) is True
    assert layer_has_ceiling(MapLayer(kind="ground")) is False
    assert layer_has_ceiling(MapLayer(kind="trench")) is False
    assert layer_has_ceiling(MapLayer(kind="ground", has_ceiling=True)) is True
    assert layer_has_ceiling(MapLayer(kind="floor", has_ceiling=False)) is False


def test_open_hex_is_in_the_open() -> None:
    ms, _ = _map()
    mods = derive_blast_modifiers(ms, 5, 0, _tok(), _char())
    assert mods == [BlastModifier.IN_THE_OPEN]
    assert len(_env_only(mods)) == 1


def test_prone_stacks_with_open() -> None:
    ms, _ = _map()
    rt = TokenCombatRuntime(stance="prone")
    mods = derive_blast_modifiers(ms, 5, 0, _tok(), _char(), rt)
    assert mods == [BlastModifier.IN_THE_OPEN, BlastModifier.PRONE]


def test_combat_suit_helmet_and_plate() -> None:
    ch = _char()
    ch.add_gear(mich_tc2000)
    ch.add_gear(iotv)
    assert has_combat_suit_protection(ch)
    ms, _ = _map()
    mods = derive_blast_modifiers(ms, 5, 0, _tok(), ch)
    assert BlastModifier.IN_COMBAT_SUIT in mods
    assert BlastModifier.IN_THE_OPEN in mods


def test_helmet_only_not_combat_suit() -> None:
    ch = _char()
    ch.add_gear(mich_tc2000)
    assert not has_combat_suit_protection(ch)


def test_soft_vest_only_not_combat_suit() -> None:
    ch = _char()
    ch.add_gear(iotv)
    assert not has_combat_suit_protection(ch)


def test_explicit_trench_kind() -> None:
    ms, _ = _map(kind="trench")
    mods = derive_blast_modifiers(ms, 5, 0, _tok(), _char())
    assert _env_only(mods) == [BlastModifier.IN_OPEN_TRENCH]


def test_explicit_floor_kind_is_small_room() -> None:
    ms, _ = _map(kind="floor")
    mods = derive_blast_modifiers(ms, 5, 0, _tok(), _char())
    assert _env_only(mods) == [BlastModifier.IN_SMALL_ROOM]


def test_explicit_basement_kind_is_small_room() -> None:
    ms, _ = _map(kind="basement")
    mods = derive_blast_modifiers(ms, 5, 0, _tok(), _char())
    assert _env_only(mods) == [BlastModifier.IN_SMALL_ROOM]


def test_deep_water_terrain() -> None:
    ms, layer = _map()
    layer.terrain["0,0"] = TerrainTile(terrain_type="water_deep")
    mods = derive_blast_modifiers(ms, 5, 0, _tok(), _char())
    assert _env_only(mods) == [BlastModifier.UNDERWATER]


def test_four_walls_open_door_with_ceiling_still_room() -> None:
    ms, layer = _map(kind="floor")
    openings = [
        Opening(kind="door", state="open"),
        Opening(kind="window", state="open"),
    ]
    _put_edge_walls(layer, 0, 0, [0, 1, 2, 3], openings=openings)
    assert count_enclosure_rays(ms, _tok()) >= 4
    mods = derive_blast_modifiers(ms, 5, 0, _tok(), _char())
    assert _env_only(mods) == [BlastModifier.IN_SMALL_ROOM]


def test_ground_walls_with_explicit_ceiling_is_room() -> None:
    ms, layer = _map(kind="ground", has_ceiling=True)
    _put_edge_walls(layer, 0, 0, [0, 1, 2, 3])
    mods = derive_blast_modifiers(ms, 5, 0, _tok(), _char())
    assert _env_only(mods) == [BlastModifier.IN_SMALL_ROOM]


def test_three_walls_not_small_room() -> None:
    ms, layer = _map()
    _put_edge_walls(layer, 0, 0, [0, 1, 2])
    assert count_enclosure_rays(ms, _tok()) == 3
    mods = derive_blast_modifiers(ms, 5, 0, _tok(), _char())
    assert BlastModifier.IN_SMALL_ROOM not in mods
    assert _env_only(mods) == [BlastModifier.IN_THE_OPEN]


def test_three_walls_with_floor_kind_is_room() -> None:
    # Indoor hard signal (roofed interior) without full enclosure
    ms, layer = _map(kind="floor")
    _put_edge_walls(layer, 0, 0, [0, 1, 2])
    mods = derive_blast_modifiers(ms, 5, 0, _tok(), _char())
    assert _env_only(mods) == [BlastModifier.IN_SMALL_ROOM]


def test_wide_pool_open_top_is_trench_not_room() -> None:
    ms, layer = _map(kind="trench", elevation=0)
    _put_edge_walls(layer, 0, 0, list(range(6)))
    mods = derive_blast_modifiers(ms, 5, 0, _tok(), _char())
    assert _env_only(mods) == [BlastModifier.IN_OPEN_TRENCH]
    assert BlastModifier.IN_SMALL_ROOM not in mods


def test_floor_with_ceiling_false_and_walls_is_trench() -> None:
    ms, layer = _map(kind="floor", has_ceiling=False)
    _put_edge_walls(layer, 0, 0, list(range(6)))
    assert layer_has_ceiling(layer) is False
    mods = derive_blast_modifiers(ms, 5, 0, _tok(), _char())
    assert _env_only(mods) == [BlastModifier.IN_OPEN_TRENCH]


def test_linear_foxhole_depression_is_trench() -> None:
    ms, layer = _map()
    layer.obstacles["1,0"] = Obstacle(height=1.5, material="common_furniture", blocks_los=True)
    layer.obstacles["-1,0"] = Obstacle(height=1.5, material="common_furniture", blocks_los=True)
    mods = derive_blast_modifiers(ms, 5, 0, _tok(), _char())
    assert _env_only(mods) == [BlastModifier.IN_OPEN_TRENCH]


def test_room_prone_suit_stacks() -> None:
    ms, _ = _map(kind="floor")
    ch = _char()
    ch.add_gear(mich_tc2000)
    ch.add_gear(iotv)
    rt = TokenCombatRuntime(stance="prone")
    mods = derive_blast_modifiers(ms, 5, 0, _tok(), ch, rt)
    assert mods[0] == BlastModifier.IN_SMALL_ROOM
    assert BlastModifier.PRONE in mods
    assert BlastModifier.IN_COMBAT_SUIT in mods
    assert len(_env_only(mods)) == 1


def test_solid_cover_stacks_with_open() -> None:
    ms, layer = _map()
    layer.walls["1,0:0"] = WallSegment(
        material="wall_brick_6", thickness=8.0, height=2.5, protection_factor=8.0
    )
    victim = _tok(q=2, r=0)
    mods = derive_blast_modifiers(ms, 0, 0, victim, _char())
    assert BlastModifier.IN_THE_OPEN in mods
    assert BlastModifier.BEHIND_SOLID_COVER in mods
    assert len(_env_only(mods)) == 1


def test_enclosure_ray_length_follows_concussion_radius() -> None:
    ms, layer = _map()
    # Wall three hexes east of victim — beyond 2-hex concussion radius
    layer.walls["3,0:0"] = _brick()
    # Edge from (2,0) toward (3,0) actually: put wall on path at distance 3
    # From (0,0) east: step to (1,0), (2,0), (3,0). Wall on edge (2,0)->(3,0)
    layer.walls.clear()
    layer.walls["2,0:0"] = _brick()
    ammo = _tiny_concussion_ammo(2)
    assert count_enclosure_rays(ms, _tok(), max_hexes=2) == 0
    assert count_enclosure_rays(ms, _tok(), max_hexes=3) >= 1
    # With ammo radius 2, wall at step 3 not seen → not enclosed on that ray alone
    mods_short = derive_blast_modifiers(
        ms, 5, 0, _tok(), _char(), explosive_ammo=ammo
    )
    assert BlastModifier.IN_SMALL_ROOM not in mods_short
    # Longer radius sees the wall on one ray only — still not room
    mods_long = derive_blast_modifiers(
        ms, 5, 0, _tok(), _char(), enclosure_max_hexes=4
    )
    assert count_enclosure_rays(ms, _tok(), max_hexes=4) == 1


def test_enclosure_within_concussion_radius_counts() -> None:
    ms, layer = _map(kind="floor")
    # Immediate walls within 1 hex — seen even with radius 2
    _put_edge_walls(layer, 0, 0, [0, 1, 2, 3])
    ammo = _tiny_concussion_ammo(2)
    assert count_enclosure_rays(ms, _tok(), max_hexes=concussion_radius_hexes(ammo)) >= 4
    mods = derive_blast_modifiers(ms, 5, 0, _tok(), _char(), explosive_ammo=ammo)
    assert _env_only(mods) == [BlastModifier.IN_SMALL_ROOM]


def test_six_axial_dirs_exist() -> None:
    assert len(AXIAL_NEIGHBORS) == 6
