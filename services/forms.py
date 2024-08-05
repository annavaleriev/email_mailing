from django import forms
from django.forms import BooleanField, ModelForm, DateTimeInput, CheckboxSelectMultiple

from services.models import SendMail, Client


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
        fields = ['date_start_send', 'periodicity', 'status', 'message', 'clients']
        widgets = { # добавляем виджеты для полей формы
            "date_start_send": DateTimeInput(attrs={"type": "datetime-local"}),
        }


class AddClientForm(StyleFormMixin, ModelForm):
    """Форма для добавления клиента"""

    class Meta:
        model = Client
        fields = "__all__"
