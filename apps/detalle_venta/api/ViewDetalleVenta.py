

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import *
from rest_framework import serializers
from .DetalleVentaSeralizers import DetalleVentaSeralizers
from rest_framework import generics



class DetalleVentaViewSet(viewsets.ModelViewSet):
    serializer_class = DetalleVentaSeralizers # Fix the typo in the variable name
    queryset =  DetalleVentaSeralizers.Meta.model.objects.all()
    # permission_classes = [IsAuthenticated]

class DetallesVentaView(generics.ListAPIView):
    serializer_class = DetalleVentaSeralizers  # Asegúrate de importar el serializador adecuado
    queryset = DetalleVenta.objects.all()  # Define el queryset inicial

    def get_queryset(self):
        id_venta_fk = self.kwargs['id_venta_fk']
        return DetalleVenta.objects.filter(id_venta_fk=id_venta_fk)