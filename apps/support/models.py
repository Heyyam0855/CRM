"""Support — Models"""
from apps.users.models import BaseModel
from django.db import models


class Ticket(BaseModel):
    """Dəstək ticket modeli."""

    class Status(models.TextChoices):
        OPEN = 'open', 'Açıq'
        IN_PROGRESS = 'in_progress', 'İşlənir'
        RESOLVED = 'resolved', 'Həll edildi'
        CLOSED = 'closed', 'Bağlı'

    class Priority(models.TextChoices):
        LOW = 'low', 'Aşağı'
        MEDIUM = 'medium', 'Orta'
        HIGH = 'high', 'Yüksək'
        URGENT = 'urgent', 'Təcili'

    student = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='support_tickets',
        verbose_name='Tələbə'
    )
    subject = models.CharField(max_length=200, verbose_name='Mövzu')
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OPEN,
        verbose_name='Status'
    )
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM,
        verbose_name='Prioritet'
    )
    resolved_at = models.DateTimeField(null=True, blank=True, verbose_name='Həll tarixi')

    class Meta:
        db_table = 'support_ticket'
        verbose_name = 'Ticket'
        verbose_name_plural = 'Ticketlər'
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"#{self.id} — {self.subject} ({self.get_status_display()})"


class TicketMessage(BaseModel):
    """Ticket mesajı."""
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Ticket'
    )
    sender = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        verbose_name='Göndərən'
    )
    body = models.TextField(verbose_name='Mesaj')
    is_from_teacher = models.BooleanField(default=False, verbose_name='Müəllimdəndir')

    class Meta:
        db_table = 'support_ticket_message'
        verbose_name = 'Ticket Mesajı'
        verbose_name_plural = 'Ticket Mesajları'
        ordering = ['created_at']

    def __str__(self) -> str:
        return f"Ticket #{self.ticket_id} — {self.sender.email}"
