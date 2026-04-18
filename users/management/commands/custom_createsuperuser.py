from getpass import getpass

from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = "Создаёт суперпользователя с email super-us@mail.ru"

    def handle(self, *args, **options):
        email = "super-us@mail.ru"
        self.stdout.write(f"Создание суперпользователя с email {email}")

        # Проверяем, если пользователь существует - удаляем его
        User.objects.filter(email=email).delete()

        # Запрашиваем пароль
        while True:
            password = getpass("Пароль: ")
            password2 = getpass("Пароль (ещё раз): ")
            if password != password2:
                self.stdout.write("Пароли не совпадают. Попробуйте снова.")
                continue
            break

        # Создаём суперпользователя
        user = User.objects.create(email=email, is_active=True, is_staff=True, is_superuser=True)
        user.set_password(password)
        user.save()

        self.stdout.write(self.style.SUCCESS(f"Суперпользователь {email} успешно создан!"))
