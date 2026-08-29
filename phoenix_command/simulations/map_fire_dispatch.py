"""Dispatch map PendingShotPreview to CombatSimulator APIs."""

from __future__ import annotations

from dataclasses import dataclass, field

from phoenix_command.models.character import Character
from phoenix_command.models.enums import (
    BlastModifier,
    ExplosiveTarget,
    SituationStanceModifier4B,
    TargetExposure,
    TargetOrientation,
    VisibilityModifier4C,
    WeaponType,
)
from phoenix_command.models.gear import AmmoType, Grenade, Weapon
from phoenix_command.models.hit_result_advanced import (
    ExplosiveShotResult,
    ShotParameters,
    ShotResult,
    TargetGroup,
)
from phoenix_command.session.domains.impulse_combat_state import (
    PendingShotPreview,
    TokenCombatRuntime,
)
from phoenix_command.session.domains.map_state import MapState, rules_hexes
from phoenix_command.session.domains.token_state import TokenPlacement, TokenState
from phoenix_command.simulations.combat_simulator import CombatSimulator
from phoenix_command.simulations.map_fire_targets import (
    build_per_target_entry,
    infer_fire_kind,
    tokens_in_arc,
    tokens_in_blast,
    tokens_in_pattern,
)
from phoenix_command.simulations.map_los import check_los
from phoenix_command.simulations.map_shot_context import build_map_shot_context
from phoenix_command.gui.utils.hex_geometry import axial_distance


def _rt(runtime: dict, token_id: str) -> TokenCombatRuntime:
    return runtime.get(token_id) or TokenCombatRuntime()


def _per_from_ctx(ctx) -> dict:
    return {
        "range_hexes": ctx.range_rule_hexes,
        "exposure": ctx.target_exposure.name,
        "orientation": ctx.shot_params.target_orientation.name,
        "orientation_key": getattr(ctx, "orientation_key", "front"),
        "is_front": ctx.is_front_shot,
        "visible_exposures": [e.name for e in ctx.visible_exposures],
        "los_clear": bool(ctx.los and ctx.los.clear and not ctx.los.blocked),
        "notes": list(ctx.visibility_notes),
    }


@dataclass
class MapFireOutcome:
    """Result of resolving a map fire action."""

    kind: str
    shot_results: list[ShotResult] = field(default_factory=list)
    explosive_results: list[ExplosiveShotResult] = field(default_factory=list)
    messages: list[str] = field(default_factory=list)
    miss_reasons: list[str] = field(default_factory=list)


def enrich_preview_targets(
    preview: PendingShotPreview,
    shooter: TokenPlacement,
    tokens: TokenState,
    map_state: MapState | None,
    token_runtime: dict,
    weapon: Weapon | Grenade | None,
    ammo: AmmoType | Grenade | None,
) -> PendingShotPreview:
    """Fill multi-target / aim fields from map geometry based on fire mode."""
    kind = infer_fire_kind(preview.fire_mode, weapon, ammo)
    preview.fire_kind = kind
    runtime = token_runtime or {}

    if kind in ("grenade", "agl", "explosive"):
        if preview.aim_q is None or preview.aim_r is None:
            # Default aim to primary target hex
            tid = preview.target_token_id
            tok = tokens.placements.get(tid) if tid else None
            if tok:
                preview.aim_q = tok.q
                preview.aim_r = tok.r
                preview.aim_layer_id = tok.layer_id or ""
            else:
                preview.aim_q = shooter.q
                preview.aim_r = shooter.r
                preview.aim_layer_id = shooter.layer_id or ""
        mph = map_state.grid.meters_per_hex if map_state else 1.0
        max_blast_m = 20.0
        if ammo and getattr(ammo, "explosive_data", None):
            max_blast_m = max(
                (d.range_hexes * 2.0 for d in ammo.explosive_data),
                default=20.0,
            )
        victims = tokens_in_blast(
            preview.aim_q,
            preview.aim_r,
            max_blast_m,
            tokens,
            map_state,
            shooter=shooter,
            layer_id=preview.aim_layer_id,
        )
        preview.target_token_ids = [tid for tid, _ in victims]
        for tid, dist_m in victims:
            tok = tokens.placements[tid]
            ctx = build_map_shot_context(
                shooter, _rt(runtime, shooter.token_id), tok, _rt(runtime, tid), map_state
            )
            entry = _per_from_ctx(ctx)
            entry["distance_m"] = dist_m
            entry["notes"] = list(entry.get("notes", [])) + [f"blast dist {dist_m:.1f}m"]
            preview.per_target[tid] = entry
        if preview.target_token_ids:
            preview.target_token_id = preview.target_token_ids[0]
        return preview

    if kind in ("burst", "shotgun_burst"):
        half_angle = 30.0
        if preview.arc_of_fire is not None and preview.arc_of_fire > 0:
            half_angle = max(15.0, min(90.0, float(preview.arc_of_fire) * 8))
        infos = tokens_in_arc(
            shooter, tokens, map_state, runtime, half_angle_deg=half_angle
        )
        clear = [i for i in infos if i.los_clear] or infos
        preview.target_token_ids = [i.token_id for i in clear]
        preview.per_target = {i.token_id: build_per_target_entry(i) for i in clear}
        if preview.target_token_ids:
            preview.target_token_id = preview.target_token_ids[0]
            pt = preview.per_target.get(preview.target_token_id, {})
            preview.range_hexes = int(pt.get("range_hexes", preview.range_hexes))
            preview.exposure = pt.get("exposure", preview.exposure)
            preview.selected_exposure = preview.exposure
            preview.orientation = pt.get("orientation", preview.orientation)
            preview.is_front = bool(pt.get("is_front", True))

        if kind == "shotgun_burst" and ammo:
            preview.secondary_by_primary = {}
            for pid in preview.target_token_ids:
                ptok = tokens.placements.get(pid)
                if not ptok:
                    continue
                radius = CombatSimulator.get_shotgun_pattern_radius(
                    ammo, int(preview.per_target.get(pid, {}).get("range_hexes", 1))
                )
                if radius is None:
                    radius = 1.0
                secs = tokens_in_pattern(
                    ptok.q,
                    ptok.r,
                    float(radius),
                    tokens,
                    map_state,
                    shooter=shooter,
                    exclude_ids={pid},
                    layer_id=ptok.layer_id or "",
                )
                preview.secondary_by_primary[pid] = secs
                for sid in secs:
                    if sid in preview.per_target:
                        continue
                    stok = tokens.placements.get(sid)
                    if not stok:
                        continue
                    ctx = build_map_shot_context(
                        shooter,
                        _rt(runtime, shooter.token_id),
                        stok,
                        _rt(runtime, sid),
                        map_state,
                    )
                    preview.per_target[sid] = _per_from_ctx(ctx)
        return preview

    if kind == "shotgun":
        tid = preview.target_token_id
        ptok = tokens.placements.get(tid) if tid else None
        if ptok and ammo:
            radius = CombatSimulator.get_shotgun_pattern_radius(ammo, preview.range_hexes)
            if radius is None:
                radius = 1.0
            secs = tokens_in_pattern(
                ptok.q,
                ptok.r,
                float(radius),
                tokens,
                map_state,
                shooter=shooter,
                exclude_ids={tid},
                layer_id=ptok.layer_id or "",
            )
            preview.target_token_ids = [tid]
            preview.secondary_by_primary = {tid: secs}
            for sid in [tid] + secs:
                stok = tokens.placements.get(sid)
                if not stok:
                    continue
                ctx = build_map_shot_context(
                    shooter,
                    _rt(runtime, shooter.token_id),
                    stok,
                    _rt(runtime, sid),
                    map_state,
                )
                preview.per_target[sid] = _per_from_ctx(ctx)
        else:
            preview.target_token_ids = [preview.target_token_id] if preview.target_token_id else []
        return preview

    # single / 3rb
    preview.target_token_ids = [preview.target_token_id] if preview.target_token_id else []
    if preview.target_token_id and preview.target_token_id not in preview.per_target:
        preview.per_target[preview.target_token_id] = {
            "range_hexes": preview.range_hexes,
            "exposure": preview.selected_exposure or preview.exposure,
            "orientation": preview.orientation,
            "is_front": preview.is_front,
            "visible_exposures": list(preview.visible_exposures),
            "los_clear": True,
            "notes": list(preview.notes),
        }
    return preview


def _enum_or(enum_cls, name: str, default):
    try:
        return enum_cls[name]
    except KeyError:
        return default


def _shot_params_from_preview(
    preview: PendingShotPreview,
    per: dict | None = None,
    *,
    intervening_barriers: list | None = None,
    shooter_stance: str = "standing",
    target_stance: str = "standing",
) -> ShotParameters:
    per = per or {}
    stance = [
        _enum_or(SituationStanceModifier4B, n, None)
        for n in preview.stance_mods
    ]
    stance = [s for s in stance if s is not None] or [SituationStanceModifier4B.STANDING]
    vis = [
        _enum_or(VisibilityModifier4C, n, None)
        for n in preview.visibility_mods
    ]
    vis = [v for v in vis if v is not None] or [VisibilityModifier4C.GOOD_VISIBILITY]
    orient_name = per.get("orientation", preview.orientation)
    customs = []
    for entry in preview.custom_eal_modifiers:
        if isinstance(entry, dict):
            customs.append((entry.get("label", "custom"), int(entry.get("alm", 0))))
        elif isinstance(entry, (list, tuple)) and len(entry) >= 2:
            customs.append((entry[0], int(entry[1])))
    cover_pf = float(preview.manual_cover_pf) if preview.manual_cover_pf is not None else 0.0
    return ShotParameters(
        aim_time_ac=preview.aim_time_ac,
        situation_stance_modifiers=stance,
        visibility_modifiers=vis,
        target_orientation=_enum_or(
            TargetOrientation, orient_name, TargetOrientation.FRONT_REAR
        ),
        shooter_speed_hex_per_impulse=preview.shooter_speed,
        target_speed_hex_per_impulse=preview.target_speed,
        custom_eal_modifiers=customs,
        cover_pf=cover_pf,
        intervening_barriers=intervening_barriers,
        shooter_stance=shooter_stance,
        target_stance=target_stance,
    )


def _barriers_for_pair(
    map_state,
    shooter_tok,
    target_tok,
):
    if not map_state or not shooter_tok or not target_tok:
        return None
    from phoenix_command.simulations.map_cover import gather_barrier_crossings
    crossings = gather_barrier_crossings(map_state, shooter_tok, target_tok)
    return crossings or None


def _params_for_target(
    preview: PendingShotPreview,
    per: dict | None,
    *,
    map_state=None,
    shooter_tok=None,
    target_tok=None,
    token_runtime: dict | None = None,
) -> ShotParameters:
    runtime = token_runtime or {}
    s_rt = runtime.get(preview.shooter_token_id)
    t_id = (target_tok.token_id if target_tok else None) or preview.target_token_id
    t_rt = runtime.get(t_id) if t_id else None
    return _shot_params_from_preview(
        preview,
        per,
        intervening_barriers=_barriers_for_pair(map_state, shooter_tok, target_tok),
        shooter_stance=getattr(s_rt, "stance", "standing") if s_rt else "standing",
        target_stance=getattr(t_rt, "stance", "standing") if t_rt else "standing",
    )


def _exposure_from(per: dict, preview: PendingShotPreview) -> TargetExposure:
    name = per.get("exposure") or preview.selected_exposure or preview.exposure
    return _enum_or(TargetExposure, name, TargetExposure.STANDING_EXPOSED)


def build_snapshot(preview: PendingShotPreview, shooter_name: str, target_names: dict[str, str]) -> dict:
    """Serialize fire params for TOF resolve."""
    return {
        "kind": preview.fire_kind or infer_fire_kind(preview.fire_mode, None, None),
        "range_hexes": preview.range_hexes,
        "exposure": preview.selected_exposure or preview.exposure,
        "is_front": preview.is_front,
        "weapon_name": preview.weapon_name,
        "ammo_name": preview.ammo_name,
        "fire_mode": preview.fire_mode,
        "fire_kind": preview.fire_kind,
        "target_token_ids": list(preview.primary_ids()),
        "secondary_by_primary": {
            k: list(v) for k, v in preview.secondary_by_primary.items()
        },
        "aim_q": preview.aim_q,
        "aim_r": preview.aim_r,
        "aim_layer_id": preview.aim_layer_id,
        "arc_of_fire": preview.arc_of_fire,
        "continuous_burst_impulses": preview.continuous_burst_impulses,
        "per_target": dict(preview.per_target),
        "shot_params": {
            "aim_time_ac": preview.aim_time_ac,
            "stance": list(preview.stance_mods),
            "visibility": list(preview.visibility_mods),
            "orientation": preview.orientation,
            "shooter_speed": preview.shooter_speed,
            "target_speed": preview.target_speed,
            "custom_eal": list(preview.custom_eal_modifiers),
            "manual_cover_pf": preview.manual_cover_pf,
        },
        "shooter_name": shooter_name,
        "target_name": target_names.get(preview.target_token_id, ""),
        "target_names": target_names,
    }


def preview_from_snapshot(snap: dict, shooter_token_id: str, target_token_id: str) -> PendingShotPreview:
    """Rebuild a minimal preview from TOF snapshot."""
    return PendingShotPreview(
        preview_id="tof",
        shooter_token_id=shooter_token_id,
        target_token_id=target_token_id or (snap.get("target_token_ids") or [""])[0],
        proposed_by="tof",
        status="confirmed",
        range_hexes=int(snap.get("range_hexes", 1)),
        exposure=snap.get("exposure", "STANDING_EXPOSED"),
        orientation=snap.get("shot_params", {}).get("orientation", "FRONT_REAR"),
        stance_mods=list(snap.get("shot_params", {}).get("stance", [])),
        visibility_mods=list(snap.get("shot_params", {}).get("visibility", [])),
        custom_eal_modifiers=list(snap.get("shot_params", {}).get("custom_eal", [])),
        aim_time_ac=int(snap.get("shot_params", {}).get("aim_time_ac", 2)),
        fire_mode=snap.get("fire_mode", "single"),
        weapon_name=snap.get("weapon_name", ""),
        ammo_name=snap.get("ammo_name", ""),
        selected_exposure=snap.get("exposure", "STANDING_EXPOSED"),
        shooter_speed=float(snap.get("shot_params", {}).get("shooter_speed", 0)),
        target_speed=float(snap.get("shot_params", {}).get("target_speed", 0)),
        is_front=bool(snap.get("is_front", True)),
        target_token_ids=list(snap.get("target_token_ids", [])),
        secondary_by_primary={
            k: list(v) for k, v in snap.get("secondary_by_primary", {}).items()
        },
        aim_q=snap.get("aim_q"),
        aim_r=snap.get("aim_r"),
        aim_layer_id=snap.get("aim_layer_id", ""),
        arc_of_fire=snap.get("arc_of_fire"),
        continuous_burst_impulses=int(snap.get("continuous_burst_impulses", 0)),
        per_target=dict(snap.get("per_target", {})),
        fire_kind=snap.get("fire_kind") or snap.get("kind", "single"),
        manual_cover_pf=(
            float(mcp)
            if (mcp := snap.get("shot_params", {}).get("manual_cover_pf")) is not None
            else None
        ),
    )


def _chars_for_ids(
    ids: list[str],
    tokens: TokenState,
    characters: dict[str, Character],
) -> tuple[list[Character], list[str], list[str]]:
    """Return (characters, token_ids kept, missing messages)."""
    chars: list[Character] = []
    kept: list[str] = []
    missing: list[str] = []
    for tid in ids:
        tok = tokens.placements.get(tid)
        if not tok or not tok.character_name:
            missing.append(f"token {tid} gone")
            continue
        ch = characters.get(tok.character_name)
        if not ch:
            missing.append(f"character for {tid} missing")
            continue
        chars.append(ch)
        kept.append(tid)
    return chars, kept, missing


def filter_ids_by_los(
    shooter_tok: TokenPlacement,
    token_ids: list[str],
    tokens: TokenState,
    map_state: MapState | None,
    token_runtime: dict,
) -> tuple[list[str], list[str]]:
    """Return (clear_ids, blocked_ids)."""
    clear, blocked = [], []
    for tid in token_ids:
        tok = tokens.placements.get(tid)
        if not tok:
            blocked.append(tid)
            continue
        los = check_los(map_state, shooter_tok, tok, token_runtime.get(tid))
        if los.blocked:
            blocked.append(tid)
        else:
            clear.append(tid)
    return clear, blocked


def dispatch_map_fire(
    preview: PendingShotPreview,
    shooter: Character,
    weapon: Weapon | Grenade,
    ammo: AmmoType | Grenade,
    tokens: TokenState,
    characters: dict[str, Character],
    map_state: MapState | None = None,
    token_runtime: dict | None = None,
    skip_los_filter: bool = False,
) -> MapFireOutcome:
    """Route preview to the correct CombatSimulator method."""
    runtime = token_runtime or {}
    kind = infer_fire_kind(preview.fire_mode, weapon, ammo)
    preview.fire_kind = kind
    shooter_tok = tokens.placements.get(preview.shooter_token_id)
    outcome = MapFireOutcome(kind=kind)

    if kind in ("grenade", "agl", "explosive"):
        return _dispatch_explosive(
            preview, shooter, weapon, ammo, tokens, characters, map_state, outcome
        )

    primary_ids = preview.primary_ids()
    if not primary_ids:
        outcome.miss_reasons.append("no targets")
        return outcome

    if not skip_los_filter and shooter_tok:
        clear, blocked = filter_ids_by_los(
            shooter_tok, primary_ids, tokens, map_state, runtime
        )
        for tid in blocked:
            name = (tokens.placements.get(tid) or TokenPlacement(token_id=tid)).character_name or tid
            outcome.miss_reasons.append(f"no LOS → {name}")
        primary_ids = clear

    if not primary_ids:
        return outcome

    if kind == "burst":
        tg = _build_target_group(
            primary_ids, preview, tokens, characters, map_state, shooter_tok, runtime
        )
        if not tg:
            outcome.miss_reasons.append("no valid burst targets")
            return outcome
        outcome.shot_results = CombatSimulator.burst_fire(
            shooter,
            weapon,
            ammo,
            tg,
            arc_of_fire=preview.arc_of_fire,
            continuous_burst_impulses=preview.continuous_burst_impulses,
        )
        return outcome

    if kind == "3rb":
        tid = primary_ids[0]
        chars, kept, miss = _chars_for_ids([tid], tokens, characters)
        outcome.miss_reasons.extend(miss)
        if not chars:
            return outcome
        per = preview.per_target.get(tid, {})
        params = _params_for_target(
            preview,
            per,
            map_state=map_state,
            shooter_tok=shooter_tok,
            target_tok=tokens.placements.get(tid),
            token_runtime=runtime,
        )
        outcome.shot_results = CombatSimulator.three_round_burst(
            shooter,
            chars[0],
            weapon,
            ammo,
            int(per.get("range_hexes", preview.range_hexes)),
            _exposure_from(per, preview),
            params,
            bool(per.get("is_front", preview.is_front)),
        )
        return outcome

    if kind == "shotgun":
        tid = primary_ids[0]
        sec_ids = list(preview.secondary_by_primary.get(tid, []))
        if shooter_tok and not skip_los_filter:
            sec_clear, sec_blocked = filter_ids_by_los(
                shooter_tok, sec_ids, tokens, map_state, runtime
            )
            for sid in sec_blocked:
                sn = (tokens.placements.get(sid) or TokenPlacement(token_id=sid)).character_name or sid
                outcome.miss_reasons.append(f"no LOS (pattern) → {sn}")
            sec_ids = sec_clear
        all_ids = [tid] + [s for s in sec_ids if s != tid]
        chars, kept, miss = _chars_for_ids(all_ids, tokens, characters)
        outcome.miss_reasons.extend(miss)
        if not chars:
            return outcome
        ranges, exposures, params_list, fronts = [], [], [], []
        for kid in kept:
            per = preview.per_target.get(kid, {})
            ranges.append(int(per.get("range_hexes", preview.range_hexes)))
            exposures.append(_exposure_from(per, preview))
            params_list.append(
                _params_for_target(
                    preview,
                    per,
                    map_state=map_state,
                    shooter_tok=shooter_tok,
                    target_tok=tokens.placements.get(kid),
                    token_runtime=runtime,
                )
            )
            fronts.append(bool(per.get("is_front", preview.is_front)))
        outcome.shot_results = CombatSimulator.shotgun_shot(
            shooter, chars, weapon, ammo, ranges, exposures, params_list, fronts, 0
        )
        return outcome

    if kind == "shotgun_burst":
        primary_chars, kept_primary, miss = _chars_for_ids(primary_ids, tokens, characters)
        outcome.miss_reasons.extend(miss)
        if not primary_chars:
            return outcome
        primary_group = _build_target_group(
            kept_primary, preview, tokens, characters, map_state, shooter_tok, runtime
        )
        pattern_groups: list[TargetGroup] = []
        for pid in kept_primary:
            sec_ids = list(preview.secondary_by_primary.get(pid, []))
            if shooter_tok and not skip_los_filter:
                sec_ids, blocked = filter_ids_by_los(
                    shooter_tok, sec_ids, tokens, map_state, runtime
                )
                for sid in blocked:
                    sn = (tokens.placements.get(sid) or TokenPlacement(token_id=sid)).character_name or sid
                    outcome.miss_reasons.append(f"no LOS (pattern) → {sn}")
            # Pattern group excludes primary; empty TargetGroup ok with empty lists
            if sec_ids:
                pg = _build_target_group(
                    sec_ids, preview, tokens, characters, map_state, shooter_tok, runtime
                )
                pattern_groups.append(
                    pg
                    if pg
                    else TargetGroup([], [], [], [], [])
                )
            else:
                pattern_groups.append(TargetGroup([], [], [], [], []))
        outcome.shot_results = CombatSimulator.shotgun_burst_fire(
            shooter,
            weapon,
            ammo,
            primary_group,
            pattern_groups,
            arc_of_fire=preview.arc_of_fire,
            continuous_burst_impulses=preview.continuous_burst_impulses,
        )
        return outcome

    # single
    tid = primary_ids[0]
    chars, kept, miss = _chars_for_ids([tid], tokens, characters)
    outcome.miss_reasons.extend(miss)
    if not chars:
        return outcome
    per = preview.per_target.get(tid, {})
    params = _params_for_target(
        preview,
        per,
        map_state=map_state,
        shooter_tok=shooter_tok,
        target_tok=tokens.placements.get(tid),
        token_runtime=runtime,
    )
    result = CombatSimulator.single_shot(
        shooter,
        chars[0],
        weapon,
        ammo,
        int(per.get("range_hexes", preview.range_hexes)),
        _exposure_from(per, preview),
        params,
        bool(per.get("is_front", preview.is_front)),
    )
    outcome.shot_results = [result]
    return outcome


def _build_target_group(
    token_ids: list[str],
    preview: PendingShotPreview,
    tokens: TokenState,
    characters: dict[str, Character],
    map_state: MapState | None = None,
    shooter_tok: TokenPlacement | None = None,
    token_runtime: dict | None = None,
) -> TargetGroup | None:
    chars, kept, _ = _chars_for_ids(token_ids, tokens, characters)
    if not chars:
        return None
    ranges, exposures, params_list, fronts = [], [], [], []
    for tid in kept:
        per = preview.per_target.get(tid, {})
        ranges.append(int(per.get("range_hexes", preview.range_hexes)))
        exposures.append(_exposure_from(per, preview))
        params_list.append(
            _params_for_target(
                preview,
                per,
                map_state=map_state,
                shooter_tok=shooter_tok,
                target_tok=tokens.placements.get(tid),
                token_runtime=token_runtime,
            )
        )
        fronts.append(bool(per.get("is_front", preview.is_front)))
    return TargetGroup(chars, ranges, exposures, params_list, fronts)


def _dispatch_explosive(
    preview: PendingShotPreview,
    shooter: Character,
    weapon: Weapon | Grenade,
    ammo: AmmoType | Grenade,
    tokens: TokenState,
    characters: dict[str, Character],
    map_state: MapState | None,
    outcome: MapFireOutcome,
) -> MapFireOutcome:
    aim_q = preview.aim_q
    aim_r = preview.aim_r
    if aim_q is None or aim_r is None:
        outcome.miss_reasons.append("no aim hex")
        return outcome

    shooter_tok = tokens.placements.get(preview.shooter_token_id)
    mph = map_state.grid.meters_per_hex if map_state else 1.0
    if shooter_tok:
        dist_m = axial_distance(shooter_tok.q, shooter_tok.r, aim_q, aim_r) * mph
        range_hex = max(1, round(rules_hexes(dist_m)))
    else:
        range_hex = preview.range_hexes

    params = _shot_params_from_preview(preview)
    kind = preview.fire_kind

    if kind == "grenade" or isinstance(weapon, Grenade):
        expl = CombatSimulator.thrown_grenade(
            shooter,
            range_hex,
            ExplosiveTarget.HEX,
            preview.aim_time_ac,
            params.situation_stance_modifiers,
            params.visibility_modifiers,
        )
        outcome.explosive_results = [expl]
        outcome.messages.append(
            f"Grenade {'HIT' if expl.hit else f'scatter {expl.scatter_hexes}'}"
        )
    elif kind == "agl" or (
        isinstance(weapon, Weapon)
        and getattr(weapon, "weapon_type", None) == WeaponType.AUTOMATIC_GRENADE_LAUNCHER
    ):
        outcome.explosive_results = CombatSimulator.automatic_grenade_launcher_burst(
            shooter,
            weapon,
            range_hex,
            ExplosiveTarget.HEX,
            params,
            arc_of_fire=preview.arc_of_fire,
            continuous_burst_impulses=preview.continuous_burst_impulses,
        )
        hits = sum(1 for r in outcome.explosive_results if r.hit)
        outcome.messages.append(f"AGL burst: {hits}/{len(outcome.explosive_results)} direct hits")
    else:
        expl = CombatSimulator.explosive_weapon_shot(
            shooter, weapon, range_hex, ExplosiveTarget.HEX, params
        )
        outcome.explosive_results = [expl]
        outcome.messages.append(
            f"Explosive {'HIT' if expl.hit else f'scatter {expl.scatter_hexes}'}"
        )

    # Apply explosion damage to tokens in blast if we have explosive_data and at least one placement
    explosive_ammo = ammo if getattr(ammo, "explosive_data", None) else (
        weapon if isinstance(weapon, Grenade) else ammo
    )
    if not getattr(explosive_ammo, "explosive_data", None):
        return outcome

    # Use aim hex (ignore scatter for map simplicity unless miss with scatter — still center on aim for now;
    # if all elevation failed, still resolve at aim for damage preview consistency)
    max_blast_m = max(
        (d.range_hexes * 2.0 for d in explosive_ammo.explosive_data),
        default=10.0,
    )
    victims = tokens_in_blast(
        aim_q, aim_r, max_blast_m, tokens, map_state,
        shooter=shooter_tok,
        layer_id=preview.aim_layer_id,
    )
    if not victims:
        return outcome

    targets, ranges_b, exposures, sp_list, fronts, blast_mods = [], [], [], [], [], []
    for tid, dist_m in victims:
        tok = tokens.placements.get(tid)
        if not tok or not tok.character_name:
            continue
        ch = characters.get(tok.character_name)
        if not ch:
            continue
        per = preview.per_target.get(tid, {})
        targets.append(ch)
        ranges_b.append(max(0, round(rules_hexes(dist_m))))
        exposures.append(_exposure_from(per, preview))
        sp_list.append(
            _params_for_target(
                preview,
                per,
                map_state=map_state,
                shooter_tok=shooter_tok,
                target_tok=tok,
                token_runtime=None,
            )
        )
        fronts.append(bool(per.get("is_front", True)))
        blast_mods.append([BlastModifier.IN_THE_OPEN])

    if targets:
        damage = CombatSimulator.explosion_damage(
            explosive_ammo, targets, ranges_b, exposures, sp_list, fronts, blast_mods
        )
        outcome.shot_results.extend(damage)
    return outcome
