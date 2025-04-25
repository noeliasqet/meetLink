from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

##################! INDEX - USUARIO !#################

class Usuario(AbstractUser):
    username = models.CharField(max_length=25, verbose_name="Username", unique=True)
    nombre = models.CharField(max_length=50, verbose_name="Nombre") 
    apellidos = models.CharField(max_length=100, verbose_name="Apellidos")
    email = models.EmailField(unique=True, verbose_name="Email")
    avatar = models.ImageField(upload_to="media/avatar/", blank=True, null=True, verbose_name="Foto de Perfil")
    fecha_registro = models.DateField(auto_now_add=True, verbose_name="Fecha de Registro")

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        
        
