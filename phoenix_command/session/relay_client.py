"""WebSocket relay client for host and guest."""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Callable

from PyQt6.QtCore import QThread, pyqtSignal

from phoenix_command.session.sync_protocol import SyncMessage, decode_message, encode_message

logger = logging.getLogger(__name__)


class RelaySessionClient(QThread):
    """Outbound WebSocket client to relay server."""

    connected = pyqtSignal()
    disconnected = pyqtSignal()
    message_received = pyqtSignal(object)
    connection_failed = pyqtSignal(str)

    def __init__(
        self,
        relay_url: str,
        room_id: str,
        role: str,
        name: str = "",
        parent=None,
    ) -> None:
        super().__init__(parent)
        self.relay_url = relay_url
        self.room_id = room_id
        self.role = role
        self.name = name
        self._loop: asyncio.AbstractEventLoop | None = None
        self._ws = None

    def run(self) -> None:
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        try:
            self._loop.run_until_complete(self._connect())
            self._loop.run_forever()
        except Exception as exc:
            logger.exception("Relay client failed")
            self.connection_failed.emit(str(exc))
        finally:
            if self._loop and not self._loop.is_closed():
                self._loop.close()

    async def _connect(self) -> None:
        import websockets

        self._ws = await websockets.connect(self.relay_url)
        join = {
            "type": "join",
            "room": self.room_id,
            "role": self.role,
            "name": self.name,
        }
        await self._ws.send(json.dumps(join))
        await self._ws.recv()
        self.connected.emit()
        asyncio.create_task(self._listen())

    async def _listen(self) -> None:
        try:
            async for raw in self._ws:
                if isinstance(raw, bytes):
                    raw = raw.decode("utf-8")
                try:
                    data = json.loads(raw)
                    if "type" in data and data["type"] not in ("joined", "join"):
                        msg = decode_message(raw.encode("utf-8") if isinstance(raw, str) else raw)
                        self.message_received.emit(msg)
                except (json.JSONDecodeError, KeyError, ValueError):
                    msg = decode_message(raw.encode("utf-8"))
                    self.message_received.emit(msg)
        except Exception:
            self.disconnected.emit()

    def send_message(self, message: SyncMessage) -> None:
        if self._loop is None or self._ws is None:
            return
        asyncio.run_coroutine_threadsafe(self._send(message), self._loop)

    async def _send(self, message: SyncMessage) -> None:
        if self._ws and self._ws.open:
            await self._ws.send(encode_message(message).decode("utf-8"))

    def stop_session(self) -> None:
        if self._loop is None:
            return

        async def _close() -> None:
            if self._ws:
                await self._ws.close()
            self._loop.stop()

        asyncio.run_coroutine_threadsafe(_close(), self._loop)
        self.wait(3000)
