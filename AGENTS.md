# AGENTS.md — LMS Platform Agent Sistemi

**AI Model**: Claude Sonnet 4.6  
**Framework**: Django 5.0+ | PostgreSQL | Redis | Celery | HTMX | Alpine.js  
**Dil**: Azərbaycan  
**Tarix**: 16.03.2026

---

## 🏗️ Layihə Konteksti

Bu **LMS (Learning Management System)** platformu tək müəllimin çoxlu tələbəni **fərdi online format** (1-1) ilə idarə etməsi üçün hazırlanıb.

```
Platform:     1-1 fərdi online tədris (müəllim → tələbə)
Dərs qiyməti: 25 AZN (SABİT — dəyişdirilməz!)
Ödəniş:       Aylıq abunə VEYA dərs əsaslı (pay-as-you-go)
Video:        Google Meet (dərslər) + YouTube (materiallar)
Repo:         Hər tələbə üçün GitHub private repo (avtomatik)
Xatırlatma:   24 saat + 1 saat əvvəl Celery task-ları
```

### Texniki Stack

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

## 📁 App Strukturu

```
apps/
├── users/              # İstifadəçi idarəetməsi (User, StudentProfile)
├── courses/            # Kurs + material idarəsi (Course, Module, Lesson, Enrollment)
├── bookings/           # Dərs rezervasiyası — Calendly tipli (AvailabilitySlot, Booking)
├── payments/           # Aylıq/dərs ödəniş sistemi (Payment, MonthlySubscription)
├── github_integration/ # GitHub API — tələbə repo-su (StudentRepository)
├── youtube/            # YouTube Data API v3 (metadata, embedded player)
├── video_conferencing/ # Google Meet API (avtomatik link)
├── notifications/      # Email/SMS/real-time bildirişlər (Notification, WebSocket)
├── support/            # Dəstək ticket sistemi (Ticket, TicketMessage)
├── analytics/          # Dashboard analitikası (KPI, Chart.js)
└── assessments/        # Qiymətləndirmə sistemi (Assessment, grading)
```

---

## 📐 Məcburi Kod Standartları

### 1. BaseModel — Hər Model Miras Almalıdır

```python
import uuid
from django.db import models

class BaseModel(models.Model):
    id         = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True
```

### 2. Model Qaydaları

- `verbose_name` **mütləq Azərbaycan dilindədir** (`verbose_name='Dərs'`)
- `TextChoices` enum-lar sinif daxilindəki class ilə təyin edilir
- `Meta.ordering`, `Meta.indexes`, `__str__` mütləqdir
- `db_table` hər modeldə göstərilməlidir

### 3. View Standartları

- `LoginRequiredMixin` bütün protected view-larda
- `TeacherRequiredMixin` müəllim əməliyyatlarında
- `StudentOwnerMixin` tələbə öz resurslarında
- `select_related` / `prefetch_related` (N+1 YASAQ!)
- Mesajlar Azərbaycan dilində

### 4. Service Layer

- Business logic `services.py`-da saxlanılır, view-dan ayrılır
- `@transaction.atomic` bütün kritik DB əməliyyatlarında
- Exception handling + logging mütləqdir
- Type hints bütün public metodlarda

### 5. LMS Biznes Sabitləri

```python
from decimal import Decimal

LESSON_PRICE         = Decimal('25.00')   # SABİT — DƏYIŞDIRILMƏZ!
CANCELLATION_HOURS   = 24                 # Ləğvetmə minimum saatı
MAX_LESSONS_PER_WEEK = 7                  # Həftəlik maksimum dərs

def calculate_monthly_price(lessons_per_week: int) -> Decimal:
    """Aylıq abunə: həftəlik × 4 × 25 AZN"""
    return Decimal(lessons_per_week) * 4 * LESSON_PRICE
```

---

## 👥 Agent Siyahısı

| # | Agent | Rol | Əsas Məsuliyyət |
|---|-------|-----|-----------------|
| 1 | `@lms-architect` | **Super Agent** | Feature analizi + agent koordinasiyası |
| 2 | `@backend-architect` | Backend Memar | Django models, views, services, URLs |
| 3 | `@frontend-dev` | Frontend İnkişafçı | Templates, HTMX, Alpine.js, Bootstrap |
| 4 | `@db-engineer` | DB Mühəndisi | PostgreSQL, ORM, migration, indekslər |
| 5 | `@security-expert` | Təhlükəsizlik | Auth, permissions, validation, CSRF |
| 6 | `@integrations-dev` | İnteqrasiya | GitHub, YouTube, Meet, Calendar API |
| 7 | `@payments-dev` | Ödəniş | Stripe, aylıq/dərs əsaslı, faktura |
| 8 | `@devops-engineer` | DevOps | Docker, DigitalOcean, CI/CD |
| 9 | `@analytics-dev` | Analitika | Dashboard, Chart.js, hesabatlar |
| 10 | `@testing-specialist` | Test | pytest-django, factory_boy, >80% coverage |
| 11 | `@notifications-dev` | Bildiriş | Email, SMS, WebSocket, Celery |
| 12 | `@performance-optimizer` | Performans | Query opt, Redis cache, profiling |

---

## 🧠 @lms-architect — Super Agent (Koordinator)

### Məsuliyyətlər
- Mürəkkəb feature-ları analiz et, alt tapşırıqlara böl
- Doğru agent-i seç və tapşırığı yönləndir
- Agent-lər arası handoff-u idarə et
- LMS biznes qaydalarının düzgünlüyünü yoxla

### Agent Seçim Qaydası

```
Nə yazmaq istəyirsən?

"model yaz"          → @backend-architect
"template yaz"       → @frontend-dev
"sorğu optimize et"  → @db-engineer + @performance-optimizer
"payment sistemi"    → @payments-dev
"GitHub API"         → @integrations-dev
"email göndər"       → @notifications-dev
"test yaz"           → @testing-specialist
"deploy et"          → @devops-engineer
"security yoxla"     → @security-expert
"dashboard qrafik"   → @analytics-dev
"hamısı lazımdır"    → @lms-architect (koordinasiya)
```

### Feature Map

```
Feature                          → Agent-lər
────────────────────────────────────────────────────────
Tələbə qeydiyyatı                → @backend + @integrations + @notifications
Dərs rezervasiyası               → @backend + @frontend + @payments
Ödəniş axını (aylıq/dərs-based)  → @payments + @notifications + @backend
GitHub repo yaratma              → @integrations + @backend
YouTube material əlavəsi         → @integrations + @frontend
Google Meet linki                → @integrations + @notifications
Dashboard analitikası            → @analytics + @db-engineer
Email xatırlatmaları             → @notifications + @devops
Deployment                       → @devops + @security
Test coverage                    → @testing + @backend
```

---

## 🏗️ @backend-architect — Backend Memar

### Məsuliyyətlər
- Django app strukturunu dizayn et
- Model şəmaları yarat (BaseModel-dən miras ilə)
- Class-Based Views (CBV) yaz
- Service layer dizayn et
- URL konfiqurasiyasını idarə et

### İş Ardıcıllığı
1. `models.py` → BaseModel miras, verbose_name AZ
2. `services.py` → @transaction.atomic, exception handling
3. `views.py` → LoginRequiredMixin, select_related
4. `forms.py` → Bootstrap 5 widgets, AZ labels
5. `urls.py` → app_name namespace, UUID pk
6. `admin.py` → ModelAdmin registration
7. `tasks.py` → Celery shared_task (async ops)

### Checklist
- [ ] BaseModel-dən miras (UUID pk, created_at, updated_at)
- [ ] verbose_name Azərbaycan dilindədir
- [ ] TextChoices enum-lar
- [ ] select_related / prefetch_related (N+1 yoxdur)
- [ ] @transaction.atomic service metodlarında
- [ ] Type hints bütün metodlarda
- [ ] Literal 25 yoxdur (LESSON_PRICE sabiti istifadə edilir)

---

## 🎨 @frontend-dev — Frontend İnkişafçı

### Məsuliyyətlər
- Django Templates (Bootstrap 5.3+)
- HTMX partial templates
- Alpine.js reaktiv komponentlər
- Form renderingi (crispy-forms)
- Responsive dizayn, mobile-first

### HTMX Standartları

```html
<!-- Partial template sorğusu -->
<div hx-get="{% url 'bookings:available-slots' %}"
     hx-target="#slots-container"
     hx-trigger="change from:#date-picker"
     hx-indicator="#loading-spinner">
</div>

<!-- Form HTMX ilə göndər -->
<form hx-post="{% url 'bookings:create' %}"
      hx-target="#booking-result"
      hx-swap="innerHTML">
    {% csrf_token %}
    {{ form|crispy }}
</form>
```

### Alpine.js Standartları

```html
<div x-data="{ selectedSlot: null, showConfirm: false }">
    <button @click="selectedSlot = slot; showConfirm = true">Seç</button>
    <div x-show="showConfirm" x-transition>
        <p x-text="`Seçilmiş saat: ${selectedSlot?.time}`"></p>
    </div>
</div>
```

### Checklist
- [ ] `{% extends 'base.html' %}` strukturu
- [ ] `{% load static %}` hər template-də
- [ ] HTMX ilə partial template-lər
- [ ] Bootstrap 5 class-ları
- [ ] Azərbaycan dilindəki mətn
- [ ] Mobile-first dizayn

---

## 🗃️ @db-engineer — Verilənlər Bazası Mühəndisi

### Məsuliyyətlər
- Django ORM model dizaynı
- Migration strategiyası
- Database indeksləri
- Query optimallaşdırma
- PostgreSQL-spesifik xüsusiyyətlər

### Checklist
- [ ] UUID primary key-lər
- [ ] Lazımlı `db_index=True` field-ləri
- [ ] `Meta.indexes` composite indekslər
- [ ] `select_related` / `prefetch_related`
- [ ] Bulk əməliyyatlar (bulk_create, bulk_update)
- [ ] `F()` expression-lar atomik yeniləmə üçün

---

## 🔐 @security-expert — Təhlükəsizlik Mütəxəssisi

### Məsuliyyətlər
- Authentication, JWT, 2FA
- Permission yoxlamaları
- Input validation, sanitizasiya
- CSRF, XSS, SQL injection qorunması
- Audit log sistemi

### Checklist
- [ ] `LoginRequiredMixin` bütün protected view-larda
- [ ] CSRF token bütün POST form-larda
- [ ] User input-ların validation-ı
- [ ] Sensitive data loglanmır
- [ ] Rate limiting tətbiqi
- [ ] Webhook signature yoxlaması

---

## 🔗 @integrations-dev — İnteqrasiya İnkişafçısı

### Məsuliyyətlər
- GitHub API (PyGithub) — tələbə repo yaratma
- YouTube Data API v3 — video metadata
- Google Meet API — dərs video linki
- Google Calendar API — sinxronizasiya
- Celery task ilə async inteqrasiyalar

### Checklist
- [ ] API key-lər environment variable-lardan okunur
- [ ] Xəta halında retry mexanizmi (max 3, 60s)
- [ ] Celery task-larında async icra
- [ ] Xəta loglanması
- [ ] Idempotency yoxlaması

---

## 💳 @payments-dev — Ödəniş İnkişafçısı

### Məsuliyyətlər
- **Aylıq abunə**: həftəlik_dərs × 4 × 25 AZN
- **Dərs əsaslı**: hər dərsdən sonra 25 AZN
- Stripe inteqrasiyası
- Faktura (PDF) yaradılması
- Borc izləmə + xatırlatma
- Webhook handler-lar

### Ödəniş Qaydaları
```python
LESSON_PRICE = Decimal('25.00')  # SABİT!

# Aylıq: 2 dərs/həftə → 2 × 4 × 25 = 200 AZN/ay
# Dərs əsaslı: Hər dərsdən sonra 25 AZN (24 saat limit)
# Gecikmiş: 2, 5, 7-ci gün xatırlatma → 10 gün → xidmət dayandırma
```

---

## ⚡ @performance-optimizer — Performans Mütəxəssisi

### Məsuliyyətlər
- N+1 sorğu problemlərini aşkar/düzəlt
- Redis keşləmə strategiyası
- Django Debug Toolbar ilə profiling
- Database indeks analizi
- Response time optimallaşdırması (< 100ms hədəf)

### Checklist
```
□ Hər QuerySet-də select_related() var?
□ M2M field-lər üçün prefetch_related() var?
□ Aggregasiya Python-da deyil DB-də edilir?
□ Keş TTL düzgündür? (dinamik: 60s, statik: 3600s)
□ Template-lərdə DB sorğusu var? → context-ə əlavə et
```

---

## 🚀 @devops-engineer — DevOps Mühəndisi

### Məsuliyyətlər
- DigitalOcean App Platform konfiqurasiyası
- Docker + Docker Compose setup
- GitHub Actions CI/CD
- Health check endpoint-ləri
- Production settings

---

## 📊 @analytics-dev — Analitika İnkişafçısı

### Məsuliyyətlər
- Müəllim dashboard KPI-ları
- Chart.js qrafiklər (aylıq gəlir, tələbə sayı)
- Maliyyə hesabatları
- Excel/PDF export
- Django ORM aggregation sorğuları

---

## 🧪 @testing-specialist — Test Mütəxəssisi

### Məsuliyyətlər
- pytest-django unit testlər
- Factory Boy fixtures
- Coverage > 80% təmin etmə
- Edge case ssenariləri

### Test Qaydaları
- `@pytest.mark.django_db` bütün DB testlərdə
- Test adları: `test_<scenario>_<expected>`
- Hər test bir şeyi yoxlamalıdır
- `conftest.py`-da fixture-lar saxlanılır
- External service-lər `unittest.mock.patch` ilə mock edilir

---

## 📬 @notifications-dev — Bildiriş İnkişafçısı

### Məsuliyyətlər
- Email (SendGrid/Mailgun)
- SMS (Twilio — opsional)
- In-app real-time (Django Channels WebSocket)
- Celery Beat scheduled tasks
- HTML email templates

### Xatırlatma Cədvəli
```
24 saat əvvəl  → tələbəyə email + SMS
1 saat əvvəl   → tələbəyə push notification
Ödəniş günü    → müəllimə + tələbəyə email
```

---

## 🔄 Yeni Feature Üçün Tam Prosess

```
1.  @lms-architect        → Feature analizi + plan + agent bölüşdürməsi
        ↓
2.  @backend-architect    → Model + Service (BaseModel, AZ verbose_name)
        ↓
3.  @db-engineer          → İndekslər + migration + query optimallaşdırma
        ↓
4.  @backend-architect    → CBV Views + URLs + Forms
        ↓
5.  @integrations-dev     → GitHub/YouTube/Meet API (lazım olsa)
        ↓
6.  @payments-dev         → 25 AZN ödəniş məntiqi (lazım olsa)
        ↓
7.  @frontend-dev         → Bootstrap 5 + HTMX + Alpine.js templates
        ↓
8.  @notifications-dev    → Celery task-lar + email/SMS (lazım olsa)
        ↓
9.  @performance-optimizer → Keş + N+1 yoxla + profiling
        ↓
10. @security-expert      → Permission audit + input validation
        ↓
11. @testing-specialist   → pytest-django + factory_boy (>80% coverage)
        ↓
12. @devops-engineer      → GitHub Actions CI/CD + deploy
```

---

## 📋 Agent Handoff Şablonu

Bir agentdən digərinə keçərkən:

```markdown
## Agent Handoff: @{from-agent} → @{to-agent}

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

## 🚨 MƏCBURİ QAYDA — HƏR TAPŞIRIQDAN SONRA AUTO-COMMIT

```bash
# 1. Bütün dəyişiklikləri stage et
git add .

# 2. Azərbaycan dilində commit mesajı
# Format: "<emoji> <nə edildi> (<fayl sayı> fayl) — dd.MM.yyyy HH:mm"
git commit -m "✅ Tapşırıq tamamlandı (3 fayl) — 16.03.2026 22:00"

# 3. GitHub-a push et
git push origin main
```

### Commit Emoji Qaydası

| Dəyişən fayllar | Emoji | Mesaj nümunəsi |
|-----------------|-------|----------------|
| `models.py` | 🗃️ | Model strukturu yeniləndi |
| `views.py` | 👁️ | View-lar yeniləndi |
| `services.py` | 🔧 | Servis məntiqi yeniləndi |
| `tasks.py` | ⚡ | Celery task-lar yeniləndi |
| `tests/` | 🧪 | Testlər əlavə edildi |
| `*.html` | 🎨 | Template və UI yeniləndi |
| `*.md` | 📝 | Sənədlər yeniləndi |
| `.json`, `.yaml` | ⚙️ | Konfiqurasiya yeniləndi |
| Qarışıq | ✅ | Tapşırıq tamamlandı |

---

## 📚 Əlaqəli Sənədlər

- [README.md](README.md) — Tam layihə planı
- [copilot-instructions.md](.github/copilot-instructions.md) — Kod standartları
- [copilot-agents.md](.github/copilot-agents.md) — Agent təfərrüatları
- [copilot-prompts.md](.github/copilot-prompts.md) — Prompt kitabxanası
- [.claude/agents/](/.claude/agents/) — Claude Code agent faylları

---

*LMS Platform — Django 5.0+ | PostgreSQL | Redis | Celery | HTMX | Alpine.js*  
*AI Model: Claude Sonnet 4.6 | Agent Sistemi: 12 ixtisaslaşmış agent*
