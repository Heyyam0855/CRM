"""Users API URLs"""
from django.urls import path
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@method_decorator(login_required, name='dispatch')
class CurrentUserAPIView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        return JsonResponse({
            'id': str(user.id),
            'email': user.email,
            'full_name': user.get_full_name(),
            'role': user.role,
            'is_active': user.is_active,
        })


urlpatterns = [
    path('me/', CurrentUserAPIView.as_view(), name='api-current-user'),
]
