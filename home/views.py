from django.shortcuts import render
from fornecedores.models import Fornecedor  # Importando o modelo corretamente

def index(request):
    termo = request.GET.get('buscar', '')
    if termo:
        fornecedores = Fornecedor.objects.filter(nome__icontains=termo)
    else:
        fornecedores = Fornecedor.objects.all()

    return render(request, 'index.html', {
        'object_list': fornecedores  # Passando a lista de fornecedores
    })