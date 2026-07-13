"""Impulse combat action engine: AC spending, movement, reload."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from phoenix_command.models.character import Character
from phoenix_command.models.gear import Weapon
from phoenix_command.session.domains.impulse_combat_state import (
    ImpulseCombatState,
    TokenCombatRuntime,
)
from phoenix_command.session.domains.map_state import MapLayer, MapState
from phoenix_command.session.domains.token_state import TokenPlacement, TokenState
from phoenix_command.simulations.hex_tactical import (
    classify_movement_base,
    neighbor_direction_index,
)
from phoenix_command.tables.catalogs.action_catalog import BUILTIN_ACTIONS
from phoenix_command.tables.catalogs.movement_catalog import (
    TERRAIN_PRESETS,
    compute_movement_cost,
)

# Table 7A costs are per 2 m hex; our grid is 1 m per hex.
METER_SCALE = 0.5

STANCE_MODIFIER_MAP = {
    "standing": "stance_standing",
    "kneeling": "stance_low_crouch",
    "prone": "stance_belly_crawl",
}

STANCE_ACTION_MAP = {
    "standing_to_kneeling": "kneeling",
    "standing_to_prone": "prone",
    "kneeling_to_prone": "prone",
    "prone_to_kneeling": "kneeling",
    "prone_to_standing": "standing",
}


@dataclass
class ActionResult:
    """Outcome of applying a combat action."""

    success: bool
    message: str
    ac_spent: float = 0.0


class ImpulseCombatEngine:
    """Validate and apply impulse combat actions on host-authoritative state."""

    def __init__(
        self,
        impulse_combat: ImpulseCombatState,
        tokens: TokenState,
        map_state: MapState | None,
        characters: dict[str, Character],
    ) -> None:
        self.impulse_combat = impulse_combat
        self.tokens = tokens
        self.map_state = map_state
        self.characters = characters

    def get_runtime(self, token_id: str) -> TokenCombatRuntime:
        if token_id not in self.impulse_combat.token_runtime:
            self.impulse_combat.token_runtime[token_id] = TokenCombatRuntime()
        return self.impulse_combat.token_runtime[token_id]

    def ensure_runtime_for_tokens(self) -> None:
        for token_id, placement in self.tokens.placements.items():
            rt = self.get_runtime(token_id)
            if placement.character_name and rt.held_weapon_name is None:
                char = self.characters.get(placement.character_name)
                if char:
                    weapon = self._first_weapon(char)
                    if weapon:
                        rt.held_weapon_name = weapon.name

    def refill_impulse_ac(self) -> None:
        """Refill AC for all tokens at start of current impulse."""
        impulse_idx = self.impulse_combat.impulse
        for token_id, placement in self.tokens.placements.items():
            char = self.characters.get(placement.character_name or "")
            if not char:
                continue
            impulses = char.impulses
            if impulse_idx < len(impulses):
                rt = self.get_runtime(token_id)
                # Finalize aim impulse count from previous impulse before reset
                if rt.aimed_this_impulse and rt.aim_target_token_id:
                    rt.aim_impulses += 1
                rt.ac_remaining = float(impulses[impulse_idx])
                rt.aim_ac_this_impulse = 0.0
                rt.aimed_this_impulse = False
                rt.moved_this_impulse = False
                rt.hexes_moved_this_impulse = 0.0

    def advance_impulse(self) -> list:
        """Move to next impulse (host only). Returns projectiles due on the new impulse."""
        self.impulse_combat.impulse += 1
        if self.impulse_combat.impulse >= 4:
            self.impulse_combat.impulse = 0
            self.impulse_combat.phase += 1
        self.refill_impulse_ac()
        return self.pop_due_projectiles()

    def absolute_impulse_index(self) -> int:
        return (self.impulse_combat.phase - 1) * 4 + self.impulse_combat.impulse

    def pop_due_projectiles(self) -> list:
        """Return and remove projectiles due at the current phase/impulse."""
        phase = self.impulse_combat.phase
        impulse = self.impulse_combat.impulse
        due = []
        remaining = []
        for proj in self.impulse_combat.pending_projectiles:
            if proj.resolve_phase < phase or (
                proj.resolve_phase == phase and proj.resolve_impulse <= impulse
            ):
                due.append(proj)
            else:
                remaining.append(proj)
        self.impulse_combat.pending_projectiles = remaining
        return due

    def schedule_projectile(
        self,
        shooter_token_id: str,
        target_token_id: str,
        tof_impulses: int,
        shot_snapshot: dict,
    ):
        from phoenix_command.session.domains.impulse_combat_state import PendingProjectile
        import uuid

        abs_now = self.absolute_impulse_index()
        abs_resolve = abs_now + max(1, int(tof_impulses))
        resolve_phase = abs_resolve // 4 + 1
        resolve_impulse = abs_resolve % 4
        proj = PendingProjectile(
            projectile_id=str(uuid.uuid4()),
            resolve_phase=resolve_phase,
            resolve_impulse=resolve_impulse,
            shooter_token_id=shooter_token_id,
            target_token_id=target_token_id,
            shot_snapshot=shot_snapshot,
        )
        self.impulse_combat.pending_projectiles.append(proj)
        return proj

    def can_control_token(self, player_id: str, token: TokenPlacement, is_host: bool) -> bool:
        if is_host:
            return True
        return token.controlled_by == player_id

    def apply_action(
        self,
        token_id: str,
        action: str,
        args: dict[str, Any] | None = None,
        player_id: str = "host",
        is_host: bool = True,
    ) -> ActionResult:
        args = args or {}
        placement = self.tokens.placements.get(token_id)
        if not placement:
            return ActionResult(False, "Token not found")
        if self.impulse_combat.map_mode != "combat":
            return ActionResult(False, "Not in combat mode")
        if not self.can_control_token(player_id, placement, is_host):
            return ActionResult(False, "No control of this token")

        if action in ("move", "movement_while_braced"):
            return self._apply_move(
                placement,
                int(args.get("target_q", placement.q)),
                int(args.get("target_r", placement.r)),
                braced=action == "movement_while_braced",
            )
        if action == "brace_weapon":
            return self._apply_simple_action(placement, "brace_weapon", set_braced=True)
        if action == "aim":
            ac = float(args.get("ac", 1))
            target_id = args.get("target_token_id")
            return self._apply_aim(placement, ac, target_id)
        if action == "reload":
            return self._apply_reload(placement)
        if action == "cycle":
            return self._apply_cycle(placement)
        if action == "select_weapon":
            return self._apply_select_weapon(placement, args.get("weapon_name", ""))
        if action == "set_fire_mode":
            return self._apply_set_fire_mode(placement, args.get("fire_mode", "single"))
        if action == "custom_action":
            return self._apply_custom_action(placement, float(args.get("ac", 1)), str(args.get("label", "Custom")))
        if action == "skip_impulse":
            return self._apply_skip(placement)
        if action in STANCE_ACTION_MAP:
            return self._apply_stance_change(placement, action)
        if action in BUILTIN_ACTIONS:
            return self._apply_catalog_action(placement, action)
        return ActionResult(False, f"Unknown action: {action}")

    def _apply_catalog_action(self, placement: TokenPlacement, action_id: str) -> ActionResult:
        action_def = BUILTIN_ACTIONS.get(action_id)
        if not action_def:
            return ActionResult(False, "Unknown action")
        cost_raw = action_def.cost
        if cost_raw == "RT":
            char = self.characters.get(placement.character_name or "")
            weapon = self._held_weapon(char, self.get_runtime(placement.token_id))
            if not weapon:
                return ActionResult(False, "No weapon for RT action")
            cost = float(weapon.reload_time)
        else:
            cost = float(cost_raw)
        rt = self.get_runtime(placement.token_id)
        if rt.ac_remaining < cost:
            return ActionResult(False, f"Need {cost} AC, have {rt.ac_remaining:.1f}")
        rt.ac_remaining -= cost
        if action_id == "brace_weapon":
            rt.braced = True
        return ActionResult(True, f"{action_def.name} ({cost} AC)", cost)

    def _apply_simple_action(
        self,
        placement: TokenPlacement,
        action_id: str,
        set_braced: bool = False,
    ) -> ActionResult:
        result = self._apply_catalog_action(placement, action_id)
        if result.success and set_braced:
            self.get_runtime(placement.token_id).braced = True
        return result

    def _apply_stance_change(self, placement: TokenPlacement, action_id: str) -> ActionResult:
        result = self._apply_catalog_action(placement, action_id)
        if result.success:
            rt = self.get_runtime(placement.token_id)
            rt.stance = STANCE_ACTION_MAP[action_id]
            rt.braced = False
        return result

    def _apply_aim(
        self,
        placement: TokenPlacement,
        ac: float,
        target_token_id: str | None = None,
    ) -> ActionResult:
        rt = self.get_runtime(placement.token_id)
        char = self.characters.get(placement.character_name or "")
        if not char:
            return ActionResult(False, "Token has no character")
        if target_token_id and target_token_id != rt.aim_target_token_id:
            rt.aim_target_token_id = target_token_id
            rt.aim_ac_accumulated = 0.0
            rt.aim_impulses = 0
        if rt.moved_this_impulse:
            max_ac = float(char.impulses[self.impulse_combat.impulse])
            if rt.aim_ac_this_impulse + ac > max_ac:
                allowed = max(0.0, max_ac - rt.aim_ac_this_impulse)
                if allowed <= 0:
                    return ActionResult(False, "Cannot aim more than 1 impulse AC while moving")
                ac = allowed
        if rt.ac_remaining < ac:
            return ActionResult(False, f"Need {ac} AC, have {rt.ac_remaining:.1f}")
        rt.ac_remaining -= ac
        rt.aim_ac_this_impulse += ac
        rt.aim_ac_accumulated += ac
        rt.aimed_this_impulse = True
        return ActionResult(True, f"Aim {ac} AC", ac)

    def _apply_select_weapon(self, placement: TokenPlacement, weapon_name: str) -> ActionResult:
        char = self.characters.get(placement.character_name or "")
        if not char:
            return ActionResult(False, "No character")
        found = None
        for item in char.equipment:
            if isinstance(item, Weapon) and item.name == weapon_name:
                found = item
                break
        if not found:
            return ActionResult(False, f"Weapon not found: {weapon_name}")
        rt = self.get_runtime(placement.token_id)
        rt.held_weapon_name = found.name
        rt.weapon_cycled = found.actions_to_cycle is None
        rt.fire_mode = "single"
        return ActionResult(True, f"Selected {found.name}")

    def _apply_set_fire_mode(self, placement: TokenPlacement, mode: str) -> ActionResult:
        if mode not in ("single", "3rb", "auto"):
            return ActionResult(False, f"Invalid fire mode: {mode}")
        rt = self.get_runtime(placement.token_id)
        char = self.characters.get(placement.character_name or "")
        weapon = self._held_weapon(char, rt)
        if mode == "3rb" and weapon and (
            not weapon.ballistic_data or not weapon.ballistic_data.three_round_burst
        ):
            return ActionResult(False, "Weapon has no 3RB")
        if mode == "auto" and weapon and not weapon.full_auto:
            return ActionResult(False, "Weapon is not full-auto")
        rt.fire_mode = mode
        return ActionResult(True, f"Fire mode: {mode}")

    def _apply_custom_action(
        self, placement: TokenPlacement, ac: float, label: str
    ) -> ActionResult:
        rt = self.get_runtime(placement.token_id)
        ac = max(0.0, ac)
        if ac <= 0:
            return ActionResult(False, "Custom action needs AC > 0")
        spend = min(ac, rt.ac_remaining)
        if spend <= 0:
            return ActionResult(False, "No AC remaining")
        rt.ac_remaining -= spend
        return ActionResult(True, f"{label} ({spend} AC)", spend)

    def _apply_skip(self, placement: TokenPlacement) -> ActionResult:
        rt = self.get_runtime(placement.token_id)
        leftover = rt.ac_remaining
        rt.ac_remaining = 0.0
        return ActionResult(True, f"Skipped impulse (discarded {leftover:.1f} AC)", leftover)

    def _apply_reload(self, placement: TokenPlacement) -> ActionResult:
        char = self.characters.get(placement.character_name or "")
        rt = self.get_runtime(placement.token_id)
        weapon = self._held_weapon(char, rt)
        if not weapon:
            return ActionResult(False, "No weapon in hands")
        cost = float(weapon.reload_time)
        if rt.ac_remaining < cost:
            return ActionResult(False, f"Reload needs {cost} AC")
        rt.ac_remaining -= cost
        rt.weapon_cycled = True
        return ActionResult(True, f"Reload {weapon.name} ({cost} AC)", cost)

    def _apply_cycle(self, placement: TokenPlacement) -> ActionResult:
        char = self.characters.get(placement.character_name or "")
        rt = self.get_runtime(placement.token_id)
        weapon = self._held_weapon(char, rt)
        if not weapon or weapon.actions_to_cycle is None:
            return ActionResult(False, "Weapon does not require cycling")
        cost = float(weapon.actions_to_cycle)
        if rt.ac_remaining < cost:
            return ActionResult(False, f"Cycle needs {cost} AC")
        rt.ac_remaining -= cost
        rt.weapon_cycled = True
        return ActionResult(True, f"Cycle {weapon.name} ({cost} AC)", cost)

    def _apply_move(
        self,
        placement: TokenPlacement,
        target_q: int,
        target_r: int,
        braced: bool = False,
    ) -> ActionResult:
        rt = self.get_runtime(placement.token_id)
        dir_idx = neighbor_direction_index(placement.q, placement.r, target_q, target_r)
        if dir_idx is None:
            return ActionResult(False, "Target is not an adjacent hex")

        layer = self._get_layer(placement.layer_id)
        if layer:
            key = f"{target_q},{target_r}"
            if key in layer.obstacles and layer.obstacles[key].blocks_movement:
                return ActionResult(False, "Hex blocked by obstacle")

        base_id = classify_movement_base(placement.facing, dir_idx)
        terrain_cost, modifier_ids = self._terrain_modifiers(layer, target_q, target_r, rt.stance)
        rule_cost = compute_movement_cost(base_id, modifier_ids, terrain_cost)
        if rule_cost < 0:
            return ActionResult(False, "Impassable terrain")
        hex_cost = rule_cost * METER_SCALE
        if braced:
            hex_cost += 1.0  # brace while moving

        ac_available = rt.ac_remaining
        if ac_available <= 0 and rt.move_progress <= 0:
            return ActionResult(False, "No AC remaining")

        if rt.move_target_q != target_q or rt.move_target_r != target_r:
            if rt.move_progress > 0:
                return ActionResult(False, "Finish current move first")
            rt.move_target_q = target_q
            rt.move_target_r = target_r
            rt.move_progress = 0.0

        spend = min(ac_available, hex_cost)
        rt.ac_remaining -= spend
        if hex_cost > 0:
            rt.move_progress += spend / hex_cost
        rt.moved_this_impulse = True
        rt.hexes_moved_this_impulse += spend / hex_cost if hex_cost else 0

        if rt.move_progress >= 1.0:
            placement.q = target_q
            placement.r = target_r
            rt.move_progress = 0.0
            rt.move_target_q = None
            rt.move_target_r = None
            if braced:
                rt.braced = True
            msg = f"Moved to ({target_q},{target_r})"
        else:
            msg = f"Moving ({rt.move_progress * 100:.0f}% to {target_q},{target_r})"

        return ActionResult(True, msg, spend)

    def _terrain_modifiers(
        self,
        layer: MapLayer | None,
        q: int,
        r: int,
        stance: str,
    ) -> tuple[int | None, list[str]]:
        modifier_ids = [STANCE_MODIFIER_MAP.get(stance, "stance_standing")]
        terrain_cost: int | None = None
        if not layer:
            return terrain_cost, modifier_ids
        key = f"{q},{r}"
        tile = layer.terrain.get(key)
        if tile:
            terrain_cost = tile.movement_cost
            preset = TERRAIN_PRESETS.get(tile.terrain_type)
            if preset:
                modifier_ids.extend(preset.modifier_ids)
        return terrain_cost, modifier_ids

    def _get_layer(self, layer_id: str) -> MapLayer | None:
        if not self.map_state:
            return None
        return self.map_state.get_layer(layer_id)

    @staticmethod
    def _first_weapon(char: Character) -> Weapon | None:
        for item in char.equipment:
            if isinstance(item, Weapon):
                return item
        return None

    @staticmethod
    def _held_weapon(char: Character | None, rt: TokenCombatRuntime) -> Weapon | None:
        if not char:
            return None
        if rt.held_weapon_name:
            for item in char.equipment:
                if isinstance(item, Weapon) and item.name == rt.held_weapon_name:
                    return item
        return ImpulseCombatEngine._first_weapon(char)

    def available_actions(self, token_id: str) -> list[tuple[str, str, float | str]]:
        """Return (action_id, label, cost) for token action menu."""
        placement = self.tokens.placements.get(token_id)
        if not placement:
            return []
        rt = self.get_runtime(token_id)
        char = self.characters.get(placement.character_name or "")
        actions: list[tuple[str, str, float | str]] = [
            ("move", "Move", "var"),
            ("movement_while_braced", "Movement While Braced", "var"),
            ("brace_weapon", "Brace Weapon", 1),
            ("aim", "Aim", "var"),
            ("custom_action", "Custom Action", "var"),
            ("skip_impulse", "Skip Impulse", 0),
            ("set_fire_mode", "Set Fire Mode", 0),
            ("select_weapon", "Select Weapon", 0),
        ]
        for action_id, new_stance in STANCE_ACTION_MAP.items():
            if rt.stance != new_stance:
                cost = BUILTIN_ACTIONS[action_id].cost
                actions.append((action_id, BUILTIN_ACTIONS[action_id].name, float(cost)))
        weapon = self._held_weapon(char, rt)
        if weapon:
            actions.append(("reload", f"Reload ({weapon.name})", float(weapon.reload_time)))
            if weapon.actions_to_cycle is not None:
                actions.append(
                    ("cycle", f"Cycle ({weapon.name})", float(weapon.actions_to_cycle))
                )
        return actions
