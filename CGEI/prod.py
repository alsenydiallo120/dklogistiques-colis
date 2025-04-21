from .settings import *
from urllib.parse import urlparse
import os
DEBUG = False

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    url = urlparse(DATABASE_URL)
    DATABASES = {
        'default': {
            'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.mysql'),
            'NAME': url.path[1:],
            'USER': url.username,
            'PASSWORD': url.password,
            'HOST': url.hostname,
            'PORT': url.port or '3306',
        }
    }

