# noinspection PyMethodMayBeStatic,PyUnresolvedReferences
# Для MenuActiveMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic.base import ContextMixin

# Для OwnerMixin
# from django.views import View
# from django.core.exceptions import PermissionDenied
from django.views.generic.edit import CreateView

# from django.views.generic.list import MultipleObjectMixin


class MenuActiveMixin(ContextMixin):
    """
    Добавляет в контекст список URL для пунктов меню,
    чтобы подсвечивать активный элемент.
    """

    menu_urls = {
        "mailings": [
            "mailings_list",
            "mailing_detail",
            "mailing_create",
            "mailing_update",
            "mailing_delete",
        ],
        "recipients": [
            "recipients_list",
            "recipient_detail",
            "recipient_create",
            "recipient_update",
            "recipient_delete",
        ],
        "messages": [
            "message_delete",
            "message_update",
            "message_create",
            "message_detail",
            "messages_list",
        ],
        "main_page": ["main_page"],
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu_urls"] = self.menu_urls
        return context


class OwnerOrManagerMixin(LoginRequiredMixin):
    """
    Универсальный миксин доступа:
    - Владелец: полный доступ к своим объектам
    - Менеджер (is_staff): просмотр всех объектов, без редактирования
    - Администратор: полный доступ
    """

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user

        # Суперпользователь и менеджер видят все объекты
        if user.is_superuser or user.is_staff:
            return qs

        # Обычный пользователь — только свои
        return qs.filter(owner=user)

    def dispatch(self, request, *args, **kwargs):
        # Запрет редактирования для менеджера, но только если это НЕ CreateView
        if request.method in ("POST", "PUT", "PATCH", "DELETE") and not isinstance(self, CreateView):
            obj = None
            # Только если у вьюхи есть get_object
            if hasattr(self, "get_object"):
                obj = self.get_object()
            if obj and request.user.is_staff and not request.user.is_superuser:
                raise PermissionDenied("Менеджер не может изменять данные")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Для новых объектов присваиваем владельца
        # if not form.instance.pk:
        #     form.instance.owner = self.request.user

        if hasattr(form, "instance") and not form.instance.pk:
            form.instance.owner = self.request.user
        return super().form_valid(form)
