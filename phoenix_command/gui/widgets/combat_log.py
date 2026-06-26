"""Combat log widget with color-coded messages and detailed log tab."""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QTextEdit
from PyQt6.QtGui import QTextCursor


class CombatLogWidget(QWidget):
    """Tabbed widget: Combat Log (color-coded events) + Detailed Log."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._log_entries: list = []
        self._detailed_lines: list[str] = []
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self._tabs = QTabWidget()

        # Tab 1 – Combat Log (normal)
        self._log_text = QTextEdit()
        self._log_text.setReadOnly(True)
        self._tabs.addTab(self._log_text, "Combat Log")

        # Tab 2 – Detailed Log
        self._detailed_text = QTextEdit()
        self._detailed_text.setReadOnly(True)
        self._tabs.addTab(self._detailed_text, "Detailed Log")

        layout.addWidget(self._tabs)

    # ── Normal log methods ────────────────────────────────────────────────

    def append_hit(self, message: str):
        """Append hit message in green."""
        self._append_colored(message, "#27ae60")

    def append_critical(self, message: str):
        """Append critical hit message in red."""
        self._append_colored(message, "#c0392b")

    def append_miss(self, message: str):
        """Append miss message in dark-yellow / orange."""
        self._append_colored(message, "#d68910")

    def append_system(self, message: str):
        """Append system message in blue."""
        self._append_colored(message, "#2471a3")

    def _append_colored(self, message: str, color: str):
        """Append message with specified color to the normal log tab."""
        category = {
            "#27ae60": "hit",
            "#c0392b": "critical",
            "#d68910": "miss",
            "#2471a3": "system",
        }.get(color, "system")
        from phoenix_command.session.domains.combat_state import CombatLogEntry
        self._log_entries.append(CombatLogEntry(message=message, category=category))
        self._log_text.moveCursor(QTextCursor.MoveOperation.End)
        self._log_text.insertHtml(f'<span style="color: {color};">{message}</span><br>')
        self._log_text.moveCursor(QTextCursor.MoveOperation.End)

    # ── Detailed log methods ──────────────────────────────────────────────

    def append_detailed(self, text: str):
        """Append a detailed log entry (plain text) with a separator."""
        if not text:
            return
        self._detailed_text.moveCursor(QTextCursor.MoveOperation.End)
        separator = "\u2500" * 60
        block = f"\n{separator}\n{text}\n"
        self._detailed_lines.append(block)
        self._detailed_text.insertPlainText(block)
        self._detailed_text.moveCursor(QTextCursor.MoveOperation.End)

    # ── Utility ───────────────────────────────────────────────────────────

    def clear(self):
        """Clear both tabs."""
        self._log_entries.clear()
        self._detailed_lines.clear()
        self._log_text.clear()
        self._detailed_text.clear()

    def get_log_entries(self):
        """Return serializable combat log entries."""
        return list(self._log_entries)

    def get_detailed_lines(self) -> list[str]:
        return list(self._detailed_lines)

    def set_log_entries(self, entries, detailed_lines: list[str] | None = None) -> None:
        """Restore log from GameState."""
        self.clear()
        color_map = {
            "hit": "#27ae60",
            "critical": "#c0392b",
            "miss": "#d68910",
            "system": "#2471a3",
        }
        for entry in entries:
            self._log_entries.append(entry)
            color = color_map.get(entry.category, "#2471a3")
            self._log_text.moveCursor(QTextCursor.MoveOperation.End)
            self._log_text.insertHtml(
                f'<span style="color: {color};">{entry.message}</span><br>'
            )
        if detailed_lines:
            for line in detailed_lines:
                self._detailed_lines.append(line)
                self._detailed_text.insertPlainText(line)

