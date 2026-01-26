"""Entry point for Phoenix Command GUI application."""

import sys
from PyQt6.QtWidgets import QApplication
from phoenix_command.gui.main_window import MainWindow


def main():
    """Run the application."""
    app = QApplication(sys.argv)
    app.setApplicationName("Phoenix Command")
    app.setOrganizationName("Phoenix Command")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
