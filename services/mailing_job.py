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
                send_mail=send_mail_object
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
                send_mail=send_mail_object
            )

            send_mail_object.status = "error"
            send_mail_object.save()



# def my_job(send_mail_id):
#     try:
#         # Получаем объект SendMail по его идентификатору
#         send_mail_object = SendMail.objects.get(pk=send_mail_id)
#
#         # Получаем первое сообщение, связанное с данной рассылкой
#         message = Message.objects.filter(send_mail=send_mail_object).first()
#
#         # Проверяем, было ли найдено сообщение
#         if not message:
#             raise ValueError("Сообщение для данной рассылки не найдено")
#
#         # Извлекаем тему и тело письма из объекта Message
#         subject = message.subject
#         body = message.body
#
#         # Получаем список email адресов всех клиентов, связанных с рассылкой
#         recipient_list = [client.email for client in send_mail_object.clients.all()]
#
#         if recipient_list:  # Проверяем, что список получателей не пуст
#             # Отправляем письмо с использованием функции send_mail
#             send_mail(
#                 subject=subject,
#                 message=body,
#                 from_email=settings.DEFAULT_FROM_EMAIL,
#                 recipient_list=recipient_list,
#                 fail_silently=False,
#             )
#
#             # Обновляем статус рассылки, если письмо успешно отправлено
#             send_mail_object.status = 'sent'
#             send_mail_object.save()
#         else:
#             raise ValueError("Нет клиентов для отправки письма.")
#
#     except SendMail.DoesNotExist:
#         # Обработка ситуации, когда объект SendMail не найден
#         print(f"Рассылка с ID {send_mail_id} не найдена.")
#
#     except ValueError as e:
#         # Обработка ситуации, когда не найдено сообщение или клиенты
#         Logs.objects.create(
#             send_mail=send_mail_object,
#             error_message=str(e)
#         )
#
#     except Exception as e:
#         # Обработка любых других ошибок
#         Logs.objects.create(
#             send_mail=send_mail_object,
#             error_message=str(e)
#         )

# zone = pytz.timezone(settings.TIME_ZONE)  # Получаем текущую временную зону
# current_datetime = datetime.now(zone)  # Получаем текущее время
#
# start_time = current_datetime - timedelta(minutes=1)  # Время начала рассылки
# end_time = current_datetime + timedelta(minutes=1)  # Время окончания рассылки
#
# mailings = SendMail.objects.filter(
#     is_active=True,
#     send_time__range=(start_time, end_time),
#     # Получаем все рассылки, которые должны быть отправлены в данный момент
#     status="created",
# )
#
# for mail in mailings:  # Проходимся по всем рассылкам
#     if mail.status == "end":  # Если рассылка завершена, то пропускаем
#         mail.save()  # Сохраняем рассылку
#         continue
#
#     last_send_time = mail.last_send or mail.date_start_send  # Получаем время последней отправки
#
#     if mail.periodicity == "once":  # Если рассылка одноразовая
#         if mail.date_end_send and current_datetime > mail.date_end_send:  # Если дата окончания рассылки меньше
#             # текущей даты
#             mail.status = "end"  # То статус рассылки меняем на "Завершено"
#             mail.save()  # Сохраняем рассылку
#             continue
#         last_send_time = mail.date_start_send  # Время последней отправки равно времени первой отправки
#
#     elif mail.periodicity == "weekly":  # Если рассылка еженедельная
#         last_send_time += timedelta(weeks=1)  # Прибавляем к времени последней отправки неделю
#
#     elif mail.periodicity == "monthly":  # Если рассылка ежемесячная
#         last_send_time += timedelta(days=30)  # Прибавляем к времени последней отправки 30 дней
#
#     if current_datetime >= last_send_time:  # Если текущее время больше времени последней отправки
#         send_mail(  # Отправляем письмо
#             subject=mail.subject,  # Тема пис
#             message=mail.body,  # Тело письма
#             from_email=settings.EMAIL_HOST_USER,  # От кого
#             recipient_list=[client.email for client in mail.clients.all()],  # Кому
#         )
#
#         mail.last_send = last_send_time  # Время последней отправки равно времени текущей отправки
#         mail.date_start_send = last_send_time  # Время первой отправки равно времени последней отправки
#         mail.status = "sent"  # Статус рассылки меняем на "Отправлено"
#         mail.save()  # Сохраняем рассылку
