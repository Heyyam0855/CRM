"""
LMS Platform — Core Permissions
DRF API üçün icazə sinifləri
"""
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsTeacher(BasePermission):
    """Yalnız müəllim rolu."""

    def has_permission(self, request, view) -> bool:
        return (
            request.user.is_authenticated
            and request.user.role == 'teacher'
        )


class IsStudent(BasePermission):
    """Yalnız tələbə rolu."""

    def has_permission(self, request, view) -> bool:
        return (
            request.user.is_authenticated
            and request.user.role == 'student'
        )


class IsOwnerOrTeacher(BasePermission):
    """Obyekt sahibi və ya müəllim."""

    def has_object_permission(self, request, view, obj) -> bool:
        if request.user.role == 'teacher':
            return True
        if hasattr(obj, 'student'):
            return obj.student == request.user
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return False


class IsTeacherOrReadOnly(BasePermission):
    """Oxuma hər kəsə, yazma yalnız müəllimə."""

    def has_permission(self, request, view) -> bool:
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        return (
            request.user.is_authenticated
            and request.user.role == 'teacher'
        )
