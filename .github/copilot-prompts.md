<!-- filepath: .github/copilot-prompts.md -->
# GitHub Copilot Prompt Kitabxanası — LMS Platformu

> **AI Model**: Claude Sonnet 4.6  
> **Framework**: Django 5.0+ | Python 3.11+  
> **İstifadə**: Bu prompt-ları Copilot Chat-da birbaşa köçürüb istifadə edin

---

## 📦 MODUL YARATMA PROMPT-LARI

---

### P-001 — Yeni Django App Yaratma

```
LMS platformu üçün `{app_name}` adlı yeni Django app yarat.

Texniki Stack:
- Django 5.0+ / Python 3.11+
- PostgreSQL ORM
- BaseModel (UUID pk, created_at, updated_at)
- Azərbaycan dilli verbose_name-lər

Tələblər:
1. apps/{app_name}/ strukturunu yarat:
   - models.py       (BaseModel-dən miras alan modellər)
   - views.py        (LoginRequiredMixin ilə CBV-lər)
   - forms.py        (Bootstrap 5 widgets)
   - services.py     (business logic, @transaction.atomic)
   - urls.py         (app_name namespace ilə)
   - admin.py        (ModelAdmin ilə)
   - tasks.py        (Celery shared_task-lar)
   - tests/
       - __init__.py
       - conftest.py
       - test_models.py
       - test_services.py
       - test_views.py

2. Bütün modellər TextChoices enum istifadə etsin
3. İmportlar isort standartına uyğun olsun
4. Hər sinif və funksiya üçün docstring yaz
5. Type hints mütləq olsun
```

---

### P-002 — Model + Migration Yaratma

```
LMS platformu üçün aşağıdakı tətbiqin modelini yarat:

Tətbiq: {app_name}
Model adı: {ModelName}
Sahələr:
{fields_description}

Qaydalar:
- BaseModel-dən miras al (UUID pk + timestamps)
- Bütün verbose_name-lər Azərbaycan dilindədir
- Status field-i varsa TextChoices enum istifadə et
- ForeignKey-lər üçün related_name müəyyən et
- Meta class-da: db_table, verbose_name, verbose_name_plural, ordering, indexes
- __str__ metodu mənalı string qaytarsın
- Gərəkli property-lər əlavə et
- get_absolute_url() metodu əlavə et
```

---

### P-003 — CRUD View Dəsti Yaratma

```
`{ModelName}` modeli üçün tam CRUD view dəsti yarat:

Model: apps/{app_name}/models.py → {ModelName}

Yaradılacaq view-lar:
1. {ModelName}ListView     — siyahı (paginate_by=20)
2. {ModelName}CreateView   — yaratma formu
3. {ModelName}DetailView   — ətraflı baxış
4. {ModelName}UpdateView   — redaktə
5. {ModelName}DeleteView   — silmə (confirm page)

Hər view üçün:
- LoginRequiredMixin əlavə et
- select_related / prefetch_related optimize et
- get_context_data-da page_title Azərbaycanca olsun
- Success mesajları Azərbaycanca olsun
- HTMX sorğusu üçün partial template dəstəyi
- Teacher üçün TeacherRequiredMixin, tələbə üçün StudentOwnerMixin

URL-lər:
- app_name='bookings' namespace
- UUID pk parametri
- HTMX endpoint-ləri ayrıca

Template path-ləri:
- templates/{app_name}/{model_name_lower}_list.html
- templates/{app_name}/{model_name_lower}_form.html
- templates/{app_name}/{model_name_lower}_detail.html
- templates/{app_name}/{model_name_lower}_confirm_delete.html
```

---

### P-004 — Django REST API Endpoint

```
`{ModelName}` üçün Django REST Framework API endpoint yarat:

Tələblər:
1. ModelSerializer (bütün öz field-lər + computed field-lər)
2. ViewSet (ListCreateAPIView + RetrieveUpdateDestroyAPIView)
3. IsAuthenticated permission
4. Pagination (PageNumberPagination, page_size=20)
5. Filter: django-filters ilə
6. Axtarış: SearchFilter ilə
7. Sıralama: OrderingFilter ilə
8. Throttling: user=100/day, anon=20/day

URL: /api/v1/{app_name}/{model_lower}/
```

---

## 🔗 İNTEQRASİYA PROMPT-LARI

---

### P-010 — GitHub Repository Avtomatik Yaratma

```
LMS-də tələbə qeydiyyatı təsdiqləndiyi zaman GitHub repository avtomatik yaratsın:

İş axını:
1. Müəllim tələbəni təsdiqləyir (Student.status → 'active')
2. `create_student_github_repo` Celery task işə düşür
3. PyGithub ilə private repo yaradılır
4. Repo adı formatı: `{student-ad-soyad}-{kurs-slug}`
5. Default qovluqlar: lessons/, projects/, resources/
6. README.md avtomatik yazılır (tələbə məlumatları ilə)
7. Tələbəyə collaborator hüququ verilir (push permission)
8. Repo URL Student modelinə saxlanılır
9. Tələbəyə email bildirişi göndərilir (repo linki ilə)

Texniki detallar:
- apps/github_integration/services.py → GitHubService sinifi
- apps/github_integration/tasks.py → Celery task
- GITHUB_TOKEN env dəyişəni ilə autentifikasiya
- Xəta halında 3 dəfə retry (60 saniyə interval)
- Hər addım logger.info() ilə log-lanır
```

---

### P-011 — Google Meet Link Yaratma

```
Dərs rezervasiyası təsdiqləndiyi zaman Google Meet linki avtomatik yaratsın:

İş axını:
1. Booking.status → 'confirmed' olduqda signal işə düşür
2. Google Calendar API ilə event yaradılır
3. Google Meet linki alınır
4. Booking.zoom_link field-inə saxlanılır
5. Həm tələbəyə həm müəllimə email göndərilir (Meet linki ilə)
6. Google Calendar-da hər iki tərəfin kalendarına əlavə edilir

Texniki:
- apps/video_conferencing/services.py → GoogleMeetService
- google-auth, google-api-python-client istifadə et
- OAuth2 credentials Django settings-dən alınsın
- Dərs müddəti: 60 dəqiqə (default)
- Alert: 24 saat + 1 saat əvvəl xatırlatma
```

---

### P-012 — YouTube Video İnteqrasiyası

```
Dərs materialına YouTube linki əlavə edildikdə avtomatik video məlumatlarını çəksin:

İş axını:
1. Müəllim YouTube URL daxil edir
2. YouTube Data API v3 ilə metadata çəkilir:
   - Başlıq (title)
   - Müddət (duration — ISO 8601 → dəqiqə)
   - Thumbnail URL
   - Kanal adı
   - Video ID
3. Məlumatlar CourseMaterial modelinə saxlanılır
4. Template-də embedded player göstərilir

Texniki:
- apps/youtube/services.py → YouTubeService
- YOUTUBE_API_KEY env dəyişəni
- URL formatları: youtube.com/watch?v=, youtu.be/, youtube.com/embed/
- Keşləmə: Redis 24 saat (dəyişilməyən məlumatlar)
```

---

### P-013 — Stripe Ödəniş İnteqrasiyası

```
LMS üçün Stripe ödəniş sistemini inteqrasiya et:

Ödəniş Modelləri:
1. Aylıq Abunə:
   - Stripe Subscription (recurring)
   - Məbləğ: həftəlik_dərs × 4 × 25 AZN
   - Ayın 1-i avtomatik çəkilir
   - Webhook: invoice.payment_succeeded / invoice.payment_failed

2. Dərs Əsaslı (Pay-as-you-go):
   - Stripe PaymentIntent (one-time)
   - Hər dərs bitimindən sonra 25 AZN
   - Webhook: payment_intent.succeeded

Texniki:
- apps/payments/services.py → StripeService
- Webhook endpoint: /payments/stripe/webhook/
- STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET env-dən
- İdempotency key hər request üçün
- Xəta halında Payment.status → 'failed' + email bildiriş
```

---

## 🎨 TEMPLATE PROMPT-LARI

---

### P-020 — Dashboard Template

```
Müəllim dashboard template-i yarat: templates/dashboard/teacher_dashboard.html

Bölmələr:
1. Statistika kartları (bu gün / bu həftə / bu ay):
   - Ümumi tələbə sayı
   - Bu günkü dərslər
   - Gözlənilən ödənişlər
   - Gecikmiş ödənişlər

2. Bugünkü dərslər cədvəli (HTMX ilə canlı yenilənən)

3. Son qeydiyyatlar (son 5 tələbə)

4. Ödəniş qrafiki (Chart.js — son 30 gün)

5. Tez əməliyyatlar:
   - Yeni tələbə əlavə et
   - Dərs planla
   - Ödəniş qeyd et

Texniki:
- Bootstrap 5.3 grid sistemi
- HTMX hx-trigger="every 30s" ilə canlı yeniləmə
- Alpine.js x-data ilə tab management
- Azərbaycan dilli bütün mətnlər
- Responsive (mobile-first)
```

---

### P-021 — Booking Calendar Template

```
Tələbə üçün dərs rezervasiya calendar template-i yarat:

Komponentlər:
1. Aylıq calendar görünüşü (Bootstrap grid)
2. Mövcud slotların rənglə göstərilməsi:
   - Yaşıl: mövcud slot
   - Sarı: seçilmiş slot
   - Qırmızı: dolu / keçmiş
3. Slot seçimi → HTMX ilə form yüklənməsi
4. Rezervasiya formu (modal):
   - Mövzu daxil et
   - Qeyd əlavə et
   - Təsdiqlə
5. Uğurlu rezervasiya → konfirmasiya mesajı

HTMX:
- Ay dəyişimi: hx-get="/bookings/htmx/calendar/?month={month}"
- Slot seçimi: hx-get="/bookings/htmx/slot/{id}/"
- Form submit: hx-post="/bookings/create/"
- Target: #calendar-container, #booking-modal

Alpine.js:
- x-data="{ selectedSlot: null, showModal: false }"
```

---

### P-022 — Tələbə Profil Template

```
Tələbə profil səhifəsi template-i yarat: templates/users/student_profile.html

Bölmələr:
1. Profil başlığı:
   - Avatar (default: baş hərflər)
   - Ad, soyad, email
   - Üzv olma tarixi
   - GitHub repo linki

2. Statistika:
   - Tamamlanmış dərslər
   - Növbəti dərs tarixi
   - Ödəniş modeli (badge)
   - Balans / borc məlumatı

3. Son dərslər (son 5):
   - Tarix, mövzu, status badge
   - Meet link (gəlecək dərslər üçün)
   - Recording link (keçmiş dərslər)

4. Ödəniş tarixi (cədvəl):
   - Tarix, məbləğ, status, metod

5. Kurs tərəqqisi (progress bar)

Texniki:
- Bootstrap 5 card layout
- HTMX ilə lazy-load bölmələri
- Azərbaycan dilli bütün mətnlər
```

---

## 🔧 API / BACKEND PROMPT-LARI

---

### P-030 — Availability Slot Sistemi

```
Müəllim üçün uyğun vaxt slot sistemi yarat (Calendly tipli):

Modellər:
1. AvailabilityTemplate — həftəlik şablon
   - Günlər (ChoiceField: B.e., Ç.a., Ç, C.a., C, Ş, B)
   - Başlanğıc saatı, bitmə saatı
   - Dərs müddəti (default: 60 dəq)
   - Buffer vaxtı dərslər arasında (default: 15 dəq)

2. AvailabilitySlot — konkret mövcud vaxt
   - start_time, end_time
   - is_reserved (bool)
   - Template-dən avtomatik generasiya

Servis:
- AvailabilityService.generate_slots_for_month(template, month, year)
  → Şablona əsasən aylıq slotlar generat edir
  → Mövcud rezervasiyaları xaric edir
  → Keçmiş tarixləri xaric edir
  → Boş slot siyahısı qaytarır

API:
- GET /api/v1/bookings/slots/?month=2026-03 → mövcud slotlar
- Response format: {date, slots: [{id, start, end, available}]}
```

---

### P-031 — Ödəniş Hesab Balansı

```
Tələbənin ödəniş balansını hesablayan sistem yarat:

Aylıq Model:
- Hər ayın 1-i ödəniş gəlməli
- Məbləğ = həftəlik_dərs_sayı × 4 × 25 AZN
- Tamamlanan dərs = 25 AZN çıxılır
- Balans = Ödənilmiş - Xərclənmiş
- Mənfi balans = borc

Pay-as-you-go Model:
- Hər dərs bitimindən sonra Payment yaradılır (status=pending)
- Ödəniş alındıqda status=completed
- Gecikmiş ödənişlər üçün bildiriş

Hesabat funksiyası:
def get_student_financial_summary(student_id: str) -> dict:
    return {
        'payment_model': '...',
        'total_paid': Decimal,
        'total_lessons_completed': int,
        'total_cost': Decimal,
        'balance': Decimal,        # müsbət = artıq ödəniş, mənfi = borc
        'pending_payments': list,
        'next_payment_date': date,
        'next_payment_amount': Decimal,
    }
```

---

### P-032 — Dərs Xatırlatma Sistemi

```
Avtomatik xatırlatma sistemi yarat:

Xatırlatma tipləri:
1. 24 saat əvvəl → tələbəyə email + SMS
2. 1 saat əvvəl  → tələbəyə push notification
3. Ödəniş günü   → müəllimə + tələbəyə email

Celery Beat cədvəli:
- Hər gün saat 09:00 — 24 saatlıq xatırlatmaları göndər
- Hər saat          — 1 saatlıq xatırlatmaları yoxla
- Hər ayın 28-i     — növbəti ay abunə bildirişi

Task-lar:
- send_24h_lesson_reminders()
- send_1h_lesson_reminders()
- send_monthly_payment_reminders()
- send_overdue_payment_alerts()

Email şablonları:
- templates/emails/lesson_reminder_24h.html
- templates/emails/lesson_reminder_1h.html
- templates/emails/payment_reminder.html
- templates/emails/overdue_payment.html

Dil: Azərbaycan dilində bütün email mətnləri
```

---

## 🧪 TEST PROMPT-LARI

---

### P-040 — Servis Testi Yaratma

```
`{ServiceName}` sinifi üçün tam test dəsti yarat:

Test faylı: apps/{app_name}/tests/test_services.py

Test ediləcəklər:
1. Uğurlu ssenari — düzgün nəticə qaytarır
2. Mövcud olmayan resurs — None / Exception qaytarır
3. Keçmiş tarix — qadağan edilmiş əməliyyat
4. İcazəsiz əməliyyat — PermissionDenied qaytarır
5. Database xətası — xəta düzgün handle edilir
6. External API xətası (mock) — retry mexanizmi işləyir

Fixture-lar (conftest.py-da):
- @pytest.fixture: student_user, teacher_user
- @pytest.fixture: active_course, available_slot, reserved_slot
- @pytest.fixture: confirmed_booking, pending_payment

Qaydalar:
- pytest.mark.django_db
- unittest.mock.patch ilə external service-lər mock et
- Factory Boy istifadə et (test data üçün)
- Hər test yalnız bir şeyi yoxlayır
- Assert mesajları izahlı olsun
```

---

### P-041 — View Testi Yaratma

```
`{ViewName}` üçün Django test client ilə view testi yarat:

Test faylı: apps/{app_name}/tests/test_views.py

Test ediləcəklər:
1. Autentifikasiyasız giriş → 302 redirect (login)
2. Tələbə öz resursuna baxır → 200 OK
3. Tələbə başqasının resursuna baxır → 403 Forbidden  
4. Müəllim bütün resurslara baxır → 200 OK
5. POST with valid data → 302 redirect (success)
6. POST with invalid data → 200 (form xətaları ilə)
7. HTMX request → partial template qaytarır

Hər test üçün:
- client.force_login(user)
- response.status_code yoxla
- response.context yoxla (template-ə doğru data gedir?)
- Redirect URL-i yoxla
- Azərbaycan dilli success mesajı yoxla
```

---

## 📊 ANALİTİKA PROMPT-LARI

---

### P-050 — Müəllim Dashboard Statistikaları

```
Müəllim dashboard üçün statistika hesablayan servis yarat:

apps/analytics/services.py → DashboardAnalyticsService

Metodlar:
1. get_today_summary() → dict
   - today_lessons_count
   - completed_today
   - cancelled_today
   - revenue_today

2. get_weekly_stats(week_start: date) → dict
   - lessons_per_day: {mon: 2, tue: 3, ...}
   - revenue_per_day: {mon: 50.0, ...}
   - completion_rate: 0.95

3. get_monthly_report(month: int, year: int) → dict
   - total_lessons
   - total_revenue
   - new_students
   - churn_students
   - avg_lessons_per_student

4. get_student_performance(student_id: str) → dict
   - attendance_rate
   - avg_assessment_score
   - lessons_completed
   - next_lesson_date

Keşləmə:
- Redis cache ilə 1 saatlıq keş
- cache_key formatı: f"analytics:{method_name}:{params_hash}"
```

---

## 🔒 TƏHLÜKƏSİZLİK PROMPT-LARI

---

### P-060 — Permission Sistemi

```
LMS üçün role-based permission sistemi yarat:

Rollər:
- teacher  : tam giriş (bütün tələbə, kurs, ödəniş məlumatları)
- student  : yalnız öz məlumatları

Permission Mixin-ləri (core/permissions.py):

1. TeacherRequiredMixin
   - Yalnız müəllim rolu
   - Başqaları → login redirect

2. StudentOwnerMixin  
   - Tələbə yalnız öz resursuna baxır
   - obj.student == request.user
   - Müəllim həmişə keçir

3. ActiveStudentMixin
   - student.status == 'active' olmalıdır
   - Deaktiv tələbə → xəbərdarlıq səhifəsi

4. PaymentRequiredMixin
   - Borclu tələbə → ödəniş xatırlatması
   - Yalnız dərs materiallarına girişi bloklayır

Django Middleware (optional):
- StudentPaymentCheckMiddleware
  → Hər request-də tələbənin balansını yoxla
  → 30 gündən çox borc varsa → xəbərdarlıq banner
```

---

## 📝 PROMPT İSTİFADƏ QAYDASI

1. **Prompt seç** — istədiyiniz ssenariyə uyğun P-XXX kod
2. **Placeholder-ları doldur** — `{app_name}`, `{ModelName}` kimi dəyişənləri əvəz et
3. **Copilot Chat-a yapışdır** — `@workspace` konteksti ilə
4. **Nəticəni yoxla** — layihə standartlarına uyğunluğu yoxla
5. **Test et** — `pytest` ilə dərhal test et

---

*LMS Platformu | Claude Sonnet 4.6 | Django 5.0+ | Azərbaycan*
