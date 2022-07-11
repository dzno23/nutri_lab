from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User

class Pacientes(models.Model):
    choice_gender = (('FC', 'Feminino (Cisgênero)'),
                    ('FT', 'Feminino (Transgênero)'),
                    ('MC', 'Masculino (Cisgênero'),
                    ('MT', 'Masculino (Transgênero)'),
                    ('N', 'Gênero Neutro'),
                    ('F', 'Gênero Fluido'),
                    ('O', 'Outro'),)
    
    nome = models.CharField(max_length=50)
    genero = models.CharField(max_length=2, choices=choice_gender)
    idade = models.IntegerField()
    email = models.EmailField()
    telefone = models.CharField(max_length=19)
    nutri = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class Dadospaciente(models.Model):
    paciente = models.ForeignKey(Pacientes, on_delete=models.CASCADE)
    data = models.DateTimeField()
    peso = models.FloatField()
    altura = models.FloatField()
    percentual_gordura = models.IntegerField()
    percentual_musculo = models.IntegerField()
    colesterol_hdl = models.IntegerField()
    colesterol_ldl = models.IntegerField()
    colesterol_total = models.IntegerField()
    triglicerideos = models.IntegerField()

    def __str__(self):
        return f'Paciente({self.paciente.nome}, {self.peso})'