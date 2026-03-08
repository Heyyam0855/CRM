"""Users App — URLs"""
from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', RedirectView.as_view(url='/accounts/login/'), name='login'),
    path('logout/', RedirectView.as_view(url='/accounts/logout/'), name='logout'),
    path('register/', views.StudentRegisterView.as_view(), name='register'),
    path(
        'register/success/',
        views.RegisterSuccessView.as_view(),
        name='register-success',
    ),

    # Tələbələr (müəllim)
    path('students/', views.StudentListView.as_view(), name='student-list'),

    # Qeydiyyat müraciətləri (müəllim)
    path(
        'registration-requests/',
        views.RegistrationRequestListView.as_view(),
        name='registration-requests',
    ),
    path(
        'registration-requests/<uuid:pk>/',
        views.RegistrationRequestDetailView.as_view(),
        name='registration-request-detail',
    ),
    path(
        'registration-requests/<uuid:pk>/approve/',
        views.ApproveRegistrationView.as_view(),
        name='registration-request-approve',
    ),
    path(
        'registration-requests/<uuid:pk>/reject/',
        views.RejectRegistrationView.as_view(),
        name='registration-request-reject',
    ),

    # Profil
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.StudentProfileUpdateView.as_view(), name='profile-edit'),
]
