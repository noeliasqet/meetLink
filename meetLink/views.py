from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .forms import UsuarioCreationForm, ContactoCreationForm, ContactoUpdateForm, GrupoContactoCreationForm, GrupoContactoUpdateForm, EventoCreationForm, EventoUpdateForm
from .models import Contacto, GrupoContacto, Evento



############################! INDEX !###########################
class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'meetLink/inicio/index.html'
    login_url = '/sesion/login/'

    def get_context_data(self, **otros):
        contexto = super().get_context_data(**otros)
        usuario = self.request.user
        contexto['usuario'] = usuario
        return contexto
    
  
############################! SESIÓN !###########################
  
User = get_user_model() 
    
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'nombre', 'apellidos', 'email', 'password1', 'password2']

class RegistroView(CreateView):
    form_class = UsuarioCreationForm
    template_name = 'meetLink/sesion/registration.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        usuario = form.cleaned_data.get("username")

        if User.objects.filter(username=usuario).exists():
            messages.error(self.request, "El nombre de usuario ya está en uso. Por favor, elige otro.")
            return render(self.request, self.template_name, {"form": form}) # Return al form CON ERROR

        return super().form_valid(form)
    
class CustomLoginView(LoginView):
    template_name = 'meetLink/sesion/login.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Bienvenido de nuevo a MeetL!nk :)')
        return super().form_valid(form)

class CustomLogoutView(LogoutView):
    template_name = 'meetLink/sesion/logout.html'

    def get_next_page(self):
        return reverse_lazy('login')
    
    
    
############################! CONTACTOS !###########################

class ContactosView(LoginRequiredMixin, TemplateView):
    template_name = 'meetLink/contactos/contactos.html'
    login_url = 'meetLink/sesion/login/'
    
    def get_context_data(self, **otros):
        return super().get_context_data(**otros)
        usuario = self.request.user
        contexto['usuario'] = usuario
        return contexto
    
class ContactosCreateView(LoginRequiredMixin, CreateView):
    model = Contacto
    form_class = ContactoCreationForm
    template_name = 'meetLink/contactos/contactos_create.html'
    success_url = reverse_lazy('contactos')

    def form_valid(self, form):
        # Asignamos el usuario logueado al contacto
        form.instance.usuario = self.request.user

        # Validación opcional: evitar contactos duplicados por email en el mismo usuario
        if Contacto.objects.filter(usuario=self.request.user, mail=form.cleaned_data['mail']).exists():
            messages.error(self.request, "Ya tienes un contacto con ese email.")
            return render(self.request, self.template_name, {"form": form})

        return super().form_valid(form)

class ContactosUpdateView(LoginRequiredMixin, UpdateView):
    model = Contacto
    form_class = ContactoUpdateForm
    template_name = 'meetLink/contactos/contactos_update.html'
    success_url = reverse_lazy('contactos')

    def get_object(self, queryset=None):
        # Aseguramos que solo se pueda editar un contacto propio
        return get_object_or_404(Contacto, pk=self.kwargs['pk'], usuario=self.request.user)

    def form_valid(self, form):
        # Validación opcional: evitar duplicados por email (excluyendo el propio contacto)
        if Contacto.objects.filter(
            usuario=self.request.user,
            mail=form.cleaned_data['mail']
        ).exclude(pk=self.object.pk).exists():
            messages.error(self.request, "Ya tienes un contacto con ese email.")
            return self.form_invalid(form)
        
        return super().form_valid(form)
    
class ContactosDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'meetLink/contactos/contactos_delete.html'
    


############################! GRUPOS CONTACTO !###########################
class GrupoContactoCreateView(LoginRequiredMixin, CreateView):
    model = GrupoContacto
    form_class = GrupoContactoCreationForm
    template_name = 'meetLink/contactos/grupo_create.html'
    success_url = reverse_lazy('contactos')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user          # pasamos el usuario al formulario
        return kwargs
    
    def form_valid(self, form):
        form.instance.usuario = self.request.user   # asignar el usuario que crea el grupo
        return super().form_valid(form)

class GrupoContactoUpdateView(LoginRequiredMixin, UpdateView):
    model = GrupoContacto
    form_class = GrupoContactoUpdateForm
    template_name = 'meetLink/contactos/grupo_update.html'
    success_url = reverse_lazy('contactos')

    def get_object(self, queryset=None):
        return get_object_or_404(GrupoContacto, pk=self.kwargs['pk'], usuario=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, "Grupo de contacto actualizado correctamente.")
        return super().form_valid(form)
    
    

############################! EVENTOS !###########################

class EventosView(LoginRequiredMixin, TemplateView):
    template_name = 'meetLink/eventos/eventos.html'
    
    
    
class EventosCreateView(LoginRequiredMixin, CreateView):
    model = Evento
    form_class = EventoCreationForm
    template_name = 'meetLink/eventos/eventos_create.html'
    success_url = reverse_lazy('eventos')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)
    
    
class EventosDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'meetLink/eventos/eventos_delete.html'
    

class EventosUpdateView(LoginRequiredMixin, UpdateView):
    model = Evento
    form_class = EventoUpdateForm
    template_name = 'meetLink/eventos/eventos_update.html'
    success_url = reverse_lazy('eventos')

    def get_object(self, queryset=None):
        return get_object_or_404(Evento, pk=self.kwargs['pk'], usuario=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, "Grupo de contacto actualizado correctamente.")
        return super().form_valid(form)
    
    
    