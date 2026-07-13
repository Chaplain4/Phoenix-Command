"""P2P session guest using WebRTC data channel."""

from __future__ import annotations

import asyncio
import logging
from typing import Callable

from PyQt6.QtCore import QThread, pyqtSignal

from phoenix_command.session.p2p_config import create_peer_connection
from phoenix_command.session.signaling_manual import decode_signaling_payload, encode_signaling_payload
from phoenix_command.session.sync_protocol import MessageType, SyncMessage
from phoenix_command.session.transport import MessageTransport

logger = logging.getLogger(__name__)


class P2PSessionGuest(QThread):
    """WebRTC guest: consumes invite, produces answer, receives GameState."""

    answer_ready = pyqtSignal(str)
    connected = pyqtSignal()
    disconnected = pyqtSignal()
    connection_failed = pyqtSignal(str)
    state_received = pyqtSignal(object)
    ice_state_changed = pyqtSignal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._loop: asyncio.AbstractEventLoop | None = None
        self._pc = None
        self._channel = None
        self._transport = MessageTransport()
        self._on_message: Callable[[SyncMessage], None] | None = None

    def set_message_handler(self, handler: Callable[[SyncMessage], None]) -> None:
        self._on_message = handler

    def run(self) -> None:
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        try:
            self._loop.run_forever()
        except Exception as exc:
            logger.exception("P2P guest failed")
            self.connection_failed.emit(str(exc))
        finally:
            if self._loop and not self._loop.is_closed():
                self._loop.close()

    def connect_with_invite(self, invite_code: str) -> None:
        if self._loop is None:
            self.start()
        while self._loop is None:
            pass
        asyncio.run_coroutine_threadsafe(
            self._connect(invite_code), self._loop
        )

    async def _connect(self, invite_code: str) -> None:
        from aiortc import RTCSessionDescription

        payload_type, offer_sdp = decode_signaling_payload(invite_code)
        if payload_type != "offer":
            self.connection_failed.emit("Expected invite (offer) code from host")
            return

        pc = create_peer_connection()
        self._pc = pc

        @pc.on("iceconnectionstatechange")
        async def on_ice() -> None:
            self.ice_state_changed.emit(pc.iceConnectionState)
            if pc.iceConnectionState == "connected":
                self.connected.emit()
            elif pc.iceConnectionState in ("failed", "disconnected", "closed"):
                self.disconnected.emit()

        @pc.on("datachannel")
        def on_datachannel(channel) -> None:
            self._channel = channel

            @channel.on("open")
            def on_open() -> None:
                self._request_state()

            @channel.on("message")
            def on_message(message) -> None:
                if isinstance(message, str):
                    data = message.encode("utf-8")
                else:
                    data = message
                parsed = self._transport.unpack(data)
                if parsed is None:
                    return
                if parsed.type == MessageType.FULL_STATE:
                    self.state_received.emit(parsed)
                if self._on_message:
                    self._on_message(parsed)

        await pc.setRemoteDescription(
            RTCSessionDescription(sdp=offer_sdp, type="offer")
        )
        answer = await pc.createAnswer()
        await pc.setLocalDescription(answer)
        await self._wait_ice_gathering(pc)
        code = encode_signaling_payload(pc.localDescription.sdp, "answer")
        self.answer_ready.emit(code)

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
            logger.warning("ICE gathering timed out")

    def send_message(self, message: SyncMessage) -> None:
        """Send a message to the host over the data channel."""
        if self._loop is None or not self._channel:
            return
        from phoenix_command.session.sync_protocol import encode_message

        data = encode_message(message)

        async def _send() -> None:
            if self._channel and self._channel.readyState == "open":
                self._channel.send(data.decode("utf-8"))

        asyncio.run_coroutine_threadsafe(_send(), self._loop)

    def send_player_hello(self, player_id: str, display_name: str) -> None:
        from phoenix_command.session.sync_protocol import make_player_hello

        self.send_message(make_player_hello(player_id, display_name))

    def _request_state(self) -> None:
        from phoenix_command.session.sync_protocol import SyncMessage, MessageType, encode_message

        if self._channel and self._channel.readyState == "open":
            msg = SyncMessage(type=MessageType.REQUEST_STATE, since_revision=0)
            self._channel.send(encode_message(msg).decode("utf-8"))

    def stop_session(self) -> None:
        if self._loop is None:
            return

        async def _close() -> None:
            if self._pc:
                await self._pc.close()
            self._loop.stop()

        asyncio.run_coroutine_threadsafe(_close(), self._loop)
        self.wait(3000)
