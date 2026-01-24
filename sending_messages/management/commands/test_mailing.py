from django.core.management.base import BaseCommand
from django.utils import timezone
from sending_messages.models import Mailing
from sending_messages.services import send_mailing


class Command(BaseCommand):
    help = 'Отправка рассылок, которые в данный момент активны'

    def handle(self, *args, **kwargs):
        now = timezone.localtime(timezone.now())

        self.stdout.write(f"Текущее время: {now}")

        mailings = Mailing.objects.filter(
            start_time__lte=now,
            end_time__gte=now
        )

        if not mailings.exists():
            self.stdout.write("Нет активных рассылок для отправки.")
            return

        for mailing in mailings:
            recipients_count = mailing.recipients.count()
            if recipients_count == 0:
                self.stdout.write(f"Рассылка #{mailing.pk} не имеет получателей.")
                continue

            sent_count = send_mailing(mailing)

            # Обновляем статус рассылки
            mailing.status = mailing.STATUS_RUNNING
            mailing.save(update_fields=['status'])

            self.stdout.write(
                f"Рассылка #{mailing.pk} отправлена {sent_count}/{recipients_count} получателям."
            )
