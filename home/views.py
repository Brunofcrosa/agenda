from django.shortcuts import render
from fornecedores.models import Fornecedor  # Importando o modelo corretamente
from django.views.generic import TemplateView
from clientes.models import Cliente
from funcionarios.models import Funcionario
from servicos.models import Servico
from produtos.models import Produto
from agendamentos.models import Agendamento

def index(request):
    termo = request.GET.get('buscar', '')
    if termo:
        fornecedores = Fornecedor.objects.filter(nome__icontains=termo)
    else:
        fornecedores = Fornecedor.objects.all()

    return render(request, 'index.html', {
        'object_list': fornecedores  # Passando a lista de fornecedores
    })

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self):
        context = super(IndexView, self).get_context_data()
        context['qtd_clientes'] = Cliente.objects.count()
        context['qtd_funcionarios'] = Funcionario.objects.count()
        context['qtd_fornecedores'] = Fornecedor.objects.count()
        context['qtd_servicos'] = Servico.objects.count()
        context['qtd_produtos'] = Produto.objects.count()
        context['qtd_agendamentos'] = Agendamento.objects.count()
        return context
    