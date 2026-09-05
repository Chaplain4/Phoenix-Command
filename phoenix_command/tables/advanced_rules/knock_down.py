"""§5.12 Knock Down: projectile (weapon KD × location) and explosive (BC × armor class)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from phoenix_command.models.character import Character
from phoenix_command.models.enums import AdvancedHitLocation

LocationBand = Literal["head", "body", "arm", "leg"]
ArmorClass = Literal["normal", "infantry"]

KIND_NONE = "none"
KIND_AC_1 = "ac_1"
KIND_AC_2 = "ac_2"
KIND_AC_4 = "ac_4"
KIND_OFF_FEET = "off_feet"

# Highest matching row wins. Thresholds are weapon KD (projectile) / BC (explosive).
_PROJECTILE_ROWS: dict[LocationBand, list[tuple[int, str, int, bool]]] = {
    "head": [
        (10, KIND_OFF_FEET, 0, True),
        (4, KIND_AC_4, 4, False),
        (3, KIND_AC_2, 2, False),
        (2, KIND_AC_1, 1, False),
    ],
    "body": [
        (19, KIND_OFF_FEET, 0, True),
        (17, KIND_AC_4, 4, False),
        (14, KIND_AC_2, 2, False),
        (11, KIND_AC_1, 1, False),
    ],
    "arm": [
        (16, KIND_OFF_FEET, 0, True),
        (4, KIND_AC_4, 4, False),
        (3, KIND_AC_2, 2, False),
        (2, KIND_AC_1, 1, False),
    ],
    "leg": [
        (6, KIND_OFF_FEET, 0, True),
        (5, KIND_AC_4, 4, False),
        (4, KIND_AC_2, 2, False),
        (3, KIND_AC_1, 1, False),
    ],
}

_NORMAL_INFANTRY_EXPLOSIVE = [
    (90, KIND_OFF_FEET, 0, True),
    (82, KIND_AC_4, 4, False),
    (66, KIND_AC_2, 2, False),
    (50, KIND_AC_1, 1, False),
]

_EXPLOSIVE_ROWS: dict[ArmorClass, list[tuple[int, str, int, bool]]] = {
    "normal": _NORMAL_INFANTRY_EXPLOSIVE,
    "infantry": _NORMAL_INFANTRY_EXPLOSIVE,
}

_HEAD_PREFIXES = (
    "HEAD",
    "SKULL",
    "FOREHEAD",
    "EYE",
    "MOUTH",
    "JAW",
    "NECK",
    "BASE_OF_SKULL",
    "BASE_OF_NECK",
)
_ARM_PREFIXES = ("ARM", "ELBOW", "FOREARM", "HAND")
_LEG_PREFIXES = ("LEG", "THIGH", "KNEE", "SHIN", "FOOT", "HIP")


@dataclass(frozen=True)
class KnockDownEffect:
    """One row from the Knock Down table."""

    kind: str = KIND_NONE
    ac_penalty: int = 0
    off_feet: bool = False

    def is_none(self) -> bool:
        return self.kind == KIND_NONE or (self.ac_penalty == 0 and not self.off_feet)

    def label(self) -> str:
        if self.off_feet:
            return "knocked off feet"
        if self.ac_penalty:
            return f"-{self.ac_penalty} AC"
        return "none"


NONE = KnockDownEffect()


def location_band(location: AdvancedHitLocation) -> LocationBand | None:
    """Map an advanced hit location to the projectile KD column."""
    if location in (AdvancedHitLocation.MISS, AdvancedHitLocation.WEAPON_CRITICAL):
        return None
    name = location.name
    if name.startswith(_HEAD_PREFIXES) or name in ("BASE_OF_NECK",):
        return "head"
    if name.startswith(_ARM_PREFIXES):
        return "arm"
    if name.startswith(_LEG_PREFIXES):
        return "leg"
    return "body"


def _lookup(rows: list[tuple[int, str, int, bool]], value: int) -> KnockDownEffect:
    for threshold, kind, ac, off in rows:
        if value >= threshold:
            return KnockDownEffect(kind=kind, ac_penalty=ac, off_feet=off)
    return NONE


def projectile_knock_down(kd: int, band: LocationBand | None) -> KnockDownEffect:
    if kd <= 0 or band is None:
        return NONE
    return _lookup(_PROJECTILE_ROWS[band], int(kd))


def explosive_knock_down(base_concussion: int, armor_class: ArmorClass) -> KnockDownEffect:
    if base_concussion <= 0:
        return NONE
    return _lookup(_EXPLOSIVE_ROWS[armor_class], int(base_concussion))


def location_ballistic_pf(
    character: Character,
    location: AdvancedHitLocation,
    is_front: bool = True,
) -> int:
    pf, _bpf = character.armor_protection.get((location, is_front), (0, 0))
    return int(pf)


def infantry_armor_class(
    character: Character,
    location: AdvancedHitLocation | None = None,
    is_front: bool = True,
) -> ArmorClass:
    """Infantry column if the struck location (or torso vitals for concussion) has PF > 0."""
    if location is not None and location != AdvancedHitLocation.MISS:
        if location_ballistic_pf(character, location, is_front) > 0:
            return "infantry"
        return "normal"
    from phoenix_command.item_database.armor import iotv_front_vital

    for loc in iotv_front_vital:
        if location_ballistic_pf(character, loc, True) > 0:
            return "infantry"
    return "normal"


def knock_down_for_projectile_hit(
    kd: int,
    location: AdvancedHitLocation,
) -> KnockDownEffect:
    return projectile_knock_down(kd, location_band(location))
