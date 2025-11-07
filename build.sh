#!/usr/bin/env bash
# build.sh

# Exit on error
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Collect static files (CSS, JavaScript, images)
python manage.py collectstatic --no-input

# Run database migrations
python manage.py migrate