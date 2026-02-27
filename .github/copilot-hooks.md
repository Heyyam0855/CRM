<!-- filepath: .github/copilot-hooks.md -->
# GitHub Copilot Hooks — LMS Platformu

> **AI Model**: Claude Sonnet 4.6  
> **Framework**: Django 5.0+ | Python 3.11+  
> **Məqsəd**: Kod yazılarkən avtomatik işə düşən hook-lar, validasiyalar və tetikleyicilər

---

## 🪝 Hook Sisteminə Giriş

Bu sənəd LMS platformunda GitHub Copilot ilə inteqrasiya olunmuş hook-ları müəyyən edir.  
Hook-lar 3 səviyyədə işləyir:

```
┌─────────────────────────────────────────────────┐
│  1. PRE-GENERATION   → Kod yazmadan əvvəl       │
│  2. POST-GENERATION  → Kod yazıldıqdan sonra    │
│  3. VALIDATION       → Hər dəyişiklikdə yoxla  │
└─────────────────────────────────────────────────┘
```

---

## 🔵 PRE-GENERATION HOOKS

> Kod generasiyasından **əvvəl** işə düşür — kontekst hazırlığı

---

### H-PRE-001 — Yeni Model Yaratma

**Tetikleyici**: `class * (BaseModel)` yazıldıqda  
**Fəaliyyət**: Aşağıdakı şablonu avtomatik tamamla

```python
# AUTO-COMPLETE ŞABLONU:
import uuid
from django.db import models


class {ModelName}(BaseModel):
    """
    {ModelName} modeli.
    
    TODO: Bu model üçün docstring əlavə et.
    """

    class Status(models.TextChoices):
        # TODO: Status seçimlərini əlavə et
        pass

    # TODO: Field-ləri əlavə et

    class Meta:
        db_table            = '{app}_{model_lower}'
        verbose_name        = '{verbose_az}'
        verbose_name_plural = '{verbose_az_plural}'
        ordering            = ['-created_at']

    def __str__(self) -> str:
        return f"..."
```

**Yoxlanılacaqlar** (pre-check):
- [ ] `BaseModel` import edilib?
- [ ] `app_name` düzgündür?
- [ ] `verbose_name` Azərbaycan dilindədir?

---

### H-PRE-002 — Yeni View Yaratma

**Tetikleyici**: `class *View(` yazıldıqda  
**Fəaliyyət**: `LoginRequiredMixin` avtomatik əlavə et

```python
# AUTO-SUGGEST:
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import {ViewType}
from django.contrib import messages

class {ViewName}(LoginRequiredMixin, {ViewType}):
    """
    {Description}
    
    Requires: Authenticated user
    Template: {template_path}
    """
    model               = {Model}
    template_name       = '{app}/{model_lower}_{action}.html'
    context_object_name = '{model_lower}'  # və ya '{model_lower}s'

    def get_queryset(self):
        return (
            {Model}.objects
            .select_related(...)       # TODO: əlavə et
            .filter(...)               # TODO: əlavə et
        )
```

**Xəbərdarlıq**: `LoginRequiredMixin` yoxdursa → ⚠️ bildiriş

---

### H-PRE-003 — Service Metodu Yaratma

**Tetikleyici**: `def create_*`, `def update_*`, `def delete_*` yazıldıqda  
**Fəaliyyət**: `@transaction.atomic` → avtomatik təklif et

```python
# AUTO-SUGGEST:
from django.db import transaction
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class {ServiceName}:

    @transaction.atomic
    def {method_name}(self, ...) -> Optional[...]:
        """
        {Description}
        
        Returns:
            Uğurlu olduqda {type}, əks halda None
        """
        try:
            # TODO: İmplementasiya
            ...
        except Exception as exc:
            logger.error("{method_name} xətası: %s", exc, exc_info=True)
            return None
```

---

### H-PRE-004 — Celery Task Yaratma

**Tetikleyici**: `@shared_task` yazıldıqda  
**Fəaliyyət**: Tam task şablonunu generat et

```python
# AUTO-COMPLETE:
from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    queue='{queue_name}'           # notifications | default | github
)
def {task_name}(self, {params}: str) -> dict:
    """
    {Description}
    
    Args:
        {params}: {description}
    
    Returns:
        {'success': bool, 'message': str}
    """
    try:
        # TODO: İmplementasiya
        logger.info("{task_name} tamamlandı: %s", {params})
        return {'success': True}
    except Exception as exc:
        logger.error("{task_name} xətası: %s", exc, exc_info=True)
        raise self.retry(exc=exc)
```

---

## 🟢 POST-GENERATION HOOKS

> Kod yaradıldıqdan **sonra** işə düşür — keyfiyyət yoxlaması

---

### H-POST-001 — Model Yoxlaması

**Tetikleyici**: Yeni model sinifi tamamlandıqda  
**Yoxlanılacaqlar**:

```
✅ KEÇMƏ KRİTERİYALARI:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

□ BaseModel-dən miras alınıb?
  → Əks halda: "BaseModel-dən miras al (UUID pk + timestamps)"

□ verbose_name Azərbaycan dilindədir?
  → Əks halda: "verbose_name Azərbaycan dilindədir"

□ __str__ metodu var?
  → Əks halda: "__str__ metodu əlavə et"

□ Meta class var (db_table, ordering)?
  → Əks halda: "Meta class əlavə et"

□ ForeignKey-də related_name var?
  → Əks halda: "related_name əlavə et"

□ Status field-i varsa TextChoices istifadə edilir?
  → Əks halda: "TextChoices enum istifadə et"

□ Decimal field-lərdə max_digits, decimal_places var?
  → Əks halda: "max_digits=8, decimal_places=2 əlavə et"
```

---

### H-POST-002 — View Yoxlaması

**Tetikleyici**: View sinifi tamamlandıqda  
**Yoxlanılacaqlar**:

```
✅ KEÇMƏ KRİTERİYALARI:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

□ LoginRequiredMixin var?
  → Əks halda: ⚠️ "Autentifikasiya mixin-i əlavə et!"

□ get_queryset-də select_related var?
  → Tövsiyə: "N+1 probleminə diqqət et, select_related əlavə et"

□ Uğur mesajları Azərbaycan dilindədir?
  → Əks halda: messages.success mesajını Azərbaycanca yaz

□ Template path düzgündür?
  → Format: '{app_name}/{model_lower}_{action}.html'

□ HTMX sorğusu handle edilir?
  → Tövsiyə: "HTMX sorğuları üçün partial template dəstəyi əlavə et"
```

---

### H-POST-003 — ORM Sorğu Optimizasiya

**Tetikleyici**: `.filter()`, `.all()`, `.get()` istifadə edildikdə  
**Yoxlanılacaqlar**:

```python
# ❌ XƏBƏRDARLIQ — aşağıdakı pattern-lər aşkar edildikdə:

# 1. Loop içindəki sorğu
for lesson in lessons:
    print(lesson.student.name)     # ⚠️ N+1 — select_related istifadə et

# 2. select_related yoxdur
Lesson.objects.filter(status='scheduled')  # ⚠️ — FK-lər lazy load

# 3. .all() lazımsız istifadə
Model.objects.all().filter(...)    # ⚠️ — birbaşa .filter() yaz

# ✅ DÜZGÜN PATTERN:
Lesson.objects.select_related('student', 'course').filter(
    status=Lesson.Status.SCHEDULED
)
```

**Avtomatik Suggestion**:
- FK field-ləri varsa → `select_related` təklif et
- M2M field-ləri varsa → `prefetch_related` təklif et
- Count lazımdırsa → `annotate(Count(...))` təklif et

---

### H-POST-004 — Import Sırası Yoxlaması

**Tetikleyici**: Fayl saxlandıqda  
**Standart** (isort):

```python
# DÜZGÜN SIRALAMA:
# ─── 1. Standart kitabxana ───────────────────
import os
import uuid
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Optional, List, Dict, Any

# ─── 2. Üçüncü tərəf ─────────────────────────
import stripe
from celery import shared_task
from django.contrib.auth import get_user_model
from django.db import models, transaction
from django.utils import timezone

# ─── 3. Lokal ────────────────────────────────
from apps.payments.models import Payment
from apps.users.models import User
from core.permissions import TeacherRequiredMixin
from core.utils import generate_invoice_number
```

**Xəbərdarlıq**: Yanlış sıralama aşkar edildikdə → `isort` çalıştır

---

### H-POST-005 — Biznes Qayda Yoxlaması

**Tetikleyici**: Ödəniş, qiymət, dərs məntiqi yazıldıqda  
**Yoxlanılacaqlar**:

```python
# ✅ SABIT QİYMƏT YOXLAMASI
LESSON_PRICE = Decimal('25.00')   # ← Bu sabitdir, dəyişdirilməz!

# ❌ XƏBƏRDARLIQ — aşağıdakı pattern-lər:
price = 25           # ⚠️ Literal 25 → LESSON_PRICE sabitindən istifadə et
amount = 25.0        # ⚠️ Float deyil Decimal istifadə et
lesson_cost = 25     # ⚠️ Sabitdən istifadə et

# ✅ DÜZGÜN:
price = LESSON_PRICE                        # Decimal('25.00')
monthly = lessons_per_week * 4 * LESSON_PRICE

# ✅ LƏĞVETMƏ SAATI YOXLAMASI
CANCELLATION_HOURS = 24   # ← Sabit
# Literal 24 aşkar edildikdə → CANCELLATION_HOURS sabitindən istifadə et
```

---

### H-POST-006 — Type Hint Yoxlaması

**Tetikleyici**: Funksiya / metod tamamlandıqda  
**Tələblər**:

```python
# ❌ XƏBƏRDARLIQ — type hint yoxdur:
def create_booking(student_id, slot_id, topic=''):
    ...

# ✅ DÜZGÜN — type hints əlavə edilib:
def create_booking(
    student_id: str,
    slot_id: str,
    topic: str = ''
) -> Optional['Booking']:
    ...
```

**Avtomatik Suggestion**: Type hint yoxdursa → əlavə et tövsiyəsi

---

## 🔴 VALİDASİYA HOOKS

> Hər `git commit` və ya fayl saxlandıqda işə düşür

---

### H-VAL-001 — Azərbaycan Dili Yoxlaması

**Tetikleyici**: `verbose_name`, `messages.*`, template mətnləri  
**Yoxlanılacaqlar**:

```python
# ❌ İNGİLİSCƏ — xəbərdarlıq:
verbose_name = 'User'
messages.success(request, 'Successfully created!')
label = 'First Name'

# ✅ AZƏRBAYCAN DİLİ:
verbose_name = 'İstifadəçi'
messages.success(request, 'Uğurla yaradıldı!')
label = 'Ad'

# YOXLANILAN YERLER:
# - models.py: verbose_name, verbose_name_plural, help_text
# - forms.py: labels, error_messages
# - views.py: messages.success/error/warning
# - templates/*.html: button text, labels, headings
```

---

### H-VAL-002 — Təhlükəsizlik Yoxlaması

**Tetikleyici**: Hər commit  
**Yoxlanılacaqlar**:

```
🔒 TƏHLÜKƏSİZLİK YOXLAMASı:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

□ Hardcoded parol / API key varmı?
  → Pattern: password=, api_key=, secret=, token=
  → ⛔ BLOKLAMA: Commit-ə icazə vermə

□ SQL injection riski?
  → raw() / extra() istifadəsi → ⚠️ Xəbərdarlıq

□ .env dəyişənləri settings-dən alınır?
  → os.environ.get('KEY') → ✅ Düzgün
  → 'hardcoded_value' → ⛔ Bloklama

□ DEBUG=True production-da?
  → settings/production.py-da DEBUG=True → ⛔ Bloklama

□ ALLOWED_HOSTS boşdur?
  → Production settings-də → ⛔ Bloklama

□ HTTPS əlaqəsi tələb edilir?
  → SECURE_SSL_REDIRECT ayarı var? → ⚠️ Tövsiyə
```

---

### H-VAL-003 — Migration Yoxlaması

**Tetikleyici**: Model dəyişikliyi saxlandıqda  

```
📋 MİQRASİYA YOXLAMASI:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

□ Model dəyişdirilib, migration yaradılıb?
  → makemigrations çalıştır

□ ForeignKey null=False olaraq əlavə edilib?
  → ⚠️ "Mövcud data üçün default dəyər lazımdır"

□ Böyük cədvəldə indeks əlavə edilir?
  → ⚠️ "concurrent index yaratmağı nəzərə al"

□ Migration geri qaytarıla bilər?
  → Hər migration üçün reverse migration yaz

□ Data migration lazımdır?
  → RunPython istifadə et
```

---

### H-VAL-004 — Test Coverage Yoxlaması

**Tetikleyici**: Yeni modul / servis / view yazıldıqda  

```
🧪 TEST COVERAGE YOXLAMASI:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Minimum Tələblər:
□ Service sinifləri → >80% coverage
□ Model metodları  → >90% coverage
□ View-lar         → >70% coverage
□ Forms            → >75% coverage
□ Tasks            → >70% coverage

Tövsiyə edilən testlər:
□ Uğurlu ssenari testi
□ Xəta halı testi
□ Edge case testi
□ Permission testi

Xəbərdarlıq:
→ Coverage <60% olan modul commit edildikcə
  "Test coverage aşağıdır, testlər əlavə et" bildirişi
```

---

## ⚙️ KONFIQURASIYA HOOKS

---

### H-CFG-001 — VS Code Ayarları

> `.vscode/settings.json` — Copilot hook davranışı

```json
{
    // Python formatter
    "editor.formatOnSave": true,
    "[python]": {
        "editor.defaultFormatter": "ms-python.black-formatter",
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.organizeImports": "explicit"
        }
    },

    // Copilot inline suggestions
    "github.copilot.enable": {
        "*": true,
        "python": true,
        "html": true,
        "django-html": true
    },

    // LMS-specific file associations
    "files.associations": {
        "*.html": "django-html",
        "*/templates/**/*.html": "django-html"
    },

    // Auto-save
    "files.autoSave": "afterDelay",
    "files.autoSaveDelay": 1000,

    // Black formatter sətir uzunluğu
    "black-formatter.args": ["--line-length", "88"],

    // isort konfiqurasiyası
    "isort.args": ["--profile", "black"]
}
```

---

### H-CFG-002 — Pre-commit Konfiqurasiyası

> `.pre-commit-config.yaml` — commit öncəsi avtomatik yoxlamalar

```yaml
# LMS Platformu — Pre-commit Hooks
# Claude Sonnet 4.6 | Django 5.0+

repos:
  # ─── KOD FORMAT ────────────────────────────────────
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        language_version: python3.11
        args: [--line-length=88]

  # ─── İMPORT SİRALAMA ───────────────────────────────
  - repo: https://github.com/PyCQA/isort
    rev: 5.13.2
    hooks:
      - id: isort
        args: [--profile=black]

  # ─── LİNTER ────────────────────────────────────────
  - repo: https://github.com/PyCQA/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
        args: [--max-line-length=88, --extend-ignore=E203]

  # ─── TİP YOXLAMA ───────────────────────────────────
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [django-stubs, types-stripe]

  # ─── TƏHLÜKƏSİZLİK ─────────────────────────────────
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: [--baseline, .secrets.baseline]

  # ─── ÜMUMI YOXLAMALAR ──────────────────────────────
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-merge-conflict
      - id: check-added-large-files
        args: [--maxkb=500]
      - id: no-commit-to-branch
        args: [--branch, main, --branch, production]

  # ─── DJANGO SPECIFIC ───────────────────────────────
  - repo: local
    hooks:
      - id: django-check
        name: Django System Check
        entry: python manage.py check --deploy
        language: system
        pass_filenames: false
        stages: [push]

      - id: django-migrations-check
        name: Check for missing migrations
        entry: python manage.py migrate --check
        language: system
        pass_filenames: false
```

---

### H-CFG-003 — GitHub Actions Workflow

> `.github/workflows/ci.yml` — CI/CD hook-ları

```yaml
name: LMS CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  # ─── KOD KEYFİYYƏT YOXLAMASI ──────────────────────
  code-quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Python 3.11 yüklə
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Asılılıqları yüklə
        run: pip install -r requirements/development.txt

      - name: Black format yoxla
        run: black --check .

      - name: isort yoxla
        run: isort --check-only .

      - name: Flake8 lint
        run: flake8 .

      - name: MyPy tip yoxlaması
        run: mypy apps/

  # ─── TEST ─────────────────────────────────────────
  test:
    runs-on: ubuntu-latest
    needs: code-quality

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: testpass
          POSTGRES_DB: lms_test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4

      - name: Python 3.11 yüklə
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Asılılıqları yüklə
        run: pip install -r requirements/development.txt

      - name: Testləri çalıştır (coverage ilə)
        env:
          DATABASE_URL: postgresql://postgres:testpass@localhost/lms_test
          REDIS_URL: redis://localhost:6379/0
          DJANGO_SETTINGS_MODULE: config.settings.testing
        run: |
          pytest --cov=apps --cov-report=xml --cov-fail-under=80

      - name: Coverage hesabatı yüklə
        uses: codecov/codecov-action@v3

  # ─── TƏHLÜKƏSİZLİK SCAN ──────────────────────────
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Bandit security scan
        run: |
          pip install bandit
          bandit -r apps/ -ll

      - name: Safety check (CVE)
        run: |
          pip install safety
          safety check
```

---

## 📋 HOOK İSTİFADƏ XƏRİTƏSİ

```
KOD YAZMA AXINI:
════════════════════════════════════════════════════════

  Yeni fayl aç
        │
        ▼
  [H-PRE-001..004]         ← Şablon avtomatik yüklənir
  Kod yazmağa başla
        │
        ▼
  Kod tamamlanır
        │
        ▼
  [H-POST-001..006]        ← Keyfiyyət yoxlamaları
  Xəbərdarlıqlar göstərilir
        │
        ▼
  Dəyişikliklər saxlanır
        │
        ▼
  [H-VAL-001..004]         ← Validasiya yoxlamaları
  Azərbaycan dili, tip yoxlaması
        │
        ▼
  git commit
        │
        ▼
  [H-CFG-002]              ← Pre-commit hooks
  black, isort, flake8, detect-secrets
        │
        ▼
  git push
        │
        ▼
  [H-CFG-003]              ← GitHub Actions CI/CD
  Test, coverage, security scan
        │
        ▼
  ✅ Deploy
```

---

## 🚨 Kritik Bloklama Qaydaları

Aşağıdakı hallarda **commit blokladılır**:

| Ssenari | Blok Səbəbi | Həll Yolu |
|---------|-------------|-----------|
| Hardcoded API key/token | Təhlükəsizlik ihlalı | `.env` faylına köçür |
| `DEBUG=True` (production) | Deploy riski | `False` et |
| Test coverage `<60%` | Keyfiyyət standartı | Test əlavə et |
| `migrate --check` uğursuz | Schema uyğunsuzluğu | Migration yarat |
| Black format xətası | Format standartı | `black .` çalıştır |
| `main` branch-ə birbaşa push | İş axınına uyğun deyil | PR aç |

---

## 🛠️ Hook Quraşdırması

```bash
# 1. Pre-commit quraşdır
pip install pre-commit

# 2. Hook-ları aktivləşdir
pre-commit install
pre-commit install --hook-type commit-msg

# 3. Bütün fayllar üzərində test et
pre-commit run --all-files

# 4. VS Code extension-ları
# - ms-python.python
# - ms-python.black-formatter
# - ms-python.isort
# - GitHub.copilot
# - GitHub.copilot-chat
# - batisteo.vscode-django
```

---

*LMS Platformu | Claude Sonnet 4.6 | Django 5.0+ | Azərbaycan*
