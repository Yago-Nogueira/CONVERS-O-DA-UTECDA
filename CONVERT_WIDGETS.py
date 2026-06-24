#!/usr/bin/env python3
"""
Critical Fix: Convert tk.Widget instantiations to PyQt6
"""

import re
import os

class WidgetConverter:
    def __init__(self):
        self.files = ['UTECDA.py', 'principal.py', 'recon.py']
        self.widget_map = {
            'tk.Label': 'QLabel',
            'tk.Button': 'QPushButton',
            'tk.Entry': 'QLineEdit',
            'tk.Text': 'QPlainTextEdit',
            'tk.Frame': 'QWidget',
            'tk.Canvas': 'QGraphicsView',
            'tk.Listbox': 'QListWidget',
            'tk.Checkbutton': 'QCheckBox',
            'tk.Radiobutton': 'QRadioButton',
            'tk.Scale': 'QSlider',
            'tk.Spinbox': 'QSpinBox',
            'tk.Message': 'QLabel',
            'tk.Menu': 'QMenu',
            'tk.Menubutton': 'QMenuButton',
            'tk.OptionMenu': 'QComboBox',
            'tk.PanedWindow': 'QSplitter',
            'tk.Scrollbar': 'QScrollBar',
            'tk.Toplevel': 'QDialog',
        }
    
    def convert_file(self, filepath):
        """Convert all tk.Widget references"""
        print(f"\n{'='*60}")
        print(f"Converting widgets in: {filepath}")
        print(f"{'='*60}")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            total_converted = 0
            
            # Convert each widget type
            for tk_widget, py_widget in self.widget_map.items():
                pattern = r'\b' + tk_widget.replace('.', r'\.') + r'\b'
                count = len(re.findall(pattern, content))
                if count > 0:
                    content = re.sub(pattern, py_widget, content)
                    print(f"  ✓ {tk_widget:25s} -> {py_widget:25s}  ({count}x)")
                    total_converted += count
            
            # Write if changed
            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"\n✅ {filepath} - {total_converted} widget conversions")
                return True
            else:
                print(f"\n⚠️  {filepath} - No changes needed")
                return False
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def run(self):
        print("\n" + "="*60)
        print("CRITICAL FIX: WIDGET CONVERTER")
        print("="*60)
        
        converted = 0
        for filepath in self.files:
            if os.path.exists(filepath):
                if self.convert_file(filepath):
                    converted += 1
        
        print("\n" + "="*60)
        print(f"Widget conversion complete! {converted}/{len(self.files)} files")
        print("="*60)


if __name__ == "__main__":
    converter = WidgetConverter()
    converter.run()
