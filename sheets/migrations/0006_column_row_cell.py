# Generated migration for new relational structure

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sheets', '0005_sheet_linhas'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sheet',
            options={'ordering': ['created_at'], 'verbose_name': 'Planilha', 'verbose_name_plural': 'Planilhas'},
        ),
        migrations.AlterField(
            model_name='sheet',
            name='colunas',
            field=models.JSONField(blank=True, default=list, help_text='Use o modelo Column relacionado', verbose_name='Configuração das Colunas (deprecated)'),
        ),
        migrations.AlterField(
            model_name='sheet',
            name='linhas',
            field=models.JSONField(blank=True, default=list, help_text='Use o modelo Row relacionado', verbose_name='Linhas de Dados (deprecated)'),
        ),
        migrations.CreateModel(
            name='Column',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255, verbose_name='Nome da Coluna')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Ordem')),
                ('editavel', models.BooleanField(default=True, verbose_name='Editável')),
                ('sheet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='columns', to='sheets.sheet', verbose_name='Planilha')),
            ],
            options={
                'verbose_name': 'Coluna',
                'verbose_name_plural': 'Colunas',
                'ordering': ['sheet', 'order'],
                'unique_together': {('sheet', 'order')},
            },
        ),
        migrations.CreateModel(
            name='Row',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Ordem')),
                ('is_subrow', models.BooleanField(default=False, verbose_name='É Sub-linha')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subrows', to='sheets.row', verbose_name='Linha Pai')),
                ('sheet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rows', to='sheets.sheet', verbose_name='Planilha')),
            ],
            options={
                'verbose_name': 'Linha',
                'verbose_name_plural': 'Linhas',
                'ordering': ['sheet', 'order'],
            },
        ),
        migrations.CreateModel(
            name='Cell',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField(blank=True, default='', verbose_name='Valor')),
                ('column', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cells', to='sheets.column', verbose_name='Coluna')),
                ('row', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cells', to='sheets.row', verbose_name='Linha')),
            ],
            options={
                'verbose_name': 'Célula',
                'verbose_name_plural': 'Células',
                'unique_together': {('row', 'column')},
            },
        ),
    ]
