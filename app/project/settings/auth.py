# -*- coding: utf-8 -*-

# AUTHENTICATION_BACKENDS = (
#     'django.contrib.auth.backends.ModelBackend', # default
# )

# SESSION_ENGINE = 'redis_sessions.session'
# ACCOUNT_BACKEND = "profiles.backends.EmailOrModelBackend"
# AUTH_USER_MODEL = "profiles.Profile"
# LOGIN_URL = '/profiles/login/'


# ACCOUNT_OPEN_SIGNUP = True
# ACCOUNT_EMAIL_UNIQUE = True
# ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = True
# ACCOUNT_LOGIN_REDIRECT_URL = "home"
# ACCOUNT_LOGOUT_REDIRECT_URL = "home"
# ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 2
# ACCOUNT_USER_DISPLAY = lambda user: "%s %s" % (user.first_name, user.last_name) if user.first_name and user.last_name \
#     else user.email