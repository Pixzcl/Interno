# Generated by Django 2.0.5 on 2018-07-06 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Eventos', '0023_auto_20180706_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventos',
            name='satisfaccion',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Satisfacción'),
        ),
    ]
