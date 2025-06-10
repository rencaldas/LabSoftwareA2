from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .models import Pet, Adocao, Perfil
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


# =============== FORMULÁRIO PARA EDITAR DADOS DO USUÁRIO (Django User) ===============

class UsuarioForm(forms.ModelForm):
    username = forms.CharField(
        label='Usuário',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu usuário'}),
        required=True
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu email'}),
        required=True
    )
    first_name = forms.CharField(
        label='Primeiro Nome:',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu nome'}),
        required=False
    )
    last_name = forms.CharField(
        label='Sobrenome',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu sobrenome'}),
        required=False
    )
    cpf = forms.CharField(
        label='CPF',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu CPF'}),
        required=False,
    )
    rg = forms.CharField(
        label='RG',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu RG'}),
        required=False,
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'email', 'cpf', 'rg']

class PerfilForm(forms.ModelForm):
    cpf = forms.CharField(
        label='CPF',
        max_length=14,
        widget=forms.TextInput(attrs={
            'placeholder': '123.456.789-00',
            'pattern': r'\d{3}\.\d{3}\.\d{3}-\d{2}',
            'title': 'Digite o CPF no formato 000.000.000-00'
        }),
        required=False
    )
    rg = forms.CharField(
        label='RG',
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': '12.345.678-9'}),
        required=False
    )

    class Meta:
        model = Perfil
        fields = ['cpf', 'rg']