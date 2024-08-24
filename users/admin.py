from django.contrib import admin
from users.models import User


@admin.register(User)  # Регистрируем модель User в админке
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "phone", "is_active")  # Поля для отображения в админке
    exclude = ("password",)
    filter_horizontal = ("groups", "user_permissions")

    actions = ['block_user']  # Добавляем метод block_user в список действий

    def block_user(self, request, queryset):
        """Метод для блокировки пользователя"""
        if not request.user.can_block_user:  # Если у пользователя нет прав
            self.message_user(request, "У вас нет прав для блокировки пользователя", level="error")  # Выводим
            return
        queryset.update(is_active=False)  # Блокируем пользователя
        self.message_user(request, "Пользователь заблокирован")  # Выводим сообщение

    block_user.short_description = "Заблокировать пользователя"  # Название действия в самой админке
