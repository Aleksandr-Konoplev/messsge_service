from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from sending_messages.models import Recipient, Mailing, Message
from sending_messages.forms import RecipientForm, MailingForm, MessageForm
from sending_messages.mixins import MenuActiveMixin, OwnerOrManagerMixin
from sending_messages.services import send_mailing


from django.views.generic import CreateView
from django.urls import reverse_lazy
from sending_messages.models import Mailing, Recipient, Message
from sending_messages.forms import MailingForm
from sending_messages.mixins import OwnerOrManagerMixin, MenuActiveMixin


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
            add_context = {'mailings_total': Mailing.objects.filter(owner=user).count(),
                           'mailings_running': Mailing.objects.filter(owner=user, status=Mailing.STATUS_RUNNING).count(),
                           'recipients_total': Recipient.objects.filter(owner=user).count()}
            context.update(add_context)
        else:

            add_context = {'mailings_total': 'Нужна регистрация',
                           'mailings_running': 'Нужна регистрация',
                           'recipients_total': 'Нужна регистрация',}
            context.update(add_context)



        return context


###########################
### Получатели рассылки ###
###########################
class RecipientsListView(OwnerOrManagerMixin, MenuActiveMixin, ListView):
    model = Recipient
    template_name = 'sending_messages/recipients_list.html'
    context_object_name = 'recipients'

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        # Если админ, или менеджер возвращаем всё
        if user.is_staff or user.is_superuser:
            return qs
        return qs.filter(owner=user)


class RecipientDetailView(OwnerOrManagerMixin, MenuActiveMixin, DetailView):
    model = Recipient
    template_name = 'sending_messages/recipient_detail.html'
    context_object_name = 'recipient'

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        # Выполняем проверку как в RecipientsListView на случай ручного ввода в адресной строке
        if user.is_staff or user.is_superuser:
            return qs
        return qs.filter(owner=user)


class RecipientCreateView(OwnerOrManagerMixin, MenuActiveMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'sending_messages/form_recipient.html'
    success_url = reverse_lazy('sending_messages:recipients_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class RecipientUpdateView(OwnerOrManagerMixin, MenuActiveMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'sending_messages/form_recipient.html'
    success_url = reverse_lazy('sending_messages:recipients_list')

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class RecipientDeleteView(OwnerOrManagerMixin, MenuActiveMixin, DeleteView):
    model = Recipient
    template_name = 'sending_messages/recipient_confirm_delete.html'
    success_url = reverse_lazy('sending_messages:recipients_list')

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

################
### Рассылки ###
################
class MailingsListView(OwnerOrManagerMixin, MenuActiveMixin, ListView):
    model = Mailing
    template_name = 'sending_messages/mailings_list.html'
    context_object_name = 'mailings'

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        # Если не админ и менеджер фильтруем
        if not user.is_staff and not user.is_superuser:
            qs = qs.filter(owner=user)
        # В каждой рассылке вызываем обновление статуса
        for mailing in qs:
            mailing.update_status()
        return qs


class MailingDetailView(OwnerOrManagerMixin, MenuActiveMixin, DetailView):
    model = Mailing
    template_name = 'sending_messages/mailing_detail.html'
    context_object_name = 'mailing'

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if not (user.is_staff or user.is_superuser):
            qs = qs.filter(owner=user)
        return qs

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


class MailingCreateView(OwnerOrManagerMixin, MenuActiveMixin, CreateView):
    """
    Создание рассылки (Mailing) с фильтрацией Получателей (Recipients) и Сообщений (Messages)
    """
    model = Mailing
    form_class = MailingForm
    template_name = 'sending_messages/form_mailing.html'
    success_url = reverse_lazy('sending_messages:mailings_list')

    def get_form(self, form_class=None):
        """
        Переопределяем форму, чтобы ограничить поля recipients и message объектами текущего пользователя.
        """
        form = super().get_form(form_class)
        user = self.request.user

        # Для обычного пользователя фильтруем получателей
        if not user.is_staff and not user.is_superuser:
            form.fields['recipients'].queryset = Recipient.objects.filter(owner=user)
            # Фильтруем сообщения
            form.fields['message'].queryset = Message.objects.filter(owner=user)

        return form

    def form_valid(self, form):
        user = self.request.user

        # Присваиваем владельца Mailing
        form.instance.owner = user

        # Сохраняем объект, чтобы ManyToMany и ForeignKey можно было обработать
        response = super().form_valid(form)

        # Фильтруем ManyToMany recipients — оставляем только свои
        if form.instance.recipients.exists() and not user.is_staff and not user.is_superuser:
            user_recipients = form.instance.recipients.filter(owner=user)
            form.instance.recipients.set(user_recipients)

        # Фильтруем поле message — оставляем только свое сообщение
        if form.instance.message and not user.is_staff and not user.is_superuser:
            if form.instance.message.owner != user:
                # Если сообщение чужое, сбрасываем выбор (можно также вызвать ошибку)
                form.instance.message = None
                form.instance.save(update_fields=['message'])

        # Назначаем владельца новым Recipient
        for recipient in form.instance.recipients.all():
            if recipient.owner is None:
                recipient.owner = user
                recipient.save()

        # Назначаем владельца новому Message (если это создаётся через форму)
        message = form.instance.message
        if message and message.owner is None:
            message.owner = user
            message.save()

        return response


class MailingUpdateView(OwnerOrManagerMixin, MenuActiveMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'sending_messages/form_mailing.html'
    success_url = reverse_lazy('sending_messages:mailings_list')

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class MailingDeleteView(OwnerOrManagerMixin, MenuActiveMixin, DeleteView):
    model = Mailing
    template_name = 'sending_messages/mailing_confirm_delete.html'
    success_url = reverse_lazy('sending_messages:mailings_list')

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


#################
### Сообщения ###
#################
class MessageListView(OwnerOrManagerMixin, MenuActiveMixin, ListView):
    model = Message
    template_name = 'sending_messages/messages_list.html'
    context_object_name = 'messages'

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if not (user.is_staff or user.is_superuser):
            qs = qs.filter(owner=user)
        return qs


class MessageDetailView(OwnerOrManagerMixin, MenuActiveMixin, DetailView):
    model = Message
    template_name = 'sending_messages/message_detail.html'
    context_object_name = 'message'

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if not (user.is_staff or user.is_superuser):
            qs = qs.filter(owner=user)
        return qs


class MessageCreateView(OwnerOrManagerMixin, MenuActiveMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'sending_messages/form_message.html'
    success_url = reverse_lazy('sending_messages:messages_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(OwnerOrManagerMixin, MenuActiveMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'sending_messages/form_message.html'
    success_url = reverse_lazy('sending_messages:messages_list')

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class MessageDeleteView(OwnerOrManagerMixin, MenuActiveMixin, DeleteView):
    model = Message
    template_name = 'sending_messages/message_confirm_delete.html'
    success_url = reverse_lazy('sending_messages:messages_list')

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


#####################
### Иные действия ###
#####################
class MailingSendView(View):
    # noinspection PyUnusedLocal
    @staticmethod
    def post(request, pk, *args, **kwargs):
        mailing = get_object_or_404(Mailing, pk=pk)
        send_mailing(mailing)
        return redirect('sending_messages:mailings_list')