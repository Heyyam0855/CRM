"""Bookings App — Services"""
import logging
import sys
from datetime import datetime, timedelta, time as dt_time
from typing import Optional

from django.db import transaction
from django.utils import timezone

from .models import AvailabilitySlot, Booking, WeeklySchedule

logger = logging.getLogger(__name__)


class BookingService:
    """Dərs rezervasiyası business logic."""

    @staticmethod
    def _should_skip_async_tasks() -> bool:
        """Pytest zamanı broker bağlantısından qaçmaq üçün async taskları burax."""
        return 'pytest' in sys.modules

    def _enqueue_booking_tasks(self, booking_id: str) -> None:
        """Booking üçün asinxron əməliyyatları etibarlı şəkildə növbəyə əlavə et."""
        if self._should_skip_async_tasks():
            return

        try:
            from apps.video_conferencing.tasks import create_meet_link_task
            create_meet_link_task.delay(booking_id)

            from apps.notifications.tasks import schedule_lesson_reminders
            schedule_lesson_reminders.delay(booking_id)

            from apps.notifications.tasks import send_booking_confirmation
            send_booking_confirmation.delay(booking_id)
        except Exception as exc:
            logger.warning("Async task enqueue alınmadı: %s", exc, exc_info=True)

    def _enqueue_cancellation_task(self, booking_id: str) -> None:
        """Ləğv bildirişini təhlükəsiz şəkildə növbəyə əlavə et."""
        if self._should_skip_async_tasks():
            return

        try:
            from apps.notifications.tasks import send_cancellation_notification
            send_cancellation_notification.delay(booking_id)
        except Exception as exc:
            logger.warning(
                "Ləğv bildirişi enqueue alınmadı: %s",
                exc,
                exc_info=True,
            )

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
        """
        try:
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

            slot.is_reserved = True
            slot.save(update_fields=['is_reserved'])

            self._enqueue_booking_tasks(str(booking.id))

            logger.info(f"Rezervasiya yaradıldı: {booking.id} (tələbə: {student.email})")
            return booking

        except Exception as e:
            logger.error(f"Rezervasiya xətası: {e}", exc_info=True)
            return None

    @transaction.atomic
    def cancel_booking(self, booking_id: str, reason: str = '') -> bool:
        """Rezervasiyanı ləğv edir."""
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

            self._enqueue_cancellation_task(str(booking.id))

            logger.info(f"Rezervasiya ləğv edildi: {booking_id}")
            return True

        except Booking.DoesNotExist:
            logger.warning(f"Rezervasiya tapılmadı: {booking_id}")
            return False
        except Exception as e:
            logger.error(f"Ləğvetmə xətası: {e}", exc_info=True)
            return False


class ScheduleService:
    """Həftəlik cədvəl və slot yaratma xidməti."""

    def generate_slots(self, weeks_ahead: int = 4) -> int:
        """
        Həftəlik cədvəl əsasında gələcək həftələr üçün slot-lar yaradır.

        Args:
            weeks_ahead: Neçə həftə irəli üçün slot yaratmaq

        Returns:
            int: Yaradılmış slot sayı
        """
        schedules = WeeklySchedule.objects.filter(is_active=True)
        if not schedules.exists():
            return 0

        now = timezone.now()
        today = now.date()
        created_count = 0

        for week_offset in range(weeks_ahead):
            week_start = today + timedelta(weeks=week_offset)
            # Həftənin bazar ertəsinə düzəlt
            monday = week_start - timedelta(days=week_start.weekday())

            for schedule in schedules:
                target_date = monday + timedelta(days=schedule.day_of_week)

                # Keçmişdəki tarix üçün slot yaratma
                if target_date < today:
                    continue
                if target_date == today:
                    min_time = (now + timedelta(hours=2)).time()
                else:
                    min_time = dt_time(0, 0)

                current_time = schedule.start_time
                while current_time < schedule.end_time:
                    if current_time < min_time and target_date == today:
                        # Bu saata çatmışıq, növbəti slota keç
                        minutes = (
                            current_time.hour * 60 + current_time.minute
                            + schedule.slot_duration
                        )
                        current_time = dt_time(minutes // 60, minutes % 60)
                        continue

                    slot_start = timezone.make_aware(
                        datetime.combine(target_date, current_time)
                    )
                    end_minutes = (
                        current_time.hour * 60 + current_time.minute
                        + schedule.slot_duration
                    )
                    slot_end_time = dt_time(
                        min(end_minutes // 60, 23),
                        end_minutes % 60
                    )
                    slot_end = timezone.make_aware(
                        datetime.combine(target_date, slot_end_time)
                    )

                    # Dublikat yoxla
                    if not AvailabilitySlot.objects.filter(
                        start_time=slot_start,
                        end_time=slot_end,
                    ).exists():
                        AvailabilitySlot.objects.create(
                            start_time=slot_start,
                            end_time=slot_end,
                            is_active=True,
                        )
                        created_count += 1

                    # Növbəti slot
                    minutes = (
                        current_time.hour * 60 + current_time.minute
                        + schedule.slot_duration
                    )
                    if minutes >= 24 * 60:
                        break
                    current_time = dt_time(minutes // 60, minutes % 60)

        logger.info(f"{created_count} slot yaradıldı ({weeks_ahead} həftəlik)")
        return created_count

    def get_available_slots_by_date(self) -> dict:
        """
        Əlçatan slot-ları tarix əsaslı qruplaşdırılmış qaytarır.

        Returns:
            dict: {date_str: [slot1, slot2, ...]}
        """
        now = timezone.now()
        slots = (
            AvailabilitySlot.objects
            .filter(
                is_reserved=False,
                is_active=True,
                start_time__gt=now,
            )
            .order_by('start_time')
        )

        grouped = {}
        for slot in slots:
            date_key = slot.start_time.strftime('%Y-%m-%d')
            if date_key not in grouped:
                grouped[date_key] = []
            grouped[date_key].append(slot)

        return grouped
