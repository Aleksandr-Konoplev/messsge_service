from django import forms
from sending_messages.models import RecipientMessage


class RecipientMessageForm(forms.ModelForm):
    """
    Форма для создания и редактирования получателя
    """
    class Meta:
        model = RecipientMessage
        fields = ('email', 'full_name', 'comment')