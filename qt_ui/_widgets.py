"""Standard tkinter widget implementations using PyQt6."""

from __future__ import annotations

from typing import Any, Callable

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QAction, QCursor, QFont, QIcon, QPixmap
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMenu,
    QPushButton,
    QRadioButton,
    QScrollArea,
    QScrollBar,
    QSlider,
    QSpinBox,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from ._base import BaseWidget, TclError
from ._variables import BooleanVar, DoubleVar, IntVar, StringVar, Variable


class Frame(BaseWidget):
    def __init__(self, master: Any = None, **kwargs):
        self._init_base(master)
        self._qt = QFrame()
        self._options = {}
        self._apply_initial_config(**kwargs)

    def _get_qt_widget(self) -> QFrame:
        return self._qt

    def _apply_initial_config(self, **kwargs) -> None:
        for key, value in kwargs.items():
            self._apply_option(key, value)

    def _apply_option(self, key: str, value: Any) -> None:
        self._options[key] = value
        if key in ("bg", "background"):
            self._apply_bg_fg(self._qt, bg=value)
        elif key == "fg":
            self._apply_bg_fg(self._qt, fg=value)
        elif key == "relief":
            if str(value).lower() in ("ridge", "groove", "raised", "sunken"):
                self._qt.setFrameShape(QFrame.Shape.Box)
                self._qt.setLineWidth(int(self._options.get("bd", 2)))
        elif key == "bd":
            self._qt.setLineWidth(int(value))


class Label(BaseWidget):
    def __init__(self, master: Any = None, **kwargs):
        self._init_base(master)
        self._qt = QLabel()
        self._textvariable: StringVar | None = None
        self._options = {}
        self._apply_initial_config(**kwargs)

    def _get_qt_widget(self) -> QLabel:
        return self._qt

    def _apply_initial_config(self, **kwargs) -> None:
        text = kwargs.pop("text", "")
        if text:
            self._qt.setText(str(text))
        for key, value in kwargs.items():
            self._apply_option(key, value)

    def _apply_option(self, key: str, value: Any) -> None:
        self._options[key] = value
        if key == "text":
            self._qt.setText(str(value))
        elif key in ("textvariable", "variable"):
            self._textvariable = value
            if value is not None:
                self._qt.setText(str(value.get()))
                value.add_observer(lambda: self._qt.setText(str(value.get())))
        elif key == "font":
            self._qt.setFont(self._parse_font(value))
        elif key in ("bg", "background"):
            self._apply_bg_fg(self._qt, bg=value)
        elif key in ("fg", "foreground"):
            self._apply_bg_fg(self._qt, fg=value)
        elif key == "width":
            self._qt.setMinimumWidth(int(value) * 7)
        elif key == "wraplength":
            self._qt.setWordWrap(True)
        elif key == "anchor":
            anchor = str(value).lower()
            align = Qt.AlignmentFlag.AlignLeft
            if "center" in anchor:
                align = Qt.AlignmentFlag.AlignCenter
            elif "right" in anchor or "e" in anchor:
                align = Qt.AlignmentFlag.AlignRight
            self._qt.setAlignment(align)
        elif key == "relief":
            pass
        elif key == "image":
            if value is not None and hasattr(value, "_pixmap"):
                self._qt.setPixmap(value._pixmap)

    def _get_option(self, key: str) -> Any:
        if key == "text":
            return self._qt.text()
        return self._options.get(key)


class Button(BaseWidget):
    def __init__(self, master: Any = None, **kwargs):
        self._init_base(master)
        self._qt = QPushButton()
        self._command: Callable | None = None
        self._options = {}
        self._qt.clicked.connect(self._on_click)
        self._apply_initial_config(**kwargs)

    def _get_qt_widget(self) -> QPushButton:
        return self._qt

    def _on_click(self) -> None:
        if self._command:
            self._command()

    def _apply_initial_config(self, **kwargs) -> None:
        self._command = kwargs.pop("command", None)
        text = kwargs.pop("text", "")
        if text:
            self._qt.setText(str(text))
        for key, value in kwargs.items():
            self._apply_option(key, value)

    def _apply_option(self, key: str, value: Any) -> None:
        self._options[key] = value
        if key == "text":
            self._qt.setText(str(value))
        elif key == "command":
            self._command = value
        elif key == "font":
            self._qt.setFont(self._parse_font(value))
        elif key in ("bg", "background"):
            self._apply_bg_fg(self._qt, bg=value)
        elif key in ("fg", "foreground"):
            self._apply_bg_fg(self._qt, fg=value)
        elif key == "state":
            self._qt.setEnabled(str(value).lower() != "disabled")
        elif key == "relief":
            pass
        elif key == "image":
            if value is not None and hasattr(value, "_pixmap"):
                self._qt.setIcon(QIcon(value._pixmap))
                self._qt.setText("")


class Entry(BaseWidget):
    def __init__(self, master: Any = None, **kwargs):
        self._init_base(master)
        self._qt = QLineEdit()
        self._textvariable: StringVar | None = None
        self._validate = None
        self._validatecommand = None
        self._options = {}
        self._qt.textChanged.connect(self._on_text_changed)
        self._apply_initial_config(**kwargs)

    def _get_qt_widget(self) -> QLineEdit:
        return self._qt

    def _apply_initial_config(self, **kwargs) -> None:
        for key, value in kwargs.items():
            self._apply_option(key, value)

    def _on_text_changed(self, text: str) -> None:
        if self._textvariable and self._textvariable.get() != text:
            self._textvariable.set(text)

    def insert(self, index: Any, string: str) -> None:
        if str(index).upper() == "END":
            self._qt.setText(self._qt.text() + string)
        else:
            pos = int(index)
            t = self._qt.text()
            self._qt.setText(t[:pos] + string + t[pos:])

    def delete(self, first: Any, last: Any = None) -> None:
        if str(first).upper() == "END":
            self._qt.clear()
        else:
            self._qt.setText("")

    def selection_to(self, index: Any) -> None:
        if str(index).upper() == "END":
            self._qt.setSelection(len(self._qt.text()), 0)

    def focus(self) -> None:
        self._qt.setFocus()

    def icursor(self, index: int) -> None:
        self._qt.setCursorPosition(int(index))

    def get(self) -> str:
        return self._qt.text()

    def _apply_option(self, key: str, value: Any) -> None:
        self._options[key] = value
        if key in ("textvariable", "variable"):
            self._textvariable = value
            if value is not None:
                self._qt.setText(str(value.get()))
                value.add_observer(lambda: self._qt.setText(str(value.get())))
        elif key == "validate":
            self._validate = value
        elif key == "validatecommand":
            self._validatecommand = value
            if self._validate == "key" and value:
                self._qt.textEdited.connect(self._validate_input)
        elif key == "state":
            self._qt.setReadOnly(str(value).lower() == "disabled")
            self._qt.setEnabled(str(value).lower() != "disabled")
        elif key == "width":
            self._qt.setMinimumWidth(int(value) * 7)
        elif key == "font":
            self._qt.setFont(self._parse_font(value))
        elif key in ("bg", "background"):
            self._apply_bg_fg(self._qt, bg=value)
        elif key in ("fg", "foreground"):
            self._apply_bg_fg(self._qt, fg=value)

    def _validate_input(self, text: str) -> None:
        if not self._validatecommand:
            return
        reg_name = self._validatecommand[0] if self._validatecommand else None
        root = self
        while root.master is not None:
            root = root.master
        func = root._validators.get(reg_name) if root else None
        if func and not func(text, text, "1"):
            self._qt.blockSignals(True)
            self._qt.setText(str(self._textvariable.get()) if self._textvariable else "")
            self._qt.blockSignals(False)


class Text(BaseWidget):
    def __init__(self, master: Any = None, **kwargs):
        self._init_base(master)
        self._qt = QTextEdit()
        self._options = {}
        self._apply_initial_config(**kwargs)

    def _get_qt_widget(self) -> QTextEdit:
        return self._qt

    def _apply_initial_config(self, **kwargs) -> None:
        for key, value in kwargs.items():
            self._apply_option(key, value)

    def insert(self, index: Any, string: str) -> None:
        self._qt.insertPlainText(string)

    def delete(self, first: Any, last: Any = None) -> None:
        cursor = self._qt.textCursor()
        cursor.select(cursor.SelectionType.Document)
        cursor.removeSelectedText()

    def get(self, start: str = "1.0", end: str = "end") -> str:
        return self._qt.toPlainText()

    def _apply_option(self, key: str, value: Any) -> None:
        self._options[key] = value
        if key in ("bg", "background"):
            self._apply_bg_fg(self._qt, bg=value)
        elif key in ("fg", "foreground"):
            self._apply_bg_fg(self._qt, fg=value)
        elif key == "width":
            self._qt.setMinimumWidth(int(value) * 7)
        elif key == "height":
            self._qt.setMinimumHeight(int(value) * 16)
        elif key == "font":
            self._qt.setFont(self._parse_font(value))
        elif key == "state":
            self._qt.setReadOnly(str(value).lower() == "disabled")


class Listbox(BaseWidget):
    def __init__(self, master: Any = None, **kwargs):
        self._init_base(master)
        self._qt = QListWidget()
        self._exportselection = True
        self._selectmode = "browse"
        self._yscrollcommand: Callable | None = None
        self._options = {}
        self._qt.currentRowChanged.connect(self._on_select)
        self._apply_initial_config(**kwargs)

    def _get_qt_widget(self) -> QListWidget:
        return self._qt

    def _apply_initial_config(self, **kwargs) -> None:
        for key, value in kwargs.items():
            self._apply_option(key, value)

    def _on_select(self, row: int) -> None:
        self.event_generate("<<ListboxSelect>>")

    def insert(self, index: Any, *elements) -> None:
        for el in elements:
            if str(index).upper() == "END":
                self._qt.addItem(str(el))
            else:
                self._qt.insertItem(int(index), str(el))

    def delete(self, first: Any, last: Any = None) -> None:
        if last is None or str(last).upper() == "END":
            if str(first).upper() == "END":
                self._qt.clear()
            else:
                self._qt.takeItem(int(first))
        else:
            for i in range(int(last), int(first) - 1, -1):
                self._qt.takeItem(i)

    def size(self) -> int:
        return self._qt.count()

    def curselection(self) -> tuple:
        row = self._qt.currentRow()
        return (row,) if row >= 0 else ()

    def selection_set(self, first: int, last: int | None = None) -> None:
        if last is None:
            self._qt.setCurrentRow(int(first))
        else:
            for i in range(int(first), int(last) + 1):
                item = self._qt.item(i)
                if item:
                    item.setSelected(True)

    def selection_clear(self, first: int, last: int | None = None) -> None:
        self._qt.clearSelection()

    def get(self, index: int) -> str:
        item = self._qt.item(int(index))
        return item.text() if item else ""

    def yview(self, *args) -> tuple:
        if args:
            self._qt.verticalScrollBar().setValue(int(float(args[0]) * self._qt.count()))
            return None
        sb = self._qt.verticalScrollBar()
        if sb.maximum() == 0:
            return (0.0, 1.0)
        top = sb.value() / max(sb.maximum(), 1)
        visible = self._qt.viewport().height() / max(self._qt.sizeHintForRow(0) * self._qt.count(), 1)
        return (top, min(1.0, top + visible))

    def see(self, index: int) -> None:
        item = self._qt.item(int(index))
        if item:
            self._qt.scrollToItem(item)

    def bind(self, sequence: str, func: Callable, add: bool | None = None) -> str:
        if sequence == "<<ListboxSelect>>":
            self._qt.itemSelectionChanged.connect(lambda: func(_ListboxEvent(self)))
            return sequence
        return super().bind(sequence, func, add)

    def _apply_option(self, key: str, value: Any) -> None:
        self._options[key] = value
        if key == "exportselection":
            self._exportselection = bool(value)
        elif key == "selectmode":
            self._selectmode = value
            if value in ("extended", "multiple"):
                self._qt.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        elif key == "yscrollcommand":
            self._yscrollcommand = value
            sb = self._qt.verticalScrollBar()
            sb.valueChanged.connect(lambda v: value(*self.yview()) if value else None)
        elif key in ("bg", "background"):
            self._apply_bg_fg(self._qt, bg=value)
        elif key in ("fg", "foreground"):
            self._apply_bg_fg(self._qt, fg=value)
        elif key == "height":
            self._qt.setMinimumHeight(int(value) * 16)


class _ListboxEvent:
    def __init__(self, widget):
        self.widget = widget


class Checkbutton(BaseWidget):
    def __init__(self, master: Any = None, **kwargs):
        self._init_base(master)
        self._qt = QCheckBox()
        self._variable: BooleanVar | None = None
        self._command: Callable | None = None
        self._options = {}
        self._qt.stateChanged.connect(self._on_toggle)
        self._apply_initial_config(**kwargs)

    def _get_qt_widget(self) -> QCheckBox:
        return self._qt

    def _on_toggle(self, state: int) -> None:
        if self._variable:
            self._variable.set(state == Qt.CheckState.Checked.value if hasattr(Qt.CheckState.Checked, "value") else state == 2)
        if self._command:
            self._command()

    def _apply_initial_config(self, **kwargs) -> None:
        self._command = kwargs.pop("command", None)
        text = kwargs.pop("text", "")
        if text:
            self._qt.setText(str(text))
        for key, value in kwargs.items():
            self._apply_option(key, value)

    def _apply_option(self, key: str, value: Any) -> None:
        self._options[key] = value
        if key == "text":
            self._qt.setText(str(value))
        elif key == "variable":
            self._variable = value
            if value is not None:
                self._qt.setChecked(bool(value.get()))
                value.add_observer(lambda: self._qt.setChecked(bool(value.get())))
        elif key == "command":
            self._command = value
        elif key == "state":
            self._qt.setEnabled(str(value).lower() != "disabled")


class Radiobutton(BaseWidget):
    def __init__(self, master: Any = None, **kwargs):
        self._init_base(master)
        self._qt = QRadioButton()
        self._variable: Variable | None = None
        self._value: Any = None
        self._command: Callable | None = None
        self._options = {}
        self._qt.toggled.connect(self._on_toggle)
        self._apply_initial_config(**kwargs)

    def _get_qt_widget(self) -> QRadioButton:
        return self._qt

    def _on_toggle(self, checked: bool) -> None:
        if checked and self._variable is not None and self._value is not None:
            self._variable.set(self._value)
        if checked and self._command:
            self._command()

    def _apply_initial_config(self, **kwargs) -> None:
        self._command = kwargs.pop("command", None)
        text = kwargs.pop("text", "")
        if text:
            self._qt.setText(str(text))
        for key, value in kwargs.items():
            self._apply_option(key, value)

    def _apply_option(self, key: str, value: Any) -> None:
        self._options[key] = value
        if key == "text":
            self._qt.setText(str(value))
        elif key == "variable":
            self._variable = value
            if value is not None:
                self._qt.setChecked(value.get() == self._value)
                value.add_observer(lambda: self._qt.setChecked(value.get() == self._value))
        elif key == "value":
            self._value = value
            if self._variable and self._variable.get() == value:
                self._qt.setChecked(True)
        elif key == "command":
            self._command = value
        elif key == "state":
            self._qt.setEnabled(str(value).lower() != "disabled")


class Scale(BaseWidget):
    def __init__(self, master: Any = None, **kwargs):
        self._init_base(master)
        self._qt = QSlider(Qt.Orientation.Horizontal)
        self._variable: Variable | None = None
        self._command: Callable | None = None
        self._options = {}
        self._qt.valueChanged.connect(self._on_change)
        self._apply_initial_config(**kwargs)

    def _get_qt_widget(self) -> QSlider:
        return self._qt

    def _on_change(self, val: int) -> None:
        if self._variable:
            self._variable.set(val)
        if self._command:
            self._command(val)

    def _apply_initial_config(self, **kwargs) -> None:
        orient = kwargs.pop("orient", "horizontal")
        if str(orient).lower() in ("vertical", "y"):
            self._qt.setOrientation(Qt.Orientation.Vertical)
        for key, value in kwargs.items():
            self._apply_option(key, value)

    def _apply_option(self, key: str, value: Any) -> None:
        self._options[key] = value
        if key == "from_":
            self._qt.setMinimum(int(value))
        elif key == "to":
            self._qt.setMaximum(int(value))
        elif key == "variable":
            self._variable = value
            if value is not None:
                self._qt.setValue(int(value.get()))
                value.add_observer(lambda: self._qt.setValue(int(value.get())))
        elif key == "command":
            self._command = value
        elif key == "orient":
            if str(value).lower() in ("vertical", "y"):
                self._qt.setOrientation(Qt.Orientation.Vertical)
        elif key == "length":
            if self._qt.orientation() == Qt.Orientation.Horizontal:
                self._qt.setMinimumWidth(int(value))
            else:
                self._qt.setMinimumHeight(int(value))


class Spinbox(BaseWidget):
    def __init__(self, master: Any = None, **kwargs):
        self._init_base(master)
        self._qt = QSpinBox()
        self._textvariable: StringVar | None = None
        self._options = {}
        self._qt.valueChanged.connect(self._on_change)
        self._apply_initial_config(**kwargs)

    def _get_qt_widget(self) -> QSpinBox:
        return self._qt

    def _on_change(self, val: int) -> None:
        if self._textvariable:
            self._textvariable.set(str(val))

    def _apply_initial_config(self, **kwargs) -> None:
        for key, value in kwargs.items():
            self._apply_option(key, value)

    def _apply_option(self, key: str, value: Any) -> None:
        self._options[key] = value
        if key == "from_":
            self._qt.setMinimum(int(value))
        elif key == "to":
            self._qt.setMaximum(int(value))
        elif key in ("textvariable", "variable"):
            self._textvariable = value
            if value is not None:
                try:
                    self._qt.setValue(int(value.get()))
                except ValueError:
                    pass
                value.add_observer(lambda: self._qt.setValue(int(value.get())) if str(value.get()).isdigit() else None)


class Canvas(BaseWidget):
    def __init__(self, master: Any = None, **kwargs):
        self._init_base(master)
        self._qt = QScrollArea()
        self._canvas = QWidget()
        self._qt.setWidget(self._canvas)
        self._qt.setWidgetResizable(True)
        self._items: dict[int, Any] = {}
        self._item_counter = 0
        self._yscrollcommand = None
        self._options = {}
        self._apply_initial_config(**kwargs)

    def _get_qt_widget(self) -> QScrollArea:
        return self._qt

    def _apply_initial_config(self, **kwargs) -> None:
        for key, value in kwargs.items():
            self._apply_option(key, value)

    def create_window(self, x, y, window=None, anchor="nw", **kwargs):
        self._item_counter += 1
        iid = self._item_counter
        if window is not None:
            qt = window._get_qt_widget()
            qt.setParent(self._canvas)
            qt.move(int(x), int(y))
            qt.show()
        self._items[iid] = window
        return iid

    def itemconfigure(self, item, **kwargs):
        if "width" in kwargs and item in self._items:
            w = self._items[item]
            if w:
                w._get_qt_widget().setFixedWidth(int(kwargs["width"]))

    def config(self, cnf=None, **kwargs):
        if cnf:
            kwargs.update(cnf)
        if "scrollregion" in kwargs:
            parts = kwargs["scrollregion"].split()
            if len(parts) == 4:
                w, h = int(float(parts[2])), int(float(parts[3]))
                self._canvas.setMinimumSize(w, h)
        if "width" in kwargs:
            self._qt.setMinimumWidth(int(kwargs["width"]))
        return super().config(**{k: v for k, v in kwargs.items() if k not in ("scrollregion", "width")})

    def yview(self, *args):
        sb = self._qt.verticalScrollBar()
        if args:
            sb.setValue(int(float(args[0]) * sb.maximum()))
            return None
        mx = max(sb.maximum(), 1)
        return (sb.value() / mx, (sb.value() + self._qt.viewport().height()) / mx)

    def xview_moveto(self, fraction: float) -> None:
        self._qt.horizontalScrollBar().setValue(int(fraction * self._qt.horizontalScrollBar().maximum()))

    def yview_moveto(self, fraction: float) -> None:
        self._qt.verticalScrollBar().setValue(int(fraction * self._qt.verticalScrollBar().maximum()))

    def _apply_option(self, key: str, value: Any) -> None:
        self._options[key] = value
        if key == "yscrollcommand":
            self._yscrollcommand = value
            sb = self._qt.verticalScrollBar()
            sb.valueChanged.connect(lambda: value(*self.yview()) if value else None)
        elif key in ("bg", "background"):
            self._apply_bg_fg(self._canvas, bg=value)
        elif key == "highlightthickness":
            pass


class Scrollbar(BaseWidget):
    def __init__(self, master: Any = None, **kwargs):
        self._init_base(master)
        orient = kwargs.get("orient", "vertical")
        if str(orient).lower() in ("horizontal", "x"):
            self._qt = QScrollBar(Qt.Orientation.Horizontal)
        else:
            self._qt = QScrollBar(Qt.Orientation.Vertical)
        self._command: Callable | None = None
        self._options = {}
        self._qt.valueChanged.connect(self._on_scroll)
        self._apply_initial_config(**kwargs)

    def _get_qt_widget(self) -> QScrollBar:
        return self._qt

    def _on_scroll(self, val: int) -> None:
        if self._command:
            mx = max(self._qt.maximum(), 1)
            self._command("moveto", val / mx)

    def set(self, first: float, last: float) -> None:
        self._qt.setRange(0, 100)
        span = max(last - first, 0.01)
        page = int(span * 100)
        self._qt.setPageStep(max(page, 1))
        self._qt.setValue(int(first * 100))

    def _apply_initial_config(self, **kwargs) -> None:
        for key, value in kwargs.items():
            self._apply_option(key, value)

    def _apply_option(self, key: str, value: Any) -> None:
        self._options[key] = value
        if key == "command":
            self._command = value


class Menu(BaseWidget):
    def __init__(self, master: Any = None, **kwargs):
        self._init_base(master)
        self._qt = QMenu()
        self._tearoff = 0
        self._options = {}
        self._apply_initial_config(**kwargs)

    def _get_qt_widget(self) -> QMenu:
        return self._qt

    def _apply_initial_config(self, **kwargs) -> None:
        for key, value in kwargs.items():
            self._apply_option(key, value)

    def add_command(self, **kwargs) -> None:
        label = kwargs.get("label", "")
        command = kwargs.get("command")
        action = QAction(label, self._qt)
        if command:
            action.triggered.connect(command)
        self._qt.addAction(action)

    def add_cascade(self, **kwargs) -> None:
        label = kwargs.get("label", "")
        menu = kwargs.get("menu")
        if menu:
            self._qt.addMenu(label).addActions(menu._qt.actions())

    def add_checkbutton(self, **kwargs) -> None:
        label = kwargs.get("label", "")
        command = kwargs.get("command")
        variable = kwargs.get("variable")
        action = QAction(label, self._qt)
        action.setCheckable(True)
        if variable:
            action.setChecked(bool(variable.get()))
            action.triggered.connect(lambda checked: variable.set(checked))
        if command:
            action.triggered.connect(command)
        self._qt.addAction(action)

    def add_separator(self) -> None:
        self._qt.addSeparator()

    def tk_popup(self, x: int, y: int, index: int = 0) -> None:
        from PyQt6.QtGui import QCursor

        self._qt.popup(QCursor.pos())
        self.after(100, self.grab_release)

    def entryconfig(self, index: int, **kwargs) -> None:
        actions = self._qt.actions()
        if 0 <= index < len(actions):
            if "state" in kwargs:
                actions[index].setEnabled(str(kwargs["state"]).lower() != "disabled")

    def _apply_option(self, key: str, value: Any) -> None:
        self._options[key] = value
        if key == "tearoff":
            self._tearoff = int(value)


class Menubutton(BaseWidget):
    def __init__(self, master: Any = None, **kwargs):
        self._init_base(master)
        self._qt = QPushButton()
        self._menu = None
        self._options = {}
        self._apply_initial_config(**kwargs)

    def _get_qt_widget(self) -> QPushButton:
        return self._qt

    def _apply_initial_config(self, **kwargs) -> None:
        text = kwargs.pop("text", "")
        if text:
            self._qt.setText(str(text))
        for key, value in kwargs.items():
            self._apply_option(key, value)

    def _apply_option(self, key: str, value: Any) -> None:
        self._options[key] = value
        if key == "text":
            self._qt.setText(str(value))
        elif key == "menu":
            self._menu = value
            self._qt.clicked.connect(lambda: value._qt.popup(self._qt.mapToGlobal(self._qt.rect().bottomLeft())))
