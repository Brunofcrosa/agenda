from django import forms
from .models import Agendamento
from clientes.models import Cliente
from funcionarios.models import Funcionario
from django.forms import inlineformset_factory
from agendamentos.models import OrdemServico


class AgendamentoListForm(forms.Form):
    cliente = forms.ModelChoiceField(label='Cliente', queryset=Cliente.objects.all(), required=False)
    funcionario = forms.ModelChoiceField(label='Funcionário', queryset=Funcionario.objects.all(), required=False)

class AgendamentoModelForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ['horario', 'cliente', 'funcionario']

        error_messages = {
            'horario': {'required': 'O horário é um campo obrigatório'},
            'cliente': {'required': 'O cliente é um campo obrigatório'},
            'funcionario': {'required': 'O funcionário é um campo obrigatório'},
        }

AgendamentosServicoInLine = inlineformset_factory(Agendamento, OrdemServico, fk_name='agendamento', fields=('servico', 'funcionario', 'situacao', 'observacoes'), extra=1, can_delete=True)