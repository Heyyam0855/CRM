"""Bookings App — Services"""
from typing import Optional
import logging

from django.db import transaction
from django.utils import timezone

from .models import AvailabilitySlot, Booking

logger = logging.getLogger(__name__)


class BookingService:
    """Dərs rezervasiyası business logic."""

    @transaction.atomic
    def create_booking(
        self,
        student_id: str,
        slot_id: str,
        lesson_type: str = 'standard',
        topic: str = '',
        notes: str = ''
    ) -> Optional[Booking]:
        """
        Yeni dərs rezervasiyası yaradır.

        Axın:
        1. Slot mövcudluğunu yoxla (select_for_update)
        2. Booking yarat
        3. Slotu rezerv et
        4. Google Meet linki al
        5. Xatırlatma task-ları planlaşdır
        6. Email bildirişi göndər

        Args:
            student_id: Tələbənin UUID-si
            slot_id: Slot UUID-si
            lesson_type: Dərs növü
            topic: Dərs mövzusu
            notes: Tələbə qeydləri

        Returns:
            Optional[Booking]: Yaradılmış booking
        """
        try:
            # Slot mövcudluğunu yoxla (race condition qaçınmaq üçün)
            slot = AvailabilitySlot.objects.select_for_update().get(
                id=slot_id,
                is_reserved=False,
                is_active=True,
                start_time__gt=timezone.now()
            )
        except AvailabilitySlot.DoesNotExist:
            logger.warning(f"Slot mövcud deyil: {slot_id}")
            return None

        try:
            from apps.users.models import User
            from django.conf import settings

            student = User.objects.get(id=student_id, role='student')
            price = getattr(settings, 'LESSON_PRICE', 25.00)

            # Sınaq dərsi üçün endirim
            if lesson_type == Booking.LessonType.TRIAL:
                discount = getattr(settings, 'TRIAL_LESSON_DISCOUNT', 50)
                price = price * (100 - discount) / 100

            booking = Booking.objects.create(
                student=student,
                slot=slot,
                lesson_type=lesson_type,
                topic=topic,
                student_notes=notes,
                price=price,
                status=Booking.Status.CONFIRMED,
            )

            # Slotu rezerv et
            slot.is_reserved = True
            slot.save(update_fields=['is_reserved'])

            # Google Meet linki yarat (async)
            from apps.video_conferencing.tasks import create_meet_link_task
            create_meet_link_task.delay(str(booking.id))

            # 24 saat + 1 saat əvvəl xatırlatmalar
            from apps.notifications.tasks import schedule_lesson_reminders
            schedule_lesson_reminders.delay(str(booking.id))

            # Confirmation email
            from apps.notifications.tasks import send_booking_confirmation
            send_booking_confirmation.delay(str(booking.id))

            logger.info(f"Rezervasiya yaradıldı: {booking.id} (tələbə: {student.email})")
            return booking

        except Exception as e:
            logger.error(f"Rezervasiya xətası: {e}", exc_info=True)
            return None

    @transaction.atomic
    def cancel_booking(self, booking_id: str, reason: str = '') -> bool:
        """
        Rezervasiyanı ləğv edir.

        Args:
            booking_id: Booking UUID-si
            reason: Ləğvetmə səbəbi

        Returns:
            bool: Uğurlu olduqda True
        """
        try:
            booking = Booking.objects.select_for_update().get(id=booking_id)

            if not booking.can_cancel:
                logger.warning(f"Ləğvetmə mümkün deyil: {booking_id}")
                return False

            booking.status = Booking.Status.CANCELLED
            booking.cancelled_at = timezone.now()
            booking.cancellation_reason = reason
            booking.save(update_fields=['status', 'cancelled_at', 'cancellation_reason'])

            booking.slot.is_reserved = False
            booking.slot.save(update_fields=['is_reserved'])

            from apps.notifications.tasks import send_cancellation_notification
            send_cancellation_notification.delay(str(booking.id))

            logger.info(f"Rezervasiya ləğv edildi: {booking_id}")
            return True

        except Booking.DoesNotExist:
            logger.warning(f"Rezervasiya tapılmadı: {booking_id}")
            return False
        except Exception as e:
            logger.error(f"Ləğvetmə xətası: {e}", exc_info=True)
            return False
