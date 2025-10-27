from django.contrib import admin
from .models import ContratosElement
from subElements.models import ContratosSubelement

class ContratosSubelementInline(admin.TabularInline):
    model = ContratosSubelement
    extra = 1  # Quantidade de linhas "em branco" para novo subelemento
    show_change_link = True  # Exibe link para edição separada do subelemento

@admin.register(ContratosElement)
class ContratosElementAdmin(admin.ModelAdmin):
    list_display = ('empresa', 'objeto', 'qtd_total_itens', 'valor_total_anterior', 'valor_total_reajustado')
    search_fields = ('empresa', 'objeto')
    inlines = [ContratosSubelementInline]

@admin.register(ContratosSubelement)
class ContratosSubelementAdmin(admin.ModelAdmin):
    list_display = ('id', 'element', 'nome', 'quantidade', 'valor_total', 'valor_total_reajustado')
    list_filter = ('element__empresa',)
