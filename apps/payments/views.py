"""Payments App — Views"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.http import HttpResponse

from .models import Payment


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
