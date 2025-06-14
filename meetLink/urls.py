from django.urls import path
from . import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #! INDEX !#
    path('', IndexView.as_view(), name='index'),
    
    #! SESIÓN !#
    path('sesion/registro/', RegistroView.as_view(), name="registro"),
    path('sesion/login/', CustomLoginView.as_view(), name='login'),
    path('sesion/logout/', CustomLogoutView.as_view(), name='logout'),
    
    #! CONTACTOS !#
    path('contactos/', ContactosView.as_view(), name='contactos'),
    path('contactos/create', ContactosCreateView.as_view(), name='contactos_create'),
    path('contactos/update/<int:pk>', ContactosUpdateView.as_view(), name='contacto_update'),
    path('contactos/delete/<int:pk>', ContactosDeleteView.as_view(), name='contacto_delete'),
    

    #! GRUPOS DE CONTACTO !#
    path('grupo/create', GrupoContactoCreateView.as_view(), name='grupo_create'),
    path('grupo/update/<int:pk>', GrupoContactoUpdateView.as_view(), name='grupo_update'),
    path('grupo/delete/<int:pk>', GrupoContactosDeleteView.as_view(), name='grupo_delete'),
    
    
    #! EVENTOS !#
    path('eventos/', EventosView.as_view(), name='eventos'),
    path('eventos/create', EventosCreateView.as_view(), name='eventos_create'),
    path('eventos/update/<int:pk>', EventosUpdateView.as_view(), name='eventos_update'),
    path('eventos/delete/<int:pk>', EventosDeleteView.as_view(), name='eventos_delete'),
    path('eventos/<int:pk>/presupuesto/', EventoPresupuestoView.as_view(), name='evento_presupuesto'),
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)