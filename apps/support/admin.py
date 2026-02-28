"""Support Admin"""
from django.contrib import admin
from .models import Ticket, TicketMessage


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('subject', 'student', 'status', 'priority', 'created_at')
    list_filter = ('status', 'priority')
    search_fields = ('subject', 'student__email')


@admin.register(TicketMessage)
class TicketMessageAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'sender', 'is_from_teacher', 'created_at')
    list_filter = ('is_from_teacher',)
