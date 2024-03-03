from django.urls import path
from .ViewInsumo import InsumoViewSet
from apps.insumo.views import generate_pdf


urlpatterns = [
    path('insumos/', InsumoViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('insumos/<int:pk>/', InsumoViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('insumos/generate-pdf/', generate_pdf, name='generate_pdf'),
]