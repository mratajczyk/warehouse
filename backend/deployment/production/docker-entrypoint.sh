#!/bin/sh

# Wait for database to be ready ex. when using docker-compose
while ! nc -z $CONFIG_DATABASE_HOST $CONFIG_DATABASE_PORT; do sleep 1; done;

set -e

if [ -z "$SKIP_MIGRATIONS"]
then
  poetry run alembic upgrade head
fi

exec poetry run gunicorn -c /app/gunicorn-config.py --access-logfile - "api.application:create_application()"