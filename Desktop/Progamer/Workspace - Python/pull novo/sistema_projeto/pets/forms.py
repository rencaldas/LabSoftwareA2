from django import forms
from .models import Pet

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['nome', 'idade', 'raca', 'especie', 'descricao', 'foto']
        widgets = {
            'descricao': forms.Textarea(attrs={
                'class': 'descricao-textarea',
                'rows': 4,
                'style': 'overflow-y:hidden; resize:none;'  # evita barra de rolagem e resize manual
            }),
        }
