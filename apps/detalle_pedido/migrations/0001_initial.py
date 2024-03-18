# Generated by Django 5.0.2 on 2024-03-12 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DetallePedido',
            fields=[
                ('id_detalle_pedido', models.AutoField(primary_key=True, serialize=False)),
                ('cantidad_producto', models.IntegerField()),
                ('subtotal_detalle_pedido', models.IntegerField()),
                ('estado', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'detalle_pedido',
            },
        ),
    ]
