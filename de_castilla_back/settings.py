"""
Django settings for de_castilla_back project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path
from datetime import timedelta
import dj_database_url


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-eq6p5-!fynf4+p#q5z$g(!jibp5ng_ky)v-hg67s6oacppm_w='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['de-castilla-back.onrender.com','127.0.0.1','localhost']


# Application definition

BASE_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

LOCAL_APPS = [
    'apps.calificacion',
    'apps.categoria',
    'apps.detalle_oc',
    'apps.detalle_pedido',
    'apps.detalle_venta',
    'apps.estado_oc',
    'apps.estado_pedido',
    'apps.historico',
    'apps.insumo',
    'apps.inventario',
    'apps.orden_compra',
    'apps.pedido',
    'apps.producto',
    'apps.proveedor',
    'apps.rol',
    'apps.sabor',
    'apps.sabor_has_producto',
    'apps.tipo_movimiento',
    'apps.usuarios',
    'apps.venta',
]


THIRD_APPS = [
    'corsheaders',
    'rest_framework',
    'drf_yasg',
    'django_rest_passwordreset',
]

INSTALLED_APPS = BASE_APPS + LOCAL_APPS + THIRD_APPS


REST_FRAMEWORK = {
    
    'DEFAULT_AUTHENTICATION_CLASSES': (
        
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
    
}


SIMPLE_JWT = {
    'USER_ID_FIELD': 'no_documento_usuario',
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=2),
    # otras configuraciones de SIMPLE_JWT
}



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# O para permitir origenes específicos:
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://de-castilla-front.vercel.app"
]

ROOT_URLCONF = 'de_castilla_back.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'de_castilla_back.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME':  'db_de_castilla',
#         'PASSWORD': '123456',
#         'USER': 'root',
#         'HOST': '127.0.0.1',
#         'PORT': '3306',
#     }
# }

DATABASES = {
    'default': dj_database_url.config(
        default='mysql://root:123456@127.0.0.1:3306/db_de_castilla'
    )
}


AUTH_USER_MODEL = 'usuarios.Usuario'

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# STATIC_URL = 'static/'
STATIC_URL = '/static/'
STATIC_ROOT = './static/'

if not DEBUG:
    # Tell Django to copy static assets into a path called `staticfiles` (this is specific to Render)
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    # Enable the WhiteNoise storage backend, which compresses static files to reduce disk use
    # and renames the files with unique names for each version to support long-term caching
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuración del servidor de correo saliente (SMTP)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.example.com'  # Dirección del servidor SMTP
EMAIL_PORT = 587  # Puerto del servidor SMTP (usualmente 587 para TLS)
EMAIL_USE_TLS = True  # Usar TLS (si es necesario)
EMAIL_HOST_USER = 'ariasruizcamilaa@gmail.com'
EMAIL_HOST_PASSWORD = ''  # Contraseña del servidor SMTP

# Otras opciones
DEFAULT_FROM_EMAIL = 'noreply@example.com'  # Dirección de correo electrónico


# Configuración de las imágenes
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
