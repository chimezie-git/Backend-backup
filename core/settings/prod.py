import os
import dj_database_url
from .common import *

SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = False

ALLOWED_HOSTS = [".onrender.com",
                 '127.0.0.1',
    'localhost',  # Optional, but recommended
                 ]

CSRF_TRUSTED_ORIGINS = ["https://nitrobills-backend-backup.onrender.com",]

# DATABASES = {
#     'default': dj_database_url.config(
#         # default= os.getenv("POSTGRESS_DATABASE_URL"),
#         default= "postgresql://nitrobills_postgre_user:900e8zPvhntNkBIkYII01pBq17KyO2JP@dpg-cuq5ka23esus738kjepg-a.oregon-postgres.render.com/nitrobills_postgre",
#         conn_max_age=600
#     )
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# DATABASES = {
#     'default': dj_database_url.config(
#         default="postgresql://nitrobills_postgre_user:900e8zPvhntNkBIkYII01pBq17KyO2JP@dpg-cuq5ka23esus738kjepg-a.oregon-postgres.render.com/nitrobills_postgre",
#         conn_max_age=600,
#     )
# }

# DATABASES = {
#     'default': dj_database_url.config(conn_max_age=600)
# }



EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.hostinger.com"
EMAIL_HOST_USER = os.getenv("EMAIL")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_PORT = 465
EMAIL_USE_SSL = True


STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
