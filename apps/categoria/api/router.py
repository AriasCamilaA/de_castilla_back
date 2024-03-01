from django.urls import path
from .ViewCategoria import CategoriaViewSet
from apps.categoria.views import generate_pdf

urlpatterns = [
    path('categorias/', CategoriaViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('categorias/<int:pk>/', CategoriaViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('categorias/generate-pdf/', generate_pdf, name='generate_pdf'),
]