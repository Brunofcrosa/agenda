from django.views.generic import ListView
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Produto
from .forms import ProdutoModelForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import UpdateView, DeleteView
from django.shortcuts import redirect
from django.contrib.auth.mixins import PermissionRequiredMixin

class ProdutosView(PermissionRequiredMixin, ListView):
    permission_required = 'produtos.view_produto'
    permission_denied_message = 'Visualizar Produto'
    model = Produto
    template_name = 'produtos.html'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(ProdutosView, self).get_queryset()

        if buscar:
            qs = qs.filter(nome__icontains=buscar)

        if qs.count()>0:
            paginator = Paginator(qs, 3)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            return messages.info(self.request, 'Não existem produtos cadastrados!')
        
class ProdutoAddView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'produtos.add_produto'
    permission_denied_message = 'Cadastrar Produto'
    model = Produto
    form_class = ProdutoModelForm
    template_name = 'produto_form.html'
    success_url = reverse_lazy('produtos')
    success_message = 'Produto cadastrado com sucesso!'
    
class ProdutoUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'produtos.update_produto'
    permission_denied_message = 'Alterar Produto'
    model = Produto
    form_class = ProdutoModelForm
    template_name = 'produto_form.html'
    success_url = reverse_lazy('produtos')
    success_message = 'produto alterado com sucesso!'

class ProdutoDeleteView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'produtos.delete_produto'
    permission_denied_message = 'Excluir Produto'
    model = Produto
    template_name = 'produto_apagar.html'
    success_url = reverse_lazy('produtos')
    success_message = 'produto apagado com sucesso!'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            return super().post(request, *args, **kwargs)
        except Exception as e:
            messages.error(request, f'O produto {self.object} não pode ser excluido.'f'Esse produto é utilizado em serviços')
        finally:
            return redirect(success_url)
        