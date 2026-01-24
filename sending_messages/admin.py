from django.contrib import admin
from sending_messages.models import RecipientMessage, Message, Mailing


@admin.register(RecipientMessage)
class RecipientMessageAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name',)
    list_filter = ('email',)
    search_fields = ('email',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('theme_message',)
    list_filter = ('theme_message',)
    search_fields = ('theme_message',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('status', 'id')
    list_filter = ('message__theme_message',)
    search_fields = ('message__theme_message',)
