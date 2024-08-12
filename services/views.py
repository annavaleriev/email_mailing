from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from services.forms import SendMailForm, AddClientForm, MessageForm
from services.mixins import CreateViewMixin, SendMailFormsetMixin
from services.models import Client, Message, SendMail, Logs


class OwnerQuerysetViewMixin:
    """Миксин для фильтрации queryset по владельцу"""

    def get_queryset(self):
        queryset = super().get_queryset()
        # if self.request.user.is_superuser:
        #     return queryset
        # else:
        return queryset.filter(owner=self.request.user)


class OwnerPermissionMixin:
    """Миксин для проверки прав доступа к объекту"""

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.owner == self.request.user or self.request.user.is_superuser:
            return obj
        else:
            raise PermissionError("У вас нет прав дял работы с этим объектом")


class HomeView(ListView):
    model = SendMail
    template_name = "services/sendmail_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Сервис рассылок"
        context["text"] = "Добро пожаловать на сайт с рассылками"
        return context


class ClientListView(LoginRequiredMixin, OwnerQuerysetViewMixin, ListView):
    """Список клиентов"""
    model = Client
    template_name = "services/client_list.html"
    extra_context = {"title": "Список клиентов"}  # Добавление дополнительного контекста на страницу


class ClientDetailView(LoginRequiredMixin, OwnerQuerysetViewMixin, DetailView):
    model = Client
    template_name = "services/client_detail.html"
    extra_context = {"title": "Информация о клиенте"}


class ClientCreateView(LoginRequiredMixin, CreateViewMixin,  CreateView):
    """Добавление клиента"""
    model = Client
    template_name = "services/client_update.html"
    form_class = AddClientForm
    success_url = reverse_lazy("services:client_list")

    # def form_valid(self, form):  # Переопределение метода form_valid
    #     self.object = form.save(commit=False)  # Сохранение формы, но не в базу данных
    #     self.object.owner = self.request.user  # Присвоение владельца
    #     self.object.save()  # Сохранение объекта
    #     return super().form_valid(form)  # Вызов родительского метода form_valid


class ClientUpdateView(LoginRequiredMixin, OwnerQuerysetViewMixin, OwnerPermissionMixin, UpdateView):
    """Редактирование клиента"""
    model = Client
    template_name = "services/client_update.html"
    form_class = AddClientForm
    context_object_name = "client"  # Переопределение имени объекта в контексте
    success_url = reverse_lazy("services:client_list")

    def get_success_url(self):  # Переопределение метода get_success_url
        return reverse_lazy("services:client_detail",
                            kwargs={"pk": self.object.pk})  # Возврат ссылки на страницу детальной информации о клиенте


class ClientDeleteView(LoginRequiredMixin, OwnerQuerysetViewMixin, OwnerPermissionMixin, DeleteView):
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


class SendMailDetailView(LoginRequiredMixin, OwnerQuerysetViewMixin, OwnerPermissionMixin, DetailView):
    """Информация о рассылке"""
    model = SendMail
    template_name = "services/sendmail_detail.html"
    context_object_name = "sendmail"
    extra_context = {"title": "Информация о рассылке"}


class SendMailCreateView(LoginRequiredMixin, CreateViewMixin, SendMailFormsetMixin, CreateView):
    """Добавление рассылки"""
    model = SendMail
    form_class = SendMailForm
    template_name = "services/sendmail_update.html"
    success_url = reverse_lazy("services:home")

    # def form_valid(self, form):
    #     self.object = form.save(commit=False)
    #     self.object.owner = self.request.user
    #     self.object.save()
    #     return super().form_valid(form)

    # def get_context_data(self, **kwargs):
    #     context_data = super().get_context_data(**kwargs)
    #     MessagesFormSet = inlineformset_factory(self.model, Message, form=MessageForm, extra=1)  # Создание формсета
    #     if self.request.POST:
    #         formset = MessagesFormSet(self.request.POST, instance=self.object)
    #     else:
    #         formset = MessagesFormSet(instance=self.object)
    #     context_data["formset"] = formset
    #     return context_data

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['clients'].queryset = Client.objects.filter(owner=self.request.user)
        return form


class SendMailUpdateView(LoginRequiredMixin, OwnerQuerysetViewMixin, OwnerPermissionMixin, SendMailFormsetMixin, UpdateView):
    """Редактирование рассылки"""
    model = SendMail
    form_class = SendMailForm
    template_name = "services/sendmail_update.html"

    def get_success_url(self):
        return reverse_lazy("services:sendmail_detail", kwargs={"pk": self.object.pk})

    # def get_context_data(self, **kwargs): # Переопределение метода get_context_data
    #     context_data = super().get_context_data(**kwargs) # Вызов родительского метода get_context_data
    #     MessagesFormSet = inlineformset_factory(SendMail, Message, fields='__all__', extra=1) # Создание формсета
    #     if self.request.POST: # Если POST запрос
    #         context_data['formset'] = MessagesFormSet(self.request.POST) # Создание формсета с POST данными
    #     else:
    #         context_data['formset'] = MessagesFormSet() # Создание пустого формсета
    #     return context_data # Возврат контекста

    def form_valid(self, form): # Переопределение метода form_valid
        context_data = self.get_context_data() # Получение контекста
        formset = context_data['formset'] # Получение формсета
        if formset.is_valid() and form.is_valid(): # Если форма и формсет валидны
            self.object = form.save() # Сохранение формы
            formset.instance = self.object # Присвоение формсету объекта
            formset.save() # Сохранение формсета
            return super().form_valid(form) # Вызов родительского метода form_valid
        else:
            return self.render_to_response(self.get_context_data(form=form)) # Возврат страницы с формой и формсетом


class SendMailDeleteView(LoginRequiredMixin, OwnerQuerysetViewMixin, OwnerPermissionMixin, DeleteView):
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