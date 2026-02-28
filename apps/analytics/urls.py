"""Analytics — URLs"""
from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('student/', views.StudentDashboardView.as_view(), name='student-dashboard'),
]
