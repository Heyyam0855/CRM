"""Payments App — Services"""
from decimal import Decimal
from typing import Optional
import logging

from django.db import transaction
from django.utils import timezone

from .models import Payment, MonthlySubscription

logger = logging.getLogger(__name__)


class PaymentService:
    """Ödəniş business logic."""

    @transaction.atomic
    def create_lesson_payment(
        self,
        student_id: str,
        booking_id: str,
        amount: Optional[Decimal] = None
    ) -> Optional[Payment]:
        """
        Dərs üçün ödəniş yaradır (pay-as-you-go model).

        Args:
            student_id: Tələbə UUID-si
            booking_id: Booking UUID-si
            amount: Məbləğ (None olduqda LESSON_PRICE istifadə olunur)

        Returns:
            Optional[Payment]: Yaradılmış ödəniş
        """
        try:
            from django.conf import settings
            from apps.users.models import User
            from apps.bookings.models import Booking

            student = User.objects.get(id=student_id)
            booking = Booking.objects.get(id=booking_id)
            pay_amount = amount or getattr(settings, 'LESSON_PRICE', Decimal('25.00'))

            # 24 saat sonra son ödəniş tarixi
            due = timezone.now() + timezone.timedelta(hours=24)

            payment = Payment.objects.create(
                student=student,
                booking=booking,
                amount=pay_amount,
                due_date=due,
                description=f"Dərs ödənişi — {booking.slot.start_time:%d.%m.%Y}",
            )

            logger.info(f"Ödəniş yaradıldı: {payment.invoice_number} ({pay_amount} AZN)")
            return payment

        except Exception as e:
            logger.error(f"Ödəniş yaratma xətası: {e}", exc_info=True)
            return None

    @transaction.atomic
    def process_stripe_payment(
        self,
        payment_id: str,
        payment_intent_id: str
    ) -> bool:
        """
        Stripe ödənişini tamamlayır.

        Args:
            payment_id: Payment UUID-si
            payment_intent_id: Stripe PaymentIntent ID

        Returns:
            bool: Uğurlu olduqda True
        """
        try:
            payment = Payment.objects.get(id=payment_id)
            payment.status = Payment.Status.COMPLETED
            payment.stripe_payment_intent_id = payment_intent_id
            payment.paid_at = timezone.now()
            payment.save(
                update_fields=['status', 'stripe_payment_intent_id', 'paid_at']
            )

            # Booking-i ödənilmiş kimi işarələ
            if payment.booking:
                payment.booking.is_paid = True
                payment.booking.save(update_fields=['is_paid'])

            from apps.notifications.tasks import send_payment_receipt
            send_payment_receipt.delay(str(payment.id))

            logger.info(f"Stripe ödənişi tamamlandı: {payment.invoice_number}")
            return True

        except Exception as e:
            logger.error(f"Stripe ödəniş xətası: {e}", exc_info=True)
            return False
