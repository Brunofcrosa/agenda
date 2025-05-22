from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import FornecedorModelForm
from .models import Fornecedor
from django.shortcuts import redirect


class FornecedoresView(ListView):
    model = Fornecedor
    template_name = 'fornecedores.html'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(FornecedoresView, self).get_queryset()

        if buscar:
            qs = qs.filter(nome__icontains=buscar)
        
        if qs.count() > 0:
            paginator = Paginator(qs, 2)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            return messages.info(self.request, 'Não existem fornecedores cadastrados!')
        
    
class FornecedorAddView(SuccessMessageMixin, CreateView):
    model = Fornecedor
    form_class = FornecedorModelForm
    template_name = 'fornecedor_form.html'
    success_url = reverse_lazy('fornecedores')
    success_message = 'Fornecedor cadastrado com sucesso!'

class FornecedorUpdateView(SuccessMessageMixin, UpdateView):
    model = Fornecedor
    form_class = FornecedorModelForm
    template_name = 'fornecedor_form.html'
    success_url = reverse_lazy('fornecedores')
    success_message = 'Fornecedor alterado com sucesso!'

class FornecedorDeleteView(SuccessMessageMixin, DeleteView):
    model = Fornecedor
    template_name = 'fornecedor_apagar.html'
    success_url = reverse_lazy('fornecedores')
    success_message = 'Fornecedor apagado com sucesso!'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            return super().post(request, *args, **kwargs)
        except Exception as e:
            messages.error(request, f'O fornecedor {self.object} não pode ser excluido.'f'Esse fornecedor está registrado no fornecimento de produtos')
        finally:
            return redirect(success_url)
        