from django.conf import settings
from django.core.mail import EmailMessage, get_connection

from sending_messages.models import Mailing, MailingAttempt


def send_mailing(mailing):
    """
    Отправляет письма всем получателям конкретной рассылки
    и сохраняет SMTP-ответ почтового сервера.
    """

    theme = mailing.message.theme_message
    body = mailing.message.body_message
    recipients = mailing.recipients.all()

    if not recipients.exists():
        mailing.status = Mailing.STATUS_FINISHED
        mailing.save(update_fields=["status"])
        return 0

    # Переводим рассылку в статус "Запущена"
    mailing.status = Mailing.STATUS_RUNNING
    mailing.save(update_fields=["status"])

    sent_count = 0

    # Получаем email backend (SMTP)
    connection = get_connection()

    try:
        # Открываем SMTP-соединение на всю рассылку
        connection.open()

        for recipient in recipients:
            try:
                email = EmailMessage(
                    subject=theme,
                    body=body,
                    from_email=settings.EMAIL_HOST_USER,
                    to=[recipient.email],
                    connection=connection,
                )

                # Отправляем письмо
                # send() вернёт 1, если Django считает отправку успешной
                email.send(fail_silently=False)

                # Получаем SMTP-объект
                smtp = connection.connection

                # Достаём из NOOP код и текст ответа
                smtp_code, smtp_message = smtp.noop()

                MailingAttempt.objects.create(
                    mailing=mailing,
                    recipient=recipient,
                    status=MailingAttempt.STATUS_SUCCESS,
                    server_response=f"{smtp_code} - {smtp_message.decode()}",
                )

                sent_count += 1

            except Exception as err:
                # Если сервер отказал или возникла ошибка
                MailingAttempt.objects.create(
                    mailing=mailing,
                    recipient=recipient,
                    status=MailingAttempt.STATUS_FAILED,
                    error_message=str(err),
                )

    except Exception as err:
        raise Exception(f"Не удалось установить соединение - {err}")

    finally:
        # Закрываем SMTP-соединение
        connection.close()

    # Отмечаем рассылку как завершённую
    mailing.status = Mailing.STATUS_FINISHED
    mailing.save(update_fields=["status"])

    return sent_count
