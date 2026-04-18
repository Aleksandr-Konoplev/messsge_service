from django import forms
from django.utils import timezone

from sending_messages.models import Mailing, Message, Recipient


class RecipientForm(forms.ModelForm):
    """
    Форма для создания и редактирования получателя
    """

    class Meta:
        model = Recipient
        fields = ("email", "full_name", "comment")
        exclude = ("owner",)


class MailingForm(forms.ModelForm):
    """
    Форма для создания и редактирования рассылки
    """

    class Meta:
        model = Mailing
        fields = ("name", "start_time", "end_time", "message", "recipients")
        exclude = ("owner",)

    def __init__(self, *args, **kwargs):
        super(MailingForm, self).__init__(*args, **kwargs)

        self.fields["name"].widget.attrs.update({"class": "form-control", "placeholder": "Введите Имя"})

        self.fields["start_time"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": 'Введите дату начала в формате: "2006-10-25 14:30"',
            }
        )

        self.fields["end_time"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": 'Введите дату окончания в формате: "2006-10-25 14:30"',
            }
        )

        self.fields["message"].widget.attrs.update({"class": "form-control", "placeholder": "Выберите сообщение"})

        self.fields["recipients"].widget.attrs.update({"class": "form-control", "placeholder": "Выберите получателей"})

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        if not start_time or not end_time:
            return cleaned_data

        now = timezone.now()

        if start_time < now:
            self.add_error("start_time", "Дата начала не может быть в прошлом")

        if start_time >= end_time:
            self.add_error("end_time", "Дата окончания должна быть позже даты начала")

        return cleaned_data


class MessageForm(forms.ModelForm):
    """
    Форма для создания и редактирования сообщения
    """

    class Meta:
        model = Message
        fields = ("theme_message", "body_message")
        exclude = ("owner",)
