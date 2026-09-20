"""Entry point for Phoenix Command GUI application."""

import sys
from importlib import resources
from pathlib import Path

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon, QPalette, QColor
from phoenix_command.gui.main_window import MainWindow


def _load_app_icon() -> QIcon:
    """Load the window/taskbar icon from packaged assets."""
    try:
        root = resources.files("phoenix_command.gui.assets")
        with resources.as_file(root.joinpath("app_icon.png")) as path:
            if path.is_file():
                return QIcon(str(path))
    except (FileNotFoundError, ModuleNotFoundError, TypeError, AttributeError, OSError):
        pass
    fallback = Path(__file__).resolve().parent / "phoenix_command" / "gui" / "assets" / "app_icon.png"
    if fallback.is_file():
        return QIcon(str(fallback))
    return QIcon()


def _apply_light_theme(app: QApplication):
    """Force a light Fusion theme regardless of OS settings."""
    app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(245, 245, 245))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(30, 30, 30))
    palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(233, 233, 233))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 220))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(0, 0, 0))
    palette.setColor(QPalette.ColorRole.Text, QColor(30, 30, 30))
    palette.setColor(QPalette.ColorRole.Button, QColor(240, 240, 240))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(30, 30, 30))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
    palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
    app.setPalette(palette)


def main():
    """Run the application."""
    if sys.platform == "win32":
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("PhoenixCommand.App")

    app = QApplication(sys.argv)
    app.setApplicationName("Phoenix Command")
    app.setOrganizationName("Phoenix Command")
    icon = _load_app_icon()
    if not icon.isNull():
        app.setWindowIcon(icon)
    _apply_light_theme(app)

    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
