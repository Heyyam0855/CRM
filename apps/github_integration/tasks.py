"""GitHub Integration — Celery Tasks"""
from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    queue='github'
)
def create_student_repo_task(self, student_id: str, course_id: str) -> dict:
    """
    Tələbə üçün GitHub repository yaradır.

    Args:
        student_id: Tələbə UUID-si
        course_id: Kurs UUID-si

    Returns:
        dict: Nəticə
    """
    try:
        from apps.users.models import User
        from apps.courses.models import Course
        from .models import StudentRepository
        from .services import GitHubService
        from core.utils import get_repo_name

        student = User.objects.get(id=student_id)
        course = Course.objects.get(id=course_id)

        # Idempotency — artıq yaradılıbsa keç
        existing = StudentRepository.objects.filter(
            student=student,
            course=course,
            status=StudentRepository.Status.CREATED
        ).first()
        if existing:
            logger.info(f"Repo artıq mövcuddur: {existing.repo_url}")
            return {'success': True, 'url': existing.repo_url, 'skipped': True}

        # Record yarat/tap
        student_repo, _ = StudentRepository.objects.get_or_create(
            student=student,
            course=course,
            defaults={'status': StudentRepository.Status.CREATING}
        )
        student_repo.status = StudentRepository.Status.CREATING
        student_repo.save(update_fields=['status'])

        repo_name = get_repo_name(student.get_full_name(), course.slug)
        student_repo.repo_name = repo_name

        github_service = GitHubService()
        github_username = getattr(student.studentprofile, 'github_username', '')

        url = github_service.create_student_repository(
            repo_name=repo_name,
            student_github_username=github_username,
            description=f"LMS — {student.get_full_name()} — {course.title}"
        )

        if url:
            student_repo.repo_url = url
            student_repo.repo_full_name = f"{github_service.org or 'user'}/{repo_name}"
            student_repo.status = StudentRepository.Status.CREATED
            student_repo.save(update_fields=['repo_name', 'repo_url', 'repo_full_name', 'status'])

            # Tələbənin profilini yenilə
            profile = student.studentprofile
            profile.github_repo_url = url
            profile.save(update_fields=['github_repo_url'])

            logger.info(f"GitHub repo yaradıldı: {url}")
            return {'success': True, 'url': url}
        else:
            student_repo.status = StudentRepository.Status.FAILED
            student_repo.save(update_fields=['status'])
            return {'success': False, 'error': 'Repo yaradıla bilmədi'}

    except Exception as exc:
        logger.error(f"GitHub repo task xətası: {exc}", exc_info=True)
        raise self.retry(exc=exc)
