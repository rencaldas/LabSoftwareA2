from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .models import Pet, Adocao, Perfil
import re


class CustomUserChangeForm(UserChangeForm):
    """
    Form personalizado para permitir que o usuário edite apenas alguns campos básicos.
    - Baseado em UserChangeForm do Django.
    - Limita os campos a first_name, last_name e email.
    """
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class PetForm(forms.ModelForm):
    """
    Form para criar ou editar instâncias de Pet.
    - Campos principais: nome, idade, raca, especie, descricao, foto.
    - O widget de descricao recebe um Textarea customizado (altura fixa e sem redimensionar verticalmente).
    - Se futuramente houver validações específicas (ex.: idade > 0), pode-se adicionar métodos clean_<campo>.
    """
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
    """
    Form para o processo de adoção de um pet.
    - Contém campos do adotante: nome, CPF, RG, telefone e comprovante de residência (arquivo).
    - Implementa validações customizadas para CPF, RG e telefone.
    - Observação: se quiser reutilizar validações de CPF/RG em outros forms, pode extrair validadores separados.
    """
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
        fields = [
            'nome_adotante',
            'cpf_adotante',
            'rg_adotante',
            'telefone_adotante',
            'comprovante_residencia'
        ]

    def clean_cpf_adotante(self):
        """
        Valida se o CPF tem exatamente 11 dígitos numéricos.
        - Remove caracteres não-dígito antes de verificar.
        - Se inválido, gera ValidationError.
        - Retorna a string original (com ou sem pontuação), caso queira armazenar com formatação original.
        """
        cpf = self.cleaned_data.get('cpf_adotante', '').strip()
        nums = re.sub(r'\D', '', cpf)
        if len(nums) != 11:
            raise forms.ValidationError("Por favor, informe um CPF válido com 11 dígitos.")
        # Aqui poderia-se normalizar para armazenar sem pontuação: return nums
        return cpf

    def clean_rg_adotante(self):
        """
        Valida se o RG possui pelo menos 8 dígitos numéricos.
        - Remove caracteres não-dígito antes de verificar.
        """
        rg = self.cleaned_data.get('rg_adotante', '').strip()
        nums = re.sub(r'\D', '', rg)
        if len(nums) < 8:
            raise forms.ValidationError("Por favor, informe um RG válido com pelo menos 8 dígitos.")
        return rg

    def clean_telefone_adotante(self):
        """
        Valida se o telefone contém pelo menos 10 dígitos (incluindo DDD).
        - Remove caracteres não-dígito antes de verificar.
        """
        tel = self.cleaned_data.get('telefone_adotante', '').strip()
        nums = re.sub(r'\D', '', tel)
        if len(nums) < 10:
            raise forms.ValidationError("Por favor, informe um telefone válido com DDD e número.")
        return tel


class UsuarioForm(forms.ModelForm):
    """
    Form para editar dados do User (do Django).
    - Campos: username, email, first_name, last_name, cpf, rg.
    - Observação: por padrão, User não possui campos 'cpf' e 'rg'; se estes não existirem diretamente
      no modelo User, deve-se tratar armazenamento via modelo Perfil ou estender User.
    - Se usar Perfil, ao salvar aqui, é preciso sincronizar com instância de Perfil associada.
    """
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
        label='Primeiro Nome',
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
        # Atenção: 'cpf' e 'rg' não existem no modelo User padrão. Se estiver salvando aqui,
        # é preciso sobrepor o método save() deste form para gravar em Perfil ou em campo extra no User.
        fields = ['username', 'email', 'first_name', 'last_name', 'cpf', 'rg']

    def save(self, commit=True):
        """
        Override do save para sincronizar CPF/RG com modelo Perfil se aplicável.
        - Primeiro salva o User normalmente.
        - Depois, obtém/atualiza instância de Perfil associada e salva cpf/rg.
        """
        user = super().save(commit=commit)
        # Verifica se há modelo Perfil relacionado ao User
        cpf = self.cleaned_data.get('cpf')
        rg = self.cleaned_data.get('rg')
        try:
            perfil = user.perfil  # assumindo OneToOneField em Perfil apontando para User
        except (AttributeError, Perfil.DoesNotExist):
            perfil = None

        if perfil:
            # Atualiza somente se foram fornecidos
            if cpf is not None:
                perfil.cpf = cpf
            if rg is not None:
                perfil.rg = rg
            if commit:
                perfil.save()
        # Se não houver Perfil e quiser criá-lo automaticamente:
        # else:
        #     Perfil.objects.create(user=user, cpf=cpf or '', rg=rg or '')
        return user


import re
from django import forms
from .models import Perfil


class PerfilForm(forms.ModelForm):
    """
    Form para editar dados de perfil adicionais do usuário:
    - Campos: cpf, rg, telefone.
    - Usa atributos HTML para guiar a formatação (pattern, placeholder, title).
    - Validações extras incluídas (ex.: CPF, RG e Telefone).
    """

    cpf = forms.CharField(
        label='CPF',
        max_length=14,
        widget=forms.TextInput(attrs={
            'placeholder': '000.000.000-00',
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

    telefone = forms.CharField(
        label='Telefone',
        max_length=15,
        widget=forms.TextInput(attrs={
            'placeholder': '(21) 91234-5678',
            'pattern': r'\(\d{2}\) \d{4,5}-\d{4}',
            'title': 'Digite o telefone no formato (21) 91234-5678'
        }),
        required=False
    )

    class Meta:
        model = Perfil
        fields = ['cpf', 'rg', 'telefone']

    def clean_cpf(self):
        """
        Validação de CPF:
        - Remove não dígitos.
        - Verifica se possui 11 dígitos.
        """
        cpf = self.cleaned_data.get('cpf', '').strip()
        if not cpf:
            return cpf
        nums = re.sub(r'\D', '', cpf)
        if len(nums) != 11:
            raise forms.ValidationError("CPF deve ter 11 dígitos numéricos.")
        return cpf

    def clean_rg(self):
        """
        Validação de RG:
        - Remove não dígitos.
        - Exige ao menos 8 dígitos.
        """
        rg = self.cleaned_data.get('rg', '').strip()
        if not rg:
            return rg
        nums = re.sub(r'\D', '', rg)
        if len(nums) < 8:
            raise forms.ValidationError("RG deve ter ao menos 8 dígitos numéricos.")
        return rg

    def clean_telefone(self):
        """
        Validação de telefone:
        - Remove não dígitos.
        - Verifica se possui entre 10 e 11 dígitos (com DDD).
        """
        telefone = self.cleaned_data.get('telefone', '').strip()
        if not telefone:
            return telefone
        nums = re.sub(r'\D', '', telefone)
        if len(nums) < 10 or len(nums) > 11:
            raise forms.ValidationError("Telefone deve ter DDD e número válido. Ex.: (21) 91234-5678")
        return telefone