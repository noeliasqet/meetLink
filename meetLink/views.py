from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class IndexView(TemplateView):
    template_name = 'meetLink/inicio/index.html'
    login_url = '/accounts/login/'

    def get_context_data(self, **otros):
        contexto = super().get_context_data(**otros)
        usuario = self.request.user
        contexto['usuario'] = usuario
        return contexto