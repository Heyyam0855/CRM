# 🎓 LMS Platform — Fərdi Online Tədris İdarəetmə Sistemi

**AI Model**: Claude Sonnet 4.6 | **Framework**: Django 5.0+ | **Dil**: Azərbaycan  
**Repository**: https://github.com/Heyyam0855/CRM.git

---

## 📌 Layihə Haqqında

Bu **LMS (Learning Management System)** platformu tək müəllimin çoxlu tələbəni **fərdi online format** (1-1) ilə idarə etməsi üçün hazırlanıb.

```
Platform:     1-1 fərdi online tədris (müəllim → tələbə)
Dərs qiyməti: 25 AZN (SABİT)
Ödəniş:       Aylıq abunə VEYA dərs əsaslı (pay-as-you-go)
Video:        Google Meet (dərslər) + YouTube (materiallar)
Repo:         Hər tələbə üçün GitHub private repo (avtomatik)
Xatırlatma:   24 saat + 1 saat əvvəl Celery task-ları
```

---

## 🏗️ Texniki Stack

| Komponent       | Texnologiya                                      |
|-----------------|--------------------------------------------------|
| Backend         | Django 5.0.6 (Python 3.11+)                      |
| Database        | PostgreSQL 15+                                   |
| Cache / Queue   | Redis 7+ · Celery 5.4.0 · Celery Beat            |
| Real-time       | Django Channels 4.1 + WebSocket (Daphne)         |
| Frontend        | Bootstrap 5.3 · HTMX · Alpine.js                |
| Auth            | django-allauth · JWT · django-otp (2FA)          |
| Storage         | DigitalOcean Spaces (S3-compatible, boto3)       |
| Payment         | ePoint payment gateway                           |
| External API    | GitHub (PyGithub) · Google Meet · YouTube        |
| REST API        | Django REST Framework + drf-spectacular          |
| Deployment      | DigitalOcean App Platform / Railway              |

---

## ✅ Görülən İşlər (Tamamlanan)

### 👤 1. İstifadəçi İdarəetməsi (`apps/users/`)
**Status: ✅ 100% Tamamlandı**

- [x] `User` modeli — email əsaslı autentifikasiya, müəllim/tələbə rolları
- [x] `StudentProfile` modeli — PENDING / ACTIVE / INACTIVE / FROZEN / GRADUATED statusları
- [x] `RegistrationRequest` — tələbə qeydiyyat sorğularının idarəsi
- [x] CRM interfeysi — müəllim bütün tələbələri görmə, axtarış, filtr
- [x] Tələbə status dəyişmə view-ı (ACTIVE/INACTIVE/FROZEN)
- [x] Tələbə qeydlər sistemi (müəllim tərəfindən)
- [x] Tələbə özü qeydiyyat formu (`/auth/register/`)
- [x] Qeydiyyat sonrası ödəniş axını
- [x] İki ödəniş modeli: `MONTHLY` (aylıq abunə) / `PER_LESSON` (dərs əsaslı)

---

### 📚 2. Kurs İdarəetməsi (`apps/courses/`)
**Status: ✅ 90% Tamamlandı**

- [x] `Category` modeli — hierarchical kurs kateqoriyaları
- [x] `Course` modeli — DRAFT / ACTIVE / ARCHIVED statusları, səviyyə seçimi
- [x] `Enrollment` modeli — tələbə kurs qeydiyyatı (unique constraint)
- [x] `Module` modeli — kurs modulları/fəsilləri, sıralama
- [x] Kurs siyahısı view-ı (HTMX dəstəkli, pagination: 12)
- [x] Kurs detalı view-ı — modul/dərs siyahısı, enrollment statusu
- [x] Kurs yaratma/redaktə view-ları (müəllim üçün)

---

### 📅 3. Dərs Rezervasiya Sistemi (`apps/bookings/`)
**Status: ✅ 95% Tamamlandı**

- [x] `WeeklySchedule` — müəllimin həftəlik proqramı (gün, başlanğıc/bitmə saatı)
- [x] `AvailabilitySlot` — fərdi dərs vaxt slotları, gələcək tarix validator
- [x] `Booking` — dərs rezervasiyası: PENDING / CONFIRMED / COMPLETED / CANCELLED / NO_SHOW / RESCHEDULED
- [x] Dərs növləri: STANDARD / TRIAL / CONSULTATION / REVIEW
- [x] Sabit qiymət: 25 AZN (biznes sabiti)
- [x] 24 saat ləğvetmə qaydası (`can_cancel` property)
- [x] `BookingService` — atomic booking yaratma (slot lock ilə)
- [x] `ScheduleService` — həftəlik proqrama əsasən avtomatik slot generasiyası
- [x] Calendly tipli calendar interfeysi
- [x] HTMX ilə mövcud slotların dinamik yüklənməsi
- [x] Google Meet linki — async Celery task ilə avtomatik yaradılır
- [x] Xatırlatma task-ları: dərsdən 24 saat + 1 saat əvvəl

---

### 💳 4. Ödəniş Sistemi (`apps/payments/`)
**Status: ✅ 95% Tamamlandı**

- [x] `Payment` modeli — universal: PENDING / COMPLETED / FAILED / REFUNDED / OVERDUE / CANCELLED
- [x] Ödəniş metodları: EPOINT / BANK_TRANSFER / CASH / ONLINE
- [x] `MonthlySubscription` modeli — aylıq abunə: ACTIVE / PAUSED / CANCELLED
- [x] **ePoint payment gateway** tam inteqrasiyası
  - [x] Ödənişin başladılması (`EPointInitiateView`)
  - [x] Uğurlu ödəniş callback (`EPointSuccessView`)
  - [x] Xəta callback (`EPointErrorView`)
  - [x] Server-to-server webhook (`EPointCallbackView`) — imza yoxlaması ilə
- [x] Faktura sistemi — avtomatik nömrələnmə
- [x] `PaymentService.create_lesson_payment()` — dərs başına 25 AZN, 24 saat limit
- [x] `PaymentService.create_monthly_payment()` — `həftəlik_dərs × 4 × 25 AZN`
- [x] Gecikmiş ödəniş izləmə (OVERDUE status)

---

### 🔔 5. Bildiriş Sistemi (`apps/notifications/`)
**Status: ⚠️ 70% Tamamlandı**

- [x] `Notification` modeli — tip: BOOKING_CONFIRMED / LESSON_REMINDER / PAYMENT_DUE / REPO_CREATED / GENERAL
- [x] JSON `data` field — əlavə kontekst üçün
- [x] Bildiriş siyahısı view-ı (pagination: 30)
- [x] "Hamısını oxunmuş işarələ" (HTMX dəstəkli)
- [x] Django Channels + WebSocket routing konfiqurasiyası
- [x] Celery task-ları: dərs xatırlatmaları, booking təsdiq emailləri
- [ ] SMS bildirişləri (Twilio) — TODO
- [ ] Email HTML şablonları — natamam

---

### 🐙 6. GitHub İnteqrasiyası (`apps/github_integration/`)
**Status: ✅ 95% Tamamlandı**

- [x] `StudentRepository` modeli — PENDING / CREATING / CREATED / FAILED / ARCHIVED
- [x] `GitHubService.create_student_repository()` — private repo yaratma
- [x] Tələbəni collaborator kimi əlavə etmə (push icazəsi)
- [x] Repo adı formatı: `{ad-soyad}-{kurs-slug}`
- [x] Xəta handling + status izləmə
- [x] Organization və şəxsi repo dəstəyi

---

### 📝 7. Qiymətləndirmə Sistemi (`apps/assessments/`)
**Status: ✅ 85% Tamamlandı**

- [x] `Assessment` modeli — QUIZ / HOMEWORK / PROJECT / EXAM növləri
- [x] Xal izləmə: `score / max_score`, `percentage` property
- [x] GitHub/fayl submission URL
- [x] Müəllim feedback sahəsi
- [x] Qiymətləndirmə siyahısı (tələbə yalnız özünküləri görür)
- [x] Müəllim qiymət verir (`AssessmentGradeView`)
- [x] Son tarix (`due_date`) + təqdim tarixi (`submitted_at`)

---

### 🎫 8. Dəstək Ticket Sistemi (`apps/support/`)
**Status: ✅ 90% Tamamlandı**

- [x] `Ticket` modeli — OPEN / IN_PROGRESS / RESOLVED / CLOSED
- [x] Prioritet: LOW / MEDIUM / HIGH / URGENT
- [x] `TicketMessage` — çoxsaylı mesaj əsaslı söhbət sistemi
- [x] Müəllim/tələbə mesaj fərqləndirməsi (`is_from_teacher`)
- [x] Ticket siyahısı, yaratma, detalı view-ları
- [x] Həll tarixi (`resolved_at`) izləmə

---

### 📊 9. Analitika Dashboard (`apps/analytics/`)
**Status: ✅ 85% Tamamlandı**

- [x] `DashboardView` — müəllim üçün əsas idarəetmə paneli
- [x] KPI kartları: aktiv tələbə sayı, gözləyən qeydiyyatlar, aylıq bookingslər
- [x] Gəlir hesablaması — cari ay COMPLETED ödənişlər
- [x] Gecikmiş ödəniş sayacı
- [x] Növbəti 5 dərs (upcoming lessons)
- [x] 6 aylıq aylıq gəlir trendi (Chart.js JSON data)
- [x] 6 aylıq aylıq booking trendi
- [x] Azərbaycan ay adları (Yan, Fev, Mar, Apr, May, İyn...)
- [ ] Excel/PDF export — TODO

---

### 🔐 10. Autentifikasiya və Təhlükəsizlik
**Status: ✅ 90% Tamamlandı**

- [x] django-allauth — tam auth sistemi (login, logout, password reset)
- [x] Google OAuth2 sosial giriş
- [x] 2FA (Two-Factor Authentication) — django-otp
- [x] JWT token-lar — djangorestframework-simplejwt
- [x] `LoginRequiredMixin` — bütün protected view-larda
- [x] `TeacherRequiredMixin` — müəllim əməliyyatları üçün
- [x] `StudentOwnerMixin` — tələbə öz resurslarına
- [x] CSRF qorunması
- [x] CORS konfiqurasiyası

---

### 🌐 11. REST API (`/api/v1/`)
**Status: ⚠️ 60% Tamamlandı**

- [x] Django REST Framework konfiqurasiyası
- [x] drf-spectacular — API sxema yaradılması
- [x] JWT autentifikasiyası API-da
- [x] Bookings API endpoint-ləri
- [x] Users API endpoint-ləri (qismən)
- [x] Courses API endpoint-ləri (qismən)
- [x] Payments API endpoint-ləri (qismən)
- [ ] Tam Swagger/OpenAPI sənədləşməsi — TODO

---

### ⚙️ 12. İnfrastruktur və Konfiqurasiya
**Status: ✅ 90% Tamamlandı**

- [x] `config/settings/base.py` — əsas konfiqurasiya
- [x] `config/settings/development.py` — lokal inkişaf mühiti
- [x] `config/settings/production.py` — production konfigurasiyası
- [x] Docker + Docker Compose (development + production)
- [x] `Dockerfile` + `entrypoint.sh`
- [x] `docker-compose.prod.yml` — production stack
- [x] WhiteNoise — static fayl xidməti
- [x] DigitalOcean Spaces (S3) — media fayl saxlama
- [x] Health check endpoint (`/health/`)
- [x] Django Debug Toolbar (development)
- [x] Rosetta — tərcümə interfeysi
- [x] i18n — çoxdilli dəstək (az/en/ru)
- [x] Celery Beat — planlaşdırılmış tapşırıqlar
- [x] Django Channels (Daphne ASGI server)
- [x] pytest + pytest-django konfiqurasiyası

---

## 📁 Layihə Strukturu

```
lms_platform/
├── apps/
│   ├── users/              ✅ CRM + tələbə idarəetməsi
│   ├── courses/            ✅ Kurs + modul idarəsi
│   ├── bookings/           ✅ Calendly tipli rezervasiya
│   ├── payments/           ✅ ePoint ödəniş gateway
│   ├── github_integration/ ✅ Avtomatik GitHub repo
│   ├── youtube/            📋 YouTube API
│   ├── video_conferencing/ 📋 Google Meet API
│   ├── notifications/      ⚠️ Bildiriş sistemi (qismən)
│   ├── support/            ✅ Ticket sistemi
│   ├── analytics/          ✅ Dashboard analitika
│   └── assessments/        ✅ Qiymətləndirmə
├── config/                 ✅ Django ayarları
├── core/                   ✅ Utilities, mixins, permissions
├── templates/              ✅ Bootstrap 5 + HTMX şablonlar
├── static/                 ✅ CSS/JS resursları
├── locale/                 ✅ az/en/ru tərcümələr
└── tests/                  ✅ pytest-django testlər
```

---

## 📊 Ümumi Tamamlanma Statusu

| Modul                    | Status | Faiz |
|--------------------------|--------|------|
| İstifadəçi İdarəetməsi   | ✅     | 100% |
| Kurs İdarəetməsi         | ✅     | 90%  |
| Dərs Rezervasiyası       | ✅     | 95%  |
| Ödəniş Sistemi (ePoint)  | ✅     | 95%  |
| Bildiriş Sistemi         | ⚠️     | 70%  |
| GitHub İnteqrasiyası     | ✅     | 95%  |
| Qiymətləndirmə           | ✅     | 85%  |
| Dəstək Ticket Sistemi    | ✅     | 90%  |
| Analitika Dashboard      | ✅     | 85%  |
| Autentifikasiya / Auth   | ✅     | 90%  |
| REST API                 | ⚠️     | 60%  |
| İnfrastruktur / DevOps   | ✅     | 90%  |

---

## 🔜 Görüləcək İşlər (TODO)

- [ ] Email HTML şablonlarının tamamlanması (SendGrid/Mailgun)
- [ ] SMS bildirişləri (Twilio inteqrasiyası)
- [ ] WebSocket consumer-larının tam implementasiyası
- [ ] Analytics Excel/PDF export funksiyası
- [ ] REST API tam Swagger sənədləşməsi
- [ ] YouTube API inteqrasiyasının tamamlanması
- [ ] Google Calendar sinxronizasiyası
- [ ] Stripe ödəniş gateway alternativ inteqrasiyası
- [ ] Test coverage-nin artırılması (hədəf: >80%)
- [ ] Course lesson (dərs materialları) detallarının əlavə edilməsi

---

## 🚀 Lokal İşə Salma

```bash
# 1. Virtual mühiti aktivləşdir
.venv-1\Scripts\activate

# 2. Paketləri quraşdır
pip install -r requirements/development.txt

# 3. Miqrasiyaları tətbiq et
python manage.py migrate --settings=config.settings.local

# 4. Superuser yarat
python manage.py runscript create_superuser --settings=config.settings.local

# 5. Serveri işə sal
python manage.py runserver --settings=config.settings.local
```

```bash
# Docker ilə işə sal
docker-compose up --build
```

---

## 💰 Biznes Qaydaları

```python
LESSON_PRICE         = Decimal('25.00')   # SABİT — DƏYIŞDIRILMƏZ!
CANCELLATION_HOURS   = 24                 # Ləğvetmə minimum saatı
MAX_LESSONS_PER_WEEK = 7                  # Həftəlik maksimum dərs

# Aylıq abunə hesablaması
# Misal: 2 dərs/həftə → 2 × 4 × 25 = 200 AZN/ay
monthly_price = lessons_per_week * 4 * 25
```

---

*LMS Platform — Django 5.0+ | PostgreSQL | Redis | Celery | HTMX | Alpine.js*  
*AI Model: Claude Sonnet 4.6 | Son yeniləmə: 03.05.2026*
