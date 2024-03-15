
from django.urls import path
from .ViewDetalleVenta import DetalleVentaViewSet, DetallesVentaView
from apps.detalle_venta.views import generate_pdf


urlpatterns = [
    path('detalleventas/', DetalleVentaViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('detalleventas/<int:pk>/', DetalleVentaViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('detalleventas/venta/<int:id_venta_fk>/', DetallesVentaView.as_view()),
    path('detallesVentas/generate_pdf/<int:id_venta>', generate_pdf, name='generate_pdf'),
]