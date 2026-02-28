"""Assessments — Forms"""
from django import forms
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
            'student': 'Tələbə',
            'lesson': 'Dərs',
            'title': 'Başlıq',
            'type': 'Növ',
            'max_score': 'Maksimum bal',
            'due_date': 'Son tarix',
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
            'score': 'Bal',
            'feedback': 'Rəy',
        }
