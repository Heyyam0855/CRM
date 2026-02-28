"""Notifications — Django Channels Consumer"""
import json
from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    """Real-time bildiriş WebSocket consumer."""

    async def connect(self):
        self.user = self.scope['user']
        if not self.user.is_authenticated:
            await self.close()
            return

        self.group_name = f"notifications_{self.user.id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        # Oxunmamış bildiriş sayını göndər
        await self.send_unread_count()

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(
                self.group_name, self.channel_name
            )

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'mark_read':
            notification_id = data.get('notification_id')
            await self.mark_notification_read(notification_id)

    async def notification_message(self, event):
        """Channel layer-dən gələn bildirişi WebSocket-ə göndərir."""
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'title': event['title'],
            'message': event['message'],
            'notification_type': event.get('notification_type', 'general'),
            'data': event.get('data', {}),
        }))

    async def send_unread_count(self):
        from channels.db import database_sync_to_async
        count = await database_sync_to_async(self._get_unread_count)()
        await self.send(text_data=json.dumps({
            'type': 'unread_count',
            'count': count,
        }))

    def _get_unread_count(self):
        from .models import Notification
        return Notification.objects.filter(
            user=self.user, is_read=False
        ).count()

    async def mark_notification_read(self, notification_id):
        from channels.db import database_sync_to_async

        @database_sync_to_async
        def _mark():
            from .models import Notification
            Notification.objects.filter(
                id=notification_id, user=self.user
            ).update(is_read=True)

        await _mark()
        await self.send_unread_count()
