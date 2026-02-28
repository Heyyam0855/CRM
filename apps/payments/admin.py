"""Payments App — Admin"""
from django.contrib import admin
from .models import Payment, MonthlySubscription


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'student', 'amount', 'status', 'payment_method', 'paid_at')
    list_filter = ('status', 'payment_method')
    search_fields = ('invoice_number', 'student__email')
    readonly_fields = ('invoice_number', 'paid_at')


@admin.register(MonthlySubscription)
class MonthlySubscriptionAdmin(admin.ModelAdmin):
    list_display = ('student', 'lessons_per_week', 'monthly_amount', 'status', 'next_billing_date')
    list_filter = ('status',)
