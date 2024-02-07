# Generated by Django 5.0.2 on 2024-02-07 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Calificacion',
            fields=[
                ('id_calificacion', models.BigAutoField(primary_key=True, serialize=False)),
                ('comentario_calificacion', models.CharField(blank=True, max_length=255, null=True)),
                ('estrallas_calificacion', models.IntegerField(blank=True, null=True)),
                ('estado', models.BooleanField()),
            ],
            options={
                'db_table': 'calificacion',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DetalleOc',
            fields=[
                ('id_detalle_oc', models.BigAutoField(primary_key=True, serialize=False)),
                ('cantidad_insumo', models.IntegerField(blank=True, null=True)),
                ('estado', models.BooleanField()),
            ],
            options={
                'db_table': 'detalle_oc',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='EstadoOc',
            fields=[
                ('id_estado_oc', models.BigAutoField(primary_key=True, serialize=False)),
                ('nombre_estado_oc', models.CharField(blank=True, max_length=255, null=True)),
                ('estado', models.BooleanField()),
            ],
            options={
                'db_table': 'estado_oc',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='OcHasProveedor',
            fields=[
                ('id_oc_has_proveedor', models.BigAutoField(primary_key=True, serialize=False)),
                ('estado', models.BooleanField()),
            ],
            options={
                'db_table': 'oc_has_proveedor',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='OrdenCompra',
            fields=[
                ('id_oc', models.BigAutoField(primary_key=True, serialize=False)),
                ('fecha_oc', models.DateField(blank=True, null=True)),
                ('hora_oc', models.TimeField(blank=True, null=True)),
                ('estado', models.BooleanField()),
            ],
            options={
                'db_table': 'orden_compra',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id_proveedor', models.BigAutoField(primary_key=True, serialize=False)),
                ('celular_proveedor', models.BigIntegerField(blank=True, null=True)),
                ('celular_respaldo_proveedor', models.BigIntegerField(blank=True, null=True)),
                ('correo_proveedor', models.CharField(blank=True, max_length=255, null=True)),
                ('empresa_proveedor', models.CharField(blank=True, max_length=255, null=True)),
                ('estado_proveedor', models.BooleanField()),
                ('nit_proveedor', models.BigIntegerField(blank=True, null=True)),
                ('nombre_proveedor', models.CharField(blank=True, max_length=255, null=True)),
                ('estado', models.BooleanField()),
            ],
            options={
                'db_table': 'proveedor',
                'managed': False,
            },
        ),
    ]
