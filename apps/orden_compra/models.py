from django.db import models
from apps.estado_oc.models import EstadoOC


class OrdenCompra(models.Model):
    id_oc = models.AutoField(primary_key=True)
    fecha_oc = models.DateField()
    hora_oc = models.TimeField()
    id_estado_oc_fk = models.ForeignKey(EstadoOC, db_column='id_estado_oc_fk', on_delete=models.CASCADE, blank=True, null=True)
    estado = models.BooleanField(default=True)

    class Meta:
        db_table = 'orden_compra'