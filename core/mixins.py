"""
LMS Platform — Core Mixins
CBV-lər üçün paylaşılan mixin-lər
"""
from typing import Any

from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages


class TeacherRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Yalnız müəllim roluna icazə verir."""

    def test_func(self) -> bool:
        return (
            self.request.user.is_authenticated
            and self.request.user.role == 'teacher'
        )

    def handle_no_permission(self) -> Any:
        messages.error(self.request, 'Bu səhifəyə giriş icazəniz yoxdur.')
        return redirect('users:login')


class StudentOwnerMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Tələbə yalnız öz məlumatlarına daxil ola bilər."""

    def test_func(self) -> bool:
        if not self.request.user.is_authenticated:
            return False
        obj = self.get_object()
        # Müəllim hər şeyə girə bilər
        if self.request.user.role == 'teacher':
            return True
        # Tələbə yalnız özününkünü görür
        return hasattr(obj, 'student') and obj.student == self.request.user

    def handle_no_permission(self) -> Any:
        messages.error(self.request, 'Bu məlumata giriş icazəniz yoxdur.')
        return redirect('analytics:dashboard')


class HTMXMixin:
    """HTMX sorğuları üçün partial template dəstəyi."""

    partial_template_name: str = ''

    def get_template_names(self) -> list[str]:
        if self.request.headers.get('HX-Request') and self.partial_template_name:
            return [self.partial_template_name]
        return super().get_template_names()  # type: ignore[misc]
