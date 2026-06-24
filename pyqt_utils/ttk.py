"""Themed widget components using PyQt6."""

from __future__ import annotations

from typing import Any, Callable

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QProgressBar,
    QPushButton,
    QScrollBar,
    QTabWidget,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from ._base import BaseWidget, AppError
from ._variables import DoubleVar, StringVar, Variable
from ._widgets import Button, Checkbutton, Entry, Frame, Label, Scrollbar


class Style:
    def __init__(self, master: Any = None):
        self.master = master
        self._configs: dict[tuple, dict] = {}

    def configure(self, style: str, **kwargs) -> None:
        self._configs[(style,)] = kwargs

    def lookup(self, style: str, option: str) -> str:
        cfg = self._configs.get((style,), {})
        if option == "background":
            return cfg.get("background", "#f0f0f0")
        return cfg.get(option, "")

    def theme_use(self, theme: str) -> None:
        pass


class Combobox(BaseWidget):
    def __init__(self, master: Any = None, **kwargs):
        self._init_base(master)
        self._qt = QComboBox()
        self._textvariable: StringVar | None = None
        self._exportselection = True
        self._values: list = []
        self._options = {}
        self._qt.currentTextChanged.connect(self._on_text_changed)
        self._qt.activated.connect(self._on_selected)
        self._apply_initial_config(**kwargs)

    def _get_qt_widget(self) -> QComboBox:
        return self._qt

    def _apply_initial_config(self, **kwargs) -> None:
        for key, value in kwargs.items():
            self._apply_option(key, value)

    def _on_text_changed(self, text: str) -> None:
        if self._textvariable and self._textvariable.get() != text:
            self._textvariable.set(text)

    def _on_selected(self, index: int) -> None:
        self.event_generate("<<ComboboxSelected>>")

    def current(self, index: int | None = None) -> int | str:
        if index is None:
            return self._qt.currentIndex()
        self._qt.setCurrentIndex(int(index))
        return index

    def bind(self, sequence: str, func: Callable, add: bool | None = None) -> str:
        if sequence == "<<ComboboxSelected>>":
            self._qt.activated.connect(lambda _: func(_ComboEvent(self)))
            return sequence
        return super().bind(sequence, func, add)

    def _apply_option(self, key: str, value: Any) -> None:
        self._options[key] = value
        if key == "values":
            self._values = list(value)
            self._qt.clear()
            self._qt.addItems([str(v) for v in value])
        elif key in ("textvariable", "variable"):
            self._textvariable = value
            if value is not None:
                idx = self._qt.findText(str(value.get()))
                if idx >= 0:
                    self._qt.setCurrentIndex(idx)
                value.add_observer(self._sync_from_var)
        elif key == "state":
            st = str(value).lower()
            if st == "readonly":
                self._qt.setEditable(False)
                self._qt.setEnabled(True)
            elif st == "disabled":
                self._qt.setEnabled(False)
            else:
                self._qt.setEditable(True)
                self._qt.setEnabled(True)
        elif key == "exportselection":
            self._exportselection = bool(value)
        elif key == "width":
            self._qt.setMinimumWidth(int(value) * 7)

    def _sync_from_var(self) -> None:
        if self._textvariable:
            idx = self._qt.findText(str(self._textvariable.get()))
            if idx >= 0:
                self._qt.setCurrentIndex(idx)


class _ComboEvent:
    def __init__(self, widget):
        self.widget = widget


class Treeview(BaseWidget):
    def __init__(self, master: Any = None, **kwargs):
        self._init_base(master)
        columns = kwargs.get("columns", ())
        show = kwargs.get("show", "tree headings")
        self._qt = QTreeWidget()
        self._columns = list(columns)
        self._show = show
        self._items: dict[str, QTreeWidgetItem] = {}
        self._item_counter = 0
        self._heading_commands: dict[str, Callable] = {}
        self._column_configs: dict[str, dict] = {}
        self._yscroll_cmd = None
        self._options = {}

        if "headings" in show:
            self._qt.setHeaderLabels([str(c) for c in columns] if columns else ["#0"])
        else:
            self._qt.setHeaderHidden(True)

        if columns:
            self._qt.setColumnCount(len(columns))
            for i, c in enumerate(columns):
                self._qt.headerItem().setText(i, str(c))

        self._apply_initial_config(**kwargs)

    def _get_qt_widget(self) -> QTreeWidget:
        return self._qt

    def _apply_initial_config(self, **kwargs) -> None:
        for key, value in kwargs.items():
            if key not in ("columns", "show"):
                self._apply_option(key, value)

    def __setitem__(self, key: str, value: Any) -> None:
        if key == "yscroll":
            self._yscroll_cmd = value
            sb = self._qt.verticalScrollBar()
            sb.valueChanged.connect(lambda: value(*self.yview()) if value else None)

    def __getitem__(self, key: str) -> Any:
        if key == "yscroll":
            return self._yscroll_cmd
        raise KeyError(key)

    def insert(self, parent: str, index: str, **kwargs) -> str:
        self._item_counter += 1
        iid = kwargs.get("iid", f"I{self._item_counter:03d}")
        values = kwargs.get("values", ())
        item = QTreeWidgetItem(list(str(v) for v in values))
        if parent == "" or parent == "end":
            if str(index) == "end":
                self._qt.addTopLevelItem(item)
            else:
                self._qt.insertTopLevelItem(int(index), item)
        else:
            parent_item = self._items.get(parent)
            if parent_item:
                parent_item.addChild(item)
        self._items[iid] = item
        item.setData(0, Qt.ItemDataRole.UserRole, iid)
        return iid

    def item(self, item_id: str, option: str | None = None, **kwargs) -> Any:
        qt_item = self._items.get(item_id)
        if qt_item is None:
            raise AppError(f"Item {item_id} not found")
        if option is None and not kwargs:
            vals = []
            for i in range(self._qt.columnCount()):
                vals.append(qt_item.text(i))
            return {"values": tuple(vals)}
        if "values" in kwargs:
            for i, v in enumerate(kwargs["values"]):
                qt_item.setText(i, str(v))
        if option:
            return qt_item.text(self._column_index(option))
        return None

    def set(self, item_id: str, column: str, value: Any) -> None:
        qt_item = self._items.get(item_id)
        if qt_item:
            qt_item.setText(self._column_index(column), str(value))

    def heading(self, column: str, **kwargs) -> Any:
        idx = self._column_index(column)
        if "text" in kwargs:
            self._qt.headerItem().setText(idx, str(kwargs["text"]))
        if "command" in kwargs:
            self._heading_commands[column] = kwargs["command"]
            header = self._qt.header()
            header.sectionClicked.connect(lambda c, col=column: self._on_heading_click(col))

    def _on_heading_click(self, column: str) -> None:
        cmd = self._heading_commands.get(column)
        if cmd:
            cmd()

    def column(self, column: str, **kwargs) -> Any:
        idx = self._column_index(column)
        self._column_configs[column] = kwargs
        header = self._qt.header()
        if "width" in kwargs:
            header.resizeSection(idx, int(kwargs["width"]))
        if "minwidth" in kwargs:
            header.setMinimumSectionSize(int(kwargs["minwidth"]))
        if "stretch" in kwargs:
            if str(kwargs["stretch"]).upper() == "NO":
                header.setSectionResizeMode(idx, QHeaderView.ResizeMode.Fixed)
            else:
                header.setSectionResizeMode(idx, QHeaderView.ResizeMode.Stretch)
        if not kwargs:
            return self._column_configs.get(column, {})
        return None

    def _column_index(self, column: str) -> int:
        if column == "#0":
            return 0
        if column in self._columns:
            return self._columns.index(column)
        try:
            return int(column)
        except ValueError:
            return 0

    def get_children(self, item: str = "") -> tuple:
        if item == "":
            return tuple(
                self._items[iid].data(0, Qt.ItemDataRole.UserRole)
                for iid in self._items
                if self._items[iid].parent() is None
            )
        parent = self._items.get(item)
        if parent is None:
            return ()
        return tuple(
            parent.child(i).data(0, Qt.ItemDataRole.UserRole)
            for i in range(parent.childCount())
        )

    def selection(self) -> tuple:
        return tuple(
            item.data(0, Qt.ItemDataRole.UserRole)
            for item in self._qt.selectedItems()
        )

    def identify_row(self, y: int) -> str:
        item = self._qt.itemAt(0, int(y))
        if item:
            iid = item.data(0, Qt.ItemDataRole.UserRole)
            return str(iid) if iid else ""
        return ""

    def identify_column(self, x: int) -> str:
        idx = self._qt.header().logicalIndexAt(int(x))
        if 0 <= idx < len(self._columns):
            return self._columns[idx]
        return ""

    def bbox(self, item_id: str, column: str | None = None) -> tuple | str:
        qt_item = self._items.get(item_id)
        if qt_item is None:
            return ""
        rect = self._qt.visualItemRect(qt_item)
        return (rect.x(), rect.y(), rect.width(), rect.height())

    def yview(self, *args) -> tuple | None:
        sb = self._qt.verticalScrollBar()
        if args:
            if args[0] == "moveto":
                sb.setValue(int(float(args[1]) * sb.maximum()))
            return None
        mx = max(sb.maximum(), 1)
        page = self._qt.viewport().height()
        total = max(self._qt.topLevelItemCount() * 20, 1)
        first = sb.value() / mx
        last = min(1.0, (sb.value() + page) / total)
        return (first, last)

    def move(self, item_id: str, parent: str, index: int) -> None:
        qt_item = self._items.get(item_id)
        if qt_item is None:
            return
        self._qt.takeTopLevelItem(self._qt.indexOfTopLevelItem(qt_item))
        self._qt.insertTopLevelItem(int(index), qt_item)

    def delete(self, *items: str) -> None:
        for iid in items:
            qt_item = self._items.pop(iid, None)
            if qt_item:
                idx = self._qt.indexOfTopLevelItem(qt_item)
                if idx >= 0:
                    self._qt.takeTopLevelItem(idx)

    def bind(self, sequence: str, func: Callable, add: bool | None = None) -> str:
        if sequence == "<<TreeviewSelect>>":
            self._qt.itemSelectionChanged.connect(lambda: func(_TreeEvent(self)))
            return sequence
        return super().bind(sequence, func, add)


class _TreeEvent:
    def __init__(self, widget):
        self.widget = widget

class _ProgressProxy:
    def __init__(self, bar: "Progressbar"):
        self._bar = bar

    def __getitem__(self, key: str) -> Any:
        if key == "value":
            if self._bar._variable:
                return self._bar._variable.get()
            return self._bar._qt.value()
        raise KeyError(key)

    def __setitem__(self, key: str, value: Any) -> None:
        if key == "value":
            if self._bar._variable:
                self._bar._variable.set(float(value))
            else:
                self._bar._qt.setValue(int(float(value)))


class Progressbar(BaseWidget):
    def __init__(self, master: Any = None, **kwargs):
        self._init_base(master)
        self._qt = QProgressBar()
        self._variable: DoubleVar | None = None
        self._proxy = _ProgressProxy(self)
        self._options = {}
        self._apply_initial_config(**kwargs)

    def _get_qt_widget(self) -> QProgressBar:
        return self._qt

    def _apply_initial_config(self, **kwargs) -> None:
        for key, value in kwargs.items():
            self._apply_option(key, value)

    def __getitem__(self, key: str) -> Any:
        return self._proxy[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self._proxy[key] = value

    def _apply_option(self, key: str, value: Any) -> None:
        self._options[key] = value
        if key == "variable":
            self._variable = value
            if value is not None:
                self._qt.setValue(int(float(value.get())))
                value.add_observer(lambda: self._qt.setValue(int(float(value.get()))))
        elif key == "maximum":
            self._qt.setMaximum(int(value))
        elif key == "orient":
            pass
        elif key == "mode":
            if value == "indeterminate":
                self._qt.setRange(0, 0)
            else:
                self._qt.setRange(0, self._qt.maximum() or 100)
        elif key == "length":
            self._qt.setMinimumWidth(int(value))


class Notebook(BaseWidget):
    def __init__(self, master: Any = None, **kwargs):
        self._init_base(master)
        self._qt = QTabWidget()
        self._tabs: dict[str, QWidget] = {}
        self._options = {}
        self._apply_initial_config(**kwargs)

    def _get_qt_widget(self) -> QTabWidget:
        return self._qt

    def add(self, child: Any, **kwargs) -> None:
        text = kwargs.get("text", "")
        qt = child._get_qt_widget()
        self._qt.addTab(qt, str(text))

    def select(self, tab_id: int | None = None) -> int:
        if tab_id is None:
            return self._qt.currentIndex()
        self._qt.setCurrentIndex(int(tab_id))
        return int(tab_id)

    def _apply_initial_config(self, **kwargs) -> None:
        for key, value in kwargs.items():
            self._apply_option(key, value)

    def _apply_option(self, key: str, value: Any) -> None:
        self._options[key] = value
