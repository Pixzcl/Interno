# Generated by Django 2.0.5 on 2018-05-28 20:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Eventos', '0040_auto_20180528_1617'),
    ]

    operations = [
        migrations.RenameField(
            model_name='planesevento',
            old_name='itemsEstacion',
            new_name='ItemsEstacion',
        ),
    ]
