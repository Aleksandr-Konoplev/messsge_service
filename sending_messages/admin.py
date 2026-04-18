from django.contrib import admin

from sending_messages.models import Mailing, MailingAttempt, Message, Recipient


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "full_name",
    )
    list_filter = ("email",)
    search_fields = ("email",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("theme_message",)
    list_filter = ("theme_message",)
    search_fields = ("theme_message",)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "status",
    )
    list_filter = ("message__theme_message",)
    search_fields = ("message__theme_message",)


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ("mailing__name", "recipient__email", "server_response")
    list_filter = ("server_response",)
    search_fields = ("mailing",)
