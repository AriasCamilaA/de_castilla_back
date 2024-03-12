# Generated by Django 5.0.2 on 2024-03-12 04:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orden_compra', '0003_ordencompra_estado'),
        ('proveedor', '0004_alter_proveedor_celular_respaldo_proveedor'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordencompra',
            name='id_proveedor_fk',
            field=models.ForeignKey(blank=True, db_column='id_proveedor_fk', null=True, on_delete=django.db.models.deletion.CASCADE, to='proveedor.proveedor'),
        ),
    ]