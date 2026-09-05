"""QA defaults and env guards for session networking."""

from __future__ import annotations

import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from phoenix_command.gui.main_window import MainWindow


def test_qa_auto_hello_default_off(monkeypatch) -> None:
    monkeypatch.delenv("PC_QA_AUTO_HELLO", raising=False)
    assert MainWindow._qa_auto_hello_enabled() is False


def test_qa_auto_hello_explicit_on(monkeypatch) -> None:
    monkeypatch.setenv("PC_QA_AUTO_HELLO", "1")
    assert MainWindow._qa_auto_hello_enabled() is True


def test_qa_auto_hello_explicit_zero(monkeypatch) -> None:
    monkeypatch.setenv("PC_QA_AUTO_HELLO", "0")
    assert MainWindow._qa_auto_hello_enabled() is False
