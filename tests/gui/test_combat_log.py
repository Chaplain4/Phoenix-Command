"""Combat log serializable entries."""

from phoenix_command.gui.widgets.combat_log import CombatLogWidget
from phoenix_command.session.domains.combat_state import CombatLogEntry


def test_append_categories_and_round_trip(qapp):
    w = CombatLogWidget()
    w.append_hit("hit")
    w.append_miss("miss")
    w.append_critical("crit")
    w.append_system("sys")
    entries = w.get_log_entries()
    cats = [e.category for e in entries]
    assert cats == ["hit", "miss", "critical", "system"]
    w.append_detailed("detail line")
    detailed = w.get_detailed_lines()
    assert detailed

    w2 = CombatLogWidget()
    w2.set_log_entries(list(entries), list(detailed))
    restored = w2.get_log_entries()
    assert [e.message for e in restored] == [e.message for e in entries]
    assert w2.get_detailed_lines() == detailed

    w2.clear()
    assert w2.get_log_entries() == []
    assert w2.get_detailed_lines() == []


def test_set_log_entries_from_domain(qapp):
    w = CombatLogWidget()
    w.set_log_entries([CombatLogEntry(message="hello", category="hit")])
    assert w.get_log_entries()[0].message == "hello"


def test_html_escape_preserves_le_and_newlines(qapp):
    """insertHtml must not eat '<='; synced guest logs stay readable."""
    w = CombatLogWidget()
    msg = "Recovery Roll 8 <= 94 — survived\nsecond line"
    w.append_system(msg)
    plain = w._log_text.toPlainText()
    assert "8 <= 94" in plain
    assert "second line" in plain
    # Stored entry keeps raw text for sync.
    assert w.get_log_entries()[0].message == msg


def test_append_shot_result_summary_uses_character_name(qapp, rifle_pair):
    from types import SimpleNamespace

    from phoenix_command.gui.main_window import MainWindow

    win = MainWindow()
    target = rifle_pair[0]
    target.name = "QA Target 1"
    result = SimpleNamespace(
        hit=True,
        roll=10,
        odds=50,
        target=target,
        damage_result=None,
        incapacitation_effect=None,
        damage_source=None,
        log="[Process Hit] Target: QA Target 1, Ammo: M855\nFull dump",
    )
    win._append_shot_result(result)
    combat_msgs = [e.message for e in win.combat_log.get_log_entries()]
    assert any("QA Target 1" in m and "Hit" in m for m in combat_msgs)
    assert not any("[Process Hit]" in m for m in combat_msgs)
    detailed = "\n".join(win.combat_log.get_detailed_lines())
    assert "[Process Hit] Target: QA Target 1" in detailed
    win.close()


def test_append_shot_result_blast_and_shrapnel_labels(qapp, rifle_pair):
    from types import SimpleNamespace

    from phoenix_command.gui.main_window import MainWindow
    from phoenix_command.models.enums import AdvancedHitLocation
    from phoenix_command.models.hit_result_advanced import DamageResult

    win = MainWindow()
    target = rifle_pair[0]
    target.name = "Vic"

    blast = SimpleNamespace(
        hit=True,
        roll=0,
        odds=100,
        target=target,
        damage_result=DamageResult(
            location=AdvancedHitLocation.BLAST_DAMAGE, damage=40, shock=0
        ),
        incapacitation_effect=None,
        damage_source="blast",
        log="concussion",
    )
    win._append_shot_result(blast)
    assert any("blast: 40 damage" in e.message for e in win.combat_log.get_log_entries())

    win.combat_log.clear()
    shrap_miss = SimpleNamespace(
        hit=False,
        roll=0,
        odds=10,
        target=target,
        damage_result=None,
        incapacitation_effect=None,
        damage_source="shrapnel",
        log="No shrapnel hits",
    )
    win._append_shot_result(shrap_miss)
    assert any(e.message == "Vic - shrapnel MISS" for e in win.combat_log.get_log_entries())
    win.close()
