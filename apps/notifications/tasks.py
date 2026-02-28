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
