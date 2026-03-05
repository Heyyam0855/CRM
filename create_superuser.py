"""Superuser yaratmaq üçün köməkçi skript."""
import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.local'
django.setup()

from apps.users.models import User

email = 'admin@lms.az'
password = 'Admin1234!'

if not User.objects.filter(email=email).exists():
    User.objects.create_superuser(
        email=email,
        password=password,
        first_name='Admin',
        last_name='LMS'
    )
    print(f'✅ Superuser yaradildi: {email} / {password}')
else:
    print(f'ℹ️  Superuser artiq movcuddur: {email}')
