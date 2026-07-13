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
        if self.move_progress > 0:
            parts.append(f"move {self.move_progress * 100:.0f}%")
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
        }

    @classmethod
    def from_dict(cls, data: dict) -> "TokenCombatRuntime":
        mtq = data.get("move_target_q")
        mtr = data.get("move_target_r")
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
            move_target_q=int(mtq) if mtq is not None else None,
            move_target_r=int(mtr) if mtr is not None else None,
            weapon_cycled=bool(data.get("weapon_cycled", True)),
            aimed_this_impulse=bool(data.get("aimed_this_impulse", False)),
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
    aim_time_ac: int = 2
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
        }

    @classmethod
    def from_dict(cls, data: dict) -> "PendingShotPreview":
        return cls(
            preview_id=data.get("preview_id", ""),
            shooter_token_id=data.get("shooter_token_id", ""),
            target_token_id=data.get("target_token_id", ""),
            proposed_by=data.get("proposed_by", ""),
            status=data.get("status", "open"),
            range_hexes=int(data.get("range_hexes", 1)),
            exposure=data.get("exposure", "STANDING_EXPOSED"),
            orientation=data.get("orientation", "FRONT_REAR"),
            stance_mods=list(data.get("stance_mods", [])),
            visibility_mods=list(data.get("visibility_mods", [])),
            custom_eal_modifiers=list(data.get("custom_eal_modifiers", [])),
            aim_time_ac=int(data.get("aim_time_ac", 2)),
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
        )
