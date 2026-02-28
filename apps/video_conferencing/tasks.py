"""Video Conferencing — Celery Tasks"""
from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=30, queue='default')
def create_meet_link_task(self, booking_id: str) -> dict:
    """
    Booking üçün Google Meet linki yaradır.

    Args:
        booking_id: Booking UUID-si

    Returns:
        dict: meet_link əks halda xəta
    """
    try:
        from apps.bookings.models import Booking
        from .services import GoogleMeetService

        booking = Booking.objects.select_related('student').get(id=booking_id)

        if booking.meet_link:
            return {'success': True, 'link': booking.meet_link, 'skipped': True}

        service = GoogleMeetService()
        meet_link = service.create_meeting(
            topic=f"LMS Dərs: {booking.topic or 'Dərs'}",
            start_time=booking.slot.start_time,
            attendee_email=booking.student.email
        )

        if meet_link:
            booking.meet_link = meet_link
            booking.save(update_fields=['meet_link'])
            logger.info(f"Meet link yaradıldı: booking={booking_id}")
            return {'success': True, 'link': meet_link}
        else:
            return {'success': False, 'error': 'Meet link alına bilmədi'}

    except Exception as exc:
        logger.error(f"Meet link task xətası: {exc}", exc_info=True)
        raise self.retry(exc=exc)
