"""Matplotlib backend wrappers compatible with backend_tkagg API."""

from __future__ import annotations

from typing import Any

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT as _NavigationToolbar2QT

from ._base import BaseWidget


class FigureCanvasTkAgg(BaseWidget):
    """Drop-in replacement for FigureCanvasTkAgg with qt_ui pack support."""

    def __init__(self, figure, master=None):
        self._init_base(master)
        self._canvas = FigureCanvasQTAgg(figure)
        self._tkcanvas = self._canvas
        self.figure = figure

    def _get_qt_widget(self):
        return self._canvas

    def get_tk_widget(self):
        return self

    def draw(self):
        self._canvas.draw()


class NavigationToolbar2Tk(BaseWidget):
    """Drop-in replacement for NavigationToolbar2Tk with qt_ui pack support."""

    def __init__(self, canvas, window, *, pack_toolbar=True):
        qt_canvas = canvas._canvas if isinstance(canvas, FigureCanvasTkAgg) else canvas
        self._init_base(window)
        self._toolbar = _NavigationToolbar2QT(qt_canvas, window._get_qt_widget() if hasattr(window, "_get_qt_widget") else window)
        self._window = window
        if pack_toolbar:
            self.pack(side="bottom", fill="x")

    def _get_qt_widget(self):
        return self._toolbar

    def pack(self, **kwargs):
        super().pack(**kwargs)

    def update(self):
        self._toolbar.update()
