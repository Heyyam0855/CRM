"""GitHub Integration — Models"""
from apps.users.models import BaseModel
from django.db import models


class StudentRepository(BaseModel):
    """Tələbənin GitHub repository-si."""

    class Status(models.TextChoices):
        PENDING = 'pending', 'Gözləmədə'
        CREATING = 'creating', 'Yaradılır'
        CREATED = 'created', 'Yaradıldı'
        FAILED = 'failed', 'Uğursuz'
        ARCHIVED = 'archived', 'Arxivləşdirildi'

    student = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='repositories',
        verbose_name='Tələbə'
    )
    course = models.ForeignKey(
        'courses.Course',
        on_delete=models.CASCADE,
        related_name='repositories',
        verbose_name='Kurs'
    )
    repo_name = models.CharField(max_length=100, verbose_name='Repository adı')
    repo_url = models.URLField(blank=True, verbose_name='Repository URL')
    repo_full_name = models.CharField(
        max_length=200, blank=True,
        verbose_name='Tam ad (owner/repo)'
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name='Status'
    )
    error_message = models.TextField(blank=True, verbose_name='Xəta mesajı')

    class Meta:
        db_table = 'github_student_repository'
        verbose_name = 'Tələbə Repository'
        verbose_name_plural = 'Tələbə Repositoryləri'
        unique_together = [('student', 'course')]

    def __str__(self) -> str:
        return f"{self.repo_name} ({self.get_status_display()})"
