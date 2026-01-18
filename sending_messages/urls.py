from sending_messages.apps import SendingMessagesConfig
from django.urls import path

from sending_messages.views import index

app_name = SendingMessagesConfig.name

urlpatterns = [
    path('', index)
]