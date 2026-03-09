"""Users App — Services (Business Logic)"""
from typing import Optional
import logging
import secrets
import string

from django.db import transaction
from django.utils import timezone

from .models import User, StudentProfile, RegistrationRequest

logger = logging.getLogger(__name__)


def generate_random_password(length: int = 12) -> str:
    """Təhlükəsiz təsadüfi parol yaradır."""
    alphabet = string.ascii_letters + string.digits + "!@#$%&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))


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
    def approve_registration_request(
        self, request_id: str, teacher
    ) -> Optional[User]:
        """
        Müəllim tərəfindən qeydiyyat müraciətini təsdiqlə.
        User hesabı yaradılır, parol generasiya edilir, email göndərilir.

        Args:
            request_id: RegistrationRequest UUID-si
            teacher: Müəllim user obyekti

        Returns:
            Optional[User]: Yaradılmış user obyekti və ya None
        """
        try:
            reg_request = RegistrationRequest.objects.get(
                id=request_id, status=RegistrationRequest.Status.PENDING
            )

            # Ad və soyadı ayır
            name_parts = reg_request.full_name.strip().split(maxsplit=1)
            first_name = name_parts[0]
            last_name = name_parts[1] if len(name_parts) > 1 else ''

            # Təsadüfi parol yarat
            raw_password = generate_random_password()

            # User hesabı yarat
            user = User.objects.create_user(
                email=reg_request.email,
                password=raw_password,
                first_name=first_name,
                last_name=last_name,
                phone=reg_request.phone,
                role=User.Role.STUDENT,
                is_active=True,
            )

            # StudentProfile yenilə (signal ilə yaradılır)
            profile = user.student_profile
            profile.status = StudentProfile.Status.ACTIVE
            profile.lessons_per_week = reg_request.lessons_per_week
            profile.status_changed_at = timezone.now()
            if reg_request.github_profile_url:
                # GitHub URL-dən username çıxar
                github_url = reg_request.github_profile_url.rstrip('/')
                profile.github_username = github_url.split('/')[-1]
            profile.save()

            # RegistrationRequest-i yenilə
            reg_request.status = RegistrationRequest.Status.APPROVED
            reg_request.approved_user = user
            reg_request.save(update_fields=['status', 'approved_user', 'updated_at'])

            # Login məlumatları ilə email göndər (async)
            from apps.notifications.tasks import send_student_credentials_email
            send_student_credentials_email.delay(
                str(user.id), raw_password
            )

            # GitHub repo yaratma task-ı başlat
            try:
                from apps.github_integration.tasks import create_student_repo_task
                create_student_repo_task.delay(str(user.id))
            except Exception:
                logger.warning(f"GitHub repo task başlada bilmədi: {user.email}")

            logger.info(
                f"Qeydiyyat təsdiqləndi: {reg_request.email} "
                f"(teacher: {teacher.email})"
            )
            return user

        except RegistrationRequest.DoesNotExist:
            logger.warning(f"Qeydiyyat müraciəti tapılmadı: {request_id}")
            return None
        except Exception as e:
            logger.error(f"Qeydiyyat təsdiq xətası: {e}", exc_info=True)
            return None

    @transaction.atomic
    def reject_registration_request(
        self, request_id: str, teacher, notes: str = ''
    ) -> bool:
        """
        Qeydiyyat müraciətini rədd et.

        Args:
            request_id: RegistrationRequest UUID-si
            teacher: Müəllim user obyekti
            notes: Rədd etmə səbəbi

        Returns:
            bool: Uğurlu olduqda True
        """
        try:
            reg_request = RegistrationRequest.objects.get(
                id=request_id, status=RegistrationRequest.Status.PENDING
            )
            reg_request.status = RegistrationRequest.Status.REJECTED
            if notes:
                reg_request.teacher_notes = notes
            reg_request.save(update_fields=['status', 'teacher_notes', 'updated_at'])

            logger.info(
                f"Qeydiyyat rədd edildi: {reg_request.email} "
                f"(teacher: {teacher.email})"
            )
            return True

        except RegistrationRequest.DoesNotExist:
            logger.warning(f"Qeydiyyat müraciəti tapılmadı: {request_id}")
            return False
        except Exception as e:
            logger.error(f"Qeydiyyat rədd xətası: {e}", exc_info=True)
            return False

    @transaction.atomic
    def approve_student(self, student_id: str, teacher) -> bool:
        """
        Müəllim tərəfindən mövcud tələbə təsdiqi.

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
