from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import *
from rest_framework import serializers
from .OcHasProvedorSeralizers import OcHasProvedorSeralizers
from rest_framework import generics

class OcHasProvedorViewSet(viewsets.ModelViewSet):
    serializer_class = OcHasProvedorSeralizers # Fix the typo in the variable name
    queryset =  OcHasProvedorSeralizers.Meta.model.objects.all()
    # permission_classes = [IsAuthenticated]

class OcHasProvedorViewProveedor(generics.ListAPIView):
    serializer_class = OcHasProvedorSeralizers  # Asegúrate de importar el serializador adecuado
    queryset = OCHasProveedor.objects.all()  # Define el queryset inicial

    def get_queryset(self):
        id_proveedor_fk = self.kwargs['id_proveedor_fk']
        return OCHasProveedor.objects.filter(id_proveedor_fk=id_proveedor_fk)

class OcHasProvedorViewOC(generics.ListAPIView):
    serializer_class = OcHasProvedorSeralizers  # Asegúrate de importar el serializador adecuado
    queryset = OCHasProveedor.objects.all()  # Define el queryset inicial

    def get_queryset(self):
        id_oc_fk = self.kwargs['id_oc_fk']
        return OCHasProveedor.objects.filter(id_oc_fk=id_oc_fk)