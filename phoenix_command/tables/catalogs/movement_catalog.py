"""Table 7A — Movement catalog."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MovementBase:
    """Base movement cost per meter (1 hex = 1 m in our grid)."""

    id: str
    name: str
    cost: int


@dataclass(frozen=True)
class MovementModifier:
    """Additive movement modifier."""

    id: str
    name: str
    category: str
    cost: int


@dataclass(frozen=True)
class TerrainPreset:
    """Terrain preset for map editor brush."""

    id: str
    name: str
    movement_cost: int
    color: str
    modifier_ids: tuple[str, ...] = ()


# Base movement costs per meter (Table 7A)
MOVEMENT_BASE: dict[str, MovementBase] = {
    "forward": MovementBase("forward", "Forward", 1),
    "backward": MovementBase("backward", "Backward", 3),
    "oblique": MovementBase("oblique", "Oblique", 4),
    "sideways": MovementBase("sideways", "Sideways", 5),
}

# Movement modifiers (Table 7A)
MOVEMENT_MODIFIERS: dict[str, MovementModifier] = {
    # Stance
    "stance_standing": MovementModifier("stance_standing", "Standing / Running", "Stance", 0),
    "stance_low_crouch": MovementModifier("stance_low_crouch", "Low Crouch", "Stance", 1),
    "stance_hands_knees": MovementModifier("stance_hands_knees", "Hands and Knees", "Stance", 2),
    "stance_belly_crawl": MovementModifier("stance_belly_crawl", "Belly Crawl", "Stance", 3),
    # Stairs / Hills
    "slope_across": MovementModifier("slope_across", "Across Slope / Downhill / On Stairs", "Stairs-Hills", 1),
    "slope_uphill": MovementModifier("slope_uphill", "Uphill", "Stairs-Hills", 2),
    # Brush or Rubble
    "brush_light": MovementModifier("brush_light", "Light Brush or Rubble", "Brush", 1),
    "brush_medium": MovementModifier("brush_medium", "Medium Brush or Rubble", "Brush", 2),
    "brush_dense": MovementModifier("brush_dense", "Dense Brush or Rubble", "Brush", 3),
    # Injuries
    "injury_above_waist": MovementModifier("injury_above_waist", "Disabling Injury above Waist", "Injuries", 2),
    "injury_below_waist": MovementModifier("injury_below_waist", "Disabling Injury below Waist", "Injuries", 12),
    # Water
    "water_1ft": MovementModifier("water_1ft", "Water Depth 1 foot", "Water", 1),
    "water_2ft": MovementModifier("water_2ft", "Water Depth 2 feet", "Water", 2),
    "water_3ft": MovementModifier("water_3ft", "Water Depth 3 feet", "Water", 4),
    "water_4ft": MovementModifier("water_4ft", "Water Depth 4 feet", "Water", 10),
    # Miscellaneous
    "concertina_wire": MovementModifier("concertina_wire", "Concertina Wire", "Misc", 5),
    "dry_sand": MovementModifier("dry_sand", "Dry Sand on Surface", "Misc", 1),
    "icy_surface": MovementModifier("icy_surface", "Icy Surface", "Misc", 2),
    "scuba_flippers": MovementModifier("scuba_flippers", "In Scuba Flippers", "Misc", 3),
    "snow_shoes": MovementModifier("snow_shoes", "In Snow Shoes", "Misc", 2),
}

# Terrain presets for editor
TERRAIN_PRESETS: dict[str, TerrainPreset] = {
    "open": TerrainPreset("open", "Open Ground", 1, "#88cc88"),
    "road": TerrainPreset("road", "Road / Pavement", 1, "#aaaaaa"),
    "light_brush": TerrainPreset("light_brush", "Light Brush", 2, "#6b8e4e", ("brush_light",)),
    "medium_brush": TerrainPreset("medium_brush", "Medium Brush", 3, "#4a7a3a", ("brush_medium",)),
    "dense_brush": TerrainPreset("dense_brush", "Dense Brush", 4, "#2d5a2d", ("brush_dense",)),
    "water_shallow": TerrainPreset("water_shallow", "Shallow Water (1ft)", 2, "#4488cc", ("water_1ft",)),
    "water_deep": TerrainPreset("water_deep", "Deep Water (3ft)", 5, "#2255aa", ("water_3ft",)),
    "sand": TerrainPreset("sand", "Dry Sand", 2, "#d4c48a", ("dry_sand",)),
    "ice": TerrainPreset("ice", "Icy Surface", 3, "#cceeff", ("icy_surface",)),
    "uphill": TerrainPreset("uphill", "Uphill", 3, "#997755", ("slope_uphill",)),
    "rubble": TerrainPreset("rubble", "Rubble", 3, "#888888", ("brush_medium",)),
    "impassable": TerrainPreset("impassable", "Impassable", -1, "#333333"),
}


def compute_movement_cost(
    base_id: str = "forward",
    modifier_ids: list[str] | None = None,
    terrain_cost: int | None = None,
) -> int:
    """Compute total movement cost for entering a hex (per meter)."""
    if terrain_cost is not None and terrain_cost < 0:
        return -1
    base = MOVEMENT_BASE.get(base_id, MOVEMENT_BASE["forward"])
    total = base.cost
    if terrain_cost is not None:
        total = max(total, terrain_cost)
    for mid in modifier_ids or []:
        mod = MOVEMENT_MODIFIERS.get(mid)
        if mod:
            total += mod.cost
    return total
