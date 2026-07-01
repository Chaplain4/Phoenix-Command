"""Table 7C — Cover Protection Factors catalog."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class BarrierDef:
    """Barrier material definition."""

    id: str
    name: str
    category: str
    pf_fixed: float | None = None
    pf_by_thickness: dict[float, float] = field(default_factory=dict)

    def pf_at_thickness(self, thickness: float) -> float:
        if self.pf_fixed is not None:
            return self.pf_fixed
        if not self.pf_by_thickness:
            return 0.0
        points = sorted(self.pf_by_thickness.items())
        if thickness <= points[0][0]:
            return points[0][1]
        if thickness >= points[-1][0]:
            return points[-1][1]
        for i in range(len(points) - 1):
            t0, pf0 = points[i]
            t1, pf1 = points[i + 1]
            if t0 <= thickness <= t1:
                ratio = (thickness - t0) / (t1 - t0)
                return pf0 + ratio * (pf1 - pf0)
        return points[-1][1]


BUILTIN_BARRIERS: dict[str, BarrierDef] = {}


def _register(barriers: list[BarrierDef]) -> None:
    for barrier in barriers:
        BUILTIN_BARRIERS[barrier.id] = barrier


_register([
    # Doors
    BarrierDef("door_automobile", "Automobile Door", "Doors", pf_fixed=2.0),
    BarrierDef("door_elevator", "Elevator Door", "Doors", pf_fixed=4.0),
    BarrierDef("door_exterior_wood", "Exterior Wood Door", "Doors", pf_fixed=2.0),
    BarrierDef("door_heavy_wood_gate", "Heavy Wood Gate", "Doors", pf_fixed=5.0),
    BarrierDef("door_interior_wood", "Interior Wood Door", "Doors", pf_fixed=0.3),
    BarrierDef("door_metal_fire", "Metal Fire Door", "Doors", pf_fixed=6.0),
    # Walls
    BarrierDef("wall_brick_6", "Brick Wall (6 inch)", "Walls", pf_fixed=370.0),
    BarrierDef("wall_brick_12", "Brick Wall (12 inch)", "Walls", pf_fixed=980.0),
    BarrierDef("wall_cinder_block", "Cinder Block", "Walls", pf_fixed=4.0),
    BarrierDef("wall_cinder_earth", "Cinder Block (Earth Filled)", "Walls", pf_fixed=25.0),
    BarrierDef("wall_cinder_concrete", "Cinder Block (Concrete Filled)", "Walls", pf_fixed=460.0),
    BarrierDef("wall_wood_interior_plaster", "Wood Frame (Interior Plaster)", "Walls", pf_fixed=0.3),
    BarrierDef("wall_wood_exterior_stucco", "Wood Frame (Exterior Stucco)", "Walls", pf_fixed=1.0),
    BarrierDef("wall_log_timber", "Wood Frame (Log Timber)", "Walls", pf_fixed=22.0),
    # Roofs and Floors
    BarrierDef("roof_asphalt_shingle", "Asphalt - Shingle Roof", "Roofs", pf_fixed=2.0),
    BarrierDef("roof_tile_slate", "Tile - Slate Roof", "Roofs", pf_fixed=4.0),
    BarrierDef("floor_house", "House Floor", "Floors", pf_fixed=1.0),
    BarrierDef("floor_high_rise", "High Rise Floor", "Floors", pf_fixed=260.0),
    # Miscellaneous
    BarrierDef("common_furniture", "Common Furniture", "Miscellaneous", pf_fixed=1.0),
    BarrierDef("drum_water", "55 gallon Drum (Water Filled)", "Miscellaneous", pf_fixed=8.0),
    BarrierDef("drum_earth", "55 gallon Drum (Earth Filled)", "Miscellaneous", pf_fixed=85.0),
    BarrierDef("drum_concrete", "55 gallon Drum (Concrete Filled)", "Miscellaneous", pf_fixed=3200.0),
    BarrierDef("horse", "Horse", "Miscellaneous", pf_fixed=18.0),
    BarrierDef("railroad_tie", "Railroad Tie", "Miscellaneous", pf_fixed=20.0),
    BarrierDef("telephone_pole", "Telephone Pole", "Miscellaneous", pf_fixed=30.0),
    BarrierDef("woods_light", "Woods Light (per 10 hexes)", "Miscellaneous", pf_fixed=1.0),
    BarrierDef("woods_medium", "Woods Medium (per 10 hexes)", "Miscellaneous", pf_fixed=4.0),
    BarrierDef("woods_heavy", "Woods Heavy (per 10 hexes)", "Miscellaneous", pf_fixed=17.0),
    # Thickness-based materials (small to medium)
    BarrierDef("aluminum", "Aluminum", "Materials", pf_by_thickness={
        0.12: 1, 0.25: 4, 0.5: 9, 0.75: 16, 1: 24, 2: 64, 4: 170,
    }),
    BarrierDef("bullet_proof_glass", "Bullet Proof Glass", "Materials", pf_by_thickness={
        0.12: 0.5, 0.25: 1, 0.5: 3, 0.75: 6, 1: 8, 2: 22, 4: 58,
    }),
    BarrierDef("fiberglass", "Fiberglass", "Materials", pf_by_thickness={
        0.12: 0.4, 0.25: 1, 0.5: 3, 0.75: 5, 1: 7, 2: 18, 4: 181,
    }),
    BarrierDef("steel", "Steel", "Materials", pf_by_thickness={
        0.12: 6, 0.25: 16, 0.5: 42, 0.75: 75, 1: 110, 2: 300, 4: 780,
    }),
    BarrierDef("steel_armor_plate", "Steel Armor Plate", "Materials", pf_by_thickness={
        0.12: 11, 0.25: 30, 0.5: 79, 0.75: 140, 1: 210, 2: 550, 4: 1500,
    }),
    BarrierDef("titanium_armor_plate", "Titanium Armor Plate", "Materials", pf_by_thickness={
        0.12: 5, 0.25: 13, 0.5: 35, 0.75: 62, 1: 93, 2: 250, 4: 650,
    }),
    BarrierDef("wood_thin", "Wood (thin)", "Materials", pf_by_thickness={
        0.12: 0.3, 0.25: 0.5, 0.5: 1, 0.75: 1, 1: 2, 2: 4, 4: 7,
    }),
    # Large thickness materials
    BarrierDef("concrete", "Concrete", "Materials", pf_by_thickness={
        6: 450, 8: 680, 10: 930, 12: 1200, 16: 1800, 24: 3200, 36: 5600,
    }),
    BarrierDef("earth_hand_packed", "Earth (hand packed)", "Materials", pf_by_thickness={
        6: 20, 8: 27, 10: 34, 12: 40, 16: 54, 24: 80, 36: 120,
    }),
    BarrierDef("earth_hard_ground", "Earth (hard ground)", "Materials", pf_by_thickness={
        6: 24, 8: 32, 10: 41, 12: 48, 16: 65, 24: 96, 36: 140,
    }),
    BarrierDef("rock", "Rock", "Materials", pf_by_thickness={
        6: 900, 8: 1300, 10: 1800, 12: 2400, 16: 3600, 24: 6400, 36: 11000,
    }),
    BarrierDef("sand_loose", "Sand (loose)", "Materials", pf_by_thickness={
        6: 11, 8: 15, 10: 19, 12: 23, 16: 30, 24: 45, 36: 68,
    }),
    BarrierDef("water", "Water", "Materials", pf_by_thickness={
        6: 1, 8: 2, 10: 2, 12: 2, 16: 3, 24: 5, 36: 7,
    }),
    BarrierDef("wood_thick", "Wood (thick)", "Materials", pf_by_thickness={
        6: 11, 8: 15, 10: 18, 12: 22, 16: 29, 24: 44, 36: 66,
    }),
])


def resolve_protection_factor(
    material_id: str,
    thickness: float,
    custom_barriers: dict | None = None,
    override_pf: float | None = None,
) -> float:
    """Resolve PF for a material at given thickness."""
    if override_pf is not None:
        return override_pf
    if custom_barriers and material_id in custom_barriers:
        entry = custom_barriers[material_id]
        if hasattr(entry, "protection_factor"):
            return entry.protection_factor
        return float(entry.get("protection_factor", 0))
    barrier = BUILTIN_BARRIERS.get(material_id)
    if barrier is None:
        return 0.0
    return barrier.pf_at_thickness(thickness)
