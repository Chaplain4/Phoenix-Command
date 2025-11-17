from dataclasses import dataclass

from phoenix_command.enums import WoundType, HitLocation


@dataclass
class HitResult:
    damage: int
    wound_type: WoundType
    hit_location: HitLocation