from rest_framework import serializers
from ..models import *

class InsumoSeralizers(serializers.ModelSerializer):
    class Meta:
        model = Insumo
        fields = '__all__'  # Incluir todos los campos del modelo