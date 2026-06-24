"""Font utilities for PyQt6."""

from __future__ import annotations

from typing import Any

from PyQt6.QtGui import QFont, QFontDatabase


def families() -> tuple:
    return tuple(sorted(QFontDatabase.families()))


class Font:
    def __init__(
        self,
        root: Any = None,
        font: Any = None,
        name: str | None = None,
        exists: bool = True,
        **kwargs,
    ):
        self.root = root
        self.name = name
        self.kwargs = kwargs
        if font:
            if isinstance(font, Font):
                self.kwargs = dict(font.kwargs)
            elif isinstance(font, (list, tuple)):
                self.kwargs["family"] = font[0]
                if len(font) > 1:
                    self.kwargs["size"] = int(font[1])
            elif isinstance(font, str):
                parts = font.split()
                if parts:
                    self.kwargs["family"] = parts[0]
                for p in parts[1:]:
                    if p.isdigit():
                        self.kwargs["size"] = int(p)
                    elif p == "bold":
                        self.kwargs["weight"] = "bold"
                    elif p == "italic":
                        self.kwargs["slant"] = "italic"
        for k, v in kwargs.items():
            self.kwargs[k] = v
        if "size" not in self.kwargs:
            self.kwargs["size"] = 12
        if "family" not in self.kwargs:
            self.kwargs["family"] = "Helvetica"

    def cget(self, option: str) -> Any:
        return self.kwargs.get(option)

    def config(self, **kwargs) -> None:
        self.kwargs.update(kwargs)

    def configure(self, **kwargs) -> None:
        self.config(**kwargs)

    def actual(self, displayof: Any = None) -> dict:
        return {
            "family": self.kwargs.get("family", "Helvetica"),
            "size": int(self.kwargs.get("size", 12)),
            "weight": self.kwargs.get("weight", "normal"),
            "slant": self.kwargs.get("slant", "roman"),
            "underline": bool(self.kwargs.get("underline", False)),
            "overstrike": bool(self.kwargs.get("overstrike", False)),
        }

    def to_qfont(self) -> QFont:
        actual = self.actual()
        font = QFont(actual["family"], actual["size"])
        font.setBold(actual["weight"] == "bold")
        font.setItalic(actual["slant"] == "italic")
        font.setUnderline(actual["underline"])
        font.setStrikeOut(actual["overstrike"])
        return font

    def __str__(self) -> str:
        actual = self.actual()
        parts = [actual["family"], str(actual["size"])]
        if actual["weight"] == "bold":
            parts.append("bold")
        if actual["slant"] == "italic":
            parts.append("italic")
        return " ".join(parts)
