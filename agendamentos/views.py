from .forms import AgendamentoListForm, AgendamentoModelForm
from .models import Agendamento, OrdemServico
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import TemplateResponseMixin, View
from django.shortcuts import get_object_or_404, redirect
from .forms import AgendamentosServicoInLine
from django.views.generic import View
from django.views.generic import DetailView
from produtos.models import Produto
from servicos.models import ProdutosServico
from django.db.models import Case, When, Value, IntegerField
from django.template.loader import render_to_string
from django.core.mail import send_mail

class AgendamentosView(ListView):
    model = Agendamento
    template_name = 'agendamentos.html'

    def get_context_data(self, **kwargs):
        context = super(AgendamentosView, self).get_context_data(**kwargs)
        if self.request.GET:
            form = AgendamentoListForm(self.request.GET)
        else:
            form = AgendamentoListForm()
        context['form'] = form
        return context

    def get_queryset(self):
        qs = super(AgendamentosView, self).get_queryset()
        if self.request.GET:
            form = AgendamentoListForm(self.request.GET)
            if form.is_valid():
                cliente = form.cleaned_data.get('cliente')
                funcionario = form.cleaned_data.get('funcionario')
                if cliente:
                    qs = qs.filter(cliente=cliente)
                if funcionario:
                    qs = qs.filter(funcionario=funcionario)
        
        qs = qs.annotate(
            status_order=Case(
                When(status='A', then=Value(1)),
                When(status='F', then=Value(2)),
                When(status='C', then=Value(3)),
                default=Value(4),
                output_field=IntegerField(),
            )
        ).order_by('status_order', '-horario')
        
        if qs.count() > 0:
            paginator = Paginator(qs, per_page=2)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            return messages.info(self.request, message='Não existem agendamentos cadastrados!')

class AgendamentoAddView(SuccessMessageMixin, CreateView):
    model = Agendamento
    form_class = AgendamentoModelForm
    template_name = 'agendamento_form.html'
    success_url = reverse_lazy('agendamentos')
    success_message = 'Agendamento cadastrado com sucesso!'

class AgendamentoUpdateView(SuccessMessageMixin, UpdateView):
    model = Agendamento
    form_class = AgendamentoModelForm
    template_name = 'agendamento_form.html'
    success_url = reverse_lazy('agendamentos')
    success_message = 'Agendamento alterado com sucesso!'

class AgendamentoDeleteView(SuccessMessageMixin, DeleteView):
    model = Agendamento
    template_name = 'agendamento_apagar.html'
    success_url = reverse_lazy('agendamentos')
    success_message = 'Agendamento excluído com sucesso!'


class AgendamentoInLineEditView(TemplateResponseMixin, View):
    template_name = 'agendamento_form_inline.html'

    def get_formset(self, data=None):
        return AgendamentosServicoInLine(instance=self.agendamento, data=data)

    def dispatch(self, request, pk):
        self.agendamento = get_object_or_404(Agendamento, id=pk)
        return super().dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'agendamento': self.agendamento, 'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            dados = formset.cleaned_data
            for item in dados:
                if item.get('situacao') != 'C':
                    produtoservico = ProdutosServico.objects.filter(servico=item.get('servico'))
                    if produtoservico:
                        for prd in produtoservico:
                            produto = Produto.objects.get(pk=prd.produto.pk)
                            if produto.quantidade < prd.quantidade and not item.get('DELETE'):
                                messages.error(self.request,
                                                        f'Atenção! Quantidade em estoque insuficiente para o produto {produto.nome}')
                                return self.render_to_response({'agendamento': self.agendamento, 'formset': formset})
                            else:
                                formset.save()
                else:
                    formset.save()
            return redirect('agendamentos')
        else:
            return self.render_to_response({'agendamento': self.agendamento, 'formset': formset})


class AgendamentoExibir(DetailView):
    model = Agendamento
    template_name = 'agendamento_exibir.html'

    def get_object(self, queryset=None):
        agendamento = Agendamento.objects.get(pk=self.kwargs.get('pk'))
        if agendamento.status == 'A':
            ordem_servico = OrdemServico.objects.filter(agendamento=agendamento)
            lista_situacao = ordem_servico.values_list('situacao', flat=True)
            if 'A' in (lista_situacao):
                messages.info(self.request, "Ordem de serviço não pode ser encerrada. Existem serviços com a situação em aberto!")
            else:
                for ordem in ordem_servico:
                    if ordem.situacao == 'R':
                        if ordem.servico.produto:
                            produto_servico = ProdutosServico.objects.filter(servico=ordem.servico)
                            for item in produto_servico:
                                produto = Produto.objects.get(pk=item.produto.pk)
                                produto.quantidade -= item.quantidade
                                produto.save()
                agendamento.status = 'F'
                agendamento.save()
                self.enviar_email(agendamento)
        return agendamento

    def enviar_email(self, agendamento):
        email = [agendamento.cliente.email]
        descricao = []
        for servico in agendamento.servicos:
            descricao.append(f'{servico} - R$ {servico.preco} ({servico.get_situacao_display()})')

        dados = {
            'cliente': agendamento.cliente.nome,
            'horario': agendamento.horario,
            'funcionario': agendamento.funcionario.nome,
            'descricao': descricao,
            'valor': agendamento.valor,
        }

        texto_email = render_to_string('emails/texto_email.txt', dados)
        html_email = render_to_string('emails/texto_email.html', dados)

        send_mail(
            subject='Lavacar - Serviço concluído',
            message=texto_email,
            from_email='brunofcrosa1@gmail.com',
            recipient_list=email,
            html_message=html_email,
            fail_silently=False
        )