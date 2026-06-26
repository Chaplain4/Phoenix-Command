"""Shared WebRTC configuration for P2P sessions."""

from __future__ import annotations

from aiortc import RTCConfiguration, RTCIceServer, RTCPeerConnection

DATA_CHANNEL_LABEL = "phoenix-command-sync"

_PEER_CONFIG = RTCConfiguration(
    iceServers=[RTCIceServer(urls="stun:stun.l.google.com:19302")],
)


def create_peer_connection() -> RTCPeerConnection:
    return RTCPeerConnection(configuration=_PEER_CONFIG)
