"""LMS Platform — Development Settings"""
from .base import *  # noqa: F401, F403

DEBUG = True

INSTALLED_APPS += [  # noqa: F405
    'debug_toolbar',
]

MIDDLEWARE += [  # noqa: F405
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = ['127.0.0.1', 'localhost']

# Redis əvəzinə yaddaş cache (Redis olmadan işləyir)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'lms-dev',
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

# Development-da lokal media saxlama
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'  # noqa: F405

# Email-ləri konsolda göstər
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Allauth — email verification-ı deaktiv et
ACCOUNT_EMAIL_VERIFICATION = 'none'

# Strict mode — development-da xətalara daha çox diqqət
TEMPLATES[0]['OPTIONS']['string_if_invalid'] = '[INVALID: %s]'  # noqa: F405
