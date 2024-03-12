from django.urls import path
from .ViewInventario import InventarioViewSet, InventarioProductoDetailView, InventarioInsumoDetailView
from apps.inventario.views import generate_pdf

urlpatterns = [
    path('inventario/', InventarioViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('inventario/<int:pk>/', InventarioViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('inventario/productos/<int:id_producto_fk>/', InventarioProductoDetailView.as_view(), name='inventario-producto-detail'),
    path('inventario/insumos/<int:id_insumo_fk>/', InventarioInsumoDetailView.as_view(), name='inventario-insumo-detail'),
    path('inventario/generate-pdf/', generate_pdf, name='generate_pdf'),
    path('inventario/generate-pdf/<filtro>', generate_pdf, name='generate_pdf'),
]