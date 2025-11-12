#!/usr/bin/env python
"""Verifica se a planilha foi criada com colunas"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from sheets.models import Sheet, Column

# Verificar planilha 24
try:
    sheet = Sheet.objects.get(id=24)
    print(f"✅ Planilha encontrada: {sheet.id} - {sheet.nome}")
    print(f"   Board: {sheet.board.nome}")
    print(f"   Tipo: {sheet.tipo}")
    print(f"   Total de colunas: {sheet.columns.count()}")
    
    if sheet.columns.count() > 0:
        print("\n📊 Colunas:")
        for col in sheet.columns.all():
            print(f"   - {col.nome} (order={col.order}, editavel={col.editavel})")
    else:
        print("\n❌ NENHUMA COLUNA ENCONTRADA!")
        
except Sheet.DoesNotExist:
    print("❌ Planilha 24 não existe no banco de dados!")

# Verificar todas as planilhas
print(f"\n📋 Total de planilhas no banco: {Sheet.objects.count()}")
print(f"📊 Total de colunas no banco: {Column.objects.count()}")
