"""Character model for Phoenix Command."""

from dataclasses import dataclass, field
from phoenix_command.models.gear import Gear, Armor
from phoenix_command.models.enums import AdvancedHitLocation
from phoenix_command.tables.core.table1_character_generation import Table1CharacterGeneration


@dataclass(eq=False)
class Character:
    """Represents a Phoenix Command character with all attributes and derived values."""

    strength: int
    intelligence: int
    will: int
    health: int
    agility: int

    gun_combat_skill_level: int

    physical_damage_total: int = 0
    equipment: list[Gear] = field(default_factory=list)
    
    @property
    def encumbrance(self) -> float:
        """Total weight of all carried equipment."""
        return sum(item.weight for item in self.equipment)
    
    @property
    def armor_protection(self) -> dict[tuple[AdvancedHitLocation, bool], tuple[int, int]]:
        """Combined armor protection from all worn armor pieces.
        
        Returns:
            dict mapping (location, is_front) -> (protection_factor, blunt_protection_factor)
        """
        combined = {}
        for item in self.equipment:
            if isinstance(item, Armor):
                for key, protection_data in item.protection.items():
                    if key not in combined:
                        combined[key] = (0, 0)
                    pf, bpf = combined[key]
                    combined[key] = (
                        pf + protection_data.get_total_protection(),
                        bpf + protection_data.get_total_blunt_protection()
                    )
        return combined
    
    @property
    def base_speed(self) -> float:
        """Base speed from Table 1A."""
        return Table1CharacterGeneration.get_base_speed_1a(self.strength, self.encumbrance)
    
    @property
    def max_speed(self) -> int:
        """Maximum speed from Table 1B."""
        return int(Table1CharacterGeneration.get_max_speed_1b(self.agility, self.base_speed))
    
    @property
    def skill_accuracy_level(self) -> int:
        """Skill accuracy level from Table 1C."""
        return Table1CharacterGeneration.get_skill_accuracy_level_1c(self.gun_combat_skill_level)
    
    @property
    def intelligence_skill_factor(self) -> int:
        """Intelligence + Skill Accuracy Level."""
        return self.intelligence + self.skill_accuracy_level
    
    @property
    def combat_actions(self) -> int:
        """Combat actions from Table 1D."""
        return Table1CharacterGeneration.get_combat_actions_1d(self.max_speed, self.intelligence_skill_factor)
    
    @property
    def impulses(self) -> list[int]:
        """Combat actions per impulse from Table 1E."""
        return Table1CharacterGeneration.get_impulses_1e(self.combat_actions)
    
    @property
    def knockout_value(self) -> int:
        """Knockout value = 0.5 × Will × Skill Level."""
        return int(0.5 * self.will * self.gun_combat_skill_level)
    
    @property
    def defensive_alm(self) -> int:
        """Defensive Accuracy Level Modifier based on ISF."""
        return Table1CharacterGeneration.get_defensive_alm(self.intelligence_skill_factor)
    
    def add_gear(self, gear: Gear) -> None:
        """Add equipment to character."""
        self.equipment.append(gear)
    
    def remove_gear(self, gear: Gear) -> None:
        """Remove equipment from character."""
        self.equipment.remove(gear)
    
    def apply_damage(self, damage: int) -> None:
        """Apply physical damage to character."""
        self.physical_damage_total += damage
