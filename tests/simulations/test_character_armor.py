"""Tests for character armor protection."""

from phoenix_command.simulations.character_generator import CharacterGenerator
from phoenix_command.models.gear import Armor
from phoenix_command.models.enums import AdvancedHitLocation, ArmorMaterial


def test_armor_protection_empty():
    """Test armor protection with no armor."""
    character = CharacterGenerator.generate_character(
        gun_combat_skill_level=5,
        strength=15,
        agility=12
    )
    
    assert character.armor_protection == {}


def test_armor_protection_single_armor():
    """Test armor protection with single armor piece."""
    character = CharacterGenerator.generate_character(
        gun_combat_skill_level=5,
        strength=15,
        agility=12
    )
    
    armor = Armor(name="Chest Plate", weight=10.0)
    armor.add_protection(
        location=AdvancedHitLocation.HEART,
        is_front=True,
        material=ArmorMaterial.STEEL,
        protection_factor=15,
        blunt_protection_factor=5
    )
    
    character.add_gear(armor)
    
    protection = character.armor_protection
    assert (AdvancedHitLocation.HEART, True) in protection
    assert protection[(AdvancedHitLocation.HEART, True)] == (15, 5)


def test_armor_protection_multiple_locations():
    """Test armor protection covering multiple locations."""
    character = CharacterGenerator.generate_character(
        gun_combat_skill_level=5,
        strength=15,
        agility=12
    )
    
    armor = Armor(name="Body Armor", weight=15.0)
    armor.add_protection(AdvancedHitLocation.HEART, True, ArmorMaterial.KEVLAR, 20, 8)
    armor.add_protection(AdvancedHitLocation.LUNG, True, ArmorMaterial.KEVLAR, 20, 8)
    armor.add_protection(AdvancedHitLocation.STOMACH, True, ArmorMaterial.KEVLAR, 18, 7)
    
    character.add_gear(armor)
    
    protection = character.armor_protection
    assert len(protection) == 3
    assert protection[(AdvancedHitLocation.HEART, True)] == (20, 8)
    assert protection[(AdvancedHitLocation.LUNG, True)] == (20, 8)
    assert protection[(AdvancedHitLocation.STOMACH, True)] == (18, 7)


def test_armor_protection_stacking():
    """Test that multiple armor pieces stack protection."""
    character = CharacterGenerator.generate_character(
        gun_combat_skill_level=5,
        strength=18,
        agility=12
    )
    
    # First armor layer
    armor1 = Armor(name="Soft Armor", weight=8.0)
    armor1.add_protection(AdvancedHitLocation.HEART, True, ArmorMaterial.KEVLAR, 12, 4)
    
    # Second armor layer
    armor2 = Armor(name="Plate Carrier", weight=12.0)
    armor2.add_protection(AdvancedHitLocation.HEART, True, ArmorMaterial.STEEL, 18, 6)
    
    character.add_gear(armor1)
    character.add_gear(armor2)
    
    protection = character.armor_protection
    # Protection should stack: 12 + 18 = 30, 4 + 6 = 10
    assert protection[(AdvancedHitLocation.HEART, True)] == (30, 10)


def test_armor_protection_front_and_rear():
    """Test armor protection for front and rear separately."""
    character = CharacterGenerator.generate_character(
        gun_combat_skill_level=5,
        strength=15,
        agility=12
    )
    
    armor = Armor(name="Full Body Armor", weight=20.0)
    armor.add_protection(AdvancedHitLocation.HEART, True, ArmorMaterial.STEEL, 20, 8)
    armor.add_protection(AdvancedHitLocation.HEART, False, ArmorMaterial.STEEL, 15, 6)
    
    character.add_gear(armor)
    
    protection = character.armor_protection
    assert protection[(AdvancedHitLocation.HEART, True)] == (20, 8)
    assert protection[(AdvancedHitLocation.HEART, False)] == (15, 6)


def test_armor_protection_updates_on_remove():
    """Test that armor protection updates when armor is removed."""
    character = CharacterGenerator.generate_character(
        gun_combat_skill_level=5,
        strength=15,
        agility=12
    )
    
    armor = Armor(name="Vest", weight=10.0)
    armor.add_protection(AdvancedHitLocation.HEART, True, ArmorMaterial.KEVLAR, 15, 5)
    
    character.add_gear(armor)
    assert len(character.armor_protection) == 1
    
    character.remove_gear(armor)
    assert len(character.armor_protection) == 0
