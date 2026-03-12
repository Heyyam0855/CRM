"""Courses App — Views"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib import messages
from django.urls import reverse_lazy

from core.mixins import TeacherRequiredMixin, HTMXMixin
from .models import Course, Enrollment
from .forms import CourseForm


class CourseListView(LoginRequiredMixin, HTMXMixin, ListView):
    """Kurs siyahısı."""
    model = Course
    template_name = 'courses/course_list.html'
    partial_template_name = 'courses/partials/course_list.html'
    context_object_name = 'courses'
    paginate_by = 12

    def get_queryset(self):
        qs = Course.objects.select_related('category').filter(
            status=Course.Status.ACTIVE
        )
        if self.request.user.is_teacher:
            qs = Course.objects.select_related('category').all()
        return qs

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Kurslar'
        return context


class CourseDetailView(LoginRequiredMixin, DetailView):
    """Kurs ətraflı baxış."""
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'

    def get_queryset(self):
        return Course.objects.prefetch_related('modules__lessons').filter(
            status=Course.Status.ACTIVE
        )

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.object.title
        if self.request.user.is_student_user:
            context['enrollment'] = Enrollment.objects.filter(
                student=self.request.user,
                course=self.object
            ).first()
        return context


class CourseCreateView(TeacherRequiredMixin, CreateView):
    """Yeni kurs yaratma."""
    model = Course
    form_class = CourseForm
    template_name = 'courses/course_form.html'

    def get_success_url(self):
        return reverse_lazy('courses:detail', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Yeni kurs əlavə et'
        context['is_edit'] = False
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Kurs uğurla yaradıldı!')
        return super().form_valid(form)


class CourseUpdateView(TeacherRequiredMixin, UpdateView):
    """Kurs redaktə etmə."""
    model = Course
    form_class = CourseForm
    template_name = 'courses/course_form.html'

    def get_success_url(self):
        return reverse_lazy('courses:detail', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'{self.object.title} — Redaktə'
        context['is_edit'] = True
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Kurs uğurla yeniləndi!')
        return super().form_valid(form)
