"""Token domain (stub): character tokens on hex map."""

from dataclasses import dataclass, field


@dataclass
class TokenPlacement:
    """A token on the tactical map."""

    token_id: str
    character_name: str | None = None
    q: int = 0
    r: int = 0
    facing: int = 0
    status_markers: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "token_id": self.token_id,
            "character_name": self.character_name,
            "q": self.q,
            "r": self.r,
            "facing": self.facing,
            "status_markers": list(self.status_markers),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "TokenPlacement":
        return cls(
            token_id=data.get("token_id", ""),
            character_name=data.get("character_name"),
            q=data.get("q", 0),
            r=data.get("r", 0),
            facing=data.get("facing", 0),
            status_markers=list(data.get("status_markers", [])),
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
