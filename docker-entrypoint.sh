#!/bin/bash

echo "Waiting for postgres..."

while ! nc -z db 5432; do
  sleep 0.1
done

echo "PostgresSQL started"

python manage.py flush --no-input
python manage.py migrate
python3 manage.py populate_data --industry industry.txt --country country.txt --skills skills.txt --currency currency.txt

exec "$@"