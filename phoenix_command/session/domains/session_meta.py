"""Session metadata domain."""

from dataclasses import dataclass, field

from phoenix_command.session.domains.player_info import PlayerInfo
from phoenix_command.tables.catalogs.action_catalog import ActionCatalogState


@dataclass
class SessionMeta:
    """Host session identity and connected guests."""

    session_name: str = ""
    host_name: str = ""
    connected_guests: list[str] = field(default_factory=list)
    players: list[PlayerInfo] = field(default_factory=list)
    actions: ActionCatalogState = field(default_factory=ActionCatalogState)

    def to_dict(self) -> dict:
        return {
            "session_name": self.session_name,
            "host_name": self.host_name,
            "connected_guests": list(self.connected_guests),
            "players": [p.to_dict() for p in self.players],
            "actions": self.actions.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "SessionMeta":
        players_raw = data.get("players")
        if players_raw:
            players = [PlayerInfo.from_dict(p) for p in players_raw]
        else:
            players = []
            host_name = data.get("host_name", "")
            if host_name:
                players.append(PlayerInfo("host", host_name, is_host=True))
            for i, guest_name in enumerate(data.get("connected_guests", [])):
                players.append(PlayerInfo(f"guest-{i}", guest_name, is_host=False))
        return cls(
            session_name=data.get("session_name", ""),
            host_name=data.get("host_name", ""),
            connected_guests=list(data.get("connected_guests", [])),
            players=players,
            actions=ActionCatalogState.from_dict(data.get("actions")),
        )

    def get_player(self, player_id: str) -> PlayerInfo | None:
        for player in self.players:
            if player.player_id == player_id:
                return player
        return None
