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
    def create_monthly_payment(
        self,
        student_id: str,
        lessons_per_week: int,
    ) -> Optional[Payment]:
        """
        Aylıq abunə ödənişi yaradır.

        Args:
            student_id: Tələbə UUID-si
            lessons_per_week: Həftəlik dərs sayı

        Returns:
            Optional[Payment]: Yaradılmış ödəniş
        """
        try:
            from apps.users.models import User
            from core.utils import calculate_monthly_price

            student = User.objects.get(id=student_id)
            amount = calculate_monthly_price(lessons_per_week)

            # Ayın sonuna qədər ödəniş tarixi
            now = timezone.now()
            if now.month == 12:
                due = now.replace(year=now.year + 1, month=1, day=1)
            else:
                due = now.replace(month=now.month + 1, day=1)

            payment = Payment.objects.create(
                student=student,
                amount=amount,
                due_date=due,
                description=f"Aylıq abunə — {lessons_per_week} dərs/həftə",
                payment_method=Payment.PaymentMethod.EPOINT,
            )

            logger.info(
                f"Aylıq ödəniş yaradıldı: {payment.invoice_number} "
                f"({amount} AZN)"
            )
            return payment

        except Exception as e:
            logger.error(f"Aylıq ödəniş yaratma xətası: {e}", exc_info=True)
            return None

    @transaction.atomic
    def create_registration_payment(
        self,
        registration_request_id: str,
        amount: Decimal,
    ) -> Optional[Payment]:
        """
        Qeydiyyat zamanı ilk ödəniş yaradır (təsdiqdən əvvəl).

        Args:
            registration_request_id: RegistrationRequest UUID-si
            amount: Hesablanmış aylıq məbləğ

        Returns:
            Optional[Payment]: Yaradılmış ödəniş
        """
        try:
            from apps.users.models import RegistrationRequest

            reg = RegistrationRequest.objects.get(id=registration_request_id)

            payment = Payment.objects.create(
                amount=amount,
                due_date=timezone.now() + timezone.timedelta(days=7),
                description=(
                    f"Qeydiyyat ödənişi — {reg.full_name} "
                    f"({reg.get_course_package_display()})"
                ),
                payment_method=Payment.PaymentMethod.EPOINT,
            )

            # RegistrationRequest-ə payment_receipt olaraq bağla
            reg.payment_receipt = payment.invoice_number
            reg.save(update_fields=['payment_receipt', 'updated_at'])

            logger.info(
                f"Qeydiyyat ödənişi yaradıldı: {payment.invoice_number} "
                f"({amount} AZN)"
            )
            return payment

        except Exception as e:
            logger.error(
                f"Qeydiyyat ödəniş xətası: {e}", exc_info=True
            )
            return None

    def initiate_epoint_payment(self, payment_id: str) -> Optional[str]:
        """
        ePoint ödəniş səhifəsinə yönləndirmə URL-i alır.

        Args:
            payment_id: Payment UUID-si

        Returns:
            Optional[str]: ePoint redirect URL
        """
        try:
            payment = Payment.objects.get(id=payment_id)
            from .epoint_service import EPointService

            epoint = EPointService()
            result = epoint.initiate_payment(
                order_id=str(payment.id),
                amount=payment.amount,
                description=payment.description or 'LMS Platform ödənişi',
            )

            if result:
                payment.epoint_order_id = str(payment.id)
                payment.epoint_transaction_id = result.get('transaction_id', '')
                payment.save(update_fields=[
                    'epoint_order_id', 'epoint_transaction_id',
                ])
                return result.get('redirect_url')

            return None

        except Payment.DoesNotExist:
            logger.warning(f"Ödəniş tapılmadı: {payment_id}")
            return None
        except Exception as e:
            logger.error(f"ePoint başlatma xətası: {e}", exc_info=True)
            return None

    @transaction.atomic
    def process_epoint_callback(self, data: dict) -> bool:
        """
        ePoint callback-ini emal edir.

        Args:
            data: Decoded callback data

        Returns:
            bool: Uğurlu olduqda True
        """
        try:
            order_id = data.get('order_id', '')
            status = data.get('status', '')
            transaction_id = data.get('transaction_id', '')

            payment = Payment.objects.get(id=order_id)

            if status == 'success':
                payment.status = Payment.Status.COMPLETED
                payment.paid_at = timezone.now()
                payment.epoint_transaction_id = transaction_id
                payment.save(update_fields=[
                    'status', 'paid_at', 'epoint_transaction_id',
                ])

                # Booking varsa ödənilmiş kimi işarələ
                if payment.booking:
                    payment.booking.is_paid = True
                    payment.booking.save(update_fields=['is_paid'])

                # Ödəniş qəbzi göndər
                from apps.notifications.tasks import send_payment_receipt
                send_payment_receipt.delay(str(payment.id))

                logger.info(
                    f"ePoint ödəniş tamamlandı: {payment.invoice_number}"
                )
                return True

            else:
                payment.status = Payment.Status.FAILED
                payment.save(update_fields=['status'])
                logger.warning(
                    f"ePoint ödəniş uğursuz: {payment.invoice_number}"
                )
                return False

        except Payment.DoesNotExist:
            logger.warning(f"ePoint callback — ödəniş tapılmadı: {order_id}")
            return False
        except Exception as e:
            logger.error(f"ePoint callback xətası: {e}", exc_info=True)
            return False
