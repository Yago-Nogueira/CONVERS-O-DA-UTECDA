"""Matplotlib backend wrappers for PyQt6."""

from __future__ import annotations

from typing import Any

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as _FigureCanvasQTAgg, NavigationToolbar2QT as _NavigationToolbar2QT

from ._base import BaseWidget


class FigureCanvasQTAgg(BaseWidget):
    """FigureCanvas wrapper with layout support."""

    def __init__(self, figure, master=None):
        self._init_base(master)
        self._canvas = _FigureCanvasQTAgg(figure)
        self._qt_canvas = self._canvas
        self._tkcanvas = self._canvas  # alias
        self.figure = figure

    def _get_qt_widget(self):
        return self._canvas

    def get_widget(self):
        """Return the widget for layout placement."""
        return self

    def get_tk_widget(self):
        """Alias for get_widget()."""
        return self.get_widget()

    def draw(self):
        self._canvas.draw()


class NavigationToolbar2QT(BaseWidget):
    """Navigation toolbar wrapper with layout support."""

    def __init__(self, canvas, window, *, pack_toolbar=True):
        qt_canvas = canvas._canvas if hasattr(canvas, '_canvas') else canvas
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
