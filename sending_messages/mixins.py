# noinspection PyMethodMayBeStatic,PyUnresolvedReferences
# Для MenuActiveMixin
from django.views.generic.base import ContextMixin

# Для OwnerMixin
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import ModelFormMixin
from django.views.generic.list import MultipleObjectMixin


class MenuActiveMixin(ContextMixin):
    """
    Добавляет в контекст список URL для пунктов меню,
    чтобы подсвечивать активный элемент.
    """
    menu_urls = {
        'mailings': [
            'mailings_list',
            'mailing_detail',
            'mailing_create',
            'mailing_update',
            'mailing_delete',
        ],
        'recipients': [
            'recipients_list',
            'recipient_detail',
            'recipient_create',
            'recipient_update',
            'recipient_delete',
        ],
        'messages': [
            'message_delete',
            'message_update',
            'message_create',
            'message_detail',
            'messages_list',
        ],
        'main_page': [
            'main_page'
        ]
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_urls'] = self.menu_urls
        return context


class OwnerMixin(LoginRequiredMixin, View, MultipleObjectMixin, ModelFormMixin):
    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_superuser:
            return qs
        return qs.filter(owner=self.request.user)

    def form_valid(self, form):
        if not form.instance.pk:
            form.instance.owner = self.request.user
        return super().form_valid(form)