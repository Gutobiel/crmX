from django import forms

from boards.models import Board
from sheets.models import Sheet

from .models import ContratosElement


class ContratosElementForm(forms.ModelForm):
    board = forms.ModelChoiceField(
        queryset=Board.objects.none(),
        required=False,
        label="Pasta",
        empty_label="Selecione uma pasta",
    )
    sheet = forms.ModelChoiceField(
        queryset=Sheet.objects.none(),
        required=False,
        label="Planilha",
        empty_label="Selecione uma planilha",
    )

    class Meta:
        model = ContratosElement
        fields = [
            "elemento",
            "empresa",
            "objeto",
            "qtd_total_itens",
            "valor_total_anterior",
            "valor_total_reajustado",
        ]
        widgets = {
            "objeto": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ajusta atributos básicos para inputs mais consistentes
        text_fields = ["elemento", "empresa"]
        numeric_fields = ["qtd_total_itens", "valor_total_anterior", "valor_total_reajustado"]

        for field_name in text_fields:
            self.fields[field_name].widget.attrs.update({
                "placeholder": "Digite...",
            })

        for field_name in numeric_fields:
            self.fields[field_name].widget.attrs.update({
                "min": 0,
                "step": "any",
            })

        self.fields["objeto"].widget.attrs.update({
            "placeholder": "Descreva o objeto do contrato",
        })

        self.fields["board"].queryset = Board.objects.all().order_by("nome")
        self.fields["sheet"].queryset = Sheet.objects.select_related("board").all().order_by("nome")
