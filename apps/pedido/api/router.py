
# Django REST Framework
from rest_framework import routers
from django.urls import path

from apps.pedido.views import generate_pdf
from .ViewPedido import PedidoViewSet


urlpatterns = [
    path('pedidos/', PedidoViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('pedidos/<int:pk>/', PedidoViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('pedidos/generate-pdf/', generate_pdf, name='generate_pdf'),
    path('pedidos/generate-pdf/<filtro>/', generate_pdf, name='generate_pdf'),
]
