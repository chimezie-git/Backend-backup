#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

python manage.py makemigrations
python manage.py migrate

gunicorn core.wsgi:application --bind 0.0.0.0:$PORT
