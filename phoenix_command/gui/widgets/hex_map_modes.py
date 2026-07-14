"""Editor modes and shared hex-map editor constants."""

from __future__ import annotations

from enum import Enum

ZOOM_MIN = 0.2
ZOOM_MAX = 5.0
ZOOM_STEP = 1.15
TERRAIN_ALPHA = 120
OBSTACLE_ALPHA = 140
HEX_WALL_ALPHA = 160
ANNOTATION_BRUSH_SIZE = 8


class EditorCategory(str, Enum):
    MAP = "map"
    TERRAIN = "terrain"
    OBJECTS = "objects"
    TOKENS = "tokens"


class EditMode(str, Enum):
    SELECT = "select"
    TERRAIN = "terrain"
    OBSTACLE = "obstacle"
    WALL = "wall"
    WINDOW = "window"
    DOOR = "door"
    TOKEN = "token"
    STAIR = "stair"
    RULER = "ruler"
    ERASER = "eraser"
    CONDITION = "condition"
    ANNOTATE_BRUSH = "annotate_brush"
    ANNOTATE_ERASER = "annotate_eraser"


CATEGORY_MODES: dict[EditorCategory, list[EditMode]] = {
    EditorCategory.MAP: [EditMode.ANNOTATE_BRUSH, EditMode.ANNOTATE_ERASER],
    EditorCategory.TERRAIN: [EditMode.TERRAIN],
    EditorCategory.OBJECTS: [
        EditMode.OBSTACLE,
        EditMode.WALL,
        EditMode.WINDOW,
        EditMode.DOOR,
        EditMode.CONDITION,
        EditMode.STAIR,
        EditMode.RULER,
        EditMode.ERASER,
    ],
    EditorCategory.TOKENS: [EditMode.SELECT, EditMode.TOKEN],
}

SIDE_COLORS = {
    "alpha": "#4a90e2",
    "bravo": "#e24a4a",
    "charlie": "#4ae24a",
    "delta": "#e2c44a",
}


