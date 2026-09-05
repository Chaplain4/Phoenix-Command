"""Tests for MessageTransport chunking under SCTP size limits."""

from phoenix_command.models.character import Character
from phoenix_command.session.game_state import GameState
from phoenix_command.session.serialization import character_to_dict
from phoenix_command.session.sync_protocol import (
    CHUNK_SIZE,
    MessageType,
    SyncMessage,
    chunk_payload,
    encode_message,
    make_full_state_message,
)
from phoenix_command.session.transport import MessageTransport


def _large_state_with_cyrillic() -> GameState:
    state = GameState()
    state.bump_revision()
    for i in range(12):
        char = Character(
            name=f"Боец-{i} — Alpha",
            strength=12,
            intelligence=10,
            will=10,
            health=10,
            agility=10,
            gun_combat_skill_level=4,
        )
        state.combat.characters.append(character_to_dict(char))
    # Pad combat log so the full_state exceeds CHUNK_SIZE.
    state.combat.detailed_log = [
        f"Лог выстрела {i}: попадание в грудь — урон {i * 3}" for i in range(800)
    ]
    return state


def test_chunk_size_constant_under_sctp() -> None:
    assert CHUNK_SIZE <= 32_000


def test_chunk_payload_uses_base64() -> None:
    data = b"x" * (CHUNK_SIZE + 100)
    chunks = chunk_payload(data)
    assert len(chunks) >= 2
    assert all(c.payload and c.payload.get("encoding") == "base64" for c in chunks)


def test_transport_round_trip_large_cyrillic_under_64kb() -> None:
    state = _large_state_with_cyrillic()
    msg = make_full_state_message(state)
    raw = encode_message(msg)
    assert len(raw) > CHUNK_SIZE

    transport = MessageTransport()
    packets = transport.pack(msg)
    assert len(packets) > 1
    for packet in packets:
        assert len(packet) < 65_536, f"packet {len(packet)} exceeds SCTP limit"

    assembled = None
    for packet in packets:
        assembled = transport.unpack(packet)
    assert assembled is not None
    assert assembled.type == MessageType.FULL_STATE
    assert assembled.payload is not None
    assert assembled.payload["combat"]["characters"][0]["name"].startswith("Боец")


def test_transport_small_message_no_chunk() -> None:
    transport = MessageTransport()
    msg = SyncMessage(type=MessageType.PING, revision=1)
    packets = transport.pack(msg)
    assert len(packets) == 1
    assert transport.unpack(packets[0]).type == MessageType.PING
