# Generated by Django 2.0.5 on 2018-06-07 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Eventos', '0002_eventos_nombre'),
    ]

    operations = [
        migrations.AddField(
            model_name='activaciones',
            name='monto',
            field=models.PositiveIntegerField(default=0, verbose_name='Monto de venta'),
        ),
    ]
