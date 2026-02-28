"""Courses API URLs"""
from django.urls import path
from django.http import JsonResponse
from django.views import View


class CourseListAPIView(View):
    def get(self, request, *args, **kwargs):
        from apps.courses.models import Course
        courses = Course.objects.filter(
            status=Course.Status.ACTIVE
        ).values('id', 'title', 'slug', 'level')[:50]
        return JsonResponse({'results': list(courses)})


urlpatterns = [
    path('courses/', CourseListAPIView.as_view(), name='api-course-list'),
]
