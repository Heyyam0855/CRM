"""
LMS Platform — Courses Models
Kurs, Modul, Dərs, Material idarəetməsi
"""
from apps.users.models import BaseModel
from django.db import models
from django.utils.text import slugify

from core.validators import validate_youtube_url


class Category(BaseModel):
    """Kurs kateqoriyası."""

    name = models.CharField(max_length=100, verbose_name='Ad')
    slug = models.SlugField(unique=True, verbose_name='Slug')
    description = models.TextField(blank=True, verbose_name='Təsvir')
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='Üst kateqoriya'
    )

    class Meta:
        db_table = 'courses_category'
        verbose_name = 'Kateqoriya'
        verbose_name_plural = 'Kateqoriyalar'
        ordering = ['name']

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Course(BaseModel):
    """Kurs modeli."""

    class Status(models.TextChoices):
        DRAFT = 'draft', 'Hazırlanır'
        ACTIVE = 'active', 'Aktiv'
        ARCHIVED = 'archived', 'Arxiv'

    class Level(models.TextChoices):
        BEGINNER = 'beginner', 'Başlanğıc'
        INTERMEDIATE = 'intermediate', 'Orta'
        ADVANCED = 'advanced', 'İrəliləmiş'

    title = models.CharField(max_length=255, verbose_name='Başlıq')
    slug = models.SlugField(unique=True, verbose_name='Slug')
    description = models.TextField(verbose_name='Təsvir')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='courses',
        verbose_name='Kateqoriya'
    )
    cover_image = models.ImageField(
        upload_to='course_images/',
        blank=True,
        verbose_name='Örtük şəkli'
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name='Status'
    )
    level = models.CharField(
        max_length=20,
        choices=Level.choices,
        default=Level.BEGINNER,
        verbose_name='Səviyyə'
    )
    objectives = models.TextField(blank=True, verbose_name='Kurs məqsədləri')
    prerequisites = models.TextField(blank=True, verbose_name='Ön şərtlər')
    duration_weeks = models.PositiveIntegerField(default=12, verbose_name='Müddət (həftə)')

    class Meta:
        db_table = 'courses_course'
        verbose_name = 'Kurs'
        verbose_name_plural = 'Kurslar'
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Enrollment(BaseModel):
    """Kursa qeydiyyat."""

    student = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name='Tələbə'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name='Kurs'
    )
    is_active = models.BooleanField(default=True, verbose_name='Aktivdir')
    completed_at = models.DateTimeField(
        null=True, blank=True, verbose_name='Tamamlanma tarixi'
    )

    class Meta:
        db_table = 'courses_enrollment'
        verbose_name = 'Qeydiyyat'
        verbose_name_plural = 'Qeydiyyatlar'
        unique_together = [('student', 'course')]
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"{self.student.get_full_name()} → {self.course.title}"


class Module(BaseModel):
    """Kurs modulu."""

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='modules',
        verbose_name='Kurs'
    )
    title = models.CharField(max_length=255, verbose_name='Başlıq')
    description = models.TextField(blank=True, verbose_name='Təsvir')
    order = models.PositiveSmallIntegerField(default=0, verbose_name='Sıra')

    class Meta:
        db_table = 'courses_module'
        verbose_name = 'Modul'
        verbose_name_plural = 'Modullar'
        ordering = ['order']

    def __str__(self) -> str:
        return f"{self.course.title} — {self.title}"


class Lesson(BaseModel):
    """Fərdi dərs materialı."""

    class MaterialType(models.TextChoices):
        VIDEO = 'video', 'Video (YouTube)'
        TEXT = 'text', 'Mətn dərsi'
        PDF = 'pdf', 'PDF sənəd'
        CODE = 'code', 'Kod nümunəsi'
        TASK = 'task', 'Tapşırıq'
        EXTERNAL = 'external', 'Xarici link'

    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='Modul'
    )
    title = models.CharField(max_length=255, verbose_name='Başlıq')
    description = models.TextField(blank=True, verbose_name='Təsvir')
    material_type = models.CharField(
        max_length=20,
        choices=MaterialType.choices,
        default=MaterialType.VIDEO,
        verbose_name='Material növü'
    )
    youtube_url = models.URLField(
        blank=True,
        validators=[validate_youtube_url],
        verbose_name='YouTube linki'
    )
    youtube_video_id = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='YouTube video ID'
    )
    youtube_title = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Video başlığı'
    )
    youtube_duration = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Video müddəti'
    )
    content = models.TextField(blank=True, verbose_name='Məzmun (rich text)')
    file = models.FileField(
        upload_to='lesson_files/',
        blank=True,
        verbose_name='Fayl'
    )
    order = models.PositiveSmallIntegerField(default=0, verbose_name='Sıra')
    is_free_preview = models.BooleanField(
        default=False,
        verbose_name='Pulsuz önizləmə'
    )

    class Meta:
        db_table = 'courses_lesson'
        verbose_name = 'Dərs'
        verbose_name_plural = 'Dərslər'
        ordering = ['order']
        indexes = [
            models.Index(fields=['module', 'order']),
        ]

    def __str__(self) -> str:
        return f"{self.module.course.title} → {self.title}"
