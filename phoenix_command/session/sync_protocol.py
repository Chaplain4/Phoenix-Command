"""Sync message encoding/decoding over session transport."""

from __future__ import annotations

import json
from dataclasses import dataclass
from enum import Enum
from typing import Any

from phoenix_command.session.game_state import GameState
from phoenix_command.session.patch import apply_patch
from phoenix_command.session.serialization import game_state_from_bytes, game_state_to_bytes


class MessageType(str, Enum):
    FULL_STATE = "full_state"
    DOMAIN_DELTA = "domain_delta"
    DOMAIN_FULL = "domain_full"
    REQUEST_STATE = "request_state"
    PLAYER_HELLO = "player_hello"
    PLAYER_INTENT = "player_intent"
    INTENT_NACK = "intent_nack"
    ACK = "ack"
    PING = "ping"
    PONG = "pong"
    CHUNK = "chunk"


CHUNK_SIZE = 60_000


@dataclass
class SyncMessage:
    type: MessageType
    revision: int = 0
    payload: dict | None = None
    domain: str | None = None
    patch: list[dict] | None = None
    since_revision: int = 0
    chunk_id: int | None = None
    chunk_index: int | None = None
    chunk_total: int | None = None

    def to_dict(self) -> dict:
        result: dict[str, Any] = {"type": self.type.value}
        if self.revision:
            result["revision"] = self.revision
        if self.payload is not None:
            result["payload"] = self.payload
        if self.domain is not None:
            result["domain"] = self.domain
        if self.patch is not None:
            result["patch"] = self.patch
        if self.since_revision:
            result["since_revision"] = self.since_revision
        if self.chunk_id is not None:
            result["chunk_id"] = self.chunk_id
            result["chunk_index"] = self.chunk_index
            result["chunk_total"] = self.chunk_total
        return result

    @classmethod
    def from_dict(cls, data: dict) -> "SyncMessage":
        return cls(
            type=MessageType(data["type"]),
            revision=data.get("revision", 0),
            payload=data.get("payload"),
            domain=data.get("domain"),
            patch=data.get("patch"),
            since_revision=data.get("since_revision", 0),
            chunk_id=data.get("chunk_id"),
            chunk_index=data.get("chunk_index"),
            chunk_total=data.get("chunk_total"),
        )


def encode_message(message: SyncMessage) -> bytes:
    return json.dumps(message.to_dict()).encode("utf-8")


def decode_message(data: bytes) -> SyncMessage:
    return SyncMessage.from_dict(json.loads(data.decode("utf-8")))


def make_player_hello(player_id: str, display_name: str) -> SyncMessage:
    return SyncMessage(
        type=MessageType.PLAYER_HELLO,
        payload={"player_id": player_id, "display_name": display_name},
    )


def make_player_intent(
    player_id: str,
    intent_id: str,
    token_id: str,
    action: str,
    args: dict | None = None,
) -> SyncMessage:
    return SyncMessage(
        type=MessageType.PLAYER_INTENT,
        payload={
            "player_id": player_id,
            "intent_id": intent_id,
            "token_id": token_id,
            "action": action,
            "args": args or {},
        },
    )


def make_intent_nack(intent_id: str, reason: str) -> SyncMessage:
    return SyncMessage(
        type=MessageType.INTENT_NACK,
        payload={"intent_id": intent_id, "reason": reason},
    )


def make_full_state_message(state: GameState) -> SyncMessage:
    return SyncMessage(
        type=MessageType.FULL_STATE,
        revision=state.revision,
        payload=state.to_dict(),
    )


def make_domain_delta(
    revision: int,
    domain: str,
    patch: list[dict],
) -> SyncMessage:
    return SyncMessage(
        type=MessageType.DOMAIN_DELTA,
        revision=revision,
        domain=domain,
        patch=patch,
    )


def apply_message_to_state(state: GameState, message: SyncMessage) -> GameState:
    """Apply incoming sync message; returns updated GameState."""
    if message.revision and message.revision <= state.revision:
        return state

    if message.type == MessageType.FULL_STATE and message.payload:
        return GameState.from_dict(message.payload)

    if message.type == MessageType.DOMAIN_DELTA and message.patch:
        doc = state.to_dict()
        if message.domain:
            domain_doc = {message.domain: doc.get(message.domain)}
            patched = apply_patch(domain_doc, message.patch)
            doc[message.domain] = patched[message.domain]
        else:
            doc = apply_patch(doc, message.patch)
        new_state = GameState.from_dict(doc)
        new_state.revision = message.revision
        return new_state

    if message.type == MessageType.DOMAIN_FULL and message.domain and message.payload:
        doc = state.to_dict()
        doc[message.domain] = message.payload
        new_state = GameState.from_dict(doc)
        new_state.revision = message.revision
        return new_state

    return state


def chunk_payload(data: bytes) -> list[SyncMessage]:
    """Split large payload into chunk messages."""
    if len(data) <= CHUNK_SIZE:
        return []
    import uuid

    chunk_id = hash(uuid.uuid4().hex) & 0xFFFFFFFF
    total = (len(data) + CHUNK_SIZE - 1) // CHUNK_SIZE
    messages = []
    for i in range(total):
        start = i * CHUNK_SIZE
        end = start + CHUNK_SIZE
        messages.append(
            SyncMessage(
                type=MessageType.CHUNK,
                chunk_id=chunk_id,
                chunk_index=i,
                chunk_total=total,
                payload={"data": data[start:end].decode("latin-1")},
            )
        )
    return messages


class ChunkAssembler:
    """Reassemble chunked sync payloads."""

    def __init__(self) -> None:
        self._buffers: dict[int, dict[int, bytes]] = {}
        self._totals: dict[int, int] = {}

    def feed(self, message: SyncMessage) -> bytes | None:
        if message.type != MessageType.CHUNK:
            return None
        if message.chunk_id is None or message.chunk_index is None or message.chunk_total is None:
            return None
        cid = message.chunk_id
        self._buffers.setdefault(cid, {})
        self._totals[cid] = message.chunk_total
        chunk_data = message.payload.get("data", "") if message.payload else ""
        self._buffers[cid][message.chunk_index] = chunk_data.encode("latin-1")
        if len(self._buffers[cid]) < self._totals[cid]:
            return None
        parts = [self._buffers[cid][i] for i in range(self._totals[cid])]
        del self._buffers[cid]
        del self._totals[cid]
        return b"".join(parts)
