"""Font chooser using QFontDialog."""

from __future__ import annotations

from typing import Any

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QFontDialog, QWidget

from pyqt_utils._app import get_app


def _parent_widget(parent: Any) -> QWidget | None:
    if parent is None:
        return None
    if hasattr(parent, "_get_qt_widget"):
        return parent._get_qt_widget()
    return parent


def _qfont_to_dict(font: QFont) -> dict:
    return {
        "family": font.family(),
        "size": font.pointSize() if font.pointSize() > 0 else 12,
        "weight": "bold" if font.bold() else "normal",
        "slant": "italic" if font.italic() else "roman",
        "underline": font.underline(),
        "overstrike": font.strikeOut(),
    }


def _dict_to_qfont(font_args: dict) -> QFont:
    family = font_args.get("family", "Helvetica")
    size = int(font_args.get("size", 12))
    font = QFont(family, size)
    if font_args.get("weight") == "bold":
        font.setBold(True)
    if font_args.get("slant") == "italic":
        font.setItalic(True)
    if font_args.get("underline"):
        font.setUnderline(True)
    if font_args.get("overstrike"):
        font.setStrikeOut(True)
    return font


def askfont(master=None, text="Abcd", title="Font Chooser", **font_args) -> dict | str:
    """
    Open the font dialog and return the chosen font dict.

    Returns empty string if cancelled.
    """
    get_app()
    parent = _parent_widget(master)
    initial = _dict_to_qfont(font_args)
    ok, font = QFontDialog.getFont(initial, parent, title)
    if ok:
        return _qfont_to_dict(font)
    return ""
