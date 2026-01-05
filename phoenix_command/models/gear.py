from dataclasses import dataclass, field
from typing import Optional

from phoenix_command.models.enums import AmmoFeedDevice, AdvancedHitLocation, ArmorMaterial, Caliber, WeaponType, Country


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
class AmmoType:
    """Ammunition type with name and ballistic characteristics at various ranges."""
    name: str  # Full name like "5.56mm NATO FMJ" or "7.62mm AP"
    abbreviation: str  # "FMJ", "JHP", "AP", etc.
    ballistic_data: list[BallisticData] = field(default_factory=list)
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


@dataclass
class RangeData:
    """Data for a specific range."""
    range_hexes: int
    value: float


@dataclass
class WeaponBallisticData:
    """Complete ballistic data for a weapon at various ranges."""
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

    def get_ballistic_accuracy(self, range_hexes: int) -> float:
        return self._get_value_by_range(
            self.ballistic_accuracy,
            range_hexes,
            0.0,
        ) or 0.0

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
        remaining_pen = penetration
        for layer in self.layers:
            if remaining_pen <= 0:
                break
            layer_protection = layer.effective_protection

            if remaining_pen > layer_protection:
                layer.apply_penetration_damage()
                remaining_pen -= layer_protection
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

    def add_protection(
        self,
        location: AdvancedHitLocation,
        is_front: bool,
        material: ArmorMaterial,
        protection_factor: int,
        blunt_protection_factor: int
    ) -> None:
        """
        Add armor protection layer to a specific location.

        Args:
            location: Hit location to protect
            is_front: True for front protection, False for rear
            material: Armor material
            protection_factor: Ballistic protection value
            blunt_protection_factor: Blunt trauma protection value
        """
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
        """
        Process a hit against this armor at a specific location.

        Args:
            location: Hit location
            is_front: True for front hit, False for rear
            penetration: Penetration value of the projectile

        Returns:
            tuple: (penetrated: bool, remaining_penetration: int)
        """
        protection_data = self.get_protection(location, is_front)
        if protection_data is None:
            # No armor at this location
            return True, int(penetration)

        # Process hit normally
        penetrated, remaining_pen = protection_data.process_hit(penetration)

        # Check if any layer has global degradation material
        for layer in protection_data.layers:
            if layer.material.global_degradation:
                # Apply degradation to all armor pieces with this material
                self.apply_global_degradation(layer.material, penetrated)
                break  # Only apply once per hit

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
