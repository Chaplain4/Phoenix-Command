"""Host-side GameState publishing with debounce."""

from __future__ import annotations

import threading
from typing import TYPE_CHECKING, Callable

from phoenix_command.session.game_state import GameState
from phoenix_command.session.sync_protocol import SyncMessage, make_full_state_message

if TYPE_CHECKING:
    from phoenix_command.gui.main_window import MainWindow


class GameStatePublisher:
    """Captures UI state and emits sync messages to connected guests."""

    def __init__(
        self,
        on_message: Callable[[SyncMessage], None],
        debounce_ms: int = 80,
    ) -> None:
        self._on_message = on_message
        self._debounce_ms = debounce_ms
        self._timer: threading.Timer | None = None
        self._lock = threading.Lock()
        self._bridge = None
        self._window: MainWindow | None = None
        self._last_revision = 0

    def attach(self, window: "MainWindow", bridge: "GameStateBridge") -> None:
        self._window = window
        self._bridge = bridge

    @property
    def state(self) -> GameState:
        return self._bridge.state

    def notify_changed(self, domain: str = "combat", immediate: bool = False) -> None:
        if self._window is None:
            return
        with self._lock:
            if self._timer:
                self._timer.cancel()
            delay = 0.0 if immediate else self._debounce_ms / 1000.0
            self._timer = threading.Timer(delay, self._publish)
            self._timer.daemon = True
            self._timer.start()

    def _publish(self) -> None:
        if self._window is None or self._bridge is None:
            return
        self._bridge.capture_from_window(self._window)
        self._bridge.state.bump_revision()
        self._last_revision = self._bridge.state.revision
        message = make_full_state_message(self._bridge.state)
        self._on_message(message)

    def publish_now(self) -> SyncMessage:
        """Publish immediately (e.g. on guest connect)."""
        self.notify_changed(immediate=True)
        if self._timer:
            self._timer.cancel()
        self._publish()
        return make_full_state_message(self._bridge.state)
