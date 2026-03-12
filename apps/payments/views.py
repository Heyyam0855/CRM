"""Payments App — Views"""
import json
import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, TemplateView
from django.contrib import messages

from .models import Payment
from .services import PaymentService

logger = logging.getLogger(__name__)


class PaymentListView(LoginRequiredMixin, ListView):
    """Ödənişlər siyahısı."""
    model = Payment
    template_name = 'payments/payment_list.html'
    context_object_name = 'payments'
    paginate_by = 20

    def get_queryset(self):
        qs = Payment.objects.select_related('student', 'booking')
        if self.request.user.is_student_user:
            qs = qs.filter(student=self.request.user)
        return qs.order_by('-created_at')

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Ödənişlər'
        return context


class EPointInitiateView(LoginRequiredMixin, View):
    """ePoint ödəniş səhifəsinə yönləndir."""

    def post(self, request, pk):
        payment = get_object_or_404(Payment, pk=pk)
        # Yalnız PENDING ödəniş üçün
        if payment.status != Payment.Status.PENDING:
            messages.error(request, 'Bu ödəniş artıq emal edilib.')
            return redirect('payments:list')

        service = PaymentService()
        redirect_url = service.initiate_epoint_payment(str(payment.id))

        if redirect_url:
            return redirect(redirect_url)

        messages.error(
            request,
            'Ödəniş sisteminə bağlanılmadı. Zəhmət olmasa yenidən cəhd edin.'
        )
        return redirect('payments:list')


class EPointSuccessView(TemplateView):
    """ePoint uğurlu ödəniş geri dönüş səhifəsi."""
    template_name = 'payments/epoint_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Ödəniş uğurlu'
        return context


class EPointErrorView(TemplateView):
    """ePoint uğursuz ödəniş geri dönüş səhifəsi."""
    template_name = 'payments/epoint_error.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Ödəniş uğursuz'
        return context


@method_decorator(csrf_exempt, name='dispatch')
class EPointCallbackView(View):
    """ePoint server-to-server callback."""

    def post(self, request):
        try:
            data_base64 = request.POST.get('data', '')
            signature = request.POST.get('signature', '')

            if not data_base64 or not signature:
                return HttpResponse('Bad request', status=400)

            from .epoint_service import EPointService
            epoint = EPointService()
            decoded = epoint.verify_callback(data_base64, signature)

            if decoded is None:
                logger.warning("ePoint callback doğrulama uğursuz")
                return HttpResponse('Invalid signature', status=403)

            service = PaymentService()
            service.process_epoint_callback(decoded)

            return HttpResponse('OK', status=200)

        except Exception as e:
            logger.error(f"ePoint callback xətası: {e}", exc_info=True)
            return HttpResponse('Error', status=500)
