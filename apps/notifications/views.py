"""Notifications — Views"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.http import JsonResponse
from django.views import View

from .models import Notification


class NotificationListView(LoginRequiredMixin, ListView):
    """Bildirişlər siyahısı."""
    model = Notification
    template_name = 'notifications/notification_list.html'
    context_object_name = 'notifications'
    paginate_by = 30

    def get_queryset(self):
        return Notification.objects.filter(
            user=self.request.user
        ).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Bildirişlər'
        return context


class MarkAllReadView(LoginRequiredMixin, View):
    """Bütün bildirişləri oxunmuş kimi işarələ."""

    def post(self, request, *args, **kwargs):
        Notification.objects.filter(
            user=request.user, is_read=False
        ).update(is_read=True)

        if request.headers.get('HX-Request'):
            return JsonResponse({'success': True, 'count': 0})
        return JsonResponse({'success': True})
