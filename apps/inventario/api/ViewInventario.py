from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import *
from rest_framework import serializers, generics
from .InventarioSeralizers import InventarioSeralizers

class InventarioViewSet(viewsets.ModelViewSet):
    serializer_class = InventarioSeralizers # Fix the typo in the variable name
    queryset =  InventarioSeralizers.Meta.model.objects.all()
    # permission_classes = [IsAuthenticated]

class InventarioProductoDetailView(generics.ListAPIView):
    queryset = Inventario.objects.all()
    serializer_class = InventarioSeralizers
    def get_queryset(self):
        id_producto_fk = self.kwargs['id_producto_fk']
        return Inventario.objects.filter(id_producto_fk =  id_producto_fk)

class InventarioInsumoDetailView(generics.ListAPIView):
    queryset = Inventario.objects.all()
    serializer_class = InventarioSeralizers
    def get_queryset(self):
        id_insumo_fk = self.kwargs['id_insumo_fk']
        return Inventario.objects.filter(id_insumo_fk =  id_insumo_fk)