"""
LMS Platform — Bookings Models
Dərs rezervasiyası sistemi (Calendly tipli)
"""
from apps.users.models import BaseModel
from django.db import models
from django.utils import timezone

from core.validators import validate_future_datetime


class WeeklySchedule(BaseModel):
    """
    Müəllimin həftəlik iş cədvəli.
    Hər gün üçün başlama/bitmə saatı təyin edilir.
    Bu cədvəl əsasında avtomatik slot-lar yaradılır.
    """

    class DayOfWeek(models.IntegerChoices):
        MONDAY = 0, 'Bazar ertəsi'
        TUESDAY = 1, 'Çərşənbə axşamı'
        WEDNESDAY = 2, 'Çərşənbə'
        THURSDAY = 3, 'Cümə axşamı'
        FRIDAY = 4, 'Cümə'
        SATURDAY = 5, 'Şənbə'
        SUNDAY = 6, 'Bazar'

    day_of_week = models.IntegerField(
        choices=DayOfWeek.choices,
        verbose_name='Həftənin günü'
    )
    start_time = models.TimeField(verbose_name='Başlama saatı')
    end_time = models.TimeField(verbose_name='Bitmə saatı')
    slot_duration = models.PositiveSmallIntegerField(
        default=60,
        verbose_name='Slot müddəti (dəqiqə)'
    )
    is_active = models.BooleanField(default=True, verbose_name='Aktivdir')

    class Meta:
        db_table = 'bookings_weekly_schedule'
        verbose_name = 'Həftəlik Cədvəl'
        verbose_name_plural = 'Həftəlik Cədvəllər'
        ordering = ['day_of_week', 'start_time']
        unique_together = ['day_of_week', 'start_time']

    def __str__(self) -> str:
        return (
            f"{self.get_day_of_week_display()} "
            f"{self.start_time:%H:%M}—{self.end_time:%H:%M}"
        )


class AvailabilitySlot(BaseModel):
    """
    Müəllimin əlçatan vaxt slotu.
    Hər slot = 1 dərs yeri.
    """

    start_time = models.DateTimeField(
        validators=[validate_future_datetime],
        verbose_name='Başlama vaxtı'
    )
    end_time = models.DateTimeField(verbose_name='Bitmə vaxtı')
    is_reserved = models.BooleanField(default=False, verbose_name='Reserv edilib')
    is_active = models.BooleanField(default=True, verbose_name='Aktivdir')

    class Meta:
        db_table = 'bookings_availability_slot'
        verbose_name = 'Əlçatan Slot'
        verbose_name_plural = 'Əlçatan Slotlar'
        ordering = ['start_time']
        indexes = [
            models.Index(fields=['start_time', 'is_reserved']),
            models.Index(fields=['is_reserved', 'is_active']),
        ]

    def __str__(self) -> str:
        return f"{self.start_time:%d.%m.%Y %H:%M} — {'Dolu' if self.is_reserved else 'Boş'}"

    def duration_minutes(self) -> int:
        """Slot müddəti dəqiqə ilə."""
        delta = self.end_time - self.start_time
        return int(delta.total_seconds() / 60)


class Booking(BaseModel):
    """
    Dərs rezervasiyası.
    Hər booking = tələbənin müəllimlə 1-1 dərs təyinatı.
    """

    class Status(models.TextChoices):
        PENDING = 'pending', 'Gözləmədə'
        CONFIRMED = 'confirmed', 'Təsdiqləndi'
        COMPLETED = 'completed', 'Tamamlandı'
        CANCELLED = 'cancelled', 'Ləğv edildi'
        NO_SHOW = 'no_show', 'Görünmədi'
        RESCHEDULED = 'rescheduled', 'Yenidən planlandı'

    class LessonType(models.TextChoices):
        STANDARD = 'standard', 'Standart dərs'
        TRIAL = 'trial', 'Sınaq dərsi'
        CONSULTATION = 'consultation', 'Məsləhət'
        REVIEW = 'review', 'Təkrar dərs'

    student = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name='Tələbə'
    )
    slot = models.OneToOneField(
        AvailabilitySlot,
        on_delete=models.CASCADE,
        related_name='booking',
        verbose_name='Vaxt slotu'
    )
    course = models.ForeignKey(
        'courses.Course',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bookings',
        verbose_name='Kurs'
    )
    lesson_type = models.CharField(
        max_length=20,
        choices=LessonType.choices,
        default=LessonType.STANDARD,
        verbose_name='Dərs növü'
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name='Status'
    )
    topic = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Mövzu'
    )
    student_notes = models.TextField(
        blank=True,
        verbose_name='Tələbə qeydləri'
    )
    teacher_notes = models.TextField(
        blank=True,
        verbose_name='Müəllim qeydləri'
    )
    meet_link = models.URLField(
        blank=True,
        verbose_name='Google Meet linki'
    )
    recording_url = models.URLField(
        blank=True,
        verbose_name='Qeyd URL'
    )
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=25.00,
        verbose_name='Qiymət (AZN)'
    )
    is_paid = models.BooleanField(default=False, verbose_name='Ödənilib')
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Tamamlanma tarixi'
    )
    cancelled_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Ləğvetmə tarixi'
    )
    cancellation_reason = models.TextField(
        blank=True,
        verbose_name='Ləğvetmə səbəbi'
    )

    class Meta:
        db_table = 'bookings_booking'
        verbose_name = 'Rezervasiya'
        verbose_name_plural = 'Rezervasiyalar'
        ordering = ['-slot__start_time']
        indexes = [
            models.Index(fields=['student', 'status']),
            models.Index(fields=['status', 'is_paid']),
        ]

    def __str__(self) -> str:
        return (
            f"{self.student.get_full_name()} — "
            f"{self.slot.start_time:%d.%m.%Y %H:%M}"
        )

    @property
    def can_cancel(self) -> bool:
        """24 saat əvvəl ləğvetmə mümkündür."""
        from django.conf import settings
        hours = getattr(settings, 'CANCELLATION_HOURS', 24)
        if self.status not in (self.Status.PENDING, self.Status.CONFIRMED):
            return False
        time_left = self.slot.start_time - timezone.now()
        return time_left.total_seconds() > hours * 3600
