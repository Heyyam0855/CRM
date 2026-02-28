"""Users App — URLs"""
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.StudentRegisterView.as_view(), name='register'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.StudentProfileUpdateView.as_view(), name='profile-edit'),
]
