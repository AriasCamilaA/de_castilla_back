from django.urls import path
from .ViewInventario import InventarioViewSet
from apps.inventario.views import generate_pdf

urlpatterns = [
    path('inventario/', InventarioViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('inventario/<int:pk>/', InventarioViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('inventario/generate-pdf/', generate_pdf, name='generate_pdf'),
]