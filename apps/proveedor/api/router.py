from rest_framework import routers
from django.urls.conf import path
from .ViewProveedor import ProveedorViewSet
from apps.proveedor.views import generate_pdf

urlpatterns = [
    path('proveedores/', ProveedorViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('proveedores/<int:pk>/', ProveedorViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('proveedor/generate-pdf/', generate_pdf, name='generate_pdf'),
    path('proveedor/generate-pdf/<filtro>/', generate_pdf, name='generate_pdf'),  
]