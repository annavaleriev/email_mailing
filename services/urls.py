from django.urls import path

from services.apps import ServicesConfig
from services.forms import AddClientForm
from services.views import (ClientCreateView, ClientDeleteView, ClientDetailView, ClientListView, ClientUpdateView,
                            HomeView, AddMailingView)

app_name = ServicesConfig.name
# app_name = 'services'


urlpatterns = [
    path("", HomeView.as_view(), name="home"),  # это ListView
    path("add-mailing/", AddMailingView.as_view(), name="add_mailing"),
    path("add-client/", AddClientForm.as_view(), name="add_client"),
]
    # path("<int:pk>/", ClientDetailView.as_view(), name="client_detail"), # это DetailView конкретретного клиента
    # path("create/", ClientCreateView.as_view(), name="client_create"), # это CreateView
    # path("update/<int:pk>/", ClientUpdateView.as_view(), name="client_update"), # это UpdateView
    # path("delete/<int:pk>/", ClientDeleteView.as_view(), name="client_delete"), # это DeleteView

