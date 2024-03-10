from rest_framework import routers
from django.urls import path
from .ViewVenta import VentaViewSet
from apps.venta.views import generate_pdf


urlpatterns = [
    path('ventas/', VentaViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('ventas/<int:pk>/', VentaViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('ventas/generate-pdf/', generate_pdf, name='generate_pdf'),
    path('ventas/generate-pdf/<filtro>/', generate_pdf, name='generate_pdf'),
]