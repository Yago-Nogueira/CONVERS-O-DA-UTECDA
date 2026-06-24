#!/usr/bin/env python3
"""
Automatic converter from Tkinter (qt_ui wrapper) to native PyQt6
This script converts all remaining Tkinter references in the project
"""

import os
import re
from pathlib import Path

# List of files to convert
FILES_TO_CONVERT = [
    'UTECDA.py',
    'principal.py',
    'recon.py',
    'EntryBox.py',
    'qtSimpleDialog.py',
    'maskedentry.py',
    'tkcalendar_Days.py',
    'comp_GRADE_MAPA.py',
    'comp_MAPA.py',
    'ordena.py'
]

# Replacement mappings
REPLACEMENTS = [
    # Import replacements
    ("from qt_ui import NavigationToolbar2Tk as NavigationToolbar", 
     "from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar"),
    
    ("from qt_ui import FigureCanvasTkAgg as FigureCanvas",
     "from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas"),
    
    ("from qt_ui import PhotoImage",
     "from PyQt6.QtGui import QPixmap as PhotoImage"),
    
    ("import qt_ui as tk",
     "from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QFileDialog"),
    
    ("from qt_ui import *",
     "# PyQt6 imports handled explicitly"),
    
    # Class replacements - Toplevel to QDialog
    ("class .*\\(tk\\.Toplevel\\):",
     lambda m: m.group(0).replace("tk.Toplevel", "QDialog")),
    
    ("class .*\\(Toplevel\\):",
     lambda m: m.group(0).replace("Toplevel", "QDialog")),
    
    # Frame replacements
    ("class .*\\(tk\\.Frame\\):",
     lambda m: m.group(0).replace("tk.Frame", "QWidget")),
    
    ("class .*\\(Frame\\):",
     lambda m: m.group(0).replace("Frame", "QWidget")),
    
    # Init replacements
    ("tk\\.Frame\\.__init__\\(self, master\\)",
     "super().__init__(master)"),
    
    ("Toplevel\\.__init__\\(self, master\\)",
     "super().__init__(master)"),
    
    ("tk\\.Toplevel\\.__init__\\(self, master\\)",
     "super().__init__(master)"),
    
    # Variable replacements
    ("= tk\\.StringVar\\(",
     "= \"\"  # was StringVar"),
    
    ("= tk\\.IntVar\\(",
     "= 0  # was IntVar"),
    
    ("= tk\\.BooleanVar\\(",
     "= False  # was BooleanVar"),
    
    # Geometry
    ("self\\.geometry\\(",
     "self.setGeometry("),
    
    # Root mainloop
    ("root\\.mainloop\\(\\)",
     "# mainloop handled by QApplication"),
]

def convert_file(filepath):
    """Convert a single file from Tkinter to PyQt6"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply simple string replacements
        for old, new in REPLACEMENTS:
            if isinstance(new, str):
                content = content.replace(old, new)
            else:  # it's a regex
                content = re.sub(old, new, content)
        
        # Write back if changed
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
        
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    """Main conversion routine"""
    base_path = Path(__file__).parent
    
    print("=" * 60)
    print("UTECDA Tkinter to PyQt6 Converter")
    print("=" * 60)
    
    converted_count = 0
    
    for filename in FILES_TO_CONVERT:
        filepath = base_path / filename
        
        if filepath.exists():
            print(f"\nConverting: {filename}...", end=" ")
            if convert_file(str(filepath)):
                print("✓ DONE")
                converted_count += 1
            else:
                print("(no changes)")
        else:
            print(f"\nSkipping: {filename} (not found)")
    
    print("\n" + "=" * 60)
    print(f"Conversion complete! {converted_count} files updated.")
    print("=" * 60)
    
    print("\nNEXT STEPS:")
    print("1. Review the converted files for any manual adjustments needed")
    print("2. Update event handling: .bind() -> .connect()")
    print("3. Update widget references as needed")
    print("4. Test the application")

if __name__ == "__main__":
    main()
