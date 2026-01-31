"""Character list widget with drag support."""

from PyQt6.QtWidgets import QListWidget
from PyQt6.QtCore import Qt, QMimeData
from PyQt6.QtGui import QDrag


class CharacterListWidget(QListWidget):
    """List widget for characters with proper drag support."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragEnabled(True)
        self.setDefaultDropAction(Qt.DropAction.CopyAction)

    def startDrag(self, supported_actions):
        """Start drag with character name as text data."""
        item = self.currentItem()
        if item:
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setText(item.text())
            drag.setMimeData(mime_data)
            drag.exec(Qt.DropAction.CopyAction)
