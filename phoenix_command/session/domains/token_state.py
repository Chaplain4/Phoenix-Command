"""Token domain: character tokens on hex map."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class TokenPlacement:
    """A token on the tactical map."""

    token_id: str
    character_name: str | None = None
    layer_id: str = ""
    q: int = 0
    r: int = 0
    facing: int = 0
    status_markers: list[str] = field(default_factory=list)
    image_b64: str = ""
    image_mime: str = "image/png"
    label: str = ""
    size: float = 1.0  # diameter in hexes

    def to_dict(self) -> dict:
        return {
            "token_id": self.token_id,
            "character_name": self.character_name,
            "layer_id": self.layer_id,
            "q": self.q,
            "r": self.r,
            "facing": self.facing,
            "status_markers": list(self.status_markers),
            "image_b64": self.image_b64,
            "image_mime": self.image_mime,
            "label": self.label,
            "size": self.size,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "TokenPlacement":
        return cls(
            token_id=data.get("token_id", ""),
            character_name=data.get("character_name"),
            layer_id=data.get("layer_id", ""),
            q=int(data.get("q", 0)),
            r=int(data.get("r", 0)),
            facing=int(data.get("facing", 0)),
            status_markers=list(data.get("status_markers", [])),
            image_b64=data.get("image_b64", ""),
            image_mime=data.get("image_mime", "image/png"),
            label=data.get("label", ""),
            size=float(data.get("size", 1.0)),
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
