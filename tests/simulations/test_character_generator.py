"""Tests for character generation."""

from phoenix_command.item_database.weapons import uzi, ammo_9mm_uzi_fmj
from phoenix_command.models.gear import Gear
from phoenix_command.simulations.character_generator import CharacterGenerator


def test_generate_character_with_fixed_characteristics():
    """Test character generation with fixed characteristics."""
    character = CharacterGenerator.generate_character(
        gun_combat_skill_level=5,
        strength=16,
        intelligence=12,
        will=14,
        health=11,
        agility=10
    )
    
    assert character.strength == 16
    assert character.intelligence == 12
    assert character.will == 14
    assert character.health == 11
    assert character.agility == 10
    assert character.gun_combat_skill_level == 5
    assert character.encumbrance == 0.0
    
    # Add equipment and verify encumbrance updates
    character.add_gear(uzi)
    assert character.encumbrance == 9.0
    character.add_gear(ammo_9mm_uzi_fmj)
    character.add_gear(ammo_9mm_uzi_fmj)
    character.add_gear(ammo_9mm_uzi_fmj)
    assert character.encumbrance == 12.9
    
    # Verify derived values with encumbrance
    assert character.base_speed == 3.0
    assert character.max_speed == 6
    assert character.skill_accuracy_level == 11
    assert character.intelligence_skill_factor == 23
    assert character.combat_actions == 7
    assert character.impulses == [2, 1, 2, 2]
    assert character.knockout_value == 35


def test_add_remove_gear():
    """Test adding and removing gear updates encumbrance."""
    character = CharacterGenerator.generate_character(
        gun_combat_skill_level=3,
        strength=15,
        agility=12
    )
    
    assert character.encumbrance == 0.0
    
    gear1 = Gear(name="Rifle", weight=10.0)
    gear2 = Gear(name="Armor", weight=15.0)
    
    character.add_gear(gear1)
    assert character.encumbrance == 10.0
    
    character.add_gear(gear2)
    assert character.encumbrance == 25.0
    
    character.remove_gear(gear1)
    assert character.encumbrance == 15.0
    
    character.remove_gear(gear2)
    assert character.encumbrance == 0.0


def test_properties_recalculate_dynamically():
    """Test that properties recalculate when gear changes."""
    character = CharacterGenerator.generate_character(
        gun_combat_skill_level=5,
        strength=18,
        agility=15
    )
    
    # No encumbrance - high speed
    initial_base_speed = character.base_speed
    initial_max_speed = character.max_speed
    
    # Add heavy gear
    heavy_gear = Gear(name="Heavy Armor", weight=50.0)
    character.add_gear(heavy_gear)
    
    # Speed should decrease
    assert character.base_speed < initial_base_speed
    assert character.max_speed <= initial_max_speed


def test_generate_character_random_characteristics():
    """Test character generation with random characteristics."""
    character = CharacterGenerator.generate_character(gun_combat_skill_level=3)
    
    # Verify characteristics are in valid range (3-18 for 3d6)
    assert 3 <= character.strength <= 18
    assert 3 <= character.intelligence <= 18
    assert 3 <= character.will <= 18
    assert 3 <= character.health <= 18
    assert 3 <= character.agility <= 18
    
    # Verify derived values exist
    assert character.base_speed >= 0.0
    assert character.max_speed >= 0
    assert character.skill_accuracy_level == 9
    assert character.combat_actions > 0
    assert len(character.impulses) == 4


def test_roll_characteristic():
    """Test characteristic rolling produces valid values."""
    for _ in range(100):
        roll = CharacterGenerator.roll_characteristic()
        assert 3 <= roll <= 18
