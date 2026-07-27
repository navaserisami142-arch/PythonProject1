#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate

python manage.py shell <<EOF
from django.contrib.auth import get_user_model

User = get_user_model()

username = "samihi"
email = "admin@example.com"
password = "123456789"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
EOF