"""Base widget mixin implementing tkinter-like geometry and event APIs."""

from __future__ import annotations

import re
import weakref
from typing import Any, Callable

from PyQt6.QtCore import QEvent, QObject, QTimer, Qt, pyqtSignal
from PyQt6.QtGui import QCursor, QFont, QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLayout,
    QMenuBar,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from ._app import get_app


class TclError(Exception):
    """Tkinter-compatible exception type."""


class _PackEntry:
    __slots__ = ("widget", "side", "fill", "expand", "padx", "pady", "in_layout")

    def __init__(self, widget, side, fill, expand, padx, pady):
        self.widget = widget
        self.side = side
        self.fill = fill
        self.expand = expand
        self.padx = padx
        self.pady = pady
        self.in_layout = False


class BaseWidget:
    """Mixin providing tkinter widget behaviour on top of Qt widgets."""

    _widget_counter = 0

    def _init_base(self, master: Any = None) -> None:
        self._master = master
        self._bindings: dict[str, list[tuple[Callable, bool]]] = {}
        self._after_ids: dict[int, QTimer] = {}
        self._after_counter = 0
        self._validators: dict[str, Callable] = {}
        self._children: list[Any] = []
        self._pack_entries: list[_PackEntry] = []
        self._pack_root: QVBoxLayout | None = None
        self._pack_row: QHBoxLayout | None = None
        self._grid_layout: QGridLayout | None = None
        self._grid_items: dict[Any, tuple[int, int, int, int]] = {}
        self._protocols: dict[str, Callable] = {}
        self._menu: Any = None
        self._hidden = False
        self._state = "normal"
        BaseWidget._widget_counter += 1
        self._winfo_id = BaseWidget._widget_counter
        if master is not None:
            master._register_child(self)

    def _register_child(self, child: Any) -> None:
        self._children.append(child)

    @property
    def master(self) -> Any:
        return self._master

    def _get_qt_widget(self) -> QWidget:
        raise NotImplementedError

    def _get_layout_container(self) -> QWidget:
        return self._get_qt_widget()

    def _ensure_pack_root(self) -> QVBoxLayout:
        if self._pack_root is None:
            container = self._get_layout_container()
            self._pack_root = QVBoxLayout(container)
            self._pack_root.setContentsMargins(0, 0, 0, 0)
            self._pack_root.setSpacing(0)
        return self._pack_root

    def _ensure_grid_layout(self) -> QGridLayout:
        if self._grid_layout is None:
            container = self._get_layout_container()
            self._grid_layout = QGridLayout(container)
            self._grid_layout.setContentsMargins(0, 0, 0, 0)
        return self._grid_layout

    @staticmethod
    def _normalize_side(side: Any) -> str:
        return str(side).lower()

    @staticmethod
    def _normalize_fill(fill: Any) -> str:
        if fill in (None, ""):
            return "none"
        return str(fill).lower()

    @staticmethod
    def _parse_padding(value: Any) -> tuple[int, int, int, int]:
        if value is None:
            return 0, 0, 0, 0
        if isinstance(value, (list, tuple)):
            if len(value) == 1:
                return value[0], value[0], value[0], value[0]
            if len(value) == 2:
                return value[0], value[1], value[0], value[1]
            if len(value) >= 4:
                return value[0], value[1], value[2], value[3]
        return int(value), int(value), int(value), int(value)

    def _size_policy(self, fill: str, expand: bool) -> QSizePolicy:
        h = QSizePolicy.Policy.Expanding if fill in ("x", "both") or expand else QSizePolicy.Policy.Preferred
        v = QSizePolicy.Policy.Expanding if fill in ("y", "both") or expand else QSizePolicy.Policy.Preferred
        return QSizePolicy(h, v)

    def pack(self, **kwargs) -> None:
        side = self._normalize_side(kwargs.get("side", "top"))
        fill = self._normalize_fill(kwargs.get("fill", "none"))
        expand = bool(kwargs.get("expand", False))
        padx = kwargs.get("padx", 0)
        pady = kwargs.get("pady", 0)
        pl, pt, pr, pb = self._parse_padding(padx)
        _, pt2, _, pb2 = self._parse_padding(pady)
        pt += pt2
        pb += pb2

        entry = _PackEntry(self, side, fill, expand, (pl, pr), (pt, pb))
        self.master._pack_entries.append(entry)
        self.master._apply_pack()

    def _apply_pack(self) -> None:
        root = self._ensure_pack_root()
        while root.count():
            item = root.takeAt(0)
            if item.layout():
                item.layout().deleteLater()

        self._pack_row = None
        qt_widgets: list[tuple[QWidget, _PackEntry]] = []

        for entry in self._pack_entries:
            qt = entry.widget._get_qt_widget()
            qt.setSizePolicy(self._size_policy(entry.fill, entry.expand))
            pl, pr = entry.padx
            pt, pb = entry.pady
            qt.setContentsMargins(pl, pt, pr, pb)
            qt_widgets.append((qt, entry))

        row_layout: QHBoxLayout | None = None

        def flush_row() -> None:
            nonlocal row_layout
            if row_layout is not None:
                root.addLayout(row_layout)
                row_layout = None

        for qt, entry in qt_widgets:
            side = entry.side
            if side in ("left", "right"):
                if row_layout is None:
                    row_layout = QHBoxLayout()
                    row_layout.setContentsMargins(0, 0, 0, 0)
                    row_layout.setSpacing(0)
                if side == "right":
                    row_layout.addStretch(1)
                    row_layout.addWidget(qt)
                else:
                    row_layout.addWidget(qt)
                    row_layout.addStretch(1)
            else:
                flush_row()
                if side == "bottom":
                    root.insertWidget(0, qt)
                else:
                    root.addWidget(qt)
        flush_row()

    def pack_forget(self) -> None:
        if self.master is None:
            return
        self.master._pack_entries = [e for e in self.master._pack_entries if e.widget is not self]
        self.master._apply_pack()

    def grid(self, **kwargs) -> None:
        row = int(kwargs.get("row", 0))
        column = int(kwargs.get("column", 0))
        rowspan = int(kwargs.get("rowspan", 1))
        columnspan = int(kwargs.get("columnspan", 1))
        sticky = str(kwargs.get("sticky", "")).upper()
        padx = kwargs.get("padx", 0)
        pady = kwargs.get("pady", 0)
        pl, pt, pr, pb = self._parse_padding(padx)
        _, pt2, _, pb2 = self._parse_padding(pady)

        layout = self.master._ensure_grid_layout()
        qt = self._get_qt_widget()
        qt.setContentsMargins(pl, pt, pr, pb)

        alignment = Qt.AlignmentFlag(0)
        if "N" in sticky:
            alignment |= Qt.AlignmentFlag.AlignTop
        if "S" in sticky:
            alignment |= Qt.AlignmentFlag.AlignBottom
        if "W" in sticky:
            alignment |= Qt.AlignmentFlag.AlignLeft
        if "E" in sticky:
            alignment |= Qt.AlignmentFlag.AlignRight
        if not sticky:
            alignment = Qt.AlignmentFlag.AlignCenter

        layout.addWidget(qt, row, column, rowspan, columnspan, alignment)
        self.master._grid_items[self] = (row, column, rowspan, columnspan)

    def grid_forget(self) -> None:
        if self.master is None or self.master._grid_layout is None:
            return
        self.master._grid_layout.removeWidget(self._get_qt_widget())
        self.master._grid_items.pop(self, None)

    def bind(self, sequence: str, func: Callable, add: bool | None = None) -> str:
        seq = sequence
        if add:
            self._bindings.setdefault(seq, []).append((func, True))
        else:
            self._bindings[seq] = [(func, False)]
        self._connect_binding(seq, func)
        return seq

    def _connect_binding(self, sequence: str, func: Callable) -> None:
        qt = self._get_qt_widget()
        if sequence == "<Configure>":
            qt.installEventFilter(_EventFilter(self, QEvent.Type.Resize, func))
        elif sequence == "<Button-1>":
            qt.mousePressEvent = _wrap_mouse(qt.mousePressEvent, func, 1)
        elif sequence == "<Button-3>":
            qt.mousePressEvent = _wrap_mouse(qt.mousePressEvent, func, 3)
        elif sequence in ("<Up>", "<Down>", "<Delete>", "<Escape>", "<Double-Button-1>"):
            qt.installEventFilter(_KeyEventFilter(self, sequence, func))
        elif sequence.startswith("<") and sequence.endswith(">"):
            qt.installEventFilter(_GenericEventFilter(self, sequence, func))

    def event_generate(self, sequence: str, **kwargs) -> None:
        for func, _ in self._bindings.get(sequence, []):
            event = _SyntheticEvent(self, sequence, **kwargs)
            func(event)

    def configure(self, cnf: dict | None = None, **kwargs) -> Any:
        if cnf:
            kwargs.update(cnf)
        return self.config(**kwargs)

    def config(self, cnf: str | None = None, **kwargs) -> Any:
        if cnf is not None and not kwargs:
            return self.cget(cnf)
        for key, value in kwargs.items():
            self._apply_option(key, value)
        return None

    def cget(self, key: str) -> Any:
        return self._get_option(key)

    def _apply_option(self, key: str, value: Any) -> None:
        raise NotImplementedError(f"{type(self).__name__} does not support option {key!r}")

    def _get_option(self, key: str) -> Any:
        raise KeyError(key)

    def register(self, func: Callable, *args: Any) -> str:
        name = f"pyfunc{len(self._validators)}"

        def wrapper(*call_args):
            full = list(args)
            for i, a in enumerate(full):
                if isinstance(a, str) and a.startswith("%"):
                    idx = {"%P": 0, "%S": 0, "%s": 1, "%d": 2, "%i": 2}.get(a, -1)
                    if 0 <= idx < len(call_args):
                        full[i] = call_args[idx]
            try:
                return bool(func(*full))
            except TypeError:
                return bool(func())

        self._validators[name] = wrapper
        return name

    def after(self, ms: int, func: Callable | None = None, *args) -> int:
        self._after_counter += 1
        timer_id = self._after_counter

        def fire():
            if func:
                func(*args)

        timer = QTimer()
        timer.setSingleShot(True)
        timer.timeout.connect(fire)
        timer.start(int(ms))
        self._after_ids[timer_id] = timer
        return timer_id

    def after_cancel(self, timer_id: int) -> None:
        timer = self._after_ids.pop(timer_id, None)
        if timer:
            timer.stop()

    def winfo_id(self) -> int:
        return self._winfo_id

    def winfo_name(self) -> str:
        return str(self._winfo_id)

    def winfo_parent(self) -> str:
        if self._master is None:
            return ""
        return str(self._master.winfo_id())

    def winfo_children(self) -> tuple:
        return tuple(self._children)

    def winfo_x(self) -> int:
        return self._get_qt_widget().mapToGlobal(self._get_qt_widget().rect().topLeft()).x()

    def winfo_y(self) -> int:
        return self._get_qt_widget().mapToGlobal(self._get_qt_widget().rect().topLeft()).y()

    def winfo_width(self) -> int:
        return self._get_qt_widget().width()

    def winfo_height(self) -> int:
        return self._get_qt_widget().height()

    def winfo_reqwidth(self) -> int:
        return self._get_qt_widget().sizeHint().width()

    def winfo_reqheight(self) -> int:
        return self._get_qt_widget().sizeHint().height()

    def winfo_screenwidth(self) -> int:
        screen = QApplication.primaryScreen()
        return screen.availableGeometry().width() if screen else 1920

    def winfo_screenheight(self) -> int:
        screen = QApplication.primaryScreen()
        return screen.availableGeometry().height() if screen else 1080

    def winfo_exists(self) -> bool:
        return not self._get_qt_widget().isHidden()

    def nametowidget(self, name: str) -> Any:
        target = int(name)
        if self.winfo_id() == target:
            return self
        for child in self._children:
            try:
                return child.nametowidget(name)
            except (ValueError, KeyError, TclError):
                continue
        raise KeyError(name)

    def wait_visibility(self, window: Any | None = None) -> None:
        target = window or self
        get_app().processEvents()
        qt = target._get_qt_widget() if hasattr(target, "_get_qt_widget") else target
        while not qt.isVisible():
            get_app().processEvents()

    def wait_window(self, window: Any | None = None) -> None:
        target = window or self
        get_app().processEvents()
        while target._get_qt_widget().isVisible():
            get_app().processEvents()

    def protocol(self, name: str, func: Callable | None = None) -> None:
        if func is None:
            return self._protocols.get(name)
        self._protocols[name] = func
        if name == "WM_DELETE_WINDOW":
            qt = self._get_qt_widget()
            if hasattr(qt, "closeEvent"):
                original = qt.closeEvent

                def close_event(event):
                    func()
                    event.accept()

                qt.closeEvent = close_event  # type: ignore[method-assign]

    def geometry(self, newGeometry: str | None = None) -> str:
        qt = self._get_qt_widget()
        if newGeometry is None:
            g = qt.geometry()
            return f"{g.width()}x{g.height()}+{g.x()}+{g.y()}"
        match = re.match(r"(\d+)x(\d+)(?:\+(-?\d+)\+(-?\d+))?", newGeometry)
        if match:
            w, h = int(match.group(1)), int(match.group(2))
            x = int(match.group(3)) if match.group(3) else qt.x()
            y = int(match.group(4)) if match.group(4) else qt.y()
            qt.setGeometry(x, y, w, h)
        return newGeometry

    def title(self, newTitle: str | None = None) -> str:
        qt = self._get_qt_widget()
        if newTitle is None:
            return qt.windowTitle()
        qt.setWindowTitle(newTitle)
        return newTitle

    def iconbitmap(self, bitmap: str | None = None) -> None:
        if bitmap:
            self._get_qt_widget().setWindowIcon(QIcon(bitmap))

    def state(self, newstate: str | None = None) -> str:
        qt = self._get_qt_widget()
        if newstate is None:
            if self._hidden:
                return "withdrawn"
            if qt.isMinimized():
                return "iconic"
            return self._state
        newstate = str(newstate).lower()
        if newstate == "withdrawn":
            qt.hide()
            self._hidden = True
        elif newstate == "iconic":
            qt.showMinimized()
            self._hidden = False
        elif newstate in ("normal", "zoomed"):
            qt.show()
            self._hidden = False
            self._state = newstate
            if newstate == "zoomed":
                qt.showMaximized()
        else:
            self._state = newstate
        return newstate

    def withdraw(self) -> None:
        self.state("withdrawn")

    def deiconify(self) -> None:
        self.state("normal")

    def lift(self, aboveThis: Any = None) -> None:
        qt = self._get_qt_widget()
        qt.raise_()
        qt.activateWindow()

    def grab_set(self) -> None:
        self._get_qt_widget().setWindowModality(Qt.WindowModality.ApplicationModal)
        self._get_qt_widget().grab()

    def grab_release(self) -> None:
        self._get_qt_widget().setWindowModality(Qt.WindowModality.NonModal)
        self._get_qt_widget().releaseMouse()

    def focus_set(self) -> None:
        self._get_qt_widget().setFocus()

    def focus_force(self) -> None:
        self._get_qt_widget().setFocus(Qt.FocusReason.OtherFocusReason)
        self._get_qt_widget().activateWindow()

    def overrideredirect(self, boolean: bool | None = None) -> bool:
        qt = self._get_qt_widget()
        if boolean is None:
            return bool(qt.windowFlags() & Qt.WindowType.FramelessWindowHint)
        flags = qt.windowFlags()
        if boolean:
            qt.setWindowFlags(flags | Qt.WindowType.FramelessWindowHint)
        else:
            qt.setWindowFlags(flags & ~Qt.WindowType.FramelessWindowHint)
        qt.show()
        return boolean

    def resizable(self, width: bool | None = None, height: bool | None = None) -> tuple:
        qt = self._get_qt_widget()
        if width is None and height is None:
            return True, True
        if width is not None and height is not None:
            if not width and not height:
                qt.setFixedSize(qt.size())
            else:
                qt.setMinimumSize(0, 0)
                qt.setMaximumSize(16777215, 16777215)
        return width, height

    def transient(self, master: Any | None = None) -> None:
        if master is not None:
            self._get_qt_widget().setWindowModality(Qt.WindowModality.WindowModal)

    def update_idletasks(self) -> None:
        get_app().processEvents()

    def destroy(self) -> None:
        qt = self._get_qt_widget()
        if self._master and self in self._master._children:
            self._master._children.remove(self)
        qt.deleteLater()

    def bell(self) -> None:
        QApplication.beep()

    def _parse_font(self, font_spec: Any) -> QFont:
        if isinstance(font_spec, QFont):
            return font_spec
        if isinstance(font_spec, (list, tuple)):
            family, size = font_spec[0], int(font_spec[1])
            font = QFont(family, size)
            if len(font_spec) > 2:
                for token in font_spec[2:]:
                    if token == "bold":
                        font.setBold(True)
                    elif token == "italic":
                        font.setItalic(True)
            return font
        if isinstance(font_spec, str):
            parts = font_spec.split()
            if parts:
                family = parts[0]
                size = 12
                font = QFont(family, size)
                for token in parts[1:]:
                    if token.isdigit():
                        font.setPointSize(int(token))
                    elif token == "bold":
                        font.setBold(True)
                    elif token == "italic":
                        font.setItalic(True)
                return font
        return QFont()

    def _apply_bg_fg(self, qt: QWidget, bg: Any = None, fg: Any = None) -> None:
        sheet_parts = []
        if bg is not None:
            sheet_parts.append(f"background-color: {bg};")
        if fg is not None:
            sheet_parts.append(f"color: {fg};")
        if sheet_parts:
            qt.setStyleSheet("".join(sheet_parts))


class _SyntheticEvent:
    def __init__(self, widget: Any, sequence: str, **kwargs):
        self.widget = widget
        self.type = sequence
        self.x_root = kwargs.get("x_root", 0)
        self.y_root = kwargs.get("y_root", 0)
        for k, v in kwargs.items():
            setattr(self, k, v)


class _EventFilter(QObject):
    def __init__(self, widget: BaseWidget, event_type: QEvent.Type, callback: Callable):
        super().__init__()
        self._widget = widget
        self._event_type = event_type
        self._callback = callback

    def eventFilter(self, obj, event):
        if event.type() == self._event_type:
            self._callback(_SyntheticEvent(self._widget, "<Configure>"))
        return False


class _KeyEventFilter(QObject):
    _KEY_MAP = {
        "<Up>": Qt.Key.Key_Up,
        "<Down>": Qt.Key.Key_Down,
        "<Delete>": Qt.Key.Key_Delete,
        "<Escape>": Qt.Key.Key_Escape,
    }

    def __init__(self, widget: BaseWidget, sequence: str, callback: Callable):
        super().__init__()
        self._widget = widget
        self._sequence = sequence
        self._callback = callback

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.KeyPress:
            if self._sequence == "<Double-Button-1>":
                return False
            key = self._KEY_MAP.get(self._sequence)
            if key and event.key() == key:
                result = self._callback(event)
                return result == "break"
        if event.type() == QEvent.Type.MouseButtonDblClick and self._sequence == "<Double-Button-1>":
            self._callback(event)
        return False


class _GenericEventFilter(QObject):
    def __init__(self, widget: BaseWidget, sequence: str, callback: Callable):
        super().__init__()
        self._widget = widget
        self._sequence = sequence
        self._callback = callback

    def eventFilter(self, obj, event):
        return False


def _wrap_mouse(original, func, button):
    def handler(event):
        if event.button() == button:
            func(_SyntheticEvent(None, f"<Button-{button}>", x_root=event.globalPosition().x(), y_root=event.globalPosition().y()))
        if original:
            original(event)

    return handler
