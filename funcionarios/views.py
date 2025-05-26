from .models import Funcionario
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.contrib import messages
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import FuncionarioModelForm
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.shortcuts import redirect
from django.contrib.auth.mixins import PermissionRequiredMixin

class FuncionariosView(PermissionRequiredMixin, ListView):
    permission_required = 'funcionarios.view_funcionario'
    permission_denied_message = 'Visualizar Funcionario'
    model = Funcionario
    template_name = 'funcionarios.html'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(FuncionariosView, self).get_queryset()

        if buscar:
            qs = qs.filter(nome__icontains=buscar)

        if qs.count() > 0:
            paginator = Paginator(qs, per_page=2)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            return messages.info(self.request, message='Não existem funcionários cadastrados!')

class FuncionarioAddView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'funcionarios.add_funcionario'
    permission_denied_message = 'Cadastrar Funcionario'
    model = Funcionario
    form_class = FuncionarioModelForm
    template_name = 'funcionario_form.html'
    success_url = reverse_lazy('funcionarios')
    success_message = 'Funcionário cadastrado com sucesso!'

class FuncionarioUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'funcionarios.update_funcionario'
    permission_denied_message = 'Alterar Funcionario'
    model = Funcionario
    form_class = FuncionarioModelForm
    template_name = 'funcionario_form.html'
    success_url = reverse_lazy('funcionarios')
    success_message = 'Funcionário alterado com sucesso!'

class FuncionarioDeleteView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'funcionarios.delete_funcionario'
    permission_denied_message = 'Excluir Funcionario'
    model = Funcionario
    template_name = 'funcionario_apagar.html'
    success_url = reverse_lazy('funcionarios')
    success_message = 'Funcionário alterado com sucesso!'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            return super().post(request, *args, **kwargs)
        except Exception as e:
            messages.error(request, f'O funcionario {self.object} não pode ser excluido.'f'Esse funcionario está registrado em agendamentos')
        finally:
            return redirect(success_url)