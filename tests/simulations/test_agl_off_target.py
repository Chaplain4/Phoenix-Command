"""AGL burst: ROF off-target landing tests."""

from unittest.mock import patch

from phoenix_command.item_database.weapons import ags_17, m19
from phoenix_command.models.character import Character
from phoenix_command.models.enums import ExplosiveTarget, SituationStanceModifier4B
from phoenix_command.models.hit_result_advanced import ExplosiveShotResult, ShotParameters
from phoenix_command.session.domains.impulse_combat_state import PendingShotPreview
from phoenix_command.session.domains.map_state import MapState
from phoenix_command.session.domains.token_state import TokenPlacement, TokenState
from phoenix_command.simulations.combat_simulator import CombatSimulator
from phoenix_command.simulations.map_fire_dispatch import dispatch_map_fire


def _shooter() -> Character:
    return Character(
        name="Shooter",
        strength=12,
        intelligence=10,
        will=11,
        health=12,
        agility=10,
        gun_combat_skill_level=5,
    )


def _shot_params() -> ShotParameters:
    return ShotParameters(
        aim_time_ac=2,
        situation_stance_modifiers=[SituationStanceModifier4B.STANDING_AND_BRACED],
        visibility_modifiers=[],
    )


def _line_tokens() -> tuple[TokenState, TokenPlacement]:
    map_state = MapState()
    layer = map_state.ensure_default_layer()
    shooter = TokenPlacement(token_id="s", q=0, r=0, layer_id=layer.id, character_name="Shooter")
    enemy = TokenPlacement(token_id="e1", q=5, r=0, layer_id=layer.id, character_name="Enemy1")
    tokens = TokenState(placements={"s": shooter, "e1": enemy})
    return tokens, shooter


def _fake_randint_pass_elevation(a: int, b: int) -> int:
    if a == 0 and b == 99:
        return 10
    if a == 0 and b == 9:
        return 6
    return 1


def test_agl_table5a_zero_yields_rof_off_target() -> None:
    shooter = _shooter()
    with patch(
        "phoenix_command.simulations.combat_simulator.random.randint",
        side_effect=_fake_randint_pass_elevation,
    ):
        with patch(
            "phoenix_command.simulations.combat_simulator.Table5AutoPelletShrapnel.get_fire_table_value5a",
            return_value=0,
        ):
            results = CombatSimulator.automatic_grenade_launcher_burst(
                shooter,
                m19,
                40,
                ExplosiveTarget.HEX,
                _shot_params(),
            )
    assert len(results) == m19.full_auto_rof
    assert all(r.off_target for r in results)
    assert not any(r.hit for r in results)


def test_agl_table5a_one_rof_three_one_on_two_off() -> None:
    shooter = _shooter()
    with patch(
        "phoenix_command.simulations.combat_simulator.random.randint",
        side_effect=[10, 6, 5, 1, 2],
    ):
        with patch(
            "phoenix_command.simulations.combat_simulator.Table5AutoPelletShrapnel.get_fire_table_value5a",
            return_value=1,
        ):
            results = CombatSimulator.automatic_grenade_launcher_burst(
                shooter,
                m19,
                40,
                ExplosiveTarget.HEX,
                _shot_params(),
            )
    assert len(results) == 3
    on_target = [r for r in results if not r.off_target]
    off_target = [r for r in results if r.off_target]
    assert len(on_target) == 1
    assert len(off_target) == 2
    assert on_target[0].hit is True


def test_agl_ags17_table5a_capped_to_rof_one() -> None:
    """Table 5A *2 at ROF 1 → exactly 1 landing (1 on-target, 0 off-target)."""
    shooter = _shooter()
    with patch(
        "phoenix_command.simulations.combat_simulator.random.randint",
        side_effect=[10, 6, 5],
    ):
        with patch(
            "phoenix_command.simulations.combat_simulator.Table5AutoPelletShrapnel.get_fire_table_value5a",
            return_value=2,
        ):
            results = CombatSimulator.automatic_grenade_launcher_burst(
                shooter,
                ags_17,
                40,
                ExplosiveTarget.HEX,
                _shot_params(),
            )
    assert len(results) == ags_17.full_auto_rof
    assert sum(1 for r in results if r.off_target) == 0
    assert sum(1 for r in results if not r.off_target) == 1


def test_agl_total_landings_always_equals_rof() -> None:
    shooter = _shooter()
    for table_hits, weapon in ((0, m19), (1, m19), (5, m19), (2, ags_17)):
        with patch(
            "phoenix_command.simulations.combat_simulator.random.randint",
            side_effect=_fake_randint_pass_elevation,
        ):
            with patch(
                "phoenix_command.simulations.combat_simulator.Table5AutoPelletShrapnel.get_fire_table_value5a",
                return_value=table_hits,
            ):
                results = CombatSimulator.automatic_grenade_launcher_burst(
                    shooter,
                    weapon,
                    40,
                    ExplosiveTarget.HEX,
                    _shot_params(),
                )
        rof = int(weapon.full_auto_rof or 1)
        assert len(results) == rof, f"table={table_hits} weapon={weapon.name}"


def test_agl_elevation_fail_rof_off_target() -> None:
    shooter = _shooter()
    with patch(
        "phoenix_command.simulations.combat_simulator.random.randint",
        return_value=99,
    ):
        results = CombatSimulator.automatic_grenade_launcher_burst(
            shooter,
            m19,
            40,
            ExplosiveTarget.HEX,
            _shot_params(),
        )
    assert len(results) == m19.full_auto_rof
    assert all(r.elevation_failed for r in results)
    assert all(r.off_target for r in results)


def test_dispatch_agl_zero_on_target_three_landings() -> None:
    tokens, shooter_tok = _line_tokens()
    chars = {
        "Shooter": _shooter(),
        "Enemy1": Character(
            name="Enemy1",
            strength=10,
            intelligence=10,
            will=10,
            health=10,
            agility=10,
            gun_combat_skill_level=3,
        ),
    }
    map_state = MapState()
    map_state.ensure_default_layer()
    ammo = m19.ammunition_types[0]
    preview = PendingShotPreview(
        preview_id="p",
        shooter_token_id="s",
        target_token_id="e1",
        proposed_by="host",
        fire_mode="auto",
        range_hexes=40,
        aim_q=5,
        aim_r=0,
        weapon_name=m19.name,
        ammo_name=ammo.name,
    )
    off_results = [
        ExplosiveShotResult(
            hit=False,
            eal=8,
            odds=30,
            roll=10,
            scatter_hexes=1,
            off_target=True,
            arc_of_fire=0.8,
        )
        for _ in range(3)
    ]
    with patch(
        "phoenix_command.simulations.map_fire_dispatch.CombatSimulator.automatic_grenade_launcher_burst",
        return_value=off_results,
    ):
        with patch(
            "phoenix_command.simulations.map_fire_dispatch.tokens_in_blast",
            return_value=[],
        ):
            outcome = dispatch_map_fire(
                preview,
                chars["Shooter"],
                m19,
                ammo,
                tokens,
                chars,
                map_state,
                {},
                apply_blast=False,
            )
    assert len(outcome.explosive_results) == 3
    assert outcome.pending_blast is not None
    assert len(outcome.pending_blast.passes) == 3
