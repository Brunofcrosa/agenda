from django.db import models
from django.db.models.functions import Upper

class Servico(models.Model):
    nome = models.CharField('Nome', max_length=100, help_text='Nome completo do serviço', unique=True)
    preco = models.DecimalField('Preço', max_digits=5, decimal_places=2, help_text='Preço do servico')
    descricao = models.TextField('Descrição', max_length=300, help_text='Descrição e observações do serviço')
    produto = models.ManyToManyField('produtos.Produto', through='servicos.ProdutosServico')

    @property
    def produtos(self):
        return ProdutosServico.objects.filter(servico=self)

    class Meta:
        verbose_name = 'Serviço'
        verbose_name = 'Serviços'
        ordering = [Upper('nome')]

    def __str__(self):
        return self.nome
    

class ProdutosServico(models.Model):
    servico = models.ForeignKey('servicos.Servico', verbose_name='Serviço', help_text='Nome do serviço realizado', on_delete=models.CASCADE, related_name='servico')
    produto = models.ForeignKey('produtos.Produto', verbose_name='Produto', help_text='Nome do produto utilizado', on_delete=models.PROTECT, related_name='produto')
    quantidade = models.DecimalField('Quantidade', max_digits=5, decimal_places=2, help_text='Quantidade utilizada de produto', default=1.00)

    class Meta:
        verbose_name = 'Produto do Serviço'
        verbose_name_plural = 'Produtos utilizados'

    def __str__(self):
        return f'{self.produto}'