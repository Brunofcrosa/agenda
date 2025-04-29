from django.db import models

class Servico(models.Model):
    nome = models.CharField('Nome', max_length=100, help_text='Nome completo do serviço', unique=True)
    descricao = models.TextField('Descrição', max_length=300, help_text='Descrição e observações do serviço')
    preco = models.DecimalField('Preço', max_digits=5, decimal_places=2, help_text='Preço do servico')


    class Meta:
        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'

    def __str__(self):
        return self.nome