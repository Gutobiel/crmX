# Generated migration

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sheets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sheet',
            name='tipo',
            field=models.CharField(
                choices=[
                    ('generico', 'Genérico'),
                    ('contratos', 'Contratos'),
                    ('colaboradores', 'Colaboradores'),
                    ('produtos', 'Produtos')
                ],
                default='generico',
                max_length=20,
                verbose_name='Tipo de Planilha'
            ),
        ),
        migrations.AddField(
            model_name='sheet',
            name='colunas',
            field=models.JSONField(
                blank=True,
                default=list,
                help_text='Lista de dicionários com nome, tipo e editável de cada coluna',
                verbose_name='Configuração das Colunas'
            ),
        ),
        migrations.AddField(
            model_name='sheet',
            name='linhas',
            field=models.JSONField(
                blank=True,
                default=list,
                help_text='Lista de linhas com os dados da planilha',
                verbose_name='Dados das Linhas'
            ),
        ),
    ]
