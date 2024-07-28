from django.db import models

from services.utils import NULLABLE


class Client(models.Model):
    """Модель для хранения данных о клиентах"""

    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    surname = models.CharField(max_length=50, verbose_name="Отчество")
    email = models.EmailField(verbose_name="Почта")
    comment = models.TextField(verbose_name="Комментарий", **NULLABLE)
    is_blocked = models.BooleanField(default=False, verbose_name="Заблокирован")  # Проверка на блокировку

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Message(models.Model):
    """Модель для хранения данных о сообщениях"""

    subject = models.CharField(max_length=150, verbose_name="Тема письма")
    body = models.TextField(verbose_name="Тело письма")

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


class SendMail(models.Model):
    """Модель для хранения данных о письмах"""

    PERIODICITY_CHOICES = (
        ("once", "Один раз в день"),
        ("weekly", "Один раз в неделю"),
        ("monthly", "Один раз в месяц"),
    )

    STATUS_MAIL = (
        ("created", "Создано"),
        ("sent", "Отправлено"),
        ("end", "Завершено"),
    )

    date_start_send = models.DateTimeField(verbose_name="Дата и время первой отправки рассылки")
    periodicity = models.CharField(max_length=10, choices=PERIODICITY_CHOICES, verbose_name="Периодичность рассылки")
    status = models.CharField(max_length=10, choices=STATUS_MAIL, default="created", verbose_name="Статус рассылки")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name="Сообщение")
    clients = models.ManyToManyField(Client, related_name="clients", verbose_name="Клиенты")

    def __str__(self):
        return f"Рассылка: {self.message} - Статус: {self.status}"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        permissions = [  # Права доступа что бы можно было управлять рассылками
            ("disable_sendmail", "Может отключать рассылки"),
            ("block_user", "Может блокировать пользователей"),
        ]


class Logs(models.Model):
    """Модель для хранения логов"""

    date_and_time_last_send = models.DateTimeField(verbose_name="Дата и время последней отправки")
    status_send = models.BooleanField(default=False, verbose_name="Статус отправки")
    server_message = models.TextField(max_length=200, verbose_name="Ответ почтового сервера", **NULLABLE)

    def __str__(self):
        return f"Дата рассылки: {self.date_and_time_last_send} - Статус: {self.status_send}"

    class Meta:
        verbose_name = "Лог"
        verbose_name_plural = "Логи"
