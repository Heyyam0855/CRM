"""Notifications — Services"""
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class NotificationService:
    """Email + in-app bildiriş servisi."""

    def create_notification(
        self,
        user_id: str,
        title: str,
        message: str,
        notification_type: str = 'general',
        data: Optional[dict] = None
    ) -> None:
        """In-app bildiriş yaradır."""
        try:
            from .models import Notification
            Notification.objects.create(
                user_id=user_id,
                type=notification_type,
                title=title,
                message=message,
                data=data or {}
            )
        except Exception as e:
            logger.error(f"Bildiriş yaratma xətası: {e}", exc_info=True)

    def send_booking_confirmation(self, booking_id: str) -> bool:
        """Rezervasiya təsdiq emaili göndərir."""
        try:
            from apps.bookings.models import Booking
            from django.template.loader import render_to_string
            from django.core.mail import send_mail
            from django.conf import settings

            booking = Booking.objects.select_related('student', 'slot').get(id=booking_id)
            student = booking.student

            subject = f"Dərs rezervasiyanız təsdiqləndi — {booking.slot.start_time:%d.%m.%Y %H:%M}"
            message = render_to_string('notifications/email/booking_confirmed.txt', {
                'booking': booking,
                'student': student,
            })

            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[student.email],
                fail_silently=False
            )

            self.create_notification(
                user_id=str(student.id),
                title='Rezervasiya təsdiqləndi',
                message=f"Dərsiniz {booking.slot.start_time:%d.%m.%Y %H:%M} tarixinə planlaşdırıldı.",
                notification_type='booking_confirmed',
                data={'booking_id': str(booking.id)}
            )

            logger.info(f"Booking confirmation göndərildi: {booking_id}")
            return True

        except Exception as e:
            logger.error(f"Booking email xətası: {e}", exc_info=True)
            return False

    def send_lesson_reminder(self, booking_id: str, hours_before: int) -> bool:
        """Dərs xatırlatması göndərir."""
        try:
            from apps.bookings.models import Booking
            from django.core.mail import send_mail
            from django.conf import settings

            booking = Booking.objects.select_related('student', 'slot').get(id=booking_id)
            student = booking.student

            subject = f"Dərs xatırlatması — {hours_before} saat qaldı"
            message = (
                f"Hörmətli {student.get_full_name()},\n\n"
                f"Dərsinizə {hours_before} saat qalır.\n"
                f"Tarix: {booking.slot.start_time:%d.%m.%Y %H:%M}\n"
                f"Meet linki: {booking.meet_link or 'Tezliklə göndəriləcək'}\n"
            )

            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[student.email],
                fail_silently=True
            )
            return True

        except Exception as e:
            logger.error(f"Xatırlatma email xətası: {e}", exc_info=True)
            return False

    def send_payment_reminder(self, payment) -> bool:
        """Ödəniş xatırlatması göndərir."""
        try:
            from django.core.mail import send_mail
            from django.conf import settings

            student = payment.student
            subject = "Ödəniş xatırlatması — LMS Platform"
            message = (
                f"Hörmətli {student.get_full_name()},\n\n"
                f"Ödəniş nömrəsi: {payment.invoice_number}\n"
                f"Məbləğ: {payment.amount} AZN\n"
                f"Son tarix: {payment.due_date:%d.%m.%Y}\n"
            )

            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[student.email],
                fail_silently=True
            )
            return True

        except Exception as e:
            logger.error(f"Ödəniş email xətası: {e}", exc_info=True)
            return False
