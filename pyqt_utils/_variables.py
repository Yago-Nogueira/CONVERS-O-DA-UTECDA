"""Variable classes backed by Qt signals."""

from __future__ import annotations

from typing import Any, Callable

from PyQt6.QtCore import QObject, pyqtSignal


class _TraceCallback:
    __slots__ = ("mode", "callback", "var_name")

    def __init__(self, mode: str, callback: Callable, var_name: str = ""):
        self.mode = mode
        self.callback = callback
        self.var_name = var_name


class Variable(QObject):
    """Base observable variable with get/set/trace functionality."""

    valueChanged = pyqtSignal(object)

    def __init__(self, master: Any = None, value: Any = None, name: str | None = None):
        super().__init__()
        self._master = master
        self._name = name
        self._value = value
        self._traces: list[_TraceCallback] = []
        self._observers: list[Callable[[], None]] = []

    def get(self) -> Any:
        return self._value

    def set(self, value: Any) -> None:
        if self._value != value:
            self._value = value
            self.valueChanged.emit(value)
            self._run_traces("w")

    def trace_add(self, mode: str, callback: Callable) -> str:
        cb = _TraceCallback(mode, callback, var_name=str(len(self._traces)))
        self._traces.append(cb)
        return cb.var_name

    def trace(self, mode: str, callback: Callable) -> str:
        return self.trace_add(mode, callback)

    def trace_remove(self, mode: str, cbname: str) -> None:
        self._traces = [t for t in self._traces if t.var_name != cbname]

    def trace_vdelete(self, mode: str, cbname: str) -> None:
        self.trace_remove(mode, cbname)

    def _run_traces(self, mode: str) -> None:
        for trace in list(self._traces):
            if trace.mode == mode or trace.mode == "wu":
                trace.callback(self._name, "", mode, self._name or "")

    def add_observer(self, callback: Callable[[], None]) -> None:
        self._observers.append(callback)
        self.valueChanged.connect(callback)

    def __str__(self) -> str:
        return str(self._value) if self._value is not None else ""


class StringVar(Variable):
    def __init__(self, master: Any = None, value: str = "", name: str | None = None):
        super().__init__(master, value, name)


class BooleanVar(Variable):
    def __init__(self, master: Any = None, value: bool = False, name: str | None = None):
        super().__init__(master, bool(value), name)

    def get(self) -> bool:
        return bool(self._value)


class IntVar(Variable):
    def __init__(self, master: Any = None, value: int = 0, name: str | None = None):
        super().__init__(master, int(value), name)

    def get(self) -> int:
        return int(self._value)

    def set(self, value: Any) -> None:
        super().set(int(value))


class DoubleVar(Variable):
    def __init__(self, master: Any = None, value: float = 0.0, name: str | None = None):
        super().__init__(master, float(value), name)

    def get(self) -> float:
        return float(self._value)

    def set(self, value: Any) -> None:
        super().set(float(value))
