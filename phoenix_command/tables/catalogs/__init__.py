"""Rulebook catalogs for actions, barriers, and movement."""

from phoenix_command.tables.catalogs.action_catalog import (
    ActionCatalogState,
    ActionDef,
    BUILTIN_ACTIONS,
    CustomActionDef,
)
from phoenix_command.tables.catalogs.barrier_catalog import (
    BUILTIN_BARRIERS,
    BarrierDef,
    resolve_protection_factor,
)
from phoenix_command.tables.catalogs.movement_catalog import (
    MOVEMENT_BASE,
    MOVEMENT_MODIFIERS,
    TERRAIN_PRESETS,
    TerrainPreset,
    compute_movement_cost,
)

__all__ = [
    "ActionCatalogState",
    "ActionDef",
    "BUILTIN_ACTIONS",
    "CustomActionDef",
    "BUILTIN_BARRIERS",
    "BarrierDef",
    "resolve_protection_factor",
    "MOVEMENT_BASE",
    "MOVEMENT_MODIFIERS",
    "TERRAIN_PRESETS",
    "TerrainPreset",
    "compute_movement_cost",
]
