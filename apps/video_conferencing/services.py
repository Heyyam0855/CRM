"""
Video Conferencing — Services
Google Meet linki yaratmaq üçün Google Calendar API istifadə edir.
"""
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class GoogleMeetService:
    """Google Meet inteqrasiya servisi."""

    def create_meeting(
        self,
        topic: str,
        start_time,
        duration_minutes: int = 60,
        attendee_email: Optional[str] = None
    ) -> Optional[str]:
        """
        Google Calendar API vasitəsilə Meet linkli tədbir yaradır.

        Args:
            topic: Görüşün mövzusu
            start_time: Başlama vaxtı (datetime)
            duration_minutes: Müddət (dəqiqə)
            attendee_email: İştirakçının emaili

        Returns:
            Optional[str]: Meet link (hangoutLink)
        """
        try:
            from django.conf import settings
            from google.oauth2.credentials import Credentials
            from googleapiclient.discovery import build
            from datetime import timedelta
            import json

            creds_json = getattr(settings, 'GOOGLE_CREDENTIALS_JSON', '')
            if not creds_json:
                logger.warning("GOOGLE_CREDENTIALS_JSON təyin edilməyib")
                return None

            creds_data = json.loads(creds_json) if isinstance(creds_json, str) else creds_json
            creds = Credentials.from_authorized_user_info(creds_data)
            service = build('calendar', 'v3', credentials=creds)

            end_time = start_time + timedelta(minutes=duration_minutes)
            event_body = {
                'summary': topic,
                'start': {
                    'dateTime': start_time.isoformat(),
                    'timeZone': 'Asia/Baku',
                },
                'end': {
                    'dateTime': end_time.isoformat(),
                    'timeZone': 'Asia/Baku',
                },
                'conferenceData': {
                    'createRequest': {
                        'requestId': f"lms-{start_time.timestamp()}",
                        'conferenceSolutionKey': {'type': 'hangoutsMeet'}
                    }
                },
            }

            if attendee_email:
                event_body['attendees'] = [{'email': attendee_email}]

            event = service.events().insert(
                calendarId='primary',
                body=event_body,
                conferenceDataVersion=1,
                sendUpdates='all' if attendee_email else 'none'
            ).execute()

            meet_link = event.get('hangoutLink', '')
            if meet_link:
                logger.info(f"Google Meet yaradıldı: {meet_link}")
                return meet_link

            return None

        except Exception as e:
            logger.error(f"Google Meet xətası: {e}", exc_info=True)
            return None
