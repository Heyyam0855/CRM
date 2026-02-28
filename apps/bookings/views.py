"""Bookings App — Views"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone

from core.mixins import HTMXMixin, StudentOwnerMixin
from .models import Booking, AvailabilitySlot
from .services import BookingService


class BookingListView(LoginRequiredMixin, HTMXMixin, ListView):
    """Tələbənin rezervasiyaları siyahısı."""
    model = Booking
    template_name = 'bookings/booking_list.html'
    partial_template_name = 'bookings/partials/booking_list.html'
    context_object_name = 'bookings'
    paginate_by = 20

    def get_queryset(self):
        qs = Booking.objects.select_related('student', 'slot', 'course')
        if self.request.user.is_student_user:
            qs = qs.filter(student=self.request.user)
        return qs.order_by('-slot__start_time')

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Rezervasiyalarım'
        return context


class AvailableSlotsView(LoginRequiredMixin, TemplateView):
    """HTMX — Əlçatan slotlar."""
    template_name = 'bookings/partials/available_slots.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['slots'] = AvailabilitySlot.objects.filter(
            is_reserved=False,
            is_active=True,
            start_time__gt=timezone.now()
        ).order_by('start_time')[:50]
        return context


class BookingCreateView(LoginRequiredMixin, TemplateView):
    """Yeni rezervasiya — HTMX form."""
    template_name = 'bookings/booking_create.html'

    def post(self, request, *args, **kwargs):
        service = BookingService()
        booking = service.create_booking(
            student_id=str(request.user.id),
            slot_id=request.POST.get('slot_id', ''),
            lesson_type=request.POST.get('lesson_type', 'standard'),
            topic=request.POST.get('topic', ''),
            notes=request.POST.get('notes', ''),
        )
        if booking:
            messages.success(request, 'Dərs uğurla rezerv edildi!')
            if request.headers.get('HX-Request'):
                return JsonResponse({'success': True, 'booking_id': str(booking.id)})
        else:
            messages.error(request, 'Rezervasiya mümkün olmadı. Slot artıq tutulmuş ola bilər.')
        return self.render_to_response(self.get_context_data())
