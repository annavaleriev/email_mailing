from apscheduler.triggers.cron import CronTrigger
from django.forms import inlineformset_factory

from services.forms import MessageForm, SendMailForm
from services.models import Client, Message, SendMail


class CreateViewMixin:
    """Миксин для создания объекта"""

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class StatisticMixin:
    """Миксин для вывода статистики"""

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        total_sendmail = SendMail.objects.count()
        total_sendmail_is_active = SendMail.objects.filter(is_active=True).count()
        total_clients = Client.objects.count()

        context = {
            "total_sendmail": total_sendmail,
            "total_sendmail_is_active": total_sendmail_is_active,
            "total_clients": total_clients,
        }
        context_data.update(context)
        return context_data


class SendmailOwnerQuerysetViewMixin:
    """Миксин для фильтрации queryset по владельцу рассылки"""

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_superuser or self.request.user.can_disable_sendmail:
            return queryset
        else:
            return queryset.filter(owner=self.request.user)


class ClientOwnerQuerysetViewMixin:
    """Миксин для фильтрации queryset по владельцу клиента"""

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            return queryset
        else:
            return queryset.filter(owner=self.request.user)


class SendMailFormsetMixin:
    """Миксин для работы с формсетом"""

    model = SendMail
    form_class = SendMailForm
    template_name = "services/sendmail_update.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        MessagesFormSet = inlineformset_factory(
            self.model, Message, form=MessageForm, extra=1, max_num=1, can_delete=False
        )  # Создание формсета
        if self.request.POST:
            formset = MessagesFormSet(self.request.POST, instance=self.object)
        else:
            formset = MessagesFormSet(instance=self.object)
        context_data["formset"] = formset
        return context_data

    def create_cron_trigger(self):
        expr = f"{self.object.date_start_send.minute} {self.object.date_start_send.hour} {self.object.periodicity}"

        cron_trigger = CronTrigger.from_crontab(expr=expr)
        cron_trigger.start_date = self.object.date_start_send
        cron_trigger.end_date = self.object.date_end_send

        return cron_trigger

    def form_valid(self, form):  # Переопределение метода form_valid
        context_data = self.get_context_data()  # Получение контекста
        formset = context_data["formset"]  # Получение формсета
        if formset.is_valid() and form.is_valid():  # Если форма и формсет валидны
            form.save()  # Сохранение формы
            formset.save()  # Сохранение формсета
            return super().form_valid(form)  # Вызов родительского метода form_valid
        else:
            return self.render_to_response(self.get_context_data(form=form))  # Возврат страницы с формой и формсетом
