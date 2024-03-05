from django.db import models
from apps.pedido.models import Pedido
from apps.usuarios.models import Usuario

class Venta(models.Model):
    id_venta = models.AutoField(primary_key=True)
    fecha_venta = models.DateField()
    hora_venta = models.TimeField()
    total_venta = models.IntegerField()
    id_pedido_fk = models.ForeignKey(Pedido, db_column='id_pedido_fk', on_delete=models.CASCADE, null=True, blank=True)
    no_documento_usuario_fk = models.ForeignKey(Usuario, db_column='no_documento_usuario_fk', on_delete=models.CASCADE, null=True, blank=True)
    estado = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
  
        if self.no_documento_usuario_fk:
            self.nombre_usuario = self.no_documento_usuario_fk.nombre_usuario
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'venta'
