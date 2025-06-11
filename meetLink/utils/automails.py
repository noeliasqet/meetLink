# utils/emails.py (crea este archivo si no existe)
from django.core.mail import send_mail
from proyectoFinal.settings.base import DEFAULT_FROM_EMAIL

def enviar_mail_evento(evento, emails):
    asunto = f"Nuevo evento: {evento.nombre}"
    mensaje = f"""
Hola 🤗​,

Has sido invitado al evento "{evento.nombre}". Aquí te dejo los detalles:

• Ubicación: {evento.ubicacion}
• Fecha y hora de inicio: {evento.fecha_inicio.strftime('%Y-%m-%d %H:%M')}
• Fecha y hora de fin: {evento.fecha_fin.strftime('%Y-%m-%d %H:%M')}
• Descripción: {evento.descripcion}

🔥​ ​¡No olvides confirmarme tu asistencia!

Saludos,
{evento.usuario.nombre}
"""
    send_mail(
        asunto,
        mensaje,
        DEFAULT_FROM_EMAIL,
        emails,
        fail_silently=False,
    )
