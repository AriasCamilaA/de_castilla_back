from django.urls import path
from .ViewClasificacion import CalificacionViewSet
from apps.calificacion.views import generate_pdf

urlpatterns = [
    path('calificaciones/', CalificacionViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('calificaciones/<int:pk>/', CalificacionViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('calificaciones/generate-pdf/', generate_pdf, name='generate_pdf'),

]