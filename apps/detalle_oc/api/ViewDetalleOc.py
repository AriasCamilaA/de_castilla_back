

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import *
from rest_framework import serializers
from .DetalleOcSeralizers import DetalleOCSeralizers
from rest_framework import generics


class DetalleOCViewSet(viewsets.ModelViewSet):
    serializer_class =  DetalleOCSeralizers # Fix the typo in the variable name
    queryset =   DetalleOCSeralizers.Meta.model.objects.all()
    # permission_classes = [IsAuthenticated]

class DetallesOCView(generics.ListAPIView):
    serializer_class = DetalleOCSeralizers  # Asegúrate de importar el serializador adecuado
    queryset = DetalleOC.objects.all()  # Define el queryset inicial

    def get_queryset(self):
        id_oc_fk = self.kwargs['id_oc_fk']
        return DetalleOC.objects.filter(id_oc_fk=id_oc_fk)