"""
YouTube Integration — Services
YouTube Data API v3 ilə video metadata əldə edir.
Redis cache istifadə edir (24 saat).
"""
from typing import Optional
import logging
import re

logger = logging.getLogger(__name__)

_YOUTUBE_URL_PATTERNS = [
    r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})',
    r'youtube\.com\/embed\/([a-zA-Z0-9_-]{11})',
    r'youtube\.com\/shorts\/([a-zA-Z0-9_-]{11})',
]


def extract_video_id(url: str) -> Optional[str]:
    """YouTube URL-dən video ID çıxarır."""
    for pattern in _YOUTUBE_URL_PATTERNS:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


class YouTubeService:
    """YouTube Data API v3 servis."""

    CACHE_TIMEOUT = 60 * 60 * 24  # 24 saat
    CACHE_PREFIX = 'youtube_video_'

    def get_video_metadata(self, video_id: str) -> Optional[dict]:
        """
        Video metadata əldə edir (Redis cache ilə).

        Args:
            video_id: YouTube video ID

        Returns:
            Optional[dict]: video_id, title, duration, thumbnail_url, description
        """
        cache_key = f"{self.CACHE_PREFIX}{video_id}"

        try:
            from django.core.cache import cache
            cached = cache.get(cache_key)
            if cached:
                logger.debug(f"Cache hit: {video_id}")
                return cached

            metadata = self._fetch_from_api(video_id)
            if metadata:
                cache.set(cache_key, metadata, self.CACHE_TIMEOUT)
                logger.info(f"YouTube metadata alındı: {video_id}")

            return metadata

        except Exception as e:
            logger.error(f"YouTube metadata xətası: {e}", exc_info=True)
            return None

    def _fetch_from_api(self, video_id: str) -> Optional[dict]:
        """YouTube API-dən birbaşa sorğu."""
        try:
            from django.conf import settings
            from googleapiclient.discovery import build

            api_key = getattr(settings, 'YOUTUBE_API_KEY', '')
            if not api_key:
                logger.warning("YOUTUBE_API_KEY təyin edilməyib")
                return None

            youtube = build('youtube', 'v3', developerKey=api_key)
            response = youtube.videos().list(
                part='snippet,contentDetails',
                id=video_id
            ).execute()

            items = response.get('items', [])
            if not items:
                return None

            item = items[0]
            snippet = item.get('snippet', {})
            content_details = item.get('contentDetails', {})

            # ISO 8601 müddəti çevir
            duration_str = content_details.get('duration', 'PT0S')
            duration_minutes = self._parse_duration(duration_str)

            thumbnails = snippet.get('thumbnails', {})
            thumbnail = (
                thumbnails.get('maxres') or
                thumbnails.get('high') or
                thumbnails.get('medium') or {}
            )

            return {
                'video_id': video_id,
                'title': snippet.get('title', ''),
                'description': snippet.get('description', '')[:500],
                'duration_minutes': duration_minutes,
                'thumbnail_url': thumbnail.get('url', ''),
                'channel_title': snippet.get('channelTitle', ''),
                'published_at': snippet.get('publishedAt', ''),
            }

        except Exception as e:
            logger.error(f"YouTube API sorğu xətası: {e}", exc_info=True)
            return None

    def _parse_duration(self, duration: str) -> int:
        """ISO 8601 duration → dəqiqəyə çevir (PT1H2M3S → 62)."""
        import re
        match = re.match(
            r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration
        )
        if not match:
            return 0
        hours = int(match.group(1) or 0)
        minutes = int(match.group(2) or 0)
        seconds = int(match.group(3) or 0)
        return hours * 60 + minutes + (1 if seconds >= 30 else 0)
