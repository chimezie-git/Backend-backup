import os
from dotenv import load_dotenv
from .common import *

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = []

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

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"