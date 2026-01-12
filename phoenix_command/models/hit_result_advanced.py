from dataclasses import dataclass, field
from typing import List, Optional

from phoenix_command.models.enums import AdvancedHitLocation, ShooterStance, VisibilityModifier4C, TargetOrientation, IncapacitationEffect
from phoenix_command.models.recovery import Recovery


@dataclass
class DamageResult:
    location: AdvancedHitLocation
    damage: int = 0
    shock: int = 0
    excess_epen: float = 0.0
    is_disabled: bool = False
    weapon_damaged: bool = False
    pierced_organs: List[str] = field(default_factory=list)


@dataclass
class ShotParameters:
    """Parameters for a single shot."""
    aim_time_ac: int
    stance: ShooterStance
    visibility: VisibilityModifier4C
    target_orientation: TargetOrientation = TargetOrientation.FRONT_REAR
    shooter_speed_hex_per_impulse: float = 0.0
    target_speed_hex_per_impulse: float = 0.0
    reflexive_duck_shooter: bool = False
    reflexive_duck_target: bool = False


@dataclass
class ShotResult:
    """Result of a shot."""
    hit: bool
    eal: int
    odds: int
    roll: int
    damage_result: Optional[DamageResult] = None
    incapacitation_effect: Optional[IncapacitationEffect] = None
    recovery: Optional[Recovery] = None
    incapacitation_time_phases: Optional[int] = None
