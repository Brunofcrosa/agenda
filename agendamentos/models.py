from django.db import models

class Agendamento(models.Model):
    horario = models.DateTimeField(verbose_name='Horário', help_text='Data e hora do atendimento')
    cliente = models.ForeignKey(to='clientes.Cliente', verbose_name='Cliente', help_text='Nome do cliente', on_delete=models.PROTECT)
    funcionario = models.ForeignKey(to='funcionarios.Funcionario', verbose_name='Funcionário', help_text='Nome do funcionário', on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'

    def __str__(self):
        return f'Cliente: {self.cliente}'