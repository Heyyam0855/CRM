"""Users App — Views"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView, UpdateView, DetailView, View
from django.contrib.auth import login, logout
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseNotAllowed, JsonResponse
from django.utils import timezone
from django.db.models import Count, Sum, Q

from core.mixins import TeacherRequiredMixin
from .models import User, StudentProfile, RegistrationRequest
from .forms import CourseRegistrationForm, StudentProfileUpdateForm
from .services import UserService


class StudentListView(TeacherRequiredMixin, ListView):
    """Müəllim üçün tələbələr siyahısı (CRM)."""

    model = User
    template_name = 'users/student_list.html'
    context_object_name = 'students'
    paginate_by = 20

    def get_queryset(self):
        qs = (
            User.objects
            .filter(role=User.Role.STUDENT)
            .select_related('student_profile')
            .order_by('-date_joined')
        )
        # Status filter
        status = self.request.GET.get('status', '')
        if status:
            qs = qs.filter(student_profile__status=status)
        # Axtarış
        search = self.request.GET.get('q', '').strip()
        if search:
            qs = qs.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search) |
                Q(phone__icontains=search)
            )
        return qs

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Tələbələr'
        context['current_status'] = self.request.GET.get('status', '')
        context['search_query'] = self.request.GET.get('q', '')
        context['status_counts'] = {
            'all': User.objects.filter(role=User.Role.STUDENT).count(),
            'active': StudentProfile.objects.filter(status='active').count(),
            'pending': StudentProfile.objects.filter(status='pending').count(),
            'inactive': StudentProfile.objects.filter(status='inactive').count(),
            'frozen': StudentProfile.objects.filter(status='frozen').count(),
        }
        return context


class StudentDetailView(TeacherRequiredMixin, DetailView):
    """CRM — Tələbə detalları."""
    model = User
    template_name = 'users/student_detail.html'
    context_object_name = 'student'

    def get_queryset(self):
        return User.objects.filter(
            role=User.Role.STUDENT
        ).select_related('student_profile')

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        student = self.object
        context['page_title'] = f'Tələbə — {student.get_full_name()}'
        context['profile'] = getattr(student, 'student_profile', None)

        # Son dərslər
        from apps.bookings.models import Booking
        context['recent_bookings'] = (
            Booking.objects
            .filter(student=student)
            .select_related('slot', 'course')
            .order_by('-slot__start_time')[:10]
        )

        # Ödəniş xülasəsi
        from apps.payments.models import Payment
        context['total_paid'] = (
            Payment.objects
            .filter(student=student, status='completed')
            .aggregate(total=Sum('amount'))['total'] or 0
        )
        context['pending_payments'] = (
            Payment.objects
            .filter(student=student, status='pending')
            .count()
        )

        # Dərs statistikası
        context['total_lessons'] = Booking.objects.filter(student=student).count()
        context['completed_lessons'] = Booking.objects.filter(
            student=student, status='completed'
        ).count()

        return context


class StudentStatusUpdateView(TeacherRequiredMixin, View):
    """CRM — Tələbə statusunu dəyiş."""

    def post(self, request, pk):
        student = get_object_or_404(User, pk=pk, role=User.Role.STUDENT)
        new_status = request.POST.get('status', '')

        valid_statuses = [s[0] for s in StudentProfile.Status.choices]
        if new_status not in valid_statuses:
            messages.error(request, 'Yanlış status.')
            return redirect('users:student-detail', pk=pk)

        profile = student.student_profile
        profile.status = new_status
        profile.status_changed_at = timezone.now()
        profile.save(update_fields=['status', 'status_changed_at'])

        # Əgər aktiv edildiyi halda user deaktivdirsə
        if new_status == 'active' and not student.is_active:
            student.is_active = True
            student.save(update_fields=['is_active'])
        elif new_status in ('inactive', 'frozen') and student.is_active:
            student.is_active = False
            student.save(update_fields=['is_active'])

        messages.success(
            request,
            f'{student.get_full_name()} statusu "{profile.get_status_display()}" olaraq dəyişdirildi.'
        )
        return redirect('users:student-detail', pk=pk)


class StudentNotesUpdateView(TeacherRequiredMixin, View):
    """CRM — Tələbə müəllim qeydləri."""

    def post(self, request, pk):
        student = get_object_or_404(User, pk=pk, role=User.Role.STUDENT)
        notes = request.POST.get('teacher_notes', '')
        profile = student.student_profile
        profile.teacher_notes = notes
        profile.save(update_fields=['teacher_notes'])
        messages.success(request, 'Qeydlər saxlanıldı.')
        return redirect('users:student-detail', pk=pk)


class RegistrationRequestListView(TeacherRequiredMixin, ListView):
    """Müəllim üçün qeydiyyat müraciətləri siyahısı."""

    model = RegistrationRequest
    template_name = 'users/registration_requests.html'
    context_object_name = 'requests'
    paginate_by = 20

    def get_queryset(self):
        status = self.request.GET.get('status', '')
        qs = RegistrationRequest.objects.order_by('-created_at')
        if status in ('pending', 'approved', 'rejected'):
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Qeydiyyat müraciətləri'
        context['current_status'] = self.request.GET.get('status', '')
        context['pending_count'] = RegistrationRequest.objects.filter(
            status=RegistrationRequest.Status.PENDING
        ).count()
        return context


class RegistrationRequestDetailView(TeacherRequiredMixin, DetailView):
    """Qeydiyyat müraciəti detalları."""

    model = RegistrationRequest
    template_name = 'users/registration_request_detail.html'
    context_object_name = 'reg_request'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Müraciət — {self.object.full_name}'
        # Aylıq ödəniş hesabla
        from core.utils import calculate_monthly_price
        context['monthly_price'] = calculate_monthly_price(
            self.object.lessons_per_week
        )
        # ePoint ödəniş statusu
        from apps.payments.models import Payment
        context['reg_payment'] = (
            Payment.objects
            .filter(registration_request=self.object)
            .order_by('-created_at')
            .first()
        )
        return context


class ApproveRegistrationView(TeacherRequiredMixin, View):
    """Qeydiyyat müraciətini təsdiqlə — User yarat, parol göndər."""

    def post(self, request, pk):
        service = UserService()
        user, error = service.approve_registration_request(
            request_id=str(pk),
            teacher=request.user,
        )
        if user:
            messages.success(
                request,
                f'{user.get_full_name()} hesabı yaradıldı. '
                f'Login məlumatları {user.email} ünvanına göndərildi.'
            )
        else:
            messages.error(request, error or 'Müraciət təsdiqlənə bilmədi.')
        return redirect('users:registration-requests')

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(['POST'])


class RejectRegistrationView(TeacherRequiredMixin, View):
    """Qeydiyyat müraciətini rədd et."""

    def post(self, request, pk):
        notes = request.POST.get('notes', '')
        service = UserService()
        success = service.reject_registration_request(
            request_id=str(pk),
            teacher=request.user,
            notes=notes,
        )
        if success:
            messages.success(request, 'Müraciət rədd edildi.')
        else:
            messages.error(request, 'Müraciət rədd edilə bilmədi.')
        return redirect('users:registration-requests')

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(['POST'])


class StudentRegisterView(TemplateView):
    """Tələbə dərs qeydiyyat formu (Google Form tipli)."""
    template_name = 'auth/register.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('analytics:dashboard')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['form'] = CourseRegistrationForm()
        context['page_title'] = 'Dərs qeydiyyat formu'
        return context

    def post(self, request, *args, **kwargs):
        form = CourseRegistrationForm(request.POST)
        if form.is_valid():
            reg_request = form.save()
            payment_method = form.cleaned_data.get('payment_method', 'epoint')

            # Aylıq ödəniş hesabla
            from core.utils import calculate_monthly_price
            monthly = calculate_monthly_price(reg_request.lessons_per_week)

            # ePoint ödəniş yarat
            from apps.payments.services import PaymentService
            payment_service = PaymentService()
            payment = payment_service.create_registration_payment(
                registration_request_id=str(reg_request.id),
                amount=monthly,
            )

            request.session['reg_monthly_price'] = str(monthly)
            request.session['reg_lessons_per_week'] = reg_request.lessons_per_week
            request.session['reg_request_id'] = str(reg_request.id)
            if payment:
                request.session['reg_payment_id'] = str(payment.id)

            # ePoint seçilibsə birbaşa ödəniş səhifəsinə yönləndir
            if payment_method == 'epoint' and payment:
                from django.conf import settings as conf_settings
                site_url = getattr(conf_settings, 'SITE_URL', 'http://localhost:8000')
                redirect_url = payment_service.initiate_registration_payment(
                    payment_id=str(payment.id),
                    success_url=f'{site_url}/auth/register/success/?payment=success',
                    error_url=f'{site_url}/auth/register/success/?payment=failed',
                )
                if redirect_url:
                    messages.success(
                        request,
                        'Qeydiyyatınız qəbul edildi! Ödəniş səhifəsinə yönləndirilirsiniz...'
                    )
                    return redirect(redirect_url)

            messages.success(
                request,
                'Qeydiyyatınız uğurla qəbul edildi!'
            )
            return redirect('users:register-success')
        return self.render_to_response({
            'form': form,
            'page_title': 'Dərs qeydiyyat formu',
        })


class RegisterSuccessView(TemplateView):
    """Qeydiyyat uğurlu səhifəsi — ödəniş məlumatı ilə."""
    template_name = 'auth/register_success.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['monthly_price'] = self.request.session.get('reg_monthly_price', '0')
        context['lessons_per_week'] = self.request.session.get('reg_lessons_per_week', 2)
        context['reg_request_id'] = self.request.session.get('reg_request_id', '')
        context['payment_id'] = self.request.session.get('reg_payment_id', '')
        # ePoint-dən qayıdış statusu
        context['payment_status'] = self.request.GET.get('payment', '')
        return context


class RegisterPaymentView(View):
    """Qeydiyyat ödənişi üçün ePoint-ə yönləndir (login tələb olunmur)."""

    def post(self, request):
        payment_id = request.session.get('reg_payment_id', '')
        if not payment_id:
            messages.error(request, 'Ödəniş tapılmadı.')
            return redirect('users:register')

        from apps.payments.services import PaymentService
        from django.conf import settings

        service = PaymentService()
        site_url = getattr(settings, 'SITE_URL', 'http://localhost:8000')
        redirect_url = service.initiate_registration_payment(
            payment_id=payment_id,
            success_url=f'{site_url}/auth/register/success/?payment=success',
            error_url=f'{site_url}/auth/register/success/?payment=failed',
        )

        if redirect_url:
            return redirect(redirect_url)

        messages.error(
            request,
            'Ödəniş sisteminə bağlanılmadı. Zəhmət olmasa yenidən cəhd edin.'
        )
        return redirect('users:register-success')


class ProfileView(LoginRequiredMixin, TemplateView):
    """İstifadəçi profil səhifəsi."""
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Profilim'
        if self.request.user.is_student_user:
            context['profile'] = getattr(self.request.user, 'student_profile', None)
        return context


class StudentProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Tələbə profil yeniləmə."""
    model = StudentProfile
    form_class = StudentProfileUpdateForm
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user.student_profile

    def form_valid(self, form):
        messages.success(self.request, 'Profil uğurla yeniləndi!')
        return super().form_valid(form)
