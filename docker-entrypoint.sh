#!/bin/bash

echo "Waiting for postgres..."

while ! nc -z db 5432; do
  sleep 0.1
done

echo "PostgresSQL started"

# be careful the below command will remove everything from the database run rebuild container every time
# python manage.py flush --no-input 
python manage.py migrate
python3 manage.py populate_data --industry industry.txt --country country.txt --skills skills.txt --currency currency.txt

exec "$@"
