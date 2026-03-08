"""Users App — Admin"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, StudentProfile, RegistrationRequest


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'get_full_name', 'role', 'is_active', 'date_joined')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-date_joined',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Şəxsi məlumatlar', {'fields': ('first_name', 'last_name', 'phone', 'avatar')}),
        ('Rol və İcazələr', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser')}),
        ('Tarixlər', {'fields': ('date_joined',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'role', 'password1', 'password2'),
        }),
    )


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'payment_model', 'lessons_per_week', 'github_username')
    list_filter = ('status', 'payment_model')
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    raw_id_fields = ('user',)


@admin.register(RegistrationRequest)
class RegistrationRequestAdmin(admin.ModelAdmin):
    list_display = (
        'full_name', 'email', 'phone',
        'course_package', 'status',
        'preferred_start_date', 'created_at',
    )
    list_filter = ('status', 'course_package', 'created_at')
    search_fields = ('full_name', 'email', 'phone')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('status',)
