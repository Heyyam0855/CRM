"""Courses App — Views"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib import messages
from django.urls import reverse_lazy

from core.mixins import TeacherRequiredMixin, HTMXMixin
from .models import Course, Module, Lesson, Enrollment


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
