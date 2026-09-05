"""Tests for GameStatePublisher debounce and single publish_now."""

import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

from phoenix_command.session.bridge import GameStateBridge
from phoenix_command.session.publisher import GameStatePublisher
from phoenix_command.session.sync_protocol import MessageType


class _FakeWindow:
    def __init__(self) -> None:
        self.characters = []
        self.combat_zone = _FakeCombatZone()
        self.character_list = _FakeList()
        self.combat_log = _FakeLog()


class _FakeCombatZone:
    def get_shooter(self):
        return None

    def get_targets(self):
        return []


class _FakeList:
    def currentRow(self):
        return -1


class _FakeLog:
    def get_log_entries(self):
        return []

    def get_detailed_lines(self):
        return []


def _qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


def test_publish_now_single_bump() -> None:
    _qapp()
    emitted: list = []
    bridge = GameStateBridge()
    assert bridge.state.revision == 0
    pub = GameStatePublisher(emitted.append, debounce_ms=50)
    window = _FakeWindow()
    pub.attach(window, bridge)

    msg = pub.publish_now()
    assert msg.type == MessageType.FULL_STATE
    assert bridge.state.revision == 1
    assert len(emitted) == 1
    assert emitted[0].revision == 1

    pub.publish_now()
    assert bridge.state.revision == 2
    assert len(emitted) == 2


def test_notify_changed_debounce() -> None:
    app = _qapp()
    emitted: list = []
    bridge = GameStateBridge()
    pub = GameStatePublisher(emitted.append, debounce_ms=40)
    pub.attach(_FakeWindow(), bridge)

    pub.notify_changed()
    pub.notify_changed()
    pub.notify_changed()
    assert emitted == []

    # Spin event loop until timer fires.
    deadline = QTimer()
    deadline.setSingleShot(True)
    done = {"ok": False}

    def _mark():
        done["ok"] = True
        app.quit()

    deadline.timeout.connect(_mark)
    deadline.start(100)
    app.exec()
    assert done["ok"]
    assert len(emitted) == 1
    assert bridge.state.revision == 1
