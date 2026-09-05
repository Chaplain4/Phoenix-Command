"""P2P session guest using WebRTC data channel."""

from __future__ import annotations

import asyncio
import logging
import threading
from typing import Callable

from PyQt6.QtCore import QThread, Qt, pyqtSignal

from phoenix_command.session.p2p_config import create_peer_connection
from phoenix_command.session.signaling_manual import decode_signaling_payload, encode_signaling_payload
from phoenix_command.session.sync_protocol import MessageType, SyncMessage, encode_message, make_player_hello
from phoenix_command.session.transport import MessageTransport

logger = logging.getLogger(__name__)


class P2PSessionGuest(QThread):
    """WebRTC guest: consumes invite, produces answer, receives GameState.

    aiortc callbacks run on the worker thread — UI work must go through signals
    with QueuedConnection (message_received / answer_ready / channel_open / etc.).

    Answerer note: aiortc may set the datachannel to ``open`` *before* emitting
    ``datachannel``, so we bootstrap immediately when ``readyState == "open"``.
    """

    answer_ready = pyqtSignal(str)
    connected = pyqtSignal()
    channel_open = pyqtSignal()
    disconnected = pyqtSignal()
    connection_failed = pyqtSignal(str)
    send_failed = pyqtSignal(str)
    message_received = pyqtSignal(object)
    ice_state_changed = pyqtSignal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._loop: asyncio.AbstractEventLoop | None = None
        self._pc = None
        self._channel = None
        self._transport = MessageTransport()
        self._on_message: Callable[[SyncMessage], None] | None = None
        self._loop_ready = threading.Event()
        self._hello_player_id: str | None = None
        self._hello_display_name: str | None = None
        self._channel_bootstrapped = False
        self._outbound_queue: list[SyncMessage] = []
        self.message_received.connect(
            self._dispatch_message, Qt.ConnectionType.QueuedConnection
        )

    def set_message_handler(self, handler: Callable[[SyncMessage], None]) -> None:
        self._on_message = handler

    def set_hello_credentials(self, player_id: str, display_name: str) -> None:
        """Store hello payload before connect so bootstrap can send immediately."""
        self._hello_player_id = player_id
        self._hello_display_name = display_name

    def _dispatch_message(self, message: SyncMessage) -> None:
        if self._on_message is not None:
            self._on_message(message)

    def run(self) -> None:
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._loop_ready.set()
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
        if not self._loop_ready.wait(timeout=5.0):
            self.connection_failed.emit("Guest event loop failed to start")
            return
        self._channel_bootstrapped = False
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
            self._on_datachannel(channel)

        await pc.setRemoteDescription(
            RTCSessionDescription(sdp=offer_sdp, type="offer")
        )
        answer = await pc.createAnswer()
        await pc.setLocalDescription(answer)
        await self._wait_ice_gathering(pc)
        code = encode_signaling_payload(pc.localDescription.sdp, "answer")
        self.answer_ready.emit(code)

    def _on_datachannel(self, channel) -> None:
        """Handle incoming host datachannel (testable without full WebRTC)."""
        self._channel = channel

        @channel.on("message")
        def on_message(message) -> None:
            if isinstance(message, str):
                data = message.encode("utf-8")
            else:
                data = message
            parsed = self._transport.unpack(data)
            if parsed is None:
                return
            self.message_received.emit(parsed)

        @channel.on("open")
        def on_open() -> None:
            self._bootstrap_channel(channel)

        # aiortc answerer: open may already have fired before datachannel event.
        if getattr(channel, "readyState", None) == "open":
            if self._loop is not None:
                self._loop.call_soon(lambda: self._bootstrap_channel(channel))
            else:
                self._bootstrap_channel(channel)

    def _bootstrap_channel(self, channel) -> None:
        """Send hello + request_state once the channel is open (idempotent)."""
        self._channel = channel
        if self._channel_bootstrapped:
            self._flush_outbound_queue()
            return
        if getattr(channel, "readyState", None) != "open":
            return
        self._channel_bootstrapped = True
        self._send_hello_on_channel()
        self._request_state()
        self._flush_outbound_queue()
        self.channel_open.emit()

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
        """Send to host; queue if channel not open yet (never silent-drop)."""
        if self._channel and getattr(self._channel, "readyState", None) == "open" and self._loop:
            data = encode_message(message)

            async def _send() -> None:
                try:
                    if self._channel and self._channel.readyState == "open":
                        self._channel.send(data.decode("utf-8"))
                    else:
                        self._outbound_queue.append(message)
                except Exception as exc:
                    logger.warning("Guest send failed: %s", exc)
                    self.send_failed.emit(str(exc))

            asyncio.run_coroutine_threadsafe(_send(), self._loop)
            return

        self._outbound_queue.append(message)
        if self._loop is None:
            logger.warning("Guest send queued (no event loop yet): %s", message.type)
        elif not self._channel:
            logger.warning("Guest send queued (no channel yet): %s", message.type)
        else:
            logger.warning(
                "Guest send queued (channel %s): %s",
                getattr(self._channel, "readyState", "?"),
                message.type,
            )

    def _flush_outbound_queue(self) -> None:
        if not self._channel or getattr(self._channel, "readyState", None) != "open":
            return
        pending = list(self._outbound_queue)
        self._outbound_queue.clear()
        for message in pending:
            try:
                self._channel.send(encode_message(message).decode("utf-8"))
            except Exception as exc:
                logger.warning("Guest queued send failed: %s", exc)
                self._outbound_queue.append(message)
                self.send_failed.emit(str(exc))
                break

    def send_player_hello(self, player_id: str, display_name: str) -> None:
        """Update credentials and send HELLO if channel is already open."""
        self.set_hello_credentials(player_id, display_name)
        if self._channel and self._channel.readyState == "open":
            if self._loop is not None:
                asyncio.run_coroutine_threadsafe(self._async_send_hello(), self._loop)
            else:
                self._send_hello_on_channel()

    def _send_hello_on_channel(self) -> None:
        """Send PLAYER_HELLO on the current thread if channel is open."""
        if not self._hello_player_id or not self._channel:
            return
        if self._channel.readyState != "open":
            return
        msg = make_player_hello(
            self._hello_player_id,
            self._hello_display_name or self._hello_player_id,
        )
        try:
            self._channel.send(encode_message(msg).decode("utf-8"))
        except Exception as exc:
            logger.exception("Failed to send PLAYER_HELLO")
            self.send_failed.emit(str(exc))

    async def _async_send_hello(self) -> None:
        self._send_hello_on_channel()

    def _request_state(self) -> None:
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
