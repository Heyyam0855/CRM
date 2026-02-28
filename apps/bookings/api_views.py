# Bookings API Views (DRF)
from rest_framework import generics, permissions
from apps.bookings.models import Booking, AvailabilitySlot


class BookingListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        from apps.bookings.models import Booking
        qs = Booking.objects.select_related('student', 'slot')
        if self.request.user.is_student_user:
            qs = qs.filter(student=self.request.user)
        return qs

    def list(self, request, *args, **kwargs):
        from django.http import JsonResponse
        qs = self.get_queryset()
        data = [
            {
                'id': str(b.id),
                'student': b.student.get_full_name(),
                'scheduled_at': b.slot.start_time.isoformat(),
                'status': b.status,
                'topic': b.topic,
                'meet_link': b.meet_link,
                'is_paid': b.is_paid,
            }
            for b in qs[:50]
        ]
        return JsonResponse({'results': data, 'count': len(data)})
