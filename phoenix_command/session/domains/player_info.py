"""Connected player roster for shared sessions."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PlayerInfo:
    """A host or guest participant in a session."""

    player_id: str
    display_name: str
    is_host: bool = False

    def to_dict(self) -> dict:
        return {
            "player_id": self.player_id,
            "display_name": self.display_name,
            "is_host": self.is_host,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "PlayerInfo":
        return cls(
            player_id=data.get("player_id", ""),
            display_name=data.get("display_name", ""),
            is_host=bool(data.get("is_host", False)),
        )
