"""QApplication singleton and mainloop for the tkinter compatibility layer."""

from __future__ import annotations

import sys

from PyQt6.QtWidgets import QApplication

_app: QApplication | None = None


def get_app() -> QApplication:
    """Return the global QApplication instance, creating it if needed."""
    global _app
    if _app is None:
        _app = QApplication.instance()
        if _app is None:
            _app = QApplication(sys.argv)
    return _app


def mainloop() -> None:
    """Run the Qt event loop (tkinter mainloop equivalent)."""
    get_app().exec()
