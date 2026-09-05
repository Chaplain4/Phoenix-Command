"""Host-side GameState publishing with debounce (GUI-thread QTimer)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from PyQt6.QtCore import QTimer

from phoenix_command.session.game_state import GameState
from phoenix_command.session.sync_protocol import SyncMessage, make_full_state_message

if TYPE_CHECKING:
    from phoenix_command.gui.main_window import MainWindow
    from phoenix_command.session.bridge import GameStateBridge


class GameStatePublisher:
    """Captures UI state and emits sync messages to connected guests.

    Uses QTimer so capture_from_window always runs on the GUI thread.
    """

    def __init__(
        self,
        on_message: Callable[[SyncMessage], None],
        debounce_ms: int = 80,
    ) -> None:
        self._on_message = on_message
        self._debounce_ms = debounce_ms
        self._timer: QTimer | None = None
        self._bridge: GameStateBridge | None = None
        self._window: MainWindow | None = None
        self._last_revision = 0

    def attach(self, window: "MainWindow", bridge: "GameStateBridge") -> None:
        self._window = window
        self._bridge = bridge
        if self._timer is not None:
            self._timer.stop()
            self._timer.deleteLater()
        # Prefer parenting to a real QObject; fall back to unparented timer for tests.
        from PyQt6.QtCore import QObject

        parent = window if isinstance(window, QObject) else None
        self._timer = QTimer(parent)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self._publish)

    @property
    def state(self) -> GameState:
        return self._bridge.state

    def notify_changed(self, domain: str = "combat", immediate: bool = False) -> None:
        # domain kept for API compatibility; MVP always publishes full_state.
        del domain
        if self._window is None or self._timer is None:
            return
        self._timer.stop()
        if immediate:
            self._publish()
        else:
            self._timer.start(self._debounce_ms)

    def _publish(self) -> None:
        if self._window is None or self._bridge is None:
            return
        self._bridge.capture_from_window(self._window)
        self._bridge.state.bump_revision()
        self._last_revision = self._bridge.state.revision
        message = make_full_state_message(self._bridge.state)
        self._on_message(message)

    def publish_now(self) -> SyncMessage:
        """Publish immediately (e.g. on guest connect). Single bump + emit."""
        if self._timer is not None:
            self._timer.stop()
        self._publish()
        return make_full_state_message(self._bridge.state)
