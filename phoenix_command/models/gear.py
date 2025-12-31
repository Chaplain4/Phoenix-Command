from dataclasses import dataclass, field
from typing import Optional

from phoenix_command.models.enums import HitLocation, AmmoFeedDevice


@dataclass
class BallisticData:
    """Ballistic characteristics at specific range."""
    range_hexes: int
    penetration: float
    damage_class: int
    beyond_max_range: bool = False


@dataclass
class AmmoType:
    """Ammunition type with name and ballistic characteristics at various ranges."""
    name: str  # Full name like "5.56mm NATO FMJ" or "7.62mm AP"
    abbreviation: str  # "FMJ", "JHP", "AP", etc.
    ballistic_data: list[BallisticData] = field(default_factory=list)

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

    def get_ballistic_accuracy(self, range_hexes: int) -> float:
        """Get ballistic accuracy for a given range."""
        for i, data in enumerate(self.ballistic_accuracy):
            if range_hexes <= data.range_hexes:
                return data.value
            if i < len(self.ballistic_accuracy) - 1:
                if range_hexes < self.ballistic_accuracy[i + 1].range_hexes:
                    return data.value
        return self.ballistic_accuracy[-1].value if self.ballistic_accuracy else 0.0

    def get_time_of_flight(self, range_hexes: int) -> float:
        """Get time of flight for a given range."""
        for i, data in enumerate(self.time_of_flight):
            if range_hexes <= data.range_hexes:
                return data.value
            if i < len(self.time_of_flight) - 1:
                if range_hexes < self.time_of_flight[i + 1].range_hexes:
                    return data.value
        return self.time_of_flight[-1].value if self.time_of_flight else 0.0


@dataclass
class Gear:
    """Base class for all equipment items."""
    name: str
    weight: float  # in pounds
    description: str = field(default="", kw_only=True)


@dataclass
class Armor(Gear):
    """Armor protection gear with location-specific protection factors."""
    protection: dict[HitLocation, int] = field(default_factory=dict)  # HitLocation -> protection_factor


@dataclass
class Weapon(Gear):
    """Weapon with ballistic and operational characteristics."""
    caliber: str
    weapon_type: str  # e.g., "Assault Rifle", "Pistol"
    country: str
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

    def __post_init__(self):
        if self.aim_time_modifiers is None:
            self.aim_time_modifiers = {}
        if self.ammunition_types is None:
            self.ammunition_types = []
