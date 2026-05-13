#!/usr/bin/env bash

echo "INSTALLING REQUIREMENTS"
pip install -r requirements.txt

echo "COLLECTING STATIC"
python manage.py collectstatic --noinput

echo "RUNNING MIGRATIONS"
python manage.py migrate --noinput

echo "CREATING SUPERUSER"
python manage.py createsuperuser --noinput || true

echo "BUILD COMPLETE"