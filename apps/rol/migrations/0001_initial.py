# Generated by Django 5.0.2 on 2024-03-12 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id_rol', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_rol', models.CharField(max_length=255)),
                ('estado', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'rol',
            },
        ),
    ]
