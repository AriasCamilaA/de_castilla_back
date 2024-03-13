# Generated by Django 5.0.2 on 2024-03-12 06:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('detalle_pedido', '0001_initial'),
        ('pedido', '0001_initial'),
        ('producto', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='detallepedido',
            name='id_pedido_fk',
            field=models.ForeignKey(blank=True, db_column='id_pedido_fk', null=True, on_delete=django.db.models.deletion.CASCADE, to='pedido.pedido'),
        ),
        migrations.AddField(
            model_name='detallepedido',
            name='id_producto_fk',
            field=models.ForeignKey(blank=True, db_column='id_producto_fk', null=True, on_delete=django.db.models.deletion.CASCADE, to='producto.producto'),
        ),
    ]