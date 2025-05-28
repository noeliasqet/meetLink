from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator



##################! USUARIO !#################
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




##################! CONTACTOS !#################
class Contacto(models.Model):
    nombre = models.CharField(max_length=20, verbose_name="Nombre")
    mail = models.EmailField(verbose_name="Email")
    telefono = models.CharField(
        max_length=9,
        validators=[RegexValidator(regex=r'^\d{9}$', message='El número debe tener 9 dígitos.')],
        verbose_name="Teléfono"
    )
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name='Usuario')

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Contacto"
        verbose_name_plural = "Contactos"
        unique_together = ('usuario', 'mail')

class GrupoContacto(models.Model):
    nombre = models.CharField(max_length=20, verbose_name="Nombre del grupo")
    descripcion = models.CharField(max_length=40, verbose_name="Descripción del grupo")
    integrantes = models.ManyToManyField('Contacto', blank=True, verbose_name="Integrantes")
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name="Usuario")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Grupo de contacto"
        verbose_name_plural = "Grupos de contacto"



##################! EVENTOS !#################
class Evento(models.Model):
    nombre = models.CharField(max_length=25, verbose_name="Nombre")
    descripcion = models.CharField(max_length=50, verbose_name="Descripción")
    ubicacion = models.CharField(max_length=50, default="Por definir", verbose_name="Ubicación")
    fecha_inicio = models.DateTimeField(verbose_name="Fecha de inicio")
    fecha_fin = models.DateTimeField(verbose_name="Fecha de fin")
    transporte = models.CharField(max_length=20, verbose_name="Medio de transporte")
    presupuesto = models.BooleanField(default=False, verbose_name="Presupuesto")
    grupo = models.ForeignKey('GrupoContacto', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Grupo de Contacto")
    maleta = models.BooleanField(default=False, verbose_name="Maleta")
    todo = models.BooleanField(default=False, verbose_name="To Do")
    p_alojamiento = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    p_transporte = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    p_comida = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    p_otros = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name='Usuario')

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"

# class Asistencia(models.Model):
#     evento = models.ForeignKey(Evento, on_delete=models.CASCADE, verbose_name="Evento")
#     asistente = models.ForeignKey(Contacto, on_delete=models.CASCADE, verbose_name="Asistente")
#     asistencia = models.BooleanField(default=False, verbose_name="Asistencia confirmada")

#     def __str__(self):
#         return f"{self.asistente.nombre} - {self.evento.nombre}"

#     class Meta:
#         verbose_name = "Asistencia"
#         verbose_name_plural = "Asistencias"
