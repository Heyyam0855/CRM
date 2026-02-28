"""Users App — allauth adapter"""
from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings


class CustomAccountAdapter(DefaultAccountAdapter):
    """LMS-ə uyğun allauth adapter."""

    def is_open_for_signup(self, request) -> bool:
        """Qeydiyyat açıqdır (yalnız tələbələr üçün)."""
        return True

    def get_login_redirect_url(self, request) -> str:
        return '/dashboard/'

    def get_logout_redirect_url(self, request) -> str:
        return '/auth/login/'
