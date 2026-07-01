"""Transport helpers for sending/receiving sync messages."""

from __future__ import annotations

from phoenix_command.session.sync_protocol import (
    CHUNK_SIZE,
    ChunkAssembler,
    SyncMessage,
    chunk_payload,
    decode_message,
    encode_message,
    MessageType,
)


class MessageTransport:
    """Encode messages with optional chunking for large payloads."""

    def __init__(self) -> None:
        self._assembler = ChunkAssembler()

    def pack(self, message: SyncMessage) -> list[bytes]:
        data = encode_message(message)
        if len(data) <= CHUNK_SIZE:
            return [data]
        chunks = chunk_payload(data)
        return [encode_message(c) for c in chunks]

    def unpack(self, data: bytes) -> SyncMessage | None:
        message = decode_message(data)
        if message.type == MessageType.CHUNK:
            assembled = self._assembler.feed(message)
            if assembled is None:
                return None
            return decode_message(assembled)
        return message
