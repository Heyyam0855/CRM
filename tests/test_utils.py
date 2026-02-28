"""
LMS Platform — Core Utils Tests
"""
import pytest
from decimal import Decimal


class TestCoreUtils:
    """core/utils.py üçün testlər."""

    def test_lesson_price_constant(self):
        """LESSON_PRICE dəyişməzdir."""
        from core.utils import LESSON_PRICE
        assert LESSON_PRICE == Decimal('25.00')

    def test_calculate_monthly_price(self):
        """Aylıq qiymət hesablaması."""
        from core.utils import calculate_monthly_price
        assert calculate_monthly_price(1) == Decimal('100.00')
        assert calculate_monthly_price(2) == Decimal('200.00')
        assert calculate_monthly_price(3) == Decimal('300.00')

    def test_get_repo_name(self):
        """GitHub repo adı formatı."""
        from core.utils import get_repo_name
        result = get_repo_name('Ali Aliyev', 'python-basics')
        assert result == 'ali-aliyev-python-basics'

    def test_extract_youtube_video_id(self):
        """YouTube video ID çıxarımı."""
        from core.utils import extract_youtube_video_id
        assert extract_youtube_video_id('https://www.youtube.com/watch?v=dQw4w9WgXcQ') == 'dQw4w9WgXcQ'
        assert extract_youtube_video_id('https://youtu.be/dQw4w9WgXcQ') == 'dQw4w9WgXcQ'
        assert extract_youtube_video_id('https://google.com') is None

    def test_format_azn(self):
        """AZN formatlaması."""
        from core.utils import format_azn
        assert format_azn(Decimal('25.00')) == '25.00 AZN'

    def test_generate_invoice_number(self):
        """Faktura nömrəsi formatı."""
        from core.utils import generate_invoice_number
        inv = generate_invoice_number()
        assert inv.startswith('INV-')
        assert len(inv) == 12  # INV-XXXXXXXX
