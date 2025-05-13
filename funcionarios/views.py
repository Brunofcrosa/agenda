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

class FuncionariosView(ListView):
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

class FuncionarioAddView(SuccessMessageMixin, CreateView):
    model = Funcionario
    form_class = FuncionarioModelForm
    template_name = 'funcionario_form.html'
    success_url = reverse_lazy('funcionarios')
    success_message = 'Funcionário cadastrado com sucesso!'

class FuncionarioUpdateView(SuccessMessageMixin, UpdateView):
    model = Funcionario
    form_class = FuncionarioModelForm
    template_name = 'funcionario_form.html'
    success_url = reverse_lazy('funcionarios')
    success_message = 'Funcionário alterado com sucesso!'

class FuncionarioDeleteView(SuccessMessageMixin, DeleteView):
    model = Funcionario
    template_name = 'funcionario_apagar.html'
    success_url = reverse_lazy('funcionarios')
    success_message = 'Funcionário alterado com sucesso!'