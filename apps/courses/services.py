"""Courses App — Services"""
from typing import Optional
import logging

from django.db import transaction

from .models import Course, Lesson

logger = logging.getLogger(__name__)


class CourseService:
    """Kurs business logic."""

    @transaction.atomic
    def create_lesson_with_youtube(
        self,
        lesson: Lesson,
        youtube_url: str
    ) -> bool:
        """
        YouTube metadata-sı ilə dərs materialı yaradır.

        Args:
            lesson: Lesson instance
            youtube_url: YouTube video URL

        Returns:
            bool: Uğurlu olduqda True
        """
        try:
            from apps.youtube.services import YouTubeService
            yt = YouTubeService()
            metadata = yt.get_video_metadata(youtube_url)
            if metadata:
                lesson.youtube_video_id = metadata.get('video_id', '')
                lesson.youtube_title = metadata.get('title', '')
                lesson.youtube_duration = metadata.get('duration', '')
                lesson.save(
                    update_fields=['youtube_video_id', 'youtube_title', 'youtube_duration']
                )
            logger.info(f"Dərs materialı yaradıldı: {lesson.title}")
            return True
        except Exception as e:
            logger.error(f"Dərs yaratma xətası: {e}", exc_info=True)
            return False
