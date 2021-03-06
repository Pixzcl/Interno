from django.db import models
from django.contrib import auth

from datetime import date, timedelta

#from django.contrib.auth.models import AbstractUser
#class User(AbstractUser):
#	is_admin = models.BooleanField(default=False)
#	is_staff = models.BooleanField(default=False)
#	is_freelance = models.BooleanField(default=False)
	#user_type = models.CharField(max_length=255, verbose_name="Tipo de usuario", blank=False, null=False, choices=[["admin","Admin"], ["staff","Staff"], ["freelance","freelance"]] )

class TipoUsuario(models.Model):
	User = models.OneToOneField(auth.models.User, verbose_name="Tipo de usuario", related_name="TipoUsuario", on_delete=models.CASCADE, blank=False, null=False)
	tipo = models.CharField(max_length=255, verbose_name="Tipo de usuario", blank=False, null=False, default="freelance")
	#is_admin = models.BooleanField(default=False)
	#is_staff = models.BooleanField(default=False)
	#is_freelance = models.BooleanField(default=False)


class Clientes(models.Model):
	idCliente = models.AutoField(primary_key=True, verbose_name="#")
	nombre = models.CharField(unique=True, max_length=255, verbose_name="Nombre", blank=False, null=False, error_messages={"unique":"Ya existe un cliente con este nombre."})
	direccion = models.CharField(max_length=255, verbose_name="Dirección", blank=True, null=True, default="")

	class Meta:
		ordering = ['-idCliente']
	

class Activaciones(models.Model):
	idActivacion = models.AutoField(primary_key=True, verbose_name="#")
	Cliente = models.ForeignKey("Clientes", verbose_name="Cliente", related_name="Activaciones", on_delete=models.CASCADE, blank=False, null=False) #to_field="idCliente"

	nombre = models.CharField(max_length=255, verbose_name="Nombre", blank=False, null=False)
	monto = models.PositiveIntegerField(verbose_name="Monto de venta", blank=False, null=False)
	montoIVA = models.PositiveIntegerField(verbose_name="Monto con IVA", blank=False, null=False)
	#adelanto = models.PositiveIntegerField(verbose_name="Adelanto", blank=False, null=False, default=0)
	tipo = models.CharField(max_length=255, verbose_name="Tipo", blank=False, null=False)
	descripcion = models.TextField(verbose_name="Descripción", blank=True, null=True, default="")

	class Meta:
		ordering = ['-idActivacion']

	@classmethod
	def por_cobrar(self):
		activaciones = self.objects.all()
		por_cobrar = []
		for a in activaciones:
			monto_restante = a.montoIVA
			if monto_restante == 0:
				por_cobrar.append(a.idActivacion)
			else:
				ingresos = a.Ingresos.all()
				for i in ingresos:
					monto_restante -= i.monto
				if monto_restante > 0:
					por_cobrar.append(a.idActivacion)
		return self.objects.filter(idActivacion__in=por_cobrar)

	@classmethod
	def vencidas(self):
		por_cobrar = self.por_cobrar()
		vencidas = []
		hoy = date.today()
		for p in por_cobrar:
			if p.tipo == "Weddi":
				for e in p.Eventos.all():
					if hoy > (e.fecha - timedelta(days=7)):
						vencidas.append(p.idActivacion)
						break
			else:
				for f in p.Facturas.all():
					if hoy > f.fecha_pago:
						vencidas.append(p.idActivacion)
						break
		return self.objects.filter(idActivacion__in=vencidas)

	@classmethod
	def por_vencer(self):
		por_cobrar = self.por_cobrar()
		por_vencer = []
		hoy = date.today()
		for p in por_cobrar:
			if p.tipo == "Weddi":
				for e in p.Eventos.all():
					if (((e.fecha - timedelta(days=7)) - hoy) <= timedelta(days=3)) and (((e.fecha - timedelta(days=7)) - hoy) >= timedelta(days=0)):
						por_vencer.append(p.idActivacion)
						break
			else:
				for f in p.Facturas.all():
					if ((f.fecha_pago - hoy) <= timedelta(days=3)) and ((f.fecha_pago - hoy) >= timedelta(days=0)):
						por_vencer.append(p.idActivacion)
						break
		return self.objects.filter(idActivacion__in=por_vencer)


class Eventos(models.Model):
	idEvento = models.AutoField(primary_key=True, verbose_name="#")
	Activacion = models.ForeignKey("Activaciones", verbose_name="Activación", related_name="Eventos", on_delete=models.CASCADE, blank=False, null=False)
	Contacto = models.ForeignKey("Contactos", verbose_name="Contacto", related_name="Eventos", on_delete=models.SET(None), blank=True, null=True)
	Planes = models.ManyToManyField("Planes", through="PlanesEvento", related_name="Eventos")
	Trabajadores = models.ManyToManyField("Trabajadores", through="TrabajadoresEvento", related_name="Eventos")
	
	nombre = models.CharField(max_length=255, verbose_name="Nombre", blank=False, null=False)
	#horas = models.DecimalField(max_digits=3, decimal_places=1, verbose_name="Horas", blank=False, null=False)
	horas = models.PositiveSmallIntegerField(verbose_name="Horas", blank=False, null=False)
	fecha = models.DateField(verbose_name="Fecha", blank=False, null=False)
	comentarios = models.TextField(verbose_name="Comentarios", blank=True, null=True, default="")
	
	# Logística
	#fecha_y_hora_instalacion = models.DateTimeField(verbose_name="Fecha y hora de instalacion", blank=True, null=True)
	#fecha_y_hora_desinstalacion = models.DateTimeField(verbose_name="Fecha y hora de desinstalacion", blank=True, null=True)
	fecha_instalacion = models.DateField(verbose_name="Fecha de instalacion", blank=True, null=True)
	fecha_desinstalacion = models.DateField(verbose_name="Fecha de desinstalacion", blank=True, null=True)
	hora_instalacion = models.TimeField(verbose_name="Hora de instalacion", blank=True, null=True)
	hora_desinstalacion = models.TimeField(verbose_name="Hora de desinstalacion", blank=True, null=True)
	inicio_servicio = models.TimeField(verbose_name="Inicio del servicio", blank=True, null=True)
	fin_servicio = models.TimeField(verbose_name="Fin del servicio", blank=True, null=True)
	direccion = models.CharField(max_length=255, verbose_name="Dirección", blank=True, null=True)

	# Tareas recurrentes en checklist
	Recurrentes = models.ManyToManyField("Recurrentes", through="RecurrentesEvento", related_name="Eventos")
	# Tareas pendientes en checkout
	Pendientes = models.ManyToManyField("Pendientes", through="PendientesEvento", related_name="Eventos")
	# Cual es el proximo paso por ingresar en el evento
	estado = models.IntegerField(verbose_name="Estado", blank=False, null=False, default=0)
	# Satisfaccion del cliente
	satisfaccion = models.SmallIntegerField(verbose_name="Satisfacción", blank=True, null=True)
	comentarios_satisfaccion = models.TextField(verbose_name="Comentarios satisfacción", blank=True, null=True, default="")

	# Itinerario - Seguimiento
	seguimiento_instalacion = models.TextField(verbose_name="Estado instalación", blank=False, null=False, default="")
	seguimiento_desinstalacion = models.TextField(verbose_name="Estado desinstalación", blank=False, null=False, default="")
	seguimiento_inicio_servicio = models.TextField(verbose_name="Estado inicio de servicio", blank=False, null=False, default="")
	seguimiento_fin_servicio = models.TextField(verbose_name="Estado fin de servicio", blank=False, null=False, default="")
	
	class Meta:
		ordering = ['-idEvento']


class Contactos(models.Model):
	idContacto = models.AutoField(primary_key=True, verbose_name="#")
	Cliente = models.ForeignKey("Clientes", verbose_name="Cliente", related_name="Contactos", on_delete=models.SET(None), blank=False, null=True)
	
	nombre = models.CharField(unique=True, max_length=255, verbose_name="Nombre", blank=False, null=False, error_messages={"unique":"Ya existe un contacto con este nombre."})
	#rut = models.CharField(max_length=255, verbose_name="RUT", blank=True, null=True, default="")
	telefono = models.CharField(max_length=255, verbose_name="Teléfono", blank=True, null=True, default="")
	mail = models.EmailField(max_length=255, verbose_name="Mail", blank=True, null=True, default="")

	class Meta:
		ordering = ['-idContacto']


class Trabajadores(models.Model):
	idTrabajador = models.AutoField(primary_key=True, verbose_name="#")

	nombre = models.CharField(unique=True, max_length=255, verbose_name="Nombre", blank=False, null=False, error_messages={"unique":"Ya existe un trabajador con este nombre."})
	rut = models.CharField(unique=True, max_length=255, verbose_name="RUT", blank=True, null=True, default="", error_messages={"unique":"Ya existe un trabajador con este RUT."})
	telefono = models.CharField(unique=True, max_length=255, verbose_name="Teléfono", blank=True, null=True, default="", error_messages={"unique":"Ya existe un trabajador con este teléfono."})
	mail = models.EmailField(unique=True, max_length=255, verbose_name="Mail", blank=True, null=True, default="", error_messages={"unique":"Ya existe un trabajador con este mail."})

	class Meta:
		ordering = ['-idTrabajador']


class TrabajadoresEvento(models.Model):
	idTrabajadorEvento = models.AutoField(primary_key=True, verbose_name="#")
	Trabajador = models.ForeignKey("Trabajadores", verbose_name="Trabajador", related_name="TrabajadoresEvento", on_delete=models.CASCADE, blank=False, null=False)
	Evento = models.ForeignKey("Eventos", verbose_name="Evento", related_name="TrabajadoresEvento", on_delete=models.CASCADE, blank=False, null=False)
	Cargo = models.ForeignKey("Cargos", verbose_name="Cargo", related_name="TrabajadoresEvento", on_delete=models.SET(None), blank=True, null=True)
	#tipo = models.CharField(max_length=255, verbose_name="Tipo", blank=False, null=False)


class PlanesTrabajador(models.Model):
	idPlanesTrabajador = models.AutoField(primary_key=True, verbose_name="#")
	Trabajador = models.ForeignKey("Trabajadores", verbose_name="Trabajador", related_name="PlanesTrabajador", on_delete=models.CASCADE, blank=False, null=False)
	Plan = models.ForeignKey("Planes", verbose_name="Plan", related_name="PlanesTrabajador", on_delete=models.CASCADE, blank=False, null=False)


class PlanesEvento(models.Model):
	idPlanesEvento = models.AutoField(primary_key=True, verbose_name="#")
	Evento = models.ForeignKey("Eventos", verbose_name="Evento", related_name="PlanesEvento", on_delete=models.CASCADE, blank=False, null=False)
	Plan = models.ForeignKey("Planes", verbose_name="Plan", related_name="PlanesEvento", on_delete=models.PROTECT, blank=False, null=False)
	ItemsPlan = models.ManyToManyField("ItemsPlan", through="ItemsPlanEvento", related_name="PlanesEvento")
	ItemsEstacion = models.ManyToManyField("ItemsEstacion", through="ItemsPlanEvento", related_name="PlanesEvento")
	cantidad = models.PositiveSmallIntegerField(verbose_name="Cantidad", blank=False, null=False, default=1)
	n = models.PositiveSmallIntegerField(verbose_name="n", blank=False, null=False, default=1) # solo para mantenerlo en el orden que se ingrese
	class Meta:
		ordering = ['n']


class ItemsPlanEvento(models.Model):
	idItemsPlanEvento = models.AutoField(primary_key=True, verbose_name="#")
	PlanesEvento = models.ForeignKey("PlanesEvento", verbose_name="Plan evento", related_name="ItemsPlanEvento", on_delete=models.CASCADE, blank=False, null=False)
	ItemsPlan = models.ForeignKey("ItemsPlan", verbose_name="Item plan", related_name="ItemsPlanEvento", on_delete=models.CASCADE, blank=False, null=True)
	ItemsEstacion = models.ForeignKey("ItemsEstacion", verbose_name="Item estación", related_name="ItemsPlanEvento", on_delete=models.SET(None), blank=True, null=True, default=None)
	check = models.BooleanField(verbose_name="Check", default=False)
	nItem = models.PositiveSmallIntegerField(verbose_name="n", blank=False, null=False, default=1)
	nPlan = models.PositiveSmallIntegerField(verbose_name="n", blank=False, null=False, default=1)
	class Meta:
		# IMPORTANTE no cambiar este orden, se usa para crear correctamente lista_planes en view eventos
		ordering = ['PlanesEvento', 'nPlan', 'ItemsPlan', 'nItem']


class Planes(models.Model):
	idPlan = models.AutoField(primary_key=True, verbose_name="#")
	mostrar = models.BooleanField(verbose_name="Mostrar en listado", default=True)
	Items = models.ManyToManyField("Items", through="ItemsPlan", related_name="Planes")
	Trabajadores = models.ManyToManyField("Trabajadores", through="PlanesTrabajador", related_name="Planes")

	nombre = models.CharField(unique=True, max_length=255, verbose_name="Nombre", blank=False, null=False, error_messages={"unique":"Ya existe un plan con este nombre."})


class ItemsPlan(models.Model):
	idItemsPlan = models.AutoField(primary_key=True, verbose_name="#")
	Plan = models.ForeignKey("Planes", verbose_name="Plan", related_name="ItemsPlan", on_delete=models.CASCADE, blank=False, null=False)
	Item = models.ForeignKey("Items", verbose_name="Item", related_name="ItemsPlan", on_delete=models.CASCADE, blank=False, null=False)
	#item = models.CharField(max_length=255, verbose_name="Item", blank=False, null=False)
	ItemsEstacion = models.ManyToManyField("ItemsEstacion", through="ItemsPlanEvento", related_name="ItemsPlan")
	cantidad = models.PositiveSmallIntegerField(verbose_name="Cantidad", blank=False, null=False, default=1)
	n = models.PositiveSmallIntegerField(verbose_name="n", blank=False, null=False, default=1) # solo para mantenerlo en el orden que se ingrese
	class Meta:
		ordering = ['n']


class Estaciones(models.Model):
	idEstacion = models.AutoField(primary_key=True, verbose_name="#")
	nombre = models.CharField(unique=True, max_length=255, verbose_name="Nombre", blank=False, null=False, error_messages={"unique":"Ya existe una estación con este nombre."})
	Items = models.ManyToManyField("Items", through="ItemsEstacion", related_name="Estaciones")


class ItemsEstacion(models.Model):
	idItemsEstacion = models.AutoField(primary_key=True, verbose_name="#")
	Estacion = models.ForeignKey("Estaciones", verbose_name="Estación", related_name="ItemsEstacion", on_delete=models.CASCADE, blank=False, null=False)
	Item = models.ForeignKey("Items", verbose_name="Item", related_name="ItemsEstacion", on_delete=models.CASCADE, blank=False, null=False)
	#item = models.CharField(max_length=255, verbose_name="Item", blank=False, null=False)
	cantidad = models.PositiveSmallIntegerField(verbose_name="Cantidad", blank=False, null=False, default=1)
	n = models.PositiveSmallIntegerField(verbose_name="n", blank=False, null=False, default=1) # solo para mantenerlo en el orden que se ingrese
	class Meta:
		ordering = ['n']


class Items(models.Model):
	idItem = models.AutoField(primary_key=True, verbose_name="#")
	
	nombre = models.CharField(unique=True, max_length=255, verbose_name="Nombre", blank=False, null=False, error_messages={"unique":"Ya existe un item con este nombre."})
	multiple = models.BooleanField(verbose_name="Multiple", default=False)


class Cargos(models.Model):
	idCargo = models.AutoField(primary_key=True, verbose_name="#")
	nombre = models.CharField(unique=True, max_length=255, verbose_name="Nombre", blank=False, null=False, error_messages={"unique":"Ya existe un cargo con este nombre."})
	n = models.PositiveSmallIntegerField(verbose_name="N°", blank=False, null=False, default=1) # solo para mantenerlo en el orden que se ingrese
	class Meta:
		ordering = ['n']

#Tareas recurrentes en checklist
class Recurrentes(models.Model):
	idRecurrente = models.AutoField(primary_key=True, verbose_name="#")
	nombre = models.CharField(unique=True, max_length=255, verbose_name="Nombre", blank=False, null=False, error_messages={"unique":"Ya existe una tarea recurrente con este nombre."})
	n = models.PositiveSmallIntegerField(verbose_name="N°", blank=False, null=False, default=1) # solo para mantenerlo en el orden que se ingrese
	class Meta:
		ordering = ['n']

#Tareas pendientes en checkout
class Pendientes(models.Model):
	idPendiente = models.AutoField(primary_key=True, verbose_name="#")
	nombre = models.CharField(unique=True, max_length=255, verbose_name="Nombre", blank=False, null=False, error_messages={"unique":"Ya existe una tarea pendiente con este nombre."})
	n = models.PositiveSmallIntegerField(verbose_name="N°", blank=False, null=False, default=1) # solo para mantenerlo en el orden que se ingrese
	class Meta:
		ordering = ['n']


class RecurrentesEvento(models.Model):
	idRecurrentesEvento = models.AutoField(primary_key=True, verbose_name="#")
	Recurrente = models.ForeignKey("Recurrentes", verbose_name="Recurrentes", related_name="RecurrentesEvento", on_delete=models.CASCADE, blank=False, null=False)
	Evento = models.ForeignKey("Eventos", verbose_name="Evento", related_name="RecurrentesEvento", on_delete=models.CASCADE, blank=False, null=False)
	check = models.BooleanField(verbose_name="Check", default=False)


class PendientesEvento(models.Model):
	idPlanesTrabajador = models.AutoField(primary_key=True, verbose_name="#")
	Pendiente = models.ForeignKey("Pendientes", verbose_name="Pendientes", related_name="PendientesEvento", on_delete=models.CASCADE, blank=False, null=False)
	Evento = models.ForeignKey("Eventos", verbose_name="Evento", related_name="PendientesEvento", on_delete=models.CASCADE, blank=False, null=False)
	check = models.BooleanField(verbose_name="Check", default=False)


class Errores(models.Model):
	idError = models.AutoField(primary_key=True, verbose_name="#")
	Evento = models.ForeignKey("Eventos", verbose_name="Evento", related_name="Errores", on_delete=models.SET(None), blank=True, null=True)
	error = models.TextField(verbose_name="Errores técnicos", blank=True, null=True, default="")
	resuelto = models.BooleanField(verbose_name="Resuelto", default=False)

	class Meta:
		ordering = ['-idError']

class Facturas(models.Model):
	#idFacturacion = models.AutoField(primary_key=True, verbose_name="#")
	nFactura = models.PositiveIntegerField(primary_key=True, unique=True, verbose_name="N° de factura", blank=False, null=False, error_messages={"unique":"Ya existe este número de factura."})
	Activacion = models.ForeignKey("Activaciones", verbose_name="Activacion", related_name="Facturas", on_delete=models.SET(None), blank=False, null=True)
	fecha_facturacion = models.DateField(verbose_name="Fecha de facturación", blank=False, null=False)
	monto = models.PositiveIntegerField(verbose_name="Monto", blank=False, null=False)
	montoIVA = models.PositiveIntegerField(verbose_name="Monto con IVA", blank=False, null=False)
	#pago = models.PositiveIntegerField(verbose_name="Pago", blank=False, null=False)
	#plazo = models.PositiveSmallIntegerField(verbose_name="Plazo", blank=False, null=False)
	fecha_pago = models.DateField(verbose_name="Fecha de pago", blank=False, null=False)

	class Meta:
		ordering = ['-nFactura']

	def pagada(self):
		ingresos = self.Ingresos.all()
		monto_restante = self.montoIVA
		for i in ingresos:
			monto_restante -= i.monto

		if monto_restante <= 0:
			return True
		else:
			return False

	@classmethod
	def pagadas(self):
		facturas = self.objects.all()
		pagadas = []
		total = 0
		for f in facturas:
			ingresos = f.Ingresos.all()
			monto_restante = f.montoIVA
			for i in ingresos:
				monto_restante -= i.monto
				total += i.monto
			if monto_restante <= 0:
				pagadas.append(f.nFactura)
		return [self.objects.filter(nFactura__in=pagadas), total]

	@classmethod
	def pendientes(self):
		facturas = self.objects.all()
		pendientes = []
		total = 0
		for f in facturas:
			ingresos = f.Ingresos.all()
			monto_restante = f.montoIVA
			for i in ingresos:
				monto_restante -= i.monto
			if monto_restante > 0:
				pendientes.append(f.nFactura)
				total += monto_restante
		return [self.objects.filter(nFactura__in=pendientes), total]


class Ingresos(models.Model):
	idIngreso = models.AutoField(primary_key=True, verbose_name="#")
	Activacion = models.ForeignKey("Activaciones", verbose_name="Activacion", related_name="Ingresos", on_delete=models.SET(None), blank=False, null=True)
	Factura = models.ForeignKey("Facturas", verbose_name="Factura", related_name="Ingresos", on_delete=models.CASCADE, blank=False, null=True)

	fecha = models.DateField(verbose_name="Fecha", blank=False, null=False)
	monto = models.PositiveIntegerField(verbose_name="Monto", blank=False, null=False)
	comentarios = models.TextField(verbose_name="Comentarios", blank=True, null=True, default="")


class CostosVariables(models.Model):
	idCostoVariable = models.AutoField(primary_key=True, verbose_name="#")
	documento = models.CharField(max_length=255, verbose_name="Documento", blank=False, null=False)
	Tipo = models.ForeignKey("TiposCostoVariable", verbose_name="Tipo", related_name="CostosVariables", on_delete=models.SET(None), blank=True, null=True)
	monto = models.PositiveIntegerField(verbose_name="Monto", blank=False, null=False)
	Evento = models.ForeignKey("Eventos", verbose_name="Evento", related_name="CostosVariables", on_delete=models.SET(None), blank=True, null=True)
	fecha = models.DateField(verbose_name="Fecha", blank=False, null=False)
	comentarios = models.TextField(verbose_name="Comentarios", blank=True, null=True, default="")


class TiposCostoVariable(models.Model):
	idTipoCostoVariable = models.AutoField(primary_key=True, verbose_name="#")
	nombre = models.CharField(unique=True, max_length=255, verbose_name="Nombre", blank=False, null=False, error_messages={"unique":"Ya existe un costo variable con este nombre."})
	class Meta:
		ordering = ['nombre']


class Metas(models.Model):
	idMeta = models.AutoField(primary_key=True, verbose_name="#")
	mes = models.DateField(unique=True, verbose_name="Mes", blank=False, null=False, error_messages={"unique":"Ya existe una meta para este mes."})
	meta = models.PositiveIntegerField(verbose_name="Meta", blank=False, null=False, default=0)
	class Meta:
		ordering = ['-mes']
