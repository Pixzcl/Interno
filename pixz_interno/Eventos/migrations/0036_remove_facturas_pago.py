# Generated by Django 2.0.5 on 2018-07-13 23:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Eventos', '0035_auto_20180713_1555'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facturas',
            name='pago',
        ),
    ]