
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.messages.views import SuccessMessageMixin
from .models import Servico
from .forms import ServicoModelForm, ProdutosServicoInLine
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.views.generic.base import TemplateResponseMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

class ServicosView(PermissionRequiredMixin, ListView):
    permission_required = 'servicos.view_servico'
    permission_denied_message = 'Visualizar Serviço'
    model = Servico
    template_name = 'servicos.html'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(ServicosView, self).get_queryset()

        if buscar:
            qs = qs.filter(Q(nome__icontains=buscar)|Q(descricao__icontains=buscar))

        if qs.count()>0:
            paginator = Paginator(qs, 2)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            return messages.info(self.request, 'Não existem Serviços cadastrados!')
        
class ServicoAddView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'servicos.add_servico'
    permission_denied_message = 'Cadastrar Serviço'
    model = Servico
    form_class = ServicoModelForm
    template_name = 'servico_form.html'
    success_url = reverse_lazy('servicos')
    success_message = 'Serviço cadastrado com sucesso!'
    
class ServicoUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'servicos.update_servico'
    permission_denied_message = 'Alterar Serviço'
    model = Servico
    form_class = ServicoModelForm
    template_name = 'servico_form.html'
    success_url = reverse_lazy('servicos')
    success_message = 'Serviço alterado com sucesso!'

class ServicoDeleteView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'servicos.delete_servico'
    permission_denied_message = 'Excluir Serviço'
    model = Servico
    template_name = 'servico_apagar.html'
    success_url = reverse_lazy('servicos')
    success_message = 'Serviço apagado com sucesso!'

class ServicoInLineEditView(PermissionRequiredMixin, TemplateResponseMixin, View):
    permission_required = 'servicos.update_servico'
    permission_denied_message = 'Alterar Serviço'
    template_name = 'servico_form_inline.html'

    def get_formset(self, data=None):
        return ProdutosServicoInLine(instance=self.servico, data=data)
    
    def dispatch(self, request, pk):
        self.servico = get_object_or_404(Servico, id=pk)
        return super().dispatch(request, pk)
    
    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'servico': self.servico, 'formset': formset})
    
    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('servicos')
        return self.render_to_response({'servico': self.servico, 'formset': formset})
    