from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from services.models import Logs, Message, SendMail

# def my_job(send_mail_pk):
#     """Рассылка писем"""
#     send_mail_queryset = SendMail.objects.filter(pk=send_mail_pk)  # Получаем объект рассылки
#     if not send_mail_queryset.exists():  # Если объект рассылки не существует
#         raise ValueError("Объект рассылки не существует")  # Вызываем исключение ValueError
#
#     send_mail_object = send_mail_queryset.first()
#     if send_mail_object.is_active:
#         # print("Посылаем почту всем клиентам")
#         send_mail(  # Отправляем письмо
#             subject=send_mail_object.subject,  # Тема письма
#             message=send_mail_object.body,  # Тело письма
#             from_email=settings.EMAIL_HOST_USER,  # От кого
#             recipient_list=[client.email for client in send_mail_object.clients.all()],  # Кому
#     else:

# меняешь статусы и всякое говно


def my_job(send_mail_pk):
    """Рассылка писем"""
    send_mail_queryset = SendMail.objects.filter(pk=send_mail_pk)  # Получаем объект рассылки
    if not send_mail_queryset.exists():  # Если объект рассылки не существует
        raise ValueError("Объект рассылки не существует")  # Вызываем исключение ValueError

    send_mail_object = send_mail_queryset.first()  # Получаем первый объект рассылки
    # message = Message.objects.filter(send_mail=send_mail_object).first()
    # # Получаем первое сообщение, связанное с рассылкой
    #
    # # Извлекаем тему и тело письма из объекта Message
    # subject = message.subject
    # body = message.body

    if send_mail_object.is_active:  # Если рассылка активна
        try:
            recipient_list = [client.email for client in send_mail_object.clients.all()]
            message = Message.objects.filter(send_mail=send_mail_object).first()
            subject = message.subject
            body = message.body
            # Получаем список email адресов всех клиентов, связанных с рассылкой
            response = send_mail(  # Отправляем письмо
                subject=subject,  # Тема письма
                # subject=send_mail_object.subject,  # Тема письма
                message=body,  # Тело письма
                # message=send_mail_object.body,  # Тело письма
                from_email=settings.EMAIL_HOST_USER,  # От кого
                recipient_list=recipient_list,  # Кому
            )

            Logs.objects.create(  # Создаем лог
                date_and_time_last_send=timezone.now(),
                status_send=True,
                server_message=response,
                send_mail=send_mail_object,
            )

            send_mail_object.status = "sent"  # Меняем статус рассылки на "Отправлено"

            if timezone.now() > send_mail_object.date_end_send:
                # Если текущее время больше времени окончания рассылки
                send_mail_object.status = "end"  # То меняем статус рассылки на "Завершено"
                send_mail_object.is_active = False  # И делаем рассылку неактивной

            send_mail_object.save()  # Сохраняем объект рассылки

        except Exception as e:  # Если произошла ошибка
            Logs.objects.create(  # Создаем лог
                date_and_time_last_send=timezone.now(),
                status_send=False,
                server_message=str(e),
                send_mail=send_mail_object,
            )

            send_mail_object.status = "error"
            send_mail_object.save()
