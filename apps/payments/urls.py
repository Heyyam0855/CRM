"""Payments App — URLs"""
from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('', views.PaymentListView.as_view(), name='list'),
    path(
        '<uuid:pk>/pay/',
        views.EPointInitiateView.as_view(),
        name='epoint-pay',
    ),
    path(
        'epoint/success/',
        views.EPointSuccessView.as_view(),
        name='epoint-success',
    ),
    path(
        'epoint/error/',
        views.EPointErrorView.as_view(),
        name='epoint-error',
    ),
    path(
        'epoint/callback/',
        views.EPointCallbackView.as_view(),
        name='epoint-callback',
    ),
]
