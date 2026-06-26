"""LAN session discovery via mDNS (optional)."""

from __future__ import annotations

import logging
import socket

logger = logging.getLogger(__name__)

SERVICE_TYPE = "_phoenix._tcp.local."
SERVICE_NAME = "PhoenixCommand"


def get_lan_service_name(session_id: str) -> str:
    return f"{SERVICE_NAME}-{session_id}.{SERVICE_TYPE}"


def get_local_hostname() -> str:
    return socket.gethostname()
