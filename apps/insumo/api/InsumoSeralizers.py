from rest_framework import serializers
from ..models import *
from rest_framework import serializers
from apps.estado_insumo.api.EstadoInsumoSeralizers import EstadoInsumoSeralizers




class InsumoSeralizers(serializers.ModelSerializer):
    estado_insumo = EstadoInsumoSeralizers(source='id_estado_insumo_fk', read_only=True)
    class Meta:
        model = Insumo
        fields = '__all__'  # Incluir todos los campos del modelo