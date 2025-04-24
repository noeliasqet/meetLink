from .base import *
from decouple import config

DEBUG = False

# ALLOWED_HOSTS = ['localhost', 'dominio_produccion']

# DATABASES = {
#     'default': {
#         'ENGINE': 'mysql.connector.django',              # Motor para MySQL
#         'NAME': config('DB_NAME'),                       # Nombre de la base de datos
#         'USER': config('DB_USER'),                       # Usuario de la base de datos
#         'PASSWORD': config('DB_PASSWORD'),               # Contraseña del usuario
#         'HOST': config('DB_HOST', default='localhost'),  # Dirección del servidor
#         'PORT': config('DB_PORT', default='3306'),       # Puerto de la base de datos
#         'OPTIONS': {
#             'autocommit': True,
#         },
#     }
# }


# SECURE_SSL_REDIRECT = True
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True

# Configuración del backend de correo para producción
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_HOST = config('EMAIL_HOST')
# EMAIL_PORT = config('EMAIL_PORT')
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = config('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')