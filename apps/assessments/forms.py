"""Assessments — Forms"""
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Assessment


class AssessmentCreateForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = ['student', 'lesson', 'title', 'type', 'max_score', 'due_date']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-select'}),
            'lesson': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'max_score': forms.NumberInput(attrs={'class': 'form-control'}),
            'due_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
        }
        labels = {
            'student': _('Tələbə'),
            'lesson': _('Dərs'),
            'title': _('Başlıq'),
            'type': _('Növ'),
            'max_score': _('Maksimum bal'),
            'due_date': _('Son tarix'),
        }


class AssessmentGradeForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = ['score', 'feedback']
        widgets = {
            'score': forms.NumberInput(attrs={'class': 'form-control'}),
            'feedback': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        labels = {
            'score': _('Bal'),
            'feedback': _('Rəy'),
        }
