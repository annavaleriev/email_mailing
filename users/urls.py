from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import UserCreateView, email_verification

app_name = UsersConfig.name

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", LoginView.as_view(template_name="user/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", UserCreateView.as_view(), name="register"),
    path("email-confirm/<str:token>/", email_verification, name="email_confirm"),
    # path('block-user/<int:user_id>/', block_user, name='block_user'),
    # path('unblock-user/<int:user_id>/', unblock_user, name='unblock_user'),
]
