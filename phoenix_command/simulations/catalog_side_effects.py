"""Table 7B catalog completion side effects (detailed path)."""

from __future__ import annotations

from typing import Any, Callable

from phoenix_command.models.character import Character
from phoenix_command.models.gear import Weapon
from phoenix_command.session.domains.impulse_combat_state import TokenCombatRuntime
from phoenix_command.session.domains.map_state import MapLayer, Opening
from phoenix_command.session.domains.token_state import TokenPlacement
from phoenix_command.simulations.equipment_mount import EQUIP_ACTIONS, apply_equipment_action
from phoenix_command.simulations.hex_tactical import axial_neighbors

DRAW_ACTIONS = frozenset(
    {
        "draw_shoulder_holster",
        "draw_belt_holster",
        "draw_police_holster",
        "draw_old_west_holster",
        "draw_modern_holster",
        "grab_slung_weapon",
        "pick_up_weapon",
    }
)

RELOAD_MICRO = frozenset(
    {
        "cock_revolver_pistol",
        "take_bullet_magazine",
        "replace_bullet_magazine",
        "link_belt_ammo",
        "load_round_magazine",
        "load_charging_strip",
        "open_hinged_ammo_can",
        "open_paper_ammo_box",
        "unload_weapon",
    }
)

WINDOW_ACTIONS = frozenset(
    {
        "open_window_two_hands",
        "break_clear_glass",
        "climb_through_window",
        "get_out_trench",
    }
)


def first_pistol_name(char: Character | None) -> str | None:
    if not char:
        return None
    from phoenix_command.models.enums import WeaponType

    pistolish = {WeaponType.AUTOMATIC_PISTOL}
    for name in ("PISTOL", "REVOLVER", "MACHINE_PISTOL", "SUBMACHINE_GUN"):
        if hasattr(WeaponType, name):
            pistolish.add(getattr(WeaponType, name))
    for item in char.equipment:
        if isinstance(item, Weapon) and item.weapon_type in pistolish:
            return item.name
    for item in char.equipment:
        if isinstance(item, Weapon):
            return item.name
    return None


def apply_reload_micro(rt: TokenCombatRuntime, action_id: str) -> None:
    if action_id == "take_bullet_magazine":
        rt.mag_in_hand = True
    elif action_id == "replace_bullet_magazine":
        if rt.mag_in_hand:
            rt.weapon_cycled = True
            rt.mag_in_hand = False
    elif action_id in ("link_belt_ammo", "load_round_magazine", "load_charging_strip"):
        rt.weapon_cycled = True
        rt.mag_in_hand = False
    elif action_id in ("open_hinged_ammo_can", "open_paper_ammo_box"):
        rt.ammo_can_open = True
    elif action_id == "cock_revolver_pistol":
        rt.weapon_cycled = True
    elif action_id == "unload_weapon":
        rt.weapon_cycled = False
        rt.mag_in_hand = True


def apply_draw(
    rt: TokenCombatRuntime,
    char: Character | None,
    action_id: str,
    weapon_name: str | None = None,
) -> None:
    name = weapon_name or first_pistol_name(char)
    if name:
        rt.held_weapon_name = name
    rt.firing_stance_held = False
    rt.looking_over_cover = False
    if action_id == "pick_up_weapon" and not name and char:
        for item in char.equipment:
            if isinstance(item, Weapon):
                rt.held_weapon_name = item.name
                break


def find_adjacent_opening(
    layer: MapLayer | None,
    placement: TokenPlacement,
    kind: str,
) -> tuple[str, Opening, int, int, int] | None:
    """Return (wall_key, opening, nq, nr, edge) for adjacent closed opening of kind."""
    if not layer:
        return None
    for nq, nr, edge in axial_neighbors(placement.q, placement.r):
        key = f"{placement.q},{placement.r}:{edge}"
        wall = layer.walls.get(key)
        if not wall:
            opp = (edge + 3) % 6
            key = f"{nq},{nr}:{opp}"
            wall = layer.walls.get(key)
        if not wall:
            continue
        for opening in wall.openings:
            if opening.kind != kind:
                continue
            if kind == "window" and opening.state == "open":
                continue
            if kind == "door" and opening.state not in ("closed", "locked"):
                continue
            if kind == "window" and opening.state not in ("closed", "locked", "broken"):
                # treat missing/closed glass
                pass
            return key, opening, nq, nr, edge
    return None


def apply_window_or_trench(
    placement: TokenPlacement,
    rt: TokenCombatRuntime,
    action_id: str,
    layer: MapLayer | None,
    terrain_is_trench: Callable[[int, int], bool] | None = None,
) -> str:
    if action_id == "get_out_trench":
        # Move to first adjacent non-trench hex if possible
        if terrain_is_trench and terrain_is_trench(placement.q, placement.r):
            for nq, nr, _ in axial_neighbors(placement.q, placement.r):
                if not terrain_is_trench(nq, nr):
                    placement.q, placement.r = nq, nr
                    return f"Climbed out of trench to ({nq},{nr})"
        return "Left trench (no adjacent clear hex)"

    found = find_adjacent_opening(layer, placement, "window")
    if not found:
        return "No adjacent window"
    _key, opening, nq, nr, _edge = found
    if action_id == "open_window_two_hands":
        opening.state = "open"
        return "Window opened"
    if action_id == "break_clear_glass":
        opening.state = "open"
        return "Glass broken and cleared"
    if action_id == "climb_through_window":
        if opening.state not in ("open",):
            opening.state = "open"
        placement.q, placement.r = nq, nr
        return f"Climbed through window to ({nq},{nr})"
    return action_id
