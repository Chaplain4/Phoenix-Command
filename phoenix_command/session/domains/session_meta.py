"""Session metadata domain."""

from dataclasses import dataclass, field

from phoenix_command.tables.catalogs.action_catalog import ActionCatalogState


@dataclass
class SessionMeta:
    """Host session identity and connected guests."""

    session_name: str = ""
    host_name: str = ""
    connected_guests: list[str] = field(default_factory=list)
    actions: ActionCatalogState = field(default_factory=ActionCatalogState)

    def to_dict(self) -> dict:
        return {
            "session_name": self.session_name,
            "host_name": self.host_name,
            "connected_guests": list(self.connected_guests),
            "actions": self.actions.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "SessionMeta":
        return cls(
            session_name=data.get("session_name", ""),
            host_name=data.get("host_name", ""),
            connected_guests=list(data.get("connected_guests", [])),
            actions=ActionCatalogState.from_dict(data.get("actions")),
        )
