from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from sending_messages.models import Recipient, Mailing, Message
from sending_messages.forms import RecipientForm, MailingForm, MessageForm
from sending_messages.mixins import MenuActiveMixin


def index(request):
    return render(request, 'sending_messages/base.html')


# Получатели рассылки
class RecipientsListView(MenuActiveMixin, ListView):
    model = Recipient
    template_name = 'sending_messages/recipients_list.html'
    context_object_name = 'recipients'


class RecipientDetailView(MenuActiveMixin, DetailView):
    model = Recipient
    template_name = 'sending_messages/recipient_detail.html'
    context_object_name = 'recipient'


class RecipientCreateView(MenuActiveMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'sending_messages/form_recipient.html'
    success_url = reverse_lazy('sending_messages:recipients_list')


class RecipientUpdateView(MenuActiveMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'sending_messages/form_recipient.html'
    success_url = reverse_lazy('sending_messages:recipients_list')


class RecipientDeleteView(MenuActiveMixin, DeleteView):
    model = Recipient
    template_name = 'sending_messages/recipient_confirm_delete.html'
    success_url = reverse_lazy('sending_messages:recipients_list')


# Рассылки
class MailingsListView(MenuActiveMixin, ListView):
    model = Mailing
    template_name = 'sending_messages/mailings_list.html'
    context_object_name = 'mailings'


class MailingDetailView(MenuActiveMixin, DetailView):
    model = Mailing
    template_name = 'sending_messages/mailing_detail.html'
    context_object_name = 'mailing'


class MailingCreateView(MenuActiveMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'sending_messages/form_mailing.html'
    success_url = reverse_lazy('sending_messages:mailings_list')


class MailingUpdateView(MenuActiveMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'sending_messages/form_mailing.html'
    success_url = reverse_lazy('sending_messages:mailings_list')


class MailingDeleteView(MenuActiveMixin, DeleteView):
    model = Mailing
    template_name = 'sending_messages/mailing_confirm_delete.html'
    success_url = reverse_lazy('sending_messages:mailings_list')


# Сообщения