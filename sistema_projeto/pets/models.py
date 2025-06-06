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


class Adocao(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='adocoes')
    nome_adotante = models.CharField(max_length=100)
    email_adotante = models.EmailField()
    cpf_adotante = models.CharField(max_length=14)  # CPF com máscara, ex: 000.000.000-00
    data_adocao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Adoção de {self.pet.nome} por {self.nome_adotante}"
