from django.urls import path
from .views import ClientesView, ClienteAddView, ClienteUpdateView, ClienteDeleteView

urlpatterns = [
    path('clientes/', ClientesView.as_view(), name='clientes'),
    path('cliente/adicionar/', ClienteAddView.as_view(), name='cliente_adicionar'),
    path('cliente/<int:pk>/editar/', ClienteUpdateView.as_view(), name='cliente_editar'),
    path('cliente/<int:pk>/apagar/', ClienteDeleteView.as_view(), name='cliente_apagar'),
]