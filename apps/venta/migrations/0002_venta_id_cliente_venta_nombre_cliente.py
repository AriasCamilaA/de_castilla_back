# Generated by Django 5.0.2 on 2024-03-19 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='venta',
            name='id_cliente',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='venta',
            name='nombre_cliente',
            field=models.TextField(blank=True, null=True),
        ),
    ]
