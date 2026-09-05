"""P2P session host using WebRTC data channels (multi-guest slots)."""

from __future__ import annotations

import asyncio
import logging
import os
import uuid
from dataclasses import dataclass, field
from typing import Callable

from PyQt6.QtCore import QThread, Qt, pyqtSignal

from phoenix_command.session.p2p_config import DATA_CHANNEL_LABEL, create_peer_connection
from phoenix_command.session.signaling_manual import decode_signaling_payload, encode_signaling_payload
from phoenix_command.session.sync_protocol import MessageType, SyncMessage
from phoenix_command.session.transport import MessageTransport

logger = logging.getLogger(__name__)


@dataclass
class PeerSlot:
    """One WebRTC peer: independent PC, channel, and chunk assembler."""

    slot_id: str
    pc: object | None = None
    channel: object | None = None
    transport: MessageTransport = field(default_factory=MessageTransport)
    player_id: str | None = None
    invite_code: str | None = None


class P2PSessionHost(QThread):
    """WebRTC host: creates per-guest offers, accepts answers, broadcasts GameState."""

    invite_ready = pyqtSignal(str, str)  # slot_id, invite_code
    guest_connected = pyqtSignal(str)  # slot_id
    guest_disconnected = pyqtSignal(str)  # slot_id
    connection_failed = pyqtSignal(str)
    ice_state_changed = pyqtSignal(str)
    # Worker → GUI: never call handler from the aiortc thread directly.
    message_received = pyqtSignal(str, object)  # slot_id, SyncMessage

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._loop: asyncio.AbstractEventLoop | None = None
        self._slots: dict[str, PeerSlot] = {}
        self._on_message: Callable[[str, SyncMessage], None] | None = None
        self._running = False
        import threading
        self._loop_ready_event = threading.Event()
        self.message_received.connect(
            self._dispatch_message, Qt.ConnectionType.QueuedConnection
        )

    def set_message_handler(self, handler: Callable[[str, SyncMessage], None]) -> None:
        self._on_message = handler

    def _dispatch_message(self, slot_id: str, message: SyncMessage) -> None:
        if self._on_message is not None:
            self._on_message(slot_id, message)

    def run(self) -> None:
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._running = True
        self._loop_ready_event.set()
        try:
            self._loop.run_until_complete(self._create_invite_async())
            self._loop.run_forever()
        except Exception as exc:
            logger.exception("P2P host failed")
            self.connection_failed.emit(str(exc))
        finally:
            self._running = False
            if self._loop and not self._loop.is_closed():
                self._loop.close()

    def create_invite(self) -> None:
        """Create an additional invite slot (first is created on start)."""
        if self._loop is None:
            return
        asyncio.run_coroutine_threadsafe(self._create_invite_async(), self._loop)

    async def _create_invite_async(self) -> str:
        slot_id = f"slot-{uuid.uuid4().hex[:8]}"
        pc = create_peer_connection()
        slot = PeerSlot(slot_id=slot_id, pc=pc)
        self._slots[slot_id] = slot

        channel = pc.createDataChannel(DATA_CHANNEL_LABEL)
        self._wire_channel(slot, channel)

        @pc.on("iceconnectionstatechange")
        async def on_ice_state() -> None:
            self.ice_state_changed.emit(pc.iceConnectionState)

        offer = await pc.createOffer()
        await pc.setLocalDescription(offer)
        await self._wait_ice_gathering(pc)
        sdp = pc.localDescription.sdp
        code = encode_signaling_payload(sdp, "offer")
        slot.invite_code = code
        self.invite_ready.emit(slot_id, code)
        return slot_id

    async def _wait_ice_gathering(self, pc) -> None:
        if pc.iceGatheringState == "complete":
            return
        complete = asyncio.Event()

        @pc.on("icegatheringstatechange")
        async def on_gathering() -> None:
            if pc.iceGatheringState == "complete":
                complete.set()

        try:
            await asyncio.wait_for(complete.wait(), timeout=10.0)
        except asyncio.TimeoutError:
            logger.warning("ICE gathering timed out; using partial candidates")

    def _wire_channel(self, slot: PeerSlot, channel) -> None:
        slot.channel = channel

        @channel.on("open")
        def on_open() -> None:
            self.guest_connected.emit(slot.slot_id)

        @channel.on("close")
        def on_close() -> None:
            self.guest_disconnected.emit(slot.slot_id)

        @channel.on("message")
        def on_message(message) -> None:
            if isinstance(message, str):
                data = message.encode("utf-8")
            else:
                data = message
            try:
                parsed = slot.transport.unpack(data)
            except Exception:
                logger.exception("Host failed to unpack guest message on %s", slot.slot_id)
                return
            if parsed is None:
                return
            if os.environ.get("PC_DEBUG_P2P") == "1":
                logger.debug("Host RX %s %s", slot.slot_id, parsed.type)
            if parsed.type in (
                MessageType.REQUEST_STATE,
                MessageType.PLAYER_HELLO,
                MessageType.PLAYER_INTENT,
            ):
                self.message_received.emit(slot.slot_id, parsed)

    def submit_answer(self, slot_id: str, answer_code: str) -> None:
        if self._loop is None:
            return
        asyncio.run_coroutine_threadsafe(
            self._apply_answer(slot_id, answer_code), self._loop
        )

    async def _apply_answer(self, slot_id: str, answer_code: str) -> None:
        from aiortc import RTCSessionDescription

        payload_type, sdp = decode_signaling_payload(answer_code)
        if payload_type != "answer":
            self.connection_failed.emit("Expected answer code from guest")
            return

        slot = self._slots.get(slot_id)
        if slot is None or slot.pc is None:
            self.connection_failed.emit(f"Unknown invite slot: {slot_id}")
            return

        await slot.pc.setRemoteDescription(
            RTCSessionDescription(sdp=sdp, type="answer")
        )

    def bind_player(self, slot_id: str, player_id: str) -> None:
        slot = self._slots.get(slot_id)
        if slot is not None:
            slot.player_id = player_id

    def player_id_for_slot(self, slot_id: str) -> str | None:
        slot = self._slots.get(slot_id)
        return slot.player_id if slot is not None else None

    def broadcast_message(self, message: SyncMessage) -> None:
        if self._loop is None:
            return
        asyncio.run_coroutine_threadsafe(self._send_to_all(message), self._loop)

    def send_to_player(self, player_id: str, message: SyncMessage) -> None:
        if self._loop is None:
            return
        asyncio.run_coroutine_threadsafe(
            self._send_to_player(player_id, message), self._loop
        )

    async def _send_to_all(self, message: SyncMessage) -> None:
        for slot in list(self._slots.values()):
            await self._send_on_slot(slot, message)

    async def _send_to_player(self, player_id: str, message: SyncMessage) -> None:
        for slot in list(self._slots.values()):
            if slot.player_id == player_id:
                await self._send_on_slot(slot, message)
                return

    async def _send_on_slot(self, slot: PeerSlot, message: SyncMessage) -> None:
        if slot.channel is None or slot.channel.readyState != "open":
            return
        packets = slot.transport.pack(message)
        for packet in packets:
            slot.channel.send(packet.decode("utf-8"))

    def stop_session(self) -> None:
        if self._loop is None:
            return

        async def _close() -> None:
            for slot in list(self._slots.values()):
                if slot.pc:
                    await slot.pc.close()
            self._slots.clear()
            self._loop.stop()

        asyncio.run_coroutine_threadsafe(_close(), self._loop)
        self.wait(3000)
