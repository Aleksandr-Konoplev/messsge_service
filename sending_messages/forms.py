from django import forms
from django.utils import timezone
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

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if not start_time or not end_time:
            return cleaned_data

        now = timezone.now()

        if start_time < now:
            self.add_error('start_time', 'Дата начала не может быть в прошлом')

        if start_time >= end_time:
            self.add_error('end_time', 'Дата окончания должна быть позже даты начала')

        return cleaned_data


class MessageForm(forms.ModelForm):
    """
    Форма для создания и редактирования сообщения
    """
    class Meta:
        model = Message
        fields = ('theme_message', 'body_message')
