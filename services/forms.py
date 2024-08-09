from django import forms
from django.forms import BooleanField, ModelForm, DateTimeInput, CheckboxSelectMultiple

from services.models import SendMail, Client, Message


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

    class Meta:
        model = SendMail
        fields = ['date_start_send', 'periodicity', 'status', 'clients']
        widgets = {  # добавляем виджеты для полей формы
            "date_start_send": DateTimeInput(attrs={"type": "datetime-local"}),
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
