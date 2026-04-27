"""Support — Forms"""
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Ticket, TicketMessage


class TicketCreateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['subject', 'priority']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'subject': _('Mövzu'),
            'priority': _('Prioritet'),
        }


class TicketMessageForm(forms.ModelForm):
    class Meta:
        model = TicketMessage
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        labels = {'body': _('Cavab')}
