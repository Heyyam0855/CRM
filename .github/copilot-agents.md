# GitHub Copilot Agent-ləri — LMS Platformu

**AI Model**: Claude Sonnet 4.6  
**Framework**: Django 5.0+ | PostgreSQL | Redis | Celery | HTMX | Alpine.js

Bu sənəd LMS platformunun inkişafı üçün ixtisaslaşmış agent rollarını, onların məsuliyyətlərini və iş axınlarını müəyyənləşdirir. Hər agent Claude Sonnet 4.6-nı əsas AI model olaraq istifadə edir.

---

## 👥 Agent Siyahısı

| Agent | Rol | Əsas Məsuliyyət |
|-------|-----|-----------------|
| `@lms-architect` | **Super Agent** | Tam feature analizi + agent koordinasiyası |
| `@backend-architect` | Backend Memar | Django apps, models, views, services |
| `@frontend-dev` | Frontend İnkişafçı | Django Templates, HTMX, Alpine.js, Bootstrap |
| `@db-engineer` | Verilənlər Bazası Mühəndisi | PostgreSQL, Django ORM, migration-lar |
| `@security-expert` | Təhlükəsizlik Mütəxəssisi | Auth, permissions, data validation |
| `@integrations-dev` | İnteqrasiya İnkişafçısı | GitHub, YouTube, Zoom, Stripe API |
| `@payments-dev` | Ödəniş İnkişafçısı | Aylıq/Dərs əsaslı ödəniş sistemi |
| `@devops-engineer` | DevOps Mühəndisi | DigitalOcean, Docker, deployment |
| `@analytics-dev` | Analitika İnkişafçısı | Hesabatlar, dashboardlar, Chart.js |
| `@testing-specialist` | Test Mütəxəssisi | pytest-django, coverage, fixtures |
| `@notifications-dev` | Bildiriş İnkişafçısı | Email, SMS, real-time, Celery |
| `@performance-optimizer` | Performans Mütəxəssisi | Query optimallaşdırma, Redis keş, profiling |

---

## 🧠 @lms-architect — Super Agent (Koordinator)

### Məsuliyyətlər
- Mürəkkəb feature-ları analiz et, alt tapşırıqlara böl
- Doğru agent-i seç və tapşırığı yönləndir
- Agent-lər arası handoff-u idarə et
- LMS biznes qaydalarının düzgünlüyünü yoxla
- Tam feature delivery-ni koordinasiya et

### İstifadə Sahəsi
```
@lms-architect, tələbə qeydiyyat axınının tam feature-ını yarat:
- Qeydiyyat formu → müəllim təsdiqi → GitHub repo yaratma
→ Email bildiriş → tələbə dashboard-u
Hər addım üçün düzgün agent-i seç və iş bölüşdür.
```

### Agent Seçim Qaydası
```
Sual: "Hansı agent-i çağırmalıyam?"

├── Yeni Django app / model / view lazımdır?
│   └── @backend-architect
│
├── Frontend template / HTMX / Alpine.js lazımdır?
│   └── @frontend-dev
│
├── DB sorğusu yavaşdır / N+1 problemi var?
│   └── @db-engineer → @performance-optimizer
│
├── GitHub / YouTube / Google Meet API lazımdır?
│   └── @integrations-dev
│
├── 25 AZN ödəniş məntiqi lazımdır?
│   └── @payments-dev
│
├── Email / SMS / xatırlatma lazımdır?
│   └── @notifications-dev
│
├── Test yaz / coverage artır?
│   └── @testing-specialist
│
├── Deploy / CI-CD / Docker lazımdır?
│   └── @devops-engineer
│
├── Auth / permission / security review?
│   └── @security-expert
│
├── Dashboard / qrafik / hesabat?
│   └── @analytics-dev
│
└── Hamısı lazımdır (tam feature)?
    └── @lms-architect (koordinasiya + bölüşdür)
```

### LMS Feature Map (Tez Baxış)

```
Feature                          → Agentlər
────────────────────────────────────────────────────────
Tələbə qeydiyyatı                → @backend + @integrations + @notifications
Dərs rezervasiyası               → @backend + @frontend + @payments
Odəniş axını (aylıq/dərs-based)  → @payments + @notifications + @backend
GitHub repo yaratma              → @integrations + @backend
YouTube material əlavəsi         → @integrations + @frontend
Google Meet linki                → @integrations + @notifications
Dashboard analitikası            → @analytics + @db-engineer
Email xatırlatmaları             → @notifications + @devops
Deployment                       → @devops + @security
Test coverage                    → @testing + @backend
```

### Handoff Şablonu

```markdown
## @lms-architect Handoff Sənədi

**Feature**: [feature adı]
**Status**: [tamamlandı / davam edir]

### Tamamlanan İş:
- [ ] Model: `apps/{app}/models.py` → {ModelName}
- [ ] Service: `apps/{app}/services.py` → {ServiceName}
- [ ] View: `apps/{app}/views.py` → {ViewName}
- [ ] URL: `{namespace}:{url-name}`

### Növbəti Agent: @{agent-name}
**Tapşırıq**: ...
**Context**: ...
**Qayda**: LESSON_PRICE = 25 AZN, verbose_name AZ dilindədir
```

---

## 🏗️ @backend-architect — Backend Memar

### Məsuliyyətlər
- Django app strukturunu dizayn et
- Model şəmaları yarat (BaseModel-dən miras ilə)
- Class-Based Views (CBV) yaz
- Service layer dizayn et
- URL konfiqurasiyasını idarə et
- API endpoints-ləri planlaşdır

### İstifadə Sahəsi
```
@backend-architect, `courses` Django app-ını yarat:
- Course, Module, Lesson model-ləri (BaseModel-dən miras)
- CRUD üçün CBV-lər (LoginRequiredMixin + TeacherRequiredMixin)
- CourseService class-ı (business logic)
- URL-lər (`app_name = 'courses'`)
- Admin registration
Django 5.0 standartlarına uyğun ol.
```

### Qiymətlendirmə Kriteriyaları
- [ ] `BaseModel`-dən miras (`uuid pk`, `created_at`, `updated_at`)
- [ ] Azərbaycan dilindəki `verbose_name`-lər
- [ ] `TextChoices` enum-ları
- [ ] `select_related` / `prefetch_related` query optimizasiyası
- [ ] `@transaction.atomic` service metodlarında
- [ ] Type hints bütün metodlarda

### Şablon Prompt
```markdown
Kontekst:
- LMS platformu, 1-1 fərdi online tədris
- Tech: Django 5.0, Django ORM, PostgreSQL
- Standartlar: BaseModel miras, UUID pk, verbose_name AZ dilindədir

Task:
[app adı] Django app-ını yarat:
- Model-lər: [model adları və field-lər]
- Views: [CBV növləri]
- Service: [business logic metodları]
- URLs: [endpointlər]
- Admin: [admin konfiqurasiyası]

Lazımi import-lar, type hints, docstring-lər əlavə et.
```

---

## 🎨 @frontend-dev — Frontend İnkişafçı

### Məsuliyyətlər
- Django Templates yaz (Bootstrap 5.3+)
- HTMX partial templates yarat
- Alpine.js reaktiv komponentlər
- Form renderingi (crispy-forms)
- Responsive dizayn
- Dashboard widget-ləri

### İstifadə Sahəsi
```
@frontend-dev, dərs rezervasiya səhifəsini yarat:
- Kalenvar görünüşü (mövcud slotlar)
- HTMX ilə dinamik slot seçimi (server-rendered)
- Rezervasiya formu (Bootstrap 5 + crispy-forms)
- Partial template-lər (slot_list.html, booking_confirm.html)
- Alpine.js ilə seçilmiş slot state-i idarəsi
Dil Azərbaycan olsun.
```

### HTMX Standartları
```html
<!-- Partial template sorğusu -->
<div hx-get="{% url 'bookings:available-slots' %}"
     hx-target="#slots-container"
     hx-trigger="change from:#date-picker"
     hx-indicator="#loading-spinner">
    <div id="loading-spinner" class="htmx-indicator spinner-border"></div>
</div>

<!-- Form HTMX ilə göndər -->
<form hx-post="{% url 'bookings:create' %}"
      hx-target="#booking-result"
      hx-swap="innerHTML">
    {% csrf_token %}
    {{ form|crispy }}
    <button type="submit" class="btn btn-primary">Rezervasiya Et</button>
</form>
```

### Alpine.js Standartları
```html
<!-- Sadə state idarəsi -->
<div x-data="{ selectedSlot: null, showConfirm: false }">
    <button @click="selectedSlot = slot; showConfirm = true">Seç</button>
    
    <div x-show="showConfirm" x-transition>
        <p x-text="`Seçilmiş saat: ${selectedSlot?.time}`"></p>
        <button @click="showConfirm = false">İmtina</button>
    </div>
</div>
```

### Qiymətlendirmə Kriteriyaları
- [ ] `{% extends 'base.html' %}` strukturu
- [ ] `{% load static %}` hər template-də
- [ ] HTMX ilə partial template-lər
- [ ] Bootstrap 5 class-ları
- [ ] Azərbaycan dilindəki mətn
- [ ] Mobile-first dizayn

---

## 🗃️ @db-engineer — Verilənlər Bazası Mühəndisi

### Məsuliyyətlər
- Django ORM model dizaynı (BaseModel)
- Migration strategiyası
- Database indeksləri planlaşdır
- Query optimallaşdırma
- PostgreSQL-spesifik xüsusiyyətlər
- Connection pooling konfiqurasiyası

### İstifadə Sahəsi
```
@db-engineer, `payments` app üçün database şemasını optimallaşdır:
- Payment, Invoice, PaymentMethod model-ləri
- Aylıq abunə + dərs əsaslı ödəniş modelləri
- Borc izləmə məntiqini support edən indekslər
- Annotasiya ilə effektiv analytics sorğuları
PostgreSQL 15 xüsusiyyətlərindən istifadə et.
```

### ORM Optimallaşdırma Şablonu
```python
# @db-engineer - Bu sorğu üçün optimallaşdırma
# Tələb: Müəllim dashboard-u üçün aylıq statistika

from django.db.models import Count, Sum, Avg, Q
from django.db.models.functions import TruncMonth
from django.utils import timezone

def get_monthly_stats(year: int = None) -> list:
    """
    Aylıq dərs və ödəniş statistikasını qaytarır.
    Yalnız 1 sorğu istifadə edir (N+1 yoxdur).
    """
    year = year or timezone.now().year
    
    return (
        Lesson.objects
        .filter(
            scheduled_at__year=year,
            status=Lesson.Status.COMPLETED
        )
        .annotate(month=TruncMonth('scheduled_at'))
        .values('month')
        .annotate(
            total_lessons=Count('id'),
            total_revenue=Sum('price'),
            unique_students=Count('student', distinct=True),
            avg_price=Avg('price')
        )
        .order_by('month')
    )
```

### Qiymətlendirmə Kriteriyaları
- [ ] UUID primary key-lər
- [ ] Lazımlı `db_index=True` field-ləri
- [ ] `Meta.indexes` composite indekslər
- [ ] `select_related` / `prefetch_related` istifadəsi
- [ ] Bulk əməliyyatlar (bulk_create, bulk_update)
- [ ] `F()` expression-lar atomik yeniləmə üçün

---

## 🔐 @security-expert — Təhlükəsizlik Mütəxəssisi

### Məsuliyyətlər
- Authentication sistemi (JWT, 2FA)
- Permission müvafiqlik yoxlamaları
- Input validation və sanitizasiya
- CSRF, XSS, SQL injection qorunması
- Sensitive məlumat şifrələmə
- Audit log sistemi

### İstifadə Sahəsi
```
@security-expert, tələbə ödəniş API endpoint-lərini audit et:
- Payment method-larına giriş icazələri
- Stripe webhook imzasının yoxlanması
- Ödəniş məlumatı PII protection
- Rate limiting tətbiqi
- Audit log qeydlərinin lazımlılığı
Aşkar edilmiş problemlər üçün konkret Django kodu göstər.
```

### Permission Şablonları
```python
# @security-expert tərəfindən standart permission-lar

from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied


class TeacherRequiredMixin(UserPassesTestMixin):
    """Yalnız müəllim roluna icazə verir."""
    
    def test_func(self) -> bool:
        return (
            self.request.user.is_authenticated and
            self.request.user.role == 'teacher'
        )

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('users:login')
        raise PermissionDenied("Yalnız müəllimlər bu əməliyyatı icra edə bilər.")


class StudentOwnerMixin(UserPassesTestMixin):
    """Tələbə yalnız öz məlumatlarına daxil ola bilər."""
    
    def test_func(self) -> bool:
        if not self.request.user.is_authenticated:
            return False
        obj = self.get_object()
        return (
            obj.student == self.request.user or
            self.request.user.role == 'teacher'
        )


def verify_stripe_webhook(payload: bytes, sig_header: str) -> dict:
    """Stripe webhook imzasını yoxla."""
    import stripe
    from django.conf import settings
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
        return event
    except stripe.error.SignatureVerificationError:
        raise PermissionDenied("Etibarsız webhook imzası")
```

### Qiymətlendirmə Kriteriyaları
- [ ] `@login_required` / `LoginRequiredMixin` bütün protected view-larda
- [ ] CSRF token bütün POST form-larda
- [ ] User input-ların validation-ı (Django Forms)
- [ ] Sensitive data-nın loglanmaması
- [ ] Rate limiting tətbiqi
- [ ] Webhook signature yoxlaması

---

## 🔗 @integrations-dev — İnteqrasiya İnkişafçısı

### Məsuliyyətlər
- GitHub API (PyGithub kitabxanası)
- YouTube Data API v3
- Zoom / Google Meet API
- Google Calendar API
- Celery task-larında async inteqrasiyalar

### GitHub İnteqrasiyası
```
@integrations-dev, tələbə qeydiyyatı üçün GitHub repo yaratma axınını implement et:
- Tələbə adı + kurs slug-ından repo adı generasiyası
- Private repo + README.md strukturu (lessons/, projects/, resources/, recordings/)
- Müəllim + tələbə collaborator olaraq əlavə edilməsi
- Celery task-ı ilə async icra
- Xəta halında retry mexanizmi (max 3 dəfə)
PyGithub kitabxanasından istifadə et.
```

### GitHub Service Şablonu
```python
# @integrations-dev — apps/github_integration/services.py

from typing import Optional
from github import Github, GithubException
from celery import shared_task
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class GitHubService:
    """GitHub API inteqrasiyası."""

    def __init__(self):
        self.client = Github(settings.GITHUB_TOKEN)
        self.org = self.client.get_organization(settings.GITHUB_ORG)

    def create_student_repo(
        self,
        student_full_name: str,
        course_slug: str,
        student_github: Optional[str] = None
    ) -> Optional[str]:
        """
        Tələbə üçün private GitHub repository yaradır.
        
        Returns:
            Uğurlu olarsa repo URL-i, əks halda None
        """
        repo_name = self._generate_repo_name(student_full_name, course_slug)
        
        try:
            repo = self.org.create_repo(
                name=repo_name,
                private=True,
                description=f"{student_full_name} — {course_slug} kursu",
                auto_init=True
            )
            
            # Əsas struktur yarat
            self._create_initial_structure(repo, student_full_name, course_slug)
            
            # Müəllimi collaborator et
            repo.add_to_collaborators(settings.TEACHER_GITHUB_USERNAME, permission='maintain')
            
            # Tələbəni collaborator et (əgər GitHub adı varsa)
            if student_github:
                repo.add_to_collaborators(student_github, permission='push')
            
            logger.info(f"Repo yaradıldı: {repo.html_url}")
            return repo.html_url
            
        except GithubException as e:
            logger.error(f"GitHub repo yaratma xətası: {e}", exc_info=True)
            return None

    @staticmethod
    def _generate_repo_name(full_name: str, course_slug: str) -> str:
        """Repo adını generasiya edir: `ali-aliyev-python-course`"""
        name_slug = full_name.lower().replace(' ', '-')
        import re
        name_slug = re.sub(r'[^a-z0-9-]', '', name_slug)
        return f"{name_slug}-{course_slug}"

    def _create_initial_structure(self, repo, student_name: str, course: str):
        """Əsas qovluq strukturunu yaradır."""
        readme_content = f"""# {student_name} — {course} Kursu

## 📚 Kurs Məlumatları
- **Tələbə**: {student_name}
- **Kurs**: {course}
- **Başlama tarixi**: {__import__('datetime').date.today()}

## 📁 Struktur
- `lessons/` — Dərs materialları
- `projects/` — Tələbə layihələri  
- `resources/` — Əlavə resurslar
- `recordings/` — Dərs qeydlərinin linkləri

## 🎥 Dərs Videoları
Dərs videoları hər dərsin öz `README.md` faylında siyahılanacaq.
"""
        repo.update_file("README.md", "İlkin README yeniləndi", readme_content, 
                         repo.get_contents("README.md").sha)
        
        # Placeholder fayllar ilə qovluqlar yarat
        for folder in ['lessons', 'projects', 'resources', 'recordings']:
            repo.create_file(
                f"{folder}/.gitkeep",
                f"{folder}/ qovluğu yaradıldı",
                ""
            )


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def create_student_repo_async(
    self,
    student_id: str,
    course_id: str
) -> dict:
    """GitHub repo-nu async olaraq yaradır."""
    try:
        from apps.users.models import User
        from apps.courses.models import Course
        
        student = User.objects.get(id=student_id)
        course = Course.objects.get(id=course_id)
        
        service = GitHubService()
        repo_url = service.create_student_repo(
            student_full_name=student.get_full_name(),
            course_slug=course.slug,
            student_github=student.github_username
        )
        
        if repo_url:
            student.github_repo_url = repo_url
            student.save(update_fields=['github_repo_url'])
            return {'success': True, 'repo_url': repo_url}
        
        return {'success': False, 'error': 'Repo yaradıla bilmədi'}
        
    except Exception as exc:
        logger.error(f"Async repo yaratma xətası: {exc}", exc_info=True)
        raise self.retry(exc=exc)
```

### YouTube Service Şablonu
```python
# @integrations-dev — apps/youtube/services.py

from typing import Optional, dict
from googleapiclient.discovery import build
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class YouTubeService:
    """YouTube Data API v3 inteqrasiyası."""

    def __init__(self):
        self.youtube = build(
            'youtube', 'v3',
            developerKey=settings.YOUTUBE_API_KEY
        )

    def get_video_metadata(self, video_url: str) -> Optional[dict]:
        """
        YouTube video URL-dən metadata çıxarır.
        
        Returns:
            Video metadata dict-i və ya None
        """
        video_id = self._extract_video_id(video_url)
        if not video_id:
            return None
        
        try:
            response = self.youtube.videos().list(
                part='snippet,contentDetails,statistics',
                id=video_id
            ).execute()
            
            if not response['items']:
                return None
            
            item = response['items'][0]
            return {
                'video_id': video_id,
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'thumbnail': item['snippet']['thumbnails']['high']['url'],
                'duration': item['contentDetails']['duration'],
                'view_count': item['statistics'].get('viewCount', 0),
                'channel': item['snippet']['channelTitle'],
                'published_at': item['snippet']['publishedAt'],
                'embed_url': f"https://www.youtube.com/embed/{video_id}"
            }
            
        except Exception as e:
            logger.error(f"YouTube metadata xətası: {e}", exc_info=True)
            return None

    @staticmethod
    def _extract_video_id(url: str) -> Optional[str]:
        """YouTube URL-dən video ID çıxarır."""
        import re
        patterns = [
            r'(?:v=|/embed/|youtu\.be/)([a-zA-Z0-9_-]{11})',
            r'(?:shorts/)([a-zA-Z0-9_-]{11})'
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
```

### Qiymətlendirmə Kriteriyaları
- [ ] API key-lər environment variable-lardan okunur
- [ ] Xəta halında retry mexanizmi
- [ ] Celery task-larında async icra
- [ ] Xəta loglanması
- [ ] Rate limiting nəzərə alınıb

---

## 💳 @payments-dev — Ödəniş İnkişafçısı

### Məsuliyyətlər
- Aylıq abunə (recurring) sistemi
- Dərs əsaslı (pay-as-you-go) sistemi
- Stripe inteqrasiyası
- Faktura yaradılması
- Borc izləmə və xatırlatmalar
- Webhook handler-lar

### İstifadə Sahəsi
```
@payments-dev, aylıq abunə ödəniş modelini implement et:
- Aylıq məbləğ hesablaması: həftəlik dərs sayı × 4 × 25 AZN
- Hər ayın 1-i Stripe recurring charge
- Gecikmiş ödəniş xatırlatması (2, 5, 7. günlər)
- 10 gün gecikdikdə xidmət dayandırma
- Invoice yaradılması və email ilə göndərilmə
transaction.atomic() istifadə et.
```

### Ödəniş Service Şablonu
```python
# @payments-dev — apps/payments/services.py

from decimal import Decimal
from typing import Optional
from django.db import transaction
from django.utils import timezone


LESSON_PRICE = Decimal('25.00')  # Sabit qiymət — dəyişdirilməz!


class PaymentService:
    """Ödəniş business logic."""

    @staticmethod
    def calculate_monthly_amount(lessons_per_week: int) -> Decimal:
        """
        Aylıq ödəniş məbləğini hesablayır.
        
        Formula: həftəlik dərs sayı × 4 həftə × 25 AZN
        Nümunə: 2 dərs/həftə = 8 dərs/ay = 200 AZN
        """
        return Decimal(lessons_per_week) * 4 * LESSON_PRICE

    @transaction.atomic
    def process_lesson_payment(
        self,
        booking_id: str,
        payment_method_id: str
    ) -> Optional['Payment']:
        """
        Tamamlanmış dərs üçün ödəniş icra edir (dərs əsaslı model).
        
        Prosess:
        1. Booking-ü tap və yoxla
        2. Stripe charge yarat
        3. Payment record yarat
        4. Invoice yarat
        5. Email ilə qəbz göndər
        """
        from apps.bookings.models import Booking
        from .models import Payment
        
        booking = Booking.objects.select_for_update().get(
            id=booking_id,
            status=Booking.Status.COMPLETED
        )
        
        # Artıq ödənilməyib yoxla
        if Payment.objects.filter(booking=booking, status='paid').exists():
            raise ValueError("Bu dərs artıq ödənilib")
        
        # Stripe charge
        stripe_charge = self._create_stripe_charge(
            amount=LESSON_PRICE,
            payment_method_id=payment_method_id,
            description=f"Dərs: {booking.scheduled_at:%d.%m.%Y} — {booking.course.title}"
        )
        
        # Payment record
        payment = Payment.objects.create(
            booking=booking,
            student=booking.student,
            amount=LESSON_PRICE,
            payment_model=Payment.Model.PER_LESSON,
            stripe_charge_id=stripe_charge['id'],
            status=Payment.Status.PAID,
            paid_at=timezone.now()
        )
        
        # Invoice yarat (async)
        from .tasks import generate_invoice_async
        generate_invoice_async.delay(str(payment.id))
        
        return payment
```

---

## ⚡ @performance-optimizer — Performans Mütəxəssisi

### Məsuliyyətlər
- N+1 sorğu problemlərini aşkar et və düzəlt
- Redis keşləmə strategiyası
- Django Debug Toolbar ilə profiling
- Database indeks analizi
- Celery task performansı
- Response time optimallaşdırması

### İstifadə Sahəsi
```
@performance-optimizer, müəllim dashboard-unun yüklənməsi 800ms çəkir:
- Hansı sorğular yavaşdır? (django-debug-toolbar ilə)
- N+1 problemlərini düzəlt (select_related/prefetch_related)
- Redis ilə 1 saatlıq keş əlavə et
- Mağaza sorğularını annotate+aggregate ilə birləşdir
Hədəf: <100ms response time.
```

### Performans Optimallaşdırma Şablonu

```python
# @performance-optimizer — Keş dekoratoru
from django.core.cache import cache
from functools import wraps
import hashlib, json


def cache_result(key_prefix: str, ttl: int = 3600):
    """Method nəticəsini Redis-də keşlə."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Key generasiyası
            raw = f"{key_prefix}:{args}:{sorted(kwargs.items())}"
            key = hashlib.md5(raw.encode()).hexdigest()[:16]
            full_key = f"{key_prefix}:{key}"

            hit = cache.get(full_key)
            if hit is not None:
                return hit

            result = func(*args, **kwargs)
            cache.set(full_key, result, ttl)
            return result
        return wrapper
    return decorator


# @performance-optimizer — N+1 yoxlama utility
from django.test.utils import CaptureQueriesContext
from django.db import connection


def assert_max_queries(max_count: int):
    """Test-lərdə sorğu sayını yoxla."""
    return CaptureQueriesContext(connection)


# İstifadə:
# with assert_max_queries(3) as ctx:
#     result = service.get_dashboard_stats()
# assert len(ctx) <= 3, f"Çox sorğu: {len(ctx)}"
```

### Performans Checklist

```
✅ PERFORMANS YOXLAMA:
─────────────────────────────────────────────────────
□ Hər QuerySet-də select_related() var?
□ M2M field-lər üçün prefetch_related() var?
□ .count() deyil len() istifadə edilir?
□ Aggregasiya Python-da deyil DB-də edilir?
□ Keş TTL düzgündür? (dinamik: 60s, statik: 3600s)
□ Celery task-lar CPU-bound? → concurrent.futures
□ Template-lərdə DB sorğusu var? → context-ə əlavə et
□ Admin-də list_select_related=True var?
```

### Query Analysis

```python
# @performance-optimizer — Slow query analizi
import time
from django.db import connection


def get_slow_queries(threshold_ms: float = 50.0) -> list[dict]:
    """50ms-dən yavaş sorğuları qaytarır."""
    return [
        {
            'sql':  q['sql'][:200],
            'time': float(q['time']) * 1000,
        }
        for q in connection.queries
        if float(q['time']) * 1000 > threshold_ms
    ]


# Dashboard stats — optimallaşdırılmış (1 sorğu)
from django.db.models import Count, Sum, Avg
from django.db.models.functions import TruncMonth


def get_optimized_dashboard(teacher_id: str) -> dict:
    from apps.bookings.models import Lesson
    from apps.users.models import User

    # 1 sorğu ilə hamısını al
    stats = Lesson.objects.filter(
        course__teacher_id=teacher_id,
        status='completed',
    ).aggregate(
        total_lessons  = Count('id'),
        total_revenue  = Sum('price'),
        unique_students= Count('student', distinct=True),
        avg_price      = Avg('price'),
    )

    return stats
```

---

## 🚀 @devops-engineer — DevOps Mühəndisi

### Məsuliyyətlər
- DigitalOcean App Platform konfiqurasiyası
- Docker + Docker Compose setup
- GitHub Actions CI/CD
- Environment variable idarəsi
- Health check endpoint-ləri
- Production settings optimallaşdırması

### İstifadə Sahəsi
```
@devops-engineer, DigitalOcean App Platform üçün tam deployment konfiqurasiyasını yarat:
- .do/app.yaml (Django + PostgreSQL + Redis + Spaces)
- Gunicorn konfiqurasiyası (workers, timeout)
- collectstatic + migrate build steps
- Health check endpoint (/health/)
- Environment variables siyahısı
Frankfurt (fra) region, EUR valyutası üçün konfiqurasiya et.
```

### DigitalOcean App Spec Şablonu
```yaml
# @devops-engineer — .do/app.yaml
name: lms-platform
region: fra  # Frankfurt — Azərbaycan üçün ən yaxın

services:
  - name: django-app
    github:
      repo: your-username/lms-platform
      branch: main
      deploy_on_push: true
    
    build_command: |
      pip install -r requirements.txt
      python manage.py collectstatic --noinput
      python manage.py migrate --noinput
    
    run_command: |
      gunicorn config.wsgi:application \
        --bind :8000 \
        --workers 3 \
        --worker-class gthread \
        --threads 2 \
        --timeout 120 \
        --keep-alive 5 \
        --access-logfile - \
        --error-logfile -
    
    environment_slug: python
    instance_count: 1
    instance_size_slug: basic-xs
    
    http_port: 8000
    
    health_check:
      http_path: /health/
      initial_delay_seconds: 60
      period_seconds: 30
      timeout_seconds: 10
      failure_threshold: 3
    
    envs:
      - key: DJANGO_SETTINGS_MODULE
        value: config.settings.production
      - key: SECRET_KEY
        type: SECRET
        scope: RUN_AND_BUILD_TIME
      - key: DEBUG
        value: "False"
      - key: DATABASE_URL
        value: ${db.DATABASE_URL}
      - key: REDIS_URL
        value: ${redis.REDIS_URL}
      - key: SPACES_BUCKET_NAME
        value: lms-media
      - key: SPACES_ENDPOINT_URL
        value: https://fra1.digitaloceanspaces.com
      - key: ALLOWED_HOSTS
        value: ".ondigitalocean.app,yourdomain.com"

databases:
  - name: db
    engine: PG
    version: "15"
    production: true

  - name: redis
    engine: REDIS
    version: "7"
    production: true
```

### Health Check View
```python
# @devops-engineer — apps/core/views.py

from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache


def health_check(request):
    """
    DigitalOcean health check endpoint-i.
    Database, Redis və disk oxuma yoxlayır.
    """
    checks = {}
    
    # Database check
    try:
        connection.ensure_connection()
        checks['database'] = 'ok'
    except Exception as e:
        checks['database'] = f'error: {str(e)}'
    
    # Redis/Cache check
    try:
        cache.set('health_check', 'ok', 10)
        val = cache.get('health_check')
        checks['cache'] = 'ok' if val == 'ok' else 'error'
    except Exception as e:
        checks['cache'] = f'error: {str(e)}'
    
    all_ok = all(v == 'ok' for v in checks.values())
    status_code = 200 if all_ok else 503
    
    return JsonResponse({'status': 'ok' if all_ok else 'degraded', 'checks': checks},
                        status=status_code)
```

---

## 📊 @analytics-dev — Analitika İnkişafçısı

### Məsuliyyətlər
- Müəllim dashboard analitikası
- Tələbə progress izləmə
- Maliyyə hesabatları
- Chart.js qrafiklər
- Excel/PDF export
- KPI hesablamaları

### İstifadə Sahəsi
```
@analytics-dev, müəllim üçün aylıq gəlir dashboard-u yarat:
- Aylıq gəlir qrafiki (Chart.js bar chart): 25 AZN × dərs sayı
- Model üzrə breakdown: aylıq abunə vs dərs əsaslı
- Aktiv tələbə sayı
- Bu ayın gözlənilən gəliri (aylıq abunə üçün)
- Django ORM ilə effektiv aggregation sorğuları
- HTMX ilə dinamik tarix filtri
```

### Analytics Service Şablonu
```python
# @analytics-dev — apps/analytics/services.py

from decimal import Decimal
from django.db.models import Count, Sum, Avg, Q
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import timedelta


class TeacherAnalyticsService:
    """Müəllim analitika xidmətləri."""

    def get_dashboard_stats(self) -> dict:
        """Müəllim dashboard üçün əsas statistika."""
        today = timezone.now().date()
        month_start = today.replace(day=1)
        
        from apps.bookings.models import Lesson
        from apps.payments.models import Payment
        from apps.users.models import User
        
        # Bu ayın dərslər
        this_month_lessons = Lesson.objects.filter(
            scheduled_at__date__gte=month_start,
            status=Lesson.Status.COMPLETED
        )
        
        return {
            'this_month': {
                'lessons_count': this_month_lessons.count(),
                'revenue': this_month_lessons.aggregate(
                    total=Sum('price')
                )['total'] or Decimal('0'),
            },
            'active_students': User.objects.filter(
                role='student',
                status='active'
            ).count(),
            'today_bookings': Lesson.objects.filter(
                scheduled_at__date=today,
                status=Lesson.Status.SCHEDULED
            ).select_related('student').count(),
            'pending_payments': Payment.objects.filter(
                status='overdue'
            ).count(),
        }

    def get_monthly_revenue_chart(self, months: int = 12) -> list:
        """
        Son N ay üçün aylıq gəlir məlumatları (Chart.js üçün).
        
        Returns:
            [{'month': '2025-01', 'revenue': 1200, 'lessons': 48}, ...]
        """
        from apps.bookings.models import Lesson
        
        start_date = timezone.now() - timedelta(days=months * 30)
        
        return list(
            Lesson.objects
            .filter(
                scheduled_at__gte=start_date,
                status=Lesson.Status.COMPLETED
            )
            .annotate(month=TruncMonth('scheduled_at'))
            .values('month')
            .annotate(
                revenue=Sum('price'),
                lessons=Count('id'),
                students=Count('student', distinct=True)
            )
            .order_by('month')
        )
```

---

## 🧪 @testing-specialist — Test Mütəxəssisi

### Məsuliyyətlər
- pytest-django unit testlər
- Factory Boy fixtures
- Integration testlər
- Coverage >80% təmin etmə
- Edge case ssenariləri
- API test client-i

### İstifadə Sahəsi
```
@testing-specialist, BookingService üçün tam test suite yarat:
- Uğurlu rezervasiya yaratma
- Artıq reserved slot
- Keçmiş vaxt slotları
- Ödəniş modeli validasiyası (aylıq vs dərs əsaslı)
- Zoom linki generasiyası (mock)
- Email bildirişinin göndərilməsi (mock)
pytest-django + factory_boy + mock istifadə et, coverage >85%.
```

### Test Şablonu
```python
# @testing-specialist — tests/conftest.py

import pytest
from django.utils import timezone
from datetime import timedelta
import factory
from factory.django import DjangoModelFactory

from apps.users.models import User
from apps.bookings.models import AvailabilitySlot, Booking
from apps.courses.models import Course


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    
    email = factory.Sequence(lambda n: f'test{n}@example.com')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    role = 'student'


class CourseFactory(DjangoModelFactory):
    class Meta:
        model = Course
    
    title = factory.Sequence(lambda n: f'Test Kursu {n}')
    slug = factory.Sequence(lambda n: f'test-course-{n}')


class AvailabilitySlotFactory(DjangoModelFactory):
    class Meta:
        model = AvailabilitySlot
    
    start_time = factory.LazyFunction(
        lambda: timezone.now() + timedelta(hours=2)
    )
    is_reserved = False


@pytest.fixture
def student_user(db):
    return UserFactory(role='student')

@pytest.fixture
def teacher_user(db):
    return UserFactory(role='teacher')

@pytest.fixture
def available_slot(db):
    return AvailabilitySlotFactory()

@pytest.fixture
def reserved_slot(db):
    return AvailabilitySlotFactory(is_reserved=True)

@pytest.fixture
def past_slot(db):
    return AvailabilitySlotFactory(
        start_time=timezone.now() - timedelta(hours=1)
    )
```

---

## 📬 @notifications-dev — Bildiriş İnkişafçısı

### Məsuliyyətlər
- Email bildirişlər (SendGrid/Mailgun)
- SMS bildirişlər (Twilio)
- In-app real-time bildirişlər (Django Channels)
- Celery Beat scheduled task-lar
- Bildiriş şablonları (HTML email)
- Unsubscribe/preference idarəsi

### İstifadə Sahəsi
```
@notifications-dev, dərs xatırlatma sistemini implement et:
- 24 saat əvvəl email xatırlatması
- 1 saat əvvəl email + SMS xatırlatması
- Zoom linkini email-ə əlavə et
- Celery Beat ilə planlaşdırılmış task-lar
- Retry mexanizmi (3 dəfə, 60 saniyə arayla)
- HTML email template-i (Bootstrap dizaynı)
```

### Bildiriş Service Şablonu
```python
# @notifications-dev — apps/notifications/services.py

from typing import Optional
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class EmailService:
    """Email bildiriş xidməti."""

    def send_lesson_reminder(
        self,
        booking,
        hours_before: int
    ) -> bool:
        """
        Dərs xatırlatma emaili göndərir.
        
        Args:
            booking: Booking obyekti
            hours_before: Neçə saat əvvəl (24 və ya 1)
        """
        context = {
            'student_name': booking.student.get_full_name(),
            'lesson_time': booking.slot.start_time,
            'course_name': booking.course.title,
            'zoom_link': booking.zoom_link,
            'hours_before': hours_before,
        }
        
        subject = (
            f"🔔 Dərs xatırlatması: {hours_before} saat sonra"
            if hours_before > 1
            else "🔔 Dərs 1 saat sonra başlayır!"
        )
        
        html_content = render_to_string(
            'notifications/email/lesson_reminder.html',
            context
        )
        text_content = render_to_string(
            'notifications/email/lesson_reminder.txt',
            context
        )
        
        try:
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[booking.student.email]
            )
            email.attach_alternative(html_content, "text/html")
            email.send()
            
            logger.info(f"Xatırlatma emaili göndərildi: {booking.student.email}")
            return True
            
        except Exception as e:
            logger.error(f"Email göndərmə xətası: {e}", exc_info=True)
            return False
```

---

## 🔄 Agent İş Axını

### ⚡ Tez Seçim (1 dəqiqə)

```
Nə yazmaq istəyirsən?

"model yaz"          → @backend-architect
"template yaz"       → @frontend-dev
"sorğu optimize et"  → @performance-optimizer + @db-engineer
"payment sistemi"    → @payments-dev
"GitHub API"         → @integrations-dev
"email göndər"       → @notifications-dev
"test yaz"           → @testing-specialist
"deploy et"          → @devops-engineer
"security yoxla"     → @security-expert
"dashboard qrafik"   → @analytics-dev
"hamısı lazımdır"    → @lms-architect
```

### Yeni Feature Üçün Tam Prosess

```
1. @lms-architect      → Feature analizi + plan + agent bölüşdürməsi
        ↓
2. @backend-architect  → Model + Service (BaseModel, AZ verbose_name)
        ↓
3. @db-engineer        → İndekslər + migration + query optimallaşdırma
        ↓
4. @backend-architect  → CBV Views + URLs + Forms
        ↓
5. @integrations-dev   → GitHub/YouTube/Meet API (lazım olsa)
        ↓
6. @payments-dev       → 25 AZN ödəniş məntiqi (lazım olsa)
        ↓
7. @frontend-dev       → Bootstrap 5 + HTMX + Alpine.js templates
        ↓
8. @notifications-dev  → Celery task-lar + email/SMS (lazım olsa)
        ↓
9. @performance-optimizer → Keş + N+1 yoxla + profiling
        ↓
10. @security-expert   → Permission audit + input validation
        ↓
11. @testing-specialist→ pytest-django + factory_boy (>80% coverage)
        ↓
12. @devops-engineer   → GitHub Actions CI/CD + DigitalOcean deploy
```

### LMS Feature Ssenarilər

#### Ssenari A: Yeni tələbə qeydiyyatı
```
@backend-architect   → User model + StudentRegistrationService
@integrations-dev   → create_student_repo_async (Celery task)
@notifications-dev  → send_welcome_email + send_github_link
@payments-dev       → ilk ödəniş setup (aylıq/dərs seçimi)
@frontend-dev       → qeydiyyat formu + müəllim təsdiq paneli
@testing-specialist → tam registration axını testi
```

#### Ssenari B: Dərs rezervasiyası
```
@backend-architect   → AvailabilitySlot + Booking modellər + BookingService
@frontend-dev       → kalenvar HTMX UI + slot seçimi + confirm modal
@integrations-dev   → Google Meet link yaratma
@notifications-dev  → 24h + 1h xatırlatma Celery Beat task-ları
@payments-dev       → dərs əsaslı model: hər dərsdən sonra 25 AZN charge
@testing-specialist → BookingService + permission testlər
```

#### Ssenari C: Ödəniş sistemi
```
@payments-dev       → PaymentService (aylıq: *4*25, dərs: 25/dərs)
@integrations-dev   → Stripe webhook handler
@notifications-dev  → gecikmiş ödəniş xatırlatmaları (2/5/7-ci gün)
@db-engineer        → Payment model indeksləri + balance annotasiyası
@analytics-dev      → aylıq gəlir qrafiki (Chart.js)
@security-expert    → Stripe webhook signature yoxlaması
```

### Agent Handoff Protokolu

Bir agentdən digərinə keçərkən kontekst sənədi hazırla:

```markdown
## Agent Handoff: @backend-architect → @frontend-dev

### Tamamlanan İş:
- `bookings` app yaradıldı
- `Booking`, `AvailabilitySlot` model-ləri hazırdır
- `BookingService.create_booking()` metodu tamamandır
- URL: `bookings:create` (POST), `bookings:available-slots` (GET, HTMX)

### Frontend Task-ları:
1. Kalenvar görünüşü (`bookings/calendar.html`)
2. Slot seçimi HTMX partial-ı (`partials/slot_list.html`)
3. Rezervasiya formu (`bookings/booking_form.html`)
4. Təsdiq modal-ı (`partials/booking_confirm.html`)

### Context Data:
- View `available_slots` context-ə qaytarır: `{slots: QuerySet[AvailabilitySlot]}`
- View `create` form: `BookingCreateForm`

### Mövcud Model-lər:
```python
class AvailabilitySlot:
    start_time: datetime
    end_time: datetime
    is_reserved: bool
    lesson_type: str  # 'standard', 'trial', 'consultation'

class Booking:
    student: User
    slot: AvailabilitySlot
    zoom_link: str
    status: str  # 'confirmed', 'cancelled', 'completed'
```
```

---

*AI Model: Claude Sonnet 4.6 | Layihə: LMS Platform (1-1 fərdi online tədris)*
