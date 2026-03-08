"""Analytics — Views (Teacher Dashboard)"""
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from core.mixins import TeacherRequiredMixin


class DashboardView(LoginRequiredMixin, TemplateView):
    """Müəllim paneli ana səhifəsi."""
    template_name = 'analytics/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'İdarəçilik Paneli'
        context.update(self._get_stats())
        return context

    def _get_stats(self) -> dict:
        """Dashboard statistikası."""
        try:
            from apps.users.models import User, StudentProfile
            from apps.bookings.models import Booking
            from apps.payments.models import Payment
            from django.utils import timezone
            from django.db.models import Count, Sum
            from datetime import timedelta

            now = timezone.now()
            this_month_start = now.replace(day=1, hour=0, minute=0, second=0)

            total_students = User.objects.filter(role='student', is_active=True).count()
            pending_students = StudentProfile.objects.filter(
                status=StudentProfile.Status.PENDING
            ).count()

            this_month_bookings = Booking.objects.filter(
                slot__start_time__gte=this_month_start
            ).count()
            upcoming_bookings = Booking.objects.filter(
                slot__start_time__gte=now,
                status=Booking.Status.CONFIRMED
            ).order_by('slot__start_time')[:5].select_related('student', 'slot')

            monthly_revenue = Payment.objects.filter(
                status=Payment.Status.COMPLETED,
                paid_at__gte=this_month_start
            ).aggregate(total=Sum('amount'))['total'] or 0

            overdue_count = Payment.objects.filter(
                status=Payment.Status.OVERDUE
            ).count()

            # Monthly chart data (last 6 months)
            month_labels = []
            monthly_revenue_data = []
            monthly_bookings_data = []
            az_months = {
                1: 'Yan', 2: 'Fev', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'İyn',
                7: 'İyl', 8: 'Avq', 9: 'Sen', 10: 'Okt', 11: 'Noy', 12: 'Dek'
            }
            for i in range(5, -1, -1):
                target = now - timedelta(days=30 * i)
                month_start = target.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                if target.month == 12:
                    month_end = month_start.replace(year=target.year + 1, month=1)
                else:
                    month_end = month_start.replace(month=target.month + 1)

                month_labels.append(az_months.get(target.month, ''))
                rev = Payment.objects.filter(
                    status=Payment.Status.COMPLETED,
                    paid_at__gte=month_start,
                    paid_at__lt=month_end
                ).aggregate(total=Sum('amount'))['total'] or 0
                monthly_revenue_data.append(float(rev))

                bk = Booking.objects.filter(
                    slot__start_time__gte=month_start,
                    slot__start_time__lt=month_end
                ).count()
                monthly_bookings_data.append(bk)

            return {
                'total_students': total_students,
                'pending_students': pending_students,
                'this_month_bookings': this_month_bookings,
                'upcoming_bookings': upcoming_bookings,
                'monthly_revenue': monthly_revenue,
                'overdue_count': overdue_count,
                'month_labels': json.dumps(month_labels),
                'monthly_revenue_data': json.dumps(monthly_revenue_data),
                'monthly_bookings_data': json.dumps(monthly_bookings_data),
            }
        except Exception:
            return {}


class StudentDashboardView(LoginRequiredMixin, TemplateView):
    """Tələbə paneli."""
    template_name = 'analytics/student_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Pəncərəm'

        from apps.bookings.models import Booking
        from apps.payments.models import Payment
        from django.utils import timezone
        from django.db.models import Sum

        user = self.request.user
        now = timezone.now()

        context['upcoming_lessons'] = Booking.objects.filter(
            student=user,
            slot__start_time__gte=now,
            status=Booking.Status.CONFIRMED
        ).select_related('slot').order_by('slot__start_time')[:3]

        context['recent_payments'] = Payment.objects.filter(
            student=user
        ).order_by('-created_at')[:5]

        context['completed_lessons'] = Booking.objects.filter(
            student=user,
            status=Booking.Status.COMPLETED
        ).count()

        context['total_paid'] = Payment.objects.filter(
            student=user,
            status=Payment.Status.COMPLETED
        ).aggregate(total=Sum('amount'))['total'] or 0

        return context
