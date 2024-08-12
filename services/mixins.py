from django.forms import inlineformset_factory

from services.forms import MessageForm, SendMailForm
from services.models import Message, SendMail


class CreateViewMixin:
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class OwnerQuerysetViewMixin:
    """Миксин для фильтрации queryset по владельцу"""

    def get_queryset(self):
        queryset = super().get_queryset()
        # if self.request.user.is_superuser:
        #     return queryset
        # else:
        return queryset.filter(owner=self.request.user)


class SendMailFormsetMixin:
    model = SendMail
    form_class = SendMailForm
    template_name = "services/sendmail_update.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        MessagesFormSet = inlineformset_factory(
            self.model,
            Message,
            form=MessageForm,
            extra=1,
            max_num=1,
            can_delete=False
        )  # Создание формсета
        if self.request.POST:
            formset = MessagesFormSet(self.request.POST, instance=self.object)
        else:
            formset = MessagesFormSet(instance=self.object)
        context_data["formset"] = formset
        return context_data
