from django.db import models
from typing import Optional, cast
from django.db.models import QuerySet
from django.contrib.auth.models import User


class Pet(models.Model):
    nome = models.CharField(max_length=100)
    idade = models.IntegerField(
        help_text="Idade do pet em anos (ou ajustar conforme necessidade)."
    )
    descricao = models.TextField(verbose_name='Descrição')
    raca = models.CharField(max_length=100, verbose_name='Raça')
    especie = models.CharField(max_length=100, verbose_name='Espécie')
    foto = models.ImageField(
        upload_to='fotos_pets/',
        null=True,
        blank=True,
        help_text="Imagem opcional do pet. Pasta de upload: fotos_pets/"
    )
    disponivel = models.BooleanField(
        default=True,
        help_text="Indica se o pet está disponível para adoção."
    )

    class Meta:
        # Ordena por nome por padrão; ajuste conforme necessidade (ex.: ordenar por data de cadastro, se existir campo).
        ordering = ['nome']
        verbose_name = 'Pet'
        verbose_name_plural = 'Pets'

    @property
    def adotante(self) -> Optional[str]:
        # Acesso ao related_name 'adocoes' obtém manager de Adocao; fazemos cast para ajudar tipo estático.
        adocoes = cast(QuerySet["Adocao"], self.adocoes)  # type: ignore
        # Filtra adoções em que disponivel=True (ou ajusta conforme semântica)
        adotacao_ativa = adocoes.filter(disponivel=True).last()
        if adotacao_ativa:
            return adotacao_ativa.nome_adotante
        return None

    def __str__(self):
        # Representação em strings, útil em admin, shell etc.
        return self.nome


class Adocao(models.Model):
    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name='adocoes',
        help_text="Pet que está sendo adotado."
    )
    nome_adotante = models.CharField(
        max_length=100,
        help_text="Nome completo do adotante."
    )
    email_adotante = models.EmailField(
        help_text="E-mail do adotante, para contato."
    )
    cpf_adotante = models.CharField(
        max_length=14,
        help_text="CPF do adotante. Formato esperado: 000.000.000-00 ou cifra limpa."
    )
    data_adocao = models.DateTimeField(
        auto_now_add=True,
        help_text="Data e hora em que a adoção foi registrada."
    )
    rg_adotante = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="RG do adotante (opcional)."
    )
    comprovante_residencia = models.FileField(
        upload_to='comprovantes/',
        blank=True,
        null=True,
        help_text="Arquivo com comprovante de residência do adotante."
    )
    disponivel = models.BooleanField(
        default=True,
        help_text="Se True: adoção ativa ou pendente. Se False: concluída ou cancelada."
    )
    telefone_adotante = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        help_text="Telefone do adotante com DDD (opcional)."
    )

    class Meta:
        # Ordena por data de adoção mais recente primeiro (descendente).
        ordering = ['-data_adocao']
        verbose_name = 'Adoção'
        verbose_name_plural = 'Adoções'

    def __str__(self):
        return f"Adoção de {self.pet.nome} por {self.nome_adotante}"


class Perfil(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='perfil',
        help_text="Usuário ao qual este perfil pertence."
    )
    cpf = models.CharField(
        'CPF',
        max_length=14,
        blank=True,
        null=True,
        help_text="CPF no formato 000.000.000-00 ou apenas dígitos."
    )
    rg = models.CharField(
        'RG',
        max_length=20,
        blank=True,
        null=True,
        help_text="RG do usuário (opcional)."
    )
    telefone = models.CharField(
        'Telefone',
        max_length=15,
        blank=True,
        null=True,
        help_text="Telefone com DDD no formato (21) 91234-5678."
    )

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'

    def __str__(self):
        return f'Perfil de {self.user.username}'