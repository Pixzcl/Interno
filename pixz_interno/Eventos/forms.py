import datetime
from django import forms

from .models import *

#fields = ['Titulo', 'Descripcion', 'Foto', ]
#exclude = ['campo1', 'campo2', ]

class ClientesForm(forms.ModelForm):
	class Meta:
		model = Clientes
		
		exclude = []
		widgets = {
			#'Calle': forms.TextInput(attrs={'onchange': "return codeAddress();"}),
			#'numeroCalle': forms.TextInput(attrs={'onchange': "return codeAddress();"}),
		}


class ActivacionesForm(forms.ModelForm):
	class Meta:
		model = Activaciones
		
		exclude = ["Cliente"]
		widgets = {
			"descripcion": forms.Textarea(attrs={'rows': 4}),
		}


# Opcional, con elección del cliente en un dropdown.
class ActivacionesSelectForm(forms.ModelForm):
	class Meta:
		model = Activaciones
		
		exclude = []
		widgets = {
			"descripcion": forms.Textarea(attrs={'rows': 4}),
		}

	def __init__(self, *args, **kwargs):
		super(ActivacionesSelectForm, self).__init__(*args, **kwargs)
		#self.fields['user'].queryset = User.objects.all()
		self.fields['Cliente'].label_from_instance = lambda obj: obj.nombre # lambda obj: "%s %s" % (obj.last_name, obj.first_name)


class EventosForm(forms.Form):
	#choices = [['1', 'First',], ['2', 'Second',]]
	choices = []
	planes = Planes.objects.all()
	for p in planes:
		if p.mostrar == True:
			choices.append([p.idPlan, p.nombre])

	#plan = forms.ChoiceField(label="Plan", choices=choices)
	fecha = forms.DateField(label="Fecha", initial=datetime.date.today(), widget=forms.SelectDateWidget())
	horas = forms.IntegerField(min_value=1, label="Horas")
	comentarios = forms.CharField(required=False, max_length=255, label="Comentarios", widget=forms.Textarea(attrs={'rows': 4}))
	
	def __init__(self, n, *args, **kwargs):
		super(EventosForm, self).__init__(*args, **kwargs)
		for i in range(1, n+1):
			self.fields['plan_%d' % i] = forms.ChoiceField(label="Plan %d" % i, choices=self.choices)


class EventosSelectForm(forms.Form):
	#choices = [['1', 'First',], ['2', 'Second',]]
	choices = []
	planes = Planes.objects.all()
	for p in planes:
		if p.mostrar == True:
			choices.append([p.idPlan, p.nombre])

	choices_activaciones = []
	activaciones = Activaciones.objects.all()
	for a in activaciones:
		choices_activaciones.append([a.idActivacion, a.nombre])
	
	activacion = forms.ChoiceField(label="Activación", choices=choices_activaciones)
	fecha = forms.DateField(label="Fecha", initial=datetime.date.today(), widget=forms.SelectDateWidget())
	horas = forms.IntegerField(min_value=1, label="Horas")
	comentarios = forms.CharField(required=False, max_length=255, label="Comentarios", widget=forms.Textarea(attrs={'rows': 4}))
	
	def __init__(self, n, *args, **kwargs):
		super(EventosSelectForm, self).__init__(*args, **kwargs)
		for i in range(1, n+1):
			self.fields['plan_%d' % i] = forms.ChoiceField(label="Plan %d" % i, choices=self.choices)


class PlanesForm(forms.Form):
	#choices = [['1', 'First',], ['2', 'Second',]]
	choices = []
	items = Items.objects.all()
	for it in items:
		choices.append([it.idItem, it.nombre])

	#plan = forms.ChoiceField(label="Plan", choices=choices)
	nombre = forms.CharField( max_length=255, label="Nombre") #, widget=forms.TextInput(attrs={'class': 'form-control'})) #formset para verificar uniqueness

	#item = forms.MultipleChoiceField(label="Item", widget=forms.SelectMultiple(choices=choices, attrs={'class': 'standardSelect'}))
	
	def __init__(self, n, *args, **kwargs):
		super(PlanesForm, self).__init__(*args, **kwargs)
		for i in range(1, n+1):
			self.fields['item_%d' % i] = forms.ChoiceField(label="Item %d" % i, choices=self.choices)


class EstacionesForm(forms.Form):
	#choices = [['1', 'First',], ['2', 'Second',]]
	choices = []
	items = Items.objects.all()
	for it in items:
		choices.append([it.idItem, it.nombre])

	#plan = forms.ChoiceField(label="Plan", choices=choices)
	nombre = forms.CharField(max_length=255, label="Nombre") #formset para verificar uniqueness
	
	def __init__(self, n, *args, **kwargs):
		super(EstacionesForm, self).__init__(*args, **kwargs)
		for i in range(1, n+1):
			self.fields['item_%d' % i] = forms.ChoiceField(label="Item %d" % i, choices=self.choices)


class ItemsForm(forms.ModelForm):
	class Meta:
		model = Items
		exclude = []
		widgets = {
		}


class TrabajadoresForm(forms.ModelForm):
	class Meta:
		model = Trabajadores
		exclude = []
		widgets = {
		}


class ContactosForm(forms.ModelForm):
	class Meta:
		model = Contactos
		exclude = ["Cliente"]
		widgets = {
		}
class ContactosFormSelect(forms.ModelForm):
	class Meta:
		model = Contactos
		exclude = []
		widgets = {
		}
	def __init__(self, *args, **kwargs):
		super(ContactosFormSelect, self).__init__(*args, **kwargs)
		#self.fields['user'].queryset = User.objects.all()
		self.fields['Cliente'].label_from_instance = lambda obj: obj.nombre # lambda obj: "%s %s" % (obj.last_name, obj.first_name)


class CoordinacionForm(forms.ModelForm):
	#choices = []
	#contactos = Contactos.objects.all()
	#for e in contactos:
	#	choices.append([e.idContacto, e.nombre])
	#contacto = forms.ChoiceField(label="Contacto", choices=choices)
	class Meta:
		model = Eventos
		fields = ["Contacto", "inicio_servicio", "fin_servicio", "fecha_instalacion", "hora_instalacion", "fecha_desinstalacion", "hora_desinstalacion", "direccion"]
		widgets = {
				"Contacto": forms.Select(attrs={'class': "standardSelect"}),
				"inicio_servicio": forms.TimeInput(attrs={'placeholder': "ej: 18:30", 'class': "form-control"}),
				"fin_servicio": forms.TimeInput(attrs={'placeholder': "ej: 18:30", 'class': "form-control"}),
				"hora_instalacion": forms.TimeInput(attrs={'placeholder': "ej: 18:30", 'class': "form-control"}),
				"hora_desinstalacion": forms.TimeInput(attrs={'placeholder': "ej: 18:30", 'class': "form-control"}),
				"fecha_instalacion": forms.SelectDateWidget(empty_label=("Año", "Mes", "Día"), attrs={'class': "standardSelect"}),
				"fecha_desinstalacion": forms.SelectDateWidget(empty_label=("Año", "Mes", "Día"), attrs={'class': "standardSelect"}),
				"direccion": forms.TextInput(attrs={'class': "form-control"}),
			}
	def __init__(self, *args, **kwargs):
		super(CoordinacionForm, self).__init__(*args, **kwargs)
		#self.fields['user'].queryset = User.objects.all()
		self.fields['Contacto'].label_from_instance = lambda obj: obj.nombre # lambda obj: "%s %s" % (obj.last_name, obj.first_name)


class LogisticaTrabajadoresForm(forms.Form):
	choices = []
	trabajadores = Trabajadores.objects.all()
	for t in trabajadores:
		choices.append([t.idTrabajador, t.nombre])

	Supervisor = forms.MultipleChoiceField(required=False, label="Supervisor(es)", choices=choices, widget=forms.SelectMultiple(attrs={'class': "standardSelect"}))
	Montaje = forms.MultipleChoiceField(required=False, label="Montaje", choices=choices, widget=forms.SelectMultiple(attrs={'class': "standardSelect"}))
	Desmontaje = forms.MultipleChoiceField(required=False, label="Desmontaje", choices=choices, widget=forms.SelectMultiple(attrs={'class': "standardSelect"}))
	Operador = forms.MultipleChoiceField(required=False, label="Operador(es)", choices=choices, widget=forms.SelectMultiple(attrs={'class': "standardSelect"}))
	
	#Trabajadores = forms.ModelMultipleChoiceField(queryset=Trabajadores.objects.all())
	#def __init__(self, nombre, *args, **kwargs):
	#	super(LogisticaTrabajadoresForm, self).__init__(*args, **kwargs)
	#	self.fields['Trabajadores'].label = "%s" % nombre

	

class LogisticaPlanesForm(forms.Form):
	#choices = []
	#estaciones = Estaciones.objects.all()
	#for p in planes:
	#	choices.append([p.idPlan, p.nombre])

	def __init__(self, planesEvento, *args, **kwargs):
		super(LogisticaPlanesForm, self).__init__(*args, **kwargs)

		estaciones = Estaciones.objects.all()
		for planEvento in planesEvento:
			for itemPlan in planEvento.Plan.ItemsPlan.all():
				choices = [["", "-----"]]
				for e in estaciones:
					if itemPlan.Item in e.Items.all():
						choices.append([e.ItemsEstacion.get(Item=itemPlan.Item).idItemsEstacion, e.nombre])
				print(choices)
				self.fields['planEvento_%d_itemPlan_%d' % (planEvento.idPlanesEvento, itemPlan.idItemsPlan)] = forms.ChoiceField(required=False, label='planEvento_%d_itemPlan_%d' % (planEvento.idPlanesEvento, itemPlan.idItemsPlan), choices=choices)