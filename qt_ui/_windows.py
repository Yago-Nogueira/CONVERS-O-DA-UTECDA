"""Tk and Toplevel window classes."""

from __future__ import annotations

from typing import Any

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QMenuBar, QVBoxLayout, QWidget

from ._app import get_app
from ._base import BaseWidget
from ._widgets import Frame


class Tk(BaseWidget):
    """Root window backed by QMainWindow."""

    def __init__(self, master: Any = None, **kwargs):
        get_app()
        self._init_base(None)
        self._qt = QMainWindow()
        self._central = QWidget()
        self._qt.setCentralWidget(self._central)
        self._pack_entries: list = []
        self._pack_root = None
        self._grid_layout = None
        self._grid_items = {}
        self._children: list = []
        self._menu_bar: QMenuBar | None = None
        for key, value in kwargs.items():
            self.config(**{key: value})

    def _get_qt_widget(self) -> QMainWindow:
        return self._qt

    def _get_layout_container(self) -> QWidget:
        return self._central

    @property
    def master(self):
        return None

    def mainloop(self) -> None:
        from ._app import mainloop

        mainloop()

    def config(self, cnf: str | None = None, **kwargs):
        if cnf is not None and not kwargs:
            return self.cget(cnf)
        if "menu" in kwargs:
            self._set_menu(kwargs.pop("menu"))
        for key, value in kwargs.items():
            self._apply_option(key, value)
        return None

    def _set_menu(self, menu) -> None:
        self._menu = menu
        if menu is not None:
            self._qt.setMenuBar(menu._get_qt_widget())

    def _apply_option(self, key: str, value: Any) -> None:
        if key == "bg":
            self._apply_bg_fg(self._central, bg=value)
        elif key == "background":
            self._apply_bg_fg(self._central, bg=value)
        else:
            super()._apply_option(key, value)


class Toplevel(BaseWidget):
    """Secondary window backed by a top-level QWidget."""

    def __init__(self, master: Any = None, **kwargs):
        get_app()
        self._init_base(master)
        self._qt = QWidget(None, Qt.WindowType.Window)
        if master is not None:
            self._qt.setWindowModality(Qt.WindowModality.WindowModal)
        for key, value in kwargs.items():
            self.config(**{key: value})

    def _get_qt_widget(self) -> QWidget:
        return self._qt

    def _apply_option(self, key: str, value: Any) -> None:
        if key == "bg":
            self._apply_bg_fg(self._qt, bg=value)
        elif key == "background":
            self._apply_bg_fg(self._qt, bg=value)
        else:
            super()._apply_option(key, value)
