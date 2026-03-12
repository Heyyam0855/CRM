"""Bookings App — Forms"""
from django import forms
from .models import WeeklySchedule


class WeeklyScheduleForm(forms.ModelForm):
    """Həftəlik cədvəl əlavə etmə formu."""

    class Meta:
        model = WeeklySchedule
        fields = ['day_of_week', 'start_time', 'end_time', 'slot_duration']
        widgets = {
            'day_of_week': forms.Select(attrs={'class': 'form-select'}),
            'start_time': forms.TimeInput(
                attrs={'class': 'form-control', 'type': 'time'},
                format='%H:%M',
            ),
            'end_time': forms.TimeInput(
                attrs={'class': 'form-control', 'type': 'time'},
                format='%H:%M',
            ),
            'slot_duration': forms.Select(
                attrs={'class': 'form-select'},
                choices=[(30, '30 dəq'), (45, '45 dəq'), (60, '60 dəq'), (90, '90 dəq')],
            ),
        }
        labels = {
            'day_of_week': 'Həftənin günü',
            'start_time': 'Başlama saatı',
            'end_time': 'Bitmə saatı',
            'slot_duration': 'Dərs müddəti',
        }

    def clean(self):
        cleaned = super().clean()
        start = cleaned.get('start_time')
        end = cleaned.get('end_time')
        if start and end and start >= end:
            raise forms.ValidationError('Bitmə saatı başlama saatından sonra olmalıdır.')
        return cleaned
