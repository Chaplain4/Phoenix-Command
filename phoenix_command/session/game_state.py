"""Root GameState document with versioned domains."""

from dataclasses import dataclass, field

from phoenix_command.session.domains.combat_state import CombatState
from phoenix_command.session.domains.impulse_combat_state import ImpulseCombatState
from phoenix_command.session.domains.map_state import MapState
from phoenix_command.session.domains.session_meta import SessionMeta
from phoenix_command.session.domains.token_state import TokenState

SCHEMA_VERSION = 1


@dataclass
class GameState:
    """Versioned shared game document."""

    schema_version: int = SCHEMA_VERSION
    revision: int = 0
    meta: SessionMeta = field(default_factory=SessionMeta)
    combat: CombatState = field(default_factory=CombatState)
    map: MapState | None = None
    tokens: TokenState | None = None
    impulse_combat: ImpulseCombatState = field(default_factory=ImpulseCombatState)

    def to_dict(self) -> dict:
        result = {
            "schema_version": self.schema_version,
            "revision": self.revision,
            "meta": self.meta.to_dict(),
            "combat": self.combat.to_dict(),
            "impulse_combat": self.impulse_combat.to_dict(),
        }
        if self.map is not None:
            result["map"] = self.map.to_dict()
        if self.tokens is not None:
            result["tokens"] = self.tokens.to_dict()
        return result

    @classmethod
    def from_dict(cls, data: dict) -> "GameState":
        schema = data.get("schema_version", 1)
        if schema > SCHEMA_VERSION:
            raise ValueError(
                f"Unsupported schema version {schema}; upgrade the application."
            )
        map_data = data.get("map")
        tokens_data = data.get("tokens")
        return cls(
            schema_version=schema,
            revision=data.get("revision", 0),
            meta=SessionMeta.from_dict(data.get("meta", {})),
            combat=CombatState.from_dict(data.get("combat", {})),
            map=MapState.from_dict(map_data) if map_data is not None else None,
            tokens=TokenState.from_dict(tokens_data) if tokens_data is not None else None,
            impulse_combat=ImpulseCombatState.from_dict(data.get("impulse_combat")),
        )

    def bump_revision(self) -> int:
        """Increment revision and return new value."""
        self.revision += 1
        return self.revision
