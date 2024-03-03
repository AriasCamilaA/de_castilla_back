
from django.urls import path
from .ViewEstadoInsumo import EstadoInsumoViewSet
from apps.estado_insumo.views import generate_pdf


urlpatterns = [
    path('estadoinsumos/', EstadoInsumoViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('estadoinsumos/<int:pk>/', EstadoInsumoViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('estadoinsumo/generate-pdf/', generate_pdf, name='generate_pdf'),
]
