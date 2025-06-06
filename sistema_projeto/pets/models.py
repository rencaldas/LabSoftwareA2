from django.db import models

class Pet(models.Model):
    nome = models.CharField(max_length=100)
    idade = models.IntegerField()
    descricao = models.TextField(verbose_name='Descrição')
    raca = models.CharField(max_length=100, verbose_name='Raça')
    especie = models.CharField(max_length=100, verbose_name='Espécie')  # Novo campo
    foto = models.ImageField(upload_to='fotos_pets/', null=True, blank=True)

    def __str__(self):
        return self.nome