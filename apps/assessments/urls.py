"""Assessments — URLs"""
from django.urls import path
from . import views

app_name = 'assessments'

urlpatterns = [
    path('', views.AssessmentListView.as_view(), name='list'),
    path('create/', views.AssessmentCreateView.as_view(), name='create'),
    path('<uuid:pk>/grade/', views.AssessmentGradeView.as_view(), name='grade'),
]
