from rest_framework import serializers

from ..models import *
from rest_framework import serializers
from apps.insumo.api.InsumoSeralizers import InsumoSeralizers
from apps.producto.api.ProductoSeralizers import ProductoSerializer




class InventarioSeralizers(serializers.ModelSerializer):
    insumo = InsumoSeralizers(source='id_insumo_fk', read_only=True)
    producto = ProductoSerializer(source='id_producto_fk', read_only=True)
    class Meta:
        model = Inventario
        fields = '__all__'  # Incluir todos los campos del modelo