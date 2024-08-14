from datetime import datetime, timedelta

import pytz
from django.conf import settings
from django.core.mail import send_mail

from services.models import SendMail


def my_job():
    """Рассылка писем"""

    zone = pytz.timezone(settings.TIME_ZONE)  # Получаем текущую временную зону
    current_datetime = datetime.now(zone)  # Получаем текущее время

    start_time = current_datetime - timedelta(minutes=1)  # Время начала рассылки
    end_time = current_datetime + timedelta(minutes=1)  # Время окончания рассылки

    mailings = SendMail.objects.filter(
        is_active=True,
        send_time__range=(start_time, end_time),
        # Получаем все рассылки, которые должны быть отправлены в данный момент
        status="created",
    )

    for mail in mailings:  # Проходимся по всем рассылкам
        if mail.status == "end":  # Если рассылка завершена, то пропускаем
            mail.save()  # Сохраняем рассылку
            continue

        last_send_time = mail.last_send or mail.date_start_send  # Получаем время последней отправки

        if mail.periodicity == "once":  # Если рассылка одноразовая
            if mail.date_end_send and current_datetime > mail.date_end_send:  # Если дата окончания рассылки меньше
                # текущей даты
                mail.status = "end"  # То статус рассылки меняем на "Завершено"
                mail.save()  # Сохраняем рассылку
                continue
            last_send_time = mail.date_start_send  # Время последней отправки равно времени первой отправки

        elif mail.periodicity == "weekly":  # Если рассылка еженедельная
            last_send_time += timedelta(weeks=1)  # Прибавляем к времени последней отправки неделю

        elif mail.periodicity == "monthly":  # Если рассылка ежемесячная
            last_send_time += timedelta(days=30)  # Прибавляем к времени последней отправки 30 дней

        if current_datetime >= last_send_time:  # Если текущее время больше времени последней отправки
            send_mail(  # Отправляем письмо
                subject=mail.subject,  # Тема пис
                message=mail.body,  # Тело письма
                from_email=settings.EMAIL_HOST_USER,  # От кого
                recipient_list=[client.email for client in mail.clients.all()],  # Кому
            )

            mail.last_send = last_send_time  # Время последней отправки равно времени текущей отправки
            mail.date_start_send = last_send_time  # Время первой отправки равно времени последней отправки
            mail.status = "sent"  # Статус рассылки меняем на "Отправлено"
            mail.save()  # Сохраняем рассылку
