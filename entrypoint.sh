#!/bin/sh

echo "Aplicando migraciones..."
python manage.py migrate --noinput

echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "Iniciando Gunicorn..."
gunicorn Back.wsgi:application \
    --bind 0.0.0.0:8001 \
    --workers 4 \
    --threads 2 \
    --timeout 120
