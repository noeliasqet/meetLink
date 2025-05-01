from django import forms
from .models import Usuario, Contacto, Evento
from django.contrib.auth.forms import UserCreationForm

class UsuarioCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'nombre', 'apellidos', 'email', 'password1', 'password2']

class ContactoCreationForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = '__all__'

class EventoCreationForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = '__all__'
