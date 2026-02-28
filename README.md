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
*AI Model: Claude Sonnet 4.6 | Tarix: 28.02.2026*
