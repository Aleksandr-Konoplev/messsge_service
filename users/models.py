from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True,
        verbose_name="Email"
    )

    is_email_verified = models.BooleanField(
        default=False,
        verbose_name="Email подтверждён"
    )

    token = models.CharField(
        max_length=100, verbose_name="Token", blank=True, null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        status = 'Подтвержден' if self.is_email_verified else 'Не подтвержден'
        return f'{self.email} - {status}'
