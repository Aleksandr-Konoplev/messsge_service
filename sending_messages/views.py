from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from sending_messages.models import Recipient, Mailing, Message
from sending_messages.forms import RecipientForm, MailingForm, MessageForm
from sending_messages.mixins import MenuActiveMixin
from sending_messages.services import send_mailing


def index(request):
    return render(request, 'sending_messages/base.html')

# Главная
class MainPageTemplateView(MenuActiveMixin ,TemplateView):
    template_name = 'sending_messages/main_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Приводим статусы в актуальное состояние
        Mailing.mass_update_statuses()

        # now = timezone.now()

        # Добавляем контекст
        # Общее кол-во рассылок
        context['mailings_total'] = Mailing.objects.count()
        # Объекты со статусом "запущенна"
        context['mailings_running'] = Mailing.objects.filter(
            status=Mailing.STATUS_RUNNING,
            # start_time__lte=now,
            # end_time__gte=now,
        ).count()
        # Кол-во получателей
        context['recipients_total'] = Recipient.objects.count()

        return context


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

    def get_queryset(self):
        qs = super().get_queryset()

        for mailing in qs:
            mailing.update_status()

        return qs


class MailingDetailView(MenuActiveMixin, DetailView):
    model = Mailing
    template_name = 'sending_messages/mailing_detail.html'
    context_object_name = 'mailing'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.update_status()
        return obj


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
class MessageListView(MenuActiveMixin, ListView):
    model = Message
    template_name = 'sending_messages/messages_list.html'
    context_object_name = 'messages'


class MessageDetailView(MenuActiveMixin, DetailView):
    model = Message
    template_name = 'sending_messages/message_detail.html'
    context_object_name = 'message'


class MessageCreateView(MenuActiveMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'sending_messages/form_message.html'
    success_url = reverse_lazy('sending_messages:messages_list')


class MessageUpdateView(MenuActiveMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'sending_messages/form_message.html'
    success_url = reverse_lazy('sending_messages:messages_list')


class MessageDeleteView(MenuActiveMixin, DeleteView):
    model = Message
    template_name = 'sending_messages/message_confirm_delete.html'
    success_url = reverse_lazy('sending_messages:messages_list')


# Иные действия
class MailingSendView(View):
    # noinspection PyUnusedLocal
    @staticmethod
    def post(request, pk, *args, **kwargs):
        mailing = get_object_or_404(Mailing, pk=pk)
        send_mailing(mailing)
        return redirect('sending_messages:mailings_list')