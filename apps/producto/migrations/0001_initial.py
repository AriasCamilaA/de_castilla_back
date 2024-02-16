# Generated by Django 5.0.2 on 2024-02-15 14:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categoria', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id_producto', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_producto', models.CharField(max_length=255)),
                ('imagen_producto', models.ImageField(upload_to='productos/')),
                ('precio_producto', models.IntegerField()),
                ('estado', models.BooleanField(default=True)),
                ('id_categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categoria.categoria')),
            ],
            options={
                'db_table': 'producto',
            },
        ),
    ]
