"""Bookings App — URLs"""
from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.BookingListView.as_view(), name='list'),
    path('new/', views.BookingCreateView.as_view(), name='create'),
    path('slots/', views.AvailableSlotsView.as_view(), name='slots'),
]
