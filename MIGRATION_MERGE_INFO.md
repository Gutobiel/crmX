# Merge de Migrações - Elements App

## 📋 Resumo
Resolução de conflito de migrações no app `elements` através do merge das migrações `0003`.

## 🔧 O que foi feito

### 1. Conflito Identificado
Duas migrações foram criadas com o mesmo número (0003):
- `0003_alter_contratoselement_options_and_more.py` - Alterações estruturais nos modelos
- `0003_contratoselement_status.py` - Adição do campo `status` ao modelo ContratosElement

### 2. Resolução
Criada migração de merge: `0004_merge_20251125_1524.py`
- **Data:** 25/11/2025
- **Tipo:** Merge migration (resolve conflito)
- **Impacto:** Nenhum dado é alterado ou perdido
- **Branch:** feature/status-field
- **Commit:** 509b79e

### 3. Alterações no Banco de Dados
A migração `0003_contratoselement_status` adiciona:
- **Campo:** `status` na tabela `elements_contratoselement`
- **Tipo:** CharField com choices
- **Valores possíveis:** ativo, inativo, em andamento, finalizado, etc.
- **Nullable:** Sim (permite null inicialmente)

## ⚠️ IMPORTANTE - Banco de Dados Local

### O que NÃO foi enviado ao Git:
- ❌ `db.sqlite3` - Banco de dados está no `.gitignore`
- ❌ Dados dos 23 contratos existentes
- ❌ Usuários e permissões configuradas

### Cada desenvolvedor tem seu próprio banco local:
Todos os desenvolvedores precisam executar as migrações no ambiente local:

```bash
# Após git pull
python manage.py migrate
```

### Dados de Teste
Os seguintes dados existem APENAS no ambiente local (Brunodev):
- 23 contratos cadastrados
- Usuário: Brunodev (superuser)
- Subelementos vinculados aos contratos

**Esses dados NÃO estarão disponíveis para outros desenvolvedores.**

## 🚀 Como Atualizar (Para Outros Desenvolvedores)

### Passo 1: Puxar as alterações
```bash
git pull origin feature/status-field
```

### Passo 2: Aplicar migrações
```bash
python manage.py migrate
```

### Passo 3: Verificar status
```bash
python manage.py showmigrations elements
```

Todas as migrações devem aparecer com `[X]`:
```
[X]  elements.0001_initial
[X]  elements.0002_contratoselement_elementfreelancer_and_more
[X]  elements.0003_alter_contratoselement_options_and_more
[X]  elements.0003_contratoselement_status
[X]  elements.0004_merge_20251125_1524
```

### Passo 4: Criar dados de teste (opcional)
Se necessário, cada desenvolvedor deve criar seus próprios dados:
- Criar usuário: `python manage.py createsuperuser`
- Adicionar contratos via interface web ou Django shell

## 📊 Estrutura Atual do Banco

### Tabelas Principais:
- `elements_contratoselement` - Contratos (23 registros localmente)
- `subelements_contratossubelement` - Subelementos dos contratos
- `sheets_sheet` - Planilhas
- `boards_board` - Boards/Quadros
- `users_user` - Usuários
- `workspaces_workspace` - Workspaces

### Campo Novo:
**ContratosElement.status**
- Permite categorizar contratos por status
- Uso futuro: filtros, relatórios, workflows

## ✅ Verificação

### Confirmar que não há erros:
```bash
python manage.py check
```

### Testar servidor:
```bash
python manage.py runserver
```

O servidor deve iniciar sem avisos de migrações pendentes.

## 📝 Notas Técnicas

1. **Arquivos .pyc**: Todos os `__pycache__` estão no `.gitignore` e não são versionados
2. **db.sqlite3**: Banco de dados local, cada desenvolvedor tem o seu
3. **Migrations**: Apenas arquivos `.py` em `*/migrations/` são versionados
4. **UTF-8 BOM**: Corrigido anteriormente, todos os arquivos estão em UTF-8 sem BOM

## 🐛 Troubleshooting

### Se encontrar erro de migração conflitante:
```bash
python manage.py migrate --fake elements 0004_merge_20251125_1524
```

### Se precisar resetar migrações (CUIDADO - perde dados):
```bash
# NÃO recomendado em produção
python manage.py migrate elements zero
python manage.py migrate elements
```

### Verificar estado do banco:
```bash
python manage.py dbshell
.tables
.schema elements_contratoselement
```

---

**Autor:** Brunodev  
**Data:** 25/11/2025  
**Branch:** feature/status-field  
**Commit:** 509b79e
