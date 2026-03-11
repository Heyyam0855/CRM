"""Bookings App — Views"""
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView, View
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone

from core.mixins import HTMXMixin, TeacherRequiredMixin
from .models import Booking, AvailabilitySlot, WeeklySchedule
from .services import BookingService, ScheduleService
from .forms import WeeklyScheduleForm


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
        context['page_title'] = 'Rezervasiyalarım' if self.request.user.is_student_user else 'Bütün Dərslər'
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


class BookingCancelView(LoginRequiredMixin, View):
    """Rezervasiya ləğv etmə."""

    def post(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk)
        if request.user.is_student_user and booking.student != request.user:
            messages.error(request, 'Bu əməliyyat üçün icazəniz yoxdur.')
            return redirect('bookings:list')

        service = BookingService()
        reason = request.POST.get('reason', '')
        success = service.cancel_booking(str(pk), reason)

        if success:
            messages.success(request, 'Dərs ləğv edildi.')
        else:
            messages.error(
                request,
                'Ləğvetmə mümkün olmadı. Dərsə 24 saatdan az qalıb.'
            )
        return redirect('bookings:list')


class BookingCompleteView(TeacherRequiredMixin, View):
    """Müəllim dərsi tamamlanmış kimi işarələ."""

    def post(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk)
        booking.status = Booking.Status.COMPLETED
        booking.completed_at = timezone.now()
        booking.save(update_fields=['status', 'completed_at'])
        messages.success(request, f'{booking.student.get_full_name()} dərsi tamamlandı.')
        return redirect('bookings:list')


# ══════════════════════════════════════
# Calendly-tipli Dərs Təyinatı (Tələbə)
# ══════════════════════════════════════

class BookingCalendarView(LoginRequiredMixin, TemplateView):
    """Calendly tipli dərs seçim təqvimi."""
    template_name = 'bookings/booking_calendar.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Dərs Təyin Et'

        schedule_service = ScheduleService()
        slots_by_date = schedule_service.get_available_slots_by_date()

        # Template üçün JSON data
        calendar_data = {}
        for date_str, slots in slots_by_date.items():
            calendar_data[date_str] = [
                {
                    'id': str(slot.id),
                    'start': slot.start_time.strftime('%H:%M'),
                    'end': slot.end_time.strftime('%H:%M'),
                }
                for slot in slots
            ]

        context['calendar_data'] = json.dumps(calendar_data)
        context['available_dates'] = json.dumps(list(slots_by_date.keys()))
        return context


class BookingQuickCreateView(LoginRequiredMixin, View):
    """HTMX — Calendly-dən slot seçib booking yarat."""

    def post(self, request):
        slot_id = request.POST.get('slot_id', '')
        topic = request.POST.get('topic', '')

        if not slot_id:
            return JsonResponse({'error': 'Slot seçilməyib'}, status=400)

        service = BookingService()
        booking = service.create_booking(
            student_id=str(request.user.id),
            slot_id=slot_id,
            lesson_type='standard',
            topic=topic,
        )

        if booking:
            messages.success(
                request,
                f"Dərs {booking.slot.start_time:%d.%m.%Y %H:%M} tarixinə təyin edildi!"
            )
            return JsonResponse({
                'success': True,
                'message': f"Dərs {booking.slot.start_time:%d.%m.%Y %H:%M} tarixinə təyin edildi!",
            })
        else:
            return JsonResponse({
                'error': 'Slot artıq tutulub. Başqa vaxt seçin.',
            }, status=409)


# ══════════════════════════════════════
# CRM — Cədvəl İdarəetməsi (Müəllim)
# ══════════════════════════════════════

class ScheduleManageView(TeacherRequiredMixin, TemplateView):
    """Müəllim həftəlik cədvəl idarəetməsi."""
    template_name = 'bookings/crm/schedule_manage.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Cədvəl İdarəetməsi'
        context['schedules'] = WeeklySchedule.objects.filter(
            is_active=True
        ).order_by('day_of_week', 'start_time')
        context['form'] = WeeklyScheduleForm()

        # Bu həftə və gələcək slotlar
        now = timezone.now()
        context['upcoming_slots'] = (
            AvailabilitySlot.objects
            .filter(start_time__gt=now, is_active=True)
            .select_related()
            .order_by('start_time')[:30]
        )

        # Gün adları JSON
        context['day_names'] = json.dumps({
            '0': 'Bazar ertəsi',
            '1': 'Çərşənbə axşamı',
            '2': 'Çərşənbə',
            '3': 'Cümə axşamı',
            '4': 'Cümə',
            '5': 'Şənbə',
            '6': 'Bazar',
        })
        return context


class ScheduleCreateView(TeacherRequiredMixin, View):
    """Həftəlik cədvəl yaratma."""

    def post(self, request):
        form = WeeklyScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cədvəl əlavə edildi.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
        return redirect('bookings:schedule-manage')


class ScheduleDeleteView(TeacherRequiredMixin, View):
    """Həftəlik cədvəl silmə."""

    def post(self, request, pk):
        schedule = get_object_or_404(WeeklySchedule, pk=pk)
        schedule.is_active = False
        schedule.save(update_fields=['is_active'])
        messages.success(request, 'Cədvəl deaktiv edildi.')
        return redirect('bookings:schedule-manage')


class GenerateSlotsView(TeacherRequiredMixin, View):
    """Cədvəl əsasında slot-lar yarat."""

    def post(self, request):
        weeks = int(request.POST.get('weeks', 4))
        weeks = min(weeks, 8)  # Maksimum 8 həftə

        service = ScheduleService()
        count = service.generate_slots(weeks_ahead=weeks)
        messages.success(request, f'{count} yeni slot yaradıldı ({weeks} həftəlik).')
        return redirect('bookings:schedule-manage')
