#!/usr/bin/env bash
# Script de build para Render: se ejecuta en cada despliegue
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
# Red de seguridad: si faltara alguna migración, se genera antes de migrar
python manage.py makemigrations --no-input
python manage.py migrate --no-input
python manage.py setup_roles
python manage.py cargar_demo
python manage.py createsuperuser --noinput || true