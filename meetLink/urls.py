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
    
    
    #! EVENTOS !#
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)