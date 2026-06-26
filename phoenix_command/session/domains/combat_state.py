"""Combat domain: characters, combat zone, log."""

from dataclasses import dataclass, field


@dataclass
class CombatZoneState:
    """Shooter and target placement by character name."""

    shooter_name: str | None = None
    target_names: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "shooter_name": self.shooter_name,
            "target_names": list(self.target_names),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "CombatZoneState":
        return cls(
            shooter_name=data.get("shooter_name"),
            target_names=list(data.get("target_names", [])),
        )


@dataclass
class CombatLogEntry:
    """Single combat log line with optional color category."""

    message: str
    category: str = "system"  # hit, critical, miss, system

    def to_dict(self) -> dict:
        return {"message": self.message, "category": self.category}

    @classmethod
    def from_dict(cls, data: dict) -> "CombatLogEntry":
        return cls(
            message=data.get("message", ""),
            category=data.get("category", "system"),
        )


@dataclass
class CombatState:
    """Combat-related shared state."""

    characters: list[dict] = field(default_factory=list)
    combat_zone: CombatZoneState = field(default_factory=CombatZoneState)
    selected_character_name: str | None = None
    combat_log: list[CombatLogEntry] = field(default_factory=list)
    detailed_log: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "characters": list(self.characters),
            "combat_zone": self.combat_zone.to_dict(),
            "selected_character_name": self.selected_character_name,
            "combat_log": [e.to_dict() for e in self.combat_log],
            "detailed_log": list(self.detailed_log),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "CombatState":
        return cls(
            characters=list(data.get("characters", [])),
            combat_zone=CombatZoneState.from_dict(data.get("combat_zone", {})),
            selected_character_name=data.get("selected_character_name"),
            combat_log=[CombatLogEntry.from_dict(e) for e in data.get("combat_log", [])],
            detailed_log=list(data.get("detailed_log", [])),
        )
