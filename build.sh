#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Apply migrations
python manage.py migrate users

python manage.py migrate

# Start the application
gunicorn core.wsgi:application --bind 0.0.0.0:$PORT
