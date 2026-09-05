"""Unit tests for multi-guest PeerSlot routing without real WebRTC."""

import asyncio

from phoenix_command.session.p2p_host import PeerSlot, P2PSessionHost
from phoenix_command.session.sync_protocol import (
    CHUNK_SIZE,
    MessageType,
    SyncMessage,
    encode_message,
    make_intent_nack,
    make_player_hello,
)
from phoenix_command.session.transport import MessageTransport


class _FakeChannel:
    def __init__(self) -> None:
        self.readyState = "open"
        self.sent: list[str] = []

    def send(self, data: str) -> None:
        self.sent.append(data)


def test_peer_slot_independent_assemblers() -> None:
    a = PeerSlot(slot_id="slot-a")
    b = PeerSlot(slot_id="slot-b")
    assert a.transport is not b.transport
    assert a.transport._assembler is not b.transport._assembler


def test_bind_player_and_send_to_player() -> None:
    host = P2PSessionHost()
    slot_a = PeerSlot(slot_id="slot-a", channel=_FakeChannel())
    slot_b = PeerSlot(slot_id="slot-b", channel=_FakeChannel())
    host._slots["slot-a"] = slot_a
    host._slots["slot-b"] = slot_b
    host.bind_player("slot-a", "guest-aaa")
    host.bind_player("slot-b", "guest-bbb")
    assert slot_a.player_id == "guest-aaa"
    assert slot_b.player_id == "guest-bbb"

    nack = make_intent_nack("i1", "nope", player_id="guest-aaa")
    asyncio.run(host._send_to_player("guest-aaa", nack))
    assert len(slot_a.channel.sent) == 1
    assert slot_b.channel.sent == []

    full = SyncMessage(type=MessageType.FULL_STATE, revision=1, payload={"x": 1})
    asyncio.run(host._send_to_all(full))
    assert len(slot_a.channel.sent) == 2
    assert len(slot_b.channel.sent) == 1


def test_intent_nack_includes_player_id() -> None:
    nack = make_intent_nack("intent-1", "rejected", player_id="guest-xyz")
    assert nack.payload["player_id"] == "guest-xyz"
    assert nack.payload["intent_id"] == "intent-1"


def test_hello_message() -> None:
    msg = make_player_hello("guest-1", "Alice")
    assert msg.type == MessageType.PLAYER_HELLO
    assert msg.payload == {"player_id": "guest-1", "display_name": "Alice"}


def test_slot_chunk_assemblers_isolated() -> None:
    """Chunks for one slot must not complete another slot's assembler."""
    big = SyncMessage(
        type=MessageType.FULL_STATE,
        revision=1,
        payload={"pad": "x" * (CHUNK_SIZE // 2), "detail": "y" * (CHUNK_SIZE // 2)},
    )
    packets = MessageTransport().pack(big)
    assert len(packets) > 1

    slot_a = PeerSlot(slot_id="a")
    slot_b = PeerSlot(slot_id="b")

    # Partial feed into A
    assert slot_a.transport.unpack(packets[0]) is None

    # Full feed into B
    out = None
    for p in packets:
        out = slot_b.transport.unpack(p)
    assert out is not None
    assert out.type == MessageType.FULL_STATE

    # A still incomplete (independent assembler)
    assert slot_a.transport.unpack(packets[0]) is None


class _WireFakeChannel:
    def __init__(self) -> None:
        self.readyState = "connecting"
        self.sent: list[str] = []
        self._handlers: dict[str, object] = {}

    def on(self, event: str):
        def decorator(fn):
            self._handlers[event] = fn
            return fn

        return decorator

    def send(self, data: str) -> None:
        self.sent.append(data)

    def deliver(self, message: SyncMessage) -> None:
        handler = self._handlers.get("message")
        assert handler is not None
        handler(encode_message(message).decode("utf-8"))


def test_host_wire_channel_emits_inbound_messages() -> None:
    host = P2PSessionHost()
    received: list[tuple[str, SyncMessage]] = []
    host.set_message_handler(lambda sid, msg: received.append((sid, msg)))
    # Bypass QueuedConnection — call dispatch directly for unit test.
    host.message_received.disconnect()
    host.message_received.connect(host._dispatch_message)

    slot = PeerSlot(slot_id="slot-rx")
    host._slots["slot-rx"] = slot
    ch = _WireFakeChannel()
    host._wire_channel(slot, ch)

    hello = make_player_hello("guest-rx", "Rx")
    ch.deliver(hello)
    assert len(received) == 1
    assert received[0][0] == "slot-rx"
    assert received[0][1].type == MessageType.PLAYER_HELLO

    req = SyncMessage(type=MessageType.REQUEST_STATE, since_revision=0)
    ch.deliver(req)
    assert received[1][1].type == MessageType.REQUEST_STATE

    intent = SyncMessage(
        type=MessageType.PLAYER_INTENT,
        payload={"player_id": "guest-rx", "action": "move", "token_id": "t1"},
    )
    ch.deliver(intent)
    assert received[2][1].type == MessageType.PLAYER_INTENT

    host.bind_player("slot-rx", "guest-rx")
    assert slot.player_id == "guest-rx"
