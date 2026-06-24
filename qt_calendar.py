"""DateEntry widget compatible with tkcalendar using PyQt6."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from PyQt6.QtCore import QDate, QLocale, Qt
from PyQt6.QtWidgets import QDateEdit, QWidget

from qt_ui._base import BaseWidget
from qt_ui._variables import StringVar


class DateEntry(BaseWidget):
    """QDateEdit with calendar popup, mimicking tkcalendar.DateEntry."""

    def __init__(self, master: Any = None, **kwargs):
        self._init_base(master)
        self._qt = QDateEdit()
        self._qt.setCalendarPopup(True)
        self._textvariable: StringVar | None = None
        self._date_pattern = kwargs.pop("date_pattern", "dd/mm/yyyy")
        self._locale_name = kwargs.pop("locale", None)
        self._options = {}

        if self._locale_name:
            locale = QLocale(self._locale_name)
            self._qt.setLocale(locale)

        self._qt.dateChanged.connect(self._on_date_changed)
        self._apply_initial_config(**kwargs)

    def _get_qt_widget(self) -> QDateEdit:
        return self._qt

    def _apply_initial_config(self, **kwargs) -> None:
        for key, value in kwargs.items():
            self._apply_option(key, value)
        if self._textvariable and self._textvariable.get():
            self._set_from_string(self._textvariable.get())

    def _apply_option(self, key: str, value: Any) -> None:
        self._options[key] = value
        if key in ("textvariable", "variable"):
            self._textvariable = value
            if value is not None and value.get():
                self._set_from_string(value.get())
                value.add_observer(lambda: self._set_from_string(value.get()))
        elif key in ("bg", "background"):
            self._apply_bg_fg(self._qt, bg=value)
        elif key in ("fg", "foreground"):
            self._apply_bg_fg(self._qt, fg=value)
        elif key == "borderwidth":
            self._qt.setStyleSheet(self._qt.styleSheet() + f" QDateEdit {{ border-width: {int(value)}px; }}")

    def _set_from_string(self, text: str) -> None:
        try:
            dt = datetime.strptime(text.strip(), "%d/%m/%Y")
            self._qt.setDate(QDate(dt.year, dt.month, dt.day))
        except ValueError:
            pass

    def _on_date_changed(self, qdate: QDate) -> None:
        formatted = self.get()
        if self._textvariable and self._textvariable.get() != formatted:
            self._textvariable.set(formatted)
        self.event_generate("<<DateEntrySelected>>")

    def get(self) -> str:
        qd = self._qt.date()
        return f"{qd.day():02d}/{qd.month():02d}/{qd.year()}"

    def set_date(self, date) -> None:
        if hasattr(date, "year"):
            self._qt.setDate(QDate(date.year, date.month, date.day))
        elif isinstance(date, datetime):
            self._qt.setDate(QDate(date.year, date.month, date.day))

    def bind(self, sequence: str, func, add=None):
        if sequence == "<<DateEntrySelected>>":
            self._date_selected_callback = func
            self._qt.dateChanged.connect(lambda _: func(_DateEvent(self)))
            return sequence
        return super().bind(sequence, func, add)


class _DateEvent:
    def __init__(self, widget):
        self.widget = widget
