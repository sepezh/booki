#!/bin/bash

# Production build script for Django application

# Exit on any error
set -e

echo "Starting production build..."

# Install dependencies
echo "Installing requirements..."
pip install -r requirements.txt

# Set production environment variables
export DEBUG=False
export SECRET_KEY=${SECRET_KEY:-'your-production-secret-key-here'}
export DATABASE_URL=${DATABASE_URL:-'sqlite:///db.sqlite3'}

# Run database migrations
echo "Running database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if environment variables are set
if [ "$CREATE_USER" = "true" ] && [ -n "$SUPERUSER_USERNAME" ] && [ -n "$SUPERUSER_PASSWORD" ]; then
    echo "Creating superuser..."
    export DJANGO_SUPERUSER_USERNAME=$SUPERUSER_USERNAME
    export DJANGO_SUPERUSER_PASSWORD=$SUPERUSER_PASSWORD
    export DJANGO_SUPERUSER_EMAIL=${SUPERUSER_EMAIL:-'admin@example.com'}
    python manage.py createsuperuser --noinput
else
    echo "Superuser environment variables not set. Skipping superuser creation."
fi

echo "Production build completed successfully."