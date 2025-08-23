#!/bin/sh
set -e

# Wait for the database to be ready
if [ "$DB_HOST" != "" ]; then
  echo "Waiting for database at $DB_HOST:$DB_PORT..."
  while ! nc -z $DB_HOST $DB_PORT; do
    sleep 1
  done
fi

echo "Database is ready!"

# Run migrations
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Start Django development server
exec python manage.py runserver 0.0.0.0:8000
