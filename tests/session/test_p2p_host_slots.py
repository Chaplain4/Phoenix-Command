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
