"""Bookings API URLs"""
from django.urls import path
from . import api_views

urlpatterns = [
    path('bookings/', api_views.BookingListAPIView.as_view(), name='api-booking-list'),
]
