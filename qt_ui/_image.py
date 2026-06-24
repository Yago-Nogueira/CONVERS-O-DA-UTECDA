"""PhotoImage compatible with tkinter and PIL images."""

from __future__ import annotations

from typing import Any

from PyQt6.QtGui import QImage, QPixmap


class PhotoImage:
    def __init__(self, master: Any = None, **kwargs):
        self.master = master
        self._pixmap = QPixmap()
        if "file" in kwargs:
            self._pixmap.load(kwargs["file"])
        elif "data" in kwargs:
            self._pixmap.loadFromData(kwargs["data"])

    @classmethod
    def from_pil(cls, master: Any, pil_image) -> "PhotoImage":
        obj = cls(master)
        if pil_image.mode != "RGBA":
            pil_image = pil_image.convert("RGBA")
        data = pil_image.tobytes("raw", "RGBA")
        qimage = QImage(data, pil_image.width, pil_image.height, QImage.Format.Format_RGBA8888)
        obj._pixmap = QPixmap.fromImage(qimage)
        return obj

    @property
    def width(self) -> int:
        return self._pixmap.width()

    @property
    def height(self) -> int:
        return self._pixmap.height()
