"""
LMS Platform — Local Development Settings
PostgreSQL/Redis olmadan SQLite + LocMemCache ilə işləyir.
"""
from .base import *  # noqa: F401, F403

DEBUG = True

# SQLite — lokal development üçün
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # noqa: F405
    }
}

# Redis əvəzinə yaddaş cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'lms-local',
    }
}

# Session — verilənlər bazasında saxla (Redis yoxdur)
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_CACHE_ALIAS = 'default'

# Channels — in-memory layer (Redis yoxdur)
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    }
}

# Email — konsolda göstər
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Debug Toolbar
INSTALLED_APPS += ['debug_toolbar']  # noqa: F405
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']  # noqa: F405
INTERNAL_IPS = ['127.0.0.1', 'localhost']

# Debug Toolbar redirect interception-ı söndür
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

# Lokal media saxlama
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'  # noqa: F405

# Strict template debug
TEMPLATES[0]['OPTIONS']['string_if_invalid'] = '[INVALID: %s]'  # noqa: F405

# Allauth — email verification-ı deaktiv et (development)
ACCOUNT_EMAIL_VERIFICATION = 'none'
