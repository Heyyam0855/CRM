"""Bookings App — URLs"""
from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    # Tələbə & Müəllim — Rezervasiyalar
    path('', views.BookingListView.as_view(), name='list'),
    path('new/', views.BookingCreateView.as_view(), name='create'),
    path('slots/', views.AvailableSlotsView.as_view(), name='slots'),
    path('<uuid:pk>/cancel/', views.BookingCancelView.as_view(), name='cancel'),
    path('<uuid:pk>/complete/', views.BookingCompleteView.as_view(), name='complete'),

    # Calendly tipli dərs təyinatı
    path('calendar/', views.BookingCalendarView.as_view(), name='calendar'),
    path('quick-book/', views.BookingQuickCreateView.as_view(), name='quick-book'),

    # CRM — Cədvəl idarəetməsi (müəllim)
    path('schedule/', views.ScheduleManageView.as_view(), name='schedule-manage'),
    path('schedule/create/', views.ScheduleCreateView.as_view(), name='schedule-create'),
    path('schedule/<uuid:pk>/delete/', views.ScheduleDeleteView.as_view(), name='schedule-delete'),
    path('schedule/generate/', views.GenerateSlotsView.as_view(), name='generate-slots'),
]
