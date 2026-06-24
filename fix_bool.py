#!/usr/bin/env python3
import re

files = ['UTECDA.py', 'principal.py', 'recon.py']

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    old_content = content
    
    # Convert tk.TRUE and tk.FALSE
    content = re.sub(r'\btk\.TRUE\b', 'True', content)
    content = re.sub(r'\btk\.FALSE\b', 'False', content)
    
    if content != old_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ {filepath} - tk.TRUE/FALSE converted")
    else:
        print(f"⚠️  {filepath} - No tk.TRUE/FALSE found")
