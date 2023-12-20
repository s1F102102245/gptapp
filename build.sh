#!/usr/bin/env bash
# exit on error
set -o errexit
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
#python manage.py createsuperuser --noinput

poetry run gunicorn gptapp.wsgi:application --bind 0.0.0.0:8000