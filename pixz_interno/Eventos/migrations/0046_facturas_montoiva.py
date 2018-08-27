# Generated by Django 2.0.5 on 2018-08-27 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Eventos', '0045_activaciones_montoiva'),
    ]

    operations = [
        migrations.AddField(
            model_name='facturas',
            name='montoIVA',
            field=models.PositiveIntegerField(default=0, verbose_name='Monto con IVA'),
            preserve_default=False,
        ),
    ]
