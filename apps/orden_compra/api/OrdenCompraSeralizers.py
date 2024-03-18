from rest_framework import serializers

from ..models import *
from rest_framework import serializers
from apps.estado_oc.api.EstadoOcSeralizers import EstadoOCSeralizers
from apps.proveedor.api.ProvedorSeralizers import ProveedorSeralizers



class OrdenCompraSeralizers(serializers.ModelSerializer):
    estado_oc = EstadoOCSeralizers(source='id_estado_oc_fk', read_only=True)
    Proveedor = ProveedorSeralizers(source='id_proveedor_fk', read_only=True)
    class Meta:
        model = OrdenCompra
        fields = '__all__'  # Incluir todos los campos del modelo