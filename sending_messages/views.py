from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from sending_messages.models import RecipientMessage
from sending_messages.forms import RecipientMessageForm


def index(request):
    return render(request, 'sending_messages/base.html')


# Просмотр получателей рассылки
class RecipientsMessageListView(ListView):
    model = RecipientMessage
    template_name = 'sending_messages/recipients_list.html'
    context_object_name = 'recipients'


class RecipientMessageDetailView(DetailView):
    model = RecipientMessage
    template_name = 'sending_messages/recipients_detail.html'
    context_object_name = 'recipient'


class RecipientMessageCreateView(CreateView):
    model = RecipientMessage
    form_class = RecipientMessageForm
    template_name = 'sending_messages/form_recipient.html'
    success_url = reverse_lazy('sending_messages:recipient_list')


class RecipientMessageUpdateView(UpdateView):
    pass


class RecipientMessageDeleteView(DeleteView):
    pass
