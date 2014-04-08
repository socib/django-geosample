"""Settings for Development Server"""
from geosample.settings.base import *   # pylint: disable=W0614,W0401

DEBUG = True
TEMPLATE_DEBUG = DEBUG

VAR_ROOT = '/var/www/geosample'
MEDIA_ROOT = os.path.join(VAR_ROOT, 'uploads')
STATIC_ROOT = os.path.join(VAR_ROOT, 'static')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'geosample',
#        'USER': 'dbuser',
#        'PASSWORD': 'dbpassword',
    }
}

# WSGI_APPLICATION = 'geosample.wsgi.dev.application'
