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
