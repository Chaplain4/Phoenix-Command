"""Character generation system for Phoenix Command."""

import random
from phoenix_command.models.character import Character


class CharacterGenerator:
    """Generates Phoenix Command characters following the official rules."""
    
    @staticmethod
    def roll_characteristic() -> int:
        """Roll 3d6 for a characteristic value."""
        return sum(random.randint(1, 6) for _ in range(3))
    
    @staticmethod
    def generate_character(
        gun_combat_skill_level: int,
        strength: int = None,
        intelligence: int = None,
        will: int = None,
        health: int = None,
        agility: int = None
    ) -> Character:
        """Generate a complete character following Phoenix Command rules."""
        return Character(
            strength=strength if strength is not None else CharacterGenerator.roll_characteristic(),
            intelligence=intelligence if intelligence is not None else CharacterGenerator.roll_characteristic(),
            will=will if will is not None else CharacterGenerator.roll_characteristic(),
            health=health if health is not None else CharacterGenerator.roll_characteristic(),
            agility=agility if agility is not None else CharacterGenerator.roll_characteristic(),
            gun_combat_skill_level=gun_combat_skill_level
        )
