#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
poetry install --no-root

# Apply any outstanding database migrations
python manage.py migrate