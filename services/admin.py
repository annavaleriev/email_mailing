from distutils.log import Log

from django.contrib import admin

from services.models import Client, Logs, Message, SendMail


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "surname", "email", "comment")
    search_fields = ("first_name", "last_name", "surname", "email")
    list_filter = ("first_name", "last_name", "surname", "email", "comment")
    ordering = ("last_name",)  # Сортировка по фамилии
    # list_editable = ("is_blocked",)  # Редактирование статуса блокировки клиента прямо там
    # readonly_fields = ("email",)  # Поле только для чтения, нельзя менять email
    list_per_page = 20
    search_help_text = "Лучше искать клиента  фамилии или email клиента"


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "body")
    search_fields = ("subject",)
    list_filter = ("subject",)


@admin.register(SendMail)
class SendMailAdmin(admin.ModelAdmin):
    list_display = ("date_start_send", "periodicity", "status", "message", "get_clients", "is_active")
    search_fields = ("date_start_send", "periodicity", "status", "message")
    list_filter = ("is_active", "date_start_send", "periodicity", "status", "message")
    readonly_fields = ("status",)  # Поле только для чтения, нельзя менять дату отправки
    ordering = ("is_active", "date_start_send",)
    list_per_page = 30
    # list_editable = ("status",)  # Редактирование статуса рассылки, только нафига это надо?
    search_help_text = "Лучше искать рассылку по дате и клиенту"
    fieldsets = (
        (None, {"fields": ("is_active", "date_start_send", "periodicity", "status")}),
        (
            "Message & Clients",
            {
                "fields": ("message", "clients"),
            },
        ),
    )  # Группировка полей в админке, не знаю что это, но вот и посмотрю
    filter_horizontal = ("clients", )

    def get_clients(self, obj):  # Это метод для вывода всех клиентов в рассылке
        return ", ".join([client.email for client in obj.clients.all()])  # Вывод всех клиентов в рассылке

    get_clients.short_description = "Клиенты"  # Название колонки в админке


@admin.register(Logs)
class LogAdmin(admin.ModelAdmin):
    list_display = ("date_and_time_last_send", "status_send", "server_message")
    search_fields = ("date_and_time_last_send", "status_send", "server_message")
    list_filter = ("date_and_time_last_send", "status_send", "server_message")
