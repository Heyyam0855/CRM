"""Notifications — Celery Tasks"""
from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60, queue='notifications')
def send_booking_confirmation(self, booking_id: str) -> dict:
    """Rezervasiya təsdiq emaili göndərir."""
    try:
        from .services import NotificationService
        ns = NotificationService()
        success = ns.send_booking_confirmation(booking_id)
        return {'success': success, 'booking_id': booking_id}
    except Exception as exc:
        logger.error(f"Booking confirmation task xətası: {exc}", exc_info=True)
        raise self.retry(exc=exc)


@shared_task(bind=True, max_retries=3, default_retry_delay=60, queue='notifications')
def send_lesson_reminder(self, booking_id: str, hours_before: int = 24) -> dict:
    """Dərs xatırlatması göndərir."""
    try:
        from .services import NotificationService
        ns = NotificationService()
        success = ns.send_lesson_reminder(booking_id, hours_before)
        return {'success': success}
    except Exception as exc:
        raise self.retry(exc=exc)


@shared_task(bind=True, max_retries=3, default_retry_delay=60, queue='notifications')
def send_payment_receipt(self, payment_id: str) -> dict:
    """Ödəniş qəbzi emaili göndərir."""
    try:
        from apps.payments.models import Payment
        from django.core.mail import send_mail
        from django.conf import settings

        payment = Payment.objects.select_related('student').get(id=payment_id)
        student = payment.student

        subject = f"Ödəniş qəbzi — {payment.invoice_number}"
        message = (
            f"Hörmətli {student.get_full_name()},\n\n"
            f"Ödənişiniz uğurla qeydə alındı.\n"
            f"Faktura: {payment.invoice_number}\n"
            f"Məbləğ: {payment.amount} AZN\n"
            f"Tarix: {payment.paid_at:%d.%m.%Y %H:%M}\n"
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[student.email],
            fail_silently=True
        )
        return {'success': True}

    except Exception as exc:
        raise self.retry(exc=exc)


@shared_task(bind=True, max_retries=3, default_retry_delay=60, queue='notifications')
def send_student_approval_email(self, student_id: str) -> dict:
    """Tələbə aktivasiya emaili göndərir."""
    try:
        from apps.users.models import User
        from django.core.mail import send_mail
        from django.conf import settings

        student = User.objects.get(id=student_id)
        subject = "Hesabınız aktivləşdirildi — LMS Platform"
        message = (
            f"Hörmətli {student.get_full_name()},\n\n"
            f"Müəllim tərəfindən hesabınız aktivləşdirildi.\n"
            f"İndi plaformaya daxil ola bilərsiniz.\n"
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[student.email],
            fail_silently=True
        )
        return {'success': True}

    except Exception as exc:
        raise self.retry(exc=exc)


@shared_task(bind=True, max_retries=3, default_retry_delay=60, queue='notifications')
def schedule_lesson_reminders(self, booking_id: str) -> dict:
    """
    Dərs üçün 24 saat və 1 saat əvvəl xatırlatma task-larını planlaşdırır.

    Args:
        booking_id: Booking UUID-si

    Returns:
        dict: Nəticə
    """
    try:
        from apps.bookings.models import Booking
        from django.utils import timezone
        from datetime import timedelta

        booking = Booking.objects.select_related('slot').get(id=booking_id)
        start_time = booking.slot.start_time
        now = timezone.now()

        scheduled = []

        # 24 saat əvvəl xatırlatma
        reminder_24h = start_time - timedelta(hours=24)
        if reminder_24h > now:
            send_lesson_reminder.apply_async(
                args=[booking_id, 24],
                eta=reminder_24h
            )
            scheduled.append('24h')

        # 1 saat əvvəl xatırlatma
        reminder_1h = start_time - timedelta(hours=1)
        if reminder_1h > now:
            send_lesson_reminder.apply_async(
                args=[booking_id, 1],
                eta=reminder_1h
            )
            scheduled.append('1h')

        logger.info(f"Xatırlatmalar planlaşdırıldı: booking={booking_id}, {scheduled}")
        return {'success': True, 'scheduled': scheduled}

    except Exception as exc:
        logger.error(f"Xatırlatma planlaşdırma xətası: {exc}", exc_info=True)
        raise self.retry(exc=exc)


@shared_task(bind=True, max_retries=3, default_retry_delay=60, queue='notifications')
def send_cancellation_notification(self, booking_id: str) -> dict:
    """
    Rezervasiya ləğvi haqqında bildiriş göndərir.

    Args:
        booking_id: Booking UUID-si

    Returns:
        dict: Nəticə
    """
    try:
        from apps.bookings.models import Booking
        from django.core.mail import send_mail
        from django.conf import settings

        booking = Booking.objects.select_related('student', 'slot').get(id=booking_id)
        student = booking.student

        subject = "Rezervasiya ləğv edildi — LMS Platform"
        message = (
            f"Hörmətli {student.get_full_name()},\n\n"
            f"Dərs rezervasiyanız ləğv edildi.\n"
            f"Tarix: {booking.slot.start_time:%d.%m.%Y %H:%M}\n"
        )
        if booking.cancellation_reason:
            message += f"Səbəb: {booking.cancellation_reason}\n"
        message += "\nSualınız varsa, müəllimlə əlaqə saxlayın.\n"

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[student.email],
            fail_silently=False
        )

        # In-app bildiriş
        from .services import NotificationService
        ns = NotificationService()
        ns.create_notification(
            user_id=str(student.id),
            title='Rezervasiya ləğv edildi',
            message=f"Dərsiniz ({booking.slot.start_time:%d.%m.%Y %H:%M}) ləğv edildi.",
            notification_type='booking_cancelled',
            data={'booking_id': str(booking.id)}
        )

        logger.info(f"Ləğv bildirişi göndərildi: booking={booking_id}")
        return {'success': True, 'booking_id': booking_id}

    except Exception as exc:
        logger.error(f"Ləğv bildirişi xətası: {exc}", exc_info=True)
        raise self.retry(exc=exc)


@shared_task(bind=True, max_retries=3, default_retry_delay=60, queue='notifications')
def send_student_credentials_email(self, student_id: str, password: str) -> dict:
    """Tələbəyə login məlumatlarını email ilə göndərir."""
    try:
        from apps.users.models import User
        from django.core.mail import send_mail
        from django.conf import settings

        student = User.objects.get(id=student_id)
        login_url = f"{settings.SITE_URL}/accounts/login/" if hasattr(settings, 'SITE_URL') else "/accounts/login/"

        subject = "Hesabınız yaradıldı — LMS Platform"
        message = (
            f"Hörmətli {student.get_full_name()},\n\n"
            f"LMS Platformunda hesabınız yaradıldı.\n\n"
            f"Giriş məlumatlarınız:\n"
            f"  Email: {student.email}\n"
            f"  Parol: {password}\n\n"
            f"Platforma giriş linki: {login_url}\n\n"
            f"Təhlükəsizlik üçün ilk girişdən sonra parolunuzu dəyişdirməyiniz tövsiyə olunur.\n\n"
            f"Uğurlar!\n"
            f"LMS Platform"
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[student.email],
            fail_silently=False,
        )
        logger.info(f"Login məlumatları göndərildi: {student.email}")
        return {'success': True, 'student_id': student_id}

    except Exception as exc:
        logger.error(f"Credentials email xətası: {exc}", exc_info=True)
        raise self.retry(exc=exc)
