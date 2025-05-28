from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Contacto, GrupoContacto, Evento

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):   
    list_display = ('username', 'nombre', 'apellidos', 'email', 'avatar', 'fecha_registro')  #! Revisar por posible modificación en models
    search_fields = ('username', 'nombre', 'apellidos', 'email', 'fecha_registro')
    list_filter = ('nombre', 'fecha_registro')
    ordering = ('fecha_registro',)
    
    
@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'mail', 'telefono', 'usuario')
    search_fields = ('nombre', 'mail', 'telefono')
    list_filter = ('nombre',)
    ordering = ('nombre',)
    
    
@admin.register(GrupoContacto)
class GrupoContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'get_integrantes', 'usuario')
    search_fields = ('nombre', 'descripcion', 'usuario__username')
    list_filter = ('usuario',)
    ordering = ('nombre',)

    def get_integrantes(self, obj):
        return ", ".join([i.nombre for i in obj.integrantes.all()])
    get_integrantes.short_description = 'Integrantes'
    
    
    
@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'ubicacion', 'fecha_inicio', 'fecha_fin', 'transporte', 'presupuesto', 'grupo', 'maleta', 'todo', 'p_alojamiento', 'p_transporte', 'p_comida', 'p_otros')
    search_fields = ('nombre', 'descripcion', 'fecha_inicio')
    list_filter = ('nombre', 'descripcion', 'fecha_inicio')
    ordering = ('fecha_inicio',)
    
    def mostrar_asistentes(self, obj):
        return ", ".join([a.nombre for a in obj.asistentes.all()])
    mostrar_asistentes.short_description = "Asistentes"    
    

# @admin.register(Asistencia)
# class AsistenciaAdmin(admin.ModelAdmin):
#     list_display = ('get_evento', 'get_asistente', 'asistencia')
#     search_fields = ('evento__nombre', 'asistente__nombre')
#     list_filter = ('evento', 'asistencia')
#     ordering = ('evento',)

#     def get_evento(self, obj):
#         return obj.evento.nombre
#     get_evento.short_description = 'Evento'

#     def get_asistente(self, obj):
#         return obj.asistente.nombre
#     get_asistente.short_description = 'Asistente'