from apscheduler.triggers.cron import CronTrigger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import HiddenInput
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from services import scheduler
from services.forms import AddClientForm, SendMailForm
from services.mailing_job import my_job
from services.mixins import CreateViewMixin, SendMailFormsetMixin, StatisticMixin, ClientOwnerQuerysetViewMixin, \
    SendmailOwnerQuerysetViewMixin
from services.models import Client, Logs, SendMail


class ClientListView(LoginRequiredMixin, ClientOwnerQuerysetViewMixin, StatisticMixin, ListView):
    """Список клиентов"""

    model = Client
    template_name = "services/client_list.html"
    extra_context = {"title": "Список клиентов"}  # Добавление дополнительного контекста на страницу


class ClientDetailView(LoginRequiredMixin, ClientOwnerQuerysetViewMixin, StatisticMixin, DetailView):
    model = Client
    template_name = "services/client_detail.html"
    extra_context = {"title": "Информация о клиенте"}


class ClientCreateView(LoginRequiredMixin, CreateViewMixin, StatisticMixin, CreateView):
    """Добавление клиента"""

    model = Client
    template_name = "services/client_update.html"
    form_class = AddClientForm
    success_url = reverse_lazy("services:client_list")


class ClientUpdateView(LoginRequiredMixin, ClientOwnerQuerysetViewMixin, StatisticMixin, UpdateView):
    """Редактирование клиента"""

    model = Client
    template_name = "services/client_update.html"
    form_class = AddClientForm
    context_object_name = "client"  # Переопределение имени объекта в контексте

    def get_success_url(self):  # Переопределение метода get_success_url
        return reverse_lazy(
            "services:client_detail", kwargs={"pk": self.object.pk}
        )  # Возврат ссылки на страницу детальной информации о клиенте


class ClientDeleteView(LoginRequiredMixin, ClientOwnerQuerysetViewMixin, StatisticMixin, DeleteView):
    """Удаление клиента"""

    model = Client
    template_name = "services/client_delete.html"
    context_object_name = "client"
    success_url = reverse_lazy("services:client_list")


class SendMailListView(LoginRequiredMixin, SendmailOwnerQuerysetViewMixin, StatisticMixin, ListView):
    """Список рассылок"""

    model = SendMail
    template_name = "services/sendmail_list.html"
    form_class = SendMailForm
    extra_context = {"title": "Список рассылок"}

    # def sendmail_list_view(request):
    #     # Проверяем, принадлежит ли текущий пользователь к группе "Manager"
    #     is_manager = request.user.groups.filter(name='Manager').exists()
    #
    #     # Получаем список рассылок (например, все)
    #     object_list = SendMail.objects.all()
    #
    #     # Передаем переменную is_manager в шаблон
    #     return render(request, 'services/sendmail_list.html', {
    #         'object_list': object_list,
    #         'is_manager': is_manager
    #     })


class SendMailDetailView(LoginRequiredMixin, SendmailOwnerQuerysetViewMixin, StatisticMixin, DetailView):
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
        cron_trigger = self.create_cron_trigger()

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


class SendMailUpdateView(LoginRequiredMixin, SendmailOwnerQuerysetViewMixin, SendMailFormsetMixin, StatisticMixin,
                         UpdateView):
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

    def post(self, request, *args, **kwargs):
        send_mail = super().post(request, *args, **kwargs)
        cron_trigger = self.create_cron_trigger()

        scheduler.reschedule_job(str(self.object.pk), trigger=cron_trigger)
        return send_mail


class SendMailDeleteView(LoginRequiredMixin, SendmailOwnerQuerysetViewMixin, StatisticMixin, DeleteView):
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


class LogsListView(LoginRequiredMixin, SendmailOwnerQuerysetViewMixin, StatisticMixin, ListView):
    """Список логов"""

    model = Logs
    template_name = "services/logs_list.html"
    extra_context = {"title": "Статистика рассылок"}

    def get_queryset(self):
        return Logs.objects.filter(send_mail__owner=self.request.user)
