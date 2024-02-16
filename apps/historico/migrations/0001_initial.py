# Generated by Django 5.0.2 on 2024-02-15 14:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('insumo', '0001_initial'),
        ('producto', '0001_initial'),
        ('tipo_movimiento', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Historico',
            fields=[
                ('id_historico', models.AutoField(primary_key=True, serialize=False)),
                ('cantidad_historico', models.IntegerField()),
                ('fecha_caducidad', models.DateField()),
                ('fecha_movimiento', models.DateField()),
                ('tipo_historico', models.CharField(max_length=255)),
                ('estado', models.BooleanField(default=True)),
                ('id_insumo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insumo.insumo')),
                ('id_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='producto.producto')),
                ('id_tipo_movimiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tipo_movimiento.tipomovimiento')),
            ],
            options={
                'db_table': 'historico',
            },
        ),
    ]