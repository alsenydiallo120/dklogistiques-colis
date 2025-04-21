from .settings import *
import os
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.mysql'),
        'NAME': os.getenv('DB_NAME','dkl_colis'),
        'USER': os.getenv('DB_USER', 'root'),
        'PASSWORD': os.getenv('DB_PASSWORD','root'),
    }
}