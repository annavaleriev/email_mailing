from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from services.forms import SendMailForm, AddClientForm
from services.models import Client, Message


# ТУТ ЕЩЕ ЧТО-ТО С КОНТАКСТОМ ДОЛЖНО БЫТЬ, СМОТРИ ПРЕД ДЗ
class HomeView(ListView):
    model = Message
    template_name = "services/home.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Сервис рассылок"
        context["text"] = "Добро пожаловать на сайт с рассылками"
        return context


class ClientListView(ListView):
    model = Client
    template_name = "services/client_list.html"
    context_object_name = "clients"


class ClientDetailView(DetailView):
    model = Client
    template_name = "services/client_detail.html"
    context_object_name = "client"


class ClientCreateView(CreateView):
    model = Client
    template_name = "services/client_create.html"
    fields = "__all__"
    success_url = reverse_lazy("services:client_list")


class ClientUpdateView(UpdateView):
    model = Client
    template_name = "services/client_update.html"
    fields = "__all__"
    context_object_name = "client"
    success_url = reverse_lazy("services:client_list")


class ClientDeleteView(DeleteView):
    model = Client
    template_name = "services/client_delete.html"
    context_object_name = "client"
    success_url = reverse_lazy("services:client_list")


# class MessageListView(ListView):
#     model = Message
#     template_name = "services/message_list.html"
#     context_object_name = "message"

class AddMailingView(CreateView):
    model = Message
    form_class = SendMailForm
    template_name = "services/add_mailing.html"
    # fields = "__all__"
    success_url = reverse_lazy("services:home")


class AddClientView(CreateView):
    model = Client
    form_class = AddClientForm
    template_name = "services/add_client.html"
    # fields = "__all__"
    success_url = reverse_lazy("client_list")
