"""Map domain (stub): sparse hex grid for future tactical map."""

from dataclasses import dataclass, field


@dataclass
class MapState:
    """Sparse hex map: only occupied cells are stored."""

    width: int = 0
    height: int = 0
    hexes: dict[str, int] = field(default_factory=dict)  # "q,r" -> tile_id
    obstacles: dict[str, str] = field(default_factory=dict)  # "q,r" -> obstacle_type

    def to_dict(self) -> dict:
        return {
            "width": self.width,
            "height": self.height,
            "hexes": dict(self.hexes),
            "obstacles": dict(self.obstacles),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "MapState":
        return cls(
            width=data.get("width", 0),
            height=data.get("height", 0),
            hexes=dict(data.get("hexes", {})),
            obstacles=dict(data.get("obstacles", {})),
        )
