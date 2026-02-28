"""Payments API URLs"""
from django.urls import path
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@method_decorator(login_required, name='dispatch')
class PaymentListAPIView(View):
    def get(self, request, *args, **kwargs):
        from apps.payments.models import Payment
        qs = Payment.objects.filter(student=request.user)
        data = [
            {
                'id': str(p.id),
                'invoice_number': p.invoice_number,
                'amount': str(p.amount),
                'status': p.status,
                'paid_at': p.paid_at.isoformat() if p.paid_at else None,
            }
            for p in qs[:50]
        ]
        return JsonResponse({'results': data})


urlpatterns = [
    path('payments/', PaymentListAPIView.as_view(), name='api-payment-list'),
]
