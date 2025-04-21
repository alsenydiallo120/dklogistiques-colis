import os
from pathlib import Path
from decouple import config
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv('SECRET_KEY','your-secret-key')
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")
env = os.getenv("DJANGO_ENV", "dev")

if env=="dev":
    from .dev import *
elif env=="prod":
    from .prod import *


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'crispy_bootstrap5',
    'active_link',
    'django.contrib.humanize',
    'mathfilters',
    'base_commandes',
    'accounts',
    'entreprise',
    'typecomptes',
    'agences',
    'pays',
    'transporteurs',
    'tauxs',
    'expeditaires',
    'destinataires',
    'colis',
    'lots',
    'qr_code',
    'embarquements',
    'depenses',
    'API',
    'rest_framework',
    'depots',
    'reglements',
    'clients',
    "conteneurs",
    "annees",
    "regulations",
    "decaissements",
    "depensevols",
    "rendezvous",
    "regulationbateaus",
    "clientsrendezvous",
    "chauffeurs",
    "debug_toolbar",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'my_middleware.middleware.TauxMiddlware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'CGEI.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], 
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



# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "formatters": {
#         "verbose": {
#             "format": "{levelname} [{asctime}] module:[{module}] line:{lineno} {message}",
#             "style": "{",
#         },
#         "simple": {
#             "format": "{levelname} {message}",
#             "style": "{",
#         },
#     },
#     "handlers": {
#         "console": {
#             "class": "logging.StreamHandler",
#             "formatter": "verbose",
#         },
#         "file": {
#             "class": "logging.FileHandler",
#             "formatter": "verbose",
#             "filename": os.path.join(os.path.dirname(__file__), 'logs', 'app.log'),
#         },
#     },
#     "root": {
#         "handlers": ["console", "file"], 
#         "level": "INFO",
#     },
# }


WSGI_APPLICATION = 'CGEI.wsgi.application'

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR/ 'media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL='accounts.CustomUser'
LOGOUT_REDIRECT_URL = "login"
LOGIN_REDIRECT_URL = "home"
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' 
EMAIL_HOST = 'mail.cediguinee.org' 
EMAIL_USE_TLS = True 
EMAIL_PORT = 587 
EMAIL_HOST_USER = 'testmail@cediguinee.org	' 
EMAIL_HOST_PASSWORD = '4rEpqsL}UsAx'

INTERNAL_IPS = ["127.0.0.1",]

LINK="https://colis.dklogistique.com"

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
