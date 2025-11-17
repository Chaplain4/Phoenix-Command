from dataclasses import dataclass
from typing import Dict, Tuple, Optional

from phoenix_command.models.enums import MedicalAid

@dataclass
class Recovery:
    healing_time_in_days: float
    aid_data: Dict[MedicalAid, Tuple[Optional[float], Optional[int]]]
    # Tuple = (critical_time_period_hours, recovery_chance_percent)