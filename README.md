# Message Service

**Message Service** — это простое Django-приложение для управления почтовыми рассылками. Оно позволяет создавать рассылки, добавлять сообщения и получателей, а также управлять отправкой писем.  

---

## Технологии
* python = 3.13
* flake8 = 7.3.0
* black = 26.1.0
* mypy = 1.19.1
* isort = 7.0.0
* django = 6.0.1
* psycopg2 = 2.9.11
* dotenv = 0.9.9
* ipython = 9.9.0
* django-stubs = 5.2.9
* redis = 7.1.0

---

## Установка
1. Установите зависимости через Poetry:
    ```
    poetry install
    ```
2. Примените миграции:
    ```
    python manage.py migrate
    ```
3. Создайте суперпользователя (есть кастомная команда):
    ```
    python manage.py custom_createsuperuser
    ```
4. Запустите сервер:
    ```
    python manage.py runserver
    ```

---


## Настройки

* Все необходимые настройки вынесены в файл ".example.env", необходимо переименовать в ".env" и указать настройки
    ```
    # Ключ Django
    SECRET_KEY=Вставить ключ django
    
    # Режим разработки
    DEBUG=True
    
    # Настройки базы данных
    NAME=messsge_service
    USER=postgres
    PASSWORD=1234
    HOST=localhost
    PORT=5432
    
    # Настройки почтового клиента
    EMAIL_HOST = 'smtp.yandex.ru'
    EMAIL_PORT = 465
    EMAIL_USE_TLS = False
    EMAIL_USE_SSL = True
    EMAIL_HOST_USER = 'your_mail@yandex.ru'
    EMAIL_HOST_PASSWORD = 'your_passwird'
    ```
* Отправка писем настраивается через стандартные Django-параметры `EMAIL_BACKEND`, `EMAIL_HOST`, `EMAIL_PORT` и т.д.
* Загрузка файлов и медиа хранится в папке media/.
* Статические файлы – в static/.
* Создайте файл .env и добавьте настройки:
    ```
    DEBUG=True
    SECRET_KEY=ваш_секретный_ключ
    ALLOWED_HOSTS=localhost,127.0.0.1
    EMAIL_HOST=smtp.example.com
    EMAIL_PORT=587
    EMAIL_HOST_USER=your_email@example.com
    EMAIL_HOST_PASSWORD=your_password
    ```

---

## Использование
* Главная страница: отображает текущие рассылки и их статусы.
* Рассылки: можно создавать, редактировать и удалять.
* Сообщения: добавляются в конкретную рассылку.
* Получатели: создаются и редактируются для каждой рассылки.

---

## Полезные команды
* Применить миграции: python manage.py migrate 
* Создать суперпользователя: python manage.py custom_createsuperuser
* Запустить сервер разработки: python manage.py runserver
---

## Структура проекта
```
message_service/
├── config/                 # Основные настройки Django проекта
├── sending_messages/       # Основное приложение для рассылок
├── users/                  # Приложение для управления пользователями
├── media/                  # Загружаемые файлы
├── static/                 # Статические файлы
├── templates/              # Глобальные шаблоны
├── manage.py               # Основной скрипт управления проектом
├── db.sqlite3              # Локальная база данных SQLite
├── .env                    # Переменные окружения
├── pyproject.toml          # Настройки Poetry
└── poetry.lock             # Фиксированные зависимости
```

### Основные приложения

- **sending_messages** – управление рассылками, сообщениями и получателями.  
- **users** – кастомная модель пользователей с подтверждением email и токенами.  

---

### Шаблоны. 

Общие шаблоны `templates/`:

1. `includes/inc_menu.html` - шаблон меню (навбара) 
2. `base.html` - базовый шаблон для вставки

Шаблоны используемые в проекте для взаимодействия с моделями приложений:

1. Приложение "sending_messages" `sending_messages/templates/`:
   1. Mailing - Модель рассылок:
      * `mailings_list.html` – список всех рассылок с названием, статусом и действиями
      * `mailing_detail.html` – детали рассылки: имя, статус, время старта, сообщение и получатели
      * `form_mailing.html` – форма создания/редактирования рассылки с основными полями
      * `mailing_confirm_delete.html` – подтверждение удаления рассылки

   2. Message - Модель сообщения:
      * `messages_list.html` – список сообщений с текстом, статусом и датой отправки
      * `message_detail.html` – детали сообщения: текст, дата, статус и связанная рассылка
      * `form_message.html` – форма создания/редактирования сообщения
      * `message_confirm_delete.html` – подтверждение удаления сообщения

   3. Recipient - Модель получателя рассылки:
      * `recipients_list.html` – список получателей с email, именем и действиями
      * `recipient_detail.html` – детали получателя: информация о подписке и истории сообщений
      * `form_recipient.html` – форма создания/редактирования получателя
      * `recipient_confirm_delete.html` – подтверждение удаления получателя
2. Приложение "users" `users/templates/`s:
   1. User - Модель пользователя:
      * `login.html` - форма входа на сайт
      * `user_form.html` - форма регистрации пользователя

---

## Функционал

- Регистрация и управление пользователями.
- Создание, редактирование и удаление рассылок.
- Добавление сообщений к рассылкам.
- Управление списками получателей.
- Привязка рассылок к конкретным пользователям (owner).  
- Простая и удобная админ-панель для управления всем процессом.



---
---
---
---
```commandline
message_service/                         # Корневая папка проекта
│
├── .venv/                               # Виртуальное окружение Python
├── config/                              # Основные настройки Django проекта
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py                          # Главный URL-конфиг проекта
│   └── wsgi.py
│
├── sending_messages/                    # Приложение для отправки сообщений
│   ├── management/
│   │   └── commands/                    # Кастомные команды management
│   │       └── test_mailing.py
│   ├── migrations/                      # Миграции базы данных
│   ├── templates/                       # Шаблоны приложения
│   │   └── sending_messages/
│   │       ├── form_mailing.html
│   │       ├── form_message.html
│   │       ├── form_recipient.html
│   │       ├── mailing_confirm_delete.html
│   │       ├── mailing_detail.html
│   │       ├── mailings_list.html
│   │       ├── main_page.html
│   │       ├── message_confirm_delete.html
│   │       ├── message_detail.html
│   │       ├── messages_list.html
│   │       ├── recipient_confirm_delete.html
│   │       ├── recipient_detail.html
│   │       ├── recipients_list.html
│   │       └── template.html
│   │
│   ├── __init__.py
│   ├── admin.py                         # Админ-панель
│   ├── apps.py                          # Конфигурация приложения
│   ├── forms.py                         # Формы
│   ├── mixins.py                        # Миксины для представлений
│   ├── models.py                        # Модели данных
│   ├── services.py                      # Бизнес-логика
│   ├── tests.py                         # Тесты
│   ├── urls.py                          # URL-маршруты приложения
│   └── views.py                         # Представления
│
├── users/                               # Приложение пользователей
│   ├── management/
│   │   └── commands/
│   │       └── custom_createsuperuser.py # Кастомная команда создания суперпользователя
│   ├── migrations/
│   ├── templates/
│   │   └── users/
│   │       ├── login.html
│   │       ├── password_reset_complete.html
│   │       ├── password_reset_confirm.html
│   │       ├── password_reset_done.html
│   │       ├── password_reset_email.html
│   │       ├── password_reset_form.html
│   │       ├── profile.html
│   │       └── user_form.html
│   │
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── templates/                           # Общие шаблоны проекта
│   ├── includes/
│   │   └── inc_menu.html                # Включение меню
│   └── base.html                        # Базовый шаблон
│
├── static/                              # Статические файлы
│   ├── css/
│   └── js/
│
├── draft/                               # Черновики или временные файлы
├── media/                               # Загружаемые пользователем файлы
│
├── .env                                 # Переменные окружения
├── .fake18                              # Файл для поддельных данных (возможно для тестов)
├── .gitignore                           # Игнорируемые Git файлы
├── __init__.py
└── manage.py                            # Основной скрипт управления Django
```