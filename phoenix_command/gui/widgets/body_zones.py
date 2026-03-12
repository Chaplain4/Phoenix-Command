"""Body zone definitions mapping AdvancedHitLocation to visual polygons."""

from dataclasses import dataclass
from typing import Optional
from phoenix_command.models.enums import AdvancedHitLocation


@dataclass
class BodyZone:
    """A visual body zone with polygon coordinates and associated hit locations."""
    name: str
    locations: list[AdvancedHitLocation]
    # Polygon points as (x, y) in normalized 0.0-1.0 coordinates
    front_polygon: list[tuple[float, float]]
    rear_polygon: list[tuple[float, float]]  # rear view polygon
    side: Optional[str] = None  # "left", "right", or None for center


# ── Standing body proportions (normalized 0.0–1.0) ──────────────────────
# Canvas: width=1.0, height=1.0. Body centered at x≈0.5.
# Approximate anatomy from top to bottom.

# Helper: mirror polygon left↔right around x=0.5
def _mirror_x(poly: list[tuple[float, float]]) -> list[tuple[float, float]]:
    return [(1.0 - x, y) for x, y in poly]


# ────────── HEAD ──────────
HEAD_TOP_POLY = [(0.42, 0.0), (0.58, 0.0), (0.60, 0.04), (0.60, 0.06),
                 (0.40, 0.06), (0.40, 0.04)]

FOREHEAD_POLY = [(0.40, 0.06), (0.60, 0.06), (0.60, 0.08), (0.40, 0.08)]

EYE_NOSE_POLY = [(0.40, 0.08), (0.60, 0.08), (0.60, 0.10), (0.40, 0.10)]

MOUTH_POLY = [(0.41, 0.10), (0.59, 0.10), (0.59, 0.12), (0.41, 0.12)]

NECK_POLY = [(0.44, 0.12), (0.56, 0.12), (0.56, 0.16), (0.44, 0.16)]

# ────────── SHOULDERS ──────────
SHOULDER_LEFT_POLY = [(0.28, 0.16), (0.44, 0.16), (0.44, 0.20), (0.30, 0.20)]
SHOULDER_RIGHT_POLY = _mirror_x(SHOULDER_LEFT_POLY)

# ────────── UPPER ARMS ──────────
ARM_UPPER_LEFT_POLY = [(0.22, 0.20), (0.30, 0.20), (0.30, 0.32), (0.24, 0.32)]
ARM_UPPER_RIGHT_POLY = _mirror_x(ARM_UPPER_LEFT_POLY)

# ────────── ELBOWS ──────────
ELBOW_LEFT_POLY = [(0.22, 0.32), (0.30, 0.32), (0.30, 0.35), (0.22, 0.35)]
ELBOW_RIGHT_POLY = _mirror_x(ELBOW_LEFT_POLY)

# ────────── FOREARMS ──────────
FOREARM_LEFT_POLY = [(0.20, 0.35), (0.28, 0.35), (0.28, 0.45), (0.22, 0.45)]
FOREARM_RIGHT_POLY = _mirror_x(FOREARM_LEFT_POLY)

# ────────── HANDS ──────────
HAND_LEFT_POLY = [(0.19, 0.45), (0.27, 0.45), (0.27, 0.50), (0.19, 0.50)]
HAND_RIGHT_POLY = _mirror_x(HAND_LEFT_POLY)

# ────────── TORSO ──────────
CHEST_POLY = [(0.38, 0.16), (0.62, 0.16), (0.62, 0.28), (0.38, 0.28)]

BASE_OF_NECK_POLY = [(0.44, 0.15), (0.56, 0.15), (0.56, 0.18), (0.44, 0.18)]

HEART_POLY = [(0.48, 0.22), (0.56, 0.22), (0.56, 0.27), (0.48, 0.27)]

LUNG_POLY = [(0.38, 0.20), (0.48, 0.20), (0.48, 0.28), (0.38, 0.28)]

LIVER_POLY = [(0.52, 0.28), (0.62, 0.28), (0.62, 0.34), (0.52, 0.34)]

STOMACH_POLY = [(0.38, 0.28), (0.52, 0.28), (0.52, 0.36), (0.38, 0.36)]

INTESTINES_POLY = [(0.38, 0.36), (0.62, 0.36), (0.62, 0.42), (0.38, 0.42)]

SPINE_POLY = [(0.47, 0.16), (0.53, 0.16), (0.53, 0.42), (0.47, 0.42)]

PELVIS_POLY = [(0.36, 0.42), (0.64, 0.42), (0.64, 0.48), (0.36, 0.48)]

# ────────── HIP ──────────
HIP_LEFT_POLY = [(0.36, 0.46), (0.44, 0.46), (0.44, 0.50), (0.36, 0.50)]
HIP_RIGHT_POLY = _mirror_x(HIP_LEFT_POLY)

# ────────── THIGHS ──────────
THIGH_LEFT_POLY = [(0.34, 0.50), (0.44, 0.50), (0.44, 0.65), (0.36, 0.65)]
THIGH_RIGHT_POLY = _mirror_x(THIGH_LEFT_POLY)

# ────────── KNEES ──────────
KNEE_LEFT_POLY = [(0.35, 0.65), (0.43, 0.65), (0.43, 0.69), (0.35, 0.69)]
KNEE_RIGHT_POLY = _mirror_x(KNEE_LEFT_POLY)

# ────────── SHINS ──────────
SHIN_LEFT_POLY = [(0.36, 0.69), (0.42, 0.69), (0.42, 0.85), (0.36, 0.85)]
SHIN_RIGHT_POLY = _mirror_x(SHIN_LEFT_POLY)

# ────────── FEET ──────────
FOOT_LEFT_POLY = [(0.33, 0.85), (0.43, 0.85), (0.43, 0.92), (0.33, 0.92)]
FOOT_RIGHT_POLY = _mirror_x(FOOT_LEFT_POLY)


# ────────── REAR POLYGONS (same shape, different overlay context) ──────
# For rear view, left and right swap visually (mirror of person facing away)
# We use the same polygons but swap left/right semantically.

# ═══════════════════════════════════════════════════════════════════════
# Zone definitions
# ═══════════════════════════════════════════════════════════════════════

BODY_ZONES: list[BodyZone] = [
    # ── HEAD ──
    BodyZone(
        name="Head (Skull/Glance)",
        locations=[
            AdvancedHitLocation.HEAD_GLANCE,
            AdvancedHitLocation.SKULL_SIDE,
        ],
        front_polygon=HEAD_TOP_POLY,
        rear_polygon=HEAD_TOP_POLY,
    ),
    BodyZone(
        name="Forehead",
        locations=[
            AdvancedHitLocation.FOREHEAD,
            AdvancedHitLocation.FOREHEAD_SIDE,
        ],
        front_polygon=FOREHEAD_POLY,
        rear_polygon=FOREHEAD_POLY,
    ),
    BodyZone(
        name="Eye / Nose",
        locations=[
            AdvancedHitLocation.EYE_NOSE,
            AdvancedHitLocation.EYE_SIDE,
        ],
        front_polygon=EYE_NOSE_POLY,
        rear_polygon=EYE_NOSE_POLY,
    ),
    BodyZone(
        name="Mouth / Jaw",
        locations=[
            AdvancedHitLocation.MOUTH,
            AdvancedHitLocation.JAW_SIDE,
        ],
        front_polygon=MOUTH_POLY,
        rear_polygon=MOUTH_POLY,
    ),
    BodyZone(
        name="Neck",
        locations=[
            AdvancedHitLocation.NECK_FLESH,
            AdvancedHitLocation.NECK_THROAT,
            AdvancedHitLocation.BASE_OF_SKULL_SIDE,
            AdvancedHitLocation.NECK_THROAT_SIDE,
            AdvancedHitLocation.NECK_SPINE_SIDE,
        ],
        front_polygon=NECK_POLY,
        rear_polygon=NECK_POLY,
    ),

    # ── SHOULDERS ──
    BodyZone(
        name="Shoulder (Left)",
        locations=[
            AdvancedHitLocation.SHOULDER_GLANCE_LEFT,
            AdvancedHitLocation.SHOULDER_SOCKET_LEFT,
            AdvancedHitLocation.SHOULDER_LEFT,
            AdvancedHitLocation.SHOULDER_SOCKET_LUNG_SIDE,
            AdvancedHitLocation.SHOULDER_SOCKET_SPINE_SIDE,
        ],
        front_polygon=SHOULDER_LEFT_POLY,
        rear_polygon=SHOULDER_RIGHT_POLY,  # mirrored in rear view
        side="left",
    ),
    BodyZone(
        name="Shoulder (Right)",
        locations=[
            AdvancedHitLocation.SHOULDER_GLANCE_RIGHT,
            AdvancedHitLocation.SHOULDER_SOCKET_RIGHT,
            AdvancedHitLocation.SHOULDER_RIGHT,
        ],
        front_polygon=SHOULDER_RIGHT_POLY,
        rear_polygon=SHOULDER_LEFT_POLY,  # mirrored in rear view
        side="right",
    ),

    # ── UPPER ARMS ──
    BodyZone(
        name="Upper Arm (Left)",
        locations=[
            AdvancedHitLocation.ARM_GLANCE_LEFT,
            AdvancedHitLocation.ARM_GLANCE_SHOULDER_LEFT,
            AdvancedHitLocation.ARM_FLESH_LEFT,
            AdvancedHitLocation.ARM_FLESH_SHOULDER_LEFT,
            AdvancedHitLocation.ARM_BONE_LEFT,
            AdvancedHitLocation.ARM_BONE_SHOULDER_LEFT,
            AdvancedHitLocation.ARM_FLESH_OFF_SIDE,
            AdvancedHitLocation.ARM_FLESH_SHOT_SIDE,
            AdvancedHitLocation.ARM_BONE_OFF_SIDE,
            AdvancedHitLocation.ARM_BONE_SHOT_SIDE,
        ],
        front_polygon=ARM_UPPER_LEFT_POLY,
        rear_polygon=ARM_UPPER_RIGHT_POLY,
        side="left",
    ),
    BodyZone(
        name="Upper Arm (Right)",
        locations=[
            AdvancedHitLocation.ARM_GLANCE_RIGHT,
            AdvancedHitLocation.ARM_GLANCE_SHOULDER_RIGHT,
            AdvancedHitLocation.ARM_FLESH_RIGHT,
            AdvancedHitLocation.ARM_FLESH_SHOULDER_RIGHT,
            AdvancedHitLocation.ARM_BONE_RIGHT,
            AdvancedHitLocation.ARM_BONE_SHOULDER_RIGHT,
        ],
        front_polygon=ARM_UPPER_RIGHT_POLY,
        rear_polygon=ARM_UPPER_LEFT_POLY,
        side="right",
    ),

    # ── ELBOWS ──
    BodyZone(
        name="Elbow (Left)",
        locations=[
            AdvancedHitLocation.ELBOW_SHOULDER_LEFT,
            AdvancedHitLocation.ELBOW_LEFT,
        ],
        front_polygon=ELBOW_LEFT_POLY,
        rear_polygon=ELBOW_RIGHT_POLY,
        side="left",
    ),
    BodyZone(
        name="Elbow (Right)",
        locations=[
            AdvancedHitLocation.ELBOW_SHOULDER_RIGHT,
            AdvancedHitLocation.ELBOW_RIGHT,
        ],
        front_polygon=ELBOW_RIGHT_POLY,
        rear_polygon=ELBOW_LEFT_POLY,
        side="right",
    ),

    # ── FOREARMS ──
    BodyZone(
        name="Forearm (Left)",
        locations=[
            AdvancedHitLocation.FOREARM_FLESH_LUNG_LEFT,
            AdvancedHitLocation.FOREARM_FLESH_LEFT,
            AdvancedHitLocation.FOREARM_BONE_LUNG_LEFT,
            AdvancedHitLocation.FOREARM_BONE_LEFT,
        ],
        front_polygon=FOREARM_LEFT_POLY,
        rear_polygon=FOREARM_RIGHT_POLY,
        side="left",
    ),
    BodyZone(
        name="Forearm (Right)",
        locations=[
            AdvancedHitLocation.FOREARM_FLESH_LUNG_RIGHT,
            AdvancedHitLocation.FOREARM_FLESH_RIGHT,
            AdvancedHitLocation.FOREARM_BONE_LUNG_RIGHT,
            AdvancedHitLocation.FOREARM_BONE_RIGHT,
        ],
        front_polygon=FOREARM_RIGHT_POLY,
        rear_polygon=FOREARM_LEFT_POLY,
        side="right",
    ),

    # ── HANDS ──
    BodyZone(
        name="Hand (Left)",
        locations=[
            AdvancedHitLocation.HAND_BASE_OF_NECK_LEFT,
            AdvancedHitLocation.HAND_LEFT,
        ],
        front_polygon=HAND_LEFT_POLY,
        rear_polygon=HAND_RIGHT_POLY,
        side="left",
    ),
    BodyZone(
        name="Hand (Right)",
        locations=[
            AdvancedHitLocation.HAND_BASE_OF_NECK_RIGHT,
            AdvancedHitLocation.HAND_RIGHT,
            AdvancedHitLocation.HAND_WEAPON_CRITICAL,
        ],
        front_polygon=HAND_RIGHT_POLY,
        rear_polygon=HAND_LEFT_POLY,
        side="right",
    ),

    # ── TORSO ──
    BodyZone(
        name="Torso Glance",
        locations=[
            AdvancedHitLocation.TORSO_GLANCE,
            AdvancedHitLocation.WEAPON_CRITICAL,
        ],
        front_polygon=CHEST_POLY,
        rear_polygon=CHEST_POLY,
    ),
    BodyZone(
        name="Base of Neck",
        locations=[
            AdvancedHitLocation.BASE_OF_NECK,
        ],
        front_polygon=BASE_OF_NECK_POLY,
        rear_polygon=BASE_OF_NECK_POLY,
    ),
    BodyZone(
        name="Lung",
        locations=[
            AdvancedHitLocation.LUNG_RIB,
            AdvancedHitLocation.LUNG,
            AdvancedHitLocation.LUNG_SIDE,
            AdvancedHitLocation.LUNG_RIB_SIDE,
        ],
        front_polygon=LUNG_POLY,
        rear_polygon=_mirror_x(LUNG_POLY),
    ),
    BodyZone(
        name="Heart",
        locations=[
            AdvancedHitLocation.HEART,
            AdvancedHitLocation.HEART_RIB_SIDE,
            AdvancedHitLocation.HEART_SIDE,
        ],
        front_polygon=HEART_POLY,
        rear_polygon=_mirror_x(HEART_POLY),
    ),
    BodyZone(
        name="Liver",
        locations=[
            AdvancedHitLocation.LIVER_RIB,
            AdvancedHitLocation.LIVER,
            AdvancedHitLocation.LIVER_SPINE,
            AdvancedHitLocation.LIVER_KIDNEY,
        ],
        front_polygon=LIVER_POLY,
        rear_polygon=_mirror_x(LIVER_POLY),
    ),
    BodyZone(
        name="Stomach",
        locations=[
            AdvancedHitLocation.STOMACH_RIB,
            AdvancedHitLocation.STOMACH,
            AdvancedHitLocation.STOMACH_SPLEEN,
            AdvancedHitLocation.STOMACH_KIDNEY,
            AdvancedHitLocation.STOMACH_LIVER_RIB_SIDE,
            AdvancedHitLocation.STOMACH_LIVER_SIDE,
            AdvancedHitLocation.SPLEEN_LIVER_SIDE,
        ],
        front_polygon=STOMACH_POLY,
        rear_polygon=STOMACH_POLY,
    ),
    BodyZone(
        name="Intestines",
        locations=[
            AdvancedHitLocation.INTESTINES,
            AdvancedHitLocation.INTESTINES_SIDE,
            AdvancedHitLocation.INTESTINES_SPINE_SIDE,
        ],
        front_polygon=INTESTINES_POLY,
        rear_polygon=INTESTINES_POLY,
    ),
    BodyZone(
        name="Spine",
        locations=[
            AdvancedHitLocation.SPINE,
            AdvancedHitLocation.SPINE_SIDE,
            AdvancedHitLocation.KIDNEY_SPINE_SIDE,
        ],
        front_polygon=SPINE_POLY,
        rear_polygon=SPINE_POLY,
    ),
    BodyZone(
        name="Pelvis",
        locations=[
            AdvancedHitLocation.PELVIS,
            AdvancedHitLocation.PELVIS_SIDE,
        ],
        front_polygon=PELVIS_POLY,
        rear_polygon=PELVIS_POLY,
    ),

    # ── HIPS ──
    BodyZone(
        name="Hip (Left)",
        locations=[
            AdvancedHitLocation.HIP_SOCKET_LEFT,
            AdvancedHitLocation.HIP_SPINE_SIDE,
            AdvancedHitLocation.HIP_SOCKET_SIDE,
        ],
        front_polygon=HIP_LEFT_POLY,
        rear_polygon=HIP_RIGHT_POLY,
        side="left",
    ),
    BodyZone(
        name="Hip (Right)",
        locations=[
            AdvancedHitLocation.HIP_SOCKET_RIGHT,
        ],
        front_polygon=HIP_RIGHT_POLY,
        rear_polygon=HIP_LEFT_POLY,
        side="right",
    ),

    # ── THIGHS ──
    BodyZone(
        name="Thigh (Left)",
        locations=[
            AdvancedHitLocation.LEG_GLANCE_LEFT,
            AdvancedHitLocation.THIGH_FLESH_LEFT,
            AdvancedHitLocation.THIGH_BONE_LEFT,
            AdvancedHitLocation.THIGH_FLESH_THIGH_FLESH,
            AdvancedHitLocation.THIGH_FLESH_THIGH_BONE,
        ],
        front_polygon=THIGH_LEFT_POLY,
        rear_polygon=THIGH_RIGHT_POLY,
        side="left",
    ),
    BodyZone(
        name="Thigh (Right)",
        locations=[
            AdvancedHitLocation.LEG_GLANCE_RIGHT,
            AdvancedHitLocation.THIGH_FLESH_RIGHT,
            AdvancedHitLocation.THIGH_BONE_RIGHT,
        ],
        front_polygon=THIGH_RIGHT_POLY,
        rear_polygon=THIGH_LEFT_POLY,
        side="right",
    ),

    # ── KNEES ──
    BodyZone(
        name="Knee (Left)",
        locations=[
            AdvancedHitLocation.KNEE_LEFT,
        ],
        front_polygon=KNEE_LEFT_POLY,
        rear_polygon=KNEE_RIGHT_POLY,
        side="left",
    ),
    BodyZone(
        name="Knee (Right)",
        locations=[
            AdvancedHitLocation.KNEE_RIGHT,
        ],
        front_polygon=KNEE_RIGHT_POLY,
        rear_polygon=KNEE_LEFT_POLY,
        side="right",
    ),

    # ── SHINS ──
    BodyZone(
        name="Shin (Left)",
        locations=[
            AdvancedHitLocation.SHIN_FLESH_LEFT,
            AdvancedHitLocation.SHIN_BONE_LEFT,
            AdvancedHitLocation.SHIN_FLESH_SIDE_LEFT,
            AdvancedHitLocation.SHIN_BONE_SIDE_LEFT,
        ],
        front_polygon=SHIN_LEFT_POLY,
        rear_polygon=SHIN_RIGHT_POLY,
        side="left",
    ),
    BodyZone(
        name="Shin (Right)",
        locations=[
            AdvancedHitLocation.SHIN_FLESH_RIGHT,
            AdvancedHitLocation.SHIN_BONE_RIGHT,
            AdvancedHitLocation.SHIN_FLESH_SIDE_RIGHT,
            AdvancedHitLocation.SHIN_BONE_SIDE_RIGHT,
        ],
        front_polygon=SHIN_RIGHT_POLY,
        rear_polygon=SHIN_LEFT_POLY,
        side="right",
    ),

    # ── FEET ──
    BodyZone(
        name="Foot (Left)",
        locations=[
            AdvancedHitLocation.FOOT_LEFT,
        ],
        front_polygon=FOOT_LEFT_POLY,
        rear_polygon=FOOT_RIGHT_POLY,
        side="left",
    ),
    BodyZone(
        name="Foot (Right)",
        locations=[
            AdvancedHitLocation.FOOT_RIGHT,
        ],
        front_polygon=FOOT_RIGHT_POLY,
        rear_polygon=FOOT_LEFT_POLY,
        side="right",
    ),
]


def build_location_to_zone_map() -> dict[AdvancedHitLocation, BodyZone]:
    """Build a reverse map from AdvancedHitLocation to its BodyZone."""
    mapping = {}
    for zone in BODY_ZONES:
        for loc in zone.locations:
            mapping[loc] = zone
    return mapping


LOCATION_TO_ZONE: dict[AdvancedHitLocation, BodyZone] = build_location_to_zone_map()

