"""
Conftest — pytest fixtures tüm testlər üçün.
"""
import pytest
from django.utils import timezone
from datetime import timedelta


@pytest.fixture
def teacher_user(db):
    """Müəllim istifadəçisi."""
    from apps.users.models import User
    return User.objects.create_user(
        email='teacher@lms.az',
        password='testpass123',
        first_name='Müəllim',
        last_name='Test',
        role='teacher',
        is_active=True
    )


@pytest.fixture
def student_user(db):
    """Tələbə istifadəçisi."""
    from apps.users.models import User
    user = User.objects.create_user(
        email='student@lms.az',
        password='testpass123',
        first_name='Tələbə',
        last_name='Test',
        role='student',
        is_active=True
    )
    return user


@pytest.fixture
def available_slot(db):
    """Mövcud AvailabilitySlot."""
    from apps.bookings.models import AvailabilitySlot
    start = timezone.now() + timedelta(days=1)
    return AvailabilitySlot.objects.create(
        start_time=start,
        end_time=start + timedelta(hours=1),
        is_reserved=False,
        is_active=True
    )


@pytest.fixture
def reserved_slot(db):
    """Artıq rezerv edilmiş slot."""
    from apps.bookings.models import AvailabilitySlot
    start = timezone.now() + timedelta(days=2)
    return AvailabilitySlot.objects.create(
        start_time=start,
        end_time=start + timedelta(hours=1),
        is_reserved=True,
        is_active=True
    )


@pytest.fixture
def past_slot(db):
    """Keçmiş vaxt slotu."""
    from apps.bookings.models import AvailabilitySlot
    start = timezone.now() - timedelta(days=1)
    return AvailabilitySlot.objects.create(
        start_time=start,
        end_time=start + timedelta(hours=1),
        is_reserved=False,
        is_active=True
    )
