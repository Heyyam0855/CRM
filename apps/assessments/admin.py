"""Assessments Admin"""
from django.contrib import admin
from .models import Assessment


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'title', 'type', 'score', 'max_score', 'due_date')
    list_filter = ('type',)
    search_fields = ('student__email', 'title')
