from distutils.log import Log

from django.contrib import admin

from services.models import Client, SendMail, Message


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "surname", "email", "comment", "is_blocked")
    search_fields = ("first_name", "last_name", "surname", "email", "is_blocked")
    list_filter = ("first_name", "last_name", "surname", "email", "comment", "is_blocked")
    ordering = ('last_name',)  # Сортировка по фамилии
    list_editable = ('is_blocked',)  # Редактирование статуса блокировки клиента прямо там
    readonly_fields = ('email',)  # Поле только для чтения, нельзя менять email
    list_per_page = 20
    search_help_text = "Лучше искать клиента  фамилии или email клиента"


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "body")
    search_fields = ("subject",)
    list_filter = ("subject",)


@admin.register(SendMail)
class SendMailAdmin(admin.ModelAdmin):
    list_display = ("date_start_send", "periodicity", "status", "message", "clients")
    search_fields = ("date_start_send", "periodicity", "status", "message", "clients")
    list_filter = ("date_start_send", "periodicity", "status", "message", "clients")
    readonly_fields = ('date_start_send',)  # Поле только для чтения, нельзя менять дату отправки
    ordering = ('date_start_send',)
    list_per_page = 30
    list_editable = ('status',)  # Редактирование статуса рассылки, только нафига это надо?
    search_help_text = "Лучше искать рассылку по дате и клиенту"
    fieldsets = (
        (None, {
            'fields': ('date_start_send', 'periodicity', 'status')
        }),
        ('Message & Clients', {
            'fields': ('message', 'clients'),
        }),
    )  # Группировка полей в админке, не знаю что  это, но вот и посмотрю


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ("date_and_time_last_send", "status_send", "server_message")
    search_fields = ("date_and_time_last_send", "status_send", "server_message")
    list_filter = ("date_and_time_last_send", "status_send", "server_message")
