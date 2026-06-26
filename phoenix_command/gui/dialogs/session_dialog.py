"""Session host/join dialogs with Discord signaling."""

from PyQt6.QtCore import pyqtSignal
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
)
from PyQt6.QtGui import QFont


class HostSessionDialog(QDialog):
    """Host session: show invite code and accept guest answer from Discord."""

    answer_submitted = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Host Session")
        self.setMinimumSize(520, 420)
        self.invite_code = ""
        self.answer_code = ""
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        tabs = QTabWidget()

        discord_tab = QWidget()
        discord_layout = QVBoxLayout(discord_tab)

        steps = QLabel(
            "<b>Discord signaling</b><br>"
            "1. Copy the invite code below and send it in Discord.<br>"
            "2. Guest pastes it and sends you an <b>answer</b> code.<br>"
            "3. Paste the answer code below and click <b>Connect Guest</b>."
        )
        steps.setWordWrap(True)
        discord_layout.addWidget(steps)

        discord_layout.addWidget(QLabel("<b>Step 1 — Invite code (send to guest):</b>"))
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

        discord_layout.addWidget(QLabel("<b>Step 3 — Answer code (from guest):</b>"))
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

    def set_invite_code(self, code: str) -> None:
        self.invite_code = code
        self.invite_edit.setPlainText(code)
        self.status_label.setText("Invite ready — send to guest via Discord.")

    def _copy_invite(self) -> None:
        from PyQt6.QtWidgets import QApplication
        QApplication.clipboard().setText(self.invite_edit.toPlainText())
        self.status_label.setText("Invite copied to clipboard.")

    def _submit_answer(self) -> None:
        self.answer_code = self.answer_edit.toPlainText().strip()
        if not self.answer_code:
            QMessageBox.warning(self, "Missing Answer", "Paste the guest answer code from Discord.")
            return
        self.answer_submitted.emit(self.answer_code)
        self.set_status("Connecting guest...")

    def set_status(self, text: str) -> None:
        self.status_label.setText(text)


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
