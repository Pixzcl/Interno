# Generated by Django 2.0.5 on 2018-05-24 16:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Eventos', '0023_auto_20180523_1157'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlanesTrabajador',
            fields=[
                ('idPlanesTrabajador', models.AutoField(primary_key=True, serialize=False, verbose_name='#')),
                ('idPlan', models.ForeignKey(on_delete=models.SET('Eliminado'), to='Eventos.Planes', verbose_name='Plan')),
                ('idTrabajador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Eventos.Trabajadores', verbose_name='Trabajador')),
            ],
        ),
        migrations.RemoveField(
            model_name='capacitaciontrabajador',
            name='idPlan',
        ),
        migrations.RemoveField(
            model_name='capacitaciontrabajador',
            name='idTrabajador',
        ),
        migrations.AddField(
            model_name='eventos',
            name='trabajadores',
            field=models.ManyToManyField(through='Eventos.TrabajadoresEvento', to='Eventos.Trabajadores'),
        ),
        migrations.DeleteModel(
            name='CapacitacionTrabajador',
        ),
    ]
