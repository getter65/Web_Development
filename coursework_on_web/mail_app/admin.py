from django.contrib import admin

from mail_app.models import Client, Message, Mailing, MailingAttempt


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'full_name', 'comments')


@admin.register(Message)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'topic', 'body',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'time', 'frequency', 'status', 'message', 'owner',)


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ('id', 'mailing', 'time', 'status', 'answer',)

