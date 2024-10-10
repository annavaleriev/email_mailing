from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from services.forms import StyleFormMixin
from users.models import User


class CustomUserCreationForm(StyleFormMixin, UserCreationForm):  # Создаем форму для регистрации пользователя
    class Meta:
        model = User
        fields = ("email", "password1", "password2", "first_name", "last_name", "phone", "avatar")


class CustomUserLoginForm(StyleFormMixin, AuthenticationForm):  # Создаем форму для авторизации пользователя
    class Meta:
        model = User
        fields = ("email", "password")
