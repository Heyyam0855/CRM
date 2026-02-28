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

# Development-da lokal media saxlama
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# Email-ləri konsolda göstər
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Strict mode — development-da xətalara daha çox diqqət
TEMPLATES[0]['OPTIONS']['string_if_invalid'] = '[INVALID: %s]'  # noqa: F405
