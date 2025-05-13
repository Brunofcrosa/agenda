from django.db import models
from django.db.models.functions import Upper
from clientes.models import Pessoa

class Funcionario(Pessoa):
    funcao = models.CharField('Função', max_length=35, help_text='Função na empresa')
    data_admissao = models.DateField(verbose_name='Admissão', help_text='Data de admissão na empresa')

    class Meta:
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'
        ordering = [Upper('nome')]
    def __str__(self):
        return super().nome
