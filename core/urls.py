"""
LMS Platform — Health Check URL
DigitalOcean App Platform üçün /health/ endpoint
"""
from django.urls import path
from django.http import JsonResponse


def health_check(request):
    """DigitalOcean health check endpoint."""
    return JsonResponse({'status': 'ok', 'service': 'lms-platform'})


urlpatterns = [
    path('', health_check),
]
