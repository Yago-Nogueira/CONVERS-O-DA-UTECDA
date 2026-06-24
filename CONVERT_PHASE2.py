#!/usr/bin/env python3
"""
Phase 2: Convert .bind() events and remaining patterns
"""

import re
import os

class BindConverter:
    def __init__(self):
        self.files = ['UTECDA.py', 'principal.py', 'recon.py']
        
    def convert_file(self, filepath):
        """Convert .bind() patterns in a file"""
        print(f"\n{'='*60}")
        print(f"Converting .bind() in: {filepath}")
        print(f"{'='*60}")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            original_lines = lines.copy()
            converted = 0
            
            # Process each line
            for i, line in enumerate(lines):
                # Simple .bind() conversions with markers for manual review
                if '.bind(' in line and '# CONVERT_PACK' not in line:
                    # Mark for manual review
                    if '# CONVERT_BIND' not in line:
                        # Add marker instead of trying to convert
                        lines[i] = line.rstrip() + '  # CONVERT_BIND\n'
                        converted += 1
                
                # Convert remaining StringVar patterns
                if 'StringVar()' in line:
                    lines[i] = line.replace('StringVar()', '""')
                    converted += 1
                
                if 'IntVar()' in line:
                    lines[i] = line.replace('IntVar()', '0')
                    converted += 1
                
                if 'BooleanVar()' in line:
                    lines[i] = line.replace('BooleanVar()', 'False')
                    converted += 1
            
            # Write if changed
            if lines != original_lines:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.writelines(lines)
                print(f"✅ {filepath} - {converted} patterns marked/converted")
                return True
            else:
                print(f"⚠️  {filepath} - No changes needed")
                return False
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def run(self):
        print("\n" + "="*60)
        print("PHASE 2: EVENT BINDING CONVERTER")
        print("="*60)
        
        converted = 0
        for filepath in self.files:
            if os.path.exists(filepath):
                if self.convert_file(filepath):
                    converted += 1
        
        print("\n" + "="*60)
        print(f"Phase 2 complete! {converted}/{len(self.files)} files processed")
        print("="*60)


if __name__ == "__main__":
    converter = BindConverter()
    converter.run()
