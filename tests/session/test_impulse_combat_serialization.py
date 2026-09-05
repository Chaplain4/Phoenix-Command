"""Serialization tests for impulse combat domain."""

from phoenix_command.session.domains.impulse_combat_state import ImpulseCombatState, TokenCombatRuntime
from phoenix_command.session.domains.player_info import PlayerInfo
from phoenix_command.session.domains.session_meta import SessionMeta
from phoenix_command.session.domains.token_state import TokenPlacement
from phoenix_command.session.domains.map_state import HexCondition, MapLayer
from phoenix_command.session.game_state import GameState


def test_impulse_combat_round_trip() -> None:
    ic = ImpulseCombatState(
        map_mode="combat",
        phase=2,
        impulse=1,
        sides={"alpha": "Alpha"},
        token_runtime={
            "t1": TokenCombatRuntime(
                ac_remaining=1.5,
                braced=True,
                balance_ac_owed=2.0,
                knockdown_phase="grounded",
                hands_free=False,
                recoil_ac_owed=1.0,
                last_shot_q=3,
                last_shot_r=4,
                last_shot_layer_id="ground",
                firing_stance_held=True,
            )
        },
        selected_token_id="t1",
    )
    restored = ImpulseCombatState.from_dict(ic.to_dict())
    assert restored.map_mode == "combat"
    assert restored.phase == 2
    assert restored.token_runtime["t1"].ac_remaining == 1.5
    assert restored.token_runtime["t1"].braced is True
    rt = restored.token_runtime["t1"]
    assert rt.balance_ac_owed == 2.0
    assert rt.knockdown_phase == "grounded"
    assert rt.hands_free is False
    assert rt.recoil_ac_owed == 1.0
    assert rt.last_shot_q == 3
    assert rt.last_shot_r == 4
    assert rt.last_shot_layer_id == "ground"
    assert rt.firing_stance_held is True


def _kd_runtime() -> TokenCombatRuntime:
    return TokenCombatRuntime(
        ac_remaining=1.5,
        braced=True,
        balance_ac_owed=2.0,
        knockdown_phase="grounded",
        hands_free=False,
        recoil_ac_owed=1.0,
        last_shot_q=3,
        last_shot_r=4,
        last_shot_layer_id="ground",
        firing_stance_held=True,
    )


def test_token_runtime_json_round_trip() -> None:
    import json

    raw = json.loads(json.dumps(_kd_runtime().to_dict()))
    rt = TokenCombatRuntime.from_dict(raw)
    assert rt.last_shot_q == 3
    assert rt.last_shot_r == 4
    assert rt.knockdown_phase == "grounded"
    assert rt.hands_free is False
    assert rt.recoil_ac_owed == 1.0
    assert rt.firing_stance_held is True
    assert rt.impulse_burst_used is False
    assert rt.held_grenade_name is None
    assert rt.grenade_armed is False


def test_token_runtime_wound_fields_round_trip() -> None:
    rt = TokenCombatRuntime(
        incap_effect="Dazed",
        incap_remaining_phases=5,
        wound_ca_penalty=2.0,
        healing_days=41.0,
        medical_aid="First Aid",
        wound_onset_abs_impulse=3,
        ctp_deadline_abs_impulse=40,
        recovery_rr=66,
        ctp_resolved=False,
        is_dead=False,
        disabled_arm_left=True,
        disabled_leg=True,
        dazed_wait_impulses=1,
    )
    restored = TokenCombatRuntime.from_dict(rt.to_dict())
    assert restored.incap_effect == "Dazed"
    assert restored.incap_remaining_phases == 5
    assert restored.wound_ca_penalty == 2.0
    assert restored.healing_days == 41.0
    assert restored.medical_aid == "First Aid"
    assert restored.wound_onset_abs_impulse == 3
    assert restored.ctp_deadline_abs_impulse == 40
    assert restored.recovery_rr == 66
    assert restored.disabled_arm_left is True
    assert restored.disabled_leg is True
    assert restored.dazed_wait_impulses == 1
    label = restored.status_label()
    assert "Dazed" in label
    assert "CTP@" in label


def test_pending_grenade_explosion_round_trip() -> None:
    from phoenix_command.session.domains.impulse_combat_state import PendingGrenadeExplosion

    expl = PendingGrenadeExplosion(
        explosion_id="e1",
        resolve_phase=2,
        resolve_impulse=1,
        shooter_token_id="t1",
        preview_snapshot={"preview_id": "p"},
        explosive_results=[{"hit": True, "eal": 5, "odds": 50, "roll": 10}],
        weapon_name="G",
        ammo_name="G",
    )
    ic = ImpulseCombatState(map_mode="combat")
    ic.pending_grenade_explosions.append(expl)
    restored = ImpulseCombatState.from_dict(ic.to_dict())
    assert len(restored.pending_grenade_explosions) == 1
    assert restored.pending_grenade_explosions[0].resolve_phase == 2


def test_token_runtime_legacy_defaults() -> None:
    rt = TokenCombatRuntime.from_dict({"ac_remaining": 2})
    assert rt.knockdown_phase == "none"
    assert rt.hands_free is True
    assert rt.balance_ac_owed == 0.0
    assert rt.recoil_ac_owed == 0.0
    assert rt.last_shot_q is None
    assert rt.last_shot_r is None
    assert rt.last_shot_layer_id == ""
    assert rt.firing_stance_held is False
    assert rt.impulse_burst_used is False
    assert rt.held_grenade_name is None
    assert rt.grenade_armed is False


def test_game_state_json_round_trip_kd_runtime() -> None:
    from phoenix_command.session.serialization import (
        game_state_from_json,
        game_state_to_json,
    )

    state = GameState()
    state.impulse_combat.map_mode = "combat"
    state.impulse_combat.token_runtime["t1"] = _kd_runtime()
    restored = game_state_from_json(game_state_to_json(state))
    rt = restored.impulse_combat.token_runtime["t1"]
    assert restored.impulse_combat.map_mode == "combat"
    assert rt.last_shot_r == 4
    assert rt.recoil_ac_owed == 1.0
    assert rt.knockdown_phase == "grounded"


def test_full_state_sync_preserves_kd_runtime() -> None:
    from phoenix_command.session.sync_protocol import (
        apply_message_to_state,
        make_full_state_message,
    )

    state = GameState()
    state.revision = 1
    state.impulse_combat.token_runtime["t1"] = _kd_runtime()
    guest = GameState()
    guest.revision = 0
    result = apply_message_to_state(guest, make_full_state_message(state))
    rt = result.impulse_combat.token_runtime["t1"]
    assert rt.recoil_ac_owed == 1.0
    assert rt.knockdown_phase == "grounded"
    assert rt.last_shot_q == 3
    assert rt.last_shot_r == 4


def test_token_side_and_control() -> None:
    tok = TokenPlacement(
        token_id="t1",
        side_id="alpha",
        controlled_by="guest-0",
    )
    data = tok.to_dict()
    restored = TokenPlacement.from_dict(data)
    assert restored.side_id == "alpha"
    assert restored.controlled_by == "guest-0"


def test_session_meta_players() -> None:
    meta = SessionMeta(
        host_name="Host",
        players=[
            PlayerInfo("host", "Host", is_host=True),
            PlayerInfo("guest-0", "Alice", is_host=False),
        ],
        connected_guests=["Alice"],
    )
    restored = SessionMeta.from_dict(meta.to_dict())
    assert len(restored.players) == 2
    assert restored.get_player("guest-0").display_name == "Alice"


def test_hex_condition_on_layer() -> None:
    layer = MapLayer()
    layer.conditions["1,2"] = HexCondition(visibility=["DUSK"], tags=["smoke"])
    data = layer.to_dict()
    restored = MapLayer.from_dict(data)
    assert restored.conditions["1,2"].visibility == ["DUSK"]


def test_game_state_includes_impulse_combat() -> None:
    state = GameState()
    state.impulse_combat.map_mode = "combat"
    restored = GameState.from_dict(state.to_dict())
    assert restored.impulse_combat.map_mode == "combat"


def test_pending_shot_preview_multi_target_in_impulse_state() -> None:
    from phoenix_command.session.domains.impulse_combat_state import PendingShotPreview

    ic = ImpulseCombatState(
        map_mode="combat",
        shot_preview=PendingShotPreview(
            preview_id="p1",
            shooter_token_id="s",
            target_token_id="t1",
            proposed_by="host",
            fire_kind="burst",
            target_token_ids=["t1", "t2"],
            aim_q=3,
            aim_r=1,
            arc_of_fire=1.5,
            per_target={"t1": {"range_hexes": 4}},
            cover_notes=["Wall PF=2.0"],
            manual_cover_pf=3.5,
            estimated_cover_pf=2.0,
        ),
    )
    restored = ImpulseCombatState.from_dict(ic.to_dict())
    assert restored.shot_preview is not None
    assert restored.shot_preview.target_token_ids == ["t1", "t2"]
    assert restored.shot_preview.aim_q == 3
    assert restored.shot_preview.arc_of_fire == 1.5
    assert restored.shot_preview.fire_kind == "burst"
    assert restored.shot_preview.cover_notes == ["Wall PF=2.0"]
    assert restored.shot_preview.manual_cover_pf == 3.5
    assert restored.shot_preview.estimated_cover_pf == 2.0


def test_pending_shot_preview_cover_defaults_for_legacy() -> None:
    from phoenix_command.session.domains.impulse_combat_state import PendingShotPreview

    p = PendingShotPreview.from_dict(
        {
            "preview_id": "x",
            "shooter_token_id": "s",
            "target_token_id": "t",
            "proposed_by": "host",
        }
    )
    assert p.cover_notes == []
    assert p.manual_cover_pf is None
    assert p.estimated_cover_pf == 0.0


def test_custom_barrier_blocks_vision_round_trip() -> None:
    from phoenix_command.session.domains.map_state import CustomBarrierMaterial, MapState

    ms = MapState()
    mat = CustomBarrierMaterial(
        id="c1", name="Plexi", protection_factor=2.0, blocks_vision=False
    )
    ms.custom_barriers[mat.id] = mat
    restored = MapState.from_dict(ms.to_dict())
    assert restored.custom_barriers["c1"].blocks_vision is False
    assert restored.custom_barriers["c1"].protection_factor == 2.0
