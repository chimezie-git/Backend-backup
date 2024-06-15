import os
from dotenv import load_dotenv
from .common import *
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "localhost", "example.com"]

# DATABASES = {
#     'default': dj_database_url.config(
#         default= os.getenv("EX_DB_URL"),
#         conn_max_age=600
#     )
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "smtp.hostinger.com"
    EMAIL_HOST_USER = "info@nitrobills.com"
    EMAIL_HOST_PASSWORD = os.getenv("EMAIL_PASSWORD")
    EMAIL_PORT = 465
    EMAIL_USE_SSL = True
    # static config
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
