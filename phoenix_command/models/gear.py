import random
from dataclasses import dataclass, field
from typing import Optional

from phoenix_command.models.enums import AmmoFeedDevice, AdvancedHitLocation, ArmorMaterial, Caliber, WeaponType, \
    Country, GrenadeType
from phoenix_command.tables.core.table3_hit_location_and_damage import Table3HitLocationAndDamage


@dataclass
class BallisticData:
    """Ballistic characteristics at specific range."""
    range_hexes: int
    penetration: float
    damage_class: int
    beyond_max_range: bool = False
    shotgun_accuracy_level_modifier: Optional[int] = None
    base_pellet_hit_chance: Optional[str] = None
    pattern_radius: Optional[float] = None

@dataclass
class ExplosiveData:
    """Explosive characteristics at specific burst ranges."""
    range_hexes: Optional[int] #can be None if explosion is in contact with target
    shrapnel_penetration: float
    shrapnel_damage_class: int
    base_shrapnel_hit_chance: str
    base_concussion: int


@dataclass
class RangeData:
    """Data for a specific range."""
    range_hexes: int
    value: float


@dataclass
class WeaponBallisticData:
    """Complete ballistic data for a weapon at various ranges."""
    angle_of_impact: Optional[list[RangeData]] = None
    three_round_burst: Optional[list[RangeData]] = None  # 3RB - only for burst-capable weapons
    minimum_arc: Optional[list[RangeData]] = None  # MA - only for automatic weapons
    ballistic_accuracy: list[RangeData] = field(default_factory=list)  # BA - required
    time_of_flight: list[RangeData] = field(default_factory=list)  # TOF - required

    def _get_value_by_range(
            self,
            data_list: Optional[list[RangeData]],
            range_hexes: int,
            default: float | None,
    ) -> float | None:
        if not data_list:
            return default

        for i, data in enumerate(data_list):
            if range_hexes <= data.range_hexes:
                return data.value

            if i < len(data_list) - 1:
                if range_hexes < data_list[i + 1].range_hexes:
                    return data.value

        return data_list[-1].value

    def get_three_round_burst(self, range_hexes: int) -> Optional[float]:
        return self._get_value_by_range(
            self.three_round_burst,
            range_hexes,
            None,
        )

    def get_minimum_arc(self, range_hexes: int) -> Optional[float]:
        return self._get_value_by_range(
            self.minimum_arc,
            range_hexes,
            None,
        )

    def get_ballistic_accuracy(self, range_hexes: int) -> int:
        return self._get_value_by_range(
            self.ballistic_accuracy,
            range_hexes,
            0,
        ) or 0

    def get_time_of_flight(self, range_hexes: int) -> float:
        return self._get_value_by_range(
            self.time_of_flight,
            range_hexes,
            0.0,
        ) or 0.0

@dataclass
class Gear:
    """Base class for all equipment items."""
    name: str
    weight: float  # in pounds
    description: str = field(default="", kw_only=True)


@dataclass
class AmmoType(Gear):
    """Ammunition type with name and ballistic characteristics at various ranges."""
    ballistic_data: list[BallisticData] = field(default_factory=list)
    explosive_data: list[ExplosiveData] = field(default_factory=list)
    pellet_count: Optional[int] = None

    def get_pen(self, range_hexes: int) -> float:
        """Get penetration value for a given range."""
        for i, data in enumerate(self.ballistic_data):
            if range_hexes <= data.range_hexes:
                return data.penetration
            if i < len(self.ballistic_data) - 1:
                if range_hexes < self.ballistic_data[i + 1].range_hexes:
                    return data.penetration
        return self.ballistic_data[-1].penetration if self.ballistic_data else 0.0

    def get_dc(self, range_hexes: int) -> int:
        """Get damage class for a given range."""
        for i, data in enumerate(self.ballistic_data):
            if range_hexes <= data.range_hexes:
                return data.damage_class
            if i < len(self.ballistic_data) - 1:
                if range_hexes < self.ballistic_data[i + 1].range_hexes:
                    return data.damage_class
        return self.ballistic_data[-1].damage_class if self.ballistic_data else 0

    def get_base_shrapnel_hit_chance(self, range_hexes: int) -> Optional[str]:
        """Get base shrapnel hit chance for a given range from burst."""
        for data in self.explosive_data:
            if data.range_hexes is None or range_hexes <= data.range_hexes:
                return data.base_shrapnel_hit_chance
        return self.explosive_data[-1].base_shrapnel_hit_chance if self.explosive_data else None

    def get_explosion_pen(self, range_hexes: int) -> float:
        """Get shrapnel penetration for a given range from burst."""
        for data in self.explosive_data:
            if data.range_hexes is None or range_hexes <= data.range_hexes:
                return data.shrapnel_penetration
        return self.explosive_data[-1].shrapnel_penetration if self.explosive_data else 0.0

    def get_explosion_dc(self, range_hexes: int) -> int:
        """Get shrapnel damage class for a given range from burst."""
        for data in self.explosive_data:
            if data.range_hexes is None or range_hexes <= data.range_hexes:
                return data.shrapnel_damage_class
        return self.explosive_data[-1].shrapnel_damage_class if self.explosive_data else 0

    def get_base_concussion(self, range_hexes: int) -> Optional[int]:
        """Get base concussion damage for a given range from burst."""
        for data in self.explosive_data:
            if data.range_hexes is None or range_hexes <= data.range_hexes:
                return data.base_concussion
        return self.explosive_data[-1].base_concussion if self.explosive_data else None

@dataclass
class ArmorLayer:
    """Single layer of armor protection."""
    material: ArmorMaterial
    protection_factor: int  # Ballistic protection value
    blunt_protection_factor: int  # Protection against blunt trauma when armor stops penetration
    current_condition: float = 1.0  # 1.0 = pristine, 0.0 = destroyed

    @property
    def effective_protection(self) -> int:
        """Get current effective protection based on condition."""
        return int(self.protection_factor * self.current_condition)

    @property
    def effective_blunt_protection(self) -> int:
        """Get current effective blunt protection based on condition."""
        return int(self.blunt_protection_factor * self.current_condition)

    def apply_hit_damage(self) -> None:
        degradation_percent = self.material.degradation_on_hit / 100.0
        self.current_condition = max(0.0, self.current_condition * (1.0 - degradation_percent))

    def apply_penetration_damage(self) -> None:
        degradation_percent = self.material.degradation_on_penetration / 100.0
        self.current_condition = max(0.0, self.current_condition * (1.0 - degradation_percent))


@dataclass
class ArmorProtectionData:
    """Protection data for a specific armor location with multiple layers."""
    layers: list[ArmorLayer] = field(default_factory=list)

    def get_total_protection(self) -> int:
        """Get total protection factor from all layers."""
        return sum(layer.effective_protection for layer in self.layers)

    def get_total_blunt_protection(self) -> int:
        """Get total blunt protection factor from all layers."""
        return sum(layer.effective_blunt_protection for layer in self.layers)

    def process_hit(self, penetration: float) -> tuple[bool, int]:
        roll = random.randint(0, 9)
        remaining_pen = penetration
        
        for layer in self.layers:
            if remaining_pen <= 0:
                break
            
            base_protection = layer.effective_protection
            effective_protection = Table3HitLocationAndDamage.get_effective_pf(base_protection, roll)
            
            if remaining_pen > effective_protection:
                layer.apply_penetration_damage()
                remaining_pen -= effective_protection
            else:
                layer.apply_hit_damage()
                remaining_pen = 0
                break

        penetrated = remaining_pen > 0
        return penetrated, int(remaining_pen)

    def add_layer(
            self,
            material: ArmorMaterial,
            protection_factor: int,
            blunt_protection_factor: int
    ) -> None:
        self.layers.append(
            ArmorLayer(
                material,
                protection_factor,
                blunt_protection_factor,
            )
        )


@dataclass
class Armor(Gear):
    """Armor protection gear with location-specific protection factors."""
    protection: dict[tuple[AdvancedHitLocation, bool], ArmorProtectionData] = field(default_factory=dict)  # (HitLocation, is_front) -> protection data

    @property
    def gost_class(self) -> Optional[int]:
        """Get GOST armor class based on maximum protection."""
        max_pf = max((data.get_total_protection() for data in self.protection.values()), default=0)
        if max_pf >= 29: return 6
        if max_pf >= 19: return 5
        if max_pf >= 17: return 4
        if max_pf >= 12: return 3
        if max_pf >= 2.5: return 2
        if max_pf >= 1.1: return 1
        return None

    @property
    def nij_class(self) -> Optional[str]:
        """Get NIJ armor class based on maximum protection."""
        max_pf = max((data.get_total_protection() for data in self.protection.values()), default=0)
        if max_pf >= 27: return "4"
        if max_pf >= 17: return "3"
        if max_pf >= 4.4: return "3a"
        if max_pf >= 2.9: return "2"
        if max_pf >= 1.5: return "2a"
        if max_pf >= 0.9: return "1"
        return None

    def add_protection(
        self,
        location: AdvancedHitLocation,
        is_front: bool,
        material: ArmorMaterial,
        protection_factor: int,
        blunt_protection_factor: int
    ) -> None:
        """Add armor protection layer to a specific location."""
        key = (location, is_front)
        self.protection.setdefault(key, ArmorProtectionData()) \
            .add_layer(material, protection_factor, blunt_protection_factor)

    def get_protection(self, location: AdvancedHitLocation, is_front: bool) -> ArmorProtectionData | None:
        """Get armor protection data for a specific location and side."""
        return self.protection.get((location, is_front))

    def apply_global_degradation(self, material: ArmorMaterial, is_penetration: bool) -> None:
        for protection_data in self.protection.values():
            for layer in protection_data.layers:
                if layer.material != material:
                    continue

                if is_penetration:
                    layer.apply_penetration_damage()
                else:
                    layer.apply_hit_damage()

    def process_hit(
        self,
        location: AdvancedHitLocation,
        is_front: bool,
        penetration: float
    ) -> tuple[bool, int]:
        """Process a hit against this armor at a specific location."""
        protection_data = self.get_protection(location, is_front)
        if protection_data is None:
            return True, int(penetration)

        penetrated, remaining_pen = protection_data.process_hit(penetration)

        for layer in protection_data.layers:
            if layer.material.global_degradation:
                self.apply_global_degradation(layer.material, penetrated)
                break

        return penetrated, remaining_pen


@dataclass
class Weapon(Gear):
    """Weapon with ballistic and operational characteristics."""
    caliber: Caliber
    weapon_type: WeaponType
    country: Country
    length_deployed: float  # Overall weapon length in inches when deployed
    length_folded: Optional[float] = None  # Length with stock folded (if applicable)
    reload_time: int = 0  # in Action Counts
    actions_to_cycle: Optional[int] = None  # in Action Counts, None if no magazine
    self_loading_action: bool = False
    full_auto: bool = False
    full_auto_rof: Optional[int] = None  # rounds per half second burst
    ammo_capacity: Optional[int] = None
    ammo_weight: float = 0.0  # weight per magazine/belt/drum/round
    ammo_feed_device: AmmoFeedDevice = AmmoFeedDevice.MAGAZINE
    knock_down: int = 0
    sustained_auto_burst: Optional[int] = None
    aim_time_modifiers: dict[int, int] = field(default_factory=dict)  # Aim Time AC -> Modifier
    ammunition_types: list[AmmoType] = field(default_factory=list)  # Available ammo types
    ballistic_data: Optional[WeaponBallisticData] = None
    built_in_optics: bool = False
    built_in_bipod: bool = False
    built_in_suppressor: bool = False
    built_in_foregrip: bool = False

    def __post_init__(self) -> None:
        if self.aim_time_modifiers is None:
            self.aim_time_modifiers = {}
        if self.ammunition_types is None:
            self.ammunition_types = []

@dataclass
class Grenade(Gear):
    country: Country
    grenade_type: GrenadeType
    length: float
    arm_time: int
    fuse_length: int #0 if impact fuse
    range: range
    explosive_data: list[ExplosiveData] = field(default_factory=list)