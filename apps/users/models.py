"""
LMS Platform — Users Models
İstifadəçi idarəetməsi: Müəllim + Tələbə
"""
import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

from core.validators import validate_phone_number, validate_github_username


class BaseModel(models.Model):
    """Bütün modellər üçün əsas sinif — UUID pk + timestamps."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yaradılma tarixi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Yenilənmə tarixi')

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    """Xüsusi istifadəçi manager."""

    def create_user(self, email: str, password: str = None, **extra_fields):
        if not email:
            raise ValueError('Email ünvanı mütləqdir.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', User.Role.TEACHER)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    LMS istifadəçi modeli.
    Müəllim və tələbə eyni model üzərindədir — role ilə fərqlənir.
    """

    class Role(models.TextChoices):
        TEACHER = 'teacher', 'Müəllim'
        STUDENT = 'student', 'Tələbə'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, verbose_name='Email')
    first_name = models.CharField(max_length=100, verbose_name='Ad')
    last_name = models.CharField(max_length=100, verbose_name='Soyad')
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.STUDENT,
        verbose_name='Rol'
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        validators=[validate_phone_number],
        verbose_name='Telefon'
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        verbose_name='Profil şəkli'
    )
    is_active = models.BooleanField(default=True, verbose_name='Aktivdir')
    is_staff = models.BooleanField(default=False, verbose_name='Admin heyəti')
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='Qeydiyyat tarixi')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        db_table = 'users_user'
        verbose_name = 'İstifadəçi'
        verbose_name_plural = 'İstifadəçilər'
        ordering = ['-date_joined']

    def __str__(self) -> str:
        return f"{self.get_full_name()} ({self.email})"

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self) -> str:
        return self.first_name

    @property
    def is_teacher(self) -> bool:
        return self.role == self.Role.TEACHER

    @property
    def is_student_user(self) -> bool:
        return self.role == self.Role.STUDENT


class StudentProfile(BaseModel):
    """
    Tələbə əlavə profil məlumatları.
    User modelini genişləndirir.
    """

    class Status(models.TextChoices):
        PENDING = 'pending', 'Gözləyir'
        ACTIVE = 'active', 'Aktiv'
        INACTIVE = 'inactive', 'Passiv'
        FROZEN = 'frozen', 'Dondurulmuş'
        GRADUATED = 'graduated', 'Bitirmiş'

    class PaymentModel(models.TextChoices):
        MONTHLY = 'monthly', 'Aylıq abunə'
        PER_LESSON = 'per_lesson', 'Dərs əsaslı'

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_profile',
        verbose_name='İstifadəçi'
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name='Status'
    )
    payment_model = models.CharField(
        max_length=20,
        choices=PaymentModel.choices,
        default=PaymentModel.MONTHLY,
        verbose_name='Ödəniş modeli'
    )
    lessons_per_week = models.PositiveSmallIntegerField(
        default=2,
        verbose_name='Həftəlik dərs sayı'
    )
    github_username = models.CharField(
        max_length=100,
        blank=True,
        validators=[validate_github_username],
        verbose_name='GitHub istifadəçi adı'
    )
    github_repo_url = models.URLField(
        blank=True,
        verbose_name='GitHub repo URL'
    )
    timezone = models.CharField(
        max_length=50,
        default='Asia/Baku',
        verbose_name='Vaxt zonası'
    )
    education_level = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Təhsil səviyyəsi'
    )
    goals = models.TextField(
        blank=True,
        verbose_name='Öyrənmə məqsədləri'
    )
    teacher_notes = models.TextField(
        blank=True,
        verbose_name='Müəllim qeydləri (gizli)'
    )
    status_changed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Status dəyişikliyi tarixi'
    )

    class Meta:
        db_table = 'users_student_profile'
        verbose_name = 'Tələbə Profili'
        verbose_name_plural = 'Tələbə Profilləri'

    def __str__(self) -> str:
        return f"{self.user.get_full_name()} — {self.get_status_display()}"

    def get_monthly_price(self):
        """Aylıq ödəniş məbləğini hesablayır."""
        from core.utils import calculate_monthly_price
        return calculate_monthly_price(self.lessons_per_week)


class RegistrationRequest(BaseModel):
    """
    Tələbə qeydiyyat müraciəti.
    Google Form tipli açıq form — hesab yaradılmır, müəllim təsdiqi gözlənilir.
    """

    class CoursePackage(models.TextChoices):
        FRONT_END = 'front_end', 'Front End Development'
        BACK_END = 'back_end', 'Back End Development'
        FULL_STACK = 'full_stack', 'Full Stack Development'
        API_DRIVEN = 'api_driven', 'API (API Driven Development)'
        DSA = 'dsa', 'DSA (Data Structure and Algorithms)'
        CYBER_SECURITY = 'cyber_security', 'Cyber Security'
        PROJECT_MENTORSHIP = 'project_mentorship', 'Project Mentorship'
        OTHER = 'other', 'Digər'

    class Status(models.TextChoices):
        PENDING = 'pending', 'Gözləyir'
        APPROVED = 'approved', 'Təsdiqləndi'
        REJECTED = 'rejected', 'Rədd edildi'

    full_name = models.CharField(max_length=200, verbose_name='Ad Soyad')
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(
        max_length=20,
        validators=[validate_phone_number],
        verbose_name='Telefon (Whatsapp)'
    )
    course_package = models.CharField(
        max_length=30,
        choices=CoursePackage.choices,
        verbose_name='Dərs paketi'
    )
    other_course = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Digər dərs paketi (əgər "Digər" seçilibsə)'
    )
    payment_receipt = models.CharField(
        max_length=500,
        blank=True,
        verbose_name='Ödəmə məlumatı'
    )
    preferred_start_date = models.DateField(
        verbose_name='Başlamaq istədiyi tarix'
    )
    lessons_per_week = models.PositiveSmallIntegerField(
        default=2,
        verbose_name='Həftəlik dərs sayı'
    )
    github_profile_url = models.URLField(
        blank=True,
        verbose_name='GitHub profil linki'
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name='Status'
    )
    teacher_notes = models.TextField(
        blank=True,
        verbose_name='Müəllim qeydləri'
    )
    approved_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='registration_request',
        verbose_name='Yaradılmış istifadəçi'
    )

    class Meta:
        db_table = 'users_registration_request'
        verbose_name = 'Qeydiyyat müraciəti'
        verbose_name_plural = 'Qeydiyyat müraciətləri'
        ordering = ['-created_at']

    def __str__(self) -> str:
        pkg = self.get_course_package_display()
        status = self.get_status_display()
        return f"{self.full_name} — {pkg} ({status})"
