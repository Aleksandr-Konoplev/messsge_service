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
        user = self.request.user

        if self.request.user.is_authenticated:
            # Приводим статусы в актуальное состояние
            Mailing.mass_update_statuses(user=user)
            # Добавляем контекст
            # Общее кол-во рассылок
            context['mailings_total'] = Mailing.objects.filter(owner=user).count()
            # Объекты со статусом "запущенна"
            context['mailings_running'] = Mailing.objects.filter(owner=user, status=Mailing.STATUS_RUNNING).count()
            # Кол-во получателей
            context['recipients_total'] = Recipient.objects.filter(owner=user).count()
        else:
            context['mailings_total'] = 'Доступно только авторизованным пользователям'
            context['mailings_running'] = 'Доступно только авторизованным пользователям'
            context['recipients_total'] = 'Доступно только авторизованным пользователям'


        return context


# Получатели рассылки
class RecipientsListView(MenuActiveMixin, ListView):
    model = Recipient
    template_name = 'sending_messages/recipients_list.html'
    context_object_name = 'recipients'

    def get_queryset(self):
        return Recipient.objects.filter(owner=self.request.user)


class RecipientDetailView(MenuActiveMixin, DetailView):
    model = Recipient
    template_name = 'sending_messages/recipient_detail.html'
    context_object_name = 'recipient'

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class RecipientCreateView(MenuActiveMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'sending_messages/form_recipient.html'
    success_url = reverse_lazy('sending_messages:recipients_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class RecipientUpdateView(MenuActiveMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'sending_messages/form_recipient.html'
    success_url = reverse_lazy('sending_messages:recipients_list')

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class RecipientDeleteView(MenuActiveMixin, DeleteView):
    model = Recipient
    template_name = 'sending_messages/recipient_confirm_delete.html'
    success_url = reverse_lazy('sending_messages:recipients_list')

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


# Рассылки
class MailingsListView(MenuActiveMixin, ListView):
    model = Mailing
    template_name = 'sending_messages/mailings_list.html'
    context_object_name = 'mailings'

    def get_queryset(self):
        qs = super().get_queryset().filter(owner=self.request.user)

        for mailing in qs:
            mailing.update_status()

        return qs


class MailingDetailView(MenuActiveMixin, DetailView):
    model = Mailing
    template_name = 'sending_messages/mailing_detail.html'
    context_object_name = 'mailing'

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.update_status()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['attempts'] = (
            self.object.attempts
            .select_related('recipient')
            .order_by('-created_at')
        )
        return context


class MailingCreateView(MenuActiveMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'sending_messages/form_mailing.html'
    success_url = reverse_lazy('sending_messages:mailings_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingUpdateView(MenuActiveMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'sending_messages/form_mailing.html'
    success_url = reverse_lazy('sending_messages:mailings_list')

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class MailingDeleteView(MenuActiveMixin, DeleteView):
    model = Mailing
    template_name = 'sending_messages/mailing_confirm_delete.html'
    success_url = reverse_lazy('sending_messages:mailings_list')

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


# Сообщения
class MessageListView(MenuActiveMixin, ListView):
    model = Message
    template_name = 'sending_messages/messages_list.html'
    context_object_name = 'messages'

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class MessageDetailView(MenuActiveMixin, DetailView):
    model = Message
    template_name = 'sending_messages/message_detail.html'
    context_object_name = 'message'

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class MessageCreateView(MenuActiveMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'sending_messages/form_message.html'
    success_url = reverse_lazy('sending_messages:messages_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(MenuActiveMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'sending_messages/form_message.html'
    success_url = reverse_lazy('sending_messages:messages_list')

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class MessageDeleteView(MenuActiveMixin, DeleteView):
    model = Message
    template_name = 'sending_messages/message_confirm_delete.html'
    success_url = reverse_lazy('sending_messages:messages_list')

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


# Иные действия
class MailingSendView(View):
    # noinspection PyUnusedLocal
    @staticmethod
    def post(request, pk, *args, **kwargs):
        mailing = get_object_or_404(Mailing, pk=pk)
        send_mailing(mailing)
        return redirect('sending_messages:mailings_list')