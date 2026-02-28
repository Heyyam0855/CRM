"""LMS Platform — Celery Konfiqurasiyası"""
import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

app = Celery('lms')

# Django settings-dən celery konfiqurasiyasını oxu
app.config_from_object('django.conf:settings', namespace='CELERY')

# Bütün registered tasks-ları avtomatik aş
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self) -> None:
    """Debug task — Celery işlədiyini yoxlamaq üçün."""
    print(f'Request: {self.request!r}')
