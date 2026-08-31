"""Impulse combat action engine: AC spending, movement, reload, pending carry-over."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from phoenix_command.models.character import Character
from phoenix_command.models.gear import Grenade, Weapon
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
from phoenix_command.simulations.map_fire_ac import clear_aim_state
from phoenix_command.simulations.map_knockdown import HANDS_FREE_AC
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
    "kneeling_to_standing": "standing",
    "prone_to_kneeling": "kneeling",
    "prone_to_standing": "standing",
}

COVER_FIRING_STANCE_ACTIONS = frozenset(
    {
        "assume_firing_stance_cover",
        "assume_hip_firing_stance_cover",
    }
)

# Actions allowed while another pending action exists (without continue match).
PENDING_EXEMPT = frozenset(
    {
        "abandon_pending",
        "duck",
        "recover",
        "recover_hands",
        "skip_impulse",
        "set_fire_mode",
    }
)

# Book: interrupting actions clear accumulated Aim Time.
AIM_INTERRUPT_ACTIONS = frozenset(
    {
        "move",
        "movement_while_braced",
        "reload",
        "cycle",
        "select_weapon",
        "pick_up_grenade",
        "arm_grenade",
        "brace_weapon",
        "look_over_cover",
        "duck",
        "duck_from_firing",
        "custom_action",
        *STANCE_ACTION_MAP.keys(),
        *COVER_FIRING_STANCE_ACTIONS,
    }
)


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
                # Keep move_progress / pending_* across impulses (carry-over).
                rt.impulse_burst_used = False
                rt.ducking = False
                if rt.knockdown_phase == "falling":
                    rt.knockdown_phase = "grounded"

    def advance_impulse(self) -> tuple[list, list]:
        """Move to next impulse (host only). Returns (due projectiles, due grenades)."""
        self.impulse_combat.impulse += 1
        if self.impulse_combat.impulse >= 4:
            self.impulse_combat.impulse = 0
            self.impulse_combat.phase += 1
        self.refill_impulse_ac()
        return self.pop_due_projectiles(), self.pop_due_grenade_explosions()

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

    def pop_due_grenade_explosions(self) -> list:
        """Return and remove grenade blasts due at the current phase/impulse."""
        from phoenix_command.session.domains.impulse_combat_state import PendingGrenadeExplosion

        phase = self.impulse_combat.phase
        impulse = self.impulse_combat.impulse
        due: list[PendingGrenadeExplosion] = []
        remaining: list[PendingGrenadeExplosion] = []
        for expl in self.impulse_combat.pending_grenade_explosions:
            if expl.resolve_phase < phase or (
                expl.resolve_phase == phase and expl.resolve_impulse <= impulse
            ):
                due.append(expl)
            else:
                remaining.append(expl)
        self.impulse_combat.pending_grenade_explosions = remaining
        return due

    def schedule_grenade_explosion(
        self,
        shooter_token_id: str,
        fuse_impulses: int,
        preview_snapshot: dict,
        explosive_results: list[dict],
        weapon_name: str,
        ammo_name: str,
    ):
        from phoenix_command.session.domains.impulse_combat_state import PendingGrenadeExplosion
        import uuid

        abs_now = self.absolute_impulse_index()
        abs_resolve = abs_now + max(1, int(fuse_impulses))
        resolve_phase = abs_resolve // 4 + 1
        resolve_impulse = abs_resolve % 4
        expl = PendingGrenadeExplosion(
            explosion_id=str(uuid.uuid4()),
            resolve_phase=resolve_phase,
            resolve_impulse=resolve_impulse,
            shooter_token_id=shooter_token_id,
            preview_snapshot=dict(preview_snapshot),
            explosive_results=list(explosive_results),
            weapon_name=weapon_name,
            ammo_name=ammo_name,
        )
        self.impulse_combat.pending_grenade_explosions.append(expl)
        return expl

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

        rt = self.get_runtime(token_id)
        if action == "abandon_pending":
            return self._apply_abandon_pending(placement)
        if action == "duck":
            return self._apply_free_duck(placement)
        if action == "recover":
            return self._apply_recover(
                placement, float(args.get("ac", rt.recoil_ac_owed + rt.balance_ac_owed))
            )
        if action == "recover_hands":
            return self._apply_recover_hands(placement)

        blocked = self._knockdown_block(rt, action)
        if blocked:
            return blocked
        auto = self._auto_pay_owed(rt, action)
        if auto:
            return auto

        conflict = self._pending_conflict(rt, action, args)
        if conflict:
            return conflict

        if action in ("move", "movement_while_braced"):
            return self._apply_move(
                placement,
                int(args.get("target_q", placement.q)),
                int(args.get("target_r", placement.r)),
                braced=action == "movement_while_braced",
            )
        if action == "brace_weapon":
            return self._apply_brace(placement)
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
        if action == "pick_up_grenade":
            return self._apply_pick_up_grenade(placement, args.get("grenade_name"))
        if action == "arm_grenade":
            return self._apply_arm_grenade(placement)
        if action == "custom_action":
            return self._apply_custom_action(
                placement, float(args.get("ac", 1)), str(args.get("label", "Custom"))
            )
        if action == "skip_impulse":
            return self._apply_skip(placement)
        if action in STANCE_ACTION_MAP:
            return self._apply_stance_change(placement, action)
        if action == "duck_from_firing":
            return self._apply_duck_from_firing(placement)
        if action in BUILTIN_ACTIONS and action != "pick_up_grenade":
            return self._apply_catalog_action(placement, action)
        return ActionResult(False, f"Unknown action: {action}")

    def _pending_conflict(
        self, rt: TokenCombatRuntime, action: str, args: dict[str, Any]
    ) -> ActionResult | None:
        if action in PENDING_EXEMPT:
            return None
        if not rt.has_pending():
            return None
        pending = rt.pending_id()
        if action == pending or (
            pending == "move" and action in ("move", "movement_while_braced")
        ):
            if pending == "move" and action in ("move", "movement_while_braced"):
                tq = args.get("target_q")
                tr = args.get("target_r")
                if (
                    tq is not None
                    and tr is not None
                    and rt.move_target_q is not None
                    and (int(tq) != rt.move_target_q or int(tr) != rt.move_target_r)
                ):
                    return ActionResult(
                        False, "Abandon or continue pending move first"
                    )
            return None
        return ActionResult(
            False, f"Abandon or continue pending {pending} first"
        )

    def _interrupt_aim_if_needed(self, rt: TokenCombatRuntime, action: str) -> None:
        if action in AIM_INTERRUPT_ACTIONS:
            clear_aim_state(rt)

    def _apply_abandon_pending(self, placement: TokenPlacement) -> ActionResult:
        rt = self.get_runtime(placement.token_id)
        pending = rt.pending_id()
        if not pending:
            return ActionResult(False, "No pending action")
        rt.clear_pending()
        return ActionResult(True, f"Abandoned pending {pending}")

    def _apply_free_duck(self, placement: TokenPlacement) -> ActionResult:
        rt = self.get_runtime(placement.token_id)
        pending = rt.pending_id()
        clear_aim_state(rt)
        if pending:
            rt.clear_pending()
        rt.firing_stance_held = False
        rt.looking_over_cover = False
        rt.ducking = True
        msg = "Duck (0 AC)"
        if pending:
            msg += f" — interrupted {pending}"
        return ActionResult(True, msg, 0.0)

    def _apply_duck_from_firing(self, placement: TokenPlacement) -> ActionResult:
        rt = self.get_runtime(placement.token_id)
        if not (rt.firing_stance_held or rt.looking_over_cover):
            return ActionResult(False, "Not in firing stance or looking over cover")

        def _complete(runtime: TokenCombatRuntime) -> None:
            runtime.firing_stance_held = False
            runtime.looking_over_cover = False
            runtime.ducking = True

        return self._partial_spend(
            placement,
            "duck_from_firing",
            1.0,
            {},
            on_complete=_complete,
            label="Duck from firing/looking",
            interrupt_aim=True,
        )

    def _partial_spend(
        self,
        placement: TokenPlacement,
        action_id: str,
        total_cost: float,
        args: dict[str, Any],
        *,
        on_complete: Callable[[TokenCombatRuntime], None],
        label: str,
        interrupt_aim: bool = True,
    ) -> ActionResult:
        rt = self.get_runtime(placement.token_id)
        total_cost = float(total_cost)
        if total_cost <= 0:
            if interrupt_aim:
                self._interrupt_aim_if_needed(rt, action_id)
            on_complete(rt)
            return ActionResult(True, f"{label} (0 AC)", 0.0)

        starting = rt.pending_action_id != action_id
        if starting:
            if interrupt_aim:
                self._interrupt_aim_if_needed(rt, action_id)
            rt.set_pending(action_id, total_cost, args, progress=0.0)

        remaining = rt.pending_total_cost_ac - rt.pending_progress_ac
        if remaining <= 1e-9:
            on_complete(rt)
            rt.pending_action_id = None
            rt.pending_progress_ac = 0.0
            rt.pending_total_cost_ac = 0.0
            rt.pending_args = {}
            return ActionResult(True, f"{label} complete", 0.0)

        spend = min(rt.ac_remaining, remaining)
        if spend <= 0:
            return ActionResult(False, "No AC remaining")
        rt.ac_remaining -= spend
        rt.pending_progress_ac += spend
        if rt.pending_progress_ac + 1e-9 >= rt.pending_total_cost_ac:
            on_complete(rt)
            done_cost = rt.pending_total_cost_ac
            rt.pending_action_id = None
            rt.pending_progress_ac = 0.0
            rt.pending_total_cost_ac = 0.0
            rt.pending_args = {}
            return ActionResult(True, f"{label} complete ({done_cost:.0f} AC)", spend)
        return ActionResult(
            True,
            f"{label} {rt.pending_progress_ac:.0f}/{rt.pending_total_cost_ac:.0f} AC",
            spend,
        )

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

        def _complete(rt: TokenCombatRuntime) -> None:
            self._apply_catalog_completion(rt, action_id)

        return self._partial_spend(
            placement,
            action_id,
            cost,
            {},
            on_complete=_complete,
            label=action_def.name,
            interrupt_aim=action_id in AIM_INTERRUPT_ACTIONS,
        )

    def _apply_catalog_completion(self, rt: TokenCombatRuntime, action_id: str) -> None:
        if action_id == "brace_weapon":
            rt.braced = True
        elif action_id == "look_over_cover":
            rt.looking_over_cover = True
        elif action_id in COVER_FIRING_STANCE_ACTIONS:
            rt.firing_stance_held = True
            rt.looking_over_cover = True
        elif action_id == "duck_from_firing":
            rt.firing_stance_held = False
            rt.looking_over_cover = False
            rt.ducking = True

    def _apply_brace(self, placement: TokenPlacement) -> ActionResult:
        return self._partial_spend(
            placement,
            "brace_weapon",
            float(BUILTIN_ACTIONS["brace_weapon"].cost),
            {},
            on_complete=lambda rt: setattr(rt, "braced", True),
            label="Brace Weapon",
            interrupt_aim=True,
        )

    def _apply_stance_change(self, placement: TokenPlacement, action_id: str) -> ActionResult:
        cost = float(BUILTIN_ACTIONS[action_id].cost)

        def _complete(rt: TokenCombatRuntime) -> None:
            rt.stance = STANCE_ACTION_MAP[action_id]
            rt.braced = False
            rt.firing_stance_held = False
            rt.looking_over_cover = False
            if rt.knockdown_phase == "grounded" and rt.stance in ("kneeling", "standing"):
                rt.knockdown_phase = "none"
                rt.hands_free = True

        return self._partial_spend(
            placement,
            action_id,
            cost,
            {},
            on_complete=_complete,
            label=BUILTIN_ACTIONS[action_id].name,
            interrupt_aim=True,
        )

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
        self._interrupt_aim_if_needed(rt, "select_weapon")
        rt.held_weapon_name = found.name
        rt.weapon_cycled = found.actions_to_cycle is None
        rt.fire_mode = "single"
        rt.firing_stance_held = False
        rt.looking_over_cover = False
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

    def _apply_pick_up_grenade(
        self, placement: TokenPlacement, grenade_name: str | None
    ) -> ActionResult:
        char = self.characters.get(placement.character_name or "")
        if not char:
            return ActionResult(False, "No character")
        grenades = [i for i in char.equipment if isinstance(i, Grenade)]
        if not grenades:
            return ActionResult(False, "No grenade in equipment")
        found = None
        if grenade_name:
            for g in grenades:
                if g.name == grenade_name:
                    found = g
                    break
        else:
            found = grenades[0]
        if not found:
            return ActionResult(False, f"Grenade not found: {grenade_name}")
        cost = float(BUILTIN_ACTIONS["pick_up_grenade"].cost)
        name = found.name
        arm_ready = found.arm_time <= 0

        def _complete(rt: TokenCombatRuntime) -> None:
            rt.held_grenade_name = name
            rt.grenade_armed = arm_ready

        return self._partial_spend(
            placement,
            "pick_up_grenade",
            cost,
            {"grenade_name": name},
            on_complete=_complete,
            label=f"Pick up {name}",
            interrupt_aim=True,
        )

    def _apply_arm_grenade(self, placement: TokenPlacement) -> ActionResult:
        char = self.characters.get(placement.character_name or "")
        if not char:
            return ActionResult(False, "No character")
        rt = self.get_runtime(placement.token_id)
        if not rt.held_grenade_name:
            return ActionResult(False, "No grenade in hand")
        found = None
        for item in char.equipment:
            if isinstance(item, Grenade) and item.name == rt.held_grenade_name:
                found = item
                break
        if not found:
            return ActionResult(False, "Grenade no longer in equipment")
        cost = float(found.arm_time or 0)
        if cost <= 0:
            rt.grenade_armed = True
            return ActionResult(True, f"{found.name} ready (no arm time)")
        name = found.name
        return self._partial_spend(
            placement,
            "arm_grenade",
            cost,
            {},
            on_complete=lambda runtime: setattr(runtime, "grenade_armed", True),
            label=f"Arm {name}",
            interrupt_aim=True,
        )

    def _apply_custom_action(
        self, placement: TokenPlacement, ac: float, label: str
    ) -> ActionResult:
        ac = max(0.0, ac)
        if ac <= 0:
            return ActionResult(False, "Custom action needs AC > 0")
        return self._partial_spend(
            placement,
            "custom_action",
            ac,
            {"label": label},
            on_complete=lambda _rt: None,
            label=label,
            interrupt_aim=True,
        )

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
        return self._partial_spend(
            placement,
            "reload",
            cost,
            {},
            on_complete=lambda runtime: setattr(runtime, "weapon_cycled", True),
            label=f"Reload {weapon.name}",
            interrupt_aim=True,
        )

    def _apply_cycle(self, placement: TokenPlacement) -> ActionResult:
        char = self.characters.get(placement.character_name or "")
        rt = self.get_runtime(placement.token_id)
        weapon = self._held_weapon(char, rt)
        if not weapon or weapon.actions_to_cycle is None:
            return ActionResult(False, "Weapon does not require cycling")
        cost = float(weapon.actions_to_cycle)
        return self._partial_spend(
            placement,
            "cycle",
            cost,
            {},
            on_complete=lambda runtime: setattr(runtime, "weapon_cycled", True),
            label=f"Cycle {weapon.name}",
            interrupt_aim=True,
        )

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
            from phoenix_command.session.domains.map_state import hex_wall_key
            if hex_wall_key(target_q, target_r) in layer.walls:
                return ActionResult(False, "Hex blocked by wall")

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
            self._interrupt_aim_if_needed(rt, "move")
            rt.move_target_q = target_q
            rt.move_target_r = target_r
            rt.move_progress = 0.0
            rt.pending_action_id = "move"
            rt.pending_total_cost_ac = hex_cost
            rt.pending_progress_ac = 0.0
            rt.pending_args = {"target_q": target_q, "target_r": target_r, "braced": braced}
        elif rt.pending_action_id != "move":
            rt.pending_action_id = "move"
            rt.pending_total_cost_ac = hex_cost
            rt.pending_args = {"target_q": target_q, "target_r": target_r, "braced": braced}

        remaining_frac = max(0.0, 1.0 - rt.move_progress)
        remaining_ac = remaining_frac * hex_cost if hex_cost else 0.0
        spend = min(ac_available, remaining_ac)
        if spend <= 0 and remaining_frac > 0:
            return ActionResult(False, "No AC remaining")

        rt.ac_remaining -= spend
        if hex_cost > 0:
            rt.move_progress += spend / hex_cost
            rt.pending_progress_ac = rt.move_progress * hex_cost
            rt.pending_total_cost_ac = hex_cost
        rt.moved_this_impulse = True
        rt.firing_stance_held = False
        rt.looking_over_cover = False
        rt.hexes_moved_this_impulse += spend / hex_cost if hex_cost else 0

        if rt.move_progress >= 1.0 - 1e-9:
            placement.q = target_q
            placement.r = target_r
            rt.move_progress = 0.0
            rt.move_target_q = None
            rt.move_target_r = None
            rt.pending_action_id = None
            rt.pending_progress_ac = 0.0
            rt.pending_total_cost_ac = 0.0
            rt.pending_args = {}
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

    @staticmethod
    def _held_grenade(char: Character | None, rt: TokenCombatRuntime) -> Grenade | None:
        if not char or not rt.held_grenade_name:
            return None
        for item in char.equipment:
            if isinstance(item, Grenade) and item.name == rt.held_grenade_name:
                return item
        return None

    def _owed(self, rt: TokenCombatRuntime) -> float:
        return max(0.0, rt.recoil_ac_owed) + max(0.0, rt.balance_ac_owed)

    def _consume_owed(self, rt: TokenCombatRuntime, amount: float) -> float:
        left = amount
        take = min(max(0.0, rt.recoil_ac_owed), left)
        rt.recoil_ac_owed -= take
        left -= take
        take = min(max(0.0, rt.balance_ac_owed), left)
        rt.balance_ac_owed -= take
        left -= take
        return amount - left

    def _knockdown_block(self, rt: TokenCombatRuntime, action: str) -> ActionResult | None:
        if action in ("skip_impulse", "set_fire_mode", "duck", "abandon_pending"):
            return None
        if rt.knockdown_phase == "falling":
            return ActionResult(False, "Knocked off feet this impulse")
        if rt.knockdown_phase == "grounded" and not rt.hands_free:
            return ActionResult(False, "Must spend 3 AC to use hands first")
        return None

    def _auto_pay_owed(self, rt: TokenCombatRuntime, action: str) -> ActionResult | None:
        if action in (
            "skip_impulse",
            "set_fire_mode",
            "recover",
            "recover_hands",
            "duck",
            "abandon_pending",
        ):
            return None
        owed = self._owed(rt)
        if owed <= 0:
            return None
        if rt.ac_remaining < owed:
            return ActionResult(False, f"Need {owed:.0f} AC to recover (recoil/balance) first")
        spent = self._consume_owed(rt, owed)
        rt.ac_remaining -= spent
        return None

    def _apply_recover(self, placement: TokenPlacement, ac: float) -> ActionResult:
        rt = self.get_runtime(placement.token_id)
        if rt.knockdown_phase == "falling":
            return ActionResult(False, "Knocked off feet this impulse")
        owed = self._owed(rt)
        if owed <= 0:
            return ActionResult(False, "Nothing to recover")
        ac = max(0.0, ac)
        spend = min(ac, owed, rt.ac_remaining)
        if spend <= 0:
            return ActionResult(False, "No AC remaining")
        paid = self._consume_owed(rt, spend)
        rt.ac_remaining -= paid
        return ActionResult(True, f"Recover {paid:.1f} AC", paid)

    def _apply_recover_hands(self, placement: TokenPlacement) -> ActionResult:
        rt = self.get_runtime(placement.token_id)
        if rt.knockdown_phase == "falling":
            return ActionResult(False, "Knocked off feet this impulse")
        if rt.hands_free:
            return ActionResult(False, "Hands already free")
        if rt.ac_remaining < HANDS_FREE_AC:
            return ActionResult(False, f"Need {HANDS_FREE_AC:.0f} AC to use hands")
        rt.ac_remaining -= HANDS_FREE_AC
        rt.hands_free = True
        return ActionResult(True, "Rolled to use hands (3 AC)", HANDS_FREE_AC)

    def available_actions(self, token_id: str) -> list[tuple[str, str, float | str]]:
        """Return (action_id, label, cost) for token action menu."""
        placement = self.tokens.placements.get(token_id)
        if not placement:
            return []
        rt = self.get_runtime(token_id)
        char = self.characters.get(placement.character_name or "")
        if rt.knockdown_phase == "falling":
            return [
                ("duck", "Duck", 0),
                ("skip_impulse", "Skip Impulse", 0),
            ]
        actions: list[tuple[str, str, float | str]] = []
        if rt.has_pending():
            pid = rt.pending_id() or "action"
            actions.append(("abandon_pending", f"Abandon pending ({pid})", 0))
        owed = self._owed(rt)
        if owed > 0:
            actions.append(("recover", f"Recover recoil/balance ({owed:.0f} AC)", owed))
        if rt.knockdown_phase == "grounded" and not rt.hands_free:
            actions.append(("recover_hands", "Use hands (roll)", HANDS_FREE_AC))
            actions.append(("duck", "Duck", 0))
            actions.append(("skip_impulse", "Skip Impulse", 0))
            return actions
        actions.extend(
            [
                ("duck", "Duck", 0),
                ("move", "Move", "var"),
                ("movement_while_braced", "Movement While Braced", "var"),
                ("brace_weapon", "Brace Weapon", 1),
                ("aim", "Aim", "var"),
                ("custom_action", "Custom Action", "var"),
                ("skip_impulse", "Skip Impulse", 0),
                ("set_fire_mode", "Set Fire Mode", 0),
                ("select_weapon", "Select Weapon", 0),
                ("look_over_cover", "Look Over or Around Cover", 1),
                (
                    "assume_firing_stance_cover",
                    "Assume Firing Stance (Cover)",
                    2,
                ),
                (
                    "assume_hip_firing_stance_cover",
                    "Assume Hip Firing Stance (Cover)",
                    1,
                ),
            ]
        )
        if rt.firing_stance_held or rt.looking_over_cover:
            actions.append(
                ("duck_from_firing", "Duck from Firing Stance / Looking", 1)
            )
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
        grenades = [i for i in (char.equipment if char else []) if isinstance(i, Grenade)]
        if grenades:
            if not rt.held_grenade_name:
                actions.append(("pick_up_grenade", "Pick up Grenade", 2.0))
            else:
                g = self._held_grenade(char, rt)
                if g and not rt.grenade_armed and (g.arm_time or 0) > 0:
                    actions.append(
                        ("arm_grenade", f"Arm {g.name}", float(g.arm_time))
                    )
        return actions
