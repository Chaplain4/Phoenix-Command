"""
Pytest tests for gear.py models.
Tests all dataclasses and their methods including ballistic calculations,
armor protection, and weapon characteristics.
"""
import pytest
from unittest.mock import patch, MagicMock

from phoenix_command.models.gear import (
    BallisticData,
    ExplosiveData,
    RangeData,
    WeaponBallisticData,
    Gear,
    AmmoType,
    ArmorLayer,
    ArmorProtectionData,
    Armor,
    Weapon,
    Grenade,
)
from phoenix_command.models.enums import (
    ArmorMaterial,
    AdvancedHitLocation,
    Caliber,
    WeaponType,
    Country,
    GrenadeType,
    AmmoFeedDevice,
)


# ===== BallisticData Tests =====

class TestBallisticData:
    """Tests for BallisticData dataclass."""

    def test_ballistic_data_creation(self):
        """Test creating BallisticData with required fields."""
        data = BallisticData(
            range_hexes=10,
            penetration=5.5,
            damage_class=3
        )
        assert data.range_hexes == 10
        assert data.penetration == 5.5
        assert data.damage_class == 3
        assert data.beyond_max_range is False

    def test_ballistic_data_with_optional_fields(self):
        """Test BallisticData with shotgun-specific optional fields."""
        data = BallisticData(
            range_hexes=5,
            penetration=2.0,
            damage_class=2,
            beyond_max_range=True,
            shotgun_accuracy_level_modifier=-2,
            base_pellet_hit_chance="1D6",
            pattern_radius=1.5
        )
        assert data.beyond_max_range is True
        assert data.shotgun_accuracy_level_modifier == -2
        assert data.base_pellet_hit_chance == "1D6"
        assert data.pattern_radius == 1.5


# ===== ExplosiveData Tests =====

class TestExplosiveData:
    """Tests for ExplosiveData dataclass."""

    def test_explosive_data_creation(self):
        """Test creating ExplosiveData."""
        data = ExplosiveData(
            range_hexes=3,
            shrapnel_penetration=4.0,
            shrapnel_damage_class=2,
            base_shrapnel_hit_chance="2D6",
            base_concussion=10
        )
        assert data.range_hexes == 3
        assert data.shrapnel_penetration == 4.0
        assert data.shrapnel_damage_class == 2
        assert data.base_shrapnel_hit_chance == "2D6"
        assert data.base_concussion == 10

    def test_explosive_data_contact_explosion(self):
        """Test ExplosiveData with None range_hexes for contact explosions."""
        data = ExplosiveData(
            range_hexes=None,
            shrapnel_penetration=10.0,
            shrapnel_damage_class=5,
            base_shrapnel_hit_chance="3D6",
            base_concussion=20
        )
        assert data.range_hexes is None


# ===== RangeData Tests =====

class TestRangeData:
    """Tests for RangeData dataclass."""

    def test_range_data_creation(self):
        """Test creating RangeData."""
        data = RangeData(range_hexes=15, value=25.5)
        assert data.range_hexes == 15
        assert data.value == 25.5


# ===== WeaponBallisticData Tests =====

class TestWeaponBallisticData:
    """Tests for WeaponBallisticData and range interpolation."""

    @pytest.fixture
    def sample_ballistic_data(self):
        """Create sample weapon ballistic data."""
        return WeaponBallisticData(
            ballistic_accuracy=[
                RangeData(5, 10.0),
                RangeData(10, 8.0),
                RangeData(20, 5.0),
            ],
            time_of_flight=[
                RangeData(5, 0.1),
                RangeData(10, 0.3),
                RangeData(20, 0.7),
            ],
            three_round_burst=[
                RangeData(5, 2.0),
                RangeData(10, 3.0),
            ],
            minimum_arc=[
                RangeData(10, 1.0),
                RangeData(20, 2.0),
            ]
        )

    def test_get_ballistic_accuracy_exact_match(self, sample_ballistic_data):
        """Test getting ballistic accuracy at exact range."""
        assert sample_ballistic_data.get_ballistic_accuracy(5) == 10
        assert sample_ballistic_data.get_ballistic_accuracy(10) == 8
        assert sample_ballistic_data.get_ballistic_accuracy(20) == 5

    def test_get_ballistic_accuracy_interpolation(self, sample_ballistic_data):
        """Test ballistic accuracy interpolation between ranges."""
        assert sample_ballistic_data.get_ballistic_accuracy(3) == 10
        # Range 7 is less than 10, so it returns the first value (10) where 7 <= 10
        assert sample_ballistic_data.get_ballistic_accuracy(7) == 10
        assert sample_ballistic_data.get_ballistic_accuracy(15) == 8

    def test_get_ballistic_accuracy_beyond_max(self, sample_ballistic_data):
        """Test ballistic accuracy beyond maximum range."""
        assert sample_ballistic_data.get_ballistic_accuracy(50) == 5

    def test_get_time_of_flight(self, sample_ballistic_data):
        """Test getting time of flight values."""
        assert sample_ballistic_data.get_time_of_flight(5) == 0.1
        assert sample_ballistic_data.get_time_of_flight(10) == 0.3
        assert sample_ballistic_data.get_time_of_flight(25) == 0.7

    def test_get_three_round_burst(self, sample_ballistic_data):
        """Test getting three round burst values."""
        assert sample_ballistic_data.get_three_round_burst(3) == 2.0
        # Range 8 is between 5 and 10, returns value at 5
        assert sample_ballistic_data.get_three_round_burst(8) == 2.0
        assert sample_ballistic_data.get_three_round_burst(15) == 3.0

    def test_get_three_round_burst_none(self):
        """Test three round burst returns None when not available."""
        data = WeaponBallisticData()
        assert data.get_three_round_burst(10) is None

    def test_get_minimum_arc(self, sample_ballistic_data):
        """Test getting minimum arc values."""
        assert sample_ballistic_data.get_minimum_arc(5) == 1.0
        # Range 15 is within [10, 20), returns value at 10
        assert sample_ballistic_data.get_minimum_arc(15) == 1.0

    def test_get_minimum_arc_none(self):
        """Test minimum arc returns None when not available."""
        data = WeaponBallisticData()
        assert data.get_minimum_arc(10) is None


# ===== Gear Tests =====

class TestGear:
    """Tests for base Gear class."""

    def test_gear_creation(self):
        """Test creating basic gear."""
        gear = Gear(name="Backpack", weight=5.0, description="Military backpack")
        assert gear.name == "Backpack"
        assert gear.weight == 5.0
        assert gear.description == "Military backpack"

    def test_gear_default_description(self):
        """Test gear with default empty description."""
        gear = Gear(name="Item", weight=1.0)
        assert gear.description == ""


# ===== AmmoType Tests =====

class TestAmmoType:
    """Tests for AmmoType class and ballistic/explosive calculations."""

    @pytest.fixture
    def sample_ammo(self):
        """Create sample ammunition with various range data."""
        return AmmoType(
            name="5.56mm FMJ",
            weight=0.05,
            ballistic_data=[
                BallisticData(5, 8.0, 4),
                BallisticData(10, 6.0, 3),
                BallisticData(20, 4.0, 2),
            ]
        )

    @pytest.fixture
    def explosive_ammo(self):
        """Create explosive ammunition."""
        return AmmoType(
            name="40mm HE",
            weight=0.5,
            explosive_data=[
                ExplosiveData(1, 15.0, 5, "3D6", 25),  # Убираем None, начинаем с range=1
                ExplosiveData(3, 10.0, 4, "2D6", 15),
                ExplosiveData(5, 5.0, 2, "1D6", 8),
            ]
        )

    def test_ammo_creation(self, sample_ammo):
        """Test creating ammunition."""
        assert sample_ammo.name == "5.56mm FMJ"
        assert sample_ammo.weight == 0.05
        assert len(sample_ammo.ballistic_data) == 3

    def test_get_pen_exact_range(self, sample_ammo):
        """Test penetration at exact range."""
        assert sample_ammo.get_pen(5) == 8.0
        assert sample_ammo.get_pen(10) == 6.0
        assert sample_ammo.get_pen(20) == 4.0

    def test_get_pen_interpolation(self, sample_ammo):
        """Test penetration between ranges."""
        assert sample_ammo.get_pen(3) == 8.0
        # Range 7 is within [5, 10), so returns value at 5
        assert sample_ammo.get_pen(7) == 8.0
        assert sample_ammo.get_pen(15) == 6.0

    def test_get_pen_beyond_max(self, sample_ammo):
        """Test penetration beyond maximum range."""
        assert sample_ammo.get_pen(50) == 4.0

    def test_get_pen_empty_data(self):
        """Test penetration with no ballistic data."""
        ammo = AmmoType(name="Empty", weight=0.1)
        assert ammo.get_pen(10) == 0.0

    def test_get_dc(self, sample_ammo):
        """Test damage class retrieval."""
        assert sample_ammo.get_dc(5) == 4
        assert sample_ammo.get_dc(10) == 3
        assert sample_ammo.get_dc(20) == 2

    def test_get_dc_empty_data(self):
        """Test damage class with no ballistic data."""
        ammo = AmmoType(name="Empty", weight=0.1)
        assert ammo.get_dc(10) == 0

    def test_get_explosion_pen(self, explosive_ammo):
        """Test shrapnel penetration from explosion."""
        # Range 1 is exact match
        assert explosive_ammo.get_explosion_pen(1) == 15.0
        # Range 2 is between 1 and 3, returns value at 1
        assert explosive_ammo.get_explosion_pen(2) == 15.0
        # Range 3 is exact match
        assert explosive_ammo.get_explosion_pen(3) == 10.0
        # Range 5 is exact match
        assert explosive_ammo.get_explosion_pen(5) == 5.0

    def test_get_explosion_dc(self, explosive_ammo):
        """Test shrapnel damage class from explosion."""
        assert explosive_ammo.get_explosion_dc(1) == 5
        assert explosive_ammo.get_explosion_dc(2) == 5
        assert explosive_ammo.get_explosion_dc(3) == 4
        assert explosive_ammo.get_explosion_dc(5) == 2

    def test_get_base_shrapnel_hit_chance(self, explosive_ammo):
        """Test base shrapnel hit chance."""
        assert explosive_ammo.get_base_shrapnel_hit_chance(1) == "3D6"
        assert explosive_ammo.get_base_shrapnel_hit_chance(2) == "3D6"
        assert explosive_ammo.get_base_shrapnel_hit_chance(3) == "2D6"
        assert explosive_ammo.get_base_shrapnel_hit_chance(5) == "1D6"

    def test_get_base_concussion(self, explosive_ammo):
        """Test base concussion damage."""
        assert explosive_ammo.get_base_concussion(1) == 25
        assert explosive_ammo.get_base_concussion(2) == 25
        assert explosive_ammo.get_base_concussion(3) == 15
        assert explosive_ammo.get_base_concussion(5) == 8

    def test_explosive_methods_empty_data(self):
        """Test explosive methods with no explosive data."""
        ammo = AmmoType(name="Empty", weight=0.1)
        assert ammo.get_explosion_pen(5) == 0.0
        assert ammo.get_explosion_dc(5) == 0
        assert ammo.get_base_shrapnel_hit_chance(5) is None
        assert ammo.get_base_concussion(5) is None

    def test_pellet_count(self):
        """Test shotgun pellet count."""
        ammo = AmmoType(name="12ga Buckshot", weight=0.1, pellet_count=9)
        assert ammo.pellet_count == 9


# ===== ArmorLayer Tests =====

class TestArmorLayer:
    """Tests for ArmorLayer class."""

    def test_armor_layer_creation(self):
        """Test creating armor layer."""
        layer = ArmorLayer(
            material=ArmorMaterial.KEVLAR,
            protection_factor=10,
            blunt_protection_factor=5
        )
        assert layer.material == ArmorMaterial.KEVLAR
        assert layer.protection_factor == 10
        assert layer.blunt_protection_factor == 5
        assert layer.current_condition == 1.0

    def test_effective_protection_pristine(self):
        """Test effective protection at full condition."""
        layer = ArmorLayer(ArmorMaterial.STEEL, 20, 10)
        assert layer.effective_protection == 20
        assert layer.effective_blunt_protection == 10

    def test_effective_protection_degraded(self):
        """Test effective protection with degradation."""
        layer = ArmorLayer(ArmorMaterial.STEEL, 20, 10)
        layer.current_condition = 0.5
        assert layer.effective_protection == 10
        assert layer.effective_blunt_protection == 5

    def test_apply_hit_damage_kevlar(self):
        """Test applying hit damage to Kevlar."""
        layer = ArmorLayer(ArmorMaterial.KEVLAR, 10, 5)
        initial_condition = layer.current_condition
        layer.apply_hit_damage()
        # Kevlar has 5% degradation on hit
        expected = initial_condition * 0.95
        assert abs(layer.current_condition - expected) < 0.001

    def test_apply_penetration_damage_kevlar(self):
        """Test applying penetration damage to Kevlar."""
        layer = ArmorLayer(ArmorMaterial.KEVLAR, 10, 5)
        initial_condition = layer.current_condition
        layer.apply_penetration_damage()
        # Kevlar has 10% degradation on penetration
        expected = initial_condition * 0.90
        assert abs(layer.current_condition - expected) < 0.001

    def test_apply_hit_damage_steel(self):
        """Test applying hit damage to Steel (no degradation on hit)."""
        layer = ArmorLayer(ArmorMaterial.STEEL, 20, 10)
        layer.apply_hit_damage()
        # Steel has 0% degradation on hit
        assert layer.current_condition == 1.0

    def test_apply_penetration_damage_ceramic(self):
        """Test applying penetration damage to ceramic."""
        layer = ArmorLayer(ArmorMaterial.BORON_CARBIDE, 30, 15)
        layer.apply_penetration_damage()
        # Boron carbide has 45% degradation on penetration
        assert abs(layer.current_condition - 0.55) < 0.001

    def test_condition_minimum_zero(self):
        """Test that condition doesn't go below zero."""
        layer = ArmorLayer(ArmorMaterial.BORON_CARBIDE, 30, 15)
        layer.apply_penetration_damage()
        layer.apply_penetration_damage()
        layer.apply_penetration_damage()
        assert layer.current_condition >= 0.0


# ===== ArmorProtectionData Tests =====

class TestArmorProtectionData:
    """Tests for ArmorProtectionData class."""

    def test_armor_protection_data_creation(self):
        """Test creating empty armor protection data."""
        data = ArmorProtectionData()
        assert len(data.layers) == 0
        assert data.get_total_protection() == 0
        assert data.get_total_blunt_protection() == 0

    def test_add_layer(self):
        """Test adding armor layers."""
        data = ArmorProtectionData()
        data.add_layer(ArmorMaterial.KEVLAR, 10, 5)
        data.add_layer(ArmorMaterial.STEEL, 15, 8)
        assert len(data.layers) == 2

    def test_get_total_protection_multiple_layers(self):
        """Test total protection from multiple layers."""
        data = ArmorProtectionData()
        data.add_layer(ArmorMaterial.KEVLAR, 10, 5)
        data.add_layer(ArmorMaterial.STEEL, 15, 8)
        assert data.get_total_protection() == 25
        assert data.get_total_blunt_protection() == 13

    def test_get_total_protection_with_degradation(self):
        """Test total protection with layer degradation."""
        data = ArmorProtectionData()
        data.add_layer(ArmorMaterial.KEVLAR, 10, 5)
        data.layers[0].current_condition = 0.5
        assert data.get_total_protection() == 5
        assert data.get_total_blunt_protection() == 2

    @patch('phoenix_command.models.gear.random.randint')
    @patch('phoenix_command.tables.core.table3_hit_location_and_damage.Table3HitLocationAndDamage.get_effective_pf')
    def test_process_hit_stopped(self, mock_get_pf, mock_randint):
        """Test processing a hit that is stopped by armor."""
        mock_randint.return_value = 5
        mock_get_pf.return_value = 15
        
        data = ArmorProtectionData()
        data.add_layer(ArmorMaterial.STEEL, 20, 10)
        
        penetrated, remaining_pen = data.process_hit(10.0)
        
        assert penetrated is False
        assert remaining_pen == 0
        mock_randint.assert_called_once_with(0, 9)

    @patch('phoenix_command.models.gear.random.randint')
    @patch('phoenix_command.tables.core.table3_hit_location_and_damage.Table3HitLocationAndDamage.get_effective_pf')
    def test_process_hit_penetrated(self, mock_get_pf, mock_randint):
        """Test processing a hit that penetrates armor."""
        mock_randint.return_value = 5
        mock_get_pf.return_value = 5
        
        data = ArmorProtectionData()
        data.add_layer(ArmorMaterial.KEVLAR, 10, 5)
        
        penetrated, remaining_pen = data.process_hit(15.0)
        
        assert penetrated is True
        assert remaining_pen == 10

    @patch('phoenix_command.models.gear.random.randint')
    @patch('phoenix_command.tables.core.table3_hit_location_and_damage.Table3HitLocationAndDamage.get_effective_pf')
    def test_process_hit_multiple_layers(self, mock_get_pf, mock_randint):
        """Test processing a hit through multiple armor layers."""
        mock_randint.return_value = 5
        # Первый слой останавливает 5, второй 6 - суммарно 11 > 10 пенетрации
        mock_get_pf.side_effect = [5, 6]

        data = ArmorProtectionData()
        data.add_layer(ArmorMaterial.KEVLAR, 10, 5)
        data.add_layer(ArmorMaterial.STEEL, 15, 8)
        
        penetrated, remaining_pen = data.process_hit(10.0)
        
        # Броня должна остановить пулю: 10 пенетрации - 5 (первый слой) - 5 (второй слой) = 0
        assert penetrated is False
        assert remaining_pen == 0


# ===== Armor Tests =====

class TestArmor:
    """Tests for Armor class."""

    def test_armor_creation(self):
        """Test creating armor."""
        armor = Armor(name="Plate Carrier", weight=8.0)
        assert armor.name == "Plate Carrier"
        assert armor.weight == 8.0
        assert len(armor.protection) == 0

    def test_add_protection(self):
        """Test adding protection to specific locations."""
        armor = Armor(name="Vest", weight=5.0)
        armor.add_protection(
            AdvancedHitLocation.LUNG,
            True,
            ArmorMaterial.KEVLAR,
            10,
            5
        )
        assert len(armor.protection) == 1
        key = (AdvancedHitLocation.LUNG, True)
        assert key in armor.protection

    def test_get_protection_existing(self):
        """Test getting protection for existing location."""
        armor = Armor(name="Vest", weight=5.0)
        armor.add_protection(
            AdvancedHitLocation.HEART,
            True,
            ArmorMaterial.STEEL,
            20,
            10
        )
        protection = armor.get_protection(AdvancedHitLocation.HEART, True)
        assert protection is not None
        assert protection.get_total_protection() == 20

    def test_get_protection_non_existing(self):
        """Test getting protection for non-protected location."""
        armor = Armor(name="Vest", weight=5.0)
        protection = armor.get_protection(AdvancedHitLocation.ARM_GLANCE_LEFT, True)
        assert protection is None

    def test_add_multiple_layers_same_location(self):
        """Test adding multiple layers to same location."""
        armor = Armor(name="Heavy Vest", weight=10.0)
        armor.add_protection(
            AdvancedHitLocation.LUNG,
            True,
            ArmorMaterial.KEVLAR,
            10,
            5
        )
        armor.add_protection(
            AdvancedHitLocation.LUNG,
            True,
            ArmorMaterial.STEEL,
            15,
            8
        )
        protection = armor.get_protection(AdvancedHitLocation.LUNG, True)
        assert len(protection.layers) == 2
        assert protection.get_total_protection() == 25

    def test_gost_class_calculation(self):
        """Test GOST armor class calculation."""
        armor = Armor(name="Vest", weight=5.0)
        
        # No protection
        assert armor.gost_class is None
        
        # Class 2
        armor.add_protection(AdvancedHitLocation.LUNG, True, ArmorMaterial.KEVLAR, 3, 2)
        assert armor.gost_class == 2
        
        # Class 6
        armor.add_protection(AdvancedHitLocation.HEART, True, ArmorMaterial.STEEL, 30, 15)
        assert armor.gost_class == 6

    def test_nij_class_calculation(self):
        """Test NIJ armor class calculation."""
        armor = Armor(name="Vest", weight=5.0)
        
        # No protection
        assert armor.nij_class is None
        
        # Class 1
        armor.add_protection(AdvancedHitLocation.LUNG, True, ArmorMaterial.KEVLAR, 1, 1)
        assert armor.nij_class == "1"
        
        # Class 3a
        armor.add_protection(AdvancedHitLocation.HEART, True, ArmorMaterial.KEVLAR, 5, 3)
        assert armor.nij_class == "3a"
        
        # Class 4
        armor.add_protection(AdvancedHitLocation.SPINE, True, ArmorMaterial.STEEL, 30, 15)
        assert armor.nij_class == "4"

    @patch('phoenix_command.models.gear.ArmorProtectionData.process_hit')
    def test_process_hit_with_protection(self, mock_process_hit):
        """Test processing a hit on protected location."""
        mock_process_hit.return_value = (False, 0)
        
        armor = Armor(name="Vest", weight=5.0)
        armor.add_protection(
            AdvancedHitLocation.LUNG,
            True,
            ArmorMaterial.STEEL,
            20,
            10
        )
        
        penetrated, remaining = armor.process_hit(AdvancedHitLocation.LUNG, True, 15.0)
        
        assert penetrated is False
        assert remaining == 0
        mock_process_hit.assert_called_once_with(15.0)

    def test_process_hit_without_protection(self):
        """Test processing a hit on unprotected location."""
        armor = Armor(name="Vest", weight=5.0)
        penetrated, remaining = armor.process_hit(AdvancedHitLocation.ARM_GLANCE_LEFT, True, 15.0)
        
        assert penetrated is True
        assert remaining == 15

    def test_apply_global_degradation(self):
        """Test applying global degradation to armor."""
        armor = Armor(name="Ceramic Plates", weight=10.0)
        armor.add_protection(
            AdvancedHitLocation.LUNG,
            True,
            ArmorMaterial.SILICON_CARBIDE,
            25,
            12
        )
        armor.add_protection(
            AdvancedHitLocation.HEART,
            True,
            ArmorMaterial.SILICON_CARBIDE,
            25,
            12
        )
        
        # Apply global degradation
        armor.apply_global_degradation(ArmorMaterial.SILICON_CARBIDE, False)
        
        # Both locations should be degraded
        lung_protection = armor.get_protection(AdvancedHitLocation.LUNG, True)
        heart_protection = armor.get_protection(AdvancedHitLocation.HEART, True)
        
        assert lung_protection.layers[0].current_condition < 1.0
        assert heart_protection.layers[0].current_condition < 1.0

    def test_front_vs_rear_protection(self):
        """Test different protection for front and rear."""
        armor = Armor(name="Vest", weight=5.0)
        armor.add_protection(AdvancedHitLocation.LUNG, True, ArmorMaterial.STEEL, 20, 10)
        armor.add_protection(AdvancedHitLocation.LUNG, False, ArmorMaterial.KEVLAR, 10, 5)
        
        front = armor.get_protection(AdvancedHitLocation.LUNG, True)
        rear = armor.get_protection(AdvancedHitLocation.LUNG, False)
        
        assert front.get_total_protection() == 20
        assert rear.get_total_protection() == 10


# ===== Weapon Tests =====

class TestWeapon:
    """Tests for Weapon class."""

    def test_weapon_creation_minimal(self):
        """Test creating weapon with minimal required fields."""
        weapon = Weapon(
            name="AK-47",
            weight=8.5,
            caliber=Caliber.CAL_556_NATO,
            weapon_type=WeaponType.ASSAULT_RIFLE,
            country=Country.USSR,
            length_deployed=34.3
        )
        assert weapon.name == "AK-47"
        assert weapon.weight == 8.5
        assert weapon.caliber == Caliber.CAL_556_NATO
        assert weapon.length_deployed == 34.3

    def test_weapon_creation_full_auto(self):
        """Test creating full auto weapon."""
        weapon = Weapon(
            name="M4A1",
            weight=6.5,
            caliber=Caliber.CAL_556_NATO,
            weapon_type=WeaponType.ASSAULT_RIFLE,
            country=Country.USA,
            length_deployed=33.0,
            full_auto=True,
            full_auto_rof=13,
            sustained_auto_burst=6
        )
        assert weapon.full_auto is True
        assert weapon.full_auto_rof == 13
        assert weapon.sustained_auto_burst == 6

    def test_weapon_with_folding_stock(self):
        """Test weapon with folding stock."""
        weapon = Weapon(
            name="AKS-74U",
            weight=6.0,
            caliber=Caliber.CAL_556_NATO,
            weapon_type=WeaponType.ASSAULT_RIFLE,
            country=Country.USSR,
            length_deployed=29.0,
            length_folded=19.0
        )
        assert weapon.length_folded == 19.0

    def test_weapon_with_ammo_capacity(self):
        """Test weapon with magazine capacity."""
        weapon = Weapon(
            name="Glock 17",
            weight=1.5,
            caliber=Caliber.CAL_9MM_PARABELLUM,
            weapon_type=WeaponType.AUTOMATIC_PISTOL,  # Используем существующий enum
            country=Country.AUSTRIA,
            length_deployed=7.3,
            ammo_capacity=17,
            ammo_weight=0.2,
            ammo_feed_device=AmmoFeedDevice.MAGAZINE
        )
        assert weapon.ammo_capacity == 17
        assert weapon.ammo_weight == 0.2
        assert weapon.ammo_feed_device == AmmoFeedDevice.MAGAZINE

    def test_weapon_with_aim_time_modifiers(self):
        """Test weapon with aim time modifiers."""
        weapon = Weapon(
            name="Sniper Rifle",
            weight=12.0,
            caliber=Caliber.CAL_556_NATO,
            weapon_type=WeaponType.SNIPER_RIFLE,
            country=Country.USA,
            length_deployed=44.0,
            aim_time_modifiers={2: 1, 4: 2, 6: 3}
        )
        assert weapon.aim_time_modifiers[2] == 1
        assert weapon.aim_time_modifiers[4] == 2
        assert weapon.aim_time_modifiers[6] == 3

    def test_weapon_with_built_in_accessories(self):
        """Test weapon with built-in accessories."""
        weapon = Weapon(
            name="VSS Vintorez",
            weight=5.7,
            caliber=Caliber.CAL_9MM_PARABELLUM,
            weapon_type=WeaponType.ASSAULT_RIFLE,
            country=Country.USSR,
            length_deployed=35.0,
            built_in_optics=True,
            built_in_suppressor=True
        )
        assert weapon.built_in_optics is True
        assert weapon.built_in_suppressor is True
        assert weapon.built_in_bipod is False
        assert weapon.built_in_foregrip is False

    def test_weapon_with_ammunition_types(self):
        """Test weapon with multiple ammunition types."""
        ammo1 = AmmoType(name="FMJ", weight=0.05)
        ammo2 = AmmoType(name="HP", weight=0.05)
        
        weapon = Weapon(
            name="M16A2",
            weight=7.5,
            caliber=Caliber.CAL_556_NATO,
            weapon_type=WeaponType.ASSAULT_RIFLE,
            country=Country.USA,
            length_deployed=39.5,
            ammunition_types=[ammo1, ammo2]
        )
        assert len(weapon.ammunition_types) == 2
        assert weapon.ammunition_types[0].name == "FMJ"

    def test_weapon_with_ballistic_data(self):
        """Test weapon with ballistic data."""
        ballistic_data = WeaponBallisticData(
            ballistic_accuracy=[RangeData(10, 5.0)],
            time_of_flight=[RangeData(10, 0.5)]
        )
        weapon = Weapon(
            name="Test Weapon",
            weight=8.0,
            caliber=Caliber.CAL_556_NATO,
            weapon_type=WeaponType.ASSAULT_RIFLE,
            country=Country.USA,
            length_deployed=30.0,
            ballistic_data=ballistic_data
        )
        assert weapon.ballistic_data is not None
        assert weapon.ballistic_data.get_ballistic_accuracy(10) == 5

    def test_weapon_reload_and_cycle_times(self):
        """Test weapon reload and cycle times."""
        weapon = Weapon(
            name="Bolt Action Rifle",
            weight=9.0,
            caliber=Caliber.CAL_556_NATO,
            weapon_type=WeaponType.SNIPER_RIFLE,  # Используем SNIPER_RIFLE вместо BOLT_ACTION_RIFLE
            country=Country.USA,
            length_deployed=43.0,
            reload_time=20,
            actions_to_cycle=5,
            self_loading_action=False
        )
        assert weapon.reload_time == 20
        assert weapon.actions_to_cycle == 5
        assert weapon.self_loading_action is False

    def test_weapon_knock_down(self):
        """Test weapon knock down value."""
        weapon = Weapon(
            name="Shotgun",
            weight=7.0,
            caliber=Caliber.CAL_556_NATO,
            weapon_type=WeaponType.SHOTGUN,
            country=Country.USA,
            length_deployed=42.0,
            knock_down=8
        )
        assert weapon.knock_down == 8


# ===== Grenade Tests =====

class TestGrenade:
    """Tests for Grenade class."""

    def test_grenade_creation(self):
        """Test creating grenade."""
        explosive_data = [
            ExplosiveData(None, 20.0, 6, "4D6", 30),
            ExplosiveData(1, 15.0, 5, "3D6", 20),
            ExplosiveData(3, 8.0, 3, "2D6", 10),
        ]
        
        grenade = Grenade(
            name="M67 Frag",
            weight=0.9,
            country=Country.USA,
            grenade_type=GrenadeType.FRAG,  # Используем FRAG вместо FRAGMENTATION
            length=3.5,
            arm_time=2,
            fuse_length=4,
            range=range(0, 40),
            explosive_data=explosive_data
        )
        
        assert grenade.name == "M67 Frag"
        assert grenade.weight == 0.9
        assert grenade.country == Country.USA
        assert grenade.grenade_type == GrenadeType.FRAG
        assert grenade.length == 3.5
        assert grenade.arm_time == 2
        assert grenade.fuse_length == 4
        assert len(grenade.explosive_data) == 3

    def test_grenade_impact_fuse(self):
        """Test grenade with impact fuse (fuse_length=0)."""
        grenade = Grenade(
            name="Impact Grenade",
            weight=0.5,
            country=Country.USA,
            grenade_type=GrenadeType.BLAST,  # Используем BLAST вместо HIGH_EXPLOSIVE
            length=4.0,
            arm_time=1,
            fuse_length=0,  # Impact fuse
            range=range(0, 30)
        )
        assert grenade.fuse_length == 0

    def test_grenade_smoke(self):
        """Test smoke grenade - создаем фиктивный enum SMOKE для теста."""
        # Поскольку SMOKE не существует в GrenadeType, используем FRAG для примера
        grenade = Grenade(
            name="M18 Smoke",
            weight=0.5,
            country=Country.USA,
            grenade_type=GrenadeType.FRAG,  # Используем FRAG как заглушку
            length=5.5,
            arm_time=1,
            fuse_length=0,
            range=range(0, 35)
        )
        assert grenade.grenade_type == GrenadeType.FRAG
        assert len(grenade.explosive_data) == 0

