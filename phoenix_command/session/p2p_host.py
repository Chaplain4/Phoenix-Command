"""P2P session host using WebRTC data channels."""

from __future__ import annotations

import asyncio
import logging
from typing import Callable

from PyQt6.QtCore import QThread, pyqtSignal

from phoenix_command.session.p2p_config import DATA_CHANNEL_LABEL, create_peer_connection
from phoenix_command.session.signaling_manual import decode_signaling_payload, encode_signaling_payload
from phoenix_command.session.sync_protocol import MessageType, SyncMessage
from phoenix_command.session.transport import MessageTransport

logger = logging.getLogger(__name__)


class P2PSessionHost(QThread):
    """WebRTC host: creates offer, accepts answers, broadcasts GameState."""

    invite_ready = pyqtSignal(str)
    guest_connected = pyqtSignal(str)
    guest_disconnected = pyqtSignal(str)
    connection_failed = pyqtSignal(str)
    ice_state_changed = pyqtSignal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._loop: asyncio.AbstractEventLoop | None = None
        self._peers: dict[str, object] = {}
        self._channels: dict[str, object] = {}
        self._pending_offer_sdp: str | None = None
        self._on_outbound: Callable[[SyncMessage], None] | None = None
        self._transport = MessageTransport()
        self._running = False

    def set_message_handler(self, handler: Callable[[SyncMessage], None]) -> None:
        self._on_outbound = handler

    def run(self) -> None:
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._running = True
        try:
            self._loop.run_until_complete(self._create_offer())
            self._loop.run_forever()
        except Exception as exc:
            logger.exception("P2P host failed")
            self.connection_failed.emit(str(exc))
        finally:
            self._running = False
            if self._loop and not self._loop.is_closed():
                self._loop.close()

    async def _create_offer(self) -> None:
        from aiortc import RTCSessionDescription

        pc = create_peer_connection()
        self._peers["pending"] = pc
        channel = pc.createDataChannel(DATA_CHANNEL_LABEL)
        self._wire_channel("pending", channel)

        @pc.on("iceconnectionstatechange")
        async def on_ice_state() -> None:
            self.ice_state_changed.emit(pc.iceConnectionState)

        offer = await pc.createOffer()
        await pc.setLocalDescription(offer)
        await self._wait_ice_gathering(pc)
        sdp = pc.localDescription.sdp
        self._pending_offer_sdp = sdp
        code = encode_signaling_payload(sdp, "offer")
        self.invite_ready.emit(code)

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

    def _wire_channel(self, guest_id: str, channel) -> None:
        self._channels[guest_id] = channel

        @channel.on("open")
        def on_open() -> None:
            self.guest_connected.emit(guest_id)

        @channel.on("close")
        def on_close() -> None:
            self.guest_disconnected.emit(guest_id)

        @channel.on("message")
        def on_message(message) -> None:
            if isinstance(message, str):
                data = message.encode("utf-8")
            else:
                data = message
            parsed = self._transport.unpack(data)
            if parsed and parsed.type == MessageType.REQUEST_STATE and self._on_outbound:
                self._on_outbound(parsed)

    def submit_answer(self, answer_code: str) -> None:
        if self._loop is None:
            return
        asyncio.run_coroutine_threadsafe(
            self._apply_answer(answer_code), self._loop
        )

    async def _apply_answer(self, answer_code: str) -> None:
        from aiortc import RTCSessionDescription

        payload_type, sdp = decode_signaling_payload(answer_code)
        if payload_type != "answer":
            self.connection_failed.emit("Expected answer code from guest")
            return

        pc = self._peers.get("pending")
        if pc is None:
            guest_pc = create_peer_connection()
            guest_id = f"guest-{len(self._peers)}"
            self._peers[guest_id] = guest_pc

            @guest_pc.on("datachannel")
            def on_datachannel(channel) -> None:
                self._wire_channel(guest_id, channel)

            await guest_pc.setRemoteDescription(RTCSessionDescription(sdp=sdp, type="answer"))
            return

        await pc.setRemoteDescription(RTCSessionDescription(sdp=sdp, type="answer"))
        self._peers["guest-0"] = pc
        del self._peers["pending"]

    def broadcast_message(self, message: SyncMessage) -> None:
        if self._loop is None:
            return
        asyncio.run_coroutine_threadsafe(self._send_to_all(message), self._loop)

    async def _send_to_all(self, message: SyncMessage) -> None:
        packets = self._transport.pack(message)
        for guest_id, channel in list(self._channels.items()):
            if channel.readyState != "open":
                continue
            for packet in packets:
                channel.send(packet.decode("utf-8"))

    def stop_session(self) -> None:
        if self._loop is None:
            return

        async def _close() -> None:
            for pc in self._peers.values():
                await pc.close()
            self._peers.clear()
            self._channels.clear()
            self._loop.stop()

        asyncio.run_coroutine_threadsafe(_close(), self._loop)
        self.wait(3000)
