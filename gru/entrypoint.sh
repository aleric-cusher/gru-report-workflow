#!/bin/bash

echo "Running Migrations"
python manage.py makemigrations
python manage.py migrate


exec "$@"
