from django.db import models
from typing import Optional, cast
from django.db.models import QuerySet
from django.contrib.auth.models import User

class Pet(models.Model):
    nome = models.CharField(max_length=100)
    idade = models.IntegerField()
    descricao = models.TextField(verbose_name='Descrição')
    raca = models.CharField(max_length=100, verbose_name='Raça')
    especie = models.CharField(max_length=100, verbose_name='Espécie')
    foto = models.ImageField(upload_to='fotos_pets/', null=True, blank=True)
    disponivel = models.BooleanField(default=True)

    @property
    def adotante(self) -> Optional[str]:
        """Retorna o nome do adotante ativo, se existir."""
        adocoes = cast(QuerySet["Adocao"], self.adocoes) # type: ignore
        adotacao_ativa = adocoes.filter(disponivel=True).last()
        return adotacao_ativa.nome_adotante if adotacao_ativa else None

    def __str__(self):
        return self.nome


class Adocao(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='adocoes')
    nome_adotante = models.CharField(max_length=100)
    email_adotante = models.EmailField()
    cpf_adotante = models.CharField(max_length=14)
    data_adocao = models.DateTimeField(auto_now_add=True)
    rg_adotante = models.CharField(max_length=20, blank=True, null=True)
    comprovante_residencia = models.FileField(upload_to='comprovantes/', blank=True, null=True)
    disponivel = models.BooleanField(default=True)
    telefone_adotante = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"Adoção de {self.pet.nome} por {self.nome_adotante}"
    
class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    cpf = models.CharField('CPF', max_length=14, blank=True, null=True)
    rg = models.CharField('RG', max_length=20, blank=True, null=True)

    def __str__(self):
        return f'Perfil de {self.user.username}'