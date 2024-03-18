from django.db import models
from apps.estado_pedido.models import EstadoPedido
from apps.usuarios.models import Usuario

class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    descripcion_pedido = models.CharField(max_length=255)
    fecha_pedido = models.DateField()
    fecha_fin_pedido = models.DateField(blank=True, null=True)
    id_estado_pedido_fk = models.ForeignKey(EstadoPedido,db_column='id_estado_pedido_fk', on_delete=models.CASCADE, blank=True, null=True)
    no_Documento_Usuario_fk = models.ForeignKey(Usuario,db_column='no_Documento_Usuario_fk', on_delete=models.CASCADE, blank=True, null=True)
    calificacion_pedido = models.IntegerField(blank=True, null=True)
    estado = models.BooleanField(default=True)

    class Meta:
        db_table = 'pedido'