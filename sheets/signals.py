from django.db.models.signals import post_save
from django.dispatch import receiver
from sheets.models import Sheet


@receiver(post_save, sender=Sheet)
def init_sheet_data(sender, instance: Sheet, created, **kwargs):
    """Ao criar uma Sheet, inicializa suas linhas internas (Sheet.linhas) em vez de criar registros em outros modelos.

    Mantém compatibilidade: não remove ainda os models antigos, apenas deixa de popular.
    Posteriormente poderemos migrar dados existentes para dentro de Sheet.linhas.
    """
    if not created:
        return

    # Definir colunas base conforme tipo (se o cliente não enviou colunas para genérico)
    if instance.tipo == 'generico' and not instance.colunas:
        instance.colunas = []  # usuário poderá adicionar depois

    tipo_colunas_map = {
        'contratos': [
            'Elemento', 'Empresa', 'Objeto', 'Qtd Total Itens', 'Valor Total Anterior', 'Valor Total Reajustado'
        ],
        'colaboradores': [
            'Nome', 'Cargo', 'Salário Bruto', 'Benefício Alimentação', 'Benefício Transporte'
        ],
        'produtos': [
            'Código', 'Nome', 'Categoria', 'Preço', 'Estoque'
        ]
    }

    # Se não for genérico, preencher colunas "visuais" para o frontend (apenas se vazio)
    if instance.tipo != 'generico' and not instance.colunas:
        instance.colunas = [
            {'nome': c, 'editavel': False} for c in tipo_colunas_map.get(instance.tipo, [])
        ]

    # Criar 3 linhas iniciais vazias (cada linha é um dict coluna->valor)
    linhas_iniciais = []
    coluna_nomes = [
        (col['nome'] if isinstance(col, dict) else col)
        for col in instance.colunas
    ]
    for _ in range(3):
        linha = {nome: '' for nome in coluna_nomes}
        linhas_iniciais.append(linha)

    instance.linhas = linhas_iniciais
    instance.save(update_fields=['colunas', 'linhas'])
