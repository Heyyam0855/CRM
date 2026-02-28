"""Notifications — Models"""
from apps.users.models import BaseModel
from django.db import models


class Notification(BaseModel):
    """İstifadəçi bildirişi modeli."""

    class Type(models.TextChoices):
        BOOKING_CONFIRMED = 'booking_confirmed', 'Rezervasiya təsdiqləndi'
        BOOKING_CANCELLED = 'booking_cancelled', 'Rezervasiya ləğv edildi'
        LESSON_REMINDER = 'lesson_reminder', 'Dərs xatırlatması'
        PAYMENT_DUE = 'payment_due', 'Ödəniş müddəti'
        PAYMENT_RECEIVED = 'payment_received', 'Ödəniş alındı'
        PAYMENT_OVERDUE = 'payment_overdue', 'Gecikmiş ödəniş'
        REPO_CREATED = 'repo_created', 'GitHub repo yaradıldı'
        GENERAL = 'general', 'Ümumi'

    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='İstifadəçi'
    )
    type = models.CharField(
        max_length=40,
        choices=Type.choices,
        default=Type.GENERAL,
        verbose_name='Növ'
    )
    title = models.CharField(max_length=200, verbose_name='Başlıq')
    message = models.TextField(verbose_name='Məzmun')
    is_read = models.BooleanField(default=False, verbose_name='Oxunub')
    data = models.JSONField(default=dict, blank=True, verbose_name='Əlavə məlumat')

    class Meta:
        db_table = 'notifications_notification'
        verbose_name = 'Bildiriş'
        verbose_name_plural = 'Bildirişlər'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
        ]

    def __str__(self) -> str:
        return f"{self.user.email} — {self.title}"
