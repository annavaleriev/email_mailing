from django.contrib import admin

from users.models import User


@admin.register(User)  # Регистрируем модель User в админке
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "phone")  # Поля для отображения в админке
