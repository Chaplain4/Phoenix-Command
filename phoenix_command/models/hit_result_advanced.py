from dataclasses import dataclass, field
from typing import List

from phoenix_command.models.enums import AdvancedHitLocation


@dataclass
class DamageResult:
    location: AdvancedHitLocation
    damage: int = 0
    shock: int = 0
    excess_epen: float = 0.0
    is_disabled: bool = False
    pierced_organs: List[str] = field(default_factory=list)
