from django.core.mail import send_mail
from proyectoFinal.settings.base import DEFAULT_FROM_EMAIL
from urllib.parse import urlencode

def generar_link_google_calendar(evento):
    base_url = "https://calendar.google.com/calendar/render?"
    params = {
        'action': 'TEMPLATE',
        'text': evento.nombre,
        'dates': f"{evento.fecha_inicio.strftime('%Y%m%dT%H%M%S')}/{evento.fecha_fin.strftime('%Y%m%dT%H%M%S')}",
        'details': evento.descripcion,
        'location': evento.ubicacion or "",
        'add': ','.join(evento.grupo.integrantes.values_list('mail', flat=True)) if evento.grupo else "",
    }
    return base_url + urlencode(params)


def enviar_mail_evento(evento, emails):
    asunto = f"Nuevo evento: {evento.nombre}"
    enlace_calendar = generar_link_google_calendar(evento)

    mensaje = f"""
Hola 🤗​,

Has sido invitado al evento "{evento.nombre}". Aquí te dejo los detalles:

• Ubicación: {evento.ubicacion or 'No especificada'}
• Fecha y hora de inicio: {evento.fecha_inicio.strftime('%Y-%m-%d %H:%M')}
• Fecha y hora de fin: {evento.fecha_fin.strftime('%Y-%m-%d %H:%M')}
• Descripción: {evento.descripcion or 'Sin descripción'}

➕ Añádelo a tu Google Calendar:
{enlace_calendar}

🔥​ ¡No olvides confirmarme tu asistencia!

Saludos,  
Equipo de MeetLink
"""
    send_mail(asunto, mensaje, DEFAULT_FROM_EMAIL, emails, fail_silently=False)
