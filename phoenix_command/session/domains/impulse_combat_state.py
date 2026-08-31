"""Impulse combat domain: phase clock, sides, per-token runtime."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class TokenCombatRuntime:
    """Per-token tactical state during impulse combat."""

    ac_remaining: float = 0.0
    stance: str = "standing"  # standing, kneeling, prone
    braced: bool = False
    held_weapon_name: str | None = None
    fire_mode: str = "single"  # single | 3rb | auto
    aim_ac_this_impulse: float = 0.0
    aim_ac_accumulated: float = 0.0
    aim_target_token_id: str | None = None
    aim_impulses: int = 0
    moved_this_impulse: bool = False
    hexes_moved_this_impulse: float = 0.0
    move_progress: float = 0.0
    move_target_q: int | None = None
    move_target_r: int | None = None
    weapon_cycled: bool = True
    aimed_this_impulse: bool = False
    balance_ac_owed: float = 0.0
    knockdown_phase: str = "none"  # none | falling | grounded
    hands_free: bool = True
    recoil_ac_owed: float = 0.0
    last_shot_q: int | None = None
    last_shot_r: int | None = None
    last_shot_layer_id: str = ""
    firing_stance_held: bool = False
    impulse_burst_used: bool = False
    held_grenade_name: str | None = None
    grenade_armed: bool = False
    pending_action_id: str | None = None
    pending_progress_ac: float = 0.0
    pending_total_cost_ac: float = 0.0
    pending_args: dict = field(default_factory=dict)
    looking_over_cover: bool = False
    ducking: bool = False

    def has_pending(self) -> bool:
        if self.pending_action_id:
            return True
        return self.move_progress > 0 and self.move_target_q is not None

    def pending_id(self) -> str | None:
        if self.pending_action_id:
            return self.pending_action_id
        if self.move_progress > 0 and self.move_target_q is not None:
            return "move"
        return None

    def clear_pending(self) -> None:
        self.pending_action_id = None
        self.pending_progress_ac = 0.0
        self.pending_total_cost_ac = 0.0
        self.pending_args = {}
        self.move_progress = 0.0
        self.move_target_q = None
        self.move_target_r = None

    def set_pending(
        self,
        action_id: str,
        total_cost: float,
        args: dict | None = None,
        progress: float = 0.0,
    ) -> None:
        self.pending_action_id = action_id
        self.pending_total_cost_ac = float(total_cost)
        self.pending_progress_ac = float(progress)
        self.pending_args = dict(args or {})

    def status_label(self) -> str:
        parts: list[str] = []
        if self.held_weapon_name:
            mode = {"single": "S", "3rb": "3RB", "auto": "A"}.get(self.fire_mode, self.fire_mode)
            parts.append(f"{self.held_weapon_name} [{mode}]")
            if not self.weapon_cycled:
                parts.append("needs cycle")
        parts.append(f"AC {self.ac_remaining:.1f}")
        if self.aim_impulses:
            parts.append(f"aim×{self.aim_impulses}")
        pid = self.pending_id()
        if pid == "move" or (self.move_progress > 0 and self.move_target_q is not None):
            parts.append(f"move {self.move_progress * 100:.0f}%")
        elif pid and self.pending_total_cost_ac > 0:
            parts.append(
                f"pending {pid} {self.pending_progress_ac:.0f}/{self.pending_total_cost_ac:.0f}"
            )
        if self.ducking:
            parts.append("ducking")
        if self.looking_over_cover:
            parts.append("looking")
        if self.knockdown_phase == "falling":
            parts.append("falling")
        elif self.knockdown_phase == "grounded":
            parts.append("grounded" if self.hands_free else "grounded (hands)")
        if self.balance_ac_owed > 0:
            parts.append(f"KD -{self.balance_ac_owed:.0f}AC")
        if self.recoil_ac_owed > 0:
            parts.append(f"recoil {self.recoil_ac_owed:.0f}AC")
        if self.held_grenade_name:
            parts.append(
                f"grenade: {self.held_grenade_name}"
                + (" armed" if self.grenade_armed else " in hand")
            )
        return " | ".join(parts)

    def to_dict(self) -> dict:
        return {
            "ac_remaining": self.ac_remaining,
            "stance": self.stance,
            "braced": self.braced,
            "held_weapon_name": self.held_weapon_name,
            "fire_mode": self.fire_mode,
            "aim_ac_this_impulse": self.aim_ac_this_impulse,
            "aim_ac_accumulated": self.aim_ac_accumulated,
            "aim_target_token_id": self.aim_target_token_id,
            "aim_impulses": self.aim_impulses,
            "moved_this_impulse": self.moved_this_impulse,
            "hexes_moved_this_impulse": self.hexes_moved_this_impulse,
            "move_progress": self.move_progress,
            "move_target_q": self.move_target_q,
            "move_target_r": self.move_target_r,
            "weapon_cycled": self.weapon_cycled,
            "aimed_this_impulse": self.aimed_this_impulse,
            "balance_ac_owed": self.balance_ac_owed,
            "knockdown_phase": self.knockdown_phase,
            "hands_free": self.hands_free,
            "recoil_ac_owed": self.recoil_ac_owed,
            "last_shot_q": self.last_shot_q,
            "last_shot_r": self.last_shot_r,
            "last_shot_layer_id": self.last_shot_layer_id,
            "firing_stance_held": self.firing_stance_held,
            "impulse_burst_used": self.impulse_burst_used,
            "held_grenade_name": self.held_grenade_name,
            "grenade_armed": self.grenade_armed,
            "pending_action_id": self.pending_action_id,
            "pending_progress_ac": self.pending_progress_ac,
            "pending_total_cost_ac": self.pending_total_cost_ac,
            "pending_args": dict(self.pending_args),
            "looking_over_cover": self.looking_over_cover,
            "ducking": self.ducking,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "TokenCombatRuntime":
        def _opt_int(key: str) -> int | None:
            raw = data.get(key)
            return int(raw) if raw is not None else None

        pending_args = data.get("pending_args") or {}
        if not isinstance(pending_args, dict):
            pending_args = {}
        return cls(
            ac_remaining=float(data.get("ac_remaining", 0.0)),
            stance=data.get("stance", "standing"),
            braced=bool(data.get("braced", False)),
            held_weapon_name=data.get("held_weapon_name"),
            fire_mode=data.get("fire_mode", "single"),
            aim_ac_this_impulse=float(data.get("aim_ac_this_impulse", 0.0)),
            aim_ac_accumulated=float(data.get("aim_ac_accumulated", 0.0)),
            aim_target_token_id=data.get("aim_target_token_id"),
            aim_impulses=int(data.get("aim_impulses", 0)),
            moved_this_impulse=bool(data.get("moved_this_impulse", False)),
            hexes_moved_this_impulse=float(data.get("hexes_moved_this_impulse", 0.0)),
            move_progress=float(data.get("move_progress", 0.0)),
            move_target_q=_opt_int("move_target_q"),
            move_target_r=_opt_int("move_target_r"),
            weapon_cycled=bool(data.get("weapon_cycled", True)),
            aimed_this_impulse=bool(data.get("aimed_this_impulse", False)),
            balance_ac_owed=float(data.get("balance_ac_owed", 0.0)),
            knockdown_phase=data.get("knockdown_phase", "none") or "none",
            hands_free=bool(data.get("hands_free", True)),
            recoil_ac_owed=float(data.get("recoil_ac_owed", 0.0)),
            last_shot_q=_opt_int("last_shot_q"),
            last_shot_r=_opt_int("last_shot_r"),
            last_shot_layer_id=data.get("last_shot_layer_id", "") or "",
            firing_stance_held=bool(data.get("firing_stance_held", False)),
            impulse_burst_used=bool(data.get("impulse_burst_used", False)),
            held_grenade_name=data.get("held_grenade_name"),
            grenade_armed=bool(data.get("grenade_armed", False)),
            pending_action_id=data.get("pending_action_id"),
            pending_progress_ac=float(data.get("pending_progress_ac", 0.0)),
            pending_total_cost_ac=float(data.get("pending_total_cost_ac", 0.0)),
            pending_args=dict(pending_args),
            looking_over_cover=bool(data.get("looking_over_cover", False)),
            ducking=bool(data.get("ducking", False)),
        )


@dataclass
class PendingShotPreview:
    """Synced shot modifier preview before confirmation."""

    preview_id: str
    shooter_token_id: str
    target_token_id: str
    proposed_by: str
    status: str = "open"  # open | confirmed | cancelled
    range_hexes: int = 1
    exposure: str = "STANDING_EXPOSED"
    orientation: str = "FRONT_REAR"
    stance_mods: list[str] = field(default_factory=list)
    visibility_mods: list[str] = field(default_factory=list)
    custom_eal_modifiers: list[dict] = field(default_factory=list)
    aim_time_ac: int = 1
    fire_mode: str = "single"
    weapon_name: str = ""
    ammo_name: str = ""
    visible_exposures: list[str] = field(default_factory=list)
    selected_exposure: str = "STANDING_EXPOSED"
    tof_impulses: int = 0
    notes: list[str] = field(default_factory=list)
    shooter_speed: float = 0.0
    target_speed: float = 0.0
    is_front: bool = True
    # Multi-target / area fire
    target_token_ids: list[str] = field(default_factory=list)
    secondary_by_primary: dict[str, list[str]] = field(default_factory=dict)
    aim_q: int | None = None
    aim_r: int | None = None
    aim_layer_id: str = ""
    arc_of_fire: float | None = None
    continuous_burst_impulses: int = 0
    per_target: dict[str, dict] = field(default_factory=dict)
    fire_kind: str = "single"  # single|burst|shotgun|shotgun_burst|3rb|grenade|agl|explosive
    cover_notes: list[str] = field(default_factory=list)
    manual_cover_pf: float | None = None
    estimated_cover_pf: float = 0.0

    def primary_ids(self) -> list[str]:
        if self.target_token_ids:
            return list(self.target_token_ids)
        if self.target_token_id:
            return [self.target_token_id]
        return []

    def to_dict(self) -> dict:
        return {
            "preview_id": self.preview_id,
            "shooter_token_id": self.shooter_token_id,
            "target_token_id": self.target_token_id,
            "proposed_by": self.proposed_by,
            "status": self.status,
            "range_hexes": self.range_hexes,
            "exposure": self.exposure,
            "orientation": self.orientation,
            "stance_mods": list(self.stance_mods),
            "visibility_mods": list(self.visibility_mods),
            "custom_eal_modifiers": list(self.custom_eal_modifiers),
            "aim_time_ac": self.aim_time_ac,
            "fire_mode": self.fire_mode,
            "weapon_name": self.weapon_name,
            "ammo_name": self.ammo_name,
            "visible_exposures": list(self.visible_exposures),
            "selected_exposure": self.selected_exposure,
            "tof_impulses": self.tof_impulses,
            "notes": list(self.notes),
            "shooter_speed": self.shooter_speed,
            "target_speed": self.target_speed,
            "is_front": self.is_front,
            "target_token_ids": list(self.target_token_ids),
            "secondary_by_primary": {
                k: list(v) for k, v in self.secondary_by_primary.items()
            },
            "aim_q": self.aim_q,
            "aim_r": self.aim_r,
            "aim_layer_id": self.aim_layer_id,
            "arc_of_fire": self.arc_of_fire,
            "continuous_burst_impulses": self.continuous_burst_impulses,
            "per_target": dict(self.per_target),
            "fire_kind": self.fire_kind,
            "cover_notes": list(self.cover_notes),
            "manual_cover_pf": self.manual_cover_pf,
            "estimated_cover_pf": self.estimated_cover_pf,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "PendingShotPreview":
        ids = list(data.get("target_token_ids", []))
        legacy = data.get("target_token_id", "")
        if not ids and legacy:
            ids = [legacy]
        aq = data.get("aim_q")
        ar = data.get("aim_r")
        arc = data.get("arc_of_fire")
        mcp = data.get("manual_cover_pf", None)
        return cls(
            preview_id=data.get("preview_id", ""),
            shooter_token_id=data.get("shooter_token_id", ""),
            target_token_id=legacy or (ids[0] if ids else ""),
            proposed_by=data.get("proposed_by", ""),
            status=data.get("status", "open"),
            range_hexes=int(data.get("range_hexes", 1)),
            exposure=data.get("exposure", "STANDING_EXPOSED"),
            orientation=data.get("orientation", "FRONT_REAR"),
            stance_mods=list(data.get("stance_mods", [])),
            visibility_mods=list(data.get("visibility_mods", [])),
            custom_eal_modifiers=list(data.get("custom_eal_modifiers", [])),
            aim_time_ac=int(data.get("aim_time_ac", 1)),
            fire_mode=data.get("fire_mode", "single"),
            weapon_name=data.get("weapon_name", ""),
            ammo_name=data.get("ammo_name", ""),
            visible_exposures=list(data.get("visible_exposures", [])),
            selected_exposure=data.get("selected_exposure", "STANDING_EXPOSED"),
            tof_impulses=int(data.get("tof_impulses", 0)),
            notes=list(data.get("notes", [])),
            shooter_speed=float(data.get("shooter_speed", 0.0)),
            target_speed=float(data.get("target_speed", 0.0)),
            is_front=bool(data.get("is_front", True)),
            target_token_ids=ids,
            secondary_by_primary={
                k: list(v) for k, v in data.get("secondary_by_primary", {}).items()
            },
            aim_q=int(aq) if aq is not None else None,
            aim_r=int(ar) if ar is not None else None,
            aim_layer_id=data.get("aim_layer_id", ""),
            arc_of_fire=float(arc) if arc is not None else None,
            continuous_burst_impulses=int(data.get("continuous_burst_impulses", 0)),
            per_target=dict(data.get("per_target", {})),
            fire_kind=data.get("fire_kind", "single"),
            cover_notes=list(data.get("cover_notes", [])),
            manual_cover_pf=float(mcp) if mcp is not None else None,
            estimated_cover_pf=float(data.get("estimated_cover_pf", 0.0)),
        )


@dataclass
class PendingProjectile:
    """In-flight shot awaiting TOF resolution on a future impulse."""

    projectile_id: str
    resolve_phase: int
    resolve_impulse: int
    shooter_token_id: str
    target_token_id: str
    shot_snapshot: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "projectile_id": self.projectile_id,
            "resolve_phase": self.resolve_phase,
            "resolve_impulse": self.resolve_impulse,
            "shooter_token_id": self.shooter_token_id,
            "target_token_id": self.target_token_id,
            "shot_snapshot": dict(self.shot_snapshot),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "PendingProjectile":
        return cls(
            projectile_id=data.get("projectile_id", ""),
            resolve_phase=int(data.get("resolve_phase", 1)),
            resolve_impulse=int(data.get("resolve_impulse", 0)),
            shooter_token_id=data.get("shooter_token_id", ""),
            target_token_id=data.get("target_token_id", ""),
            shot_snapshot=dict(data.get("shot_snapshot", {})),
        )


@dataclass
class PendingGrenadeExplosion:
    """Timed grenade blast awaiting fuse resolution."""

    explosion_id: str
    resolve_phase: int
    resolve_impulse: int
    shooter_token_id: str
    preview_snapshot: dict = field(default_factory=dict)
    explosive_results: list[dict] = field(default_factory=list)
    weapon_name: str = ""
    ammo_name: str = ""

    def to_dict(self) -> dict:
        return {
            "explosion_id": self.explosion_id,
            "resolve_phase": self.resolve_phase,
            "resolve_impulse": self.resolve_impulse,
            "shooter_token_id": self.shooter_token_id,
            "preview_snapshot": dict(self.preview_snapshot),
            "explosive_results": list(self.explosive_results),
            "weapon_name": self.weapon_name,
            "ammo_name": self.ammo_name,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "PendingGrenadeExplosion":
        return cls(
            explosion_id=data.get("explosion_id", ""),
            resolve_phase=int(data.get("resolve_phase", 1)),
            resolve_impulse=int(data.get("resolve_impulse", 0)),
            shooter_token_id=data.get("shooter_token_id", ""),
            preview_snapshot=dict(data.get("preview_snapshot", {})),
            explosive_results=list(data.get("explosive_results", [])),
            weapon_name=data.get("weapon_name", ""),
            ammo_name=data.get("ammo_name", ""),
        )


@dataclass
class ImpulseCombatState:
    """Tactical combat clock and token runtime on the map."""

    map_mode: str = "edit"  # "edit" | "combat"
    phase: int = 1
    impulse: int = 0  # 0..3
    sides: dict[str, str] = field(default_factory=dict)
    token_runtime: dict[str, TokenCombatRuntime] = field(default_factory=dict)
    selected_token_id: str | None = None
    shot_preview: PendingShotPreview | None = None
    pending_projectiles: list[PendingProjectile] = field(default_factory=list)
    pending_grenade_explosions: list[PendingGrenadeExplosion] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "map_mode": self.map_mode,
            "phase": self.phase,
            "impulse": self.impulse,
            "sides": dict(self.sides),
            "token_runtime": {
                tid: rt.to_dict() for tid, rt in self.token_runtime.items()
            },
            "selected_token_id": self.selected_token_id,
            "shot_preview": self.shot_preview.to_dict() if self.shot_preview else None,
            "pending_projectiles": [p.to_dict() for p in self.pending_projectiles],
            "pending_grenade_explosions": [
                g.to_dict() for g in self.pending_grenade_explosions
            ],
        }

    @classmethod
    def from_dict(cls, data: dict | None) -> "ImpulseCombatState":
        if not data:
            return cls()
        raw_rt = data.get("token_runtime", {})
        preview_raw = data.get("shot_preview")
        return cls(
            map_mode=data.get("map_mode", "edit"),
            phase=int(data.get("phase", 1)),
            impulse=int(data.get("impulse", 0)),
            sides=dict(data.get("sides", {})),
            token_runtime={
                tid: TokenCombatRuntime.from_dict(rt)
                for tid, rt in raw_rt.items()
            },
            selected_token_id=data.get("selected_token_id"),
            shot_preview=PendingShotPreview.from_dict(preview_raw) if preview_raw else None,
            pending_projectiles=[
                PendingProjectile.from_dict(p)
                for p in data.get("pending_projectiles", [])
            ],
            pending_grenade_explosions=[
                PendingGrenadeExplosion.from_dict(g)
                for g in data.get("pending_grenade_explosions", [])
            ],
        )
