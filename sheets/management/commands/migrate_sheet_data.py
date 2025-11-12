"""
Comando para migrar dados de JSONField para estrutura relacional
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from sheets.models import Sheet, Column, Row, Cell


class Command(BaseCommand):
    help = 'Migra dados de colunas/linhas JSONField para estrutura relacional'

    def handle(self, *args, **options):
        sheets = Sheet.objects.all()
        
        for sheet in sheets:
            self.stdout.write(f"Processando sheet: {sheet.nome} (ID: {sheet.id})")
            
            # Verificar se já tem colunas relacionais
            if sheet.columns.exists():
                self.stdout.write(self.style.WARNING(f"  Sheet já possui colunas relacionais. Pulando..."))
                continue
            
            # Migrar colunas
            colunas_json = sheet.colunas or []
            if not colunas_json:
                self.stdout.write(self.style.WARNING(f"  Sem colunas para migrar"))
                continue
            
            with transaction.atomic():
                # Criar colunas
                columns_created = []
                for idx, col in enumerate(colunas_json):
                    if isinstance(col, dict):
                        nome = col.get('nome', f'Coluna {idx+1}')
                        editavel = col.get('editavel', True)
                    else:
                        nome = col
                        editavel = True
                    
                    column = Column.objects.create(
                        sheet=sheet,
                        nome=nome,
                        order=idx,
                        editavel=editavel
                    )
                    columns_created.append(column)
                    self.stdout.write(f"    ✓ Coluna criada: {nome}")
                
                # Migrar linhas
                linhas_json = sheet.linhas or []
                for row_idx, linha in enumerate(linhas_json):
                    # Criar linha
                    row = Row.objects.create(
                        sheet=sheet,
                        order=row_idx,
                        is_subrow=False
                    )
                    
                    # Criar células
                    for column in columns_created:
                        valor = ''
                        if isinstance(linha, dict):
                            valor = linha.get(column.nome, '')
                        
                        Cell.objects.create(
                            row=row,
                            column=column,
                            value=valor
                        )
                    
                    self.stdout.write(f"    ✓ Linha {row_idx+1} migrada com {len(columns_created)} células")
                
                self.stdout.write(self.style.SUCCESS(f"  ✓ Sheet migrada com sucesso!"))
        
        self.stdout.write(self.style.SUCCESS("\n✓ Migração concluída!"))
