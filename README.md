# LMS Platform — Fərdi Online Tədris İdarəetmə Sistemi

> **Tək müəllim + çoxlu tələbə** modeli ilə 1-1 fərdi online tədris platforması.  
> **AI Model**: Claude Sonnet 4.6 | **Framework**: Django 5.0+ | **Dil**: Azərbaycan

---

## Layihə Haqqında

Bu LMS (Learning Management System) platformu tək müəllimin çoxlu sayda tələbəni **fərdi online format** (1-1) ilə effektiv idarə etməsi üçün hazırlanıb. Sistem bütün tədris prosesini — rezervasiyadan ödənişə, GitHub repo yaradılmasından analitikaya qədər — avtomatlaşdırır.

### Biznes Modelinin Əsas Xüsusiyyətləri

| Parametr | Dəyər |
|---|---|
| Tədris növü | Yalnız 1-1 fərdi dərslər |
| Tədris forması | Online (Google Meet) |
| Dərs qiyməti | **25 AZN / dərs (SABİT)** |
| Ödəniş Model 1 | Aylıq abunə (həftəlik dərs × 4 × 25 AZN) |
| Ödəniş Model 2 | Dərs əsaslı (pay-as-you-go) |
| Müəllim sayı | 1 (tək müəllim sistemi) |

---

## Texniki Arxitektura

```
Arxitektura:    Django Fullstack Monolithic
Backend:        Django 5.0+ (Python 3.11+)
Database:       PostgreSQL 15+ (Django ORM)
Cache:          Redis 7+
Queue:          Celery + Celery Beat
Real-time:      Django Channels (WebSocket)
Frontend:       Django Templates + Bootstrap 5.3 + HTMX + Alpine.js
Storage:        DigitalOcean Spaces (S3-compatible)
Deployment:     DigitalOcean App Platform / Railway
```

---

## Layihə Strukturu

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
│   ├── courses/            # Kurs + material idarəsi
│   ├── bookings/           # Dərs rezervasiyası (Calendly tipli)
│   ├── payments/           # Aylıq/dərs ödəniş sistemi
│   ├── github_integration/ # GitHub API — tələbə repo-su
│   ├── youtube/            # YouTube Data API v3
│   ├── video_conferencing/ # Google Meet API
│   ├── notifications/      # Email/SMS/real-time bildirişlər
│   ├── support/            # Dəstək ticket sistemi
│   ├── analytics/          # Dashboard analitikası
│   └── assessments/        # Qiymətləndirmə sistemi
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

## Əsas Funksionallıqlar

### 1. İstifadəçi İdarəetməsi (`apps/users/`)
- **Müəllim**: Tam sistem nəzarəti, bütün tələbə məlumatlarına giriş
- **Tələbə**: Fərdi profil, kurslara giriş, dərs rezervasiyası
- Qeydiyyat → Müəllim təsdiqi → GitHub repo yaratma → Email bildiriş axını
- İki faktorlu autentifikasiya (2FA)
- Social login dəstəyi (opsional)

### 2. Kurs İdarəetməsi (`apps/courses/`)
- Kurs, Modul, Dərs hierarxiyası
- YouTube video linklərinin avtomatik metadata çəkilməsi
- GitHub inteqrasiyası ilə material sync
- Drag & drop sıralama, versiya idarəetməsi
- PDF, kod nümunələri, rich text dəstəyi

### 3. Dərs Rezervasiyası (`apps/bookings/`)
- Calendly tipli slot seçim sistemi
- Real-time mövcud saatların göstərilməsi
- Avtomatik Google Meet link generasiyası
- 24 saat + 1 saat əvvəl xatırlatma (Celery tasks)
- Ləğvetmə qaydaları (minimum 24 saat əvvəl)

### 4. Ödəniş Sistemi (`apps/payments/`)
- **Model 1 — Aylıq**: həftəlik_dərs × 4 × 25 AZN (prepaid)
- **Model 2 — Dərs əsaslı**: Hər dərsdən sonra 25 AZN (24 saat limit)
- Stripe inteqrasiyası (beynəlxalq kartlar)
- Lokal ödəniş sistemləri (e-Manat, Milliköçürmə)
- Avtomatik faktura generasiyası (PDF)
- Gecikmiş ödəniş — növbəti dərs bloklanması

### 5. GitHub İnteqrasiyası (`apps/github_integration/`)
- Tələbə təsdiqlənəndə avtomatik **private repo** yaradılması
- Repo adı formatı: `{student-ad-soyad}-{kurs-slug}`
- Default qovluqlar: `lessons/`, `projects/`, `resources/`
- README.md avtomatik yaradılması (tələbə məlumatları ilə)
- Müəllim + tələbə collaborator hüquqları
- Celery task ilə async icra (3 retry, 60s interval)

### 6. YouTube İnteqrasiyası (`apps/youtube/`)
- Metadata avtomatik çəkilməsi (başlıq, müddət, thumbnail)
- Embedded player (platforma daxilindən izləmə)
- Redis keşi (24 saatlıq caching)
- URL formatları: `youtube.com/watch?v=`, `youtu.be/`

### 7. Bildiriş Sistemi (`apps/notifications/`)
- Email (SendGrid / Mailgun / AWS SES)
- SMS xatırlatmaları (opsional)
- Real-time in-app bildirişlər (Django Channels + WebSocket)
- Bulk email, fərdi mesajlaşma

### 8. Dəstək Sistemi (`apps/support/`)
- Ticket sistemi (Yeni → Baxılır → Cavablandı → Həll → Bağlandı)
- Rich text editor, file əlavəsi, kod formatı
- FAQ bazası, şablon cavablar
- Orta cavab müddəti analitikası

### 9. Qiymətləndirmə (`apps/assessments/`)
- Çoxseçimli, doğru/yanlış, kod yazma sualları
- Avtomatik qiymətləndirmə
- Rəqəmsal sertifikatlar və nailiyyət nişanları

### 10. Analitika (`apps/analytics/`)
- Gündəlik/Aylıq gəlir hesabatı (25 AZN × dərs sayı)
- Model üzrə breakdown (aylıq vs dərs əsaslı)
- Tələbə churn/retention analizi
- Doldurulma nisbəti (booked vs available slots)
- Chart.js ilə vizual dashboardlar

---

## Ödəniş Məntiqi (Biznes Qaydaları)

```python
from decimal import Decimal

LESSON_PRICE         = Decimal('25.00')  # SABİT — heç vaxt dəyişdirilməz!
CANCELLATION_HOURS   = 24               # Ləğvetmə minimum saatı
MAX_LESSONS_PER_WEEK = 7                # Həftəlik maksimum dərs

def calculate_monthly_price(lessons_per_week: int) -> Decimal:
    """Aylıq ödəniş: həftəlik dərs × 4 həftə × 25 AZN"""
    return Decimal(lessons_per_week) * 4 * LESSON_PRICE

# Nümunə: 2 dərs/həftə → 2 × 4 × 25 = 200 AZN/ay
```

---

## Üçüncü Tərəf İnteqrasiyaları

| Xidmət | Məqsəd | Kitabxana |
|---|---|---|
| GitHub API | Tələbə repo yaratma | `PyGithub` |
| YouTube Data API v3 | Video metadata | `google-api-python-client` |
| Google Meet | Dərs video linki | `google-auth` |
| Google Calendar | Sinxronizasiya | `google-api-python-client` |
| Stripe | Ödəniş | `stripe` |
| SendGrid / Mailgun | Email | `django-anymail` |
| Twilio | SMS | `twilio` |
| DigitalOcean Spaces | Fayl saxlama | `django-storages` |

---

## Deployment

### DigitalOcean App Platform (Tövsiyə)
- Python 3.11 native runtime
- Managed PostgreSQL 15+ ($15/ay)
- Managed Redis 7+ ($15/ay)
- Spaces CDN ($5/ay — 250GB)
- Gunicorn + Whitenoise
- Avtomatik SSL sertifikatları
- Push-to-deploy (GitHub inteqrasiyası)

### Railway (Alternativ)
- `railway up` ilə deployment
- PostgreSQL + Redis daxil
- $5/ay başlanğıc

---

## Kurulum

```bash
# 1. Repo-nu klonla
git clone <repo-url>
cd lms_platform

# 2. Virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Asılılıqları quraşdır
pip install -r requirements.txt

# 4. Mühit dəyişənlərini təyin et
cp .env.example .env
# .env faylını redaktə et

# 5. Verilənlər bazasını hazırla
python manage.py migrate

# 6. Superuser yarat
python manage.py createsuperuser

# 7. Serveri başlat
python manage.py runserver
```

### Mühit Dəyişənləri

```env
SECRET_KEY=<django-secret-key>
DEBUG=False
DATABASE_URL=postgresql://...
REDIS_URL=redis://...

GITHUB_TOKEN=<github-personal-access-token>
YOUTUBE_API_KEY=<youtube-data-api-key>
GOOGLE_CREDENTIALS_JSON=<google-oauth-credentials>

STRIPE_PUBLIC_KEY=<stripe-pk>
STRIPE_SECRET_KEY=<stripe-sk>
STRIPE_WEBHOOK_SECRET=<stripe-webhook>

SENDGRID_API_KEY=<sendgrid-key>
AWS_ACCESS_KEY_ID=<do-spaces-key>
AWS_SECRET_ACCESS_KEY=<do-spaces-secret>
AWS_STORAGE_BUCKET_NAME=<spaces-bucket>
```

---

## Celery İşçiləri

```bash
# Background işçi başlat
celery -A config worker -l info -Q default,notifications,github

# Scheduled tasks (xatırlatmalar, aylıq ödənişlər)
celery -A config beat -l info

# Flower (monitoring)
celery -A config flower
```

---

## Test

```bash
# Bütün testlər
pytest

# Coverage hesabatı (hədəf: >80%)
pytest --cov=apps --cov-report=html

# Xüsusi app
pytest apps/bookings/
pytest apps/payments/
```

---

## Kod Standartları

- **PEP 8** (Black formatter, 88 simvol)
- **isort** (import sıralaması)
- **Type hints** — bütün public metodlarda məcburi
- **Docstring** — Args + Returns formatı
- **BaseModel** — bütün modellər UUID pk + timestamps ilə
- **verbose_name** — Azərbaycan dilindədir
- **`@transaction.atomic`** — bütün kritik DB əməliyyatlarında

---

## Scaffold Statusu — 28.02.2026

Aşağıdakı bütün fayllar yaradılıb və GitHub-a push edilib (**120 fayl, 5 196 sətir**).

### `config/` — Django Konfiqurası

| Fayl | Təyinat |
|------|---------|
| `config/settings/base.py` | INSTALLED_APPS, Redis, Celery, LMS konstantları |
| `config/settings/development.py` | Debug toolbar, konsol email |
| `config/settings/production.py` | Sentry, DigitalOcean Spaces, HTTPS |
| `config/urls.py` | Bütün app URL-lərinin birləşdirilməsi |
| `config/asgi.py` | Django Channels ASGI (WebSocket) |
| `config/celery.py` | Celery app, 4 queue (default/notifications/github/payments) |

### `core/` — Ümumi Yardımçılar

| Fayl | Təyinat |
|------|---------|
| `core/utils.py` | `LESSON_PRICE`, `calculate_monthly_price()`, `get_repo_name()`, `generate_invoice_number()`, `extract_youtube_video_id()` |
| `core/mixins.py` | `TeacherRequiredMixin`, `StudentOwnerMixin`, `HTMXMixin` |
| `core/permissions.py` | DRF: `IsTeacher`, `IsStudent`, `IsOwnerOrTeacher` |
| `core/validators.py` | `validate_future_datetime`, `validate_youtube_url`, `validate_github_username`, `validate_phone_number` |
| `core/context_processors.py` | `lms_globals` — LESSON_PRICE, APP_NAME, rol məlumatı |

### `apps/users/` — İstifadəçi Sistemi

| Fayl | Təyinat |
|------|---------|
| `models.py` | `BaseModel` (UUID+timestamps), `User` (AbstractBaseUser), `StudentProfile` |
| `services.py` | `UserService.register_student()`, `approve_student()` |
| `signals.py` | `post_save` → tələbəyə avtomatik `StudentProfile` |
| `forms.py` | `StudentRegistrationForm`, `StudentProfileUpdateForm` |
| `views.py` | `StudentRegisterView`, `ProfileView`, `StudentProfileUpdateView` |
| `api_urls.py` | `/api/v1/me/` — cari istifadəçi JSON |

### `apps/courses/` — Kurs İdarəetməsi

| Fayl | Təyinat |
|------|---------|
| `models.py` | `Category`, `Course`, `Enrollment`, `Module`, `Lesson` (MaterialType choices) |
| `services.py` | `CourseService.create_lesson_with_youtube()` |
| `views.py` | `CourseListView`, `CourseDetailView` |
| `api_urls.py` | `/api/v1/courses/` — aktiv kurslar JSON |

### `apps/bookings/` — Rezervasiya Sistemi

| Fayl | Təyinat |
|------|---------|
| `models.py` | `AvailabilitySlot`, `Booking` (Status + LessonType choices, `can_cancel` property) |
| `services.py` | `BookingService.create_booking()` (`select_for_update`), `cancel_booking()` |
| `tasks.py` | `send_lesson_reminder_task` (max_retries=3, queue=notifications) |
| `views.py` | `BookingListView`, `AvailableSlotsView`, `BookingCreateView` |
| `api_views.py` + `api_urls.py` | `/api/v1/bookings/` |

### `apps/payments/` — Ödəniş Sistemi

| Fayl | Təyinat |
|------|---------|
| `models.py` | `Payment` (Status, PaymentMethod, auto invoice_number), `MonthlySubscription` |
| `services.py` | `PaymentService.create_lesson_payment()`, `process_stripe_payment()` |
| `tasks.py` | `check_overdue_payments_task`, `send_overdue_payment_reminders_task` |
| `views.py` | `PaymentListView` (müəllim + tələbə görünüşü) |
| `api_urls.py` | `/api/v1/payments/` |

### `apps/github_integration/` — GitHub API

| Fayl | Təyinat |
|------|---------|
| `models.py` | `StudentRepository` (Status choices, idempotency) |
| `services.py` | `GitHubService.create_student_repository()`, `repo_exists()` |
| `tasks.py` | `create_student_repo_task` (max_retries=3, 60s delay, idempotency check) |

### `apps/youtube/` — YouTube API

| Fayl | Təyinat |
|------|---------|
| `services.py` | `YouTubeService` — Redis 24h cache, ISO 8601 duration parser, thumbnail |

### `apps/video_conferencing/` — Google Meet

| Fayl | Təyinat |
|------|---------|
| `services.py` | `GoogleMeetService.create_meeting()` — Calendar API, attendee invite |
| `tasks.py` | `create_meet_link_task` (max_retries=3, idempotency) |

### `apps/notifications/` — Bildiriş Sistemi

| Fayl | Təyinat |
|------|---------|
| `models.py` | `Notification` (7 növ, `is_read`, JSON data) |
| `services.py` | `NotificationService` — booking confirmation, lesson reminder, payment reminder |
| `tasks.py` | `send_booking_confirmation`, `send_lesson_reminder`, `send_payment_receipt`, `send_student_approval_email` |
| `consumers.py` | `NotificationConsumer` — AsyncWebsocketConsumer (unread count, mark_read) |
| `routing.py` | `ws/notifications/` WebSocket route — `config/asgi.py` tərəfindən import edilir |
| `views.py` | `NotificationListView`, `MarkAllReadView` (HTMX-uyğun) |

### `apps/support/` — Dəstək Ticketləri

| Fayl | Təyinat |
|------|---------|
| `models.py` | `Ticket` (Status + Priority), `TicketMessage` |
| `forms.py` | `TicketCreateForm`, `TicketMessageForm` |
| `views.py` | `TicketListView`, `TicketCreateView`, `TicketDetailView` |

### `apps/analytics/` — Dashboard

| Fayl | Təyinat |
|------|---------|
| `views.py` | `DashboardView` (KPI: tələbə, dərs, gəlir, gecikmiş ödəniş), `StudentDashboardView` |

### `apps/assessments/` — Qiymətləndirmə

| Fayl | Təyinat |
|------|---------|
| `models.py` | `Assessment` (Quiz/Homework/Project/Exam, `percentage` property) |
| `forms.py` | `AssessmentCreateForm`, `AssessmentGradeForm` |
| `views.py` | `AssessmentListView`, `AssessmentCreateView`, `AssessmentGradeView` |

### `templates/` — HTML Şablonlar

| Şablon | Təyinat |
|--------|---------|
| `base.html` | Bootstrap 5.3 + HTMX + Alpine.js + Chart.js + WebSocket toast |
| `partials/navbar.html` | Bildiriş badge, istifadəçi dropdown |
| `partials/sidebar.html` | Müəllim/tələbə rol əsaslı menyu |
| `partials/pagination.html` | Bootstrap pagination (universal) |
| `auth/login.html` | Allauth uyğun login formu |
| `analytics/dashboard.html` | Müəllim KPI kartları + yaxınlaşan dərslər cədvəli |
| `bookings/booking_list.html` | Dərslər cədvəli (status badge, meet link) |
| `payments/payment_list.html` | Ödənişlər cədvəli (status badge, faktura nömrəsi) |

### Deploy & Test

| Fayl | Təyinat |
|------|---------|
| `Dockerfile` | Python 3.11-slim, non-root user, Daphne |
| `docker-compose.yml` | web + db + redis + celery_worker + celery_beat |
| `.do/app.yaml` | DigitalOcean App Platform spec (3 servis + Managed PG) |
| `pytest.ini` | DJANGO_SETTINGS_MODULE, coverage, --cov-fail-under=50 |
| `setup.cfg` | flake8 (88 char), isort (profile=black), mypy (django-stubs) |
| `conftest.py` | `teacher_user`, `student_user`, `available_slot`, `reserved_slot`, `past_slot` fixtures |
| `tests/test_booking_service.py` | BookingService — 4 test (uğurlu, rezerv slot, keçmiş slot, ləğv) |
| `tests/test_utils.py` | core utils — 6 test (LESSON_PRICE, calculate, repo_name, youtube_id, azn format, invoice) |

---

## Sənədlər

- [Tam Layihə Planı](docs/project.md) — Bütün funksionallıqların ətraflı təsviri
- [Copilot Təlimatları](.github/copilot-instructions.md) — AI kod standartları
- [Agent Siyahısı](.github/copilot-agents.md) — Spesializasiya agentləri
- [Prompt Kitabxanası](.github/copilot-prompts.md) — Hazır prompt şablonları

---

## Lisenziya

Bu layihə şəxsi istifadə üçündür. Bütün hüquqlar qorunur.

---

*LMS Platform — Django 5.0+ | PostgreSQL | Redis | Celery | HTMX | Alpine.js*  
*AI Model: Claude Sonnet 4.6 | Scaffold tamamlandı: 28.02.2026*
