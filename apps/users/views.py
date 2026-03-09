"""Users App — Views"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView, UpdateView, DetailView, View
from django.contrib.auth import login, logout
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseNotAllowed

from core.mixins import TeacherRequiredMixin
from .models import User, StudentProfile, RegistrationRequest
from .forms import CourseRegistrationForm, StudentProfileUpdateForm
from .services import UserService


class StudentListView(TeacherRequiredMixin, ListView):
    """Müəllim üçün tələbələr siyahısı."""

    model = User
    template_name = 'users/student_list.html'
    context_object_name = 'students'
    paginate_by = 20

    def get_queryset(self):
        return (
            User.objects
            .filter(role=User.Role.STUDENT)
            .select_related('student_profile')
            .order_by('-date_joined')
        )

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Tələbələr'
        return context


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
        return context


class ApproveRegistrationView(TeacherRequiredMixin, View):
    """Qeydiyyat müraciətini təsdiqlə — User yarat, parol göndər."""

    def post(self, request, pk):
        service = UserService()
        user = service.approve_registration_request(
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
            messages.error(request, 'Müraciət təsdiqlənə bilmədi.')
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
            form.save()
            messages.success(
                request,
                'Qeydiyyatınız uğurla qəbul edildi! Sizinlə əlaqə saxlanılacaq.'
            )
            return redirect('users:register-success')
        return self.render_to_response({
            'form': form,
            'page_title': 'Dərs qeydiyyat formu',
        })


class RegisterSuccessView(TemplateView):
    """Qeydiyyat uğurlu səhifəsi."""
    template_name = 'auth/register_success.html'


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
