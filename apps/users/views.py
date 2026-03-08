"""Users App — Views"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy

from .models import User, StudentProfile
from .forms import CourseRegistrationForm, StudentProfileUpdateForm
from .services import UserService


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
