from rest_framework import serializers
from ..models import *
from rest_framework import serializers




class PrermisoSeralizers(serializers.ModelSerializer):
    class Meta:
        model = Permiso
        fields = '__all__'  # Incluir todos los campos del modelo