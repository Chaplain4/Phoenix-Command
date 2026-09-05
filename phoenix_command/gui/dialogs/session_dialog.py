"""Session host/join dialogs with Discord signaling."""

from __future__ import annotations

from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTextEdit,
    QPushButton,
    QTabWidget,
    QWidget,
    QLineEdit,
    QMessageBox,
    QListWidget,
    QListWidgetItem,
)
from PyQt6.QtGui import QFont


class HostSessionDialog(QDialog):
    """Host session: create invite codes and accept guest answers."""

    answer_submitted = pyqtSignal(str, str)  # slot_id, answer_code
    new_invite_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Host Session")
        self.setMinimumSize(560, 480)
        self.invite_code = ""
        self.answer_code = ""
        self._slots: dict[str, dict] = {}
        self._active_slot_id: str | None = None
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        tabs = QTabWidget()

        discord_tab = QWidget()
        discord_layout = QVBoxLayout(discord_tab)

        steps = QLabel(
            "<b>Discord signaling</b><br>"
            "1. Select or create an invite slot, copy the invite code, send it in Discord.<br>"
            "2. Guest pastes it and sends you an <b>answer</b> code.<br>"
            "3. Paste the answer below and click <b>Connect Guest</b>."
        )
        steps.setWordWrap(True)
        discord_layout.addWidget(steps)

        discord_layout.addWidget(QLabel("Your display name:"))
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Host")
        discord_layout.addWidget(self.name_edit)

        discord_layout.addWidget(QLabel("<b>Guest slots:</b>"))
        self.slot_list = QListWidget()
        self.slot_list.setMaximumHeight(100)
        self.slot_list.currentItemChanged.connect(self._on_slot_selected)
        discord_layout.addWidget(self.slot_list)

        new_invite_btn = QPushButton("New Invite")
        new_invite_btn.clicked.connect(self.new_invite_requested.emit)
        discord_layout.addWidget(new_invite_btn)

        discord_layout.addWidget(QLabel("<b>Invite code (send to guest):</b>"))
        self.invite_edit = QTextEdit()
        self.invite_edit.setReadOnly(True)
        self.invite_edit.setMaximumHeight(80)
        mono = QFont("Consolas")
        mono.setStyleHint(QFont.StyleHint.Monospace)
        self.invite_edit.setFont(mono)
        discord_layout.addWidget(self.invite_edit)

        copy_invite_btn = QPushButton("Copy Invite to Clipboard")
        copy_invite_btn.clicked.connect(self._copy_invite)
        discord_layout.addWidget(copy_invite_btn)

        discord_layout.addWidget(QLabel("<b>Answer code (from guest):</b>"))
        self.answer_edit = QTextEdit()
        self.answer_edit.setMaximumHeight(80)
        self.answer_edit.setFont(mono)
        discord_layout.addWidget(self.answer_edit)

        btn_row = QHBoxLayout()
        self.connect_btn = QPushButton("Connect Guest")
        self.connect_btn.clicked.connect(self._submit_answer)
        btn_row.addWidget(self.connect_btn)
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.reject)
        btn_row.addWidget(close_btn)
        discord_layout.addLayout(btn_row)

        self.status_label = QLabel("Waiting for invite code...")
        discord_layout.addWidget(self.status_label)
        tabs.addTab(discord_tab, "Discord")

        lan_tab = QWidget()
        lan_layout = QVBoxLayout(lan_tab)
        lan_layout.addWidget(
            QLabel("LAN discovery: start hosting from the main window status bar when available.")
        )
        tabs.addTab(lan_tab, "Local Network")

        layout.addWidget(tabs)

    def set_invite_code(self, code: str, slot_id: str | None = None) -> None:
        """Register or update an invite for a peer slot."""
        if slot_id is None:
            slot_id = f"slot-{len(self._slots)}"
        self._slots[slot_id] = {
            "invite": code,
            "status": "invite ready",
            "player_id": None,
        }
        self._active_slot_id = slot_id
        self._refresh_slot_list()
        self.invite_code = code
        self.invite_edit.setPlainText(code)
        self.status_label.setText(f"Invite ready ({slot_id}) — send to guest via Discord.")

    def set_slot_status(self, slot_id: str, status: str, player_id: str | None = None) -> None:
        info = self._slots.get(slot_id)
        if not info:
            return
        info["status"] = status
        if player_id is not None:
            info["player_id"] = player_id
        self._refresh_slot_list()
        if slot_id == self._active_slot_id:
            self.status_label.setText(f"{slot_id}: {status}")

    def _refresh_slot_list(self) -> None:
        current = self._active_slot_id
        self.slot_list.clear()
        for slot_id, info in self._slots.items():
            label = f"{slot_id}: {info['status']}"
            if info.get("player_id"):
                label += f" ({info['player_id']})"
            item = QListWidgetItem(label)
            item.setData(int(Qt.ItemDataRole.UserRole), slot_id)
            self.slot_list.addItem(item)
            if slot_id == current:
                self.slot_list.setCurrentItem(item)

    def _on_slot_selected(self, current: QListWidgetItem | None, _previous) -> None:
        if current is None:
            return
        slot_id = current.data(int(Qt.ItemDataRole.UserRole))
        if not slot_id or slot_id not in self._slots:
            return
        self._active_slot_id = slot_id
        self.invite_code = self._slots[slot_id]["invite"]
        self.invite_edit.setPlainText(self.invite_code)
        self.status_label.setText(f"{slot_id}: {self._slots[slot_id]['status']}")

    def _copy_invite(self) -> None:
        from PyQt6.QtWidgets import QApplication
        QApplication.clipboard().setText(self.invite_edit.toPlainText())
        self.status_label.setText("Invite copied to clipboard.")

    def _submit_answer(self) -> None:
        self.answer_code = self.answer_edit.toPlainText().strip()
        if not self.answer_code:
            QMessageBox.warning(self, "Missing Answer", "Paste the guest answer code from Discord.")
            return
        if not self._active_slot_id:
            QMessageBox.warning(self, "No Slot", "Select or create an invite slot first.")
            return
        self.answer_submitted.emit(self._active_slot_id, self.answer_code)
        self.set_status("Connecting guest...")

    def set_status(self, text: str) -> None:
        self.status_label.setText(text)

    @property
    def display_name(self) -> str:
        return self.name_edit.text().strip() or "Host"


class JoinSessionDialog(QDialog):
    """Join session: paste invite, produce answer for Discord."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Join Session")
        self.setMinimumSize(520, 400)
        self.invite_code = ""
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        steps = QLabel(
            "<b>Discord signaling</b><br>"
            "1. Paste the host's invite code from Discord.<br>"
            "2. Click <b>Connect</b> to generate your answer code.<br>"
            "3. Copy the answer and send it back to the host in Discord."
        )
        steps.setWordWrap(True)
        layout.addWidget(steps)

        layout.addWidget(QLabel("Your display name:"))
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Player")
        layout.addWidget(self.name_edit)

        layout.addWidget(QLabel("<b>Invite code (from host):</b>"))
        self.invite_edit = QTextEdit()
        self.invite_edit.setMaximumHeight(80)
        mono = QFont("Consolas")
        mono.setStyleHint(QFont.StyleHint.Monospace)
        self.invite_edit.setFont(mono)
        layout.addWidget(self.invite_edit)

        self.connect_btn = QPushButton("Connect")
        self.connect_btn.clicked.connect(self._on_connect)
        layout.addWidget(self.connect_btn)

        layout.addWidget(QLabel("<b>Answer code (send to host):</b>"))
        self.answer_edit = QTextEdit()
        self.answer_edit.setReadOnly(True)
        self.answer_edit.setMaximumHeight(80)
        self.answer_edit.setFont(mono)
        layout.addWidget(self.answer_edit)

        copy_answer_btn = QPushButton("Copy Answer to Clipboard")
        copy_answer_btn.clicked.connect(self._copy_answer)
        layout.addWidget(copy_answer_btn)

        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.reject)
        layout.addWidget(close_btn)

    def _on_connect(self) -> None:
        self.invite_code = self.invite_edit.toPlainText().strip()
        if not self.invite_code:
            QMessageBox.warning(self, "Missing Invite", "Paste the host invite code from Discord.")
            return
        self.accept()

    def set_answer_code(self, code: str) -> None:
        self.answer_edit.setPlainText(code)
        self.status_label.setText("Answer ready — send to host via Discord.")
        self.connect_btn.setEnabled(False)

    def _copy_answer(self) -> None:
        from PyQt6.QtWidgets import QApplication
        text = self.answer_edit.toPlainText()
        if text:
            QApplication.clipboard().setText(text)
            self.status_label.setText("Answer copied to clipboard.")

    @property
    def display_name(self) -> str:
        return self.name_edit.text().strip() or "Player"


class SaveLoadSessionDialog(QDialog):
    """Simple file path prompt for save/load."""

    def __init__(self, title: str, default_name: str = "session.json", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Session file:"))
        self.path_edit = QLineEdit(default_name)
        layout.addWidget(self.path_edit)
        browse = QPushButton("Browse...")
        browse.clicked.connect(self._browse)
        layout.addWidget(browse)
        row = QHBoxLayout()
        ok = QPushButton("OK")
        ok.clicked.connect(self.accept)
        cancel = QPushButton("Cancel")
        cancel.clicked.connect(self.reject)
        row.addWidget(ok)
        row.addWidget(cancel)
        layout.addLayout(row)

    def _browse(self) -> None:
        from PyQt6.QtWidgets import QFileDialog
        path, _ = QFileDialog.getSaveFileName(
            self, "Session File", self.path_edit.text(), "JSON (*.json)"
        )
        if path:
            self.path_edit.setText(path)

    @property
    def file_path(self) -> str:
        return self.path_edit.text().strip()
