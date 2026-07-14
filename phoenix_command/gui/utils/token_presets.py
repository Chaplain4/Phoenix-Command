"""Built-in top-down token image presets."""

from __future__ import annotations

import base64
from importlib import resources
from pathlib import Path

TOKEN_PRESETS: list[tuple[str, str]] = [
    ("assault", "Assault"),
    ("rifle", "Rifle"),
    ("smg", "SMG"),
    ("lmg", "LMG"),
    ("rpg", "RPG"),
]


def list_token_presets() -> list[tuple[str, str]]:
    """Return (preset_id, label) pairs."""
    return list(TOKEN_PRESETS)


def _fallback_path(preset_id: str) -> Path:
    return Path(__file__).resolve().parent.parent / "assets" / "tokens" / f"{preset_id}.png"


def load_preset_bytes(preset_id: str) -> bytes | None:
    filename = f"{preset_id}.png"
    try:
        root = resources.files("phoenix_command.gui.assets.tokens")
        data = root.joinpath(filename).read_bytes()
        if data:
            return data
    except (FileNotFoundError, ModuleNotFoundError, TypeError, AttributeError, OSError):
        pass
    fallback = _fallback_path(preset_id)
    if fallback.is_file():
        return fallback.read_bytes()
    return None


def load_preset_b64(preset_id: str) -> tuple[str, str]:
    """Return (base64, mime) for a preset. Raises KeyError if missing."""
    ids = {pid for pid, _ in TOKEN_PRESETS}
    if preset_id not in ids:
        raise KeyError(preset_id)
    raw = load_preset_bytes(preset_id)
    if not raw:
        raise KeyError(preset_id)
    return base64.b64encode(raw).decode("ascii"), "image/png"


def preset_pixmap_path(preset_id: str) -> str | None:
    """Filesystem path for UI thumbnails, or None."""
    fallback = _fallback_path(preset_id)
    if fallback.is_file():
        return str(fallback)
    try:
        root = resources.files("phoenix_command.gui.assets.tokens")
        with resources.as_file(root.joinpath(f"{preset_id}.png")) as path:
            if path.is_file():
                return str(path)
    except (FileNotFoundError, ModuleNotFoundError, TypeError, AttributeError, OSError):
        pass
    return None
