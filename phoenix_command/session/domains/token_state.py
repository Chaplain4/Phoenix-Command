"""Token domain: character tokens on hex map."""

from __future__ import annotations

from dataclasses import dataclass, field

FACING_RESOLUTION = 12


@dataclass
class TokenPlacement:
    """A token on the tactical map."""

    token_id: str
    character_name: str | None = None
    layer_id: str = ""
    q: int = 0
    r: int = 0
    facing: int = 0  # 0-11: every 30° (even=side, odd=corner on flat-top grid)
    status_markers: list[str] = field(default_factory=list)
    image_b64: str = ""
    image_mime: str = "image/png"
    label: str = ""
    size: float = 0.35  # diameter in hexes
    scale_x: float = 1.0
    scale_y: float = 1.0
    side_id: str = ""
    controlled_by: str | None = None  # player_id; None = host-only / unassigned

    def to_dict(self) -> dict:
        return {
            "token_id": self.token_id,
            "character_name": self.character_name,
            "layer_id": self.layer_id,
            "q": self.q,
            "r": self.r,
            "facing": self.facing,
            "facing_resolution": FACING_RESOLUTION,
            "status_markers": list(self.status_markers),
            "image_b64": self.image_b64,
            "image_mime": self.image_mime,
            "label": self.label,
            "size": self.size,
            "scale_x": self.scale_x,
            "scale_y": self.scale_y,
            "side_id": self.side_id,
            "controlled_by": self.controlled_by,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "TokenPlacement":
        facing = int(data.get("facing", 0))
        if data.get("facing_resolution") != FACING_RESOLUTION and facing <= 5:
            facing *= 2
        return cls(
            token_id=data.get("token_id", ""),
            character_name=data.get("character_name"),
            layer_id=data.get("layer_id", ""),
            q=int(data.get("q", 0)),
            r=int(data.get("r", 0)),
            facing=facing,
            status_markers=list(data.get("status_markers", [])),
            image_b64=data.get("image_b64", ""),
            image_mime=data.get("image_mime", "image/png"),
            label=data.get("label", ""),
            size=float(data.get("size", 1.0)),
            scale_x=float(data.get("scale_x", 1.0)),
            scale_y=float(data.get("scale_y", 1.0)),
            side_id=data.get("side_id", ""),
            controlled_by=data.get("controlled_by"),
        )


@dataclass
class TokenState:
    """All token placements."""

    placements: dict[str, TokenPlacement] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "placements": {
                tid: p.to_dict() for tid, p in self.placements.items()
            },
        }

    @classmethod
    def from_dict(cls, data: dict) -> "TokenState":
        raw = data.get("placements", {})
        return cls(
            placements={
                tid: TokenPlacement.from_dict(p) for tid, p in raw.items()
            },
        )
