"""Courses App — Forms"""
from django import forms

from .models import Course


class CourseForm(forms.ModelForm):
    """Kurs yaratma / redaktə formu."""

    class Meta:
        model = Course
        fields = [
            'title', 'description', 'category', 'cover_image',
            'status', 'level', 'objectives', 'prerequisites',
            'duration_weeks',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Məsələn: Front End Development',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 4,
                'placeholder': 'Kurs haqqında qısa təsvir yazın...',
            }),
            'category': forms.Select(attrs={
                'class': 'form-input',
            }),
            'cover_image': forms.ClearableFileInput(attrs={
                'class': 'form-input',
                'accept': 'image/*',
            }),
            'status': forms.Select(attrs={
                'class': 'form-input',
            }),
            'level': forms.Select(attrs={
                'class': 'form-input',
            }),
            'objectives': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 4,
                'placeholder': 'Hər sətirə bir məqsəd yazın...',
            }),
            'prerequisites': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 3,
                'placeholder': 'Tələb olunan biliklər (boş buraxıla bilər)',
            }),
            'duration_weeks': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': 1,
                'max': 52,
            }),
        }
        labels = {
            'title': 'Kurs adı',
            'description': 'Təsvir',
            'category': 'Kateqoriya',
            'cover_image': 'Örtük şəkli',
            'status': 'Status',
            'level': 'Səviyyə',
            'objectives': 'Kurs məqsədləri',
            'prerequisites': 'Ön şərtlər',
            'duration_weeks': 'Müddət (həftə)',
        }
