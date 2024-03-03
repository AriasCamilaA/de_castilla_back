from django.urls import path
from .ViewEstadoOc import EstadoOCViewSet
from apps.estado_oc.views import generate_pdf



urlpatterns = [
    path('estadoocs/', EstadoOCViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('estadoocs/<int:pk>/', EstadoOCViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('estadoocs/generate-pdf/', generate_pdf, name='generate_pdf'),

]