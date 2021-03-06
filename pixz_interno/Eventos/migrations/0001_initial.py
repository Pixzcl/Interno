# Generated by Django 2.0.5 on 2018-06-05 21:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activaciones',
            fields=[
                ('idActivacion', models.AutoField(primary_key=True, serialize=False, verbose_name='#')),
                ('nombre', models.CharField(max_length=255, verbose_name='Activación')),
                ('descripcion', models.TextField(blank=True, default='', null=True, verbose_name='Descripción')),
            ],
        ),
        migrations.CreateModel(
            name='Clientes',
            fields=[
                ('idCliente', models.AutoField(primary_key=True, serialize=False, verbose_name='#')),
                ('nombre', models.CharField(max_length=255, unique=True, verbose_name='Cliente')),
                ('direccion', models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='Dirección')),
            ],
        ),
        migrations.CreateModel(
            name='Contactos',
            fields=[
                ('idContacto', models.AutoField(primary_key=True, serialize=False, verbose_name='#')),
                ('nombre', models.CharField(max_length=255, unique=True, verbose_name='Nombre')),
                ('telefono', models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='Teléfono')),
                ('mail', models.EmailField(blank=True, default='', max_length=255, null=True, verbose_name='Mail')),
                ('Cliente', models.ForeignKey(on_delete=models.SET('Cliente eliminado'), related_name='Contactos', to='Eventos.Clientes', verbose_name='Cliente')),
            ],
        ),
        migrations.CreateModel(
            name='Estaciones',
            fields=[
                ('idEstacion', models.AutoField(primary_key=True, serialize=False, verbose_name='#')),
                ('nombre', models.CharField(max_length=255, unique=True, verbose_name='Estación')),
            ],
        ),
        migrations.CreateModel(
            name='Eventos',
            fields=[
                ('idEvento', models.AutoField(primary_key=True, serialize=False, verbose_name='#')),
                ('horas', models.PositiveSmallIntegerField(verbose_name='Horas')),
                ('fecha', models.DateField(verbose_name='Fecha')),
                ('comentarios', models.TextField(blank=True, default='', null=True, verbose_name='Comentarios')),
                ('fecha_instalacion', models.DateField(blank=True, null=True, verbose_name='Fecha de instalacion')),
                ('fecha_desinstalacion', models.DateField(blank=True, null=True, verbose_name='Fecha de desinstalacion')),
                ('hora_instalacion', models.TimeField(blank=True, null=True, verbose_name='Hora de instalacion')),
                ('hora_desinstalacion', models.TimeField(blank=True, null=True, verbose_name='Hora de desinstalacion')),
                ('inicio_servicio', models.TimeField(blank=True, null=True, verbose_name='Inicio del servicio')),
                ('fin_servicio', models.TimeField(blank=True, null=True, verbose_name='Fin del servicio')),
                ('direccion', models.CharField(blank=True, max_length=255, null=True, verbose_name='Dirección')),
                ('Activacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Eventos', to='Eventos.Activaciones', verbose_name='Activación')),
                ('Contacto', models.ForeignKey(blank=True, null=True, on_delete=models.SET('Persona eliminada'), related_name='Eventos', to='Eventos.Contactos', verbose_name='Contacto')),
            ],
        ),
        migrations.CreateModel(
            name='Items',
            fields=[
                ('idItem', models.AutoField(primary_key=True, serialize=False, verbose_name='#')),
                ('nombre', models.CharField(max_length=255, unique=True, verbose_name='Item')),
            ],
        ),
        migrations.CreateModel(
            name='ItemsEstacion',
            fields=[
                ('idItemsEstacion', models.AutoField(primary_key=True, serialize=False, verbose_name='#')),
                ('Estacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ItemsEstacion', to='Eventos.Estaciones', verbose_name='Estación')),
                ('Item', models.ForeignKey(on_delete=models.SET('Item eliminado de Items'), related_name='ItemsEstacion', to='Eventos.Items', verbose_name='Item')),
            ],
        ),
        migrations.CreateModel(
            name='ItemsPlan',
            fields=[
                ('idItemsPlan', models.AutoField(primary_key=True, serialize=False, verbose_name='#')),
                ('Item', models.ForeignKey(on_delete=models.SET('Item eliminado de Items'), related_name='ItemsPlan', to='Eventos.Items', verbose_name='Item')),
            ],
        ),
        migrations.CreateModel(
            name='ItemsPlanEvento',
            fields=[
                ('idItemsPlanEvento', models.AutoField(primary_key=True, serialize=False, verbose_name='#')),
                ('ItemsEstacion', models.ForeignKey(blank=True, null=True, on_delete=models.SET('Item eliminado de la estación'), related_name='ItemsPlanEvento', to='Eventos.ItemsEstacion', verbose_name='Item estación')),
                ('ItemsPlan', models.ForeignKey(on_delete=models.SET('Item eliminado del plan'), related_name='ItemsPlanEvento', to='Eventos.ItemsPlan', verbose_name='Item plan')),
            ],
        ),
        migrations.CreateModel(
            name='Planes',
            fields=[
                ('idPlan', models.AutoField(primary_key=True, serialize=False, verbose_name='#')),
                ('mostrar', models.BooleanField(default=True, verbose_name='Mostrar en listado')),
                ('nombre', models.CharField(max_length=255, unique=True, verbose_name='Plan')),
                ('Items', models.ManyToManyField(related_name='Planes', through='Eventos.ItemsPlan', to='Eventos.Items')),
            ],
        ),
        migrations.CreateModel(
            name='PlanesEvento',
            fields=[
                ('idPlanesEvento', models.AutoField(primary_key=True, serialize=False, verbose_name='#')),
                ('Evento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='PlanesEvento', to='Eventos.Eventos', verbose_name='Evento')),
                ('ItemsEstacion', models.ManyToManyField(related_name='PlanesEvento', through='Eventos.ItemsPlanEvento', to='Eventos.ItemsEstacion')),
                ('ItemsPlan', models.ManyToManyField(related_name='PlanesEvento', through='Eventos.ItemsPlanEvento', to='Eventos.ItemsPlan')),
                ('Plan', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='PlanesEvento', to='Eventos.Planes', verbose_name='Plan')),
            ],
        ),
        migrations.CreateModel(
            name='PlanesTrabajador',
            fields=[
                ('idPlanesTrabajador', models.AutoField(primary_key=True, serialize=False, verbose_name='#')),
                ('Plan', models.ForeignKey(on_delete=models.SET('Eliminado'), related_name='PlanesTrabajador', to='Eventos.Planes', verbose_name='Plan')),
            ],
        ),
        migrations.CreateModel(
            name='Trabajadores',
            fields=[
                ('idTrabajador', models.AutoField(primary_key=True, serialize=False, verbose_name='#')),
                ('nombre', models.CharField(error_messages={'unique': 'Ya existe un trabajador con este nombre'}, max_length=255, unique=True, verbose_name='Nombre')),
                ('rut', models.CharField(blank=True, default='', max_length=255, null=True, unique=True, verbose_name='RUT')),
                ('telefono', models.CharField(blank=True, default='', max_length=255, null=True, unique=True, verbose_name='Teléfono')),
                ('mail', models.EmailField(blank=True, default='', max_length=255, null=True, unique=True, verbose_name='Mail')),
            ],
        ),
        migrations.CreateModel(
            name='TrabajadoresEvento',
            fields=[
                ('idTrabajadorEvento', models.AutoField(primary_key=True, serialize=False, verbose_name='#')),
                ('tipo', models.CharField(max_length=255, verbose_name='Tipo')),
                ('Evento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='TrabajadoresEvento', to='Eventos.Eventos', verbose_name='Evento')),
                ('Trabajador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='TrabajadoresEvento', to='Eventos.Trabajadores', verbose_name='Trabajador')),
            ],
        ),
        migrations.AddField(
            model_name='planestrabajador',
            name='Trabajador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='PlanesTrabajador', to='Eventos.Trabajadores', verbose_name='Trabajador'),
        ),
        migrations.AddField(
            model_name='planes',
            name='Trabajadores',
            field=models.ManyToManyField(related_name='Planes', through='Eventos.PlanesTrabajador', to='Eventos.Trabajadores'),
        ),
        migrations.AddField(
            model_name='itemsplanevento',
            name='PlanesEvento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ItemsPlanEvento', to='Eventos.PlanesEvento', verbose_name='Plan evento'),
        ),
        migrations.AddField(
            model_name='itemsplan',
            name='ItemsEstacion',
            field=models.ManyToManyField(related_name='ItemsPlan', through='Eventos.ItemsPlanEvento', to='Eventos.ItemsEstacion'),
        ),
        migrations.AddField(
            model_name='itemsplan',
            name='Plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ItemsPlan', to='Eventos.Planes', verbose_name='Plan'),
        ),
        migrations.AddField(
            model_name='eventos',
            name='Planes',
            field=models.ManyToManyField(related_name='Eventos', through='Eventos.PlanesEvento', to='Eventos.Planes'),
        ),
        migrations.AddField(
            model_name='eventos',
            name='Trabajadores',
            field=models.ManyToManyField(related_name='Eventos', through='Eventos.TrabajadoresEvento', to='Eventos.Trabajadores'),
        ),
        migrations.AddField(
            model_name='estaciones',
            name='Items',
            field=models.ManyToManyField(related_name='Estaciones', through='Eventos.ItemsEstacion', to='Eventos.Items'),
        ),
        migrations.AddField(
            model_name='activaciones',
            name='Cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Activaciones', to='Eventos.Clientes', verbose_name='Cliente'),
        ),
    ]
