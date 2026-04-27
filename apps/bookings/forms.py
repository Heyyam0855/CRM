"""Bookings App — Forms"""
from django import forms
from django.utils.translation import gettext_lazy as _
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
                choices=[(30, _('30 dəq')), (45, _('45 dəq')), (60, _('60 dəq')), (90, _('90 dəq'))],
            ),
        }
        labels = {
            'day_of_week': _('Ħəftənin günü'),
            'start_time': _('Başlama saatı'),
            'end_time': _('Bitmə saatı'),
            'slot_duration': _('Dərs müddəti'),
        }

    def clean(self):
        cleaned = super().clean()
        start = cleaned.get('start_time')
        end = cleaned.get('end_time')
        if start and end and start >= end:
            raise forms.ValidationError(_('Bitmə saatı başlama saatından sonra olmalıdır.'))
        return cleaned
