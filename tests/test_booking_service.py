"""
LMS Platform — BookingService Tests
"""
import pytest
from apps.bookings.services import BookingService
from apps.bookings.models import Booking


@pytest.mark.django_db
class TestBookingService:
    """BookingService üçün testlər."""

    def setup_method(self):
        self.service = BookingService()

    def test_create_booking_success(self, student_user, available_slot):
        """Uğurlu rezervasiya yaratma."""
        booking = self.service.create_booking(
            student_id=str(student_user.id),
            slot_id=str(available_slot.id),
            lesson_type='standard',
            topic='Python Əsasları'
        )

        assert booking is not None
        assert booking.status == Booking.Status.CONFIRMED
        assert booking.student == student_user
        assert booking.topic == 'Python Əsasları'

    def test_create_booking_reserved_slot(self, student_user, reserved_slot):
        """Rezerv edilmiş slot üçün booking yaratma uğursuz olmalıdır."""
        booking = self.service.create_booking(
            student_id=str(student_user.id),
            slot_id=str(reserved_slot.id),
            lesson_type='standard'
        )
        assert booking is None

    def test_create_booking_past_slot(self, student_user, past_slot):
        """Keçmiş slot üçün booking yaratma uğursuz olmalıdır."""
        booking = self.service.create_booking(
            student_id=str(student_user.id),
            slot_id=str(past_slot.id),
            lesson_type='standard'
        )
        assert booking is None

    def test_cancel_booking_success(self, student_user, available_slot):
        """Uğurlu booking ləğvi."""
        booking = self.service.create_booking(
            student_id=str(student_user.id),
            slot_id=str(available_slot.id),
            lesson_type='standard'
        )
        assert booking is not None

        cancelled = self.service.cancel_booking(
            booking_id=str(booking.id),
            reason='Test ləğvi'
        )
        assert cancelled is True

        booking.refresh_from_db()
        assert booking.status == Booking.Status.CANCELLED
