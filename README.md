# LMS Platform — Personal Online Learning Management System

> A **one-teacher + multiple students** model for 1-on-1 personalized online tutoring.  
> **AI Model**: Claude Sonnet 4.6 | **Framework**: Django 5.0+ | **Language**: English

---

## About the Project

This LMS (Learning Management System) platform is designed to help a single teacher efficiently manage multiple students in a **1-on-1 online tutoring format**. The system automates the entire teaching workflow — from lesson booking and payments to GitHub repository creation and analytics.

### Business Model Overview

| Parameter | Value |
|---|---|
| Teaching format | 1-on-1 private lessons only |
| Delivery method | Online (Google Meet) |
| Lesson price | **25 AZN / lesson (FIXED)** |
| Payment Model 1 | Monthly subscription (lessons/week × 4 × 25 AZN) |
| Payment Model 2 | Pay-as-you-go (per lesson) |
| Number of teachers | 1 (single-teacher system) |

---

## Technical Architecture

```
Architecture:   Django Fullstack Monolithic
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

## Project Structure

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
│   ├── users/              # User management
│   ├── courses/            # Course + material management
│   ├── bookings/           # Lesson scheduling (Calendly-style)
│   ├── payments/           # Monthly/per-lesson payment system
│   ├── github_integration/ # GitHub API — student repositories
│   ├── youtube/            # YouTube Data API v3
│   ├── video_conferencing/ # Google Meet API
│   ├── notifications/      # Email/SMS/real-time notifications
│   ├── support/            # Support ticket system
│   ├── analytics/          # Dashboard analytics
│   └── assessments/        # Assessment & grading system
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

## Key Features

### 1. User Management (`apps/users/`)
- **Teacher**: Full system control, access to all student data
- **Student**: Personal profile, course access, lesson booking
- Registration → Teacher approval → GitHub repo creation → Email notification flow
- Two-factor authentication (2FA)
- Social login support (optional)

### 2. Course Management (`apps/courses/`)
- Course → Module → Lesson hierarchy
- Automatic YouTube video metadata fetching
- Material sync with GitHub integration
- Drag & drop ordering, version control
- PDF, code snippets, and rich text support

### 3. Lesson Booking (`apps/bookings/`)
- Calendly-style time slot selection
- Real-time availability display
- Automatic Google Meet link generation
- Reminders 24 hours and 1 hour before the lesson (Celery tasks)
- Cancellation policy (minimum 24 hours in advance)

### 4. Payment System (`apps/payments/`)
- **Model 1 — Monthly**: lessons/week × 4 × 25 AZN (prepaid)
- **Model 2 — Per Lesson**: 25 AZN after each lesson (24-hour payment window)
- Stripe integration (international cards)
- Local payment methods (e-Manat, Milliköçürmə)
- Automatic invoice generation (PDF)
- Overdue payment → next lesson blocked

### 5. GitHub Integration (`apps/github_integration/`)
- Automatic **private repository** creation upon student approval
- Repository naming convention: `{student-full-name}-{course-slug}`
- Default folders: `lessons/`, `projects/`, `resources/`
- Auto-generated README.md with student details
- Teacher + student collaborator access
- Async execution via Celery task (3 retries, 60s interval)

### 6. YouTube Integration (`apps/youtube/`)
- Automatic metadata fetching (title, duration, thumbnail)
- Embedded player (watch within the platform)
- Redis caching (24-hour TTL)
- Supported URL formats: `youtube.com/watch?v=`, `youtu.be/`

### 7. Notification System (`apps/notifications/`)
- Email (SendGrid / Mailgun / AWS SES)
- SMS reminders (optional)
- Real-time in-app notifications (Django Channels + WebSocket)
- Bulk email and individual messaging

### 8. Support System (`apps/support/`)
- Ticket lifecycle (New → In Review → Answered → Resolved → Closed)
- Rich text editor, file attachments, code formatting
- FAQ database, template responses
- Average response time analytics

### 9. Assessments (`apps/assessments/`)
- Multiple choice, true/false, and code-writing questions
- Automatic grading
- Digital certificates and achievement badges

### 10. Analytics (`apps/analytics/`)
- Daily/Monthly revenue report (25 AZN × number of lessons)
- Breakdown by payment model (monthly vs. per-lesson)
- Student churn/retention analysis
- Slot utilization rate (booked vs. available)
- Visual dashboards with Chart.js

---

## Payment Logic (Business Rules)

```python
from decimal import Decimal

LESSON_PRICE         = Decimal('25.00')  # FIXED — never changes!
CANCELLATION_HOURS   = 24               # Minimum hours required for cancellation
MAX_LESSONS_PER_WEEK = 7                # Maximum lessons allowed per week

def calculate_monthly_price(lessons_per_week: int) -> Decimal:
    """Monthly payment: lessons per week × 4 weeks × 25 AZN"""
    return Decimal(lessons_per_week) * 4 * LESSON_PRICE

# Example: 2 lessons/week → 2 × 4 × 25 = 200 AZN/month
```

---

## Third-Party Integrations

| Service | Purpose | Library |
|---|---|---|
| GitHub API | Student repository creation | `PyGithub` |
| YouTube Data API v3 | Video metadata | `google-api-python-client` |
| Google Meet | Lesson video link | `google-auth` |
| Google Calendar | Calendar synchronization | `google-api-python-client` |
| Stripe | Payment processing | `stripe` |
| SendGrid / Mailgun | Email delivery | `django-anymail` |
| Twilio | SMS notifications | `twilio` |
| DigitalOcean Spaces | File storage | `django-storages` |

---

## Deployment

### DigitalOcean App Platform (Recommended)
- Python 3.11 native runtime
- Managed PostgreSQL 15+ ($15/month)
- Managed Redis 7+ ($15/month)
- Spaces CDN ($5/month — 250GB)
- Gunicorn + Whitenoise
- Automatic SSL certificates
- Push-to-deploy (GitHub integration)

### Railway (Alternative)
- Deploy with `railway up`
- PostgreSQL + Redis included
- Starting at $5/month

---

## Installation

```bash
# 1. Clone the repository
git clone <repo-url>
cd lms_platform

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit the .env file with your values

# 5. Run database migrations
python manage.py migrate

# 6. Create a superuser
python manage.py createsuperuser

# 7. Start the development server
python manage.py runserver
```

### Environment Variables

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

## Celery Workers

```bash
# Start background worker
celery -A config worker -l info -Q default,notifications,github

# Scheduled tasks (reminders, monthly payments)
celery -A config beat -l info

# Flower (monitoring dashboard)
celery -A config flower
```

---

## Testing

```bash
# Run all tests
pytest

# Coverage report (target: >80%)
pytest --cov=apps --cov-report=html

# Run tests for a specific app
pytest apps/bookings/
pytest apps/payments/
```

---

## Code Standards

- **PEP 8** (Black formatter, 88 characters per line)
- **isort** (import ordering)
- **Type hints** — required on all public methods
- **Docstrings** — Args + Returns format
- **BaseModel** — all models use UUID primary key + timestamps
- **verbose_name** — defined in Azerbaijani in the source code (localized for end users)
- **`@transaction.atomic`** — applied to all critical database operations

---

## Scaffold Status — 28.02.2026

All files listed below have been created and pushed to GitHub (**120 files, 5,196 lines**).

### `config/` — Django Configuration

| File | Purpose |
|------|---------|
| `config/settings/base.py` | INSTALLED_APPS, Redis, Celery, LMS constants |
| `config/settings/development.py` | Debug toolbar, console email backend |
| `config/settings/production.py` | Sentry, DigitalOcean Spaces, HTTPS settings |
| `config/urls.py` | Root URL configuration aggregating all app URLs |
| `config/asgi.py` | Django Channels ASGI entry point (WebSocket) |
| `config/celery.py` | Celery app, 4 queues (default/notifications/github/payments) |

### `core/` — Shared Utilities

| File | Purpose |
|------|---------|
| `core/utils.py` | `LESSON_PRICE`, `calculate_monthly_price()`, `get_repo_name()`, `generate_invoice_number()`, `extract_youtube_video_id()` |
| `core/mixins.py` | `TeacherRequiredMixin`, `StudentOwnerMixin`, `HTMXMixin` |
| `core/permissions.py` | DRF permissions: `IsTeacher`, `IsStudent`, `IsOwnerOrTeacher` |
| `core/validators.py` | `validate_future_datetime`, `validate_youtube_url`, `validate_github_username`, `validate_phone_number` |
| `core/context_processors.py` | `lms_globals` — injects LESSON_PRICE, APP_NAME, and user role into templates |

### `apps/users/` — User System

| File | Purpose |
|------|---------|
| `models.py` | `BaseModel` (UUID+timestamps), `User` (AbstractBaseUser), `StudentProfile` |
| `services.py` | `UserService.register_student()`, `approve_student()` |
| `signals.py` | `post_save` → auto-creates `StudentProfile` for new students |
| `forms.py` | `StudentRegistrationForm`, `StudentProfileUpdateForm` |
| `views.py` | `StudentRegisterView`, `ProfileView`, `StudentProfileUpdateView` |
| `api_urls.py` | `/api/v1/me/` — current user JSON endpoint |

### `apps/courses/` — Course Management

| File | Purpose |
|------|---------|
| `models.py` | `Category`, `Course`, `Enrollment`, `Module`, `Lesson` (MaterialType choices) |
| `services.py` | `CourseService.create_lesson_with_youtube()` |
| `views.py` | `CourseListView`, `CourseDetailView` |
| `api_urls.py` | `/api/v1/courses/` — active courses JSON endpoint |

### `apps/bookings/` — Booking System

| File | Purpose |
|------|---------|
| `models.py` | `AvailabilitySlot`, `Booking` (Status + LessonType choices, `can_cancel` property) |
| `services.py` | `BookingService.create_booking()` (`select_for_update`), `cancel_booking()` |
| `tasks.py` | `send_lesson_reminder_task` (max_retries=3, queue=notifications) |
| `views.py` | `BookingListView`, `AvailableSlotsView`, `BookingCreateView` |
| `api_views.py` + `api_urls.py` | `/api/v1/bookings/` REST endpoint |

### `apps/payments/` — Payment System

| File | Purpose |
|------|---------|
| `models.py` | `Payment` (Status, PaymentMethod, auto invoice_number), `MonthlySubscription` |
| `services.py` | `PaymentService.create_lesson_payment()`, `process_stripe_payment()` |
| `tasks.py` | `check_overdue_payments_task`, `send_overdue_payment_reminders_task` |
| `views.py` | `PaymentListView` (teacher + student views) |
| `api_urls.py` | `/api/v1/payments/` REST endpoint |

### `apps/github_integration/` — GitHub API

| File | Purpose |
|------|---------|
| `models.py` | `StudentRepository` (Status choices, idempotency guard) |
| `services.py` | `GitHubService.create_student_repository()`, `repo_exists()` |
| `tasks.py` | `create_student_repo_task` (max_retries=3, 60s delay, idempotency check) |

### `apps/youtube/` — YouTube API

| File | Purpose |
|------|---------|
| `services.py` | `YouTubeService` — Redis 24h cache, ISO 8601 duration parser, thumbnail fetching |

### `apps/video_conferencing/` — Google Meet

| File | Purpose |
|------|---------|
| `services.py` | `GoogleMeetService.create_meeting()` — Calendar API, attendee invite |
| `tasks.py` | `create_meet_link_task` (max_retries=3, idempotency check) |

### `apps/notifications/` — Notification System

| File | Purpose |
|------|---------|
| `models.py` | `Notification` (7 types, `is_read` flag, JSON data field) |
| `services.py` | `NotificationService` — booking confirmation, lesson reminder, payment reminder |
| `tasks.py` | `send_booking_confirmation`, `send_lesson_reminder`, `send_payment_receipt`, `send_student_approval_email` |
| `consumers.py` | `NotificationConsumer` — AsyncWebsocketConsumer (unread count, mark_read) |
| `routing.py` | `ws/notifications/` WebSocket route — imported by `config/asgi.py` |
| `views.py` | `NotificationListView`, `MarkAllReadView` (HTMX-compatible) |

### `apps/support/` — Support Tickets

| File | Purpose |
|------|---------|
| `models.py` | `Ticket` (Status + Priority choices), `TicketMessage` |
| `forms.py` | `TicketCreateForm`, `TicketMessageForm` |
| `views.py` | `TicketListView`, `TicketCreateView`, `TicketDetailView` |

### `apps/analytics/` — Dashboard

| File | Purpose |
|------|---------|
| `views.py` | `DashboardView` (KPIs: students, lessons, revenue, overdue payments), `StudentDashboardView` |

### `apps/assessments/` — Grading System

| File | Purpose |
|------|---------|
| `models.py` | `Assessment` (Quiz/Homework/Project/Exam, `percentage` property) |
| `forms.py` | `AssessmentCreateForm`, `AssessmentGradeForm` |
| `views.py` | `AssessmentListView`, `AssessmentCreateView`, `AssessmentGradeView` |

### `templates/` — HTML Templates

| Template | Purpose |
|--------|---------|
| `base.html` | Bootstrap 5.3 + HTMX + Alpine.js + Chart.js + WebSocket toast notifications |
| `partials/navbar.html` | Notification badge, user dropdown menu |
| `partials/sidebar.html` | Role-based navigation menu (teacher/student) |
| `partials/pagination.html` | Universal Bootstrap pagination component |
| `auth/login.html` | Allauth-compatible login form |
| `analytics/dashboard.html` | Teacher KPI cards + upcoming lessons table |
| `bookings/booking_list.html` | Lessons table with status badges and Meet links |
| `payments/payment_list.html` | Payments table with status badges and invoice numbers |

### Deploy & Test

| File | Purpose |
|------|---------|
| `Dockerfile` | Python 3.11-slim, non-root user, Daphne ASGI server |
| `docker-compose.yml` | web + db + redis + celery_worker + celery_beat services |
| `.do/app.yaml` | DigitalOcean App Platform spec (3 services + Managed PostgreSQL) |
| `pytest.ini` | DJANGO_SETTINGS_MODULE, coverage config, --cov-fail-under=50 |
| `setup.cfg` | flake8 (88 chars), isort (profile=black), mypy (django-stubs) |
| `conftest.py` | `teacher_user`, `student_user`, `available_slot`, `reserved_slot`, `past_slot` fixtures |
| `tests/test_booking_service.py` | BookingService — 4 tests (success, reserved slot, past slot, cancellation) |
| `tests/test_utils.py` | core utils — 6 tests (LESSON_PRICE, calculate, repo_name, youtube_id, azn format, invoice) |

---

## Documentation

- [Full Project Plan](docs/project.md) — Detailed description of all features
- [Copilot Instructions](.github/copilot-instructions.md) — AI coding standards
- [Agent List](.github/copilot-agents.md) — Specialized agent definitions
- [Prompt Library](.github/copilot-prompts.md) — Ready-to-use prompt templates

---

## License

This project is for personal use. All rights reserved.

---

*LMS Platform — Django 5.0+ | PostgreSQL | Redis | Celery | HTMX | Alpine.js*  
*AI Model: Claude Sonnet 4.6 | Scaffold completed: 28.02.2026*
