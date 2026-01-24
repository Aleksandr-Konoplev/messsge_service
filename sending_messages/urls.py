from django.urls import path

from sending_messages.apps import SendingMessagesConfig
from sending_messages.views import index, RecipientsMessageListView, RecipientMessageDetailView


app_name = SendingMessagesConfig.name

urlpatterns = [
    path('', index),
    path('recipients_list', RecipientsMessageListView.as_view(), name='recipients_list'),
    path('recipient_detail/<int:pk>', RecipientMessageDetailView.as_view(), name='recipient_detail'),
]