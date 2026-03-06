"""Superuser yaratmaq üçün köməkçi skript."""
import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.development'
django.setup()

from apps.users.models import User

email = 'xeyyamsirinov07@gmail.com'
password = 'Admin1234'

if not User.objects.filter(email=email).exists():
    User.objects.create_superuser(
        email=email,
        password=password,
        first_name='Xeyyam',
        last_name='Sirinov'
    )
    print(f'Superuser yaradildi: {email} / {password}')
else:
    u = User.objects.get(email=email)
    u.set_password(password)
    u.is_superuser = True
    u.is_staff = True
    u.save()
    print(f'Yenilendi: {email} / {password}')
