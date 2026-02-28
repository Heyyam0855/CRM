"""Users App — Services (Business Logic)"""
from typing import Optional
import logging

from django.db import transaction
from django.utils import timezone

from .models import User, StudentProfile

logger = logging.getLogger(__name__)


class UserService:
    """İstifadəçi business logic."""

    @transaction.atomic
    def register_student(self, data: dict) -> Optional[User]:
        """
        Yeni tələbə qeydiyyatı.

        Args:
            data: Form cleaned_data

        Returns:
            Optional[User]: Yaradılmış user obyekti
        """
        try:
            user = User.objects.create_user(
                email=data['email'],
                password=data['password1'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                phone=data.get('phone', ''),
                role=User.Role.STUDENT,
                is_active=False,  # Müəllim təsdiqi gözləyir
            )
            # Profil signal vasitəsilə yaradılır
            profile = user.student_profile
            profile.payment_model = data['payment_model']
            profile.lessons_per_week = data.get('lessons_per_week', 2)
            profile.goals = data.get('goals', '')
            profile.timezone = data.get('timezone', 'Asia/Baku')
            profile.save()

            logger.info(f"Yeni tələbə qeydiyyatı: {user.email}")
            return user

        except Exception as e:
            logger.error(f"Tələbə qeydiyyat xətası: {e}", exc_info=True)
            return None

    @transaction.atomic
    def approve_student(self, student_id: str, teacher) -> bool:
        """
        Müəllim tərəfindən tələbə təsdiqi.

        Args:
            student_id: Tələbənin UUID-si
            teacher: Müəllim user obyekti

        Returns:
            bool: Uğurlu olduqda True
        """
        try:
            user = User.objects.get(id=student_id, role=User.Role.STUDENT)
            user.is_active = True
            user.save(update_fields=['is_active'])

            profile = user.student_profile
            profile.status = StudentProfile.Status.ACTIVE
            profile.status_changed_at = timezone.now()
            profile.save(update_fields=['status', 'status_changed_at'])

            # GitHub repo yaratma task-ı başlat
            from apps.github_integration.tasks import create_student_repo_task
            create_student_repo_task.delay(str(user.id))

            # Email bildirişi göndər
            from apps.notifications.tasks import send_student_approval_email
            send_student_approval_email.delay(str(user.id))

            logger.info(f"Tələbə təsdiqləndi: {user.email} (teacher: {teacher.email})")
            return True

        except User.DoesNotExist:
            logger.warning(f"Tələbə tapılmadı: {student_id}")
            return False
        except Exception as e:
            logger.error(f"Tələbə təsdiq xətası: {e}", exc_info=True)
            return False
