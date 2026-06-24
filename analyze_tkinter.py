#!/usr/bin/env python3
"""Analyze remaining Tkinter patterns"""
import re

files = ['UTECDA.py', 'principal.py', 'recon.py']
total = {'bind': 0, 'pack': 0, 'grid': 0, 'tk_ref': 0, 'stringvar': 0, 'backend_qt5': 0}

print("=" * 60)
print("ANÁLISE DE PADRÕES TKINTER RESTANTES")
print("=" * 60)
print()

for fname in files:
    try:
        with open(fname, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        bind_count = len(re.findall(r'\.bind\s*\(', content))
        pack_count = len(re.findall(r'\.pack\s*\(', content))
        grid_count = len(re.findall(r'\.grid\s*\(', content))
        tk_count = len(re.findall(r'\btk\.', content))
        stringvar_count = len(re.findall(r'(StringVar|IntVar|BooleanVar)', content))
        backend_qt5_count = len(re.findall(r'backend_qt5', content))
        
        print(f"📄 {fname}")
        print(f"   .bind() calls:        {bind_count}")
        print(f"   .pack() calls:        {pack_count}")
        print(f"   .grid() calls:        {grid_count}")
        print(f"   tk.* references:      {tk_count}")
        print(f"   StringVar/IntVar:     {stringvar_count}")
        if backend_qt5_count > 0:
            print(f"   ⚠️  backend_qt5agg:     {backend_qt5_count}  <- PRECISA CONVERTER PARA qt6agg")
        print()
        
        total['bind'] += bind_count
        total['pack'] += pack_count
        total['grid'] += grid_count
        total['tk_ref'] += tk_count
        total['stringvar'] += stringvar_count
        total['backend_qt5'] += backend_qt5_count
    except Exception as e:
        print(f"❌ Error reading {fname}: {e}")

print("=" * 60)
print("TOTAIS (3 ARQUIVOS PRINCIPAIS)")
print("=" * 60)
print(f".bind() calls:         {total['bind']:3d}  <- Convertir para .connect()")
print(f".pack() calls:         {total['pack']:3d}  <- Convertir para layout.addWidget()")
print(f".grid() calls:         {total['grid']:3d}  <- Convertir para layout")
print(f"tk.* references:       {total['tk_ref']:3d}  <- Convertir constantes")
print(f"StringVar/IntVar:      {total['stringvar']:3d}  <- Convertir a variables Python")
if total['backend_qt5'] > 0:
    print(f"\n⚠️  CRÍTICO: backend_qt5agg encontrado {total['backend_qt5']} vezes")
    print("   SOLUÇÃO: Mudar para 'backend_qt6agg'")
