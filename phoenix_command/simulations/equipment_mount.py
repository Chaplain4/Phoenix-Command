"""Table 7B Equipment In/Out side effects on runtime flags / character gear."""

from __future__ import annotations

from phoenix_command.models.character import Character
from phoenix_command.models.gear import Armor, Weapon
from phoenix_command.session.domains.impulse_combat_state import TokenCombatRuntime

# action_id -> (flag_key, mounting True=in)
EQUIP_ACTIONS: dict[str, tuple[str, bool]] = {
    "backpack_in": ("backpack", True),
    "backpack_out": ("backpack", False),
    "bandolier_in": ("bandolier", True),
    "bandolier_out": ("bandolier", False),
    "bayonet_scabbard_in": ("bayonet_scabbard", True),
    "bayonet_scabbard_out": ("bayonet_scabbard", False),
    "bayonet_weapon": ("bayonet_weapon", True),
    "bipod_in": ("bipod", True),
    "bipod_out": ("bipod", False),
    "body_armor_in": ("body_armor", True),
    "body_armor_out": ("body_armor", False),
    "climbing_harness_in": ("climbing_harness", True),
    "climbing_harness_out": ("climbing_harness", False),
    "folding_stock_in": ("folding_stock", True),
    "folding_stock_out": ("folding_stock", False),
    "gas_mask_in": ("gas_mask", True),
    "gas_mask_out": ("gas_mask", False),
    "scope_in": ("scope", True),
    "scope_out": ("scope", False),
    "parachute_in": ("parachute", True),
    "parachute_out": ("parachute", False),
    "pistol_stock_in": ("pistol_stock", True),
    "pistol_stock_out": ("pistol_stock", False),
    "silencer_in": ("silencer", True),
    "silencer_out": ("silencer", False),
    "slung_weapon_in": ("slung_weapon", True),
    "slung_weapon_out": ("slung_weapon", False),
    "tripod_in": ("tripod", True),
    "tripod_out": ("tripod", False),
}


def apply_equipment_action(rt: TokenCombatRuntime, action_id: str) -> str:
    """Toggle equipment flag; return status message."""
    spec = EQUIP_ACTIONS.get(action_id)
    if not spec:
        return f"Unknown equipment action {action_id}"
    key, mounting = spec
    rt.equipment_flags[key] = mounting
    if key == "bipod" and mounting:
        rt.braced = True
    if key == "bipod" and not mounting:
        rt.braced = False
    verb = "donned" if mounting else "doffed"
    return f"Equipment {key} {verb}"


def has_relevant_gear(char: Character | None, flag_key: str) -> bool:
    """Heuristic: show In/Out when character has any matching gear type."""
    if not char:
        return False
    if flag_key == "body_armor":
        return any(isinstance(i, Armor) for i in char.equipment)
    if flag_key in ("scope", "silencer", "bipod", "folding_stock", "pistol_stock", "tripod"):
        return any(isinstance(i, Weapon) for i in char.equipment)
    if flag_key == "slung_weapon":
        return any(isinstance(i, Weapon) for i in char.equipment)
    # Cosmetic / general: always offer if character exists
    return True


def detailed_equipment_actions(char: Character | None, rt: TokenCombatRuntime) -> list[tuple[str, str, float]]:
    """Return (action_id, label, cost) for equipment matching gear + current flags."""
    from phoenix_command.tables.catalogs.action_catalog import BUILTIN_ACTIONS

    out: list[tuple[str, str, float]] = []
    for action_id, (flag_key, mounting) in EQUIP_ACTIONS.items():
        if not has_relevant_gear(char, flag_key):
            continue
        currently = bool(rt.equipment_flags.get(flag_key, False))
        # Offer "in" when not mounted, "out" when mounted (bayonet_weapon is in-only)
        if action_id == "bayonet_weapon":
            if currently:
                continue
        elif mounting and currently:
            continue
        elif not mounting and not currently:
            continue
        ad = BUILTIN_ACTIONS.get(action_id)
        if not ad:
            continue
        cost = float(ad.cost) if isinstance(ad.cost, (int, float)) else 0.0
        out.append((action_id, f"[7B] {ad.name}", cost))
    return out
