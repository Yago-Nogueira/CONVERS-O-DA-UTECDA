# UTECDA - Tkinter para PyQt6 Conversion Guide

## ✅ Conversion Status

### Already Converted ✓
- [x] **Balloon_info.py** - Tooltip widget
- [x] **util.py** - Base utilities and DadoIdioma class (70%)
- [x] **comp_INDV.py** - Individual component (imports)
- [x] **comp_DESVIO.py** - Deviation component (imports)
- [x] **comp_ONDAS.py** - Waves component (imports)
- [x] **comp_ROT.py** - ROT component (imports)
- [x] **comp_EIA.py** - EIA component (imports)
- [x] **cadastrarMAPA.py** - Map registration dialog (imports)
- [x] **cadastrarOBS.py** - OBS registration dialog (imports)

### Partially Converted 🟡
- [ ] **EntryBox.py** - Entry/Dialog widgets (50%)
- [ ] **UTECDA.py** - Main application (0%)
- [ ] **principal.py** - Main interface (0%)
- [ ] **recon.py** - Secondary interface (0%)

### Not Yet Converted ⏳
- [ ] **qtSimpleDialog.py** - Loading dialog
- [ ] **maskedentry.py** - Masked entry widget
- [ ] **tkcalendar_Days.py** - Calendar widget
- [ ] **comp_GRADE_MAPA.py** - Grade map component
- [ ] **comp_MAPA.py** - Map component

---

## 📋 Conversion Roadmap

### Phase 1: Global Import Replacements ✓
```python
# OLD
import qt_ui as tk
from qt_ui import *

# NEW
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QDialog
from PyQt6.QtCore import Qt, QRect, QTimer
from PyQt6.QtGui import QFont, QIcon, QPixmap
```

### Phase 2: Class Conversions
```python
# OLD
class MyDialog(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)

# NEW
from PyQt6.QtWidgets import QDialog
class MyDialog(QDialog):
    def __init__(self, master):
        super().__init__(master)
```

### Phase 3: Widget Conversions

| Tkinter | PyQt6 |
|---------|-------|
| `tk.Frame` | `QWidget` |
| `tk.Toplevel` | `QDialog` |
| `tk.Label` | `QLabel` |
| `tk.Button` | `QPushButton` |
| `tk.Entry` | `QLineEdit` |
| `tk.Text` | `QPlainTextEdit` |
| `tk.Listbox` | `QListWidget` |
| `tk.Canvas` | `QGraphicsView` |
| `tk.Menu` | `QMenu` |
| `tk.StringVar` | `str` variable |
| `tk.IntVar` | `int` variable |
| `tk.BooleanVar` | `bool` variable |

### Phase 4: Event Handling Conversions
```python
# OLD - Tkinter
widget.bind("<Button-1>", callback)
button.pack(fill='x')
window.geometry("800x600")

# NEW - PyQt6
widget.mousePressEvent = callback
layout.addWidget(button)
window.setGeometry(0, 0, 800, 600)
```

### Phase 5: Variable Conversions
```python
# OLD
var = tk.StringVar(self)
var.set("value")
value = var.get()

# NEW
self.var = "value"  # Direct assignment
value = self.var    # Direct access
```

---

## 🔄 Matplotlib Integration

The project uses matplotlib with custom backends. Updates needed:

```python
# OLD
from qt_ui import FigureCanvasTkAgg as FigureCanvas
from qt_ui import NavigationToolbar2Tk as NavigationToolbar

# NEW
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
```

---

## 🛠️ Manual Conversion Steps

### For Each File:

#### 1. Update Imports
```python
# Add these at the top of the file
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QDialog, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QMessageBox, QFileDialog, QTreeWidget, QTreeWidgetItem,
    QComboBox, QSpinBox, QCheckBox, QScrollArea, QFrame, QScrollBar
)
from PyQt6.QtCore import Qt, QRect, QSize, QTimer, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QIcon, QPixmap, QKeySequence

# Remove
# import qt_ui as tk
# from qt_ui import *
```

#### 2. Convert Class Definitions
```python
# Change: class MyClass(tk.Toplevel): → class MyClass(QDialog):
# Change: class MyClass(Frame): → class MyClass(QWidget):
# Change: tk.Frame.__init__(self, master) → super().__init__(master)
```

#### 3. Convert Pack/Grid to Layout
```python
# OLD
button.pack(fill='x')
frame.pack(side='left', expand=True)

# NEW
layout = QVBoxLayout(self)
layout.addWidget(button)
layout.addStretch()
```

#### 4. Convert Geometry Calls
```python
# OLD: self.geometry('800x600+100+50')
# NEW: self.setGeometry(100, 50, 800, 600)
```

#### 5. Update Event Binding
This is more complex - requires connecting signals/slots instead of bind()

---

## 📝 Key Considerations

### 1. Main Application Entry Point
```python
# OLD
if __name__ == "__main__":
    root = tk.Tk()
    app = Main_UTECDA(root)
    root.mainloop()

# NEW
if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys
    
    qapp = QApplication(sys.argv)
    window = Main_UTECDA()
    window.show()
    sys.exit(qapp.exec())
```

### 2. Variables (StringVar, IntVar, etc.)
PyQt6 uses direct Python variables instead of Tkinter variable classes:

```python
# OLD
self.value = tk.StringVar()
self.value.set("test")
print(self.value.get())

# NEW
self.value = "test"
print(self.value)

# For signals/slots with changes:
self.value_changed = pyqtSignal(str)
```

### 3. DialogsMessageBoxes

```python
# OLD
messagebox.showinfo("Title", "Message")

# NEW
QMessageBox.information(self, "Title", "Message")
QMessageBox.warning(self, "Title", "Warning message")
QMessageBox.critical(self, "Title", "Error message")
```

### 4. File Dialogs
```python
# OLD
from qt_ui.filedialog import askdirectory
dir = askdirectory()

# NEW
from PyQt6.QtWidgets import QFileDialog
dir = QFileDialog.getExistingDirectory(self, "Choose Directory")
```

---

## 🚀 Automated Conversion Script

Run the included conversion script to apply global replacements:

```bash
python CONVERT_TO_PYQT6.py
```

This will:
- Replace imports automatically
- Convert class definitions
- Update common patterns
- Generate a report

---

## ✨ Best Practices for PyQt6

1. **Always use layouts** instead of manual positioning
2. **Use signals/slots** for event handling
3. **Keep business logic separate** from UI code
4. **Use QThread** for long-running tasks (already present in code)
5. **Handle closeEvent()** instead of WM_DELETE_WINDOW protocol
6. **Use stylesheets** for styling instead of tk relief/bd parameters

---

## 🧪 Testing Checklist

- [ ] All imports resolve without errors
- [ ] Main window opens and displays
- [ ] All dialogs and secondary windows work
- [ ] File dialogs function correctly
- [ ] Data input fields work
- [ ] Matplotlib graphs render
- [ ] Buttons and menus respond
- [ ] Threading operations work smoothly
- [ ] Error messages display properly
- [ ] Application closes cleanly

---

## 📚 Useful Resources

- PyQt6 Documentation: https://doc.qt.io/qt-6/
- PyQt6 API Reference: https://www.riverbankcomputing.com/static/Docs/PyQt6/
- Matplotlib PyQt6 Backend: https://matplotlib.org/stable/backends/backend_qt.html

---

## 💡 Notes

- The `qt_ui/` wrapper directory can be removed once conversion is complete
- All non-UI logic (calculations, data processing) remains unchanged
- Threading utilities (`thread_with_trace`) work with PyQt6 as-is
- Matplotlib integration continues to work with the new backend

---

## 🎯 Next Steps

1. Review converted files
2. Complete manual conversions for main files (UTECDA.py, principal.py, recon.py)
3. Test the application thoroughly
4. Remove qt_ui dependency
5. Deploy

---

**Created:** 2026-06-23
**Status:** In Progress (45% Complete)
**Estimated Completion:** After manual review and testing
