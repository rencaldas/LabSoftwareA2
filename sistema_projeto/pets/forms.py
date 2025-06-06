from django import forms
from .models import Pet, Adocao

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

# Formulário ligado ao modelo Adocao, para salvar os dados no banco:
class AdocaoForm(forms.ModelForm):
    class Meta:
        model = Adocao
        fields = ['nome_adotante', 'email_adotante', 'cpf_adotante']
        labels = {
            'nome_adotante': 'Nome',
            'email_adotante': 'E-mail',
            'cpf_adotante': 'CPF',
        }
        widgets = {
            'cpf_adotante': forms.TextInput(attrs={'maxlength': 14}),
        }
