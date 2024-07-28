# from django.contrib.auth.forms import BaseUserCreationForm, UserChangeForm
#
# from catalog.forms import StyleFormMixin
# from user.models import User
#
#
# class RegisterForm(StyleFormMixin, BaseUserCreationForm):
#     class Meta:
#         model = User
#         fields = ("email",)
#
#
# class ChangeUserForm(StyleFormMixin, UserChangeForm):
#     password = None
#
#     class Meta:
#         model = User
#         fields = ("phone", "avatar", "country", "first_name", "last_name")
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from users.models import User


class CustomUserCreationForm(UserCreationForm):  # Создаем форму для регистрации пользователя
    class Meta:
        model = User
        fields = ("email", "password1", "password2", "first_name", "last_name ", "phone", "avatar")


class CustomUserLoginForm(AuthenticationForm):  # Создаем форму для авторизации пользователя
    class Meta:
        model = User
        fields = ("email", "password")
