#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

echo "from django.contrib.auth import get_user_model;
User=get_user_model();
u,created=User.objects.get_or_create(username='samihi');
u.is_staff=True;
u.is_superuser=True;
u.set_password('123456789');
u.save()" | python manage.py shell