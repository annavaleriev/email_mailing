from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import HiddenInput
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from services.forms import AddClientForm, SendMailForm
from services.mixins import CreateViewMixin, SendMailFormsetMixin, OwnerQuerysetViewMixin
from services.models import Client, Logs, SendMail


class ClientListView(LoginRequiredMixin, OwnerQuerysetViewMixin, ListView):
    """Список клиентов"""

    model = Client
    template_name = "services/client_list.html"
    extra_context = {"title": "Список клиентов"}  # Добавление дополнительного контекста на страницу


class ClientDetailView(LoginRequiredMixin, OwnerQuerysetViewMixin, DetailView):
    model = Client
    template_name = "services/client_detail.html"
    extra_context = {"title": "Информация о клиенте"}


class ClientCreateView(LoginRequiredMixin, CreateViewMixin, CreateView):
    """Добавление клиента"""

    model = Client
    template_name = "services/client_update.html"
    form_class = AddClientForm
    success_url = reverse_lazy("services:client_list")


class ClientUpdateView(LoginRequiredMixin, OwnerQuerysetViewMixin, UpdateView):
    """Редактирование клиента"""

    model = Client
    template_name = "services/client_update.html"
    form_class = AddClientForm
    context_object_name = "client"  # Переопределение имени объекта в контексте

    def get_success_url(self):  # Переопределение метода get_success_url
        return reverse_lazy(
            "services:client_detail", kwargs={"pk": self.object.pk}
        )  # Возврат ссылки на страницу детальной информации о клиенте


class ClientDeleteView(LoginRequiredMixin, OwnerQuerysetViewMixin, DeleteView):
    """Удаление клиента"""

    model = Client
    template_name = "services/client_delete.html"
    context_object_name = "client"
    success_url = reverse_lazy("services:client_list")


class SendMailListView(LoginRequiredMixin, OwnerQuerysetViewMixin, ListView):
    """Список рассылок"""

    model = SendMail
    template_name = "services/sendmail_list.html"
    form_class = SendMailForm
    extra_context = {"title": "Список рассылок"}


class SendMailDetailView(LoginRequiredMixin, OwnerQuerysetViewMixin, DetailView):
    """Информация о рассылке"""

    model = SendMail
    template_name = "services/sendmail_detail.html"
    context_object_name = "sendmail"
    extra_context = {"title": "Информация о рассылке"}


class SendMailCreateView(LoginRequiredMixin, CreateViewMixin, SendMailFormsetMixin, CreateView):
    """Добавление рассылки"""

    success_url = reverse_lazy("services:home")

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields["clients"].queryset = Client.objects.filter(owner=self.request.user)
        return form


class SendMailUpdateView(
    LoginRequiredMixin, OwnerQuerysetViewMixin, SendMailFormsetMixin, UpdateView
):
    """Редактирование рассылки"""

    def get_form(self, form_class=None):
        form_class = super().get_form(form_class)
        if self.request.user.id == 2:  # прописать условия для супер и менеджера
            form_class.base_fields["is_active"].widget = HiddenInput()
        return form_class

    def get_success_url(self):
        return reverse_lazy("services:sendmail_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):  # Переопределение метода form_valid
        context_data = self.get_context_data()  # Получение контекста
        formset = context_data["formset"]  # Получение формсета
        if formset.is_valid() and form.is_valid():  # Если форма и формсет валидны
            self.object = form.save()  # Сохранение формы
            formset.instance = self.object  # Присвоение формсету объекта
            formset.save()  # Сохранение формсета
            return super().form_valid(form)  # Вызов родительского метода form_valid
        else:
            return self.render_to_response(self.get_context_data(form=form))  # Возврат страницы с формой и формсетом


class SendMailDeleteView(LoginRequiredMixin, OwnerQuerysetViewMixin, DeleteView):
    """Удаление рассылки"""

    model = SendMail
    template_name = "services/sendmail_delete.html"
    success_url = reverse_lazy("services:sendmail_list")


class LogsListView(LoginRequiredMixin, OwnerQuerysetViewMixin, ListView):
    """Список логов"""

    model = Logs
    extra_context = {"title": "Список логов"}

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_superuser:
            context_data["logs"] = Logs.objects.all()
        else:
            context_data["logs"] = Logs.objects.filter(sendmail__owner=user)


# class MessageListView(ListView):
#     model = Message
#     template_name = "services/message_list.html"
#     context_object_name = "message"
