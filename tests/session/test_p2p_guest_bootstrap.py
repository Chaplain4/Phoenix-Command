"""Guest datachannel bootstrap: already-open answerer + send queue."""

from __future__ import annotations

import json

from phoenix_command.session.p2p_guest import P2PSessionGuest
from phoenix_command.session.sync_protocol import MessageType, SyncMessage, make_player_intent


class _FakeChannel:
    def __init__(self, ready_state: str = "open") -> None:
        self.readyState = ready_state
        self.sent: list[str] = []
        self._handlers: dict[str, object] = {}

    def on(self, event: str):
        def decorator(fn):
            self._handlers[event] = fn
            return fn

        return decorator

    def send(self, data: str) -> None:
        self.sent.append(data)

    def fire(self, event: str) -> None:
        handler = self._handlers.get(event)
        if handler:
            handler()


def _parsed_types(channel: _FakeChannel) -> list[str]:
    types = []
    for raw in channel.sent:
        types.append(json.loads(raw)["type"])
    return types


def test_already_open_bootstrap_sends_hello_and_request_state() -> None:
    guest = P2PSessionGuest()
    guest.set_hello_credentials("guest-abc", "Alice")
    opened: list[bool] = []
    guest.channel_open.connect(lambda: opened.append(True))

    ch = _FakeChannel("open")
    guest._on_datachannel(ch)

    assert guest._channel_bootstrapped
    assert _parsed_types(ch) == ["player_hello", "request_state"]
    assert opened == [True]
    hello = json.loads(ch.sent[0])
    assert hello["payload"]["player_id"] == "guest-abc"
    assert hello["payload"]["display_name"] == "Alice"


def test_bootstrap_without_credentials_skips_hello() -> None:
    guest = P2PSessionGuest()
    ch = _FakeChannel("open")
    guest._on_datachannel(ch)
    assert _parsed_types(ch) == ["request_state"]


def test_bootstrap_idempotent() -> None:
    guest = P2PSessionGuest()
    guest.set_hello_credentials("guest-1", "Bob")
    ch = _FakeChannel("open")
    guest._on_datachannel(ch)
    guest._bootstrap_channel(ch)
    assert _parsed_types(ch).count("player_hello") == 1
    assert _parsed_types(ch).count("request_state") == 1


def test_late_open_handler_bootstraps() -> None:
    guest = P2PSessionGuest()
    guest.set_hello_credentials("guest-2", "Carol")
    ch = _FakeChannel("connecting")
    guest._on_datachannel(ch)
    assert ch.sent == []
    assert not guest._channel_bootstrapped
    ch.readyState = "open"
    ch.fire("open")
    assert _parsed_types(ch) == ["player_hello", "request_state"]


def test_send_message_queues_until_open() -> None:
    guest = P2PSessionGuest()
    guest.set_hello_credentials("guest-q", "Queued")
    intent = make_player_intent("guest-q", "i1", "tok1", "move", {"q": 1, "r": 0})
    guest.send_message(intent)
    assert len(guest._outbound_queue) == 1
    assert intent in guest._outbound_queue

    ch = _FakeChannel("open")
    guest._on_datachannel(ch)
    types = _parsed_types(ch)
    assert types[0] == "player_hello"
    assert types[1] == "request_state"
    assert "player_intent" in types
    assert guest._outbound_queue == []


def test_credentials_then_retry_hello() -> None:
    guest = P2PSessionGuest()
    ch = _FakeChannel("open")
    guest._on_datachannel(ch)
    assert "player_hello" not in _parsed_types(ch)
    guest.send_player_hello("guest-r", "Retry")
    # Channel open but no loop — send_player_hello calls _send_hello_on_channel directly
    assert _parsed_types(ch).count("player_hello") == 1
