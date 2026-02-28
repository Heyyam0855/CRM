"""
LMS Platform — Core Utilities
Bütün app-lar tərəfindən paylaşılan köməkçi funksiyalar
"""
import re
import uuid
from decimal import Decimal
from typing import Optional
from django.conf import settings


# ─────────────────────────────────────────────
#  LMS Biznes Sabitləri
# ─────────────────────────────────────────────
LESSON_PRICE: Decimal = getattr(settings, 'LESSON_PRICE', Decimal('25.00'))
CANCELLATION_HOURS: int = getattr(settings, 'CANCELLATION_HOURS', 24)
MAX_LESSONS_PER_WEEK: int = getattr(settings, 'MAX_LESSONS_PER_WEEK', 7)


def calculate_monthly_price(lessons_per_week: int) -> Decimal:
    """
    Aylıq ödəniş məbləğini hesablayır.

    Args:
        lessons_per_week: Həftəlik dərs sayı (1-7)

    Returns:
        Decimal: Aylıq ödəniş məbləği (AZN)

    Example:
        >>> calculate_monthly_price(2)
        Decimal('200.00')
    """
    if not 1 <= lessons_per_week <= MAX_LESSONS_PER_WEEK:
        raise ValueError(
            f"Həftəlik dərs sayı 1-{MAX_LESSONS_PER_WEEK} arasında olmalıdır."
        )
    return Decimal(lessons_per_week) * 4 * LESSON_PRICE


def get_repo_name(student_full_name: str, course_slug: str) -> str:
    """
    GitHub repo adını generasiya edir.

    Args:
        student_full_name: Tələbənin tam adı
        course_slug: Kursun slug-ı

    Returns:
        str: Repo adı (məs: ali-aliyev-frontend-course)
    """
    name_slug = re.sub(r'[^a-z0-9]+', '-', student_full_name.lower().strip()).strip('-')
    return f"{name_slug}-{course_slug}"


def generate_invoice_number() -> str:
    """
    Unikal faktura nömrəsi generasiya edir.

    Returns:
        str: INV-XXXXXXXX formatında faktura nömrəsi
    """
    return f"INV-{uuid.uuid4().hex[:8].upper()}"


def extract_youtube_video_id(url: str) -> Optional[str]:
    """
    YouTube URL-dən video ID çıxarır.

    Args:
        url: YouTube URL (müxtəlif formatlar)

    Returns:
        Optional[str]: Video ID və ya None

    Supported formats:
        - https://www.youtube.com/watch?v=VIDEO_ID
        - https://youtu.be/VIDEO_ID
        - https://www.youtube.com/embed/VIDEO_ID
    """
    patterns = [
        r'(?:youtube\.com/watch\?v=)([a-zA-Z0-9_-]{11})',
        r'(?:youtu\.be/)([a-zA-Z0-9_-]{11})',
        r'(?:youtube\.com/embed/)([a-zA-Z0-9_-]{11})',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def format_azn(amount: Decimal) -> str:
    """
    AZN məbləğini formatlaşdırır.

    Args:
        amount: Decimal məbləğ

    Returns:
        str: '25.00 AZN' formatında
    """
    return f"{amount:.2f} AZN"
