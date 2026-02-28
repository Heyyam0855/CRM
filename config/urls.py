"""
LMS Platform — Ana URL Konfiqurasiyası
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView


urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Auth (django-allauth)
    path('accounts/', include('allauth.urls')),
    path('auth/', include('apps.users.urls', namespace='users')),

    # Ana səhifə → dashboard yönləndir
    path('', RedirectView.as_view(url='/dashboard/', permanent=False)),

    # Dashboard
    path('dashboard/', include('apps.analytics.urls', namespace='analytics')),

    # Core apps
    path('courses/', include('apps.courses.urls', namespace='courses')),
    path('bookings/', include('apps.bookings.urls', namespace='bookings')),
    path('payments/', include('apps.payments.urls', namespace='payments')),
    path('support/', include('apps.support.urls', namespace='support')),
    path('assessments/', include('apps.assessments.urls', namespace='assessments')),
    path('notifications/', include('apps.notifications.urls', namespace='notifications')),

    # Health check (DigitalOcean)
    path('health/', include('core.urls')),

    # API v1
    path('api/v1/', include([
        path('auth/', include('apps.users.api_urls')),
        path('courses/', include('apps.courses.api_urls')),
        path('bookings/', include('apps.bookings.api_urls')),
        path('payments/', include('apps.payments.api_urls')),
    ])),
]

# Development-da media faylları servis et
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    import debug_toolbar
    urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns
