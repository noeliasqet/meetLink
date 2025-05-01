from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .forms import UsuarioCreationForm


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
    template_name = 'meetLink/contactos/contactos_create.html'
    
    
class ContactosDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'meetLink/contactos/contactos_delete.html'
    

class ContactosUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'meetLink/contactos/contactos_update.html'
    
    

############################! EVENTOS !###########################

class EventosView(LoginRequiredMixin, TemplateView):
    template_name = 'meetLink/eventos/eventos.html'
    
class EventosCreateView(LoginRequiredMixin, CreateView):
    template_name = 'meetLink/eventos/eventos_create.html'
    
class EventosDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'meetLink/eventos/eventos_delete.html'
    
    
class EventosUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'meetLink/eventos/eventos_update.html'
    
    
    