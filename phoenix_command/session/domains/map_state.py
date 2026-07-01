"""Map domain: multi-layer hex grid for tactical maps."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any


def _hex_key(q: int, r: int) -> str:
    return f"{q},{r}"


def _wall_key(q: int, r: int, edge: int) -> str:
    return f"{q},{r}:{edge}"


def _parse_hex_key(key: str) -> tuple[int, int]:
    q, r = key.split(",")
    return int(q), int(r)


def _parse_wall_key(key: str) -> tuple[int, int, int]:
    coords, edge = key.rsplit(":", 1)
    q, r = coords.split(",")
    return int(q), int(r), int(edge)


@dataclass
class HexGridConfig:
    """Hex grid layout and scale."""

    orientation: str = "flat"  # "flat" or "pointy"
    size: float = 24.0  # hex radius in pixels
    origin_x: float = 0.0
    origin_y: float = 0.0
    meters_per_hex: float = 1.0
    cols: int = 20
    rows: int = 20

    def to_dict(self) -> dict:
        return {
            "orientation": self.orientation,
            "size": self.size,
            "origin_x": self.origin_x,
            "origin_y": self.origin_y,
            "meters_per_hex": self.meters_per_hex,
            "cols": self.cols,
            "rows": self.rows,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "HexGridConfig":
        return cls(
            orientation=data.get("orientation", "flat"),
            size=float(data.get("size", 24.0)),
            origin_x=float(data.get("origin_x", 0.0)),
            origin_y=float(data.get("origin_y", 0.0)),
            meters_per_hex=float(data.get("meters_per_hex", 1.0)),
            cols=int(data.get("cols", 20)),
            rows=int(data.get("rows", 20)),
        )


@dataclass
class BackgroundImage:
    """Layer background image embedded as base64."""

    data_b64: str = ""
    mime: str = "image/png"
    offset_x: float = 0.0
    offset_y: float = 0.0
    scale: float = 1.0
    rotation: float = 0.0
    opacity: float = 1.0

    def to_dict(self) -> dict:
        return {
            "data_b64": self.data_b64,
            "mime": self.mime,
            "offset_x": self.offset_x,
            "offset_y": self.offset_y,
            "scale": self.scale,
            "rotation": self.rotation,
            "opacity": self.opacity,
        }

    @classmethod
    def from_dict(cls, data: dict | None) -> "BackgroundImage | None":
        if not data:
            return None
        return cls(
            data_b64=data.get("data_b64", ""),
            mime=data.get("mime", "image/png"),
            offset_x=float(data.get("offset_x", 0.0)),
            offset_y=float(data.get("offset_y", 0.0)),
            scale=float(data.get("scale", 1.0)),
            rotation=float(data.get("rotation", 0.0)),
            opacity=float(data.get("opacity", 1.0)),
        )


@dataclass
class TerrainTile:
    """Terrain on a hex cell."""

    terrain_type: str = "open"
    movement_cost: int = 1
    color: str = "#88cc88"

    def to_dict(self) -> dict:
        return {
            "terrain_type": self.terrain_type,
            "movement_cost": self.movement_cost,
            "color": self.color,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "TerrainTile":
        return cls(
            terrain_type=data.get("terrain_type", "open"),
            movement_cost=int(data.get("movement_cost", 1)),
            color=data.get("color", "#88cc88"),
        )


@dataclass
class Obstacle:
    """Obstacle occupying a hex cell."""

    height: float = 1.0
    material: str = "common_furniture"
    thickness: float = 1.0  # inches per Table 7C
    protection_factor: float | None = None  # override; None = compute from catalog
    blocks_movement: bool = True
    blocks_los: bool = True

    def to_dict(self) -> dict:
        result: dict[str, Any] = {
            "height": self.height,
            "material": self.material,
            "thickness": self.thickness,
            "blocks_movement": self.blocks_movement,
            "blocks_los": self.blocks_los,
        }
        if self.protection_factor is not None:
            result["protection_factor"] = self.protection_factor
        return result

    @classmethod
    def from_dict(cls, data: dict) -> "Obstacle":
        pf = data.get("protection_factor")
        return cls(
            height=float(data.get("height", 1.0)),
            material=data.get("material", "common_furniture"),
            thickness=float(data.get("thickness", 1.0)),
            protection_factor=float(pf) if pf is not None else None,
            blocks_movement=bool(data.get("blocks_movement", True)),
            blocks_los=bool(data.get("blocks_los", True)),
        )

    def resolved_pf(self, custom_barriers: dict | None = None) -> float:
        from phoenix_command.tables.catalogs.barrier_catalog import resolve_protection_factor
        return resolve_protection_factor(
            self.material, self.thickness, custom_barriers, self.protection_factor
        )

    def tooltip_text(self, custom_barriers: dict | None = None) -> str:
        from phoenix_command.tables.catalogs.barrier_catalog import BUILTIN_BARRIERS
        mat = BUILTIN_BARRIERS.get(self.material)
        name = mat.name if mat else self.material
        pf = self.resolved_pf(custom_barriers)
        return (
            f"Obstacle: {name}\n"
            f"Height: {self.height:.1f} m\n"
            f"Thickness: {self.thickness:.2f}\"\n"
            f"PF: {pf:.1f}\n"
            f"Blocks movement: {self.blocks_movement}\n"
            f"Blocks LOS: {self.blocks_los}"
        )


@dataclass
class Opening:
    """Window or door on a wall segment."""

    kind: str = "window"  # "window" or "door"
    state: str = "closed"  # "locked", "closed", "open" (doors)
    position: float = 0.5  # 0..1 along edge

    def to_dict(self) -> dict:
        return {
            "kind": self.kind,
            "state": self.state,
            "position": self.position,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Opening":
        return cls(
            kind=data.get("kind", "window"),
            state=data.get("state", "closed"),
            position=float(data.get("position", 0.5)),
        )


@dataclass
class WallSegment:
    """Wall along a hex edge."""

    material: str = "cinder_block"
    thickness: float = 8.0  # inches
    protection_factor: float | None = None
    height: float = 2.5
    openings: list[Opening] = field(default_factory=list)

    def to_dict(self) -> dict:
        result: dict[str, Any] = {
            "material": self.material,
            "thickness": self.thickness,
            "height": self.height,
            "openings": [o.to_dict() for o in self.openings],
        }
        if self.protection_factor is not None:
            result["protection_factor"] = self.protection_factor
        return result

    @classmethod
    def from_dict(cls, data: dict) -> "WallSegment":
        pf = data.get("protection_factor")
        return cls(
            material=data.get("material", "cinder_block"),
            thickness=float(data.get("thickness", 8.0)),
            protection_factor=float(pf) if pf is not None else None,
            height=float(data.get("height", 2.5)),
            openings=[Opening.from_dict(o) for o in data.get("openings", [])],
        )

    def resolved_pf(self, custom_barriers: dict | None = None) -> float:
        from phoenix_command.tables.catalogs.barrier_catalog import resolve_protection_factor
        return resolve_protection_factor(
            self.material, self.thickness, custom_barriers, self.protection_factor
        )

    def tooltip_text(self, custom_barriers: dict | None = None) -> str:
        from phoenix_command.tables.catalogs.barrier_catalog import BUILTIN_BARRIERS
        mat = BUILTIN_BARRIERS.get(self.material)
        name = mat.name if mat else self.material
        pf = self.resolved_pf(custom_barriers)
        openings = ", ".join(f"{o.kind}({o.state})" for o in self.openings) or "none"
        return (
            f"Wall: {name}\n"
            f"Height: {self.height:.1f} m\n"
            f"Thickness: {self.thickness:.2f}\"\n"
            f"PF: {pf:.1f}\n"
            f"Openings: {openings}"
        )


@dataclass
class CustomBarrierMaterial:
    """User-defined barrier material with custom PF."""

    id: str
    name: str
    protection_factor: float

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "protection_factor": self.protection_factor,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "CustomBarrierMaterial":
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            protection_factor=float(data.get("protection_factor", 0.0)),
        )


@dataclass
class MapLayer:
    """One elevation layer of the map."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "Ground"
    kind: str = "ground"  # ground, floor, basement, trench
    elevation: int = 0
    background: BackgroundImage | None = None
    terrain: dict[str, TerrainTile] = field(default_factory=dict)
    obstacles: dict[str, Obstacle] = field(default_factory=dict)
    walls: dict[str, WallSegment] = field(default_factory=dict)
    visible: bool = True
    opacity: float = 1.0

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "kind": self.kind,
            "elevation": self.elevation,
            "background": self.background.to_dict() if self.background else None,
            "terrain": {k: v.to_dict() for k, v in self.terrain.items()},
            "obstacles": {k: v.to_dict() for k, v in self.obstacles.items()},
            "walls": {k: v.to_dict() for k, v in self.walls.items()},
            "visible": self.visible,
            "opacity": self.opacity,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "MapLayer":
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            name=data.get("name", "Ground"),
            kind=data.get("kind", "ground"),
            elevation=int(data.get("elevation", 0)),
            background=BackgroundImage.from_dict(data.get("background")),
            terrain={
                k: TerrainTile.from_dict(v) for k, v in data.get("terrain", {}).items()
            },
            obstacles={
                k: Obstacle.from_dict(v) for k, v in data.get("obstacles", {}).items()
            },
            walls={
                k: WallSegment.from_dict(v) for k, v in data.get("walls", {}).items()
            },
            visible=bool(data.get("visible", True)),
            opacity=float(data.get("opacity", 1.0)),
        )


@dataclass
class MapState:
    """Multi-layer hex map document."""

    grid: HexGridConfig = field(default_factory=HexGridConfig)
    layers: list[MapLayer] = field(default_factory=list)
    active_layer_id: str = ""
    custom_barriers: dict[str, CustomBarrierMaterial] = field(default_factory=dict)
    # Legacy fields for backward compatibility
    width: int = 0
    height: int = 0
    hexes: dict[str, int] = field(default_factory=dict)
    obstacles_legacy: dict[str, str] = field(default_factory=dict)

    def ensure_default_layer(self) -> MapLayer:
        if not self.layers:
            layer = MapLayer(name="Ground", kind="ground", elevation=0)
            self.layers.append(layer)
            self.active_layer_id = layer.id
            return layer
        if not self.active_layer_id:
            self.active_layer_id = self.layers[0].id
        for layer in self.layers:
            if layer.id == self.active_layer_id:
                return layer
        self.active_layer_id = self.layers[0].id
        return self.layers[0]

    def get_active_layer(self) -> MapLayer:
        return self.ensure_default_layer()

    def get_layer(self, layer_id: str) -> MapLayer | None:
        for layer in self.layers:
            if layer.id == layer_id:
                return layer
        return None

    def to_dict(self) -> dict:
        self.ensure_default_layer()
        return {
            "grid": self.grid.to_dict(),
            "layers": [layer.to_dict() for layer in self.layers],
            "active_layer_id": self.active_layer_id,
            "custom_barriers": {
                k: v.to_dict() for k, v in self.custom_barriers.items()
            },
        }

    @classmethod
    def from_dict(cls, data: dict) -> "MapState":
        if "layers" in data:
            layers = [MapLayer.from_dict(layer) for layer in data.get("layers", [])]
            custom = {
                k: CustomBarrierMaterial.from_dict(v)
                for k, v in data.get("custom_barriers", {}).items()
            }
            state = cls(
                grid=HexGridConfig.from_dict(data.get("grid", {})),
                layers=layers,
                active_layer_id=data.get("active_layer_id", ""),
                custom_barriers=custom,
            )
            state.ensure_default_layer()
            return state

        # Legacy stub format migration
        state = cls(
            width=data.get("width", 0),
            height=data.get("height", 0),
            hexes=dict(data.get("hexes", {})),
            obstacles_legacy=dict(data.get("obstacles", {})),
        )
        layer = MapLayer(name="Ground", kind="ground", elevation=0)
        for key, tile_id in state.hexes.items():
            layer.terrain[key] = TerrainTile(
                terrain_type=f"tile_{tile_id}",
                movement_cost=1,
            )
        for key, obstacle_type in state.obstacles_legacy.items():
            layer.obstacles[key] = Obstacle(material=obstacle_type)
        state.layers = [layer]
        state.active_layer_id = layer.id
        return state


def rules_hexes(meters: float) -> float:
    """Convert meters to rulebook hexes (1 rule hex = 2 m)."""
    return meters / 2.0
