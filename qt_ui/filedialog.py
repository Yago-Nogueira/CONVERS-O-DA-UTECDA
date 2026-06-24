"""File dialogs using PyQt6."""

from __future__ import annotations

from typing import Any

from PyQt6.QtWidgets import QFileDialog, QWidget


def _parent_widget(parent: Any) -> QWidget | None:
    if parent is None:
        return None
    if hasattr(parent, "_get_qt_widget"):
        return parent._get_qt_widget()
    return parent


def askdirectory(**kwargs) -> str:
    parent = _parent_widget(kwargs.get("parent"))
    initialdir = kwargs.get("initialdir", "")
    title = kwargs.get("title", "")
    path = QFileDialog.getExistingDirectory(parent, title, initialdir)
    return path or ""


def askopenfilename(**kwargs) -> str:
    parent = _parent_widget(kwargs.get("parent"))
    initialdir = kwargs.get("initialdir", "")
    title = kwargs.get("title", "")
    filetypes = kwargs.get("filetypes", [])
    filter_str = ";;".join(f"{desc} ({pat})" for desc, pat in filetypes) if filetypes else "All Files (*.*)"
    path, _ = QFileDialog.getOpenFileName(parent, title, initialdir, filter_str)
    return path or ""


def asksaveasfilename(**kwargs) -> str:
    parent = _parent_widget(kwargs.get("parent"))
    initialdir = kwargs.get("initialdir", "")
    title = kwargs.get("title", "")
    defaultextension = kwargs.get("defaultextension", "")
    filetypes = kwargs.get("filetypes", [])
    filter_str = ";;".join(f"{desc} ({pat})" for desc, pat in filetypes) if filetypes else "All Files (*.*)"
    path, _ = QFileDialog.getSaveFileName(parent, title, initialdir, filter_str)
    if path and defaultextension and not path.endswith(defaultextension):
        path += defaultextension
    return path or ""
