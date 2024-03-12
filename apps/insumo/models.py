from django.db import models
from apps.estado_insumo.models import EstadoInsumo

class Insumo(models.Model):
    id_insumo = models.AutoField(primary_key=True)
    nombre_insumo = models.CharField(max_length=255)
    id_estado_insumo_fk = models.ForeignKey(EstadoInsumo, db_column='id_estado_insumo_fk', on_delete=models.CASCADE, blank=True, null=True)
    estado = models.BooleanField(default=True)

    class Meta:
        db_table = 'insumo'