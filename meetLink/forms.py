from django import forms
from django.utils import timezone
from .models import Usuario, Contacto, GrupoContacto, Evento
from django.contrib.auth.forms import UserCreationForm



############################! SESIÓN !###########################
class UsuarioCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'nombre', 'apellidos', 'email', 'password1', 'password2', 'avatar']



############################! CONTACTOS !###########################
class ContactoCreationForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ['nombre', 'mail', 'telefono']
        
class ContactoUpdateForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ['nombre', 'mail', 'telefono']



############################! GRUPOS CONTACTO !###########################
class GrupoContactoCreationForm(forms.ModelForm):
    class Meta:
        model = GrupoContacto
        fields = ['nombre', 'descripcion', 'integrantes']   # No se incluye user porque se añade en la vista
        widgets = {
            'integrantes': forms.SelectMultiple(attrs={
                'class': 'form-select',
                'size': 5  # Opciones visibles en la lista
            }),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')                           # Extraer el usuario que pasamos desde la vista
        super().__init__(*args, **kwargs)
        
        # Filtrar los contactos para que solo salgan los del usuario logueado:
        self.fields['integrantes'].queryset = Contacto.objects.filter(usuario=user)

class GrupoContactoUpdateForm(forms.ModelForm):
    class Meta:
        model = GrupoContacto
        fields = ['nombre', 'descripcion', 'integrantes']
        widgets = {
            'integrantes': forms.SelectMultiple(attrs={
                'class': 'form-select',
                'size': 5  # Opciones visibles en la lista
            }),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        # Solo mostrar contactos del usuario
        self.fields['integrantes'].queryset = Contacto.objects.filter(usuario=self.user)

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')

        # Buscar grupos con ese nombre para el usuario actual:
        grupo_existente = GrupoContacto.objects.filter(nombre=nombre, usuario=self.user)

        # Excluir el grupo actual si es una edición (para eliminar error en formulario de editar)
        if self.instance.pk:
            grupo_existente = grupo_existente.exclude(pk=self.instance.pk)

        if grupo_existente.exists():
            raise forms.ValidationError("Ya tienes un grupo con ese nombre.")

        return nombre



############################! EVENTOS !###########################

# Para poder mostrar la fecha con el widget en Update de Eventos hay que cambiar el formato para adaptar lo guardado por Django al datetime-local que lee el widget
class DateTimeLocalInput(forms.DateTimeInput):
    input_type = 'datetime-local'

    def format_value(self, value):
        if value is None:
            return ''
        return value.strftime('%Y-%m-%dT%H:%M')


class EventoCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['grupo'].queryset = self.user.grupocontacto_set.all()
            self.fields['grupo'].empty_label = "Selecciona un grupo"
            self.fields['grupo'].required = True

    class Meta:
        model = Evento
        fields = [
            'nombre', 'descripcion', 'ubicacion', 'fecha_inicio', 'fecha_fin',
            'transporte', 'presupuesto', 'grupo', 'maleta', 'todo'
        ]
        widgets = {
            'fecha_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'fecha_fin': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'presupuesto': forms.Select(choices=[(True, 'Sí'), (False, 'No')]),
            'maleta': forms.Select(choices=[(True, 'Sí'), (False, 'No')]),
            'todo': forms.Select(choices=[(True, 'Sí'), (False, 'No')]),
        }

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')
        nombre = cleaned_data.get('nombre')

        from django.utils import timezone
        now = timezone.now()

        if fecha_inicio and fecha_inicio < now:
            self.add_error('fecha_inicio', "La fecha de inicio debe ser igual o mayor a la fecha actual.")
        if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
            self.add_error('fecha_fin', "La fecha de fin no puede ser anterior a la fecha de inicio.")

        # Validar nombre único para el usuario
        if nombre and self.user:
            exists = Evento.objects.filter(nombre=nombre, usuario=self.user)
            if self.instance.pk:
                exists = exists.exclude(pk=self.instance.pk)
            if exists.exists():
                self.add_error('nombre', "Ya tienes un evento con este nombre.")

        return cleaned_data


class EventoUpdateForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = [
            'nombre', 'descripcion', 'ubicacion', 'fecha_inicio', 'fecha_fin',
            'transporte', 'presupuesto', 'grupo', 'maleta', 'todo'
        ]
        widgets = {
            'fecha_inicio': DateTimeLocalInput(),
            'fecha_fin': DateTimeLocalInput(),
            'presupuesto': forms.Select(choices=[(True, 'Sí'), (False, 'No')]),
            'maleta': forms.Select(choices=[(True, 'Sí'), (False, 'No')]),
            'todo': forms.Select(choices=[(True, 'Sí'), (False, 'No')]),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['grupo'].queryset = GrupoContacto.objects.filter(usuario=self.user)
        self.fields['grupo'].empty_label = "Selecciona un grupo"

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre:
            qs = Evento.objects.filter(nombre=nombre, usuario=self.user)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("Ya tienes otro evento con ese nombre.")
        return nombre

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')

        from django.utils import timezone
        now = timezone.now()

        if fecha_inicio and fecha_inicio < now:
            self.add_error('fecha_inicio', "La fecha de inicio no puede ser anterior a hoy.")
        if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
            self.add_error('fecha_fin', "La fecha de fin no puede ser anterior a la de inicio.")

        return cleaned_data

            
            
            
############################! PRESUPUESTO !###########################
         
class PresupuestoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['p_alojamiento', 'p_transporte', 'p_comida', 'p_otros']
        widgets = {
            'p_alojamiento': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'p_transporte': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'p_comida': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'p_otros': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
        }

    def total(self):
        return sum([
            self.cleaned_data.get('p_alojamiento', 0),
            self.cleaned_data.get('p_transporte', 0),
            self.cleaned_data.get('p_comida', 0),
            self.cleaned_data.get('p_otros', 0),
        ])