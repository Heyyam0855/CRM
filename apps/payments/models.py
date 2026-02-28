"""
LMS Platform — Payments Models
Aylıq abunə + Dərs əsaslı ödəniş sistemi
"""
from decimal import Decimal
from apps.users.models import BaseModel
from django.db import models


class Payment(BaseModel):
    """Ödəniş modeli — hər iki model üçün."""

    class Status(models.TextChoices):
        PENDING = 'pending', 'Gözləmədə'
        COMPLETED = 'completed', 'Tamamlandı'
        FAILED = 'failed', 'Uğursuz'
        REFUNDED = 'refunded', 'Geri qaytarıldı'
        OVERDUE = 'overdue', 'Gecikib'
        CANCELLED = 'cancelled', 'Ləğv edildi'

    class PaymentMethod(models.TextChoices):
        STRIPE = 'stripe', 'Stripe (Kart)'
        BANK_TRANSFER = 'bank_transfer', 'Bank Köçürməsi'
        CASH = 'cash', 'Nağd'
        ONLINE = 'online', 'Online (e-Manat)'

    student = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Tələbə'
    )
    booking = models.ForeignKey(
        'bookings.Booking',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payments',
        verbose_name='Rezervasiya'
    )
    amount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='Məbləğ (AZN)'
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name='Status'
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
        default=PaymentMethod.STRIPE,
        verbose_name='Ödəniş üsulu'
    )
    stripe_payment_intent_id = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Stripe PaymentIntent ID'
    )
    invoice_number = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        verbose_name='Faktura nömrəsi'
    )
    description = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Açıqlama'
    )
    paid_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Ödəniş tarixi'
    )
    due_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Son ödəniş tarixi'
    )

    class Meta:
        db_table = 'payments_payment'
        verbose_name = 'Ödəniş'
        verbose_name_plural = 'Ödənişlər'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['student', 'status']),
            models.Index(fields=['status', 'due_date']),
        ]

    def __str__(self) -> str:
        return f"{self.student.get_full_name()} — {self.amount} AZN ({self.get_status_display()})"

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            from core.utils import generate_invoice_number
            self.invoice_number = generate_invoice_number()
        super().save(*args, **kwargs)


class MonthlySubscription(BaseModel):
    """Aylıq abunə modeli."""

    class Status(models.TextChoices):
        ACTIVE = 'active', 'Aktiv'
        PAUSED = 'paused', 'Dayandırılıb'
        CANCELLED = 'cancelled', 'Ləğv edildi'

    student = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Tələbə'
    )
    lessons_per_week = models.PositiveSmallIntegerField(
        verbose_name='Həftəlik dərs sayı'
    )
    monthly_amount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='Aylıq məbləğ (AZN)'
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
        verbose_name='Status'
    )
    stripe_subscription_id = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Stripe Subscription ID'
    )
    next_billing_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Növbəti ödəniş tarixi'
    )

    class Meta:
        db_table = 'payments_monthly_subscription'
        verbose_name = 'Aylıq Abunə'
        verbose_name_plural = 'Aylıq Abunələr'

    def __str__(self) -> str:
        return (
            f"{self.student.get_full_name()} — "
            f"{self.monthly_amount} AZN/ay ({self.get_status_display()})"
        )
