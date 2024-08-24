from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import HiddenInput
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from pytz import timezone

from services.forms import AddClientForm, SendMailForm
from services.mailing_job import my_job
from services.mixins import CreateViewMixin, OwnerQuerysetViewMixin, SendMailFormsetMixin, StatisticMixin
from services.models import Client, Logs, SendMail

DATABASE = settings.DATABASES["default"]  # Получение настроек базы данных

job_stores = {  # Создание хранилища задач
    "default": SQLAlchemyJobStore(  # Использование SQLAlchemyJobStore
        url=f'postgresql://{DATABASE["USER"]}:{DATABASE["PASSWORD"]}'  # Подключение к базе данных
        f'@{DATABASE["HOST"]}:{DATABASE["PORT"]}/{DATABASE["NAME"]}'  # Подключение к базе данных
    )
}

scheduler = BackgroundScheduler(jobstores=job_stores, timezone=timezone(settings.TIME_ZONE))
# Создание планировщика
scheduler.start()  # Запуск планировщика


class ClientListView(LoginRequiredMixin, OwnerQuerysetViewMixin, StatisticMixin, ListView):
    """Список клиентов"""

    model = Client
    template_name = "services/client_list.html"
    extra_context = {"title": "Список клиентов"}  # Добавление дополнительного контекста на страницу


class ClientDetailView(LoginRequiredMixin, OwnerQuerysetViewMixin, StatisticMixin, DetailView):
    model = Client
    template_name = "services/client_detail.html"
    extra_context = {"title": "Информация о клиенте"}


class ClientCreateView(LoginRequiredMixin, CreateViewMixin, StatisticMixin, CreateView):
    """Добавление клиента"""

    model = Client
    template_name = "services/client_update.html"
    form_class = AddClientForm
    success_url = reverse_lazy("services:client_list")


class ClientUpdateView(LoginRequiredMixin, OwnerQuerysetViewMixin, StatisticMixin, UpdateView):
    """Редактирование клиента"""

    model = Client
    template_name = "services/client_update.html"
    form_class = AddClientForm
    context_object_name = "client"  # Переопределение имени объекта в контексте

    def get_success_url(self):  # Переопределение метода get_success_url
        return reverse_lazy(
            "services:client_detail", kwargs={"pk": self.object.pk}
        )  # Возврат ссылки на страницу детальной информации о клиенте


class ClientDeleteView(LoginRequiredMixin, OwnerQuerysetViewMixin, StatisticMixin, DeleteView):
    """Удаление клиента"""

    model = Client
    template_name = "services/client_delete.html"
    context_object_name = "client"
    success_url = reverse_lazy("services:client_list")


class SendMailListView(LoginRequiredMixin, OwnerQuerysetViewMixin, StatisticMixin, ListView):
    """Список рассылок"""

    model = SendMail
    template_name = "services/sendmail_list.html"
    form_class = SendMailForm
    extra_context = {"title": "Список рассылок"}


class SendMailDetailView(LoginRequiredMixin, OwnerQuerysetViewMixin, StatisticMixin, DetailView):
    """Информация о рассылке"""

    model = SendMail
    template_name = "services/sendmail_detail.html"
    context_object_name = "sendmail"
    extra_context = {"title": "Информация о рассылке"}


class SendMailCreateView(LoginRequiredMixin, CreateViewMixin, SendMailFormsetMixin, StatisticMixin, CreateView):
    """Добавление рассылки"""

    success_url = reverse_lazy("services:home")

    def post(self, request, *args, **kwargs):  # Переопределение метода post
        send_mail = super().post(request, *args, **kwargs)  # Вызов родительского метода post
        expr = f"{self.object.date_start_send.minute} {self.object.date_start_send.hour} {self.object.periodicity}"
        # Формирование строки для периодичности
        cron_trigger = CronTrigger.from_crontab(expr=expr)  # Создание триггера
        cron_trigger.start_date = self.object.date_start_send  # Установка времени начала
        cron_trigger.end_date = self.object.date_end_send  # Установка времени окончания

        scheduler.add_job(  # Добавление задачи
            my_job,  # Функция, которую нужно выполнить
            trigger=cron_trigger,  # Триггер
            args=[self.object.pk],  # Аргументы
            id=str(self.object.pk),  # Идентификатор задачи
        )
        return send_mail  # Возврат результата

    def get_form(self, *args, **kwargs):  # Переопределение метода get_form
        form = super().get_form(*args, **kwargs)  # Вызов родительского метода get_form
        form.fields["clients"].queryset = Client.objects.filter(owner=self.request.user)  # Фильтрация клиентов
        return form  # Возврат формы


class SendMailUpdateView(LoginRequiredMixin, OwnerQuerysetViewMixin, SendMailFormsetMixin, StatisticMixin, UpdateView):
    """Редактирование рассылки"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = context["form"]
        formset = context["formset"].form

        if not (
            self.request.user.is_superuser or self.request.user.can_disable_sendmail
        ):  # прописать условия для супер и менеджера
            form.base_fields["is_active"].widget = HiddenInput()

        if self.request.user.can_disable_sendmail:
            for name, field in form.base_fields.items():
                if name != "is_active":
                    field.disabled = True

            for name, field in formset.base_fields.items():
                field.disabled = True
        return context

    def get_success_url(self):
        return reverse_lazy("services:sendmail_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):  # Переопределение метода form_valid
        context_data = self.get_context_data()  # Получение контекста
        formset = context_data["formset"]  # Получение формсета
        if formset.is_valid() and form.is_valid():  # Если форма и формсет валидны
            form.save()  # Сохранение формы
            formset.save()  # Сохранение формсета
            return super().form_valid(form)  # Вызов родительского метода form_valid
        else:
            return self.render_to_response(self.get_context_data(form=form))  # Возврат страницы с формой и формсетом

    def post(self, request, *args, **kwargs):
        send_mail = super().post(request, *args, **kwargs)
        expr = f"{self.object.date_start_send.minute} {self.object.date_start_send.hour} {self.object.periodicity}"

        cron_trigger = CronTrigger.from_crontab(expr=expr)
        cron_trigger.start_date = self.object.date_start_send
        cron_trigger.end_date = self.object.date_end_send

        scheduler.reschedule_job(str(self.object.pk), trigger=cron_trigger)
        return send_mail


class SendMailDeleteView(LoginRequiredMixin, OwnerQuerysetViewMixin, StatisticMixin, DeleteView):
    """Удаление рассылки"""

    model = SendMail
    template_name = "services/sendmail_delete.html"
    success_url = reverse_lazy("services:home")

    def post(self, request, *args, **kwargs):  # Переопределение метода post
        send_mail = self.get_object()  # Получение объекта рассылки

        try:
            job_id = str(send_mail.pk)  # Получение идентификатора задачи
            scheduler.remove_job(job_id)  # Удаление задачи
        except Exception as e:  # Обработка исключения
            print(f"Не удалось удалить задачу: {e}")

        return super().post(request, *args, **kwargs)  # Вызов родительского метода post


class LogsListView(LoginRequiredMixin, OwnerQuerysetViewMixin, StatisticMixin, ListView):
    """Список логов"""

    model = Logs
    template_name = "services/logs_list.html"
    extra_context = {"title": "Статистика рассылок"}

    def get_queryset(self):
        return Logs.objects.filter(send_mail__owner=self.request.user)
