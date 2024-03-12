from django.db import models

class Insumo(models.Model):
    id_insumo = models.AutoField(primary_key=True)
    nombre_insumo = models.CharField(max_length=255)
    estado = models.BooleanField(default=True)

    class Meta:
        db_table = 'insumo'