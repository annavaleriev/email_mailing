import secrets

from django.contrib import messages
from django.contrib.auth.decorators import permission_required
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
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("user:login"))


# @permission_required('users.block_user')
# def block_user(request, user_id):
#     """Блокировка пользователя"""
#     user = get_object_or_404(User, id=user_id)
#     if not user.is_staff and not user.is_superuser:
#         user.is_active = False
#         user.save()
#         messages.success(request, f"Пользователь {user.first_name} {user.last_name} {user.email} заблокирован")
#     else:
#         messages.error(request, "Нельзя заблокировать сотрудника или админа")
#     return redirect("services:client_list")
#
#
# @permission_required('users.block_user') # Декоратор для проверки прав доступа
# def unblock_user(request, user_id):
#     """Разблокировка пользователя"""
#     user = get_object_or_404(User, id=user_id)
#     if not user.is_staff and not user.is_superuser:
#         user.is_active = True
#         user.save()
#         messages.success(request, f"Пользователь {user.first_name} {user.last_name} {user.email} разблокирован")
#     else:
#         messages.error(request, "Нельзя разблокировать пользователя")
#     return redirect("services:client_list")
