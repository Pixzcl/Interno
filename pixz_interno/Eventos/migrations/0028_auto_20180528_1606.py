# Generated by Django 2.0.5 on 2018-05-28 20:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Eventos', '0027_auto_20180524_1503'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eventos',
            old_name='planes',
            new_name='Planes',
        ),
    ]