from django.forms import BooleanField


class StyleFormMixin:
    """Класс для добавления стилей к формам"""

    def __init__(self, *args, **kwargs):  # переопределяем метод __init__
        super().__init__(*args, **kwargs)  # вызываем родительский метод __init__
        for field_name, field in self.fields.items():  # перебираем все поля формы
            if isinstance(field, BooleanField):  # если поле является BooleanField
                field.widget.attrs["class"] = "form-check-input"  # добавляем класс form-check-input
            else:
                field.widget.attrs["class"] = "form-control"  # добавляем класс form-control
