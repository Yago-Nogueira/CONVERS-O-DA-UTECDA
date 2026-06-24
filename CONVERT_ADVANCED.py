#!/usr/bin/env python3
"""
Advanced UTECDA Tkinter to PyQt6 Converter
Handles complex conversions like .pack(), .grid(), .bind(), constants
"""

import re
import os
from pathlib import Path

class AdvancedConverter:
    def __init__(self):
        self.files = ['UTECDA.py', 'principal.py', 'recon.py']
        self.changes_log = []
        
    def convert_file(self, filepath):
        """Convert a single file with advanced patterns"""
        print(f"\n{'='*60}")
        print(f"Converting: {filepath}")
        print(f"{'='*60}")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            original_content = content
            
            # Apply conversions in order
            content = self.convert_tk_constants(content)
            content = self.convert_stringvar_intvar(content)
            content = self.convert_pack_layout_simple(content)
            content = self.convert_tk_module_references(content)
            
            # Write back if changed
            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ {filepath} - CONVERTIDO COM SUCESSO")
                return True
            else:
                print(f"⚠️  {filepath} - Nenhuma mudança necessária")
                return False
                
        except Exception as e:
            print(f"❌ Error processing {filepath}: {e}")
            return False
    
    def convert_tk_constants(self, content):
        """Convert tk.* constants to PyQt6 equivalents"""
        
        # Horizontal/Vertical orientation
        replacements = [
            # Orientation
            (r'\btk\.HORIZONTAL\b', 'Qt.Orientation.Horizontal'),
            (r'\btk\.VERTICAL\b', 'Qt.Orientation.Vertical'),
            
            # Sides
            (r'\bside\s*=\s*["\']?tk\.LEFT["\']?', 'side="left"'),
            (r'\bside\s*=\s*["\']?tk\.RIGHT["\']?', 'side="right"'),
            (r'\bside\s*=\s*["\']?tk\.TOP["\']?', 'side="top"'),
            (r'\bside\s*=\s*["\']?tk\.BOTTOM["\']?', 'side="bottom"'),
            
            # Fill options
            (r'\bfill\s*=\s*tk\.BOTH\b', 'fill="both"'),
            (r'\bfill\s*=\s*tk\.X\b', 'fill="x"'),
            (r'\bfill\s*=\s*tk\.Y\b', 'fill="y"'),
            (r'\bfill\s*=\s*tk\.NONE\b', 'fill="none"'),
            
            # Relief options
            (r'\brelief\s*=\s*tk\.FLAT\b', 'relief="flat"'),
            (r'\brelief\s*=\s*tk\.RAISED\b', 'relief="raised"'),
            (r'\brelief\s*=\s*tk\.SUNKEN\b', 'relief="sunken"'),
            (r'\brelief\s*=\s*tk\.GROOVE\b', 'relief="groove"'),
            (r'\brelief\s*=\s*tk\.RIDGE\b', 'relief="ridge"'),
            
            # Color constants
            (r'\btk\.BLUE\b', '"blue"'),
            (r'\btk\.RED\b', '"red"'),
            (r'\btk\.GREEN\b', '"green"'),
            (r'\btk\.BLACK\b', '"black"'),
            (r'\btk\.WHITE\b', '"white"'),
            
            # Anchor options
            (r'\banchor\s*=\s*tk\.CENTER\b', 'anchor="center"'),
            (r'\banchor\s*=\s*tk\.W\b', 'anchor="w"'),
            (r'\banchor\s*=\s*tk\.E\b', 'anchor="e"'),
            (r'\banchor\s*=\s*tk\.N\b', 'anchor="n"'),
            (r'\banchor\s*=\s*tk\.S\b', 'anchor="s"'),
            
            # Justify
            (r'\bjustify\s*=\s*tk\.LEFT\b', 'justify="left"'),
            (r'\bjustify\s*=\s*tk\.CENTER\b', 'justify="center"'),
            (r'\bjustify\s*=\s*tk\.RIGHT\b', 'justify="right"'),
        ]
        
        for pattern, replacement in replacements:
            old_count = len(re.findall(pattern, content))
            content = re.sub(pattern, replacement, content)
            if old_count > 0:
                print(f"  ✓ {pattern[:30]:30s} -> {replacement[:30]:30s}  ({old_count}x)")
        
        return content
    
    def convert_stringvar_intvar(self, content):
        """Convert StringVar, IntVar, BooleanVar to Python types"""
        
        # StringVar()
        pattern = r'tk\.StringVar\(\)'
        old_count = len(re.findall(pattern, content))
        content = re.sub(pattern, '""', content)
        if old_count > 0:
            print(f"  ✓ tk.StringVar() -> \"\"  ({old_count}x)")
        
        # IntVar()
        pattern = r'tk\.IntVar\(\)'
        old_count = len(re.findall(pattern, content))
        content = re.sub(pattern, '0', content)
        if old_count > 0:
            print(f"  ✓ tk.IntVar() -> 0  ({old_count}x)")
        
        # BooleanVar()
        pattern = r'tk\.BooleanVar\(\)'
        old_count = len(re.findall(pattern, content))
        content = re.sub(pattern, 'False', content)
        if old_count > 0:
            print(f"  ✓ tk.BooleanVar() -> False  ({old_count}x)")
        
        return content
    
    def convert_pack_layout_simple(self, content):
        """Simple conversion of .pack() and .grid() - marks for manual review"""
        
        # Add comment markers for .pack() - these need manual review
        pattern = r'(\w+)\.pack\s*\('
        def pack_replacer(match):
            var_name = match.group(1)
            return f'{var_name}.pack(  # CONVERT_PACK'
        
        old_count = len(re.findall(pattern, content))
        content = re.sub(pattern, pack_replacer, content)
        if old_count > 0:
            print(f"  ⚠️  .pack() marked for manual conversion  ({old_count}x)")
        
        # Add comment markers for .grid() - these need manual review
        pattern = r'(\w+)\.grid\s*\('
        def grid_replacer(match):
            var_name = match.group(1)
            return f'{var_name}.grid(  # CONVERT_GRID'
        
        old_count = len(re.findall(pattern, content))
        content = re.sub(pattern, grid_replacer, content)
        if old_count > 0:
            print(f"  ⚠️  .grid() marked for manual conversion  ({old_count}x)")
        
        return content
    
    def convert_tk_module_references(self, content):
        """Convert tk.* module references"""
        
        # Replace tk.NORMAL, tk.DISABLED, tk.ACTIVE
        replacements = [
            (r'\btk\.NORMAL\b', '"normal"'),
            (r'\btk\.DISABLED\b', '"disabled"'),
            (r'\btk\.ACTIVE\b', '"active"'),
            (r'\btk\.END\b', 'END'),  # Usually used with text widgets
        ]
        
        for pattern, replacement in replacements:
            old_count = len(re.findall(pattern, content))
            content = re.sub(pattern, replacement, content)
            if old_count > 0:
                print(f"  ✓ {pattern:30s} -> {replacement:30s}  ({old_count}x)")
        
        return content
    
    def run(self):
        """Run conversion on all files"""
        print("\n" + "="*60)
        print("ADVANCED UTECDA TKINTER → PYQT6 CONVERTER")
        print("="*60)
        
        converted = 0
        for filepath in self.files:
            if os.path.exists(filepath):
                if self.convert_file(filepath):
                    converted += 1
            else:
                print(f"❌ File not found: {filepath}")
        
        print("\n" + "="*60)
        print(f"Conversion complete! {converted}/{len(self.files)} files updated")
        print("="*60)
        print("\n⚠️  IMPORTANT:")
        print("   1. .pack() and .grid() are marked with # CONVERT_PACK/CONVERT_GRID")
        print("   2. Manual review and conversion needed for layouts")
        print("   3. .bind() needs manual conversion to .connect()")
        print("   4. Test the application after manual fixes")


if __name__ == "__main__":
    converter = AdvancedConverter()
    converter.run()
