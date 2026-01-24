from django.core.mail import send_mail
import os
from config.settings import EMAIL_HOST_USER

from django.conf import settings


# def send_mailing(mailing):
#     """
#     Отправляет письма всем получателям конкретной рассылки.
#     Принимает модель рассылки
#     """
#
#     theme = mailing.message.theme_message
#     body = mailing.message.body_message
#     recipients = [recipient.email for recipient in mailing.recipients.all()]
#
#     if recipients:
#         send_mail(subject=theme,
#                   message=body,
#                   from_email=EMAIL_HOST_USER,
#                   recipient_list=recipients,
#                   fail_silently=False)
#
#     return len(recipients)
def send_mailing(mailing):
    theme = mailing.message.theme_message
    body = mailing.message.body_message
    recipients = [recipient.email for recipient in mailing.recipients.all()]

    print(f"Отправка '{theme}' на {recipients}")  # <-- DEBUG

    if recipients:
        send_mail(
            subject=theme,
            message=body,
            from_email=EMAIL_HOST_USER,
            recipient_list=recipients,
            fail_silently=False
        )

    return len(recipients)