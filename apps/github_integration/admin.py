"""GitHub Integration Admin"""
from django.contrib import admin
from .models import StudentRepository


@admin.register(StudentRepository)
class StudentRepositoryAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'repo_name', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('student__email', 'repo_name')
    readonly_fields = ('created_at', 'updated_at')
