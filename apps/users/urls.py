"""Users App — URLs"""
from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', RedirectView.as_view(url='/accounts/login/'), name='login'),
    path('logout/', RedirectView.as_view(url='/accounts/logout/'), name='logout'),
    path('register/', views.StudentRegisterView.as_view(), name='register'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.StudentProfileUpdateView.as_view(), name='profile-edit'),
]
