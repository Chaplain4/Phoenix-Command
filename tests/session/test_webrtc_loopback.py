"""In-process aiortc loopback: guest uplink HELLO/REQUEST/INTENT without STUN."""

from __future__ import annotations

import asyncio

import pytest

pytest.importorskip("aiortc")
from aiortc import RTCConfiguration, RTCPeerConnection, RTCSessionDescription

from phoenix_command.session.p2p_config import DATA_CHANNEL_LABEL
from phoenix_command.session.p2p_guest import P2PSessionGuest
from phoenix_command.session.sync_protocol import (
    MessageType,
    SyncMessage,
    encode_message,
    make_player_intent,
)
from phoenix_command.session.transport import MessageTransport


async def _wait_until(pred, timeout: float = 8.0) -> None:
    loop = asyncio.get_event_loop()
    deadline = loop.time() + timeout
    while loop.time() < deadline:
        if pred():
            return
        await asyncio.sleep(0.05)
    raise TimeoutError("condition not met")


async def _run_loopback() -> list[MessageType]:
    cfg = RTCConfiguration(iceServers=[])
    host_pc = RTCPeerConnection(configuration=cfg)
    guest_pc = RTCPeerConnection(configuration=cfg)

    host_rx: list[SyncMessage] = []
    host_transport = MessageTransport()
    host_channel = host_pc.createDataChannel(DATA_CHANNEL_LABEL)

    @host_channel.on("message")
    def on_host_message(message) -> None:
        data = message.encode("utf-8") if isinstance(message, str) else message
        parsed = host_transport.unpack(data)
        if parsed is not None:
            host_rx.append(parsed)

    guest = P2PSessionGuest()
    guest.set_hello_credentials("guest-loop", "Loopback")

    @guest_pc.on("datachannel")
    def on_dc(channel) -> None:
        guest._on_datachannel(channel)

    offer = await host_pc.createOffer()
    await host_pc.setLocalDescription(offer)
    await guest_pc.setRemoteDescription(
        RTCSessionDescription(sdp=host_pc.localDescription.sdp, type="offer")
    )
    answer = await guest_pc.createAnswer()
    await guest_pc.setLocalDescription(answer)
    await host_pc.setRemoteDescription(
        RTCSessionDescription(sdp=guest_pc.localDescription.sdp, type="answer")
    )

    await _wait_until(lambda: guest._channel_bootstrapped)
    await _wait_until(
        lambda: any(m.type == MessageType.PLAYER_HELLO for m in host_rx)
        and any(m.type == MessageType.REQUEST_STATE for m in host_rx)
    )

    intent = make_player_intent(
        "guest-loop", "intent-1", "tok1", "move", {"target_q": 1, "target_r": 0}
    )
    assert guest._channel is not None
    assert guest._channel.readyState == "open"
    guest._channel.send(encode_message(intent).decode("utf-8"))

    await _wait_until(lambda: any(m.type == MessageType.PLAYER_INTENT for m in host_rx))

    await host_pc.close()
    await guest_pc.close()
    return [m.type for m in host_rx]


def test_webrtc_loopback_guest_uplink() -> None:
    """Host creates channel; guest answerer bootstraps already-open and sends HELLO+INTENT."""
    types = asyncio.run(_run_loopback())
    assert MessageType.PLAYER_HELLO in types
    assert MessageType.REQUEST_STATE in types
    assert MessageType.PLAYER_INTENT in types
