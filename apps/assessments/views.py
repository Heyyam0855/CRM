"""Assessments — Views"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages

from .models import Assessment
from .forms import AssessmentCreateForm, AssessmentGradeForm
from core.mixins import TeacherRequiredMixin


class AssessmentListView(LoginRequiredMixin, ListView):
    model = Assessment
    template_name = 'assessments/assessment_list.html'
    context_object_name = 'assessments'
    paginate_by = 20

    def get_queryset(self):
        qs = Assessment.objects.select_related('student', 'lesson')
        if self.request.user.is_student_user:
            qs = qs.filter(student=self.request.user)
        return qs.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Qiymətləndirmələr'
        return context


class AssessmentCreateView(TeacherRequiredMixin, CreateView):
    model = Assessment
    form_class = AssessmentCreateForm
    template_name = 'assessments/assessment_form.html'
    success_url = reverse_lazy('assessments:list')

    def form_valid(self, form):
        messages.success(self.request, 'Qiymətləndirmə yaradıldı!')
        return super().form_valid(form)


class AssessmentGradeView(TeacherRequiredMixin, UpdateView):
    model = Assessment
    form_class = AssessmentGradeForm
    template_name = 'assessments/assessment_grade.html'
    success_url = reverse_lazy('assessments:list')

    def form_valid(self, form):
        messages.success(self.request, 'Qiymət qeyd edildi!')
        return super().form_valid(form)
