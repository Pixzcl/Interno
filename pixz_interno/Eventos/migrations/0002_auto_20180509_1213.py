# Generated by Django 2.0.5 on 2018-05-09 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Eventos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientes',
            name='idCliente',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='Id'),
        ),
    ]
