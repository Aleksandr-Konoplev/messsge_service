from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER
from sending_messages.models import MailingAttempt, Mailing


def send_mailing(mailing):
    """
    Отправляет письма всем получателям конкретной рассылки.
    """
    theme = mailing.message.theme_message
    body = mailing.message.body_message
    recipients = mailing.recipients.all()
    sent_count = 0

    if not recipients:
        return 'Нет получателей в рассылке'

    # Ставим статус "Запущена" до отправки
    mailing.status = Mailing.STATUS_RUNNING
    mailing.save(update_fields=['status'])

    for recipient in recipients:
        try:
            send_mail(
                subject=theme,
                message=body,
                from_email=EMAIL_HOST_USER,
                recipient_list=[recipient.email],
                fail_silently=False
            )

            MailingAttempt.objects.create(
                mailing=mailing,
                recipient=recipient,
                status=MailingAttempt.STATUS_SUCCESS
            )

            sent_count += 1

        except Exception as err:
            MailingAttempt.objects.create(
                mailing=mailing,
                recipient=recipient,
                status=MailingAttempt.STATUS_FAILED,
                error_message=str(err)
            )

    # Отмечаем рассылку как отправленную
    mailing.status = Mailing.STATUS_FINISHED
    mailing.save(update_fields=['status'])

    return sent_count
