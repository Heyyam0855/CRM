"""Assessments — Models"""
from apps.users.models import BaseModel
from django.db import models


class Assessment(BaseModel):
    """Qiymətləndirmə / Test modeli."""

    class Type(models.TextChoices):
        QUIZ = 'quiz', 'Test'
        HOMEWORK = 'homework', 'Ev tapşırığı'
        PROJECT = 'project', 'Layihə'
        EXAM = 'exam', 'İmtahan'

    student = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='assessments',
        verbose_name='Tələbə'
    )
    lesson = models.ForeignKey(
        'courses.Lesson',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assessments',
        verbose_name='Dərs'
    )
    title = models.CharField(max_length=200, verbose_name='Başlıq')
    type = models.CharField(
        max_length=20,
        choices=Type.choices,
        default=Type.HOMEWORK,
        verbose_name='Növ'
    )
    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Bal (100 üzərindən)'
    )
    max_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=100,
        verbose_name='Maksimum bal'
    )
    feedback = models.TextField(blank=True, verbose_name='Rəy')
    submission_url = models.URLField(blank=True, verbose_name='GitHub / Fayl linki')
    due_date = models.DateTimeField(null=True, blank=True, verbose_name='Son tarix')
    submitted_at = models.DateTimeField(null=True, blank=True, verbose_name='Göndərilmə tarixi')

    class Meta:
        db_table = 'assessments_assessment'
        verbose_name = 'Qiymətləndirmə'
        verbose_name_plural = 'Qiymətləndirmələr'
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"{self.student.get_full_name()} — {self.title}"

    @property
    def percentage(self):
        """Faiz hesabla."""
        if self.score is not None and self.max_score:
            return round(float(self.score) / float(self.max_score) * 100, 1)
        return None
