from django.urls import path

from services.apps import ServicesConfig
from services.views import (ClientCreateView, ClientDeleteView, ClientDetailView, ClientListView, ClientUpdateView,
                            HomeView, SendMailCreateView, SendMailDeleteView, SendMailDetailView, SendMailUpdateView)

app_name = ServicesConfig.name

urlpatterns = [
    path("", HomeView.as_view(), name="home"),  # это ListView
    path("clients/", ClientListView.as_view(), name="client_list"),
    path("clients/<int:pk>/", ClientDetailView.as_view(), name="client_detail"),
    path("add-client/", ClientCreateView.as_view(), name="add_client"),
    path("clients/<int:pk>/update/", ClientUpdateView.as_view(), name="client_update"),
    path("clients/<int:pk>/delete/", ClientDeleteView.as_view(), name="client_delete"),
    path("mailing/", SendMailCreateView.as_view(), name="sendmail_list"),
    path("mailing/<int:pk>/", SendMailDetailView.as_view(), name="sendmail_detail"),
    path("mailing/add/", SendMailCreateView.as_view(), name="add_mailing"),
    path("mailing/<int:pk>/update/", SendMailUpdateView.as_view(), name="sendmail_update"),
    path("mailing/<int:pk>/delete/", SendMailDeleteView.as_view(), name="sendmail_delete"),
]
