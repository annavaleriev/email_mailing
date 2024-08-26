from django import forms
from django.core.exceptions import ValidationError
from django.forms import BooleanField, DateTimeInput, ModelForm

from services.models import Client, Message, SendMail


class StyleFormMixin:
    """Класс для добавления стилей к формам"""

    def __init__(self, *args, **kwargs):  # переопределяем метод __init__
        super().__init__(*args, **kwargs)  # вызываем родительский метод __init__
        for field_name, field in self.fields.items():  # перебираем все поля формы
            if isinstance(field, BooleanField):  # если поле является BooleanField
                field.widget.attrs["class"] = "form-check-input"  # добавляем класс form-check-input
            else:
                field.widget.attrs["class"] = "form-control"  # добавляем класс form-control


class SendMailForm(StyleFormMixin, ModelForm):
    """Форма для создания рассылки"""

    def __init__(self, *args, **kwargs):  # переопределяем метод __init__
        super().__init__(*args, **kwargs)  # вызываем родительский метод __init__
        for field_name, field in self.fields.items():  # перебираем все поля формы
            if field_name == "status":  # если имя поля равно "status"
                field.disabled = True  # то делаем его неактивным

    def clean_date_end_send(self):  # переопределяем метод clean_date_end_send
        date_start_send = self.cleaned_data["date_start_send"]  # получаем значение поля date_start_send
        date_end_send = self.cleaned_data["date_end_send"]  # получаем значение поля date_end_send
        if date_start_send > date_end_send:  # если дата начала рассылки больше даты окончания рассылки
            raise ValidationError(  # вызываем исключение ValidationError
                "Дата и время первой отправки рассылки должна быть меньше Дата и время завершения рассылки"
            )  # возвращаем сообщение об ошибке
        return date_end_send  # возвращаем значение поля date_end_send

    class Meta:
        model = SendMail
        fields = ["is_active", "date_start_send", "date_end_send", "periodicity", "status", "clients"]
        widgets = {  # добавляем виджеты для полей формы
            "date_start_send": DateTimeInput(format=("%Y-%m-%dT%H:%M"), attrs={"type": "datetime-local"}),
            "date_end_send": DateTimeInput(format=("%Y-%m-%dT%H:%M"), attrs={"type": "datetime-local"}),
            # добавляем виджет для поля date_start_send
        }


class AddClientForm(StyleFormMixin, ModelForm):
    """Форма для добавления клиента"""

    class Meta:
        model = Client
        exclude = ("owner",)  # исключаем поле owner из формы


class MessageForm(StyleFormMixin, ModelForm):
    """Форма для создания сообщения"""

    class Meta:
        model = Message
        fields = "__all__"  # добавляем все поля модели
        widgets = {  # добавляем виджеты для полей формы
            "body": forms.Textarea(attrs={"rows": 5}),
        }
