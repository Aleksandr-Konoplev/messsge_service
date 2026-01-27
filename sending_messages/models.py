from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Manager
from django.utils import timezone


class Recipient(models.Model):
    """
    Модель получателя рассылки (клиента).
    """
    email = models.EmailField(unique=True, verbose_name='Email')
    full_name = models.CharField(max_length=255, verbose_name='Полное имя')
    comment = models.TextField(verbose_name='Комментарий', blank=True, null=True)

    # Объявление для линтера
    object: Manager['Recipient']
    objects: Manager['Recipient']

    def __str__(self):
        return f'{self.full_name} {self.email}'

    class Meta:
        verbose_name = 'Получатель'
        verbose_name_plural = 'Получатели'


class Message(models.Model):
    """
    Модель сообщения
    """
    theme_message = models.CharField(verbose_name='Тема письма', max_length=255)
    body_message = models.TextField(verbose_name='Сообщение')

    # Объявление для линтера
    object: Manager['Message']
    objects: Manager['Message']

    def __str__(self):
        return self.theme_message

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Mailing(models.Model):
    """
    Модель рассылки
    """
    STATUS_CREATED = "created"
    STATUS_RUNNING = "running"
    STATUS_FINISHED = "finished"

    STATUS_CHOICES = (
        (STATUS_CREATED, "Создана"),
        (STATUS_RUNNING, "Запущена"),
        (STATUS_FINISHED, "Завершена"),
    )

    name = models.CharField(verbose_name='Название рассылки', max_length=50)
    start_time = models.DateTimeField(verbose_name='Дата и время начала отправки')
    end_time = models.DateTimeField(verbose_name='Дата и время окончания отправки')
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=STATUS_CREATED,
        verbose_name="Статус рассылки"
    )
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщение')
    recipients = models.ManyToManyField(Recipient, verbose_name='Получатели')

    # Объявление для линтера
    object: Manager['Mailing']
    objects: Manager['Mailing']

    from django.core.exceptions import ValidationError
    from django.utils import timezone

    def clean(self):
        super().clean()

        # если одно из полей не заполнено — выходим
        if not self.start_time or not self.end_time:
            return

        # now = timezone.now()
        # if self.start_time < now:
        #     raise ValidationError({'start_time': 'Дата начала не может быть в прошлом'})

        if self.start_time >= self.end_time:
            raise ValidationError({
                'end_time': 'Дата окончания должна быть позже даты начала'
            })

    def update_status(self):
        now = timezone.now()
        previous_status = self.status

        if now < self.start_time:
            self.status = self.STATUS_CREATED
        elif self.start_time <= now <= self.end_time:
            self.status = self.STATUS_RUNNING
        else:
            self.status = self.STATUS_FINISHED

        if self.status != previous_status:
            self.save(update_fields=['status'])

    def save(self, *args, **kwargs):
        self.full_clean()
        self.update_status()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Рассылка №{self.pk}: {self.message} ({self.status})'

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
