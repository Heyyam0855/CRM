"""Bookings App — Admin"""
from django.contrib import admin
from .models import WeeklySchedule, AvailabilitySlot, Booking


@admin.register(WeeklySchedule)
class WeeklyScheduleAdmin(admin.ModelAdmin):
    list_display = ('get_day_of_week_display', 'start_time', 'end_time', 'slot_duration', 'is_active')
    list_filter = ('day_of_week', 'is_active')
    ordering = ('day_of_week', 'start_time')


@admin.register(AvailabilitySlot)
class AvailabilitySlotAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time', 'is_reserved', 'is_active')
    list_filter = ('is_reserved', 'is_active')
    ordering = ('start_time',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'student', 'slot', 'lesson_type', 'status', 'price', 'is_paid'
    )
    list_filter = ('status', 'lesson_type', 'is_paid')
    search_fields = ('student__email', 'topic')
    raw_id_fields = ('student', 'slot', 'course')
    readonly_fields = ('completed_at', 'cancelled_at')
