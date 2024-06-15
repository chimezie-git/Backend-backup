import os
import dj_database_url
from .common import *

SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = False

ALLOWED_HOSTS = ["nitrobills-backend.onrender.com",]

CSRF_TRUSTED_ORIGINS = ["https://nitrobills-backend.onrender.com",]

DATABASES = {
    'default': dj_database_url.config(
        default= os.getenv("POSTGRESS_DATABASE_URL"),
        conn_max_age=600
    )
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.hostinger.com"
EMAIL_HOST_USER = os.getenv("EMAIL")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_PORT = 465
EMAIL_USE_SSL = True


STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
