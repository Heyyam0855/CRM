<!-- filepath: .github/copilot-skills.md -->
# GitHub Copilot Bacarıqları (Skills) — LMS Platformu

> **AI Model**: Claude Sonnet 4.6  
> **Framework**: Django 5.0+ | Python 3.11+  
> **Məqsəd**: Copilot-ın LMS layihəsində hansı bacarıqlardan istifadə edəcəyini müəyyənləşdirir

---

## 🧠 Əsas Bacarıq Sahələri

### 1. Django Model Yaratma

**Aktivasiya**: Yeni model yaratmaq lazım olduqda

**Standart Davranış**:
- `BaseModel`-dən miras al (UUID primary key + timestamps)
- `verbose_name` Azərbaycan dilində olmalıdır
- `TextChoices` enum-ları sinif daxilində təyin et
- `Meta.indexes` gərəkli field-lər üçün əlavə et
- `__str__` mənalı string qaytarmalıdır

```python
# Nümunə: Yeni model yaratma şablonu
import uuid
from django.db import models


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class YeniModel(BaseModel):
    class Status(models.TextChoices):
        ACTIVE   = 'active',   'Aktiv'
        INACTIVE = 'inactive', 'Deaktiv'

    # ... fields ...

    class Meta:
        db_table        = 'app_yenimodel'
        verbose_name    = 'Yeni Model'
        verbose_name_plural = 'Yeni Modellər'
        ordering        = ['-created_at']
        indexes         = [
            models.Index(fields=['status', 'created_at']),
        ]

    def __str__(self) -> str:
        return f"..."
```

---

### 2. Django View Yaratma (Class-Based)

**Aktivasiya**: View yaratmaq lazım olduqda

**Standart Davranış**:
- `LoginRequiredMixin` həmişə əlavə et
- Business logic-i `services.py`-a çıxar
- `select_related` / `prefetch_related` yaddaşda saxla
- Mesajları Azərbaycan dilində yaz
- HTMX sorğuları üçün ayrı `partial` template qaytarma yaz

```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from django.contrib import messages
from django.urls import reverse_lazy

from .models    import Lesson
from .forms     import LessonForm
from .services  import LessonService


class LessonListView(LoginRequiredMixin, ListView):
    model               = Lesson
    template_name       = 'bookings/lesson_list.html'
    context_object_name = 'lessons'
    paginate_by         = 20

    def get_queryset(self):
        return (
            Lesson.objects
            .select_related('student', 'course')
            .filter(student=self.request.user)
            .order_by('-scheduled_at')
        )

    def get_context_data(self, **kwargs) -> dict:
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Dərslərim'
        return ctx
```

---

### 3. Service Layer Bacarığı

**Aktivasiya**: Business logic yazılmalı olduqda

**Standart Davranış**:
- `@transaction.atomic` ilə data bütövlüyünü qoru
- Exception handling mütləq olmalıdır
- External API çağırışlarını ayrı service-ə çıxar
- Async əməliyyatlar üçün Celery task istifadə et

```python
from django.db import transaction
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class BookingService:

    @transaction.atomic
    def create_booking(self, student_id: str, slot_id: str) -> Optional['Booking']:
        try:
            # 1. Slot yoxla
            # 2. Booking yarat
            # 3. Zoom link əldə et
            # 4. Email bildirişi göndər (async)
            ...
        except Exception as exc:
            logger.error("Booking xətası: %s", exc, exc_info=True)
            return None
```

---

### 4. Django Form Bacarığı

**Aktivasiya**: Form yaratmaq lazım olduqda

**Standart Davranış**:
- `ModelForm` istifadə et
- Bootstrap 5 class-larını `widgets`-də əlavə et
- `labels` Azərbaycan dilindədir
- `clean_<field>` metodları ilə validasiya

```python
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone


class BookingForm(forms.ModelForm):
    class Meta:
        model   = Booking
        fields  = ['scheduled_at', 'topic', 'notes']
        widgets = {
            'scheduled_at': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
            'topic': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels  = {
            'scheduled_at': 'Tarix və Saat',
            'topic':        'Mövzu',
            'notes':        'Əlavə Qeydlər',
        }

    def clean_scheduled_at(self):
        dt = self.cleaned_data.get('scheduled_at')
        if dt and dt < timezone.now() + timezone.timedelta(hours=1):
            raise ValidationError('Dərs ən azı 1 saat irəlidən planlaşdırılmalıdır.')
        return dt
```

---

### 5. Celery Task Bacarığı

**Aktivasiya**: Async tapşırıq yaratmaq lazım olduqda

**Standart Davranış**:
- `@shared_task(bind=True, max_retries=3)` istifadə et
- `get_task_logger` ilə log aç
- `self.retry(exc=exc)` ilə xətaları yenilə
- Task-ları müvafiq `queue`-ya yönləndir

```python
from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    queue='notifications'
)
def send_lesson_reminder(self, booking_id: str) -> dict:
    try:
        from apps.bookings.models import Booking
        booking = Booking.objects.select_related('student').get(id=booking_id)
        # ... email göndər ...
        logger.info("Xatırlatma göndərildi: %s", booking_id)
        return {'success': True}
    except Exception as exc:
        logger.error("Xəta: %s", exc, exc_info=True)
        raise self.retry(exc=exc)
```

---

### 6. Django ORM Sorğu Optimizasiyası

**Aktivasiya**: Database sorğusu yazılmalı olduqda

**Qaydalar**:
- N+1 problemini önlə — `select_related` / `prefetch_related`
- `values()` / `values_list()` yalnız lazımi field-lər üçün
- Kütləvi əməliyyat üçün `bulk_create` / `bulk_update`
- `update()` ilə kütləvi yeniləmə — `save()` deyil
- `annotate()` ilə aggregasiya hesablamaları

```python
from django.db.models import Count, Sum, Avg, Q

# ✅ Düzgün — N+1 yoxdur
lessons = (
    Lesson.objects
    .select_related('student', 'course')
    .prefetch_related('materials')
    .filter(status=Lesson.Status.SCHEDULED)
    .annotate(material_count=Count('materials'))
    .order_by('scheduled_at')
)

# ✅ Kütləvi yeniləmə
Payment.objects.filter(status='pending', due_date__lt=today).update(
    status='overdue'
)

# ✅ Statistika
stats = Student.objects.annotate(
    total_lessons=Count('lessons'),
    total_paid=Sum('payments__amount'),
    avg_score=Avg('assessments__score')
)
```

---

### 7. GitHub API İnteqrasiyası Bacarığı

**Aktivasiya**: GitHub repo əməliyyatları lazım olduqda

**Davranış**:
- `PyGithub` kitabxanasından istifadə et
- Repo adı formatı: `{student-full-name}-{course-slug}`
- Private repo yarat, müəllim + tələbəyə giriş ver
- README.md avtomatik yaradılmalıdır

```python
from github import Github
from typing import Optional
import logging

logger = logging.getLogger(__name__)

REPO_NAME_FORMAT = "{student_slug}-{course_slug}"

DEFAULT_FOLDERS = ['lessons/', 'projects/', 'resources/']


def create_student_repository(
    student_full_name: str,
    course_slug: str,
    teacher_github: str,
    student_github: str,
    github_token: str
) -> Optional[str]:
    """
    Tələbə üçün private GitHub repository yaradır.
    Returns: repo URL və ya None (xəta olduqda)
    """
    try:
        g    = Github(github_token)
        org  = g.get_user()

        slug      = student_full_name.lower().replace(' ', '-')
        repo_name = REPO_NAME_FORMAT.format(
            student_slug=slug, course_slug=course_slug
        )

        repo = org.create_repo(
            name=repo_name,
            private=True,
            description=f"{student_full_name} — {course_slug} kursu",
            auto_init=True
        )

        # Tələbəyə collaborator əlavə et
        repo.add_to_collaborators(student_github, permission='push')

        # Əsas qovluq strukturunu yarat
        for folder in DEFAULT_FOLDERS:
            repo.create_file(
                path=f"{folder}.gitkeep",
                message=f"Init: {folder} qovluğu yaradıldı",
                content=""
            )

        logger.info("GitHub repo yaradıldı: %s", repo.html_url)
        return repo.html_url

    except Exception as exc:
        logger.error("GitHub repo xətası: %s", exc, exc_info=True)
        return None
```

---

### 8. HTMX + Alpine.js Frontend Bacarığı

**Aktivasiya**: Interactive komponent yaratmaq lazım olduqda

**Davranış**:
- HTMX atributları ilə server-side partial yenilə
- Alpine.js yalnız client-state üçün istifadə et
- Bootstrap 5 class-ları standart
- HTMX request-ləri üçün ayrı view yaz

```html
<!-- HTMX ilə canlı axtarış nümunəsi -->
<div x-data="{ query: '' }">
    <input
        type="text"
        x-model="query"
        class="form-control"
        placeholder="Tələbə axtar..."
        hx-get="{% url 'users:student-search' %}"
        hx-trigger="keyup changed delay:400ms"
        hx-target="#student-results"
        hx-include="[name='query']"
        name="query"
    >
</div>

<div id="student-results">
    {% include 'partials/student_list.html' %}
</div>
```

---

### 9. Payment (Ödəniş) Bacarığı

**Aktivasiya**: Ödəniş məntiqi yazılmalı olduqda

**Biznes Qaydaları**:
- Sabit qiymət: `25.00 AZN`
- Aylıq: `həftəlik_dərs_sayı × 4 × 25 AZN`
- Dərs əsaslı: hər dərsdən sonra `25 AZN`
- Stripe inteqrasiyası üçün `stripe` kitabxanası

```python
from decimal import Decimal

LESSON_PRICE = Decimal('25.00')          # Dəyişdirilməz!
CANCELLATION_HOURS = 24                  # Ləğvetmə üçün minimum saat


def calculate_monthly_payment(lessons_per_week: int) -> Decimal:
    """Aylıq ödəniş məbləğini hesablayır."""
    return lessons_per_week * 4 * LESSON_PRICE


def calculate_balance(total_paid: Decimal, completed_lessons: int) -> Decimal:
    """Tələbənin balansını hesablayır (aylıq modeldə)."""
    used = completed_lessons * LESSON_PRICE
    return total_paid - used
```

---

### 10. Notification (Bildiriş) Bacarığı

**Aktivasiya**: Email / SMS bildirişi lazım olduqda

**Davranış**:
- Email-ləri Celery task ilə async göndər
- Django templates ilə HTML email hazırla
- Xatırlatmalar: 24 saat əvvəl, 1 saat əvvəl
- Bildiriş tiplərini `enum` ilə idarə et

```python
class NotificationType(models.TextChoices):
    BOOKING_CONFIRMED  = 'booking_confirmed',  'Rezervasiya Təsdiqləndi'
    BOOKING_REMINDER   = 'booking_reminder',   'Dərs Xatırlatması'
    PAYMENT_DUE        = 'payment_due',        'Ödəniş Vaxtı'
    PAYMENT_RECEIVED   = 'payment_received',   'Ödəniş Alındı'
    GITHUB_REPO_READY  = 'github_repo_ready',  'GitHub Repo Hazırdır'
    LESSON_CANCELLED   = 'lesson_cancelled',   'Dərs Ləğv Edildi'
```

---

### 11. Test Yazma Bacarığı (pytest-django)

**Aktivasiya**: Test yazılmalı olduqda

**Standart Davranış**:
- `@pytest.mark.django_db` dekoratoru
- Fixture-ları `conftest.py`-da saxla
- Test adı: `test_<scenario>_<expected_result>`
- Factory Boy ilə test datası yarat
- Coverage hədəfi: **>80%**

```python
import pytest
from apps.bookings.services import BookingService
from apps.bookings.models   import Booking


@pytest.mark.django_db
class TestBookingService:

    def setup_method(self):
        self.service = BookingService()

    def test_create_booking_returns_confirmed_booking(
        self, student_user, available_slot
    ):
        booking = self.service.create_booking(
            student_id=str(student_user.id),
            slot_id=str(available_slot.id),
        )
        assert booking is not None
        assert booking.status == Booking.Status.CONFIRMED

    def test_create_booking_with_reserved_slot_returns_none(
        self, student_user, reserved_slot
    ):
        booking = self.service.create_booking(
            student_id=str(student_user.id),
            slot_id=str(reserved_slot.id),
        )
        assert booking is None
```

---

### 12. URL Konfiqurasiyası Bacarığı

**Aktivasiya**: URL pattern yaratmaq lazım olduqda

```python
from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    # Standard CRUD
    path('',                    views.BookingListView.as_view(),   name='list'),
    path('create/',             views.BookingCreateView.as_view(), name='create'),
    path('<uuid:pk>/',          views.BookingDetailView.as_view(), name='detail'),
    path('<uuid:pk>/cancel/',   views.BookingCancelView.as_view(), name='cancel'),

    # HTMX Endpoints
    path('htmx/slots/',         views.AvailableSlotsView.as_view(),  name='htmx-slots'),
    path('htmx/calendar/',      views.CalendarPartialView.as_view(), name='htmx-calendar'),
]
```

---

## 📋 Bacarıq Aktivasiya Cədvəli

| Ssenari                             | Aktivasiya Açar Sözü               | İstifadə Olunan Bacarıq     |
|-------------------------------------|------------------------------------|-----------------------------|
| Yeni model lazımdır                 | `model`, `models.Model`            | Django Model Yaratma        |
| Yeni view lazımdır                  | `view`, `ListView`, `CreateView`   | CBV Yaratma                 |
| Business logic                      | `service`, `transaction`           | Service Layer               |
| Form yaratmaq                       | `form`, `ModelForm`                | Form Bacarığı               |
| Async task                          | `task`, `celery`, `delay`          | Celery Task                 |
| DB sorğu                            | `objects.filter`, `queryset`       | ORM Optimizasiya            |
| GitHub əməliyyatı                   | `github`, `repo`, `repository`     | GitHub API İnteqrasiyası    |
| Frontend interaktivlik              | `htmx`, `alpine`, `partial`        | HTMX + Alpine.js            |
| Ödəniş hesablaması                  | `payment`, `25 AZN`, `stripe`      | Payment Bacarığı            |
| Email / SMS bildiriş                | `notification`, `email`, `remind`  | Notification Bacarığı       |
| Test yazmaq                         | `test`, `pytest`, `assert`         | Test Yazma                  |
| URL pattern                         | `urlpatterns`, `path`, `app_name`  | URL Konfiqurasiyası         |
