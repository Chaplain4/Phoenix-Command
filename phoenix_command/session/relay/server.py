"""Optional WebSocket relay for symmetric NAT fallback."""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Dict, Set

logger = logging.getLogger(__name__)


class RelayRoom:
    def __init__(self, room_id: str) -> None:
        self.room_id = room_id
        self.host = None
        self.guests: Set = set()


class SessionRelay:
    """Minimal room-based message relay."""

    def __init__(self) -> None:
        self.rooms: Dict[str, RelayRoom] = {}

    def _get_room(self, room_id: str) -> RelayRoom:
        if room_id not in self.rooms:
            self.rooms[room_id] = RelayRoom(room_id)
        return self.rooms[room_id]

    async def handler(self, websocket) -> None:
        room_id = None
        role = None
        try:
            async for raw in websocket:
                data = json.loads(raw)
                msg_type = data.get("type")

                if msg_type == "join":
                    room_id = data["room"]
                    role = data["role"]
                    room = self._get_room(room_id)
                    if role == "host":
                        room.host = websocket
                    else:
                        room.guests.add(websocket)
                    await websocket.send(json.dumps({"type": "joined", "room": room_id}))
                    continue

                if room_id is None:
                    continue

                room = self.rooms.get(room_id)
                if room is None:
                    continue

                if role == "host":
                    targets = list(room.guests)
                else:
                    targets = [room.host] if room.host else []

                for target in targets:
                    if target and target.open:
                        await target.send(raw)
        except Exception:
            logger.exception("Relay connection error")
        finally:
            if room_id and room_id in self.rooms:
                room = self.rooms[room_id]
                if role == "host" and room.host is websocket:
                    room.host = None
                elif websocket in room.guests:
                    room.guests.discard(websocket)
                if room.host is None and not room.guests:
                    del self.rooms[room_id]


async def main(host: str = "localhost", port: int = 8765) -> None:
    import websockets

    relay = SessionRelay()
    async with websockets.serve(relay.handler, host, port):
        logger.info("Relay listening on ws://%s:%s", host, port)
        await asyncio.Future()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
