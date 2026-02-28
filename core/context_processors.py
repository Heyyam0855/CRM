"""
LMS Platform — Core Context Processors
Bütün template-lərə əlavə olunacaq global dəyişənlər
"""
from decimal import Decimal

from django.conf import settings


def lms_globals(request) -> dict:
    """Template-lərdə istifadə olunan LMS global dəyişənləri."""
    return {
        'LESSON_PRICE': getattr(settings, 'LESSON_PRICE', Decimal('25.00')),
        'APP_NAME': 'LMS Platform',
        'APP_VERSION': '1.0.0',
        'is_teacher': (
            request.user.is_authenticated
            and request.user.role == 'teacher'
        ),
        'is_student': (
            request.user.is_authenticated
            and request.user.role == 'student'
        ),
    }
