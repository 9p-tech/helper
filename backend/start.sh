#!/bin/bash
# One-time setup + start script for Snitch backend

set -e

echo "=== Snitch Backend Setup ==="

# 1. Create & activate venv
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created."
fi
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run migrations
python manage.py migrate

# 4. Seed sample data
python manage.py seed_data

# 5. Create superuser if not exists
echo "from apps.accounts.models import User; User.objects.filter(email='admin@snitch.in').exists() or User.objects.create_superuser('admin', 'admin@snitch.in', 'admin123')" | python manage.py shell

echo ""
echo "=== Starting server on http://127.0.0.1:8000 ==="
echo "Admin panel: http://127.0.0.1:8000/django-admin/"
echo "Credentials: admin@snitch.in / admin123"
echo ""
python manage.py runserver
