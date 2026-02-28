"""
LMS Platform — Core Validators
Ümumi validasiya funksiyaları
"""
import re
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_future_datetime(value) -> None:
    """Tarix gələcəkdə olmalıdır."""
    if value <= timezone.now():
        raise ValidationError('Tarix gələcəkdə olmalıdır.')


def validate_youtube_url(value: str) -> None:
    """YouTube URL validasiyası."""
    pattern = r'(youtube\.com|youtu\.be)'
    if not re.search(pattern, value):
        raise ValidationError('Düzgün YouTube URL daxil edin.')


def validate_github_username(value: str) -> None:
    """GitHub istifadəçi adı validasiyası."""
    pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9-]{0,37}[a-zA-Z0-9])?$'
    if not re.match(pattern, value):
        raise ValidationError('Düzgün GitHub istifadəçi adı daxil edin.')


def validate_phone_number(value: str) -> None:
    """Azərbaycan telefon nömrəsi validasiyası."""
    pattern = r'^(\+994|0)(50|51|55|60|70|77|99)\d{7}$'
    if not re.match(pattern, value.replace(' ', '').replace('-', '')):
        raise ValidationError(
            'Düzgün Azərbaycan telefon nömrəsi daxil edin. (+994XXXXXXXXX)'
        )


def validate_positive_decimal(value: Decimal) -> None:
    """Müsbət ondalıq ədəd."""
    if value <= Decimal('0'):
        raise ValidationError('Dəyər müsbət olmalıdır.')
