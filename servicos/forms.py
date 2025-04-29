from django import forms

from .models import Servico

class ServicoModelForm(forms.ModelForm):
    
    class Meta:
        model = Servico
        fields = '__all__'

        error_messages = {
            'nome': {'required': 'O nome do Serviço é um campo obrigatorio', 'unique': 'Serviço já cadastrado'},
            'descricao': {'required': 'A descrição do Serviço é um campo obrigatório'},
            'preco': {'required': 'O Preço do Serviço é um campo obrigatório'},
        }
