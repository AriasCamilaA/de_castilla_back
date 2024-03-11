from django.db import models
from apps.categoria.models import Categoria

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre_producto = models.CharField(max_length=255)
    imagen_producto = models.ImageField(upload_to='productos/', null=True, blank=True)
    precio_producto = models.IntegerField()
    id_categoria_fk = models.ForeignKey(Categoria, db_column='id_categoria_fk', on_delete=models.CASCADE)
    estado = models.BooleanField(default=True)

    class Meta:
        db_table = 'producto'