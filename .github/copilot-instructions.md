# GitHub Copilot İstifadə Təlimatları — LMS Platformu

---

## 🚨 MƏCBURİ QAYDA — HƏR TAPŞIRIQDAN SONRA AUTO-COMMIT

**Bu qayda dəyişdirilməzdir. Hər prompt tamamlandıqdan sonra aşağıdakı addımlar MÜTLƏQdir:**

### Claude/Copilot hər işin sonunda bu əmrləri çalışdırmalıdır:

```powershell
# 1. Bütün dəyişiklikləri stage et
git add .

# 2. Azərbaycan dilində qısa commit mesajı yaz
#    Format: "<emoji> <nə edildi> (<fayl sayı> fayl) — dd.MM.yyyy HH:mm"
#    Nümunələr:
#    ✅ Tapşırıq tamamlandı (3 fayl) — 27.02.2026 14:30
#    🗃️ Model strukturu yeniləndi (2 fayl) — 27.02.2026 14:30
#    🔧 Servis məntiqi yeniləndi (1 fayl) — 27.02.2026 14:30
#    🎨 Template və UI yeniləndi (4 fayl) — 27.02.2026 14:30
#    🐍 Python kodu yeniləndi (2 fayl) — 27.02.2026 14:30
#    📝 Sənədlər yeniləndi (1 fayl) — 27.02.2026 14:30
#    🧪 Testlər əlavə edildi (3 fayl) — 27.02.2026 14:30
#    ⚙️ Konfiqurasiya yeniləndi (1 fayl) — 27.02.2026 14:30
git commit -m "<emoji> <nə edildi> (<N> fayl) — <tarix>"

# 3. GitHub-a push et
git push origin main
```

### Commit Mesajı Seçim Qaydası:
| Dəyişən fayllar           | Emoji | Mesaj nümunəsi                              |
|---------------------------|-------|---------------------------------------------|
| `models.py`               | 🗃️   | Model strukturu yeniləndi                   |
| `views.py`                | 👁️   | View-lar yeniləndi                          |
| `services.py`             | 🔧    | Servis məntiqi yeniləndi                   |
| `tasks.py`                | ⚡    | Celery task-lar yeniləndi                   |
| `tests/`, `test_*.py`     | 🧪    | Testlər əlavə edildi/yeniləndi              |
| `*.html` + `*.py`         | ✅    | Backend və frontend yeniləndi               |
| `*.html`                  | 🎨    | Template və UI yeniləndi                    |
| `*.md`                    | 📝    | Sənədlər yeniləndi                          |
| `.json`, `.yaml`, `.env`  | ⚙️   | Konfiqurasiya yeniləndi                     |
| Digər / qarışıq           | ✅    | Tapşırıq tamamlandı                        |

> **Not**: `.claude/hooks/auto-commit.ps1` skripti Claude Code `Stop` hook-u vasitəsilə avtomatik işə düşür.  
> Manuel commit etmədən əvvəl dəyişiklik olmadığını yoxla: `git status`

---

## 🤖 AI Model Məlumatı
- **Əsas AI Model**: Claude Sonnet 4.6 (arxitektura, code review, debugging)
- **Kod Yaratma**: GitHub Copilot (real-time completion, boilerplate)
- **Model Versiyası**: Claude Sonnet 4.6 — Əlavə izahat tələb edən hər sorğuda bu modeldən istifadə et

---

## 📌 Layihə Haqqında

Bu **LMS (Learning Management System)** platformu tək müəllim tərəfindən çoxlu sayda tələbənin **fərdi online tədris** formatında (1-1) idarə edilməsi üçündür.

### Əsas Xüsusiyyətlər:
- Yalnız fərdi dərslər (1-1 format)
- Online video tədris (Zoom / Google Meet)
- Sabit qiymət: **25 AZN / dərs**
- İki ödəniş modeli: **Aylıq abunə** və **Dərs əsaslı (pay-as-you-go)**
- Hər tələbə üçün avtomatik **GitHub repository** yaradılması
- YouTube linklər ilə dərs videoları
- Calendly tipli dərs təyinatı sistemi

---

## 🏗️ Texniki Arxitektura

```
Arxitektura:    Django Fullstack Monolithic
Backend:        Django 5.0+ (Python 3.11+)
Database:       PostgreSQL 15+ (Django ORM)
Cache:          Redis 7+
Queue:          Celery + Celery Beat
Real-time:      Django Channels (WebSocket)
Frontend:       Django Templates + Bootstrap 5.3+ + HTMX + Alpine.js
Storage:        DigitalOcean Spaces (S3-compatible)
Deployment:     DigitalOcean App Platform / Railway
```

---

## 📁 Layihə Strukturu

```
lms_platform/
├── manage.py
├── config/
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── apps/
│   ├── users/              # İstifadəçi idarəetməsi
│   ├── courses/            # Kurs idarəetməsi
│   ├── bookings/           # Dərs təyinatı sistemi
│   ├── payments/           # Ödəniş sistemi
│   ├── github_integration/ # GitHub API inteqrasiyası
│   ├── youtube/            # YouTube API inteqrasiyası
│   ├── video_conferencing/ # Zoom/Meet inteqrasiyası
│   ├── notifications/      # Bildiriş sistemi
│   ├── support/            # Dəstək ticket sistemi
│   ├── analytics/          # Analitika
│   └── assessments/        # Qiymətləndirmə
│
├── templates/
│   ├── base.html
│   ├── auth/
│   ├── dashboard/
│   ├── courses/
│   ├── bookings/
│   ├── payments/
│   └── partials/           # HTMX partial templates
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
└── core/
    ├── utils.py
    ├── mixins.py
    ├── permissions.py
    └── validators.py
```

---

## 🐍 Python / Django Kod Standartları

### PEP 8 Qaydaları
- Sətir uzunluğu: **maksimum 88 simvol** (Black formatter)
- İdent: **4 boşluq** (tab istifadə etmə)
- Funksiya adları: `snake_case`
- Sinif adları: `PascalCase`
- Sabit dəyərlər: `UPPER_SNAKE_CASE`
- Private metodlar: `_single_underscore` prefiksi

### Import Sırası (isort)
```python
# 1. Standart kitabxana
import os
import uuid
from datetime import datetime, timedelta
from typing import Optional

# 2. Üçüncü tərəf
import stripe
from celery import shared_task
from django.contrib.auth import get_user_model

# 3. Lokal
from apps.payments.models import Payment
from core.utils import generate_invoice_number
```

### Type Hints — Məcburi
```python
from typing import Optional, List, Dict, Any, Tuple

def create_student_repository(
    student: User,
    course: Course,
    teacher_github: str
) -> Optional[str]:
    """
    GitHub-da tələbə üçün private repository yaradır.
    
    Args:
        student: Tələbə obyekti
        course: Kurs obyekti
        teacher_github: Müəllimin GitHub istifadəçi adı
    
    Returns:
        Uğurlu olarsa repo URL-i, əks halda None
    """
    ...
```

---

## 🗃️ Django Model Standartları

### Model Şablonu
```python
import uuid
from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    """Bütün modellər üçün əsas sinif."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Lesson(BaseModel):
    """Dərs modeli."""
    
    class Status(models.TextChoices):
        SCHEDULED = 'scheduled', 'Planlaşdırılıb'
        COMPLETED = 'completed', 'Tamamlandı'
        CANCELLED = 'cancelled', 'Ləğv edildi'
        NO_SHOW = 'no_show', 'Görünmədi'

    student = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='Tələbə'
    )
    course = models.ForeignKey(
        'courses.Course',
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='Kurs'
    )
    scheduled_at = models.DateTimeField(verbose_name='Planlaşdırılma tarixi')
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SCHEDULED,
        verbose_name='Status'
    )
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=25.00,
        verbose_name='Qiymət (AZN)'
    )
    zoom_link = models.URLField(blank=True, verbose_name='Zoom/Meet linki')
    recording_url = models.URLField(blank=True, verbose_name='Recording URL')
    notes = models.TextField(blank=True, verbose_name='Qeydlər')

    class Meta:
        db_table = 'bookings_lesson'
        verbose_name = 'Dərs'
        verbose_name_plural = 'Dərslər'
        ordering = ['-scheduled_at']
        indexes = [
            models.Index(fields=['student', 'scheduled_at']),
            models.Index(fields=['status', 'scheduled_at']),
        ]

    def __str__(self) -> str:
        return f"{self.student.get_full_name()} — {self.scheduled_at:%d.%m.%Y %H:%M}"
```

### Model Qaydaları
- Hər model `BaseModel`-dən miras almalıdır (UUID primary key + timestamps)
- `verbose_name` mütləq Azərbaycan dilində olmalıdır
- `TextChoices` enum-lar sinif daxilindəki `class` ilə təyin edilməlidir
- Sıralamanı `Meta.ordering`-də göstər
- Gərəkli field-lər üçün `indexes` əlavə et
- `__str__` metodu həmişə mənalı string qaytarmalıdır

---

## 👁️ Django View Standartları (Class-Based Views)

### CBV Şablonu
```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy

from .models import Lesson
from .forms import LessonCreateForm
from .services import LessonService


class LessonListView(LoginRequiredMixin, ListView):
    """Tələbənin dərslərinin siyahısı."""
    
    model = Lesson
    template_name = 'bookings/lesson_list.html'
    context_object_name = 'lessons'
    paginate_by = 20

    def get_queryset(self):
        return (
            Lesson.objects
            .select_related('student', 'course')
            .filter(student=self.request.user)
            .order_by('-scheduled_at')
        )

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Dərslərim'
        return context


class LessonCreateView(LoginRequiredMixin, CreateView):
    """Yeni dərs yaratma."""
    
    model = Lesson
    form_class = LessonCreateForm
    template_name = 'bookings/lesson_form.html'
    success_url = reverse_lazy('bookings:lesson-list')

    def form_valid(self, form):
        lesson = form.save(commit=False)
        lesson.student = self.request.user
        lesson_service = LessonService()
        result = lesson_service.create_with_zoom_link(lesson)
        if result:
            messages.success(self.request, 'Dərs uğurla yaradıldı!')
        return super().form_valid(form)
```

### View Qaydaları
- Həmişə `LoginRequiredMixin` istifadə et
- Business logic-i view-dan `services.py`-a çıxar
- `select_related` və `prefetch_related` ilə query optimizasiya et
- Mesajları Azərbaycan dilində yaz
- HTMX sorğuları üçün partial template qaytarma mexanizmi əlavə et

---

## 📋 Django Forms Standartları

```python
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Booking


class BookingCreateForm(forms.ModelForm):
    """Dərs rezervasiyası formu."""
    
    class Meta:
        model = Booking
        fields = ['lesson_type', 'scheduled_at', 'topic', 'notes']
        widgets = {
            'scheduled_at': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
            'topic': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'lesson_type': 'Dərs növü',
            'scheduled_at': 'Tarix və saat',
            'topic': 'Mövzu',
            'notes': 'Əlavə qeydlər',
        }

    def clean_scheduled_at(self):
        scheduled_at = self.cleaned_data.get('scheduled_at')
        if scheduled_at and scheduled_at < timezone.now() + timezone.timedelta(hours=1):
            raise ValidationError('Dərs ən azı 1 saat irəlidən planlaşdırılmalıdır.')
        return scheduled_at
```

---

## 🔧 Service Layer Standartları

```python
from typing import Optional
from django.db import transaction
from django.utils import timezone

from apps.notifications.services import NotificationService
from apps.video_conferencing.services import ZoomService
from .models import Booking


class BookingService:
    """Dərs rezervasiyası üçün business logic."""

    def __init__(self):
        self.notification_service = NotificationService()
        self.zoom_service = ZoomService()

    @transaction.atomic
    def create_booking(
        self,
        student_id: str,
        slot_id: str,
        lesson_type: str,
        topic: str = ''
    ) -> Optional[Booking]:
        """
        Yeni dərs rezervasiyası yaradır.
        
        Prosess:
        1. Slot mövcudluğunu yoxla
        2. Booking yarat
        3. Zoom linki əldə et
        4. Email bildirişi göndər
        5. Google Calendar-a əlavə et
        """
        try:
            # Slot mövcudluğunu yoxla
            slot = self._get_available_slot(slot_id)
            if not slot:
                return None

            # Booking yarat
            booking = Booking.objects.create(
                student_id=student_id,
                slot=slot,
                lesson_type=lesson_type,
                topic=topic,
                status=Booking.Status.CONFIRMED
            )

            # Slot-u reserved et
            slot.is_reserved = True
            slot.save(update_fields=['is_reserved'])

            # Zoom linki yarat
            zoom_link = self.zoom_service.create_meeting(
                topic=f"Dərs: {topic or 'LMS Dərsi'}",
                start_time=slot.start_time,
                duration=60
            )
            if zoom_link:
                booking.zoom_link = zoom_link
                booking.save(update_fields=['zoom_link'])

            # Email bildirişi göndər (async)
            self.notification_service.send_booking_confirmation.delay(booking.id)

            return booking

        except Exception as e:
            # Xəta loq et, None qaytar
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Booking yaratma xətası: {e}", exc_info=True)
            return None

    def _get_available_slot(self, slot_id: str):
        """Mövcud sloту yoxla və qaytar."""
        from apps.bookings.models import AvailabilitySlot
        try:
            return AvailabilitySlot.objects.select_for_update().get(
                id=slot_id,
                is_reserved=False,
                start_time__gt=timezone.now()
            )
        except AvailabilitySlot.DoesNotExist:
            return None
```

### Service Qaydaları
- Hər service sinif bir məntiqi sahəni əhatə etməlidir
- **`@transaction.atomic`** ilə data bütövlüyünü qoruyun
- Exception handling mütləq olmalıdır
- External API çağırışları ayrı service-lərdə tutulmalıdır
- Async əməliyyatlar üçün Celery task-ları istifadə edin

---

## 🎨 Django Templates + HTMX Standartları

### Base Template Strukturu
```html
{# templates/base.html #}
<!DOCTYPE html>
<html lang="az">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}LMS Platform{% endblock %}</title>
    {% load static %}
    <link rel="stylesheet" href="{% static 'css/main.css' %}">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
</head>
<body x-data="{ sidebarOpen: true }">
    {% include 'partials/navbar.html' %}
    {% include 'partials/sidebar.html' %}
    
    <main>
        {% if messages %}
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }}">{{ message }}</div>
            {% endfor %}
        {% endif %}
        
        {% block content %}{% endblock %}
    </main>
    
    <script src="https://unpkg.com/htmx.org@1.9.0"></script>
    <script src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js" defer></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

### HTMX Partial Template Nümunəsi
```html
{# templates/partials/lesson_card.html #}
<div class="card lesson-card"
     hx-get="{% url 'bookings:lesson-detail' lesson.pk %}"
     hx-target="#lesson-detail-modal"
     hx-trigger="click">
    <div class="card-body">
        <h5 class="card-title">{{ lesson.scheduled_at|date:"d M Y, H:i" }}</h5>
        <p class="card-text">{{ lesson.course.title }}</p>
        <span class="badge bg-{{ lesson.status|status_badge_color }}">
            {{ lesson.get_status_display }}
        </span>
        <span class="price-tag">25 AZN</span>
    </div>
</div>
```

### Template Qaydaları
- Şablonlar Azərbaycan dilindəki mətn içərəyin istifadə etməlidir
- HTMX atributları partial template-ləri hədəf almalıdır
- Alpine.js yalnız client-side state üçün istifadə edin
- Bootstrap 5 class-larından istifadə edin (custom CSS minimuma endirin)
- `{% load static %}` hər template-də yüklənməlidir

---

## 🔐 Autentifikasiya və İcazə Standartları

```python
# core/permissions.py
from django.contrib.auth.mixins import UserPassesTestMixin


class TeacherRequiredMixin(UserPassesTestMixin):
    """Yalnız müəllim roluna icazə verir."""
    
    def test_func(self) -> bool:
        return self.request.user.is_authenticated and self.request.user.role == 'teacher'

    def handle_no_permission(self):
        from django.shortcuts import redirect
        return redirect('users:login')


class StudentOwnerMixin(UserPassesTestMixin):
    """Tələbə yalnız öz məlumatlarına daxil ola bilər."""
    
    def test_func(self) -> bool:
        if not self.request.user.is_authenticated:
            return False
        obj = self.get_object()
        return obj.student == self.request.user or self.request.user.role == 'teacher'
```

---

## 📊 Django ORM Optimallaşdırma Qaydaları

```python
# ✅ Düzgün — N+1 problemi yoxdur
lessons = (
    Lesson.objects
    .select_related('student', 'course', 'course__category')
    .prefetch_related('materials', 'assessments')
    .filter(status=Lesson.Status.SCHEDULED)
    .order_by('scheduled_at')
)

# ❌ Yanlış — N+1 problemi
lessons = Lesson.objects.filter(status='scheduled')
for lesson in lessons:
    print(lesson.student.full_name)  # Hər iterasiyada ayrı sorğu!

# ✅ Yalnız lazımlı field-ləri seç
payments = Payment.objects.values('id', 'amount', 'status', 'created_at')

# ✅ Bulk əməliyyatlar
Payment.objects.filter(status='pending').update(
    status='overdue',
    updated_at=timezone.now()
)

# ✅ Annotation istifadə et
from django.db.models import Count, Sum, Avg
stats = Student.objects.annotate(
    total_lessons=Count('lessons'),
    total_paid=Sum('payments__amount'),
    avg_score=Avg('assessments__score')
)
```

---

## 📦 Celery Task Standartları

```python
# apps/notifications/tasks.py
from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    queue='notifications'
)
def send_lesson_reminder(self, booking_id: str, hours_before: int = 24) -> dict:
    """
    Dərs xatırlatma emaili göndərir.
    
    Args:
        booking_id: Rezervasiya ID-si
        hours_before: Neçə saat əvvəl xatırlatma
    
    Returns:
        Nəticə dict-i
    """
    try:
        from apps.bookings.models import Booking
        from .services import EmailService
        
        booking = Booking.objects.select_related(
            'student', 'slot'
        ).get(id=booking_id)
        
        email_service = EmailService()
        success = email_service.send_reminder(booking, hours_before)
        
        logger.info(f"Xatırlatma göndərildi: booking={booking_id}, hours={hours_before}")
        return {'success': success, 'booking_id': booking_id}

    except Booking.DoesNotExist:
        logger.warning(f"Booking tapılmadı: {booking_id}")
        return {'success': False, 'error': 'Booking tapılmadı'}
    except Exception as exc:
        logger.error(f"Xatırlatma xətası: {exc}", exc_info=True)
        raise self.retry(exc=exc)
```

---

## 🧪 Test Standartları (pytest-django)

```python
# tests/test_booking_service.py
import pytest
from django.utils import timezone
from datetime import timedelta

from apps.bookings.services import BookingService
from apps.bookings.models import Booking


@pytest.mark.django_db
class TestBookingService:
    """BookingService üçün testlər."""

    def setup_method(self):
        self.service = BookingService()

    def test_create_booking_success(self, student_user, available_slot):
        """Uğurlu rezervasiya yaratma."""
        booking = self.service.create_booking(
            student_id=str(student_user.id),
            slot_id=str(available_slot.id),
            lesson_type='standard',
            topic='Python Əsasları'
        )
        
        assert booking is not None
        assert booking.status == Booking.Status.CONFIRMED
        assert booking.student == student_user

    def test_create_booking_unavailable_slot(self, student_user, reserved_slot):
        """Mövcud olmayan slot üçün rezervasiya."""
        booking = self.service.create_booking(
            student_id=str(student_user.id),
            slot_id=str(reserved_slot.id),
            lesson_type='standard'
        )
        
        assert booking is None

    def test_create_booking_past_time(self, student_user, past_slot):
        """Keçmiş vaxt üçün rezervasiya."""
        booking = self.service.create_booking(
            student_id=str(student_user.id),
            slot_id=str(past_slot.id),
            lesson_type='standard'
        )
        
        assert booking is None
```

### Test Qaydaları
- Hər app üçün `tests/` qovluğu yarat
- Fixture-ları `conftest.py`-da saxla
- Test adları mənalı olmalıdır: `test_<scenario>_<expected>`
- Hər test bir şeyi yoxlamalıdır
- API testləri üçün `APIClient` istifadə et
- Coverage hədəfi: **>80%**

---

## 🌐 URL Konfiqurasyonu Standartları

```python
# apps/bookings/urls.py
from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.BookingListView.as_view(), name='list'),
    path('create/', views.BookingCreateView.as_view(), name='create'),
    path('<uuid:pk>/', views.BookingDetailView.as_view(), name='detail'),
    path('<uuid:pk>/cancel/', views.BookingCancelView.as_view(), name='cancel'),
    
    # HTMX endpoints
    path('slots/', views.AvailableSlotsView.as_view(), name='available-slots'),
    path('htmx/calendar/', views.CalendarPartialView.as_view(), name='htmx-calendar'),
]
```

---

## 📝 Logging Standartları

```python
import logging

logger = logging.getLogger(__name__)

# İstifadə nümunələri:
logger.debug("Debug məlumatı: %s", data)           # Development
logger.info("Rezervasiya yaradıldı: %s", booking)  # Normal axış
logger.warning("Gecikmiş ödəniş: %s", payment)     # Diqqət
logger.error("Xəta baş verdi:", exc_info=True)      # Xəta
logger.critical("Kritik sistem xətası!")             # Kritik
```

---

## ⚠️ Copilot İstifadə Qaydaları

### Copilot-dan Gözlənilənlər:
- ✅ Django models, views, forms, serializers yaratma
- ✅ CRUD əməliyyatları tamamlama
- ✅ Standard pattern implementasiyaları
- ✅ Test yaratma
- ✅ Django ORM sorğuları
- ✅ HTMX + Alpine.js template-ləri

### Claude Sonnet 4.6-dan Gözlənilənlər:
- ✅ Arxitektura qərarları
- ✅ Mürəkkəb business logic dizaynı
- ✅ Security review
- ✅ Performance optimallaşdırma
- ✅ Debugging mürəkkəb xətalar
- ✅ Integration planlaması

### Əsas Qaydalar:
1. **Hər generasiya edilmiş kodu oxu** — blindly accept etmə
2. **Azərbaycan dilindəki verbose_name-ləri yoxla**
3. **Security-critical kod üçün həmişə Claude review tələb et**
4. **Test-ləri həmişə run et** qəbul etməzdən əvvəl
5. **Layihə konvensiyalarına uyğunlaşdır** — auto-suggestion-ları kor-koranə qəbul etmə

---

## 🔑 Mühüm Biznes Qaydaları (Kod Yazarkən Nəzərə Al)

```python
# Sabit qiymət
LESSON_PRICE_AZN = 25.00  # Dəyişdirilməz!

# Ödəniş modelləri
class PaymentModel:
    MONTHLY = 'monthly'        # Aylıq abunə
    PER_LESSON = 'per_lesson'  # Dərs əsaslı

# Aylıq ödəniş hesablaması
def calculate_monthly_payment(lessons_per_week: int) -> float:
    return lessons_per_week * 4 * LESSON_PRICE_AZN

# Dərs statusları
LESSON_CANCELLATION_HOURS = 24  # Ləğvetmə üçün minimum saat

# GitHub repo adı formatı
def get_repo_name(student_full_name: str, course_slug: str) -> str:
    name_slug = student_full_name.lower().replace(' ', '-')
    return f"{name_slug}-{course_slug}"
```

---

*Bu sənəd GitHub Copilot-ın layihənin kontekstini başa düşməsi üçün hazırlanıb.*
*AI Model: Claude Sonnet 4.6 | Framework: Django 5.0+ | Dil: Azərbaycan*
