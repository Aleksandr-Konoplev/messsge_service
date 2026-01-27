from django import forms
from sending_messages.models import Recipient, Mailing, Message


class RecipientForm(forms.ModelForm):
    """
    Форма для создания и редактирования получателя
    """
    class Meta:
        model = Recipient
        fields = ('email', 'full_name', 'comment')


class MailingForm(forms.ModelForm):
    """
    Форма для создания и редактирования рассылки
    """
    start_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control'
        }),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    end_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control'
        }),
        input_formats=['%Y-%m-%dT%H:%M']
    )

    class Meta:
        model = Mailing
        fields = ('name', 'start_time', 'end_time', 'message', 'recipients')


class MessageForm(forms.ModelForm):
    """
    Форма для создания и редактирования сообщения
    """
    class Meta:
        model = Message
        fields = ('theme_message', 'body_message')
