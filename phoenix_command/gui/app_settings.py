"""Persistent desktop preferences (QSettings)."""

from __future__ import annotations

from PyQt6.QtCore import QSettings

ORG = "PhoenixCommand"
APP = "PhoenixCommand"
KEY_SHOW_BLAST_REVIEW = "combat/show_blast_modifier_dialog"


def _settings() -> QSettings:
    return QSettings(ORG, APP)


def get_show_blast_modifier_dialog() -> bool:
    val = _settings().value(KEY_SHOW_BLAST_REVIEW, True)
    if isinstance(val, bool):
        return val
    if isinstance(val, str):
        return val.lower() not in ("0", "false", "no")
    return bool(val)


def set_show_blast_modifier_dialog(enabled: bool) -> None:
    s = _settings()
    s.setValue(KEY_SHOW_BLAST_REVIEW, bool(enabled))
    s.sync()
