# -*- coding: utf-8 -*-

##################################################################
# TEMPLATE OF LOCAL SETTINGS FILE
# Real file with local settings should have a name:
# local.py
##################################################################

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test',
    }
}

SECRET_KEY = 'huBlW0v-HHC1fpo931HBFhAsBQMGrNO9'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'xxx@gmail.com'
EMAIL_HOST_PASSWORD = ''