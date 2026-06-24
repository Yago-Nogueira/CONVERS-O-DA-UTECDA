"""
PyQt6 UI utility module.

Provides widget classes, layout helpers, and variable bindings
for building desktop applications with PyQt6.
"""

from __future__ import annotations

from . import filedialog, font, messagebox, ttk
from ._app import get_app, mainloop
from ._base import AppError

# Alias
TclError = AppError
from ._image import PhotoImage
from ._matplotlib import FigureCanvasQTAgg, NavigationToolbar2QT

# Aliases
FigureCanvasTkAgg = FigureCanvasQTAgg
NavigationToolbar2Tk = NavigationToolbar2QT
from ._variables import BooleanVar, DoubleVar, IntVar, StringVar, Variable
from ._widgets import (
    Button,
    Canvas,
    Checkbutton,
    Entry,
    Frame,
    Label,
    Listbox,
    Menu,
    Menubutton,
    Radiobutton,
    Scale,
    Scrollbar,
    Spinbox,
    Text,
)
from ._windows import Tk, Toplevel

# Layout / anchor constants
BOTH = "both"
X = "x"
Y = "y"
LEFT = "left"
RIGHT = "right"
TOP = "top"
BOTTOM = "bottom"
HORIZONTAL = "horizontal"
VERTICAL = "vertical"
END = "end"
RIDGE = "ridge"
GROOVE = "groove"
SUNKEN = "sunken"
SOLID = "solid"
DISABLED = "disabled"
NORMAL = "normal"
TRUE = True
FALSE = False
NO = "no"
YES = "yes"
W = "w"
E = "e"
N = "n"
S = "s"
NW = "nw"
NE = "ne"
SW = "sw"
SE = "se"
EW = "ew"
NS = "ns"
NSEW = "nsew"
WORD = "word"
CENTER = "center"
NONE = "none"
BROWSE = "browse"
EXTENDED = "extended"
INSERT = "insert"

__all__ = [
    "BOTH",
    "BOTTOM",
    "BROWSE",
    "Button",
    "Canvas",
    "Checkbutton",
    "CENTER",
    "DISABLED",
    "DoubleVar",
    "E",
    "END",
    "EW",
    "EXTENDED",
    "Entry",
    "FALSE",
    "FigureCanvasQTAgg",
    "Frame",
    "GROOVE",
    "HORIZONTAL",
    "INSERT",
    "IntVar",
    "Label",
    "LEFT",
    "Listbox",
    "Menu",
    "Menubutton",
    "NE",
    "NO",
    "NONE",
    "NORMAL",
    "NS",
    "NSEW",
    "NW",
    "NavigationToolbar2QT",
    "PhotoImage",
    "Radiobutton",
    "RIDGE",
    "RIGHT",
    "S",
    "SE",
    "SOLID",
    "SUNKEN",
    "Scale",
    "Scrollbar",
    "Spinbox",
    "StringVar",
    "SW",
    "AppError",
    "Text",
    "Tk",
    "TOP",
    "TRUE",
    "Toplevel",
    "Variable",
    "VERTICAL",
    "W",
    "WORD",
    "X",
    "Y",
    "YES",
    "BooleanVar",
    "filedialog",
    "font",
    "get_app",
    "mainloop",
    "messagebox",
    "ttk",
]
