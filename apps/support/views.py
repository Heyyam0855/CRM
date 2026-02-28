"""Support — Views"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages

from .models import Ticket, TicketMessage
from .forms import TicketCreateForm, TicketMessageForm


class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'support/ticket_list.html'
    context_object_name = 'tickets'
    paginate_by = 20

    def get_queryset(self):
        qs = Ticket.objects.select_related('student')
        if self.request.user.is_student_user:
            qs = qs.filter(student=self.request.user)
        return qs.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Dəstək Ticketləri'
        return context


class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    form_class = TicketCreateForm
    template_name = 'support/ticket_form.html'
    success_url = reverse_lazy('support:list')

    def form_valid(self, form):
        form.instance.student = self.request.user
        messages.success(self.request, 'Ticket uğurla yaradıldı!')
        return super().form_valid(form)


class TicketDetailView(LoginRequiredMixin, DetailView):
    model = Ticket
    template_name = 'support/ticket_detail.html'
    context_object_name = 'ticket'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message_form'] = TicketMessageForm()
        context['messages_list'] = self.object.messages.select_related('sender').all()
        return context
