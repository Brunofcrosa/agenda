from django import forms

from .models import Servico
from .models import ProdutosServico
from django.forms import inlineformset_factory

class ServicoModelForm(forms.ModelForm):
    
    class Meta:
        model = Servico
        fields = '__all__'

        error_messages = {
            'nome': {'required': 'O nome do Serviço é um campo obrigatorio', 'unique': 'Serviço já cadastrado'},
            'descricao': {'required': 'A descrição do Serviço é um campo obrigatório'},
            'preco': {'required': 'O Preço do Serviço é um campo obrigatório'},
        }


ProdutosServicoInLine = inlineformset_factory(Servico, ProdutosServico, fk_name='servico', fields=('produto', 'quantidade'), extra=1, can_delete=True)