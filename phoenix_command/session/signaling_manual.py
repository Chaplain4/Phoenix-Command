"""Encode/decode WebRTC SDP for manual Discord signaling."""

from __future__ import annotations

import base64
import json
import zlib


def encode_signaling_payload(sdp: str, payload_type: str = "offer") -> str:
    """Compress and base64-encode SDP for pasting into Discord."""
    data = json.dumps({"type": payload_type, "sdp": sdp}).encode("utf-8")
    compressed = zlib.compress(data, level=9)
    return base64.urlsafe_b64encode(compressed).decode("ascii")


def decode_signaling_payload(code: str) -> tuple[str, str]:
    """Decode invite or answer code. Returns (payload_type, sdp)."""
    raw = base64.urlsafe_b64decode(code.strip().encode("ascii"))
    data = json.loads(zlib.decompress(raw).decode("utf-8"))
    return data["type"], data["sdp"]
