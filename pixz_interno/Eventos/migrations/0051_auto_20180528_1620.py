# Generated by Django 2.0.5 on 2018-05-28 20:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Eventos', '0050_auto_20180528_1619'),
    ]

    operations = [
        migrations.RenameField(
            model_name='itemsestacion',
            old_name='idItem',
            new_name='Item',
        ),
    ]