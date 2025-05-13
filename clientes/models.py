from django.db import models
from django.db.models.functions import Upper
from stdimage import StdImageField
# Create your models here.
class Pessoa(models.Model):
    nome = models.CharField('Nome', max_length=50, help_text='Nome completo')
    fone = models.CharField('Telefone', max_length=15, help_text='Numero do telefone')
    email = models.EmailField('E-mail', max_length=100, help_text='Endereço de e-mail', unique=True)
    foto = StdImageField('Foto', upload_to='pessoas', delete_orphans=True, null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.nome


class Cliente(Pessoa):
    endereco = models.CharField('Endereço', max_length=100, help_text='Endereço completo')

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = [Upper('nome')]

    def __str__(self):
        return self.nome