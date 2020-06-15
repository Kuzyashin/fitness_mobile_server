"""
Django settings for project project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
from django.utils.translation import ugettext_lazy as _


# folder with main django project which contains settings, urls and applications package
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

# base repo folder, here stored virtualenv files, manage.py etc
BASE_DIR = os.path.abspath(os.path.join(PROJECT_ROOT, os.pardir))

LOGS_ROOT = os.path.join(BASE_DIR, "logs")

# folder with collected static files, ready to download by client apps
PUBLIC_ROOT = os.path.join(BASE_DIR, "public")

sys.path.append(os.path.join(PROJECT_ROOT, 'applications'))


ROOT_URLCONF = 'project.urls'

WSGI_APPLICATION = 'project.wsgi.application'
ASGI_APPLICATION = 'project.routing.application'

REDIS_HOST = os.environ['REDIS_HOST']


CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [f"redis://{REDIS_HOST}:6379/2"],
            "capacity": 1500,
        },
    },
}

#USE_X_FORWARDED_HOST = True
#SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SWAGGER_SETTINGS = {
    'DEFAULT_API_URL': 'https://backend.mobile.fitnesskit.awkr.site/'
}

REDOC_SETTINGS = {
   'DEFAULT_API_URL': 'https://backend.mobile.fitnesskit.awkr.site/'
}