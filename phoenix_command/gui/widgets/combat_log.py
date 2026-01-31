"""Combat log widget with color-coded messages."""

from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtGui import QTextCursor


class CombatLogWidget(QTextEdit):
    """Text widget for displaying combat events with color coding."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setMaximumHeight(150)
    
    def append_hit(self, message: str):
        """Append hit message in green."""
        self._append_colored(message, "#2ecc71")
    
    def append_critical(self, message: str):
        """Append critical hit message in red."""
        self._append_colored(message, "#e74c3c")
    
    def append_miss(self, message: str):
        """Append miss message in yellow."""
        self._append_colored(message, "#f39c12")
    
    def append_system(self, message: str):
        """Append system message in blue."""
        self._append_colored(message, "#3498db")
    
    def _append_colored(self, message: str, color: str):
        """Append message with specified color."""
        self.moveCursor(QTextCursor.MoveOperation.End)
        self.insertHtml(f'<span style="color: {color};">{message}</span><br>')
        self.moveCursor(QTextCursor.MoveOperation.End)
