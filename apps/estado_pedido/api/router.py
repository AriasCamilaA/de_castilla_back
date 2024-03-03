
from django.urls import path
from .ViewEstadoPedido import EstadoPedidoViewSet
from apps.estado_pedido.views import generate_pdf



urlpatterns = [
    path('estadopedidos/', EstadoPedidoViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('estadopedidos/<int:pk>/', EstadoPedidoViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('estadopedidos/generate-pdf/', generate_pdf, name='generate_pdf'),

]