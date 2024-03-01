from django.urls import path
from .ViewHistorico import HistoricoViewSet
from apps.historico.views import generate_pdf



urlpatterns = [
    path('historicos/', HistoricoViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('historicos/<int:pk>/', HistoricoViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('historicos/generate-pdf/', generate_pdf, name='generate_pdf'),

]