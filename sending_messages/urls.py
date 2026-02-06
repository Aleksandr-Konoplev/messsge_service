from django.urls import path

from sending_messages.apps import SendingMessagesConfig
from sending_messages.views import (
    MailingCreateView,
    MailingDeleteView,
    MailingDetailView,
    MailingSendView,
    MailingsListView,
    MailingUpdateView,
    MainPageTemplateView,
    MessageCreateView,
    MessageDeleteView,
    MessageDetailView,
    MessageListView,
    MessageUpdateView,
    RecipientCreateView,
    RecipientDeleteView,
    RecipientDetailView,
    RecipientsListView,
    RecipientUpdateView,
    index,
)

app_name = SendingMessagesConfig.name

urlpatterns = [
    path("index/", index),
    # Главная
    path("", MainPageTemplateView.as_view(), name="main_page"),
    # Получатели
    path("recipients_list/", RecipientsListView.as_view(), name="recipients_list"),
    path(
        "recipient_detail/<int:pk>/",
        RecipientDetailView.as_view(),
        name="recipient_detail",
    ),
    path("recipient_create/", RecipientCreateView.as_view(), name="recipient_create"),
    path(
        "recipient_update/<int:pk>/",
        RecipientUpdateView.as_view(),
        name="recipient_update",
    ),
    path(
        "recipient_delete/<int:pk>/",
        RecipientDeleteView.as_view(),
        name="recipient_delete",
    ),
    # Сообщения
    path("messages_list/", MessageListView.as_view(), name="messages_list"),
    path("message_detail/<int:pk>/", MessageDetailView.as_view(), name="message_detail"),
    path("message_create/", MessageCreateView.as_view(), name="message_create"),
    path("message_update/<int:pk>", MessageUpdateView.as_view(), name="message_update"),
    path("message_delete/<int:pk>/", MessageDeleteView.as_view(), name="message_delete"),
    # Рассылки
    path("mailings_list/", MailingsListView.as_view(), name="mailings_list"),
    path("mailing_detail/<int:pk>/", MailingDetailView.as_view(), name="mailing_detail"),
    path("mailing_create/", MailingCreateView.as_view(), name="mailing_create"),
    path("mailing_update/<int:pk>/", MailingUpdateView.as_view(), name="mailing_update"),
    path("mailing_delete/<int:pk>/", MailingDeleteView.as_view(), name="mailing_delete"),
    # Иные действия
    path("mailing_send/<int:pk>/", MailingSendView.as_view(), name="mailing_send"),
]
