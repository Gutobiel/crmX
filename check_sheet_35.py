import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from sheets.models import Sheet
from boards.models import Board

# Verificar planilha ID 35
try:
    sheet = Sheet.objects.get(id=35)
    print(f"✅ Planilha ID 35 encontrada!")
    print(f"   Nome: {sheet.nome}")
    print(f"   Tipo: {sheet.tipo}")
    print(f"   Board ID: {sheet.board.id}")
    print(f"   Board Nome: {sheet.board.nome}")
except Sheet.DoesNotExist:
    print("❌ Planilha ID 35 NÃO encontrada no banco!")

print("\n" + "="*60)

# Listar todas as planilhas do Board 6
board6_sheets = Sheet.objects.filter(board_id=6)
print(f"\nPlanilhas do Board 6:")
print(f"Total: {board6_sheets.count()}")
for s in board6_sheets:
    print(f"  - ID {s.id}: {s.nome} (Tipo: {s.tipo})")
