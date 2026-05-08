# 🎓 LMS Platform — Personal 1-on-1 Online Teaching Management System

**AI Model**: Claude Sonnet 4.6 | **Framework**: Django 5.0+ | **Repository**: https://github.com/Heyyam0855/CRM.git

---

## 📌 About the Project

This **LMS (Learning Management System)** platform is designed for a single teacher to manage multiple students in a **1-on-1 online format**.

```
Platform:     1-on-1 personalized online teaching (teacher → student)
Lesson price: 25 AZN (FIXED)
Payment:      Monthly subscription OR pay-as-you-go (per lesson)
Video:        Google Meet (live lessons) + YouTube (course materials)
Repo:         Automatic private GitHub repository per student
Reminders:    Celery tasks — 24 hours and 1 hour before each lesson
```

---

## 🏗️ Tech Stack

| Component      | Technology                                        |
|----------------|---------------------------------------------------|
| Backend        | Django 5.0.6 (Python 3.11+)                       |
| Database       | PostgreSQL 15+                                    |
| Cache / Queue  | Redis 7+ · Celery 5.4.0 · Celery Beat             |
| Real-time      | Django Channels 4.1 + WebSocket (Daphne)          |
| Frontend       | Tailwind CSS 3 · HTMX · Alpine.js                |
| Auth           | django-allauth · JWT · django-otp (2FA)           |
| Storage        | DigitalOcean Spaces (S3-compatible, boto3)        |
| Payment        | ePoint payment gateway                            |
| External APIs  | GitHub (PyGithub) · Google Meet · YouTube         |
| REST API       | Django REST Framework + drf-spectacular           |
| Deployment     | DigitalOcean App Platform / Railway               |

---

## ✅ Completed Features

### 👤 1. User Management (`apps/users/`)
**Status: ✅ 100% Complete**

- [x] `User` model — email-based authentication, teacher/student roles
- [x] `StudentProfile` model — PENDING / ACTIVE / INACTIVE / FROZEN / GRADUATED statuses
- [x] `RegistrationRequest` — student registration request management
- [x] CRM interface — teacher can view, search and filter all students
- [x] Student status change view (ACTIVE / INACTIVE / FROZEN)
- [x] Student notes system (added by teacher)
- [x] Student self-registration form (`/auth/register/`)
- [x] Post-registration payment flow
- [x] Two payment models: `MONTHLY` (subscription) / `PER_LESSON` (pay-as-you-go)

---

### 📚 2. Course Management (`apps/courses/`)
**Status: ✅ 90% Complete**

- [x] `Category` model — hierarchical course categories
- [x] `Course` model — DRAFT / ACTIVE / ARCHIVED statuses, difficulty level
- [x] `Enrollment` model — student course enrollment (unique constraint)
- [x] `Module` model — course modules/chapters with ordering
- [x] Course list view (HTMX-powered, pagination: 12)
- [x] Course detail view — module/lesson list, enrollment status
- [x] Course create/edit views (teacher only)

---

### 📅 3. Lesson Booking System (`apps/bookings/`)
**Status: ✅ 95% Complete**

- [x] `WeeklySchedule` — teacher's weekly schedule (day, start/end time)
- [x] `AvailabilitySlot` — individual lesson time slots with future date validation
- [x] `Booking` — lesson reservations: PENDING / CONFIRMED / COMPLETED / CANCELLED / NO_SHOW / RESCHEDULED
- [x] Lesson types: STANDARD / TRIAL / CONSULTATION / REVIEW
- [x] Fixed price: 25 AZN (business constant)
- [x] 24-hour cancellation policy (`can_cancel` property)
- [x] `BookingService` — atomic booking creation (with slot locking)
- [x] `ScheduleService` — automatic slot generation based on weekly schedule
- [x] Calendly-style calendar interface
- [x] HTMX-powered dynamic slot loading
- [x] Google Meet link — auto-created via async Celery task
- [x] Reminder tasks: 24 hours and 1 hour before the lesson

---

### 💳 4. Payment System (`apps/payments/`)
**Status: ✅ 95% Complete**

- [x] `Payment` model — universal statuses: PENDING / COMPLETED / FAILED / REFUNDED / OVERDUE / CANCELLED
- [x] Payment methods: EPOINT / BANK_TRANSFER / CASH / ONLINE
- [x] `MonthlySubscription` model — ACTIVE / PAUSED / CANCELLED
- [x] **ePoint payment gateway** full integration
  - [x] Payment initiation (`EPointInitiateView`)
  - [x] Success callback (`EPointSuccessView`)
  - [x] Error callback (`EPointErrorView`)
  - [x] Server-to-server webhook (`EPointCallbackView`) — with signature verification
- [x] Invoice system — automatic numbering
- [x] `PaymentService.create_lesson_payment()` — 25 AZN per lesson, 24-hour limit
- [x] `PaymentService.create_monthly_payment()` — `lessons_per_week × 4 × 25 AZN`
- [x] Overdue payment tracking (OVERDUE status)

---

### 🔔 5. Notification System (`apps/notifications/`)
**Status: ⚠️ 70% Complete**

- [x] `Notification` model — types: BOOKING_CONFIRMED / LESSON_REMINDER / PAYMENT_DUE / REPO_CREATED / GENERAL
- [x] JSON `data` field for additional context
- [x] Notification list view (pagination: 30)
- [x] "Mark all as read" (HTMX-powered)
- [x] Django Channels + WebSocket routing configuration
- [x] Real-time badge counter via WebSocket (`notifications.js`)
- [x] Celery tasks: lesson reminders, booking confirmation emails
- [ ] SMS notifications (Twilio) — TODO
- [ ] HTML email templates — TODO

---

### 🐙 6. GitHub Integration (`apps/github_integration/`)
**Status: ✅ 95% Complete**

- [x] `StudentRepository` model — PENDING / CREATING / CREATED / FAILED / ARCHIVED
- [x] `GitHubService.create_student_repository()` — private repo creation
- [x] Add student as collaborator (push access)
- [x] Repo naming format: `{first-last}-{course-slug}`
- [x] Error handling + status tracking
- [x] Organization and personal repo support

---

### 📝 7. Assessment System (`apps/assessments/`)
**Status: ✅ 85% Complete**

- [x] `Assessment` model — types: QUIZ / HOMEWORK / PROJECT / EXAM
- [x] Score tracking: `score / max_score`, `percentage` property
- [x] GitHub/file submission URL
- [x] Teacher feedback field
- [x] Assessment list (students see only their own)
- [x] Teacher grades submissions (`AssessmentGradeView`)
- [x] Due date (`due_date`) + submission date (`submitted_at`)

---

### 🎫 8. Support Ticket System (`apps/support/`)
**Status: ✅ 90% Complete**

- [x] `Ticket` model — OPEN / IN_PROGRESS / RESOLVED / CLOSED
- [x] Priority levels: LOW / MEDIUM / HIGH / URGENT
- [x] `TicketMessage` — multi-message conversation thread
- [x] Teacher/student message distinction (`is_from_teacher`)
- [x] Ticket list, create, and detail views
- [x] Auto-scroll to latest message on page load (`support.js`)
- [x] Resolution date (`resolved_at`) tracking

---

### 📊 9. Analytics Dashboard (`apps/analytics/`)
**Status: ✅ 85% Complete**

- [x] `DashboardView` — main teacher control panel
- [x] KPI cards: active students, pending registrations, monthly bookings
- [x] Revenue calculation — completed payments for current month
- [x] Overdue payment counter
- [x] Next 5 upcoming lessons
- [x] 6-month monthly revenue trend (ApexCharts)
- [x] 6-month monthly booking trend (ApexCharts)
- [x] Animated KPI counters (`dashboard.js`)
- [x] Live clock widget (`dashboard.js`)
- [ ] Excel / PDF export — TODO

---

### 🔐 10. Authentication & Security
**Status: ✅ 90% Complete**

- [x] django-allauth — full auth system (login, logout, password reset)
- [x] Google OAuth2 social login
- [x] 2FA (Two-Factor Authentication) — django-otp
- [x] JWT tokens — djangorestframework-simplejwt
- [x] `LoginRequiredMixin` on all protected views
- [x] `TeacherRequiredMixin` for teacher-only operations
- [x] `StudentOwnerMixin` — students access only their own resources
- [x] CSRF protection
- [x] CORS configuration

---

### 🌐 11. REST API (`/api/v1/`)
**Status: ⚠️ 60% Complete**

- [x] Django REST Framework configuration
- [x] drf-spectacular — API schema generation
- [x] JWT authentication on API endpoints
- [x] Bookings API endpoints
- [x] Users API endpoints (partial)
- [x] Courses API endpoints (partial)
- [x] Payments API endpoints (partial)
- [ ] Full Swagger/OpenAPI documentation — TODO

---

### ⚙️ 12. Infrastructure & Configuration
**Status: ✅ 90% Complete**

- [x] `config/settings/base.py` — base configuration
- [x] `config/settings/development.py` — local development environment
- [x] `config/settings/production.py` — production configuration
- [x] Docker + Docker Compose (development + production)
- [x] `Dockerfile` + `entrypoint.sh`
- [x] `docker-compose.prod.yml` — production stack
- [x] WhiteNoise — static file serving
- [x] DigitalOcean Spaces (S3) — media file storage
- [x] Health check endpoint (`/health/`)
- [x] Django Debug Toolbar (development only)
- [x] Rosetta — translation interface
- [x] i18n — multilingual support (az/en/ru)
- [x] Celery Beat — scheduled tasks
- [x] Django Channels (Daphne ASGI server)
- [x] pytest + pytest-django configuration

---

## 📁 Project Structure

```
lms_platform/
├── apps/
│   ├── users/              ✅ CRM + student management
│   ├── courses/            ✅ Course + module management
│   ├── bookings/           ✅ Calendly-style reservations
│   ├── payments/           ✅ ePoint payment gateway
│   ├── github_integration/ ✅ Automatic GitHub repo
│   ├── youtube/            📋 YouTube API
│   ├── video_conferencing/ 📋 Google Meet API
│   ├── notifications/      ⚠️ Notification system (partial)
│   ├── support/            ✅ Support ticket system
│   ├── analytics/          ✅ Dashboard analytics
│   └── assessments/        ✅ Assessment & grading
├── config/                 ✅ Django settings
├── core/                   ✅ Utilities, mixins, permissions
├── templates/              ✅ Tailwind CSS + HTMX templates
├── static/                 ✅ CSS (Tailwind output) + JS modular files
├── locale/                 ✅ az/en/ru translations
└── tests/                  ✅ pytest-django tests
```

---

## 🧩 Frontend JS Module Structure

All inline `<script>` blocks have been extracted into dedicated module files under `static/js/`:

| File | Purpose |
|------|---------|
| `static/js/notifications.js` | WebSocket real-time notification badge updater |
| `static/js/dashboard.js` | Alpine.js: `liveClock()` + animated `counter()` |
| `static/js/charts.js` | ApexCharts: 6-month revenue & bookings chart |
| `static/js/bookings.js` | Alpine.js: `bookingCalendar()` — Calendly-style UI |
| `static/js/auth.js` | Alpine.js: `pricingCalc()` — 25 AZN × weekly lessons |
| `static/js/courses.js` | Alpine.js: `courseForm()` — image drag-and-drop preview |
| `static/js/support.js` | Auto-scroll to latest chat message on page load |

> Django template variables (`calendar_data`, `csrf_token`, etc.) are passed to JavaScript via `data-*` attributes on container elements, keeping templates and scripts cleanly separated.

---

## 📊 Overall Progress

| Module                   | Status | Progress |
|--------------------------|--------|----------|
| User Management          | ✅     | 100%     |
| Course Management        | ✅     | 90%      |
| Lesson Booking           | ✅     | 95%      |
| Payment System (ePoint)  | ✅     | 95%      |
| Notification System      | ⚠️     | 70%      |
| GitHub Integration       | ✅     | 95%      |
| Assessment System        | ✅     | 85%      |
| Support Ticket System    | ✅     | 90%      |
| Analytics Dashboard      | ✅     | 85%      |
| Authentication / Auth    | ✅     | 90%      |
| REST API                 | ⚠️     | 60%      |
| Infrastructure / DevOps  | ✅     | 90%      |

---

## 🔜 Remaining TODO

- [ ] Complete HTML email templates (SendGrid/Mailgun)
- [ ] SMS notifications (Twilio integration)
- [ ] Full WebSocket consumer implementation
- [ ] Analytics Excel/PDF export
- [ ] Full Swagger/OpenAPI documentation
- [ ] YouTube API integration
- [ ] Google Calendar synchronization
- [ ] Stripe payment gateway as alternative
- [ ] Increase test coverage (target: >80%)
- [ ] Course lesson material detail pages

---

## 🚀 Local Setup

```bash
# 1. Activate virtual environment
.venv-1\Scripts\activate

# 2. Install dependencies
pip install -r requirements/development.txt

# 3. Apply migrations
python manage.py migrate --settings=config.settings.local

# 4. Create superuser
python manage.py runscript create_superuser --settings=config.settings.local

# 5. Run the server
python manage.py runserver --settings=config.settings.local
```

```bash
# Run with Docker
docker-compose up --build
```

---

## 💰 Business Rules

```python
LESSON_PRICE         = Decimal('25.00')   # FIXED — DO NOT CHANGE!
CANCELLATION_HOURS   = 24                 # Minimum hours before cancellation
MAX_LESSONS_PER_WEEK = 7                  # Maximum lessons per week

# Monthly subscription calculation
# Example: 2 lessons/week → 2 × 4 × 25 = 200 AZN/month
monthly_price = lessons_per_week * 4 * 25
```

---

*LMS Platform — Django 5.0+ | PostgreSQL | Redis | Celery | HTMX | Alpine.js*  
*AI Model: Claude Sonnet 4.6 | Last updated: 08.05.2026*
