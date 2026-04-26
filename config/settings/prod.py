from .base import *

DEBUG = False

DATABASES = {
    'default': env.db('DATABASE_URL')   # postgres://user:pass@host/db
}

SECURE_HSTS_SECONDS = 31536000
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True