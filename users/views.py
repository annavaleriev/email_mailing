import secrets

from django.contrib import messages
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView

from config.settings import EMAIL_HOST_USER
from users.forms import CustomUserCreationForm
from users.models import User


class UserCreateView(CreateView):
    """Регистрация пользователя"""

    model = User
    form_class = CustomUserCreationForm
    template_name = "user/register.html"
    success_url = reverse_lazy("user:login")

    def form_valid(self, form):
        """Отправка письма с подтверждением почты"""
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/user/email-confirm/{token}/"
        send_mail(
            subject="Подтверждение почты",
            message=f"Для подтверждения перейдите по ссылке {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        messages.info(self.request, message="Для авторизации подтвердите почту и потом залогиньтесь")
        return super().form_valid(form)


def email_verification(request, token):
    """Подтверждение почты"""
    user_permissions = (
        {
            "app_label": "services",
            "model": "client",
            "codename": "view_client",
        },
        {
            "app_label": "services",
            "model": "client",
            "codename": "add_client",
        },
        {
            "app_label": "services",
            "model": "client",
            "codename": "change_client",
        },
        {
            "app_label": "services",
            "model": "client",
            "codename": "delete_client",
        },
        {
            "app_label": "services",
            "model": "sendmail",
            "codename": "add_sendmail",
        },
        {
            "app_label": "services",
            "model": "sendmail",
            "codename": "change_sendmail",
        },
        {
            "app_label": "services",
            "model": "sendmail",
            "codename": "delete_sendmail",
        },
        {
            "app_label": "services",
            "model": "sendmail",
            "codename": "view_sendmail",
        },
        {
            "app_label": "services",
            "model": "Message",
            "codename": "add_message",
        },
        {
            "app_label": "services",
            "model": "Message",
            "codename": "change_message",
        },
        {
            "app_label": "services",
            "model": "Message",
            "codename": "delete_message",
        },
        {
            "app_label": "services",
            "model": "Message",
            "codename": "view_message",
        },
        {
            "app_label": "services",
            "model": "Logs",
            "codename": "view_logs",
        },
        {
            "app_label": "services",
            "model": "Article",
            "codename": "add_article",
        },
        {
            "app_label": "services",
            "model": "Article",
            "codename": "change_article",
        },
        {
            "app_label": "services",
            "model": "Article",
            "codename": "delete_article",
        },
        {
            "app_label": "services",
            "model": "Article",
            "codename": "view_article",
        },
    )

    user = get_object_or_404(User, token=token)
    user.is_active = True
    user_group, created = Group.objects.get_or_create(name="Пользователи")
    if created:
        permissions = [
            Permission.objects.filter(
                content_type=ContentType.objects.get(app_label=perm["app_label"], model=perm["model"]),
                codename=perm["codename"],
            ).first()
            for perm in user_permissions
        ]
        user_group.permissions.set(permissions)
    user.groups.add(user_group)
    user.save()
    return redirect(reverse("user:login"))
