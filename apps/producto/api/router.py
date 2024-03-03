from django.urls import path
from .ViewProducto import ProductoViewSet
from apps.producto.views import generate_pdf


urlpatterns = [
    path('productos/', ProductoViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('productos/<int:pk>/', ProductoViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('productos/generate-pdf/', generate_pdf, name='generate_pdf'),
]