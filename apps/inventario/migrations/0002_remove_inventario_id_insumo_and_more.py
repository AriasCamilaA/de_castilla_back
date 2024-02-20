# Generated by Django 5.0.2 on 2024-02-17 22:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insumo', '0001_initial'),
        ('inventario', '0001_initial'),
        ('producto', '0003_alter_producto_id_categoria_fk'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventario',
            name='id_insumo',
        ),
        migrations.RemoveField(
            model_name='inventario',
            name='id_producto',
        ),
        migrations.AddField(
            model_name='inventario',
            name='id_insumo_fk',
            field=models.ForeignKey(blank=True, db_column='id_insumo_fk', null=True, on_delete=django.db.models.deletion.CASCADE, to='insumo.insumo'),
        ),
        migrations.AddField(
            model_name='inventario',
            name='id_producto_fk',
            field=models.ForeignKey(blank=True, db_column='id_producto_fk', null=True, on_delete=django.db.models.deletion.CASCADE, to='producto.producto'),
        ),
    ]