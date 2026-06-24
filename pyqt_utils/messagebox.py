"""Message box dialogs using PyQt6."""

from __future__ import annotations

from typing import Any

from PyQt6.QtWidgets import QMessageBox, QWidget


def _parent_widget(parent: Any) -> QWidget | None:
    if parent is None:
        return None
    if hasattr(parent, "_get_qt_widget"):
        return parent._get_qt_widget()
    return parent


def showinfo(title: str, message: str, **kwargs) -> None:
    parent = _parent_widget(kwargs.get("parent"))
    QMessageBox.information(parent, title, message)


def showerror(title: str, message: str, **kwargs) -> None:
    parent = _parent_widget(kwargs.get("parent"))
    QMessageBox.critical(parent, title, message)


def showwarning(title: str, message: str, **kwargs) -> None:
    parent = _parent_widget(kwargs.get("parent"))
    QMessageBox.warning(parent, title, message)


def askokcancel(title: str, message: str, **kwargs) -> bool:
    parent = _parent_widget(kwargs.get("parent"))
    result = QMessageBox.question(
        parent,
        title,
        message,
        QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel,
    )
    return result == QMessageBox.StandardButton.Ok


def askyesno(title: str, message: str, **kwargs) -> bool:
    parent = _parent_widget(kwargs.get("parent"))
    result = QMessageBox.question(
        parent,
        title,
        message,
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
    )
    return result == QMessageBox.StandardButton.Yes
