"""Bookings App — Celery Tasks"""
from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=300,
    queue='notifications'
)
def send_lesson_reminder_task(self, booking_id: str, hours_before: int) -> dict:
    """
    Dərs xatırlatması göndərir.

    Args:
        booking_id: Booking UUID-si
        hours_before: Neçə saat əvvəl xatırlatma (24 və ya 1)

    Returns:
        dict: Nəticə məlumatı
    """
    try:
        from .models import Booking
        booking = Booking.objects.select_related('student', 'slot').get(id=booking_id)

        if booking.status != Booking.Status.CONFIRMED:
            return {'success': False, 'reason': 'Booking artıq aktiv deyil'}

        from apps.notifications.services import NotificationService
        ns = NotificationService()
        ns.send_lesson_reminder(booking, hours_before)

        logger.info(f"Xatırlatma göndərildi: booking={booking_id}, saat={hours_before}")
        return {'success': True, 'booking_id': booking_id}

    except Exception as exc:
        logger.error(f"Xatırlatma xətası: {exc}", exc_info=True)
        raise self.retry(exc=exc)
