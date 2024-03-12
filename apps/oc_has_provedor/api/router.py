
# Django REST Framework
from rest_framework.routers import DefaultRouter
from django.urls import path
from .ViewOcHasProvedor import OcHasProvedorViewSet, OcHasProvedorViewProveedor, OcHasProvedorViewOC
from apps.oc_has_provedor.views import generate_pdf

urlpatterns = [
    path('ochasproveedores/', OcHasProvedorViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('ochasproveedores/<int:pk>/', OcHasProvedorViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('ochasproveedores/proveedor/<int:id_proveedor_fk>/', OcHasProvedorViewProveedor.as_view()),
    path('ochasproveedores/oc/<int:id_oc_fk>/', OcHasProvedorViewOC.as_view()),
    path('ochasproveedores/generate-pdf/', generate_pdf, name='generate_pdf'),
    path('ochasproveedores/generate-pdf/<filtro>/', generate_pdf, name='generate_pdf'),
]