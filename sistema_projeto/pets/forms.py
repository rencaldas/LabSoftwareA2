from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .models import Pet, Adocao
import re

# =============== FORMULÁRIO PERSONALIZADO PARA EDIÇÃO DE DADOS DO USUÁRIO ===============
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')  # os campos que o usuário pode editar

# ==========================================================================================

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['nome', 'idade', 'raca', 'especie', 'descricao', 'foto']
        widgets = {
            'descricao': forms.Textarea(attrs={
                'class': 'descricao-textarea',
                'rows': 4,
                'style': 'overflow-y:hidden; resize:none;'
            }),
        }

class AdocaoForm(forms.ModelForm):
    nome_adotante = forms.CharField(
        label='Nome',
        error_messages={'required': 'Este campo é obrigatório. Por favor, informe seu nome completo.'},
        widget=forms.TextInput(attrs={'placeholder': 'Digite seu nome completo'})
    )
    cpf_adotante = forms.CharField(
        label='CPF',
        error_messages={'required': 'Este campo é obrigatório. Por favor, informe seu CPF.'},
        widget=forms.TextInput(attrs={'maxlength': 14, 'placeholder': '000.000.000-00'})
    )
    rg_adotante = forms.CharField(
        label='RG',
        error_messages={'required': 'Este campo é obrigatório. Por favor, informe seu RG.'},
        widget=forms.TextInput(attrs={'maxlength': 12, 'placeholder': '00.000.000-0'})
    )
    telefone_adotante = forms.CharField(
        label='Telefone',
        error_messages={'required': 'Este campo é obrigatório. Por favor, informe seu telefone.'},
        widget=forms.TextInput(attrs={'maxlength': 15, 'placeholder': '(00) 00000-0000'})
    )
    comprovante_residencia = forms.FileField(
        label='Comprovante de Residência',
        error_messages={'required': 'Este campo é obrigatório.'}
    )

    class Meta:
        model = Adocao
        fields = ['nome_adotante', 'cpf_adotante', 'rg_adotante', 'telefone_adotante', 'comprovante_residencia']

    def clean_cpf_adotante(self):
        cpf = self.cleaned_data.get('cpf_adotante', '').strip()
        cpf_numbers = re.sub(r'\D', '', cpf)
        if len(cpf_numbers) != 11:
            raise forms.ValidationError("Por favor, informe um CPF válido com 11 dígitos.")
        return cpf

    def clean_rg_adotante(self):
        rg = self.cleaned_data.get('rg_adotante', '').strip()
        rg_numbers = re.sub(r'\D', '', rg)
        if len(rg_numbers) < 8:
            raise forms.ValidationError("Por favor, informe um RG válido com pelo menos 8 dígitos.")
        return rg

    def clean_telefone_adotante(self):
        telefone = self.cleaned_data.get('telefone_adotante', '').strip()
        telefone_numbers = re.sub(r'\D', '', telefone)
        if len(telefone_numbers) < 10:
            raise forms.ValidationError("Por favor, informe um telefone válido com DDD e número.")
        return telefone
