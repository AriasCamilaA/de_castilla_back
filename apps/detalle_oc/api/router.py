
from django.urls import path
from .ViewDetalleOc import DetalleOCViewSet, DetallesOCView
from apps.detalle_oc.views import generate_pdf


urlpatterns = [
    path('detalleocs/', DetalleOCViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('detalleocs/<int:pk>/', DetalleOCViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('detalleocs/oc/<int:id_oc_fk>/', DetallesOCView.as_view()),
    path('detalleocs/generate-pdf/', generate_pdf, name='generate_pdf'),
    
]