"""Payments App — Celery Tasks"""
from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task(bind=True, max_retries=3, queue='payments')
def check_overdue_payments_task(self) -> dict:
    """
    Gecikmiş ödənişləri yoxlayıb statuslarını yeniləyir.
    Celery Beat tərəfindən hər gün işə düşür.
    """
    try:
        from .models import Payment
        from django.utils import timezone

        updated = Payment.objects.filter(
            status=Payment.Status.PENDING,
            due_date__lt=timezone.now()
        ).update(status=Payment.Status.OVERDUE)

        logger.info(f"Gecikmiş ödəniş statusları yeniləndi: {updated} ödəniş")
        return {'updated': updated}

    except Exception as exc:
        logger.error(f"Ödəniş yoxlama xətası: {exc}", exc_info=True)
        raise self.retry(exc=exc)


@shared_task(bind=True, max_retries=3, queue='payments')
def send_overdue_payment_reminders_task(self) -> dict:
    """
    Gecikmiş ödənişlər üçün xatırlatma göndərir.
    """
    try:
        from .models import Payment
        from apps.notifications.services import NotificationService

        overdue = Payment.objects.filter(
            status=Payment.Status.OVERDUE
        ).select_related('student')

        ns = NotificationService()
        count = 0
        for payment in overdue:
            ns.send_payment_reminder(payment)
            count += 1

        logger.info(f"Ödəniş xatırlatmaları göndərildi: {count}")
        return {'sent': count}

    except Exception as exc:
        logger.error(f"Xatırlatma göndərmə xətası: {exc}", exc_info=True)
        raise self.retry(exc=exc)
