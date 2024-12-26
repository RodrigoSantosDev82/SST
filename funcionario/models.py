from django.db import models

class Cargo(models.Model):
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome

class Funcionario(models.Model):
    nome = models.CharField(max_length=100)
    cargo = models.ForeignKey('Cargo', on_delete=models.CASCADE
                              )  # Relacionamento obrigatório com Cargo
    matricula = models.IntegerField(unique=True)
    data_admissao = models.DateField()

    def __str__(self):
        return self.nome